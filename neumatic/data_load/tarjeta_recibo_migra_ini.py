# neumatic\data_load\tarjeta_recibo_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from django.db import transaction
from datetime import date, datetime
from decimal import Decimal

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.recibo_models import TarjetaRecibo
from apps.ventas.models.factura_models import Factura
from apps.maestros.models.base_models import Tarjeta
from apps.ventas.models.caja_models import Caja

# Configuración de logging
logging.basicConfig(
    filename='tarjeta_recibo_migra.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def safe_int(value, default=0):
    """Conversión segura a entero"""
    try:
        if value is None:
            return default
        str_val = str(value).strip()
        if not str_val:
            return default
        return int(float(str_val))
    except (ValueError, TypeError):
        return default

def safe_small_int(value, default=None):
    """Conversión segura a SmallInteger"""
    try:
        if value is None or str(value).strip() == '':
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default

def safe_decimal(value, default=0.0):
    """Conversión segura a Decimal"""
    try:
        if value is not None and str(value).strip():
            return Decimal(str(value))
        return Decimal(str(default))
    except (ValueError, TypeError):
        return Decimal(str(default))

def reset_tarjeta_recibo():
    """Elimina los datos existentes de manera controlada"""
    try:
        print("<info>Iniciando reset de TarjetaRecibo...</info>")
        with transaction.atomic():
            count = TarjetaRecibo.objects.count()
            TarjetaRecibo.objects.all().delete()
            logger.info(f"Eliminados {count} registros existentes de TarjetaRecibo")
            print(f"<info>Eliminados {count} registros existentes de TarjetaRecibo</info>")
            
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='tarjeta_recibo';")
            elif 'postgresql' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("ALTER SEQUENCE tarjeta_recibo_id_tarjeta_recibo_seq RESTART WITH 1;")
        print("<info>Reset de TarjetaRecibo completado</info>")
    except Exception as e:
        logger.error(f"Error en reset_tarjeta_recibo: {e}")
        print(f"<error>ERROR en reset_tarjeta_recibo: {e}</error>")
        raise

def cargar_datos_tarjeta_recibo():
    """Migración optimizada de cuponestarj.DBF a modelo TarjetaRecibo"""
    try:
        start_time = time.time()
        
        print("<info>Iniciando migración de TarjetaRecibo...</info>")
        reset_tarjeta_recibo()

        # Precargar caches
        print("<info>Cargando cachés...</info>")
        
        cajas_cache = {}
        for caja in Caja.objects.all():
            if caja.numero_caja:
                cajas_cache[caja.numero_caja] = caja
        print(f"<info>Cargadas {len(cajas_cache)} cajas en caché</info>")
        
        facturas_cache = {}
        for factura in Factura.objects.all():
            if factura.compro and factura.numero_comprobante:
                compro_limpio = str(factura.compro).strip().upper()
                clave = f"{compro_limpio}_{factura.numero_comprobante}"
                facturas_cache[clave] = factura
        
        print(f"<info>Cargadas {len(facturas_cache)} facturas en caché</info>")
        
        tarjetas_cache = {tarjeta.id_tarjeta: tarjeta for tarjeta in Tarjeta.objects.all()}
        print(f"<info>Cargadas {len(tarjetas_cache)} tarjetas en caché</info>")

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'cuponestarj.DBF')
        print(f"<info>Procesando archivo: {dbf_path}</info>")
        
        table = DBF(dbf_path, encoding='latin-1')
        total_records = len(table)
        print(f"<info>Total de registros en DBF: {total_records}</info>")
        
        # Procesamiento
        batch_size = 5000
        tarjetas_batch = []
        facturas_actualizadas = []
        registros_procesados = 0
        registros_validos = 0
        total_regs = 0
        errores = 0
        facturas_no_encontradas = 0
        cajas_no_encontradas = 0
        tarjetas_no_encontradas = 0
        facturas_actualizadas_count = 0
        tarjetas_con_factura = 0

        for idx, record in enumerate(table, 1):
            try:
                # ============================================
                # 1. OBTENER DATOS BÁSICOS (SIEMPRE)
                # ============================================
                # Obtener tarjeta (campo obligatorio para TarjetaRecibo)
                tarjeta_raw = record.get('TARJETA')
                id_tarjeta_instancia = None
                tarjeta_id = safe_int(tarjeta_raw)
                
                if tarjeta_id:
                    id_tarjeta_instancia = tarjetas_cache.get(tarjeta_id)
                    if not id_tarjeta_instancia:
                        tarjetas_no_encontradas += 1
                
                # Obtener otros campos del TarjetaRecibo (requeridos)
                cupon = safe_small_int(record.get('CUPON'))
                lote = safe_small_int(record.get('LOTE'))
                cuotas = safe_small_int(record.get('CUOTAS'))
                importe_raw = record.get('IMPORTE')
                importe_tarjeta = safe_decimal(importe_raw)
                
                # ============================================
                # 2. VERIFICAR DATOS MÍNIMOS PARA TARJETA RECIBO
                # ============================================
                # Necesitamos al menos: tarjeta Y (cupon O importe)
                datos_minimos = (id_tarjeta_instancia is not None) and (cupon is not None or importe_tarjeta > 0)
                
                if not datos_minimos:
                    # No tenemos datos suficientes, omitir registro
                    if idx <= 10:
                        print(f"<warning>Registro {idx}: Datos insuficientes. Tarjeta: {tarjeta_id}, Cupón: {cupon}, Importe: {importe_tarjeta}</warning>")
                    continue
                
                # ============================================
                # 3. BUSCAR FACTURA (OPCIONAL - para asociar y actualizar)
                # ============================================
                id_factura_instancia = None
                
                # Buscar campos de factura (pueden estar truncados)
                comproing_raw = None
                nrocomproing_raw = None
                
                posibles_compro = ['COMPROING', 'COMPROIN', 'COMPROI', 'COMPRO', 'COMPR', 'COMP']
                for campo in posibles_compro:
                    if campo in record:
                        comproing_raw = record.get(campo)
                        break
                
                posibles_nrocompro = ['NROCOMPROIN', 'NROCOMPROI', 'NROCOMPRO', 'NROCOMPR', 'NROCOMP', 'NROCOM']
                for campo in posibles_nrocompro:
                    if campo in record:
                        nrocomproing_raw = record.get(campo)
                        break
                
                # Obtener caja para factura
                caja_raw = record.get('CAJA')
                caja_numero = safe_int(caja_raw)
                
                # Si tenemos datos de factura, intentar buscarla
                if comproing_raw is not None and nrocomproing_raw is not None and caja_numero:
                    comproing = str(comproing_raw).strip().upper()
                    nrocomproing = safe_int(nrocomproing_raw)
                    
                    if comproing and nrocomproing:
                        clave = f"{comproing}_{nrocomproing}"
                        
                        if clave in facturas_cache:
                            factura_encontrada = facturas_cache[clave]
                            id_factura_instancia = factura_encontrada
                            tarjetas_con_factura += 1
                            
                            # Actualizar factura con caja
                            caja_obj = cajas_cache.get(caja_numero)
                            if caja_obj:
                                if factura_encontrada.id_caja_id != caja_obj.id_caja:
                                    factura_encontrada.id_caja = caja_obj
                                    facturas_actualizadas.append(factura_encontrada)
                                    facturas_actualizadas_count += 1
                            else:
                                cajas_no_encontradas += 1
                        else:
                            facturas_no_encontradas += 1
                
                # ============================================
                # 4. CREAR TARJETA RECIBO (SIEMPRE si tenemos datos mínimos)
                # ============================================
                # Verificar duplicados (opcional, para eficiencia)
                crear_registro = True
                
                # Filtro básico para duplicados
                filtro = {
                    'id_tarjeta': id_tarjeta_instancia,
                    'cupon': cupon,
                    'importe_tarjeta': importe_tarjeta,
                }
                
                if id_factura_instancia:
                    filtro['id_factura'] = id_factura_instancia
                
                # Solo verificar duplicados si tenemos todos los campos del filtro
                if all(v is not None for v in [id_tarjeta_instancia, cupon, importe_tarjeta]):
                    existe = TarjetaRecibo.objects.filter(**filtro).exists()
                    crear_registro = not existe
                
                if crear_registro:
                    tarjeta_recibo = TarjetaRecibo(
                        id_factura=id_factura_instancia,  # Puede ser None
                        id_tarjeta=id_tarjeta_instancia,  # Debe tener valor
                        cupon=cupon,
                        lote=lote,
                        cuotas=cuotas,
                        importe_tarjeta=importe_tarjeta
                    )
                    
                    tarjetas_batch.append(tarjeta_recibo)
                    registros_validos += 1
                    
                    # Debug primeros registros
                    if registros_validos <= 10:
                        factura_info = f"con factura {id_factura_instancia.id_factura}" if id_factura_instancia else "sin factura"
                        print(f"<success>✓ TarjetaRecibo #{registros_validos}: Tarjeta {tarjeta_id}, Cupón {cupon}, {factura_info}</success>")
                else:
                    # Duplicado, omitir
                    pass
                
                registros_procesados += 1

                # Mostrar progreso
                if registros_procesados % 5000 == 0:
                    print(f"<info>Procesados: {registros_procesados}/{total_records} | Válidos: {registros_validos} | Con factura: {tarjetas_con_factura}</info>")

                # Guardar lotes
                if len(tarjetas_batch) >= batch_size:
                    with transaction.atomic():
                        TarjetaRecibo.objects.bulk_create(tarjetas_batch)
                        print(f"<success>✅ Lote guardado: {len(tarjetas_batch)} registros</success>")
                        total_regs += len(tarjetas_batch)
                        tarjetas_batch = []
                
                if len(facturas_actualizadas) >= 1000:  # Lote más pequeño para actualizaciones
                    with transaction.atomic():
                        Factura.objects.bulk_update(facturas_actualizadas, ['id_caja'])
                        print(f"<success>✅ Facturas actualizadas: {len(facturas_actualizadas)}</success>")
                        facturas_actualizadas = []

            except Exception as e:
                errores += 1
                if errores <= 10:
                    print(f"<error>Error en registro {idx}: {str(e)}</error>")
                continue

        # Guardar últimos registros
        if tarjetas_batch:
            with transaction.atomic():
                TarjetaRecibo.objects.bulk_create(tarjetas_batch)
                print(f"<success>✅ Último lote: {len(tarjetas_batch)} registros</success>")
                total_regs += len(tarjetas_batch)
        
        if facturas_actualizadas:
            with transaction.atomic():
                Factura.objects.bulk_update(facturas_actualizadas, ['id_caja'])
                print(f"<success>✅ Últimas facturas: {len(facturas_actualizadas)} actualizadas</success>")

        # Resultados finales
        elapsed_time = time.time() - start_time
        
        print(f"\n<info>{'='*60}</info>")
        print("<info>RESUMEN FINAL</info>")
        print(f"<info>{'='*60}</info>")
        print(f"<info>Total registros en DBF: {total_records}</info>")
        print(f"<info>Registros procesados: {registros_procesados}</info>")
        print(f"\n<success>Tarjetas Recibo creadas: {registros_validos}</success>")
        print(f"<success>Tarjetas con factura asociada: {tarjetas_con_factura}</success>")
        print(f"<success>Facturas actualizadas con caja: {facturas_actualizadas_count}</success>")
        print(f"\n<warning>Registros omitidos (datos insuficientes): {total_records - registros_procesados}</warning>")
        print(f"<warning>Facturas no encontradas: {facturas_no_encontradas}</warning>")
        print(f"<warning>Cajas no encontradas: {cajas_no_encontradas}</warning>")
        print(f"<warning>Tarjetas no encontradas: {tarjetas_no_encontradas}</warning>")
        print(f"\n<error>Errores encontrados: {errores}</error>")
        print(f"\n<info>Tiempo total: {elapsed_time:.2f} segundos</info>")
        
        # Verificar BD
        try:
            total_final = TarjetaRecibo.objects.count()
            print(f"\n<info>Total en BD TarjetaRecibo: {total_final}</info>")
            
            if total_regs != total_final:
                print(f"<warning>⚠️  Diferencia: guardados={total_regs}, BD={total_final}</warning>")
            
            if total_final > 0:
                print(f"\n<info>=== ESTADÍSTICAS BD ===</info>")
                con_factura = TarjetaRecibo.objects.filter(id_factura__isnull=False).count()
                sin_factura = TarjetaRecibo.objects.filter(id_factura__isnull=True).count()
                print(f"<info>Con factura: {con_factura} ({con_factura/total_final*100:.1f}%)</info>")
                print(f"<info>Sin factura: {sin_factura} ({sin_factura/total_final*100:.1f}%)</info>")
                
        except Exception as e:
            print(f"\n<error>Error al verificar BD: {e}</error>")

    except Exception as e:
        logger.error(f"Error fatal: {str(e)}")
        print(f"<error>ERROR FATAL: {str(e)}</error>")
        raise

if __name__ == '__main__':
    cargar_datos_tarjeta_recibo()
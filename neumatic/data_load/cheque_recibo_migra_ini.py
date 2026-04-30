# neumatic\data_load\cheque_recibo_migra.py
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

from apps.ventas.models.recibo_models import ChequeRecibo
from apps.ventas.models.factura_models import Factura
from apps.maestros.models.base_models import Banco
from apps.ventas.models.caja_models import Caja

# Configuración de logging
logging.basicConfig(
    filename='cheque_recibo_migra.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def safe_int(value, default=0):
    """Conversión segura a entero"""
    try:
        return int(float(value)) if value is not None and str(value).strip() else default
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

def safe_date(value, default=None):
    """Conversión segura para fechas de DBF"""
    try:
        if value and isinstance(value, (date, datetime)):
            return value
        elif value and str(value).strip():
            if isinstance(value, str):
                for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y'):
                    try:
                        return datetime.strptime(value, fmt).date()
                    except ValueError:
                        continue
            return default
        return default
    except (ValueError, TypeError):
        return default

def safe_bool(value, default=False):
    """Conversión segura a booleano"""
    try:
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            value = value.upper().strip()
            return value in ['T', 'TRUE', '1', 'S', 'SI', 'Y', 'YES', 'V']
        return default
    except (ValueError, TypeError):
        return default

def reset_cheque_recibo():
    """Elimina los datos existentes de manera controlada"""
    try:
        print("<info>Iniciando reset de ChequeRecibo...</info>")
        with transaction.atomic():
            count = ChequeRecibo.objects.count()
            ChequeRecibo.objects.all().delete()
            logger.info(f"Eliminados {count} registros existentes de ChequeRecibo")
            print(f"<info>Eliminados {count} registros existentes de ChequeRecibo</info>")
            
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='cheque_recibo';")
            elif 'postgresql' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("ALTER SEQUENCE cheque_recibo_id_cheque_recibo_seq RESTART WITH 1;")
        print("<info>Reset de ChequeRecibo completado</info>")
    except Exception as e:
        logger.error(f"Error en reset_cheque_recibo: {e}")
        print(f"<error>ERROR en reset_cheque_recibo: {e}</error>")
        raise

def cargar_datos_cheque_recibo():
    """Migración optimizada de cheques.DBF a modelo ChequeRecibo"""
    try:
        start_time = time.time()
        
        print("<info>Iniciando migración de ChequeRecibo...</info>")
        reset_cheque_recibo()

        # Precargar caches para optimización
        print("<info>Cargando cachés...</info>")
        
        # Cache de cajas por numero_caja para asignar a facturas
        cajas_cache = {}
        for caja in Caja.objects.all():
            if caja.numero_caja:
                cajas_cache[caja.numero_caja] = caja
        print(f"<info>Cargadas {len(cajas_cache)} cajas en caché</info>")
        
        # Cache de facturas por compro + numero_comprobante para búsqueda rápida
        facturas_cache = {}
        for factura in Factura.objects.all():
            if factura.compro and factura.numero_comprobante:
                # Limpiar y normalizar compro (puede tener espacios)
                compro_limpio = str(factura.compro).strip().upper()
                clave = f"{compro_limpio}_{factura.numero_comprobante}"
                facturas_cache[clave] = factura
        
        print(f"<info>Cargadas {len(facturas_cache)} facturas en caché</info>")
        
        # Cache de bancos por id_banco
        bancos_cache = {banco.id_banco: banco for banco in Banco.objects.all()}
        print(f"<info>Cargados {len(bancos_cache)} bancos en caché</info>")

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'cheques.DBF')
        print(f"<info>Procesando archivo: {dbf_path}</info>")
        
        table = DBF(dbf_path, encoding='latin-1')
        total_records = len(table)
        print(f"<info>Total de registros en DBF: {total_records}</info>")
        
        # Mostrar estructura del DBF (solo campos importantes)
        print("\n<info>=== CAMPOS IMPORTANTES DEL DBF ===</info>")
        campos_importantes = ['IDCHEQUE', 'CAJA', 'CODBCO', 'SUCURSAL', 'LOCALIDAD', 
                            'NUMERO', 'CUENTA', 'CUIT', 'FECHA', 'IMPORTE', 
                            'COMPROING', 'NROCOMPROING', 'ELECTRONIC']
        
        # Verificar qué campos realmente existen en el DBF
        print("<info>Campos disponibles en el DBF (primeros 15):</info>")
        for i, field in enumerate(table.fields[:15]):
            print(f"  <info>{field.name:15} | Tipo: {field.type} | Tamaño: {field.length}</info>")
        
        # Crear archivo para facturas no encontradas
        archivo_no_encontradas = os.path.join(BASE_DIR, 'data_load', 'facturas_sin_caja.txt')
        with open(archivo_no_encontradas, 'w', encoding='utf-8') as f:
            f.write("COMPROING\tNROCOMPROING\tCAJA\tRAZÓN\n")
        
        # Procesamiento por lotes
        batch_size = 5000
        cheques_batch = []
        facturas_actualizadas = []
        registros_procesados = 0
        registros_validos = 0
        total_regs = 0
        errores = 0
        facturas_no_encontradas = 0
        cajas_no_encontradas = 0
        bancos_no_encontrados = 0
        facturas_actualizadas_count = 0
        cheques_con_factura = 0

        for idx, record in enumerate(table, 1):
            try:
                # DEBUG: Mostrar primeros registros para ver estructura
                if idx <= 5:
                    print(f"\n<debug>=== REGISTRO {idx} (DEBUG) ===</debug>")
                    print(f"<debug>Campos disponibles: {list(record.keys())[:10]}...</debug>")
                    print(f"<debug>COMPROING campo: {record.get('COMPROING')} (tipo: {type(record.get('COMPROING')).__name__})</debug>")
                    print(f"<debug>NROCOMPROING campo: {record.get('NROCOMPROING')} (tipo: {type(record.get('NROCOMPROING')).__name__})</debug>")
                    print(f"<debug>CAJA campo: {record.get('CAJA')} (tipo: {type(record.get('CAJA')).__name__})</debug>")
                
                # ============================================
                # 1. OBTENER DATOS PARA BUSCAR/ACTUALIZAR FACTURA
                # ============================================
                comproing_raw = None
                nrocomproing_raw = None
                
                # Buscar campo COMPROING (puede estar truncado a 10 chars)
                posibles_compro = ['COMPROING', 'COMPROIN', 'COMPROI', 'COMPRO', 'COMPR', 'COMP']
                for campo in posibles_compro:
                    if campo in record:
                        comproing_raw = record.get(campo)
                        if idx <= 5:
                            print(f"<debug>Encontrado campo '{campo}': {comproing_raw}</debug>")
                        break
                
                # Buscar campo NROCOMPROING (puede estar truncado a 10 chars)
                posibles_nrocompro = ['NROCOMPROIN', 'NROCOMPROI', 'NROCOMPRO', 'NROCOMPR', 'NROCOMP', 'NROCOM']
                for campo in posibles_nrocompro:
                    if campo in record:
                        nrocomproing_raw = record.get(campo)
                        if idx <= 5:
                            print(f"<debug>Encontrado campo '{campo}': {nrocomproing_raw}</debug>")
                        break
                
                # Obtener número de caja para asignar a la factura
                caja_raw = record.get('CAJA')
                caja_numero = safe_int(caja_raw)
                
                # ============================================
                # 2. BUSCAR FACTURA PARA ASIGNAR ID_FACTURA A CHEQUE Y ACTUALIZAR FACTURA
                # ============================================
                id_factura_instancia = None
                factura_encontrada = None
                
                if comproing_raw and nrocomproing_raw and caja_numero:
                    comproing = str(comproing_raw).strip().upper()
                    nrocomproing = safe_int(nrocomproing_raw)
                    
                    if comproing and nrocomproing:
                        clave = f"{comproing}_{nrocomproing}"
                        
                        if clave in facturas_cache:
                            factura_encontrada = facturas_cache[clave]
                            id_factura_instancia = factura_encontrada
                            cheques_con_factura += 1
                            
                            # Buscar caja para asignar a la factura
                            caja_obj = cajas_cache.get(caja_numero)
                            
                            if caja_obj:
                                # Actualizar factura con id_caja si es diferente
                                if factura_encontrada.id_caja_id != caja_obj.id_caja:
                                    factura_encontrada.id_caja = caja_obj
                                    facturas_actualizadas.append(factura_encontrada)
                                    facturas_actualizadas_count += 1
                                    
                                    if facturas_actualizadas_count <= 5:
                                        print(f"<success>✓ Factura actualizada: {comproing} {nrocomproing} -> Caja {caja_numero}</success>")
                            else:
                                cajas_no_encontradas += 1
                                if cajas_no_encontradas <= 10:
                                    print(f"<warning>Caja no encontrada: {caja_numero} para factura {comproing} {nrocomproing}</warning>")
                                
                                # Registrar en archivo
                                with open(archivo_no_encontradas, 'a', encoding='utf-8') as f:
                                    f.write(f"{comproing}\t{nrocomproing}\t{caja_numero}\tCAJA_NO_ENCONTRADA\n")
                        else:
                            facturas_no_encontradas += 1
                            if facturas_no_encontradas <= 10:
                                print(f"<warning>Factura no encontrada: {comproing} {nrocomproing}</warning>")
                            
                            # Registrar en archivo
                            with open(archivo_no_encontradas, 'a', encoding='utf-8') as f:
                                f.write(f"{comproing}\t{nrocomproing}\t{caja_numero}\tFACTURA_NO_ENCONTRADA\n")
                
                # ============================================
                # 3. PROCESAR CHEQUE RECIBO CON ID_FACTURA ASIGNADO
                # ============================================
                # Obtener banco
                codbco_raw = record.get('CODBCO')
                id_banco_instancia = None
                
                if codbco_raw:
                    codbco = safe_int(codbco_raw)
                    if codbco:
                        id_banco_instancia = bancos_cache.get(codbco)
                        if not id_banco_instancia:
                            bancos_no_encontrados += 1
                
                # Obtener otros campos para ChequeRecibo
                codigo_banco = safe_small_int(codbco_raw)
                sucursal = safe_small_int(record.get('SUCURSAL'))
                codigo_postal = safe_small_int(record.get('LOCALIDAD'))
                numero_cheque = safe_small_int(record.get('NUMERO'))
                cuenta_cheque = safe_small_int(record.get('CUENTA'))
                cuit_cheque = safe_small_int(record.get('CUIT'))
                fecha_cheque1 = safe_date(record.get('FECHA'))
                importe_raw = record.get('IMPORTE')
                importe_cheque = safe_decimal(importe_raw)
                
                # Obtener electronico
                electronico_raw = None
                for campo in ['ELECTRONIC', 'ELECTRONI', 'ELECTRON', 'ELECTRO', 'ELECTR']:
                    if campo in record:
                        electronico_raw = record.get(campo)
                        break
                electronico = safe_bool(electronico_raw)
                
                # Verificar duplicados
                filtro = {
                    'numero_cheque_recibo': numero_cheque,
                    'cuenta_cheque_recibo': cuenta_cheque,
                    'cuit_cheque_recibo': cuit_cheque,
                    'importe_cheque': importe_cheque,
                    'id_banco': id_banco_instancia,
                }
                
                # Si tenemos factura, incluirla en el filtro de duplicados
                if id_factura_instancia:
                    filtro['id_factura'] = id_factura_instancia
                
                existe = ChequeRecibo.objects.filter(**filtro).exists()
                
                if not existe:
                    # Crear ChequeRecibo CON id_factura asignado
                    cheque_recibo = ChequeRecibo(
                        id_factura=id_factura_instancia,  # ¡ASIGNAMOS LA FACTURA!
                        id_banco=id_banco_instancia,
                        codigo_banco=codigo_banco,
                        sucursal=sucursal,
                        codigo_postal=codigo_postal,
                        numero_cheque_recibo=numero_cheque,
                        cuenta_cheque_recibo=cuenta_cheque,
                        cuit_cheque_recibo=cuit_cheque,
                        fecha_cheque1=fecha_cheque1,
                        fecha_cheque2=None,
                        importe_cheque=importe_cheque,
                        electronico=electronico
                    )
                    
                    cheques_batch.append(cheque_recibo)
                    registros_validos += 1
                    
                    # DEBUG: Mostrar primeros cheques con factura
                    if cheques_con_factura <= 5 and id_factura_instancia:
                        print(f"<success>✓ Cheque {numero_cheque} asociado a factura: {comproing} {nrocomproing}</success>")
                
                registros_procesados += 1

                # Mostrar progreso cada 5000 registros
                if registros_procesados % 5000 == 0:
                    print(f"<info>Registros procesados: {registros_procesados}/{total_records} | Cheques con factura: {cheques_con_factura}</info>")

                # Guardar lotes de ChequeRecibo
                if len(cheques_batch) >= batch_size:
                    with transaction.atomic():
                        ChequeRecibo.objects.bulk_create(cheques_batch)
                        print(f"<success>✅ Lote ChequeRecibo guardado: {len(cheques_batch)} registros</success>")
                        total_regs += len(cheques_batch)
                        cheques_batch = []
                
                # Guardar lotes de Facturas actualizadas
                if len(facturas_actualizadas) >= batch_size:
                    with transaction.atomic():
                        Factura.objects.bulk_update(facturas_actualizadas, ['id_caja'])
                        print(f"<success>✅ Lote Facturas actualizadas: {len(facturas_actualizadas)} registros</success>")
                        facturas_actualizadas = []

            except Exception as e:
                errores += 1
                if errores <= 10:
                    print(f"<error>Error en registro {idx}: {str(e)}</error>")
                continue

        # Guardar últimos registros
        if cheques_batch:
            with transaction.atomic():
                ChequeRecibo.objects.bulk_create(cheques_batch)
                print(f"<success>✅ Último lote ChequeRecibo: {len(cheques_batch)} registros</success>")
                total_regs += len(cheques_batch)
        
        if facturas_actualizadas:
            with transaction.atomic():
                Factura.objects.bulk_update(facturas_actualizadas, ['id_caja'])
                print(f"<success>✅ Último lote Facturas: {len(facturas_actualizadas)} actualizadas</success>")

        # Resultados finales
        elapsed_time = time.time() - start_time
        
        print(f"\n<info>{'='*60}</info>")
        print("<info>RESUMEN FINAL</info>")
        print(f"<info>{'='*60}</info>")
        print(f"<info>Total registros en DBF: {total_records}</info>")
        print(f"<info>Registros procesados: {registros_procesados}</info>")
        print(f"\n<success>Cheques Recibos creados: {registros_validos}</success>")
        print(f"<success>Cheques con factura asociada: {cheques_con_factura}</success>")
        print(f"<success>Facturas actualizadas con caja: {facturas_actualizadas_count}</success>")
        print(f"\n<warning>Registros omitidos:</warning>")
        print(f"  <warning>- Facturas no encontradas: {facturas_no_encontradas}</warning>")
        print(f"  <warning>- Cajas no encontradas: {cajas_no_encontradas}</warning>")
        print(f"  <warning>- Bancos no encontrados: {bancos_no_encontrados}</warning>")
        print(f"  <warning>- Duplicados: {registros_procesados - registros_validos - facturas_no_encontradas - cajas_no_encontradas}</warning>")
        print(f"\n<error>Errores encontrados: {errores}</error>")
        print(f"\n<info>Tiempo total: {elapsed_time:.2f} segundos</info>")
        
        # Información del archivo de no encontrados
        print(f"\n<info>Archivo de facturas no encontradas: {archivo_no_encontradas}</info>")
        
        # Verificar conteo final y estadísticas
        try:
            total_final_cheques = ChequeRecibo.objects.count()
            print(f"\n<info>Total ChequeRecibo en BD: {total_final_cheques}</info>")
            
            if total_regs != total_final_cheques:
                print(f"<warning>⚠️  ADVERTENCIA: Cheques guardados ({total_regs}) no coincide con BD ({total_final_cheques})</warning>")
            
            # Estadísticas detalladas
            if total_final_cheques > 0:
                print(f"\n<info>=== ESTADÍSTICAS DETALLADAS ===</info>")
                cheques_con_factura_db = ChequeRecibo.objects.filter(id_factura__isnull=False).count()
                cheques_sin_factura_db = ChequeRecibo.objects.filter(id_factura__isnull=True).count()
                electronicos_db = ChequeRecibo.objects.filter(electronico=True).count()
                
                print(f"<info>Cheques con factura en BD: {cheques_con_factura_db} ({cheques_con_factura_db/total_final_cheques*100:.1f}%)</info>")
                print(f"<info>Cheques sin factura en BD: {cheques_sin_factura_db} ({cheques_sin_factura_db/total_final_cheques*100:.1f}%)</info>")
                print(f"<info>Cheques electrónicos: {electronicos_db} ({electronicos_db/total_final_cheques*100:.1f}%)</info>")
                
        except Exception as e:
            print(f"\n<error>Nota: Error al verificar BD: {e}</error>")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_cheque_recibo: {str(e)}")
        print(f"<error>ERROR FATAL: {str(e)}</error>")
        raise

if __name__ == '__main__':
    cargar_datos_cheque_recibo()
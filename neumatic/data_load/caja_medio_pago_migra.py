# neumatic\data_load\caja_medio_pago_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from django.db import transaction
from decimal import Decimal

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.caja_models import Caja, CajaMedioPago
from apps.maestros.models.base_models import FormaPago

# Configuración de logging
logging.basicConfig(
    filename='caja_medio_pago_migra.log',
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

def safe_decimal(value, default=0.0):
    """Conversión segura a Decimal"""
    try:
        if value is not None and str(value).strip():
            return Decimal(str(value))
        return Decimal(str(default))
    except (ValueError, TypeError):
        return Decimal(str(default))

def reset_caja_medio_pago():
    """Elimina los datos existentes de manera controlada"""
    try:
        print("Iniciando reset de CajaMedioPago...")
        with transaction.atomic():
            count = CajaMedioPago.objects.count()
            CajaMedioPago.objects.all().delete()
            logger.info(f"Eliminados {count} registros existentes de CajaMedioPago")
            print(f"Eliminados {count} registros existentes de CajaMedioPago")
            
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='caja_medio_pago';")
            elif 'postgresql' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("ALTER SEQUENCE caja_medio_pago_id_caja_medio_pago_seq RESTART WITH 1;")
        print("Reset de CajaMedioPago completado")
    except Exception as e:
        logger.error(f"Error en reset_caja_medio_pago: {e}")
        print(f"ERROR en reset_caja_medio_pago: {e}")
        raise

def cargar_datos_caja_medio_pago():
    """Migración optimizada de mediopagos.DBF a modelo CajaMedioPago"""
    try:
        start_time = time.time()
        
        print("Iniciando migración de CajaMedioPago...")
        reset_caja_medio_pago()

        # Precargar caches para optimización
        print("Cargando cachés...")
        
        # Cache de cajas por numero_caja
        cajas_cache = {}
        for caja in Caja.objects.all():
            if caja.numero_caja:
                cajas_cache[caja.numero_caja] = caja
        
        print(f"Cargadas {len(cajas_cache)} cajas en caché")
        
        # Cache de formas de pago
        formas_pago_cache = {fp.pk: fp for fp in FormaPago.objects.all()}
        print(f"Cargadas {len(formas_pago_cache)} formas de pago en caché")

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'mediopagos.DBF')
        print(f"Procesando archivo: {dbf_path}")
        
        table = DBF(dbf_path, encoding='latin-1')
        total_records = len(table)
        print(f"Total de registros en DBF: {total_records}")
        
        # Mostrar estructura del DBF
        print("\n=== ESTRUCTURA DEL DBF ===")
        for field in table.fields:
            print(f"  {field.name:12} | Tipo: {field.type} | Tamaño: {field.length}")

        # Procesamiento por lotes
        batch_size = 5000
        medios_pago_batch = []
        registros_procesados = 0
        registros_validos = 0
        total_regs = 0
        errores = 0
        cajas_no_encontradas = 0
        formas_pago_no_encontradas = 0
        duplicados = 0
        cajas_vacias = 0

        for idx, record in enumerate(table, 1):
            try:
                # ============================================
                # 1. OBTENER Y VALIDAR CAJA (RELACIÓN PRINCIPAL)
                # ============================================
                caja_numero = safe_int(record.get('CAJA'))
                
                if not caja_numero:
                    cajas_vacias += 1
                    continue
                
                # Buscar caja en el cache
                caja_obj = cajas_cache.get(caja_numero)
                
                if not caja_obj:
                    cajas_no_encontradas += 1
                    continue
                
                # ============================================
                # 2. OBTENER IDVENTAS
                # ============================================
                idventa_raw = record.get('IDVENTA')
                idventas_int = safe_int(idventa_raw) if idventa_raw and safe_int(idventa_raw) != 0 else None
                
                # ============================================
                # 3. OBTENER FORMA DE PAGO
                # ============================================
                forma_pago_id = safe_int(record.get('FORMAPAGO'))
                forma_pago_obj = None
                
                if forma_pago_id:
                    forma_pago_obj = formas_pago_cache.get(forma_pago_id)
                    if not forma_pago_obj:
                        formas_pago_no_encontradas += 1
                
                # ============================================
                # 4. OBTENER IMPORTE
                # ============================================
                importe_raw = record.get('IMPORTE')
                importe_decimal = safe_decimal(importe_raw, 0.0)
                
                # ============================================
                # 5. VERIFICAR SI EL REGISTRO YA EXISTE
                # ============================================
                # Buscar por combinación única
                existe = CajaMedioPago.objects.filter(
                    id_caja=caja_obj,
                    idventas=idventas_int,
                    id_forma_pago=forma_pago_obj,
                    importe=importe_decimal
                ).exists()
                
                if existe:
                    duplicados += 1
                    continue
                
                # ============================================
                # 6. CREAR OBJETO CAJA MEDIO PAGO
                # ============================================
                caja_medio_pago = CajaMedioPago(
                    id_caja=caja_obj,
                    idventas=idventas_int,
                    id_forma_pago=forma_pago_obj,
                    importe=importe_decimal
                )
                
                medios_pago_batch.append(caja_medio_pago)
                registros_procesados += 1
                registros_validos += 1

                # Mostrar progreso cada 5000 registros VÁLIDOS
                if registros_validos % 5000 == 0:
                    print(f"Registros válidos procesados: {registros_validos} (Total leídos: {idx}/{total_records})")
                    
                    # Mostrar ejemplo del último registro procesado (solo primeros lotes)
                    if registros_validos <= 25000:
                        print(f"  Ejemplo: Caja {caja_numero} | IDVenta: {idventas_int} | FormaPago: {forma_pago_id} | Importe: {importe_decimal}")

                # Guardar por lotes cuando batch_size se alcanza
                if len(medios_pago_batch) >= batch_size:
                    with transaction.atomic():
                        CajaMedioPago.objects.bulk_create(medios_pago_batch)
                        print(f"✅ Lote guardado: {len(medios_pago_batch)} registros (Total válidos: {registros_validos})")
                        total_regs += len(medios_pago_batch)
                        medios_pago_batch = []

            except Exception as e:
                errores += 1
                if errores <= 10:
                    print(f"Error en registro {idx}: {str(e)}")
                continue

        # Guardar últimos registros
        if medios_pago_batch:
            with transaction.atomic():
                CajaMedioPago.objects.bulk_create(medios_pago_batch)
                print(f"✅ Último lote guardado: {len(medios_pago_batch)} registros")
                total_regs += len(medios_pago_batch)

        # Resultados finales
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*60}")
        print("RESUMEN FINAL")
        print(f"{'='*60}")
        print(f"Total registros en DBF: {total_records}")
        print(f"Registros leídos: {idx}")
        print(f"\nRegistros omitidos:")
        print(f"  - CAJA vacío/inválido: {cajas_vacias}")
        print(f"  - Cajas no encontradas: {cajas_no_encontradas}")
        print(f"  - Formas pago no encontradas: {formas_pago_no_encontradas}")
        print(f"  - Duplicados: {duplicados}")
        print(f"\nRegistros procesados exitosamente: {registros_validos}")
        print(f"Registros guardados en BD: {total_regs}")
        print(f"Errores encontrados: {errores}")
        print(f"\nTiempo total: {elapsed_time:.2f} segundos")
        
        # Verificar conteo final
        try:
            total_final = CajaMedioPago.objects.count()
            print(f"\nTotal registros en tabla caja_medio_pago: {total_final}")
            
            if total_regs != total_final:
                print(f"⚠️  ADVERTENCIA: Total guardado ({total_regs}) no coincide con BD ({total_final})")
        except Exception as e:
            print(f"\nNota: Error al verificar BD: {e}")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_caja_medio_pago: {str(e)}")
        print(f"ERROR FATAL: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_caja_medio_pago()
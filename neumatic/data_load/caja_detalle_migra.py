# neumatic\data_load\cajadetalle_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from django.db import transaction
from decimal import Decimal
from django.conf import settings

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.caja_models import Caja, CajaDetalle
from apps.maestros.models.base_models import FormaPago

# Configuración de logging
logging.basicConfig(
    filename='cajadetalle_migra.log',
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

def reset_cajadetalle():
    """Elimina los datos existentes en la tabla CajaDetalle y resetea su ID"""
    CajaDetalle.objects.all().delete()
    print("Tabla CajaDetalle limpiada.")
    
    engine = settings.DATABASES['default']['ENGINE']
    
    try:
        with connection.cursor() as cursor:
            if 'sqlite' in engine:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='caja_detalle';")
                print("Secuencia de ID reseteada (SQLite).")
            elif 'postgresql' in engine:
                cursor.execute("SELECT setval(pg_get_serial_sequence('caja_detalle', 'id_caja_detalle'), 1, false);")
                print("Secuencia de ID reseteada (PostgreSQL).")
            elif 'mssql' in engine or 'sql_server' in engine:
                cursor.execute("DBCC CHECKIDENT ('caja_detalle', RESEED, 0);")
                print("Secuencia de ID reseteada (SQL Server).")
            elif 'mysql' in engine:
                cursor.execute("ALTER TABLE caja_detalle AUTO_INCREMENT = 1;")
                print("Secuencia de ID reseteada (MySQL).")
            else:
                print(f"Motor {engine} no requiere reset manual de secuencia.")
        
        logger.info("Tabla CajaDetalle limpiada y secuencia reseteada.")
        
    except Exception as e:
        logger.error(f"Error al resetear tabla: {e}")
        raise

def cargar_datos_cajadetalle():
    """Migración optimizada de cajadetalle.DBF a modelo CajaDetalle"""
    try:
        start_time = time.time()
        reset_cajadetalle()
        
        print("Iniciando migración de CajaDetalle...")

        # Precargar cajas usando values_list
        print("Precargando cajas...")
        cajas_cache = {}
        for c in Caja.objects.values_list('numero_caja', 'id_caja'):
            if c[0]:
                cajas_cache[c[0]] = c[1]  # numero_caja -> id_caja
        print(f"Cajas precargadas: {len(cajas_cache)}")
        
        # Precargar formas de pago usando values_list
        print("Precargando formas de pago...")
        formas_pago_cache = {}
        for fp in FormaPago.objects.values_list('id_forma_pago', flat=True):
            formas_pago_cache[fp] = fp
        print(f"Formas de pago precargadas: {len(formas_pago_cache)}")

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'cajadetalle.DBF')
        print(f"Procesando archivo: {dbf_path}")
        
        table = list(DBF(dbf_path, encoding='latin-1'))
        total_records = len(table)
        print(f"Total de registros en DBF: {total_records}")
        
        batch_size = 5000
        detalles_batch = []
        registros_procesados = 0
        total_regs = 0
        errores = 0
        cajas_no_encontradas = 0
        formas_pago_no_encontradas = 0
        contador_id = 1

        for idx, record in enumerate(table, 1):
            if idx % 5000 == 0:
                print(f"Procesados: {idx}/{total_records} registros")

            try:
                # Obtener caja
                caja_numero = safe_int(record.get('CAJA'))
                if not caja_numero:
                    continue
                
                id_caja_id = cajas_cache.get(caja_numero)
                if not id_caja_id:
                    cajas_no_encontradas += 1
                    continue
                
                # Obtener forma de pago
                forma_pago_id = safe_int(record.get('FORMAPAGO'))
                id_forma_pago_id = formas_pago_cache.get(forma_pago_id) if forma_pago_id else None
                if forma_pago_id and not id_forma_pago_id:
                    formas_pago_no_encontradas += 1
                
                # Valores numéricos
                idventas_val = record.get('IDVENTAS')
                idventas_int = safe_int(idventas_val) if idventas_val and safe_int(idventas_val) != 0 else None
                
                idcompras_val = record.get('IDCOMPRAS')
                idcompras_int = safe_int(idcompras_val) if idcompras_val and safe_int(idcompras_val) != 0 else None
                
                idbancos_val = record.get('IDBANCOS')
                idbancos_int = safe_int(idbancos_val) if idbancos_val and safe_int(idbancos_val) != 0 else None
                
                importe_val = record.get('IMPORTE')
                importe_decimal = safe_decimal(importe_val, 0.0)
                
                # Tipo de movimiento
                tipo_movimiento = 1 if importe_decimal >= Decimal('0') else 2
                
                # Observación
                observacion_raw = record.get('OBSERVACIO')
                observacion = ''
                if observacion_raw is not None:
                    observacion_str = str(observacion_raw)
                    if observacion_str.strip():
                        observacion = observacion_str.strip()[:50]

                # Crear instancia con ID manual
                caja_detalle = CajaDetalle(
                    id_caja_detalle=contador_id,
                    id_caja_id=id_caja_id,
                    idventas=idventas_int,
                    idcompras=idcompras_int,
                    idbancos=idbancos_int,
                    id_forma_pago_id=id_forma_pago_id,
                    importe=importe_decimal,
                    tipo_movimiento=tipo_movimiento,
                    observacion=observacion
                )
                contador_id += 1
                
                detalles_batch.append(caja_detalle)
                registros_procesados += 1

                if len(detalles_batch) >= batch_size:
                    CajaDetalle.objects.bulk_create(detalles_batch)
                    total_regs += len(detalles_batch)
                    print(f"Lote guardado: {len(detalles_batch)} registros - Total: {total_regs}")
                    detalles_batch = []

            except Exception as e:
                errores += 1
                if errores <= 10:
                    print(f"Error en registro {idx}: {str(e)[:100]}")
                continue

        if detalles_batch:
            CajaDetalle.objects.bulk_create(detalles_batch)
            total_regs += len(detalles_batch)
            print(f"Último lote guardado: {len(detalles_batch)} registros")

        elapsed_time = time.time() - start_time
        mins = int(elapsed_time // 60)
        secs = int(elapsed_time % 60)
        
        print(f"\n{'='*60}")
        print(f"RESUMEN DE MIGRACIÓN DE CAJA_DETALLE")
        print(f"{'='*60}")
        print(f"Total registros en DBF: {total_records}")
        print(f"Registros procesados: {registros_procesados}")
        print(f"✅ Registros creados: {contador_id - 1}")
        print(f"❌ Errores: {errores}")
        print(f"Cajas no encontradas: {cajas_no_encontradas}")
        print(f"Formas de pago no encontradas: {formas_pago_no_encontradas}")
        print(f"⏱️ Tiempo total: {mins} min {secs} seg")
        print(f"{'='*60}")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_cajadetalle: {str(e)}")
        print(f"ERROR FATAL: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_cajadetalle()
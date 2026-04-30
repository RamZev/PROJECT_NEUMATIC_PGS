# neumatic\data_load\caja_arqueo_migra.py
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

from apps.ventas.models.caja_models import Caja, CajaArqueo

# Configuración de logging
logging.basicConfig(
    filename='caja_arqueo_migra.log',
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

def reset_caja_arqueo():
    """Elimina los datos existentes en la tabla CajaArqueo y resetea su ID"""
    CajaArqueo.objects.all().delete()
    print("Tabla CajaArqueo limpiada.")
    
    engine = settings.DATABASES['default']['ENGINE']
    
    try:
        with connection.cursor() as cursor:
            if 'sqlite' in engine:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='caja_arqueo';")
                print("Secuencia de ID reseteada (SQLite).")
            elif 'postgresql' in engine:
                cursor.execute("SELECT setval(pg_get_serial_sequence('caja_arqueo', 'id_caja_arqueo'), 1, false);")
                print("Secuencia de ID reseteada (PostgreSQL).")
            elif 'mssql' in engine or 'sql_server' in engine:
                cursor.execute("DBCC CHECKIDENT ('caja_arqueo', RESEED, 0);")
                print("Secuencia de ID reseteada (SQL Server).")
            elif 'mysql' in engine:
                cursor.execute("ALTER TABLE caja_arqueo AUTO_INCREMENT = 1;")
                print("Secuencia de ID reseteada (MySQL).")
            else:
                print(f"Motor {engine} no requiere reset manual de secuencia.")
        
        logger.info("Tabla CajaArqueo limpiada y secuencia reseteada.")
        
    except Exception as e:
        logger.error(f"Error al resetear tabla: {e}")
        raise

def cargar_datos_caja_arqueo():
    """Migración optimizada de cajaarqueo.DBF a modelo CajaArqueo"""
    try:
        start_time = time.time()
        reset_caja_arqueo()
        
        print("Iniciando migración de CajaArqueo...")

        # Precargar cajas usando values_list (numero_caja -> id_caja)
        print("Precargando cajas...")
        cajas_cache = {}
        for c in Caja.objects.values_list('numero_caja', 'id_caja'):
            if c[0]:
                cajas_cache[c[0]] = c[1]
        print(f"Cajas precargadas: {len(cajas_cache)}")

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'cajaarqueo.DBF')
        print(f"Procesando archivo: {dbf_path}")
        
        table = list(DBF(dbf_path, encoding='latin-1'))
        total_records = len(table)
        print(f"Total de registros en DBF: {total_records}")
        
        batch_size = 5000
        arqueos_batch = []
        registros_procesados = 0
        total_regs = 0
        errores = 0
        cajas_no_encontradas = 0
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
                
                # Procesar cantidad
                cantidad_raw = record.get('CANTIDAD')
                cantidad_decimal = safe_decimal(cantidad_raw, 0)
                cantidad_int = int(cantidad_decimal) if cantidad_decimal else None
                
                # Procesar valor unitario
                valor_raw = record.get('VALOR')
                valor_decimal = safe_decimal(valor_raw, 0)
                
                # Procesar detalle
                detalle_raw = record.get('DETALLE', '')
                detalle = ''
                if detalle_raw is not None:
                    detalle_str = str(detalle_raw).strip()
                    if detalle_str:
                        detalle = detalle_str[:15]
                
                # Calcular total
                total_raw = record.get('TOTAL')
                total_decimal = None
                if total_raw is not None:
                    total_decimal = safe_decimal(total_raw, 0)
                else:
                    if cantidad_decimal and valor_decimal:
                        total_decimal = cantidad_decimal * valor_decimal
                    else:
                        total_decimal = Decimal('0')

                # Crear instancia con ID manual
                caja_arqueo = CajaArqueo(
                    id_caja_arqueo=contador_id,
                    id_caja_id=id_caja_id,
                    cantidad=cantidad_int,
                    valor=valor_decimal,
                    detalle=detalle,
                    total=total_decimal
                )
                contador_id += 1
                
                arqueos_batch.append(caja_arqueo)
                registros_procesados += 1

                if len(arqueos_batch) >= batch_size:
                    CajaArqueo.objects.bulk_create(arqueos_batch)
                    total_regs += len(arqueos_batch)
                    print(f"Lote guardado: {len(arqueos_batch)} registros - Total: {total_regs}")
                    arqueos_batch = []

            except Exception as e:
                errores += 1
                if errores <= 10:
                    print(f"Error en registro {idx}: {str(e)[:100]}")
                continue

        if arqueos_batch:
            CajaArqueo.objects.bulk_create(arqueos_batch)
            total_regs += len(arqueos_batch)
            print(f"Último lote guardado: {len(arqueos_batch)} registros")

        elapsed_time = time.time() - start_time
        mins = int(elapsed_time // 60)
        secs = int(elapsed_time % 60)
        
        print(f"\n{'='*60}")
        print(f"RESUMEN DE MIGRACIÓN DE CAJA_ARQUEO")
        print(f"{'='*60}")
        print(f"Total registros en DBF: {total_records}")
        print(f"Registros procesados: {registros_procesados}")
        print(f"✅ Registros creados: {contador_id - 1}")
        print(f"❌ Errores: {errores}")
        print(f"Cajas no encontradas: {cajas_no_encontradas}")
        print(f"⏱️ Tiempo total: {mins} min {secs} seg")
        print(f"{'='*60}")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_caja_arqueo: {str(e)}")
        print(f"ERROR FATAL: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_caja_arqueo()
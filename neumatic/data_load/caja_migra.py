# neumatic\data_load\caja_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from django.db import transaction
from datetime import date, datetime
from django.utils import timezone
from django.conf import settings

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.sucursal_models import Sucursal
from apps.usuarios.models import User
from apps.ventas.models.caja_models import Caja

# Configuración de logging
logging.basicConfig(
    filename='caja_migra.log',
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

def safe_float(value, default=0.0):
    """Conversión segura a float"""
    try:
        return float(value) if value is not None and str(value).strip() else default
    except (ValueError, TypeError):
        return default

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

def safe_datetime(value, default=None):
    """Conversión segura para fechas/horas de DBF"""
    try:
        if value and isinstance(value, datetime):
            return timezone.make_aware(value)
        elif value and str(value).strip():
            if isinstance(value, str):
                for fmt in ('%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S'):
                    try:
                        dt = datetime.strptime(value, fmt)
                        return timezone.make_aware(dt)
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
            return value in ['T', 'TRUE', '1', 'S', 'SI', 'Y', 'YES']
        return default
    except (ValueError, TypeError):
        return default

def reset_caja():
    """Elimina los datos existentes de manera controlada"""
    Caja.objects.all().delete()
    print("Tabla Caja limpiada.")
    
    engine = settings.DATABASES['default']['ENGINE']
    
    try:
        with connection.cursor() as cursor:
            if 'sqlite' in engine:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='caja';")
                print("Secuencia de ID reseteada (SQLite).")
            elif 'postgresql' in engine:
                cursor.execute("SELECT setval(pg_get_serial_sequence('caja', 'id_caja'), 1, false);")
                print("Secuencia de ID reseteada (PostgreSQL).")
            elif 'mssql' in engine or 'sql_server' in engine:
                cursor.execute("DBCC CHECKIDENT ('caja', RESEED, 0);")
                print("Secuencia de ID reseteada (SQL Server).")
            elif 'mysql' in engine:
                cursor.execute("ALTER TABLE caja AUTO_INCREMENT = 1;")
                print("Secuencia de ID reseteada (MySQL).")
            else:
                print(f"Motor {engine} no requiere reset manual de secuencia.")
        
        logger.info("Tabla Caja limpiada y secuencia reseteada.")
        
    except Exception as e:
        logger.error(f"Error en reset_caja: {e}")
        raise

def cargar_datos_caja():
    """Migración optimizada de caja.DBF a modelo Caja"""
    try:
        start_time = time.time()
        reset_caja()

        # Precargar relaciones usando values_list (evita el bug del driver)
        print("Precargando relaciones...")
        
        sucursales_cache = {}
        for s in Sucursal.objects.values_list('id_sucursal', flat=True):
            sucursales_cache[s] = s
        print(f"Sucursales precargadas: {len(sucursales_cache)}")
        
        # Para usuarios, necesitamos username e id
        usuarios_cache = {}
        for u in User.objects.values_list('id', 'username'):
            usuarios_cache[u[1].lower() if u[1] else ''] = u[0]
        print(f"Usuarios precargados: {len(usuarios_cache)}")

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'caja.DBF')
        print(f"Procesando archivo: {dbf_path}")
        
        table = list(DBF(dbf_path, encoding='latin-1'))
        total_records = len(table)
        print(f"Total de registros en DBF: {total_records}")
        
        batch_size = 1000
        cajas_batch = []
        registros_procesados = 0
        total_regs = 0
        errores = 0
        contador_id = 1

        for idx, record in enumerate(table, 1):
            if idx % 1000 == 0:
                print(f"Procesados: {idx}/{total_records} registros")

            try:
                numero_caja = safe_int(record.get('NUMERO'))
                if not numero_caja:
                    continue

                # Obtener sucursal
                sucursal_id = safe_int(record.get('SUCURSAL'))
                id_sucursal_id = sucursales_cache.get(sucursal_id)
                
                # Buscar usuario para cierre
                usuario_cierre_nombre = record.get('USUARIO', '').strip().lower()
                id_usercierre_id = usuarios_cache.get(usuario_cierre_nombre) if usuario_cierre_nombre else None

                # Crear instancia con ID manual
                caja = Caja(
                    id_caja=contador_id,
                    numero_caja=numero_caja,
                    fecha_caja=safe_date(record.get('FECHA')),
                    saldoanterior=safe_float(record.get('SALDOANTERIO')),
                    ingresos=safe_float(record.get('INGRESOS')),
                    egresos=safe_float(record.get('EGRESOS')),
                    saldo=safe_float(record.get('SALDO')),
                    caja_cerrada=safe_bool(record.get('CERRADA')),
                    recuento=safe_float(record.get('RECUENTO')),
                    diferencia=safe_float(record.get('DIFERENCIA')),
                    id_sucursal_id=id_sucursal_id,
                    hora_cierre=safe_datetime(record.get('HORACIERRE')),
                    observacion_caja=record.get('OBSERVA', '').strip()[:50] if record.get('OBSERVA') else None,
                    id_usercierre_id=id_usercierre_id
                )
                contador_id += 1
                
                cajas_batch.append(caja)
                registros_procesados += 1

                if len(cajas_batch) >= batch_size:
                    Caja.objects.bulk_create(cajas_batch)
                    total_regs += len(cajas_batch)
                    print(f"Lote guardado: {len(cajas_batch)} registros - Acumulado: {total_regs}")
                    cajas_batch = []

            except Exception as e:
                errores += 1
                if errores <= 10:
                    print(f"Error en registro {idx}: {str(e)[:100]}")
                continue

        if cajas_batch:
            Caja.objects.bulk_create(cajas_batch)
            total_regs += len(cajas_batch)
            print(f"Último lote guardado: {len(cajas_batch)} registros")

        elapsed_time = time.time() - start_time
        mins = int(elapsed_time // 60)
        secs = int(elapsed_time % 60)
        
        print(f"\n{'='*60}")
        print(f"RESUMEN DE MIGRACIÓN DE CAJA")
        print(f"{'='*60}")
        print(f"Total registros en DBF: {total_records}")
        print(f"Registros procesados: {registros_procesados}")
        print(f"✅ Registros creados: {contador_id - 1}")
        print(f"❌ Errores: {errores}")
        print(f"⏱️ Tiempo total: {mins} min {secs} seg")
        print(f"{'='*60}")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_caja: {str(e)}")
        print(f"ERROR FATAL: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_caja()
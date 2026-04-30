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
            # Convertir naive datetime a timezone aware
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
        return default  # Permitir None - ahora el campo lo acepta
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
    try:
        with transaction.atomic():
            count = Caja.objects.count()
            Caja.objects.all().delete()
            logger.info(f"Eliminados {count} registros existentes de Caja")
            print(f"Eliminados {count} registros existentes de Caja")
            
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='caja';")
            elif 'postgresql' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("ALTER SEQUENCE caja_id_caja_seq RESTART WITH 1;")
    except Exception as e:
        logger.error(f"Error en reset_caja: {e}")
        raise

def cargar_datos_caja():
    """Migración optimizada de caja.DBF a modelo Caja"""
    try:
        start_time = time.time()
        reset_caja()

        # Precargar relaciones para optimización
        sucursales_cache = {s.id_sucursal: s for s in Sucursal.objects.all()}
        usuarios_cache = {u.pk: u for u in User.objects.all()}

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'caja.DBF')
        print(f"Procesando archivo: {dbf_path}")
        
        table = DBF(dbf_path, encoding='latin-1')
        total_records = len(table)
        print(f"Total de registros en DBF: {total_records}")
        
        # Procesamiento por lotes
        batch_size = 1000
        cajas_batch = []
        registros_procesados = 0
        total_regs = 0
        errores = 0

        for idx, record in enumerate(table, 1):
            try:
                # Procesamiento seguro de campos - USANDO NOMBRES EN MAYÚSCULAS
                numero_caja = safe_int(record.get('NUMERO'))
                if not numero_caja:
                    logger.warning(f"Registro sin número de caja válido en posición {idx}")
                    continue

                # Obtener e INSTANCIAR la sucursal
                sucursal_id = safe_int(record.get('SUCURSAL'))
                id_sucursal_instancia = None
                if sucursal_id and sucursal_id in sucursales_cache:
                    id_sucursal_instancia = sucursales_cache[sucursal_id]
                else:
                    logger.warning(f"Sucursal ID {sucursal_id} no encontrada para caja {numero_caja}")
                
                # Buscar usuario para cierre (si existe)
                usuario_cierre_nombre = record.get('USUARIO', '').strip()
                id_usercierre_instancia = None
                if usuario_cierre_nombre:
                    # Buscar usuario por nombre de usuario
                    for user in usuarios_cache.values():
                        if user.username and usuario_cierre_nombre.lower() in user.username.lower():
                            id_usercierre_instancia = user
                            break
                    if not id_usercierre_instancia:
                        logger.warning(f"Usuario '{usuario_cierre_nombre}' no encontrado para caja {numero_caja}")

                # Manejar hora_cierre - ahora puede ser None sin problemas
                hora_cierre_value = safe_datetime(record.get('HORACIERRE'))
                
                # Crear instancia de Caja
                caja = Caja(
                    numero_caja=numero_caja,
                    fecha_caja=safe_date(record.get('FECHA')),
                    saldoanterior=safe_float(record.get('SALDOANTER')),
                    ingresos=safe_float(record.get('INGRESOS')),
                    egresos=safe_float(record.get('EGRESOS')),
                    saldo=safe_float(record.get('SALDO')),
                    caja_cerrada=safe_bool(record.get('CERRADA')),
                    recuento=safe_float(record.get('RECUENTO')),
                    diferencia=safe_float(record.get('DIFERENCIA')),
                    id_sucursal=id_sucursal_instancia,
                    hora_cierre=hora_cierre_value,  # Ahora puede ser None sin problemas
                    observacion_caja=record.get('OBSERVA', '').strip()[:50],
                    id_usercierre=id_usercierre_instancia
                )
                
                cajas_batch.append(caja)
                registros_procesados += 1

                # Mostrar progreso cada 1000 registros
                if registros_procesados % 1000 == 0:
                    print(f"Procesados: {registros_procesados}/{total_records} registros")

                # Guardar por lotes
                if len(cajas_batch) >= batch_size:
                    Caja.objects.bulk_create(cajas_batch)
                    logger.info(f"Lote guardado: {len(cajas_batch)} registros")
                    total_regs += len(cajas_batch)
                    print(f"Lote guardado: {len(cajas_batch)} registros - Acumulado: {total_regs} registros")
                    cajas_batch = []

            except Exception as e:
                errores += 1
                logger.error(f"Error en registro {idx} (Número: {record.get('NUMERO')}): {str(e)}")
                print(f"Error en registro {idx}: {str(e)}")
                continue

        # Guardar últimos registros
        if cajas_batch:
            Caja.objects.bulk_create(cajas_batch)
            logger.info(f"Último lote guardado: {len(cajas_batch)} registros")
            total_regs += len(cajas_batch)
            print(f"Último lote guardado: {len(cajas_batch)} registros")

        # Resultados finales
        elapsed_time = time.time() - start_time
        logger.info(f"Migración completada. Registros: {registros_procesados}, Errores: {errores}")
        logger.info(f"Tiempo total: {elapsed_time:.2f} segundos")

        print(f"\nResumen de migración de Caja:")
        print(f"Total registros en DBF: {total_records}")
        print(f"Registros procesados: {registros_procesados}")
        print(f"Errores encontrados: {errores}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_caja: {str(e)}")
        print(f"ERROR FATAL: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_caja()
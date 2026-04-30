# neumatic\data_load\detalle_factura_migra.py
import os
import sys
import django
import time
import logging
import re
from dbfread import DBF
from django.db import connection
from decimal import Decimal, InvalidOperation
from django.db import transaction

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.factura_models import Factura, DetalleFactura, SerialFactura
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.base_models import Operario

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migracion_detalle_factura_detallado.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def limpiar_numero(valor):
    """Limpia un número eliminando caracteres no numéricos (excepto punto decimal)"""
    if valor is None:
        return None
    
    valor_str = str(valor).strip()
    if not valor_str:
        return None
    
    # Solo eliminar caracteres que no sean dígitos, punto o signo menos
    valor_str = re.sub(r'[^\d\.-]', '', valor_str)
    
    return valor_str

def safe_decimal(value, field_name='campo', default=None):
    """Conversión segura a Decimal"""
    if value is None:
        return default
    
    valor_limpio = limpiar_numero(value)
    if not valor_limpio:
        return default
    
    try:
        return Decimal(valor_limpio)
    except InvalidOperation:
        logger.warning(f"Error de conversión Decimal en {field_name}: '{value}' -> '{valor_limpio}'")
        return default
    except Exception as e:
        logger.error(f"Error inesperado en {field_name}: {str(e)}")
        return default

def safe_int(value, field_name='campo', default=None):
    """Conversión segura a entero"""
    if value is None:
        return default
    
    try:
        # Si es string, limpiar
        if isinstance(value, str):
            valor_limpio = re.sub(r'[^\d-]', '', value.strip())
            if not valor_limpio:
                return default
            return int(float(valor_limpio))
        return int(value)
    except (ValueError, TypeError):
        logger.warning(f"Error convirtiendo a entero en {field_name}: '{value}'")
        return default

def safe_str(value, default=""):
    """Conversión segura a string"""
    if value is None:
        return default
    return str(value).strip()

def reset_detalle_factura():
    """Elimina los datos existentes en la tabla DetalleFactura y resetea su ID"""
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    try:
        if 'mssql' in engine or 'sql_server' in engine:
            with connection.cursor() as cursor:
                count = DetalleFactura.objects.count()
                cursor.execute("DELETE FROM detalle_factura")
                cursor.execute("DBCC CHECKIDENT ('detalle_factura', RESEED, 0);")
                logger.info(f"Tabla DetalleFactura limpiada (SQL Server). {count} registros eliminados.")
        else:
            with transaction.atomic():
                count = DetalleFactura.objects.count()
                DetalleFactura.objects.all().delete()
                if 'sqlite' in connection.settings_dict['ENGINE']:
                    with connection.cursor() as cursor:
                        cursor.execute("DELETE FROM sqlite_sequence WHERE name='detalle_factura';")
            logger.info(f"Tabla DetalleFactura limpiada (SQLite). {count} registros eliminados.")
    except Exception as e:
        logger.error(f"Error al resetear tabla: {e}")
        raise

def cargar_datos_detalle_factura():
    """Proceso de migración"""
    start_time = time.time()
    reset_detalle_factura()

    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'detven.DBF')
    
    if not os.path.exists(dbf_path):
        logger.error(f"Archivo DBF no encontrado en: {dbf_path}")
        return

    try:
        table = DBF(dbf_path, encoding='latin-1')
    except UnicodeDecodeError:
        table = DBF(dbf_path, encoding='utf-8')

    total_registros = len(table)
    logger.info(f"Iniciando migración. Total registros: {total_registros}")

    # Precargar IDs de facturas
    print("🧠 Precargando facturas...")
    facturas_cache = set()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_factura FROM factura")
        for row in cursor.fetchall():
            facturas_cache.add(row[0])
    print(f"✅ Facturas precargadas: {len(facturas_cache)}")

    # Precargar IDs de operarios
    print("🧠 Precargando operarios...")
    operarios_cache = set()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_operario FROM operario")
        for row in cursor.fetchall():
            operarios_cache.add(row[0])
    print(f"✅ Operarios precargados: {len(operarios_cache)}")

    batch_size = 500
    detalles_batch = []
    registros_procesados = 0
    errores = 0
    contador_id = 1

    for idx, record in enumerate(table, 1):
        if idx % 10000 == 0:
            print(f"⏳ Progreso: {idx}/{total_registros} registros...")

        try:
            id_factura = safe_int(record.get('ID'))
            if id_factura is None or id_factura not in facturas_cache:
                continue

            codigo_raw = record.get('CODIGO')
            codigo_producto = safe_int(codigo_raw)
            
            id_operario = safe_int(record.get('OPERARIO'))
            if id_operario is not None and id_operario not in operarios_cache:
                id_operario = None

            producto_venta = safe_str(codigo_raw)[:50] if codigo_raw else None

            detalle = DetalleFactura(
                id_detalle_factura=contador_id,
                id_factura_id=id_factura,
                id_producto_id=None,
                codigo=codigo_producto,
                producto_venta=producto_venta,
                cantidad=safe_decimal(record.get('CANTIDAD'), 'CANTIDAD'),
                costo=safe_decimal(record.get('COSTO'), 'COSTO'),
                precio=safe_decimal(record.get('PRECIO'), 'PRECIO'),
                descuento=safe_decimal(record.get('DESCUENTO'), 'DESCUENTO'),
                gravado=safe_decimal(record.get('GRAVADO'), 'GRAVADO'),
                alic_iva=safe_decimal(record.get('ALICIVA'), 'ALICIVA'),
                iva=safe_decimal(record.get('IVA'), 'IVA'),
                total=safe_decimal(record.get('TOTAL'), 'TOTAL'),
                reventa=safe_str(record.get('REVENTA'))[:1],
                stock=safe_decimal(record.get('STOCK'), 'STOCK'),
                act_stock=bool(safe_int(record.get('ACTSTOCK'), default=0)),
                id_operario_id=id_operario
            )
            
            detalles_batch.append(detalle)
            registros_procesados += 1
            contador_id += 1

            if len(detalles_batch) >= batch_size:
                DetalleFactura.objects.bulk_create(detalles_batch)
                logger.info(f"✅ Lote guardado: {len(detalles_batch)} registros - Total: {registros_procesados}")
                detalles_batch = []

        except Exception as e:
            errores += 1
            if errores <= 10:
                logger.error(f"Error en registro {idx}: {str(e)[:150]}")
            continue

    if detalles_batch:
        DetalleFactura.objects.bulk_create(detalles_batch)
        logger.info(f"✅ Último lote guardado: {len(detalles_batch)} registros")

    elapsed_time = time.time() - start_time
    mins, secs = divmod(elapsed_time, 60)
    
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN DE MIGRACIÓN DE DETALLE_FACTURA")
    print(f"{'='*60}")
    print(f"✅ Registros procesados: {registros_procesados}")
    print(f"❌ Errores: {errores}")
    print(f"📊 Total en DBF: {total_registros}")
    print(f"⏱️ Tiempo total: {int(mins)} min {int(secs)} seg")
    print(f"{'='*60}")

if __name__ == '__main__':
    cargar_datos_detalle_factura()
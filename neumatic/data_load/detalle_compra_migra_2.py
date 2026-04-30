# neumatic\data_load\detalle_compra_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from decimal import Decimal, InvalidOperation
from django.db import transaction

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.compra_models import Compra, DetalleCompra
from apps.maestros.models.producto_models import Producto

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migracion_detalle_compra_detallado.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def safe_decimal(value, field_name='campo', default=None):
    if value is None or str(value).strip() == '':
        return default
    try:
        str_value = str(value).strip().replace(',', '.')
        cleaned = ''.join(c for c in str_value if c.isdigit() or c in '-.')
        if not cleaned or cleaned == '-':
            return default
        return Decimal(cleaned)
    except InvalidOperation:
        logger.warning(f"Error de conversión Decimal en {field_name}: '{value}'")
        return default
    except Exception as e:
        logger.error(f"Error inesperado en {field_name} con valor '{value}': {str(e)}")
        return default

def safe_int(value, field_name='campo', default=None):
    """Conversión robusta a entero"""
    try:
        if value is None or str(value).strip() == '':
            return default
        decimal_val = safe_decimal(value, field_name)
        if decimal_val is None:
            return default
        return int(decimal_val)
    except Exception as e:
        logger.warning(f"Error convirtiendo a entero en {field_name}: '{value}' - {str(e)}")
        return default

def reset_detalle_compra():
    """Elimina los datos existentes en la tabla DetalleCompra"""
    try:
        with transaction.atomic():
            count = DetalleCompra.objects.count()
            if count > 0:
                logger.info(f"Eliminando {count} registros existentes...")
                DetalleCompra.objects.all().delete()
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='detalle_compra';")
    except Exception as e:
        logger.error(f"Error al resetear tabla: {e}")
        raise

def cargar_datos_detalle_compra():
    """Proceso de migración optimizado con manejo robusto de errores"""
    start_time = time.time()
    # reset_detalle_compra()

    # Optimización para SQLite
    if 'sqlite' in connection.settings_dict['ENGINE']:
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA synchronous = OFF;")
            cursor.execute("PRAGMA journal_mode = MEMORY;")
            cursor.execute("PRAGMA cache_size = 10000;")

    # Ruta del archivo DBF
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'detcom.DBF')
    
    if not os.path.exists(dbf_path):
        logger.error(f"Archivo DBF no encontrado en: {dbf_path}")
        return

    try:
        table = DBF(dbf_path, encoding='latin-1')
    except UnicodeDecodeError:
        table = DBF(dbf_path, encoding='utf-8')

    logger.info(f"Iniciando migración. Total registros: {len(table)}")

    # Precargar datos en caché
    logger.info("Cargando cachés de referencia...")
    productos_cache = {}
    for p in Producto.objects.all():
        try:
            key = safe_int(p.codigo_producto, 'codigo_producto')
            if key is not None:
                productos_cache[key] = p
        except Exception as e:
            logger.error(f"Error procesando producto ID {p.id}: {str(e)}")
            continue
    
    compras_cache = {c.id_compra: c for c in Compra.objects.all()}

    # Configuración de procesamiento por lotes
    batch_size = 2000
    detalles_batch = []
    registros_procesados = 0
    errores = 0
    productos_no_encontrados = set()

    for idx, record in enumerate(table, 1):
        try:
            # Obtener ID de compra
            id_compra = safe_int(record.get('ID'), 'ID_compra')
            if id_compra is None:
                logger.warning(f"Registro {idx} sin ID de compra válido")
                continue

            # Verificar existencia de compra
            compra = compras_cache.get(id_compra)
            if not compra:
                logger.warning(f"Compra no encontrada ID: {id_compra}")
                continue

            # Obtener producto
            codigo_producto = safe_int(record.get('CODIGO'), 'CODIGO_producto')
            producto = productos_cache.get(codigo_producto) if codigo_producto is not None else None
            
            if not producto and codigo_producto is not None:
                productos_no_encontrados.add((codigo_producto, record.get('CODIGO')))
                continue

            # Crear instancia con conversiones seguras
            detalle = DetalleCompra(
                id_compra=compra,
                id_producto=producto,
                cantidad=safe_decimal(record.get('CANTIDAD'), 'CANTIDAD', Decimal('0.00')),
                precio=safe_decimal(record.get('PRECIO'), 'PRECIO', Decimal('0.00')),
                total=safe_decimal(record.get('TOTAL'), 'TOTAL', Decimal('0.00')),
                despacho=str(record.get('DESPACHO', '')).strip()
            )
            
            detalles_batch.append(detalle)
            registros_procesados += 1

            # Guardar por lotes
            if len(detalles_batch) >= batch_size:
                with transaction.atomic():
                    DetalleCompra.objects.bulk_create(detalles_batch)
                logger.info(f"Lote guardado: {len(detalles_batch)} registros")
                detalles_batch = []

            if registros_procesados % 10000 == 0:
                logger.info(f"Progreso: {registros_procesados} registros procesados")

        except Exception as e:
            errores += 1
            # Registrar el valor problemático de los campos numéricos
            cantidad_raw = record.get('CANTIDAD')
            precio_raw = record.get('PRECIO')
            total_raw = record.get('TOTAL')
            error_msg = f"Error en compra ID {id_compra} - Registro {idx}: {str(e)} - Valor problemático: CANTIDAD={cantidad_raw}, PRECIO={precio_raw}, TOTAL={total_raw}"
            logger.error(error_msg)
            logger.debug(f"Registro problemático completo: {record}")
            continue

    # Guardar últimos registros
    if detalles_batch:
        with transaction.atomic():
            DetalleCompra.objects.bulk_create(detalles_batch)
        logger.info(f"Último lote guardado: {len(detalles_batch)} registros")

    # Reporte final
    logger.info("\n=== REPORTE FINAL ===")
    logger.info(f"Total registros procesados: {registros_procesados}")
    logger.info(f"Total errores: {errores}")
    
    if productos_no_encontrados:
        logger.warning(f"\nProductos no encontrados ({len(productos_no_encontrados)}):")
        for codigo, codigo_raw in sorted(productos_no_encontrados)[:100]:
            logger.warning(f" - Código convertido: {codigo} | Valor original: {codigo_raw}")

    elapsed_time = time.time() - start_time
    mins, secs = divmod(elapsed_time, 60)
    logger.info(f"\nTiempo total: {int(mins)} minutos {int(secs)} segundos")

if __name__ == '__main__':
    cargar_datos_detalle_compra()
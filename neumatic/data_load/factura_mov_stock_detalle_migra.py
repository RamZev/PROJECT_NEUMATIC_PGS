# neumatic\data_load\factura_mov_stock_detalle_migra.py
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

from apps.ventas.models.factura_models import Factura, DetalleFactura
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.base_models import Operario

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migracion_movstockdetalle_detallado.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def safe_decimal(value, field_name='campo', default=None):
    """Conversión robusta a Decimal con diagnóstico mejorado"""
    if value is None or str(value).strip() == '':
        return default
        
    try:
        # Limpieza del valor
        str_value = str(value).strip().replace(',', '.')
        
        # Eliminar caracteres no numéricos (excepto punto y signo)
        cleaned = ''.join(c for c in str_value if c.isdigit() or c in '.-')
        if not cleaned:
            return default
            
        # Verificar formato válido
        if cleaned.count('.') > 1 or '-' in cleaned[1:]:
            logger.warning(f"Formato numérico inválido en {field_name}: '{value}'")
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
            
        # Primero convertir a Decimal (maneja formatos con decimales)
        decimal_val = safe_decimal(value, field_name)
        if decimal_val is None:
            return default
            
        return int(decimal_val)
    except Exception as e:
        logger.warning(f"Error convirtiendo a entero en {field_name}: '{value}' - {str(e)}")
        return default

def reset_detalle_factura():
    """Elimina los datos existentes en la tabla DetalleFactura"""
    try:
        with transaction.atomic():
            count = DetalleFactura.objects.count()
            if count > 0:
                logger.info(f"Eliminando {count} registros existentes...")
                DetalleFactura.objects.all().delete()
                
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='detalle_factura';")
    except Exception as e:
        logger.error(f"Error al resetear tabla: {e}")
        raise

def cargar_datos_movstockdetalle():
    """Proceso de migración optimizado con manejo robusto de errores — desde movstockdetalle.DBF"""
    start_time = time.time()
    # reset_detalle_factura()

    # Optimización para SQLite
    if 'sqlite' in connection.settings_dict['ENGINE']:
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA synchronous = OFF;")
            cursor.execute("PRAGMA journal_mode = MEMORY;")
            cursor.execute("PRAGMA cache_size = 10000;")

    # Ruta del archivo DBF — ¡CAMBIO CLAVE!
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'movstockdetalle.DBF')
    
    if not os.path.exists(dbf_path):
        logger.error(f"Archivo DBF no encontrado en: {dbf_path}")
        return

    try:
        table = DBF(dbf_path, encoding='latin-1')
    except UnicodeDecodeError:
        table = DBF(dbf_path, encoding='utf-8')

    logger.info(f"Iniciando migración desde movstockdetalle.DBF. Total registros: {len(table)}")

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
    
    facturas_cache = {f.pk: f for f in Factura.objects.all()}
    operarios_cache = {o.pk: o for o in Operario.objects.all()}

    # Configuración de procesamiento por lotes
    batch_size = 2000
    detalles_batch = []
    registros_procesados = 0
    errores = 0
    productos_no_encontrados = set()

    for idx, record in enumerate(table, 1):
        try:
            # Obtener ID de factura
            id_factura = safe_int(record.get('ID'), 'ID_factura')
            if id_factura is None:
                logger.warning(f"Registro {idx} sin ID de factura válido")
                continue

            # Verificar existencia de factura
            factura = facturas_cache.get(id_factura)
            if not factura:
                logger.warning(f"Factura no encontrada ID: {id_factura}")
                continue

            # Obtener producto
            codigo_producto = safe_int(record.get('CODIGO'), 'CODIGO_producto')
            producto = productos_cache.get(codigo_producto) if codigo_producto is not None else None
            
            if not producto:
                productos_no_encontrados.add((codigo_producto, record.get('CODIGO')))
                continue

            # Crear instancia con conversiones seguras
            detalle = DetalleFactura(
                id_factura=factura,
                id_producto=producto,
                codigo=codigo_producto,
                producto_venta=producto.nombre_producto[:50] if producto.nombre_producto else None,
                cantidad=safe_decimal(record.get('CANTIDAD'), 'CANTIDAD', Decimal('0.00')),
                costo=safe_decimal(record.get('COSTO'), 'COSTO'),
                precio=safe_decimal(record.get('PRECIO'), 'PRECIO'),
                precio_lista=safe_decimal(producto.precio, 'precio_lista') if producto.precio else None,
                descuento=safe_decimal(record.get('DESCUENTO'), 'DESCUENTO'),
                gravado=safe_decimal(record.get('GRAVADO'), 'GRAVADO'),
                alic_iva=safe_decimal(record.get('ALICIVA'), 'ALICIVA'),
                iva=safe_decimal(record.get('IVA'), 'IVA'),
                total=safe_decimal(record.get('TOTAL'), 'TOTAL'),
                reventa=str(record.get('REVENTA', '')).strip()[:1],
                stock=safe_decimal(record.get('STOCK'), 'STOCK'),
                act_stock=bool(safe_int(record.get('ACTSTOCK'), 'ACTSTOCK', 0)),
                id_operario=operarios_cache.get(safe_int(record.get('OPERARIO'), 'OPERARIO'))
            )
            
            detalles_batch.append(detalle)
            registros_procesados += 1

            # Guardar por lotes
            if len(detalles_batch) >= batch_size:
                with transaction.atomic():
                    DetalleFactura.objects.bulk_create(detalles_batch)
                logger.info(f"Lote guardado: {len(detalles_batch)} registros")
                detalles_batch = []

            if registros_procesados % 10000 == 0:
                logger.info(f"Progreso: {registros_procesados} registros procesados")

        except Exception as e:
            errores += 1
            logger.error(f"Error en factura ID {id_factura} - Registro {idx}: {str(e)}")
            logger.debug(f"Registro problemático: {record}")
            continue

    # Guardar últimos registros
    if detalles_batch:
        with transaction.atomic():
            DetalleFactura.objects.bulk_create(detalles_batch)
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
    cargar_datos_movstockdetalle()
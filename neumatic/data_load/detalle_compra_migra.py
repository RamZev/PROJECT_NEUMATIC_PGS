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
from django.conf import settings

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
    """Conversión robusta a Decimal"""
    if value is None or str(value).strip() == '':
        return default
    try:
        str_value = str(value).strip().replace(',', '.')
        cleaned = ''.join(c for c in str_value if c.isdigit() or c in '.-')
        if not cleaned:
            return default
        if cleaned.count('.') > 1 or '-' in cleaned[1:]:
            logger.warning(f"Formato numérico inválido en {field_name}: '{value}'")
            return default
        return Decimal(cleaned)
    except InvalidOperation:
        logger.warning(f"Error de conversión Decimal en {field_name}: '{value}'")
        return default
    except Exception as e:
        logger.error(f"Error inesperado en {field_name}: {str(e)}")
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
        logger.warning(f"Error convirtiendo a entero en {field_name}: '{value}'")
        return default

def reset_detalle_compra():
    """Elimina los datos existentes en la tabla DetalleCompra y resetea su ID"""
    DetalleCompra.objects.all().delete()
    print("Tabla DetalleCompra limpiada.")
    
    engine = settings.DATABASES['default']['ENGINE']
    
    try:
        with connection.cursor() as cursor:
            if 'sqlite' in engine:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='detalle_compra';")
                print("Secuencia de ID reseteada (SQLite).")
            elif 'postgresql' in engine:
                cursor.execute("SELECT setval(pg_get_serial_sequence('detalle_compra', 'id_detalle_compra'), 1, false);")
                print("Secuencia de ID reseteada (PostgreSQL).")
            elif 'mssql' in engine or 'sql_server' in engine:
                cursor.execute("DBCC CHECKIDENT ('detalle_compra', RESEED, 0);")
                print("Secuencia de ID reseteada (SQL Server).")
            elif 'mysql' in engine:
                cursor.execute("ALTER TABLE detalle_compra AUTO_INCREMENT = 1;")
                print("Secuencia de ID reseteada (MySQL).")
            else:
                print(f"Motor {engine} no requiere reset manual de secuencia.")
        
        logger.info("Tabla DetalleCompra limpiada y secuencia reseteada.")
        
    except Exception as e:
        logger.error(f"Error al resetear tabla: {e}")
        raise

def cargar_datos_detalle_compra():
    """Proceso de migración optimizado para SQL Server con values_list"""
    start_time = time.time()
    reset_detalle_compra()

    # Precargar productos usando values_list (evita el bug del driver)
    print("Precargando productos...")
    productos_cache = {}
    for p in Producto.objects.values_list('id_producto', 'codigo_producto'):
        key = safe_int(p[1], 'codigo_producto')
        if key is not None:
            producto = Producto(id_producto=p[0])
            producto.codigo_producto = p[1]
            productos_cache[key] = producto
    print(f"Productos precargados: {len(productos_cache)}")
    
    # Precargar compras usando values_list (creando objetos)
    print("Precargando compras...")
    compras_cache = {}
    for c in Compra.objects.values_list('id_compra', flat=True):
        compras_cache[c] = Compra(id_compra=c)
    print(f"Compras precargadas: {len(compras_cache)}")

    # Ruta del archivo DBF
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'detcom.DBF')
    
    if not os.path.exists(dbf_path):
        logger.error(f"Archivo DBF no encontrado en: {dbf_path}")
        return

    # Leer DBF
    try:
        table = list(DBF(dbf_path, encoding='latin-1'))
    except UnicodeDecodeError:
        table = list(DBF(dbf_path, encoding='utf-8'))

    total_registros = len(table)
    print(f"\nTotal registros en DBF: {total_registros}")
    
    batch_size = 2000
    detalles_batch = []
    registros_procesados = 0
    errores = 0
    productos_no_encontrados = set()
    contador_id = 1

    for idx, record in enumerate(table, 1):
        if idx % 10000 == 0:
            print(f"Progreso: {idx}/{total_registros} registros...")

        try:
            # Obtener ID de compra y el objeto Compra
            id_compra = safe_int(record.get('ID'), 'ID_compra')
            if id_compra is None:
                continue
            
            compra = compras_cache.get(id_compra)
            if not compra:
                continue

            # Obtener producto
            codigo_producto = safe_int(record.get('CODIGO'), 'CODIGO_producto')
            producto = productos_cache.get(codigo_producto) if codigo_producto is not None else None
            
            if not producto and codigo_producto is not None:
                productos_no_encontrados.add((codigo_producto, record.get('CODIGO')))
                continue

            # Convertir campos decimales
            cantidad = safe_decimal(record.get('CANTIDAD'), 'CANTIDAD', Decimal('0.00'))
            precio = safe_decimal(record.get('PRECIO'), 'PRECIO', Decimal('0.00'))
            total = safe_decimal(record.get('TOTAL'), 'TOTAL', Decimal('0.00'))

            # Validar valores no finitos
            if cantidad is not None and not cantidad.is_finite():
                cantidad = Decimal('0.00')
            if precio is not None and not precio.is_finite():
                precio = Decimal('0.00')
            if total is not None and not total.is_finite():
                total = Decimal('0.00')

            # Crear instancia con ID manual
            detalle = DetalleCompra(
                id_detalle_compra=contador_id,
                id_compra=compra,           # ← Objeto Compra
                id_producto=producto,       # ← Objeto Producto
                cantidad=cantidad,
                precio=precio,
                total=total,
                stock=None,
                despacho=str(record.get('DESPACHO', '')).strip() if record.get('DESPACHO') else None
            )
            
            contador_id += 1
            detalles_batch.append(detalle)
            registros_procesados += 1

            if len(detalles_batch) >= batch_size:
                DetalleCompra.objects.bulk_create(detalles_batch)
                print(f"✅ Lote guardado: {len(detalles_batch)} registros - Total: {registros_procesados}")
                detalles_batch = []

        except Exception as e:
            errores += 1
            if errores <= 10:
                print(f"❌ Error en registro {idx}: {str(e)[:100]}")
            continue

    if detalles_batch:
        DetalleCompra.objects.bulk_create(detalles_batch)
        print(f"✅ Último lote guardado: {len(detalles_batch)} registros")

    elapsed_time = time.time() - start_time
    mins, secs = divmod(elapsed_time, 60)
    
    print(f"\n{'='*60}")
    print(f"RESUMEN DE MIGRACIÓN DE DETALLE_COMPRA")
    print(f"{'='*60}")
    print(f"Total registros en DBF: {total_registros}")
    print(f"Registros procesados: {registros_procesados}")
    print(f"✅ Registros creados: {contador_id - 1}")
    print(f"❌ Errores: {errores}")
    print(f"⏱️ Tiempo total: {mins} min {secs} seg")
    print(f"{'='*60}")
    
    if productos_no_encontrados:
        print(f"\n⚠️ Productos no encontrados ({len(productos_no_encontrados)}):")
        for codigo, codigo_raw in sorted(productos_no_encontrados)[:20]:
            print(f"   - Código: {codigo} | Original: {codigo_raw}")
        if len(productos_no_encontrados) > 20:
            print(f"   ... y {len(productos_no_encontrados) - 20} más")

if __name__ == '__main__':
    cargar_datos_detalle_compra()
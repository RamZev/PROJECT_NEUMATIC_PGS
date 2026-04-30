# neumatic\data_load\stock_cliente_migra.py
import os
import sys
import django
import logging
import re
from dbfread import DBF
from django.db import transaction, connection
from decimal import Decimal, InvalidOperation
from datetime import datetime

# Configuración básica
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.producto_models import Producto
from apps.ventas.models.factura_models import Factura
from apps.ventas.models.venta_models import StockCliente

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stockcliente_migration_errors.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def limpiar_numero(valor):
    """Limpia un número para convertir a Decimal"""
    if valor is None:
        return None
    
    valor_str = str(valor).strip()
    if not valor_str:
        return None
    
    valor_str = valor_str.replace(' ', '')
    valor_str = valor_str.replace(',', '.')
    valor_str = re.sub(r'[^\d\.-]', '', valor_str)
    
    if valor_str.count('.') > 1:
        partes = valor_str.split('.')
        valor_str = partes[0] + '.' + ''.join(partes[1:])
    
    if valor_str.count('.') == 1 and len(valor_str.split('.')[1]) > 2:
        valor_str = valor_str.replace('.', '')
    
    if not valor_str or valor_str == '-' or valor_str == '.':
        return None
    
    return valor_str

def safe_decimal(value, field_name='', default=Decimal('0')):
    """Conversión segura a Decimal - SIEMPRE devuelve un Decimal (default 0)"""
    if value is None:
        return default
    
    valor_limpio = limpiar_numero(value)
    if valor_limpio is None:
        return default
    
    try:
        return Decimal(valor_limpio)
    except (InvalidOperation, ValueError, TypeError):
        return default

def safe_date(value):
    """Conversión segura para fechas"""
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == '':
        return None
    if isinstance(value, str):
        try:
            return datetime.strptime(value.strip(), '%Y-%m-%d').date()
        except ValueError:
            return None
    if hasattr(value, 'strftime'):
        return value
    return None

def safe_int(value):
    """Conversión segura a entero"""
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == '':
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None

def reset_stockcliente():
    """Elimina los datos existentes y resetea la secuencia"""
    StockCliente.objects.all().delete()
    print("Tabla StockCliente limpiada.")
    
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    try:
        with connection.cursor() as cursor:
            if 'sqlite' in engine:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='stock_cliente';")
                print("Secuencia de ID reseteada (SQLite).")
            elif 'postgresql' in engine:
                cursor.execute("SELECT setval(pg_get_serial_sequence('stock_cliente', 'id_stock_cliente'), 1, false);")
                print("Secuencia de ID reseteada (PostgreSQL).")
            elif 'mssql' in engine or 'sql_server' in engine:
                cursor.execute("DBCC CHECKIDENT ('stock_cliente', RESEED, 0);")
                print("Secuencia de ID reseteada (SQL Server).")
            elif 'mysql' in engine:
                cursor.execute("ALTER TABLE stock_cliente AUTO_INCREMENT = 1;")
                print("Secuencia de ID reseteada (MySQL).")
            else:
                print(f"Motor {engine} no requiere reset manual de secuencia.")
        
        logger.info("Tabla StockCliente limpiada y secuencia reseteada.")
        
    except Exception as e:
        logger.error(f"Error al resetear tabla: {str(e)}")
        raise

def precargar_facturas_sql():
    """Precarga facturas usando SQL directo"""
    print("Precargando facturas...")
    facturas_cache = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_factura FROM factura")
        for row in cursor.fetchall():
            facturas_cache[row[0]] = Factura(id_factura=row[0])
    print(f"Facturas precargadas: {len(facturas_cache)}")
    return facturas_cache

def precargar_productos_sql():
    """Precarga productos usando SQL directo"""
    print("Precargando productos...")
    productos_cache = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_producto FROM producto")
        for row in cursor.fetchall():
            productos_cache[row[0]] = Producto(id_producto=row[0])
    print(f"Productos precargados: {len(productos_cache)}")
    return productos_cache

def cargar_datos():
    """Migración principal - NO se omiten registros por valores nulos de cantidad/retirado"""
    reset_stockcliente()
    
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'stockcliente.DBF')
    table = DBF(dbf_path, encoding='latin-1')
    total_registros = len(table)
    
    logger.info(f"Total registros en DBF: {total_registros}")
    
    # Precargar relaciones
    logger.info("Cargando cache de relaciones...")
    facturas_cache = precargar_facturas_sql()
    productos_cache = precargar_productos_sql()
    
    batch_size = 500
    batch = []
    contador_id = 1
    exitosos = 0
    errores = 0
    
    for idx, record in enumerate(table, 1):
        if idx % 10000 == 0:
            print(f"Progreso: {idx}/{total_registros} registros...")
        
        try:
            id_factura = safe_int(record.get('ID'))
            id_producto = safe_int(record.get('CODIGO'))
            
            # Verificar claves foráneas
            if not id_factura or id_factura not in facturas_cache:
                errores += 1
                logger.warning(f"Registro {idx}: Factura {id_factura} no encontrada. Omitido.")
                continue
            if not id_producto or id_producto not in productos_cache:
                errores += 1
                logger.warning(f"Registro {idx}: Producto {id_producto} no encontrado. Omitido.")
                continue
            
            # Todos los valores se convierten (nulos a 0 o None según corresponda)
            cantidad = safe_decimal(record.get('CANTIDAD'), 'CANTIDAD', Decimal('0'))
            retirado = safe_decimal(record.get('RETIRADO'), 'RETIRADO', Decimal('0'))
            fecha = safe_date(record.get('FECHA'))
            numero = safe_int(record.get('NUMERO'))
            comentario = str(record.get('COMENTARIO', '')).strip() if record.get('COMENTARIO') else None
            
            stock_item = StockCliente(
                id_stock_cliente=contador_id,
                id_factura_id=id_factura,
                id_producto_id=id_producto,
                cantidad=cantidad,
                retirado=retirado,
                fecha_retiro=fecha,
                numero=numero,
                comentario=comentario
            )
            
            batch.append(stock_item)
            contador_id += 1
            
            if len(batch) >= batch_size:
                try:
                    with transaction.atomic():
                        StockCliente.objects.bulk_create(batch)
                    exitosos += len(batch)
                    print(f"Lote guardado: {len(batch)} registros - Total exitosos: {exitosos}")
                    batch = []
                except Exception as e:
                    logger.error(f"Error en lote: {str(e)[:200]}")
                    batch = []
                    errores += len(batch)
                    
        except Exception as e:
            errores += 1
            if errores <= 10:
                logger.error(f"Error en registro {idx}: {str(e)[:150]}")
            continue
    
    # Procesar último lote
    if batch:
        try:
            with transaction.atomic():
                StockCliente.objects.bulk_create(batch)
            exitosos += len(batch)
            print(f"Ultimo lote guardado: {len(batch)} registros")
        except Exception as e:
            logger.error(f"Error en ultimo lote: {str(e)[:200]}")
            errores += len(batch)
    
    # Resumen final
    print(f"\n{'='*60}")
    print(f"RESUMEN DE MIGRACION DE STOCK_CLIENTE")
    print(f"{'='*60}")
    print(f"Total registros procesados: {total_registros}")
    print(f"Registros migrados exitosamente: {exitosos}")
    print(f"Errores (registros omitidos): {errores}")
    if total_registros > 0:
        print(f"Tasa de exito: {exitosos/total_registros*100:.2f}%")
    print(f"{'='*60}")

if __name__ == '__main__':
    cargar_datos()
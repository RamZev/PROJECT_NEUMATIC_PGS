# neumatic\data_load\stockcliente_migra.py
import os
import sys
import django
import logging
from dbfread import DBF
from django.db import transaction, connection
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.db import connection


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
        logging.FileHandler('stockcliente_migration_errors.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def safe_decimal(value, field_name=''):
    """Conversión segura a Decimal con manejo de nulos"""
    if value is None or str(value).strip() == '':
        return None
    
    try:
        str_value = str(value).strip().replace(',', '.')
        return Decimal(str_value)
    except (InvalidOperation, ValueError, TypeError):
        logger.warning(f"Valor inválido en {field_name}: '{value}'")
        return None

def safe_date(value):
    """Conversión segura para fechas con manejo de nulos"""
    if value is None or str(value).strip() == '':
        return None
    try:
        return value if hasattr(value, 'strftime') else None
    except:
        return None

def safe_int(value):
    """Conversión segura a entero con manejo de nulos"""
    if value is None or str(value).strip() == '':
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None

def reset_stockcliente():
    """Elimina los datos existentes y resetea la secuencia"""
    try:
        with transaction.atomic():
            deleted_count = StockCliente.objects.count()
            StockCliente.objects.all().delete()
            logger.info(f"Eliminados {deleted_count} registros existentes")
            
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='stock_cliente';")
    except Exception as e:
        logger.error(f"Error al resetear tabla: {str(e)}")
        raise

def cargar_datos():
    """Migración con manejo específico de campos nulos"""
    reset_stockcliente()
    
    # Ruta del archivo DBF
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'stockcliente.DBF')
    table = DBF(dbf_path, encoding='latin-1')
    
    # Contadores
    counters = {
        'total': 0,
        'exitosos': 0,
        'facturas_no_encontradas': 0,
        'productos_no_encontrados': 0,
        'decimales_invalidos': 0,
        'fechas_invalidas': 0,
        'enteros_invalidos': 0,
        'otros_errores': 0
    }
    
    # Precargar relaciones
    logger.info("Cargando cache de relaciones...")
    facturas_cache = {f.id_factura: f for f in Factura.objects.all()}
    productos_cache = {p.id_producto: p for p in Producto.objects.all()}
    
    # Procesamiento por lotes
    batch_size = 1000
    batch = []
    
    for record in table:
        counters['total'] += 1
        record_id = record.get('ID', 'N/A')
        
        try:
            # Validar relaciones obligatorias
            factura = facturas_cache.get(record['ID'])
            producto = productos_cache.get(record['CODIGO'])
            
            if not factura:
                counters['facturas_no_encontradas'] += 1
                logger.warning(f"Factura no encontrada: ID {record['ID']}")
                continue
            if not producto:
                counters['productos_no_encontrados'] += 1
                logger.warning(f"Producto no encontrado: CODIGO {record['CODIGO']}")
                continue
            
            # Convertir valores con manejo de nulos
            cantidad = safe_decimal(record.get('CANTIDAD'), 'CANTIDAD')
            retirado = safe_decimal(record.get('RETIRADO'), 'RETIRADO')
            fecha = safe_date(record.get('FECHA'))
            numero = safe_int(record.get('NUMERO'))
            
            # Contar conversiones fallidas
            if retirado is None and record.get('RETIRADO') not in [None, '']:
                counters['decimales_invalidos'] += 1
            if fecha is None and record.get('FECHA') not in [None, '']:
                counters['fechas_invalidas'] += 1
            if numero is None and record.get('NUMERO') not in [None, '']:
                counters['enteros_invalidos'] += 1
            
            # Crear instancia y validar antes de agregar al batch
            stock_item = StockCliente(
                id_factura=factura,
                id_producto=producto,
                cantidad=cantidad,
                retirado=retirado,
                fecha_retiro=fecha,
                numero=numero,
                comentario=record.get('COMENTARIO', '').strip() or None
            )
            
            # Validación adicional: verificar que los valores Decimal estén dentro de los límites del modelo
            if cantidad is not None:
                # Validar que no exceda max_digits=7, decimal_places=2
                if abs(cantidad) > Decimal('99999.99'):
                    logger.warning(f"CANTIDAD excede límites: {cantidad} en registro ID {record_id}")
                    cantidad = None
            
            if retirado is not None:
                # Validar que no exceda max_digits=7, decimal_places=2
                if abs(retirado) > Decimal('99999.99'):
                    logger.warning(f"RETIRADO excede límites: {retirado} en registro ID {record_id}")
                    retirado = None
            
            batch.append(stock_item)
            
            # Procesar lote completo
            if len(batch) >= batch_size:
                try:
                    with transaction.atomic():
                        StockCliente.objects.bulk_create(batch)
                    counters['exitosos'] += len(batch)
                    logger.info(f"Lote guardado: {len(batch)} registros")
                    batch = []
                except Exception as e:
                    logger.error(f"Error en lote de {len(batch)} registros: {str(e)}")
                    logger.error(f"Último registro procesado: ID={record_id}, CODIGO={record.get('CODIGO')}")
                    
                    # Probar registro por registro para identificar el problema
                    logger.info("Identificando registro problemático...")
                    problematic_record = None
                    for i, item in enumerate(batch):
                        try:
                            # Intentar guardar individualmente
                            with transaction.atomic():
                                item.save()
                            counters['exitosos'] += 1
                        except Exception as individual_error:
                            problematic_record = i
                            logger.error(f"Registro problemático encontrado en posición {i}:")
                            logger.error(f"  ID Factura: {item.id_factura.id_factura if item.id_factura else 'None'}")
                            logger.error(f"  ID Producto: {item.id_producto.id_producto if item.id_producto else 'None'}")
                            logger.error(f"  Cantidad: {item.cantidad}")
                            logger.error(f"  Retirado: {item.retirado}")
                            logger.error(f"  Fecha: {item.fecha_retiro}")
                            logger.error(f"  Número: {item.numero}")
                            logger.error(f"  Comentario: {item.comentario}")
                            logger.error(f"  Error específico: {str(individual_error)}")
                            counters['otros_errores'] += 1
                    
                    batch = []  # Limpiar el lote después del error
                    
        except Exception as e:
            counters['otros_errores'] += 1
            logger.error(f"Error procesando registro {record_id}: {str(e)}")
            logger.error(f"Datos del registro: {record}")
            continue

    # Procesar último lote
    if batch:
        try:
            with transaction.atomic():
                StockCliente.objects.bulk_create(batch)
            counters['exitosos'] += len(batch)
            logger.info(f"Último lote guardado: {len(batch)} registros")
        except Exception as e:
            logger.error(f"Error en último lote: {str(e)}")
            # Guardar individualmente los registros restantes
            for item in batch:
                try:
                    with transaction.atomic():
                        item.save()
                    counters['exitosos'] += 1
                except Exception as individual_error:
                    counters['otros_errores'] += 1
                    logger.error(f"Error guardando registro individual:")
                    logger.error(f"  ID Factura: {item.id_factura.id_factura if item.id_factura else 'None'}")
                    logger.error(f"  ID Producto: {item.id_producto.id_producto if item.id_producto else 'None'}")
                    logger.error(f"  Error: {str(individual_error)}")

    # Resumen final
    logger.info("\nRESUMEN FINAL:")
    logger.info(f"Total registros procesados: {counters['total']}")
    logger.info(f"Registros migrados exitosamente: {counters['exitosos']}")
    logger.info(f"Facturas no encontradas: {counters['facturas_no_encontradas']}")
    logger.info(f"Productos no encontrados: {counters['productos_no_encontrados']}")
    logger.info(f"Decimales inválidos (RETIRADO): {counters['decimales_invalidos']}")
    logger.info(f"Fechas inválidas: {counters['fechas_invalidas']}")
    logger.info(f"Enteros inválidos (NUMERO): {counters['enteros_invalidos']}")
    logger.info(f"Otros errores: {counters['otros_errores']}")
    
    if counters['total'] > 0:
        logger.info(f"Tasa de éxito: {counters['exitosos']/counters['total']*100:.2f}%")
    else:
        logger.info("Tasa de éxito: 0%")

if __name__ == '__main__':
    cargar_datos()
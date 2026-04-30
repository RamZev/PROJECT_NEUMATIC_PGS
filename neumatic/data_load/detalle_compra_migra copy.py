import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from decimal import Decimal, InvalidOperation, getcontext, setcontext, DefaultContext
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
    """Conversión robusta a Decimal con diagnóstico mejorado"""
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
    """Proceso de migración optimizado con manejo robusto de errores, reinicio por bloques Y reinicio del contexto decimal"""
    start_time = time.time()
    reset_detalle_compra()

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

    # Configuración de procesamiento
    batch_size = 2000
    block_size = 150000  # 🆕 Reiniciar lectura y contexto cada 150k registros
    registros_procesados = 0
    errores = 0
    productos_no_encontrados = set()
    bloque = 0

    # Intentar obtener total de registros (opcional)
    try:
        temp_table = DBF(dbf_path, encoding='latin-1')
        total_estimado = len(temp_table)
        logger.info(f"Total registros estimados: {total_estimado}")
    except Exception as e:
        logger.warning(f"No se pudo obtener conteo total: {e}")
        total_estimado = "Desconocido"

    logger.info("Iniciando migración por bloques...")

    while True:
        logger.info(f"--- Iniciando Bloque {bloque + 1} (registros {bloque * block_size} a {(bloque + 1) * block_size - 1}) ---")

        # 🆕 REINICIAR CONTEXTO DECIMAL (¡CLAVE PARA EVITAR CORRUPCIÓN ACUMULADA!)
        setcontext(DefaultContext)

        # 🆕 ABRIR ARCHIVO DBF PARA ESTE BLOQUE
        try:
            table = DBF(dbf_path, encoding='latin-1')
        except UnicodeDecodeError:
            table = DBF(dbf_path, encoding='utf-8')

        # Leer registros del bloque actual
        records_in_block = []
        for idx, record in enumerate(table):
            # Saltar registros anteriores al bloque
            if idx < bloque * block_size:
                continue
            # Detenerse al final del bloque
            if idx >= (bloque + 1) * block_size:
                break
            records_in_block.append((idx + 1, record))  # Guardar índice global y registro

        # Si no hay registros en este bloque, terminar
        if not records_in_block:
            logger.info("No se encontraron más registros. Fin del procesamiento.")
            break

        logger.info(f"Bloque {bloque + 1}: Procesando {len(records_in_block)} registros...")

        detalles_batch = []

        # Procesar cada registro del bloque
        for idx_global, record in records_in_block:
            try:
                # Obtener ID de compra
                id_compra = safe_int(record.get('ID'), 'ID_compra')
                if id_compra is None:
                    logger.warning(f"Registro {idx_global} sin ID de compra válido")
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

                # Convertir campos decimales
                cantidad = safe_decimal(record.get('CANTIDAD'), 'CANTIDAD', Decimal('0.00'))
                precio = safe_decimal(record.get('PRECIO'), 'PRECIO', Decimal('0.00'))
                total = safe_decimal(record.get('TOTAL'), 'TOTAL', Decimal('0.00'))

                # 🛡️ VALIDACIÓN EXTRA: Asegurar que son finitos justo antes de crear el modelo
                valores = {'cantidad': cantidad, 'precio': precio, 'total': total}
                corregido = False
                for key, val in valores.items():
                    if val is not None and not val.is_finite():
                        logger.warning(f"Valor no finito detectado en {key.upper()} (registro {idx_global}): {val}. Reemplazando por 0.00")
                        if key == 'cantidad':
                            cantidad = Decimal('0.00')
                        elif key == 'precio':
                            precio = Decimal('0.00')
                        elif key == 'total':
                            total = Decimal('0.00')
                        corregido = True

                # Crear instancia
                detalle = DetalleCompra(
                    id_compra=compra,
                    id_producto=producto,
                    cantidad=cantidad,
                    precio=precio,
                    total=total,
                    despacho=str(record.get('DESPACHO', '')).strip()
                )
                
                detalles_batch.append(detalle)
                registros_procesados += 1

                # Guardar por lotes pequeños
                if len(detalles_batch) >= batch_size:
                    with transaction.atomic():
                        DetalleCompra.objects.bulk_create(detalles_batch)
                    logger.info(f"Lote guardado: {len(detalles_batch)} registros (bloque {bloque + 1})")
                    detalles_batch = []

                # Log de progreso cada 10k registros globales
                if registros_procesados % 10000 == 0:
                    logger.info(f"Progreso global: {registros_procesados} registros procesados")

            except Exception as e:
                errores += 1
                logger.error(f"Error en compra ID {id_compra} - Registro {idx_global}: {str(e)}")
                logger.debug(f"Registro problemático: {record}")
                continue

        # Guardar restos del bloque
        if detalles_batch:
            with transaction.atomic():
                DetalleCompra.objects.bulk_create(detalles_batch)
            logger.info(f"Último lote del bloque {bloque + 1} guardado: {len(detalles_batch)} registros")

        bloque += 1

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
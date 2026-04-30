# neumatic\data_load\actualiza_factura_id_caja_mult.py
import os
import sys
import django
import time
import logging
from datetime import datetime
from django.db import connection
from django.conf import settings

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.factura_models import Factura
from apps.maestros.models.base_models import ComprobanteVenta
from apps.ventas.models.caja_models import Caja

# Configurar logging
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file = os.path.join(LOG_DIR, 'actualiza_factura_id_caja.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def actualizar_id_caja_facturas():
    """
    Asigna id_caja al modelo Factura basado en:
    1. id_comprobante_venta.mult_caja ≠ 0
    2. Factura.id_caja es NULL/vacío
    3. Busca en Caja por id_sucursal y fecha_comprobante
    """
    start_time = time.time()
    
    logger.info("=" * 60)
    logger.info("INICIANDO PROCESO DE ACTUALIZACIÓN DE ID_CAJA EN FACTURAS")
    logger.info("=" * 60)
    
    # === 1. Obtener IDs de facturas con mult_caja != 0 y id_caja NULL ===
    # Usar values_list para evitar cargar objetos completos
    facturas_list = list(Factura.objects.exclude(
        id_comprobante_venta__mult_caja=0
    ).filter(
        id_caja__isnull=True
    ).values_list(
        'id_factura', 'id_sucursal_id', 'fecha_comprobante', 
        'compro', 'numero_comprobante', 'id_cliente__nombre_cliente'
    ))
    
    total_facturas = len(facturas_list)
    logger.info(f"Facturas sin id_caja con mult_caja != 0: {total_facturas}")
    
    if total_facturas == 0:
        logger.info("No hay facturas para procesar.")
        return

    # === 2. Precargar cajas en caché ===
    logger.info("Precargando cajas...")
    cajas_cache = {}
    for c in Caja.objects.values_list('id_caja', 'id_sucursal_id', 'fecha_caja'):
        key = (c[1], c[2])  # (id_sucursal, fecha_caja)
        cajas_cache[key] = c[0]
    logger.info(f"Cajas precargadas: {len(cajas_cache)}")

    # === 3. Procesamiento por lotes ===
    batch_size = 2000
    facturas_actualizar = []  # Lista de (id_factura, id_caja)
    facturas_actualizadas = 0
    facturas_no_encontradas = 0
    errores = 0
    
    # Archivo de log detallado para facturas no encontradas
    detalle_log_file = os.path.join(LOG_DIR, 'facturas_sin_caja_detalle.txt')
    
    with open(detalle_log_file, 'w', encoding='utf-8') as detalle_log:
        detalle_log.write("FACTURAS SIN CAJA ASIGNADA - DETALLE\n")
        detalle_log.write("=" * 80 + "\n")
        detalle_log.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        detalle_log.write("=" * 80 + "\n\n")
        
        for idx, (id_factura, id_sucursal, fecha_comprobante, compro, numero, nombre_cliente) in enumerate(facturas_list, 1):
            try:
                if not id_sucursal or not fecha_comprobante:
                    errores += 1
                    logger.warning(f"Factura {id_factura}: falta sucursal o fecha")
                    continue
                
                # Buscar caja en caché
                key = (id_sucursal, fecha_comprobante)
                id_caja = cajas_cache.get(key)
                
                if id_caja:
                    facturas_actualizar.append((id_factura, id_caja))
                    facturas_actualizadas += 1
                else:
                    facturas_no_encontradas += 1
                    
                    # Registrar en archivo detallado
                    detalle_log.write(
                        f"Factura ID: {id_factura}\n"
                        f"Comprobante: {compro} - {numero}\n"
                        f"Fecha: {fecha_comprobante}\n"
                        f"Sucursal ID: {id_sucursal}\n"
                        f"Cliente: {nombre_cliente or 'N/A'}\n"
                        f"{'-' * 40}\n"
                    )
                    
                    if facturas_no_encontradas <= 10:
                        logger.warning(
                            f"Factura {id_factura}: No se encontró caja para sucursal={id_sucursal}, fecha={fecha_comprobante}"
                        )
                
                # Guardar por lotes
                if len(facturas_actualizar) >= batch_size:
                    with connection.cursor() as cursor:
                        for factura_id, caja_id in facturas_actualizar:
                            cursor.execute(
                                "UPDATE factura SET id_caja_id = %s WHERE id_factura = %s",
                                [caja_id, factura_id]
                            )
                    logger.info(f"Lote guardado: {len(facturas_actualizar)} facturas actualizadas - Total: {facturas_actualizadas}")
                    facturas_actualizar = []
                
                if idx % 2000 == 0:
                    logger.info(f"Procesados: {idx}/{total_facturas}")

            except Exception as e:
                errores += 1
                logger.error(f"Error procesando factura {id_factura}: {str(e)}")
                continue
        
        # Guardar último lote
        if facturas_actualizar:
            with connection.cursor() as cursor:
                for factura_id, caja_id in facturas_actualizar:
                    cursor.execute(
                        "UPDATE factura SET id_caja_id = %s WHERE id_factura = %s",
                        [caja_id, factura_id]
                    )
            logger.info(f"Último lote guardado: {len(facturas_actualizar)} facturas actualizadas - Total final: {facturas_actualizadas}")

    # Resumen final
    elapsed_time = time.time() - start_time
    mins = int(elapsed_time // 60)
    secs = int(elapsed_time % 60)
    
    logger.info("=" * 60)
    logger.info("RESUMEN DEL PROCESO")
    logger.info("=" * 60)
    logger.info(f"Facturas procesadas: {total_facturas}")
    logger.info(f"Facturas actualizadas: {facturas_actualizadas}")
    logger.info(f"Facturas sin caja encontrada: {facturas_no_encontradas}")
    logger.info(f"Errores: {errores}")
    logger.info(f"Tiempo total: {mins} min {secs} seg")
    logger.info(f"Log detallado guardado en: {detalle_log_file}")
    logger.info(f"Log general guardado en: {log_file}")
    
    # Escribir resumen en archivo detallado
    with open(detalle_log_file, 'a', encoding='utf-8') as detalle_log:
        detalle_log.write("\n" + "=" * 80 + "\n")
        detalle_log.write("RESUMEN DEL PROCESO\n")
        detalle_log.write("=" * 80 + "\n")
        detalle_log.write(f"Total facturas procesadas: {total_facturas}\n")
        detalle_log.write(f"Facturas actualizadas: {facturas_actualizadas}\n")
        detalle_log.write(f"Facturas sin caja encontrada: {facturas_no_encontradas}\n")
        detalle_log.write(f"Errores: {errores}\n")
        detalle_log.write(f"Tiempo total: {mins} min {secs} seg\n")
        detalle_log.write(f"Fecha finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == '__main__':
    actualizar_id_caja_facturas()
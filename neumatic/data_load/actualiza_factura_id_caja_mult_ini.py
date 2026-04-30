# neumatic\data_load\actualiza_factura_id_caja_mult.py
import os
import sys
import django
import logging
from datetime import datetime

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
    logger.info("=" * 60)
    logger.info("INICIANDO PROCESO DE ACTUALIZACIÓN DE ID_CAJA EN FACTURAS")
    logger.info("=" * 60)
    
    # Filtrar facturas donde:
    # 1. mult_caja del comprobante es distinto de cero
    # 2. id_caja de la factura es NULL
    # CORRECCIÓN: Usar exclude() en lugar de __ne
    facturas = Factura.objects.exclude(
        id_comprobante_venta__mult_caja=0  # Excluir donde mult_caja = 0
    ).filter(
        id_caja__isnull=True  # id_caja no asignado
    ).select_related(
        'id_comprobante_venta',
        'id_sucursal'
    ).iterator(chunk_size=1000)
    
    # ALTERNATIVA 2: Usando Q objects para mayor claridad
    # from django.db.models import Q
    # facturas = Factura.objects.filter(
    #     ~Q(id_comprobante_venta__mult_caja=0),  # mult_caja ≠ 0
    #     Q(id_caja__isnull=True)
    # ).select_related(...)
    
    facturas_procesadas = 0
    facturas_actualizadas = 0
    facturas_no_encontradas = 0
    errores = 0
    bloque_actual = 0
    
    # Archivo de log detallado para facturas no encontradas
    detalle_log_file = os.path.join(LOG_DIR, 'facturas_sin_caja_detalle.txt')
    
    with open(detalle_log_file, 'w', encoding='utf-8') as detalle_log:
        detalle_log.write("FACTURAS SIN CAJA ASIGNADA - DETALLE\n")
        detalle_log.write("=" * 80 + "\n")
        detalle_log.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        detalle_log.write("=" * 80 + "\n\n")
        
        for factura in facturas:
            facturas_procesadas += 1
            
            try:
                # Verificar mult_caja (ya filtrado, pero por seguridad)
                if factura.id_comprobante_venta.mult_caja == 0:
                    logger.debug(f"Factura {factura.id_factura}: mult_caja=0, omitiendo")
                    continue
                
                # Obtener datos de búsqueda
                sucursal = factura.id_sucursal
                fecha_comprobante = factura.fecha_comprobante
                
                if not sucursal or not fecha_comprobante:
                    logger.warning(f"Factura {factura.id_factura}: falta sucursal o fecha")
                    errores += 1
                    continue
                
                # Buscar caja (NO se requiere que esté abierta)
                caja_encontrada = Caja.objects.filter(
                    id_sucursal=sucursal,
                    fecha_caja=fecha_comprobante
                ).first()
                
                if caja_encontrada:
                    # Asignar id_caja
                    factura.id_caja = caja_encontrada
                    factura.save(update_fields=['id_caja'])
                    facturas_actualizadas += 1
                    
                    logger.debug(
                        f"Factura {factura.id_factura}: "
                        f"Caja #{caja_encontrada.id_caja} asignada "
                        f"(sucursal: {sucursal}, fecha: {fecha_comprobante})"
                    )
                else:
                    facturas_no_encontradas += 1
                    
                    # Registrar en archivo detallado
                    detalle_log.write(
                        f"Factura ID: {factura.id_factura}\n"
                        f"Comprobante: {factura.compro} - {factura.numero_comprobante}\n"
                        f"Fecha: {fecha_comprobante}\n"
                        f"Sucursal: {sucursal.id_sucursal} - {sucursal.nombre_sucursal}\n"
                        f"Cliente: {factura.id_cliente.nombre_cliente if factura.id_cliente else 'N/A'}\n"
                        f"Comprobante mult_caja: {factura.id_comprobante_venta.mult_caja}\n"
                        f"{'-' * 40}\n"
                    )
                    
                    logger.warning(
                        f"Factura {factura.id_factura}: "
                        f"No se encontró caja para sucursal={sucursal.id_sucursal}, "
                        f"fecha={fecha_comprobante}"
                    )
                
                # Mostrar progreso cada 1000 facturas
                if facturas_procesadas % 1000 == 0:
                    bloque_actual += 1
                    logger.info(f"Bloque {bloque_actual} procesado: {facturas_procesadas} facturas revisadas")
                    
            except Exception as e:
                errores += 1
                logger.error(f"Error procesando factura {factura.id_factura}: {str(e)}")
                continue
    
    # Resumen final
    logger.info("=" * 60)
    logger.info("RESUMEN DEL PROCESO")
    logger.info("=" * 60)
    logger.info(f"Facturas procesadas: {facturas_procesadas}")
    logger.info(f"Facturas actualizadas: {facturas_actualizadas}")
    logger.info(f"Facturas sin caja encontrada: {facturas_no_encontradas}")
    logger.info(f"Errores: {errores}")
    logger.info(f"Log detallado guardado en: {detalle_log_file}")
    logger.info(f"Log general guardado en: {log_file}")
    
    # Escribir resumen en archivo detallado
    with open(detalle_log_file, 'a', encoding='utf-8') as detalle_log:
        detalle_log.write("\n" + "=" * 80 + "\n")
        detalle_log.write("RESUMEN DEL PROCESO\n")
        detalle_log.write("=" * 80 + "\n")
        detalle_log.write(f"Total facturas procesadas: {facturas_procesadas}\n")
        detalle_log.write(f"Facturas actualizadas: {facturas_actualizadas}\n")
        detalle_log.write(f"Facturas sin caja encontrada: {facturas_no_encontradas}\n")
        detalle_log.write(f"Errores: {errores}\n")
        detalle_log.write(f"Fecha finalización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == '__main__':
    actualizar_id_caja_facturas()
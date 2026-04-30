# neumatic\data_load\vincular_factura_caja.py
import os
import sys
import django
import time
import logging
from django.db import connection
from django.db import transaction
from django.conf import settings

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.caja_models import CajaDetalle, Caja
from apps.ventas.models.factura_models import Factura

# Configuración de logging
logging.basicConfig(
    filename='vincular_factura_caja.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def vincular_facturas_con_cajas():
    """Actualiza el campo id_caja en Factura usando datos de CajaDetalle"""
    try:
        start_time = time.time()
        print("Iniciando vinculación de Facturas con Cajas desde CajaDetalle...")

        # Precargar cajas usando values_list (id_caja -> existe o no)
        print("Precargando cajas...")
        cajas_cache = set()
        for c in Caja.objects.values_list('id_caja', flat=True):
            cajas_cache.add(c)
        print(f"Cajas precargadas: {len(cajas_cache)}")

        # Obtener registros relevantes: solo con idventas > 0
        # Usar values_list para evitar cargar objetos completos
        caja_detalles_list = list(CajaDetalle.objects.filter(idventas__gt=0).values_list('pk', 'idventas', 'id_caja_id'))
        total_registros = len(caja_detalles_list)
        print(f"Registros de CajaDetalle con idventas > 0: {total_registros}")

        if total_registros == 0:
            print("No hay registros con idventas > 0. Nada que procesar.")
            return

        # Contadores
        actualizados = 0
        no_encontrados = 0
        errores = 0
        batch_size = 2000
        facturas_actualizar = []

        for idx, (detalle_pk, id_venta, id_caja_db) in enumerate(caja_detalles_list, 1):
            try:
                if not id_caja_db:
                    mensaje = f"id_caja_detalle={detalle_pk}, idventa={id_venta}, id_caja=None"
                    print(f"Caja nula: {mensaje}")
                    logger.warning(mensaje)
                    continue

                # Verificar si la caja existe
                if id_caja_db not in cajas_cache:
                    mensaje = f"id_caja_detalle={detalle_pk}, idventa={id_venta}, id_caja={id_caja_db} | Caja no existe"
                    print(f"Error: {mensaje}")
                    logger.error(mensaje)
                    errores += 1
                    continue

                # Verificar si la factura existe
                if not Factura.objects.filter(id_factura=id_venta).exists():
                    no_encontrados += 1
                    mensaje = f"id_caja_detalle={detalle_pk}, idventa={id_venta}, id_caja={id_caja_db}"
                    print(f"Factura no encontrada: {mensaje}")
                    logger.warning(mensaje)
                    continue

                # Agregar a la lista para actualizar
                facturas_actualizar.append((id_venta, id_caja_db))

                if len(facturas_actualizar) >= batch_size:
                    with transaction.atomic():
                        for factura_id, caja_id in facturas_actualizar:
                            Factura.objects.filter(id_factura=factura_id).update(id_caja_id=caja_id)
                        actualizados += len(facturas_actualizar)
                        print(f"Lote guardado: {len(facturas_actualizar)} facturas actualizadas - Total: {actualizados}")
                        facturas_actualizar = []

                if idx % 2000 == 0:
                    print(f"Procesados: {idx}/{total_registros}")

            except Exception as e:
                errores += 1
                mensaje_error = f"id_caja_detalle={detalle_pk}, idventa={id_venta}, id_caja={id_caja_db} | Error: {str(e)}"
                print(f"Error: {mensaje_error}")
                logger.error(mensaje_error)
                continue

        # Guardar último lote
        if facturas_actualizar:
            with transaction.atomic():
                for factura_id, caja_id in facturas_actualizar:
                    Factura.objects.filter(id_factura=factura_id).update(id_caja_id=caja_id)
                actualizados += len(facturas_actualizar)
                print(f"Último lote guardado: {len(facturas_actualizar)} facturas actualizadas - Total: {actualizados}")

        # Resumen final
        elapsed_time = time.time() - start_time
        print("\n=== RESUMEN FINAL ===")
        print(f"Total CajaDetalle procesados (idventas > 0): {total_registros}")
        print(f"Facturas actualizadas: {actualizados}")
        print(f"Facturas no encontradas: {no_encontrados}")
        print(f"Errores: {errores}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")

        logger.info("=== RESUMEN FINAL ===")
        logger.info(f"Facturas actualizadas: {actualizados}")
        logger.info(f"Facturas no encontradas: {no_encontrados}")
        logger.info(f"Errores: {errores}")

    except Exception as e:
        mensaje_fatal = f"ERROR FATAL: {str(e)}"
        print(mensaje_fatal)
        logger.critical(mensaje_fatal)
        raise

if __name__ == '__main__':
    vincular_facturas_con_cajas()
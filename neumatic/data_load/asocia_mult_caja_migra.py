# neumatic\data_load\asocia_mult_caja_migra.py
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

# Modelos
from apps.ventas.models.factura_models import Factura
from apps.ventas.models.caja_models import Caja

# Logging
logging.basicConfig(
    filename='asocia_mult_caja_migra.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def asocia_mult_caja_migra():
    """Asocia id_caja en Factura basado en mult_caja y coincidencia de sucursal/fecha"""
    print("Iniciando asociación de caja para facturas con mult_caja...")
    start_time = time.time()
    
    # === 1. Obtener IDs de facturas con mult_caja != 0 ===
    # Usar values_list para evitar cargar objetos completos
    facturas_list = list(Factura.objects.filter(
        id_comprobante_venta__isnull=False,
        id_comprobante_venta__mult_caja__isnull=False
    ).exclude(
        id_comprobante_venta__mult_caja=0
    ).values_list(
        'id_factura', 'id_sucursal_id', 'fecha_comprobante'
    ))
    
    total_facturas = len(facturas_list)
    print(f"Facturas con mult_caja != 0: {total_facturas}")
    
    if total_facturas == 0:
        print("No hay facturas con mult_caja != 0. Nada que hacer.")
        return

    # === 2. Precargar cajas en caché ===
    print("Precargando cajas...")
    cajas_cache = {}
    for c in Caja.objects.values_list('id_caja', 'id_sucursal_id', 'fecha_caja'):
        key = (c[1], c[2])  # (id_sucursal, fecha_caja)
        cajas_cache[key] = c[0]
    print(f"Cajas precargadas: {len(cajas_cache)}")

    # === 3. Procesamiento por lotes ===
    batch_size = 2000
    facturas_actualizar = []  # Lista de (id_factura, id_caja)
    actualizados = 0
    no_encontrados = 0
    errores = 0

    for idx, (id_factura, id_sucursal, fecha_comprobante) in enumerate(facturas_list, 1):
        try:
            if not id_sucursal or not fecha_comprobante:
                continue

            # Buscar caja en caché
            key = (id_sucursal, fecha_comprobante)
            id_caja = cajas_cache.get(key)
            
            if not id_caja:
                no_encontrados += 1
                mensaje = f"Factura ID={id_factura}, id_sucursal={id_sucursal}, fecha={fecha_comprobante} | Caja no encontrada"
                if no_encontrados <= 10:
                    print(mensaje)
                logger.warning(mensaje)
                continue

            # Agregar a lista para actualizar
            facturas_actualizar.append((id_factura, id_caja))
            actualizados += 1

            # Guardar por lotes
            if len(facturas_actualizar) >= batch_size:
                with transaction.atomic():
                    for factura_id, caja_id in facturas_actualizar:
                        Factura.objects.filter(id_factura=factura_id).update(id_caja_id=caja_id)
                    print(f"Lote guardado: {len(facturas_actualizar)} facturas actualizadas - Total: {actualizados}")
                facturas_actualizar = []

            if idx % 2000 == 0:
                print(f"Procesados: {idx}/{total_facturas}")

        except Exception as e:
            errores += 1
            mensaje_error = f"Error en Factura ID={id_factura}: {str(e)}"
            logger.error(mensaje_error)
            if errores <= 10:
                print(mensaje_error)
            continue

    # Guardar último lote
    if facturas_actualizar:
        with transaction.atomic():
            for factura_id, caja_id in facturas_actualizar:
                Factura.objects.filter(id_factura=factura_id).update(id_caja_id=caja_id)
            print(f"Último lote guardado: {len(facturas_actualizar)} facturas actualizadas - Total final: {actualizados}")

    # === Resumen final ===
    elapsed_time = time.time() - start_time
    mins = int(elapsed_time // 60)
    secs = int(elapsed_time % 60)
    
    print(f"\n{'='*60}")
    print("RESUMEN FINAL - ASOCIACIÓN MULT_CAJA")
    print(f"{'='*60}")
    print(f"Facturas procesadas: {total_facturas}")
    print(f"Facturas actualizadas (id_caja): {actualizados}")
    print(f"Cajas no encontradas: {no_encontrados}")
    print(f"Errores: {errores}")
    print(f"Tiempo total: {mins} min {secs} seg")
    print(f"{'='*60}")
    print("Log detallado: asocia_mult_caja_migra.log")

if __name__ == '__main__':
    asocia_mult_caja_migra()
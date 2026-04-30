# neumatic\data_load\asocia_mult_caja_migra.py
import os
import sys
import django
import logging
from django.db import transaction

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
    print("<info>Iniciando asociación de caja para facturas con mult_caja...</info>")
    
    # === 1. Filtrar facturas con mult_caja != 0 ===
    facturas_filtradas = Factura.objects.filter(
        id_comprobante_venta__isnull=False,
        id_comprobante_venta__mult_caja__isnull=False
    ).exclude(
        id_comprobante_venta__mult_caja=0  # ← ¡CORRECTO! Así se hace "distinto de cero"
    ).select_related('id_comprobante_venta')
    
    total_facturas = facturas_filtradas.count()
    print(f"<info>Facturas con mult_caja != 0: {total_facturas}</info>")
    
    if total_facturas == 0:
        print("<info>No hay facturas con mult_caja != 0. Nada que hacer.</info>")
        return

    # === 2. Procesamiento por lotes ===
    batch_size = 2000
    facturas_a_actualizar = []
    actualizados = 0
    no_encontrados = 0

    for factura in facturas_filtradas:
        try:
            id_sucursal = factura.id_sucursal_id  # ID directo (más eficiente)
            fecha_comprobante = factura.fecha_comprobante

            if not id_sucursal or not fecha_comprobante:
                continue

            # Buscar caja por id_sucursal y fecha_caja
            try:
                caja = Caja.objects.get(
                    id_sucursal_id=id_sucursal,
                    fecha_caja=fecha_comprobante
                )
            except Caja.DoesNotExist:
                no_encontrados += 1
                mensaje = f"Factura ID={factura.pk}, id_sucursal={id_sucursal}, fecha={fecha_comprobante} | Caja no encontrada"
                logger.warning(mensaje)
                continue

            # Asignar id_caja
            factura.id_caja = caja
            facturas_a_actualizar.append(factura)
            actualizados += 1

            # Guardar por lotes
            if len(facturas_a_actualizar) >= batch_size:
                with transaction.atomic():
                    Factura.objects.bulk_update(facturas_a_actualizar, ['id_caja'])
                    print(f"<success>Lote guardado: {len(facturas_a_actualizar)} facturas actualizadas</success>")
                facturas_a_actualizar = []

        except Exception as e:
            mensaje_error = f"Error en Factura ID={factura.pk}: {str(e)}"
            logger.error(mensaje_error)
            continue

    # Guardar último lote
    if facturas_a_actualizar:
        with transaction.atomic():
            Factura.objects.bulk_update(facturas_a_actualizar, ['id_caja'])
            print(f"<success>Último lote guardado: {len(facturas_a_actualizar)} facturas actualizadas</success>")

    # === Resumen final ===
    print(f"\n<info>{'='*50}</info>")
    print("<info>RESUMEN FINAL</info>")
    print(f"<info>Facturas procesadas: {total_facturas}</info>")
    print(f"<success>Facturas actualizadas (id_caja): {actualizados}</success>")
    print(f"<warning>Cajas no encontradas: {no_encontrados}</warning>")
    print(f"<info>Log detallado: asocia_mult_caja_migra.log</info>")

if __name__ == '__main__':
    asocia_mult_caja_migra()
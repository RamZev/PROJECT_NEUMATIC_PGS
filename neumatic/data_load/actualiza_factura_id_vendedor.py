# neumatic\data_load\actualiza_factura_id_vendedor.py
import os
import sys
import django

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.factura_models import Factura
from apps.maestros.models.cliente_models import Cliente
from apps.maestros.models.vendedor_models import Vendedor

def asignar_vendedor_a_facturas():
    """Asigna id_vendedor al modelo Factura basado en id_cliente."""
    # Obtener todas las facturas y procesarlas en bloques de 1000
    facturas = Factura.objects.all().iterator(chunk_size=1000)
    facturas_actualizadas = 0
    bloque_actual = 0

    for factura in facturas:
        # Obtener el cliente asociado a la factura
        cliente = factura.id_cliente  # id_cliente es una instancia de Cliente

        # Buscar el vendedor asociado al cliente
        try:
            vendedor = cliente.id_vendedor  # id_vendedor es una instancia de Vendedor

            # Asignar el id_vendedor a la factura
            factura.id_vendedor = vendedor  # Asignamos la instancia de Vendedor
            factura.save()
            facturas_actualizadas += 1
        except AttributeError:
            print(f"El cliente asociado a la factura {factura.id_factura} no tiene un vendedor asignado.")
        except Vendedor.DoesNotExist:
            print(f"Vendedor no encontrado para el cliente con ID '{cliente.id_cliente}' en factura {factura.id_factura}")

        # Mostrar mensaje cada 1000 facturas procesadas
        if facturas_actualizadas % 1000 == 0:
            bloque_actual += 1
            print(f"Bloque {bloque_actual} procesado: {facturas_actualizadas} facturas actualizadas.")

    # Mensaje final
    print(f"Proceso completado. Total facturas actualizadas: {facturas_actualizadas}")

if __name__ == '__main__':
    asignar_vendedor_a_facturas()
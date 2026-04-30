# neumatic\data_load\actualiza_factura_claves.py
import os
import sys
import django
from dbfread import DBF

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import ComprobanteVenta, ProductoDeposito
from apps.maestros.models.sucursal_models import Sucursal
from apps.ventas.models.factura_models import Factura

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'facturas.DBF')

def asignar_claves_a_facturas():
    """Asigna id_sucursal, id_deposito e id_comprobante_venta al modelo Factura."""
    # Leer la tabla facturas.DBF
    print("Cargando datos desde la tabla facturas.DBF...")
    table = DBF(dbf_path, encoding='latin-1')

    # Crear un diccionario para buscar rápidamente por ID en la tabla DBF
    dbf_data = {
        record['ID']: {
            'sucursal': record['SUCURSAL'],
            'deposito': record['DEPOSITO'],
            'compro': record['COMPRO']
        }
        for record in table
        if record['ID']  # Asegurarse de que ID no sea nulo
    }
    print(f"Total registros en facturas.DBF: {len(dbf_data)}")

    # Recorrer los registros del modelo Factura
    facturas_actualizadas = 0
    for factura in Factura.objects.all():
        # Buscar en la tabla DBF usando el campo ID
        datos = dbf_data.get(factura.id_factura)

        if datos:
            # Asignar id_sucursal como una instancia de Sucursal
            try:
                sucursal = Sucursal.objects.get(id_sucursal=datos['sucursal'])
                factura.id_sucursal = sucursal
            except Sucursal.DoesNotExist:
                print(f"Sucursal con ID '{datos['sucursal']}' no encontrada para factura {factura.id_factura}")

            # Asignar id_deposito como una instancia de ProductoDeposito
            try:
                deposito = ProductoDeposito.objects.get(id_producto_deposito=datos['deposito'])  # Usar el campo primario
                factura.id_deposito = deposito
            except ProductoDeposito.DoesNotExist:
                print(f"Depósito con ID '{datos['deposito']}' no encontrado para factura {factura.id_factura}")

            # Asignar id_comprobante_venta como una instancia de ComprobanteVenta
            compro = datos['compro']
            if compro:
                try:
                    comprobante = ComprobanteVenta.objects.get(codigo_comprobante_venta=compro)
                    factura.id_comprobante_venta = comprobante
                except ComprobanteVenta.DoesNotExist:
                    print(f"Comprobante con código '{compro}' no encontrado para factura {factura.id_factura}")

            # Guardar cambios en la factura
            factura.save()
            facturas_actualizadas += 1

    print(f"Total facturas actualizadas: {facturas_actualizadas}")

if __name__ == '__main__':
    asignar_claves_a_facturas()

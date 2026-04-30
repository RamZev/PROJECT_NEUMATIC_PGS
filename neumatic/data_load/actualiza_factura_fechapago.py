# neumatic\data_load\actualiza_factura_fechapago.py
import os
import sys
import django
from dbfread import DBF
from datetime import datetime
from datetime import date

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.factura_models import Factura

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'facturas.DBF')

def actualizar_fechapago_facturas():
    """Actualiza el campo fecha_pago en el modelo Factura basado en la tabla facturas.DBF."""
    print("Cargando datos desde la tabla facturas.DBF...")
    
    # Leer la tabla DBF y filtrar registros donde FECHPAGO no esté vacío
    table = DBF(dbf_path, encoding='latin-1')
    
    # Filtrar registros donde FECHAPAGO tenga un valor válido
    registros_filtrados = []
    for record in table:
        fech_pago = record.get('FECHAPAGO')  # Obtener el valor del campo

        # Validar que no sea None y que sea un objeto datetime.date
        if fech_pago and isinstance(fech_pago, date) and fech_pago.year > 1900:  
            registros_filtrados.append(record)

    print(f"Total registros filtrados con FECHAPAGO no vacío: {len(registros_filtrados)}")
    
    # Procesar cada registro filtrado
    facturas_actualizadas = 0
    for record in registros_filtrados:
        factura_id = record['ID']
        fecha_pago = record['FECHAPAGO']
        
        try:
            # Buscar la factura en la base de datos
            factura = Factura.objects.get(id_factura=factura_id)
            
            # Actualizar el campo fecha_pago
            factura.fecha_pago = fecha_pago
            factura.save()
            facturas_actualizadas += 1
            print(f"Factura {factura_id} actualizada con fecha de pago {fecha_pago}")
        except Factura.DoesNotExist:
            print(f"Factura con ID {factura_id} no encontrada en la base de datos.")
    
    print(f"Total facturas actualizadas: {facturas_actualizadas}")

if __name__ == '__main__':
    actualizar_fechapago_facturas()

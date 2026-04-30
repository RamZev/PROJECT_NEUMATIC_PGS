# neumatic\data_load\factura_noestadist_migra.py
import os
import sys
import django
from dbfread import DBF
from django.db import transaction

# Configuración de Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.factura_models import Factura

def actualizar_facturas_noestadist():
    """Actualiza el campo noestadist en Factura desde facturas.DBF filtrando por noestadist=True"""
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'facturas.DBF')
    
    try:
        # Leer y filtrar la tabla DBF
        table = DBF(dbf_path, encoding='latin-1')
        registros_filtrados = [r for r in table if r.get('NOESTADIST') == True]
        
        print(f"Total registros en DBF: {len(table)}")
        print(f"Registros con NOESTADIST=True: {len(registros_filtrados)}")
        
        actualizados = 0
        omitidos = 0
        
        with transaction.atomic():
            for record in registros_filtrados:
                factura_id = record.get('ID')
                try:
                    # Buscar la factura por id_factura (equivalente a ID en DBF)
                    factura = Factura.objects.get(id_factura=factura_id)
                    
                    # Actualizar el campo noestadist
                    factura.no_estadist = True
                    factura.save()
                    actualizados += 1
                    
                    # Opcional: Mostrar progreso cada X registros
                    if actualizados % 100 == 0:
                        print(f"Actualizadas {actualizados} facturas...")
                        
                except Factura.DoesNotExist:
                    print(f"Factura con ID {factura_id} no encontrada. Omitiendo...")
                    omitidos += 1
                except Exception as e:
                    print(f"Error actualizando factura {factura_id}: {str(e)}")
                    omitidos += 1
        
        print(f"\nResumen de actualización:")
        print(f" - Facturas actualizadas: {actualizados}")
        print(f" - Registros omitidos: {omitidos}")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {dbf_path}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == '__main__':
    actualizar_facturas_noestadist()
# neumatic\data_load\factura_sucimp_migra.py
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

def actualizar_facturas_comisiones():
    """Actualiza suc_imp y comision en Factura desde facturas.DBF"""
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'facturas.DBF')
    
    try:
        # Leer la tabla DBF
        table = DBF(dbf_path, encoding='latin-1')
        
        # Filtrar registros de manera más segura
        registros_filtrados = []
        for record in table:
            try:
                # Verificar SUCIMP
                sucimp_valido = False
                sucimp = record.get('SUCIMP')
                if sucimp is not None:
                    try:
                        sucimp_valido = int(sucimp) > 0
                    except (ValueError, TypeError):
                        pass
                
                # Verificar COMISION
                comision_valida = str(record.get('COMISION', '')).strip() not in ['', None]
                
                if sucimp_valido or comision_valida:
                    registros_filtrados.append(record)
                    
            except Exception as e:
                print(f"Error analizando registro: {str(e)}")
                continue
        
        print(f"Total registros en DBF: {len(table)}")
        print(f"Registros que cumplen condiciones: {len(registros_filtrados)}")
        
        actualizados = 0
        omitidos = 0
        
        with transaction.atomic():
            for record in registros_filtrados:
                factura_id = record.get('ID')
                try:
                    factura = Factura.objects.get(id_factura=factura_id)
                    updates = {}
                    
                    # Procesar SUCIMP de manera segura
                    sucimp = record.get('SUCIMP')
                    if sucimp is not None:
                        try:
                            sucimp_int = int(sucimp)
                            if sucimp_int > 0:
                                updates['suc_imp'] = sucimp_int
                        except (ValueError, TypeError):
                            print(f"Valor inválido de SUCIMP en factura {factura_id}: {sucimp}")
                    
                    # Procesar COMISION de manera segura
                    comision = str(record.get('COMISION', '')).strip()
                    if comision not in ['', None]:
                        updates['comision'] = comision
                    
                    # Actualizar si hay campos válidos
                    if updates:
                        Factura.objects.filter(pk=factura.id_factura).update(**updates)
                        actualizados += 1
                    else:
                        omitidos += 1
                        
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
    actualizar_facturas_comisiones()
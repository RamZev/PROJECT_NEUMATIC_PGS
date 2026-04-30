import json
import os
import sys
import django
from django.db import connection

# Configuración del entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import MedioPago

def reset_medio_pago():
    """Elimina los datos existentes y resetea la secuencia de IDs"""
    MedioPago.objects.all().delete()
    print("Tabla MedioPago limpiada.")
    
    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='medio_pago';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('medio_pago', 'id_medio_pago'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('medio_pago', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE medio_pago AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_medio_pago_desde_json(ruta_json):
    """Carga los medios de pago desde JSON"""
    try:
        with open(ruta_json, 'r', encoding='utf-8') as file:
            medios_pago = json.load(file)
            
        for item in medios_pago:
            MedioPago.objects.create(
                id_medio_pago=item["id_medio_pago"],
                estatus_medio_pago=bool(item["estatus_medio_pago"]),
                nombre_medio_pago=item["nombre_medio_pago"],
                condicion_medio_pago=int(item["condicion_medio_pago"]),
                plazo_medio_pago=int(item["plazo_medio_pago"])
            )
            
        print(f"Se migraron {len(medios_pago)} medios de pago correctamente.")
        
    except FileNotFoundError:
        print(f"Error: Archivo {ruta_json} no encontrado.")
    except json.JSONDecodeError:
        print("Error: El archivo JSON tiene formato incorrecto.")
    except KeyError as e:
        print(f"Error: Falta campo obligatorio en JSON: {e}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'medio_pago.json')
    reset_medio_pago()
    cargar_medio_pago_desde_json(ruta_json)
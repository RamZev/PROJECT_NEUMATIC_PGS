# neumatic\data_load\concepto_banco_migra.py
import json
import os
import sys
import django
from django.db import connection
from django.core.exceptions import ValidationError
from django.conf import settings

# Configuración del entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import ConceptoBanco

def reset_concepto_banco():
    """Elimina los datos existentes en la tabla ConceptoBanco y resetea su ID."""
    ConceptoBanco.objects.all().delete()
    print("Tabla ConceptoBanco limpiada.")

    # Detectar el motor de base de datos
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='concepto_banco';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('concepto_banco', 'id_concepto_banco'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('concepto_banco', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE concepto_banco AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_conceptos_desde_json(ruta_json):
    """Carga los conceptos bancarios desde un archivo JSON con IDs manuales."""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        conceptos = json.load(file)

    # Contador para IDs manuales
    contador_id = 1

    for item in conceptos:
        try:
            ConceptoBanco.objects.create(
                id_concepto_banco=contador_id,  # ← Asignar ID manual
                estatus_concepto_banco=bool(item.get("estatus_concepto_banco", True)),
                nombre_concepto_banco=item["nombre_concepto_banco"],
                factor=int(item["factor"])
            )
            contador_id += 1
        except ValidationError as e:
            print(f"Error validando concepto {item.get('nombre_concepto_banco')}: {e}")
        except Exception as e:
            print(f"Error creando concepto {item.get('nombre_concepto_banco')}: {e}")

    print(f"Se han migrado {ConceptoBanco.objects.count()} conceptos bancarios con IDs desde 1 hasta {contador_id - 1}.")

if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'concepto_banco.json')

    reset_concepto_banco()
    cargar_conceptos_desde_json(ruta_json)
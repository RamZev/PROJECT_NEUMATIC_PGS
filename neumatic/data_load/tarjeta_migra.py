# neumatic\data_load\tarjeta_migra.py
import json
import os
import sys
import django
from django.db import connection
from django.conf import settings

# Configuración del entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import Tarjeta

def reset_tarjeta():
    """Elimina los datos existentes en la tabla Tarjeta y resetea su ID."""
    Tarjeta.objects.all().delete()
    print("Tabla Tarjeta limpiada.")

    # Detectar el motor de base de datos
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='tarjeta';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('tarjeta', 'id_tarjeta'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('tarjeta', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE tarjeta AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_tarjetas_desde_json(ruta_json):
    """Carga las tarjetas desde un archivo JSON."""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        tarjetas = json.load(file)

    # Contador para IDs manuales
    contador_id = 1

    for item in tarjetas:
        Tarjeta.objects.create(
            id_tarjeta=contador_id,  # ← Asignar ID manual
            estatus_tarjeta=bool(item.get("estatus_tarjeta", True)),
            nombre_tarjeta=item["nombre_tarjeta"],
            imputacion=item["imputacion"] if item["imputacion"] else None,
            banco_acreditacion=item["banco_acreditacion"] if item["banco_acreditacion"] else None,
            propia=bool(item.get("propia", False))
        )
        contador_id += 1

    print(f"Se han migrado {len(tarjetas)} tarjetas con IDs desde 1 hasta {contador_id - 1}.")

if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'tarjeta.json')

    reset_tarjeta()
    cargar_tarjetas_desde_json(ruta_json)
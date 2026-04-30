# neumatic\data_load\leyenda_migra.py
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

from apps.maestros.models.base_models import Leyenda

def reset_leyenda():
    """Elimina los datos existentes en la tabla Leyenda y resetea su ID."""
    Leyenda.objects.all().delete()
    print("Tabla Leyenda limpiada.")

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='leyenda';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('leyenda', 'id_leyenda'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('leyenda', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE leyenda AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_leyendas_desde_json(ruta_json):
    """Carga las leyendas desde un archivo JSON."""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        leyendas = json.load(file)

    for item in leyendas:
        Leyenda.objects.create(
            id_leyenda=item["id_leyenda"],  # Mantenemos el ID original
            estatus_leyenda=bool(item.get("estatus_leyenda", True)),
            nombre_leyenda=item["nombre_leyenda"],
            leyenda=item["leyenda"]
        )

    print(f"Se han migrado {len(leyendas)} leyendas.")

if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'leyenda.json')

    reset_leyenda()
    cargar_leyendas_desde_json(ruta_json)
# neumatic\data_load\codigo_retencion_migra.py
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

from apps.maestros.models.base_models import CodigoRetencion

def reset_codigo_retencion():
    """Elimina los datos existentes en la tabla CodigoRetencion y resetea su ID."""
    CodigoRetencion.objects.all().delete()
    print("Tabla CodigoRetencion limpiada.")

    # Detectar el motor de base de datos
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='codigo_retencion';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('codigo_retencion', 'id_codigo_retencion'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('codigo_retencion', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE codigo_retencion AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_codigos_retencion_desde_json(ruta_json):
    """Carga los códigos de retención desde un archivo JSON con IDs manuales."""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        codigos = json.load(file)

    # Contador para IDs manuales
    contador_id = 1

    for item in codigos:
        CodigoRetencion.objects.create(
            id_codigo_retencion=contador_id,  # ← Asignar ID manual
            estatus_cod_retencion=bool(item.get("estatus_cod_retencion", True)),
            nombre_codigo_retencion=item["nombre_codigo_retencion"],
            imputacion=item["imputacion"] if item["imputacion"] is not None else 0
        )
        contador_id += 1

    print(f"Se han migrado {len(codigos)} códigos de retención con IDs desde 1 hasta {contador_id - 1}.")

if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'codigo_retencion.json')

    reset_codigo_retencion()
    cargar_codigos_retencion_desde_json(ruta_json)
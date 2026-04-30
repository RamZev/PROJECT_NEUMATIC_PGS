# neumatic\data_load\tipo_documento_identidad_migra.py
import json
import os
import sys
import django
from django.db import connection

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import TipoDocumentoIdentidad  

def reset_tipo_documento_identidad():
    """Elimina los datos existentes en la tabla TipoDocumentoIdentidad y resetea su ID."""
    # Eliminar los datos existentes en la tabla
    TipoDocumentoIdentidad.objects.all().delete()
    print("Tabla TipoDocumentoIdentidad limpiada.")

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='tipo_documento_identidad';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('tipo_documento_identidad', 'id_tipo_documento_identidad'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('tipo_documento_identidad', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE tipo_documento_identidad AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_tipo_documento_identidad_desde_json(ruta_json):
    """Carga los tipos de documento de identidad desde un archivo JSON y los guarda en la base de datos."""
    # Abrir y cargar el archivo JSON
    with open(ruta_json, 'r', encoding='utf-8') as file:
        tipos_documento_identidad = json.load(file)

    # Recorrer los elementos del JSON y migrar cada uno
    for item in tipos_documento_identidad:
        nombre_documento_identidad = item["nombre_documento_identidad"]
        tipo_documento_identidad = item["tipo_documento_identidad"]
        codigo_afip = item["codigo_afip"]
        ws_afip = item["ws_afip"]

        # Crear el registro en la base de datos incluyendo el ID del JSON
        TipoDocumentoIdentidad.objects.create(
            id_tipo_documento_identidad=item["id_tipo_documento_identidad"],  # ← AGREGAR ESTA LÍNEA
            estatus_tipo_documento_identidad=True,
            nombre_documento_identidad=nombre_documento_identidad,
            tipo_documento_identidad=tipo_documento_identidad,
            codigo_afip=codigo_afip,
            ws_afip=ws_afip
        )

    print(f"Se han migrado {len(tipos_documento_identidad)} tipos de documento de identidad de forma exitosa.")

if __name__ == '__main__':
    # Ruta al archivo tipo_documento_identidad.json
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'tipo_documento_identidad.json')

    # Resetear la tabla TipoDocumentoIdentidad antes de la migración
    reset_tipo_documento_identidad()

    # Ejecutar la migración
    cargar_tipo_documento_identidad_desde_json(ruta_json)

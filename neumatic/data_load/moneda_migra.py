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

from apps.maestros.models.base_models import Moneda

def reset_moneda():
    """Elimina los datos existentes en la tabla Moneda y resetea su ID."""
    Moneda.objects.all().delete()
    print("Tabla Moneda limpiada.")

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            # SQLite: reiniciar secuencia
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='moneda';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            # PostgreSQL: reiniciar secuencia usando setval
            cursor.execute("SELECT setval(pg_get_serial_sequence('moneda', 'id_moneda'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            # SQL Server: reiniciar identity
            cursor.execute("DBCC CHECKIDENT ('moneda', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            # MySQL: reiniciar autoincremento
            cursor.execute("ALTER TABLE moneda AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_moneda_desde_json(ruta_json):
    """Carga las monedas desde un archivo JSON y las guarda en la base de datos."""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        monedas = json.load(file)

    for item in monedas:
        Moneda.objects.create(
            id_moneda=item["id_moneda"],
            estatus_moneda=bool(item["estatus_moneda"]),
            nombre_moneda=item["nombre_moneda"],
            cotizacion_moneda=item["cotizacion_moneda"],
            simbolo_moneda=item["simbolo_moneda"],
            ws_afip=item["ws_afip"],
            predeterminada=bool(item["predeterminada"])
        )

    print(f"Se han migrado {len(monedas)} monedas con sus ID explícitos.")

if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'moneda.json')

    reset_moneda()
    cargar_moneda_desde_json(ruta_json)
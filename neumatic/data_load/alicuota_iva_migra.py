import json
import os
import sys
import django
from django.db import connection

# Añadir el directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import AlicuotaIva

def reset_alicuota_iva():
    """Elimina los datos existentes en la tabla AlicuotaIva y resetea su ID."""
    AlicuotaIva.objects.all().delete()
    print("Tabla AlicuotaIva limpiada.")

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='codigo_alicuota';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('codigo_alicuota', 'id_alicuota_iva'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('codigo_alicuota', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE codigo_alicuota AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_alicuota_iva_desde_json(ruta_json):
    """Carga los datos del archivo JSON e inserta los registros en la tabla."""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        AlicuotaIva.objects.create(
            id_alicuota_iva=item["id_alicuota_iva"],
            estatus_alicuota_iva=bool(item["estatus_alicuota_iva"]),
            codigo_alicuota=item["codigo_alicuota"],
            alicuota_iva=item["alicuota_iva"],
            descripcion_alicuota_iva=item.get("descripcion_alicuota_iva", None)
        )

    print(f"Se han migrado {len(data)} alícuotas IVA con IDs explícitos.")

if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'alicuota_iva.json')

    reset_alicuota_iva()
    cargar_alicuota_iva_desde_json(ruta_json)

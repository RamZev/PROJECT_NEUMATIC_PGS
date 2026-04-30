# neumatic\data_load\banco_migra.py
import os
import sys
import django
from dbfread import DBF
from django.db import connection
from django.conf import settings

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import Banco

def reset_banco():
    """Elimina los datos existentes en la tabla Banco y resetea su ID."""
    Banco.objects.all().delete()
    print("Tabla Banco limpiada.")

    # Detectar el motor de base de datos
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='banco';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('banco', 'id_banco'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('banco', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE banco AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_datos():
    """Lee los datos de codbco.DBF, los ordena por CODBCO y los migra al modelo Banco,
    usando el índice del ciclo como id_banco."""
    reset_banco()

    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'codbco.DBF')

    # Leer y ordenar por CODBCO
    records = list(DBF(dbf_path, encoding='cp1252'))
    records_sorted = sorted(records, key=lambda r: r['CODBCO'])

    for idx, record in enumerate(records_sorted, start=1):
        codbco = int(record['CODBCO'])
        nombre = (record['NOMBRE'] or "").strip()

        Banco.objects.create(
            id_banco=idx,               # ← Asignar el índice del ciclo (empieza en 1)
            estatus_banco=True,
            nombre_banco=nombre,
            codigo_banco=codbco,
            cuit_banco=None
        )

    print(f"Se han migrado {len(records_sorted)} registros de Banco de forma exitosa.")

if __name__ == '__main__':
    cargar_datos()
    print("Migración de Banco completada.")
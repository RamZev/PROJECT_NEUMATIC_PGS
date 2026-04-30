# neumatic\data_load\producto_estado_migra.py
import os
import sys
import django
from dbfread import DBF
from django.db import connection

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import ProductoEstado

def reset_producto_estado():
    """Elimina los datos existentes en la tabla ProductoEstado y resetea su ID."""
    ProductoEstado.objects.all().delete()
    print("Tabla ProductoEstado limpiada.")

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto_estado';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('producto_estado', 'id_producto_estado'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('producto_estado', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE producto_estado AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_datos():
    """Lee los datos de la tabla listaestados.DBF y asigna ID manualmente con el índice del bucle."""
    reset_producto_estado()

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'listaestados.DBF')

    # Abrir la tabla de Visual FoxPro
    table = DBF(dbf_path, encoding='latin-1')

    registros_crear = []
    
    for idx, record in enumerate(table, start=1):  # start=1 para que empiece en 1
        estado = record['ESTADO'].strip() if record['ESTADO'] else ""
        nombre = record['NOMBRE'].strip() if record['NOMBRE'] else ""

        registros_crear.append(
            ProductoEstado(
                id_producto_estado=idx,  # ← Asignar el índice del bucle como ID
                estatus_producto_estado=True,
                estado_producto=estado,
                nombre_producto_estado=nombre
            )
        )

    # Crear todos los registros en lote
    if registros_crear:
        ProductoEstado.objects.bulk_create(registros_crear)
        print(f"Se han migrado {len(registros_crear)} registros de ProductoEstado con IDs desde 1 hasta {len(registros_crear)}.")
    else:
        print("No se encontraron registros para migrar.")

if __name__ == '__main__':
    cargar_datos()
    print("Migración de ProductoEstado completada.")
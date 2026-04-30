# neumatic\data_load\producto_migra_cai.py
import os
import sys
import django
import time  # Para medir el tiempo de procesamiento
from dbfread import DBF
from django.db import connection

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.producto_models import ProductoCai

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'lista.DBF')

def reset_producto_cai():
    """Elimina los datos existentes en la tabla y resetea su ID."""
    ProductoCai.objects.all().delete()
    print("Tabla ProductoCai limpiada.")

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto_cai';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('producto_cai', 'id_cai'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('producto_cai', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE producto_cai AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def migrar_productos_cai():
    start_time = time.time()  # Registrar el tiempo inicial

    reset_producto_cai()

    # Abrir la tabla DBF y procesar los datos
    print("Cargando datos desde la tabla DBF...")
    table = DBF(dbf_path, encoding='latin-1')

    # Usar un conjunto para almacenar los valores únicos de CODFABRICA
    valores_unicos = set()

    for record in table:
        cod_fabrica = record.get('CODFABRICA', '').strip()

        # Ignorar valores vacíos o nulos
        if not cod_fabrica:
            continue

        # Agregar valores únicos al conjunto
        valores_unicos.add(cod_fabrica)

    print(f"Total valores únicos encontrados: {len(valores_unicos)}")

    # Filtrar valores que ya existen en la base de datos
    existentes = set(
        ProductoCai.objects.values_list('cai', flat=True)
    )
    nuevos_valores = valores_unicos - existentes
    print(f"Total valores a insertar: {len(nuevos_valores)}")

    # Insertar los nuevos valores en la tabla ProductoCai
    nuevos_registros = [
        ProductoCai(
            estatus_cai=True,  # Asignación obligatoria
            cai=valor,         # Asignación obligatoria
            descripcion_cai=valor  # Asignación obligatoria
        )
        for valor in nuevos_valores
    ]
    ProductoCai.objects.bulk_create(nuevos_registros, batch_size=1000)
    
    print(f"{len(nuevos_valores)} registros insertados exitosamente.")
    print(f"Proceso completado en {time.time() - start_time:.2f} segundos.")

if __name__ == '__main__':
    migrar_productos_cai()

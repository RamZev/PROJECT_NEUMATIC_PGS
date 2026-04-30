# neumatic\data_load\producto_deposito_migra.py
import os
import sys
import django
import time  # Para medir el tiempo de procesamiento
from dbfread import DBF
from django.db import connection
from datetime import date

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

# Importación de los modelos
from apps.maestros.models.producto_models import ProductoDeposito
from apps.maestros.models.sucursal_models import Sucursal

def reset_producto_deposito():
    """Elimina los datos existentes en la tabla y resetea su ID."""
    ProductoDeposito.objects.all().delete()
    print("Tabla ProductoDeposito limpiada.")

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto_deposito';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('producto_deposito', 'id_producto_deposito'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('producto_deposito', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE producto_deposito AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")


# Eliminación de datos y secuencia de ID
reset_producto_deposito()

# Tabla origen y modelo destino
tabla_origen = 'depositos.DBF'
modelo_dest = ProductoDeposito

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', tabla_origen)

# Abrir la tabla de Visual FoxPro usando dbfread
table = DBF(dbf_path, encoding='latin-1')

# Rango de registros 
codigo_inicio = 1
codigo_final = None     # Hasta el final

# Nombre de variable id en la tabla origen
codigo_id = "DEPOSITO"

# Nombre del atributo id del modelo destino
id_destino = "id_producto_deposito"

# Filtrar y ordenar la tabla DBF
table = sorted(
    [
        record
        for record in table
        if int(record.get(codigo_id, 0)) >= codigo_inicio and 
           (codigo_final is None or int(record.get(codigo_id, 0)) <= codigo_final)
    ],
    key=lambda record: int(record.get(codigo_id, 0))
)

total_registros = len(table)
print(f"{tabla_origen}: Total de registros a procesar: {total_registros}")

# Datos de ajuste


# Ejemplos base para asignar valores 
''' ejemplos base para asignar valores 
    record.get('NOMBRE', '').strip(),   # String
    int(record.get('MICHELIN', 0)),     # Integer
    float(record.get('EXENTO') or 0)    # Float
    record.get('INICIOACT', None)       # Date
    bool(record.get('PROMO', False))    # Boolean
'''

# Procesar registros
for idx, record in enumerate(table):
    id_origen = int(record.get(codigo_id, 0))
    # print(f"Procesando {tabla_origen} con ID: {id_origen}")

    # Evitar id duplicados
    if modelo_dest.objects.filter(**{id_destino: id_origen}).exists():
        print(f"{tabla_origen} con ID {id_origen} ya existe. Saltando registro.")
        continue

    pk_sucursal = int(record.get('SUCURSAL', 0))
    try:
        id_sucursal_instancia = Sucursal.objects.get(pk=pk_sucursal)
    except Sucursal.DoesNotExist:
        print(f"Sucursal con ID {pk_sucursal} no encontrada. Saltando registro.")
        continue
    
    # Crear registro
    try:
        modelo_dest.objects.create(
            id_producto_deposito=id_origen,
            estatus_producto_deposito=bool(record.get('ACTIVO', False)),
            id_sucursal=id_sucursal_instancia,
            nombre_producto_deposito=record.get('NOMBRE', '').strip(),

        )
        print(f"{tabla_origen} con ID {id_origen} creado exitosamente.")
    except Exception as e:
        print(f"Error al crear {tabla_origen} con ID {id_origen}: {e}")
        continue
    
print(f"La migración de la tabla {tabla_origen} terminó con éxito!")

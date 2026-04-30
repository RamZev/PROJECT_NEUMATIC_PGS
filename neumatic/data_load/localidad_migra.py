# neumatic\data_load\localidad_migra.py
import csv
import os
import sys
import django
from django.db import transaction
from django.db.models import Q
from django.db import connection

import socket
from datetime import datetime


# Configuración de paths y Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from django.contrib.auth.models import User
from apps.maestros.models.base_models import Localidad, Provincia

BATCH_SIZE = 2000  # Tamaño del lote para procesamiento por lotes

def cargar_localidades_desde_csv(archivo_csv):
    """Carga los datos de localidades desde un archivo CSV optimizado con lotes."""
    # Pre-cargar todas las provincias en memoria para evitar consultas repetidas
    provincias_cache = {p.id_provincia: p for p in Provincia.objects.all()}
    
    # Leer todo el archivo CSV primero (mejor para procesamiento por lotes)
    with open(archivo_csv, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        rows = [clean_row(row) for row in reader if validate_row(row)]
    
    # Procesar en lotes
    total_rows = len(rows)
    localidades_batch = []
    filas_procesadas = 0
    
    with transaction.atomic():
        reset_localidades()
        
        for i, row in enumerate(rows, 1):
            try:
                localidad = process_row(row, provincias_cache)
                if localidad:
                    localidades_batch.append(localidad)
                    
                    # Procesar lote cuando alcanza el tamaño definido
                    if len(localidades_batch) >= BATCH_SIZE:
                        Localidad.objects.bulk_create(localidades_batch)
                        filas_procesadas += len(localidades_batch)
                        localidades_batch = []
                        print(f"Procesadas {filas_procesadas}/{total_rows} filas...")
            except Exception as e:
                print(f"Error procesando fila {i}: {e}")
        
        # Procesar el último lote (si queda algo)
        if localidades_batch:
            Localidad.objects.bulk_create(localidades_batch)
            filas_procesadas += len(localidades_batch)
    
    print(f"Migración completada. {filas_procesadas}/{total_rows} localidades procesadas.")

def clean_row(row):
    """Limpia los nombres de campos y valores del row."""
    return {key.strip(): value.strip() if value else '' for key, value in row.items()}

def validate_row(row):
    """Valida que la fila tenga los campos requeridos."""
    required_fields = {'CP', 'Localidad', 'Cod_Provincia'}
    return all(field in row for field in required_fields)

def process_row(row, provincias_cache):
    """Procesa una fila individual y devuelve un objeto Localidad no guardado."""
    nombre_localidad = row['Localidad']
    codigo_postal = row['CP']
    id_provincia = int(row['Cod_Provincia']) + 1
    
    provincia = provincias_cache.get(id_provincia)
    if not provincia:
        print(f"Provincia con código {id_provincia} no encontrada. Fila omitida.")
        return None
    
    # Obtener valores para campos heredados
    id_user = 1  # Obtener instancia del usuario admin
    estacion = socket.gethostname()   # Obtener nombre de la estación
    fcontrol = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha actual
    
    return Localidad(
        estatus_localidad=True,
        nombre_localidad=nombre_localidad,
        id_provincia=provincia,
        codigo_postal=codigo_postal,
        # Campos heredados
        usuario="admin",
        estacion=estacion,
        fcontrol=fcontrol
    )

def reset_localidades():
    """Elimina los datos existentes de forma optimizada."""
    # Usar DELETE más eficiente para tablas grandes
    Localidad.objects.all().delete()
    
    # Resetear secuencia de forma compatible con múltiples bases de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            # SQLite: reiniciar secuencia
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='localidad';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            # PostgreSQL: reiniciar secuencia (usando setval)
            cursor.execute("SELECT setval(pg_get_serial_sequence('localidad', 'id_localidad'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            # SQL Server: reiniciar identity
            cursor.execute("DBCC CHECKIDENT ('localidad', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            # MySQL: reiniciar autoincremento
            cursor.execute("ALTER TABLE localidad AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")
    
    print("Tabla Localidad reseteada correctamente.")

if __name__ == '__main__':
    archivo_csv = os.path.join(BASE_DIR, 'data_load', 'Codigos-Postales-Argentina.csv')
    cargar_localidades_desde_csv(archivo_csv)
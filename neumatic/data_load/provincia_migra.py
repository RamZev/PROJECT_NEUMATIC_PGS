# neumatic\data_load\provincia_migra.py
import csv
import os
import sys
import django
from django.db import connection
from django.conf import settings

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import Provincia

def reset_provincia():
    """Elimina los datos existentes en la tabla Provincia y resetea su ID."""
    # Eliminar los datos existentes
    cantidad = Provincia.objects.all().delete()
    print(f"Tabla Provincia limpiada. ({cantidad[0]} registros eliminados)")

    # Detectar el motor de base de datos
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            # SQLite: reiniciar secuencia
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='provincia';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            # PostgreSQL: reiniciar secuencia
            cursor.execute("SELECT setval(pg_get_serial_sequence('provincia', 'id_provincia'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            # SQL Server: reiniciar identity
            cursor.execute("DBCC CHECKIDENT ('provincia', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            # MySQL: reiniciar autoincremento
            cursor.execute("ALTER TABLE provincia AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_provincias_desde_csv(archivo_csv):
    """Carga los datos de provincias desde el archivo provincia.csv."""
    
    # Resetear la tabla Provincia (eliminar los datos existentes)
    reset_provincia()
    
    with open(archivo_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        contador = 0
        for row in reader:
            codigo = int(row['Cod_Provincia'].strip())
            
            print(f"Código: {codigo}, Provincia: {row['Provincia']}")
            
            # Forzar el ID para que coincida con código + 1
            # (Esto mantiene la compatibilidad con localidad_migra.py que usa id_provincia = codigo + 1)
            provincia = Provincia(
                id_provincia=codigo + 1,  # ← Agregar ID explícito
                estatus_provincia=True,
                codigo_provincia=row['Cod_Provincia'].strip(),
                nombre_provincia=row['Provincia'].strip()
            )
            provincia.save()  # Usar save() en lugar de create() para ID manual
            contador += 1

        print(f"Se han migrado {contador} provincias correctamente desde {archivo_csv}.")

if __name__ == '__main__':
    # Ruta del archivo CSV
    archivo_csv = os.path.join(os.path.dirname(__file__), 'provincia.csv')

    # Ejecutar la migración
    cargar_provincias_desde_csv(archivo_csv)
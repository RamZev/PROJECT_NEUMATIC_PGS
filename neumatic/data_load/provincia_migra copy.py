# neumatic\data_load\provincia_migra.py
import csv
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

from apps.maestros.models.base_models import Provincia

def cargar_provincias_desde_csv(archivo_csv):
    """Carga los datos de provincias desde un archivo CSV y los 
    ordena por código de provincia numéricamente antes de migrar."""
    # Crear un conjunto para almacenar las provincias únicas
    provincias_unicas = set()
    print(provincias_unicas)

    # Abrir el archivo CSV y leer su contenido
    with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Iterar sobre cada fila del archivo CSV
        for row in reader:
            # Extraer los valores de 'Provincia' y 'Cod_Provincia'
            nombre_provincia = row['Provincia'].strip()
            codigo_provincia = row['Cod_Provincia'].strip()

            # Añadir una tupla única al conjunto
            provincias_unicas.add((nombre_provincia, codigo_provincia))

    # Ordenar el conjunto de provincias numéricamente por 'codigo_provincia' antes de migrar
    provincias_ordenadas = sorted(provincias_unicas, key=lambda x: int(x[1]))  # Convertir 'codigo_provincia' a entero para ordenarlo numéricamente

    # Resetear la tabla Provincia (eliminar los datos existentes)
    # reset_provincias()

    # Recorrer la lista de provincias ordenadas y migrarlas al modelo Provincia
    for nombre_provincia, codigo_provincia in provincias_ordenadas:
        # Crear el registro en la base de datos
        Provincia.objects.create(
            estatus_provincia=True,  # Establecer el estatus en True
            codigo_provincia=codigo_provincia,
            nombre_provincia=nombre_provincia
        )

    print(f"Se han migrado {len(provincias_ordenadas)} provincias de forma exitosa.")

def reset_provincias():
    # """Elimina los datos existentes en la tabla Provincia y resetea su ID en SQLite."""
    # # Eliminar los datos existentes en la tabla
    # Provincia.objects.all().delete()

    # # Reiniciar el autoincremento en SQLite
    # with connection.cursor() as cursor:
    #     cursor.execute("DELETE FROM sqlite_sequence WHERE name='provincia';")  # Ajustar el nombre de la tabla según sea necesario

    # print("Datos de la tabla Provincia eliminados y autoincremento reseteado.")
    """Desactiva restricciones, elimina registros y reinicia autoincremento."""
    with connection.cursor() as cursor:
        # Desactiva las restricciones de claves foráneas
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        # Elimina los registros de la tabla Provincia
        # Provincia.objects.all().delete()

        # Resetea el autoincremento
        # cursor.execute("DELETE FROM sqlite_sequence WHERE name='provincia';")
        
        # Reactiva las restricciones de claves foráneas
        cursor.execute("PRAGMA foreign_keys = ON;")
    print("Datos de la tabla Provincia eliminados y autoincremento reseteado.")
    

if __name__ == '__main__':
    # Ruta del archivo CSV
    archivo_csv = os.path.join(BASE_DIR, 'data_load', 'Codigos-Postales-Argentina.csv')

    # Ejecutar la migración
    cargar_provincias_desde_csv(archivo_csv)

# neumatic\data_load\provincia_migra.py
import csv
import os
import sys
import django

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import Provincia

def cargar_provincias_desde_csv(archivo_csv):
    """Carga los datos de provincias desde el archivo provincia.csv."""
    with open(archivo_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Resetear la tabla Provincia (eliminar los datos existentes)
        # Provincia.objects.all().delete()
        # print("Datos existentes eliminados.")

        # Leer cada fila y crear las instancias
        for row in reader:
            print(row['Cod_Provincia'], row['Provincia'])
            
            # Provincia.objects.create(
            Provincia.objects.get_or_create(
                estatus_provincia=True,  # Estatus por defecto
                codigo_provincia=row['Cod_Provincia'].strip(),
                nombre_provincia=row['Provincia'].strip()
            )

        print(f"Provincias migradas correctamente desde {archivo_csv}.")

if __name__ == '__main__':
    # Ruta del archivo CSV
    archivo_csv = os.path.join(os.path.dirname(__file__), 'provincia.csv')

    # Ejecutar la migración
    cargar_provincias_desde_csv(archivo_csv)

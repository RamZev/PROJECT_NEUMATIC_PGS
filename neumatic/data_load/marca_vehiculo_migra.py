# neumatic/data_load/marca_vehiculo_migra.py
import csv
import os
import sys
import django
from django.db import connection
from django.conf import settings

# Configurar entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.vehiculo_models import MarcaVehiculo

def reset_tabla():
    print("Limpiando tabla MarcaVehiculo...")
    MarcaVehiculo.objects.all().delete()
    engine = settings.DATABASES['default']['ENGINE']
    with connection.cursor() as cursor:
        if 'postgresql' in engine:
            cursor.execute("TRUNCATE TABLE marca_vehiculo RESTART IDENTITY CASCADE;")
            print("Secuencia de ID reseteada (PostgreSQL).")

def cargar_desde_csv(archivo_csv):
    reset_tabla()
    
    with open(archivo_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        contador = 0
        max_id = 0
        
        for row in reader:
            # Forzamos el ID para mantener la relación con ModeloVehiculo
            marca = MarcaVehiculo(
                id_marca_vehiculo=int(row['id_marca_vehiculo']),
                estatus_marca_vehiculo=row['estatus_marca_vehiculo'] == 'True',
                marca_vehiculo=row['marca_vehiculo']
            )
            marca.save()
            contador += 1
            if marca.id_marca_vehiculo > max_id:
                max_id = marca.id_marca_vehiculo

        print(f"Se migraron {contador} marcas correctamente.")
        
        # Actualizar la secuencia para futuros inserts
        engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in engine:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('marca_vehiculo', 'id_marca_vehiculo'), {max_id}, true);")
            print(f"Secuencia de ID actualizada al máximo ({max_id}).")

if __name__ == '__main__':
    # Busca el CSV en la misma carpeta (data_load)
    archivo_csv = os.path.join(os.path.dirname(__file__), 'marca_vehiculo.csv')
    if os.path.exists(archivo_csv):
        cargar_desde_csv(archivo_csv)
    else:
        print(f"❌ No se encontró el archivo {archivo_csv}")
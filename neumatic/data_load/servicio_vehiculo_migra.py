# neumatic/data_load/servicio_vehiculo_migra.py
import csv
import os
import sys
import django
from django.db import connection
from django.conf import settings
from datetime import datetime

# Configurar entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.servicio_vehiculo_models import ServicioVehiculo

BATCH_SIZE = 1000

def reset_tabla():
    print("Limpiando tabla ServicioVehiculo...")
    # Eliminamos en cascada por si hay detalles asociados
    ServicioVehiculo.objects.all().delete()
    engine = settings.DATABASES['default']['ENGINE']
    with connection.cursor() as cursor:
        if 'postgresql' in engine:
            cursor.execute("TRUNCATE TABLE servicio_vehiculo RESTART IDENTITY CASCADE;")
            print("Secuencia de ID reseteada (PostgreSQL).")

def limpiar_valor(valor, tipo='str'):
    if not valor or str(valor).strip() == '' or str(valor).lower() == 'null':
        return None if tipo in ['int', 'date'] else ''
    
    if tipo == 'int':
        try:
            return int(valor)
        except ValueError:
            return None
            
    if tipo == 'date':
        try:
            return datetime.strptime(valor.strip(), '%Y-%m-%d').date()
        except ValueError:
            return None
            
    return str(valor).strip()

def cargar_desde_csv(archivo_csv):
    reset_tabla()
    
    print("Iniciando migración masiva de servicios de vehículos...")
    
    with open(archivo_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        
        batch = []
        contador = 0
        max_id = 0
        
        for row in reader:
            id_actual = int(row['id_servicio_vehiculo'])
            if id_actual > max_id:
                max_id = id_actual
                
            servicio = ServicioVehiculo(
                id_servicio_vehiculo=id_actual,
                estatus_servicio_vehiculo=row['estatus_servicio_vehiculo'] == 'True',
                id_cliente_id=int(row['id_cliente']),
                id_vehiculo_id=int(row['id_vehiculo']),
                kmxmes=limpiar_valor(row['kmxmes'], 'int'),
                proxima_visita=limpiar_valor(row['proxima_visita'], 'date'),
                observaciones=limpiar_valor(row['observaciones'])
            )
            
            batch.append(servicio)
            contador += 1
            
            if len(batch) >= BATCH_SIZE:
                ServicioVehiculo.objects.bulk_create(batch, batch_size=BATCH_SIZE)
                batch = []
                if contador % 5000 == 0:
                    print(f"   ... {contador} migrados")

        if batch:
            ServicioVehiculo.objects.bulk_create(batch, batch_size=BATCH_SIZE)

        print(f"\n✅ Se migraron {contador} servicios de vehículos correctamente.")
        
        engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in engine and max_id > 0:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('servicio_vehiculo', 'id_servicio_vehiculo'), {max_id}, true);")
            print(f"✅ Secuencia de ID actualizada al máximo ({max_id}).")

if __name__ == '__main__':
    archivo_csv = os.path.join(os.path.dirname(__file__), 'servicio_vehiculo.csv')
    if os.path.exists(archivo_csv):
        cargar_desde_csv(archivo_csv)
    else:
        print(f"❌ No se encontró el archivo {archivo_csv}")
# neumatic/data_load/vehiculo_migra.py
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

from apps.maestros.models.vehiculo_models import Vehiculo

# Tamaño del lote para inserciones masivas
BATCH_SIZE = 1000

def reset_tabla():
    print("Limpiando tabla Vehiculo...")
    Vehiculo.objects.all().delete()
    engine = settings.DATABASES['default']['ENGINE']
    with connection.cursor() as cursor:
        if 'postgresql' in engine:
            cursor.execute("TRUNCATE TABLE vehiculo RESTART IDENTITY CASCADE;")
            print("Secuencia de ID reseteada (PostgreSQL).")

def limpiar_valor(valor, tipo='str'):
    """Convierte cadenas vacías o 'null' en None según el tipo."""
    if not valor or str(valor).strip() == '' or str(valor).lower() == 'null':
        return None if tipo in ['int', 'date'] else ''
    
    if tipo == 'int':
        try:
            return int(valor)
        except ValueError:
            return None
            
    if tipo == 'date':
        try:
            # Formato esperado YYYY-MM-DD
            return datetime.strptime(valor.strip(), '%Y-%m-%d').date()
        except ValueError:
            return None
            
    return str(valor).strip()

def cargar_desde_csv(archivo_csv):
    reset_tabla()
    
    print("Iniciando migración masiva de vehículos...")
    
    with open(archivo_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        
        batch = []
        contador = 0
        max_id = 0
        
        for row in reader:
            # 1. Procesar Kilometraje (con la corrección de negativos)
            kmxmes_val = limpiar_valor(row['kmxmes'], 'int')
            if kmxmes_val is not None and kmxmes_val < 0:
                kmxmes_val = kmxmes_val * -1  # Convierte -1076 en 1076
                
            # 2. Obtener ID actual para calcular el max_id
            id_actual = int(row['id_vehiculo'])
            if id_actual > max_id:
                max_id = id_actual
                
            # 3. Crear la instancia del vehículo
            vehiculo = Vehiculo(
                id_vehiculo=id_actual,
                estatus_vehiculo=row['estatus_vehiculo'] == 'True',
                tipo_vehiculo=int(row['tipo_vehiculo']) if row['tipo_vehiculo'] else 1,
                id_marca_vehiculo_id=int(row['id_marca_vehiculo']),
                id_modelo_vehiculo_id=int(row['id_modelo_vehiculo']),
                segmento=limpiar_valor(row['segmento'])[:3],
                anio=limpiar_valor(row['anio'], 'int'),
                patente=limpiar_valor(row['patente']),
                kmxmes=kmxmes_val, # Aplicamos la corrección
                visita=limpiar_valor(row['visita'], 'date'),
                exportado=row['exportado'] == 'True',
                observacion=limpiar_valor(row['observacion'])
            )
            
            batch.append(vehiculo)
            contador += 1
            
            # 4. Insertar por lotes cuando alcanza el BATCH_SIZE
            if len(batch) >= BATCH_SIZE:
                Vehiculo.objects.bulk_create(batch, batch_size=BATCH_SIZE)
                batch = []
                if contador % 5000 == 0:
                    print(f"   ... {contador} migrados")

        # Insertar los registros restantes que no llegaron a completar el lote
        if batch:
            Vehiculo.objects.bulk_create(batch, batch_size=BATCH_SIZE)

        print(f"\n✅ Se migraron {contador} vehículos correctamente.")
        
        # 5. Actualizar la secuencia de PostgreSQL
        engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in engine and max_id > 0:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('vehiculo', 'id_vehiculo'), {max_id}, true);")
            print(f"✅ Secuencia de ID actualizada al máximo ({max_id}).")

if __name__ == '__main__':
    archivo_csv = os.path.join(os.path.dirname(__file__), 'vehiculo.csv')
    if os.path.exists(archivo_csv):
        cargar_desde_csv(archivo_csv)
    else:
        print(f"❌ No se encontró el archivo {archivo_csv}")
# neumatic\data_load\producto_modelo_migra.py
import os
import sys
import django
from dbfread import DBF
from django.db import connection
from django.utils import timezone


# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import ProductoModelo

def reset_producto_modelo():
    """Elimina los datos existentes y resetea la secuencia"""
    print("🔁 Reseteando tabla ProductoModelo...")
    
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'postgresql' in engine:
            cursor.execute("DELETE FROM producto_modelo;")
            cursor.execute("SELECT setval(pg_get_serial_sequence('producto_modelo', 'id_modelo'), 1, false);")
            print("✅ Tabla reseteada correctamente (PostgreSQL)")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DELETE FROM producto_modelo")
            cursor.execute("DBCC CHECKIDENT ('producto_modelo', RESEED, 0);")
            print("✅ Tabla reseteada correctamente (SQL Server)")
        elif 'sqlite' in engine:
            cursor.execute("PRAGMA foreign_keys = OFF;")
            ProductoModelo.objects.all().delete()
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto_modelo';")
            cursor.execute("PRAGMA foreign_keys = ON;")
            print("✅ Tabla reseteada correctamente (SQLite)")
        elif 'mysql' in engine:
            cursor.execute("DELETE FROM producto_modelo;")
            cursor.execute("ALTER TABLE producto_modelo AUTO_INCREMENT = 1;")
            print("✅ Tabla reseteada correctamente (MySQL)")
        else:
            print(f"Motor {engine} - No se requiere reset manual de secuencia.")

def cargar_datos():
    """Carga los datos desde el DBF en lotes con progreso"""
    reset_producto_modelo()

    # Configuración de rutas y lectura de datos
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'modelos.DBF')
    records = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda r: r['CODIGO'])
    total_registros = len(records)
    lote_size = 200  # Tamaño del lote para bulk_create
    
    print(f"\n📊 Total de registros a procesar: {total_registros:,}")
    print(f"⚡ Procesando en lotes de {lote_size} registros...\n")

    # Procesamiento por lotes
    start_time = timezone.now()
    batch = []
    processed = 0

    for i, record in enumerate(records, 1):
        batch.append(ProductoModelo(
            id_modelo=record['CODIGO'],
            estatus_modelo=True,
            nombre_modelo=record['NOMBRE'].strip()
        ))

        # Procesar lote completo o último lote parcial
        if len(batch) >= lote_size or i == total_registros:
            ProductoModelo.objects.bulk_create(batch)
            processed += len(batch)
            batch = []
            
            # Mostrar progreso
            percent = (i / total_registros) * 100
            print(f"🔄 Progreso: {i:,}/{total_registros:,} ({percent:.1f}%)", end='\r')

    # Estadísticas finales
    end_time = timezone.now()
    duration = (end_time - start_time).total_seconds()
    print(f"\n\n✅ Migración completada: {processed:,} registros")
    print(f"⏱  Tiempo total: {duration:.2f} segundos")
    print(f"🚀 Velocidad: {total_registros/duration:.1f} registros/segundo")

if __name__ == '__main__':
    cargar_datos()
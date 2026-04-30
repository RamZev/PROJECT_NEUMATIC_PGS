# neumatic\data_load\medidas_estados_migra.py
import os
import sys
import django
from dbfread import DBF
from django.db import connection

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import MedidasEstados
from apps.maestros.models.base_models import ProductoCai
from apps.maestros.models.base_models import ProductoEstado

def reset_medidas_estados():
    """Elimina los datos existentes en la tabla y resetea su ID."""
    MedidasEstados.objects.all().delete()
    print("Tabla MedidasEstados limpiada.")

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='medidas_estados';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('medidas_estados', 'id_medida_estado'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('medidas_estados', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE medidas_estados AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_datos():
    """Lee los datos de la tabla medidasestados.DBF y asigna ID manualmente con el índice del bucle."""
    reset_medidas_estados()

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'medidasestados.DBF')

    # Abrir la tabla de Visual FoxPro
    table = DBF(dbf_path, encoding='latin-1')

    # Filtrar los registros donde ESTADO sea igual a "P"
    filtered_records = [record for record in table if record['ESTADO'] == 'P']

    registros_crear = []
    
    for idx, record in enumerate(filtered_records, start=1):
        stock_desde = record['DESDE']
        stock_hasta = record['HASTA']

        # Obtener ProductoCai
        cai_value = record['CAI'].strip() if record['CAI'] else ""
        producto_cai = None
        if cai_value:
            try:
                producto_cai = ProductoCai.objects.get(cai=cai_value)
            except ProductoCai.DoesNotExist:
                producto_cai = None

        # Obtener ProductoEstado (id_estado = 3)
        producto_estado = None
        try:
            producto_estado = ProductoEstado.objects.get(id_producto_estado=3)
        except ProductoEstado.DoesNotExist:
            producto_estado = None

        # Crear registro con ID explícito (el índice del bucle)
        registros_crear.append(
            MedidasEstados(
                id_medida_estado=idx,  # ← Asignar el índice como ID
                estatus_medida_estado=True,
                id_cai=producto_cai,
                id_estado=producto_estado,
                stock_desde=stock_desde,
                stock_hasta=stock_hasta
            )
        )

    # Crear todos los registros en lote
    if registros_crear:
        MedidasEstados.objects.bulk_create(registros_crear)
        print(f"Se han migrado {len(registros_crear)} registros de MedidasEstados con IDs desde 1 hasta {len(registros_crear)}.")
    else:
        print("No se encontraron registros para migrar.")

if __name__ == '__main__':
    cargar_datos()
    print("Migración de MedidasEstados completada.")
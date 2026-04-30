# neumatic\data_load\producto_familia_migra.py
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

from apps.maestros.models.base_models import ProductoFamilia

def reset_producto_familia():
    """Elimina los datos existentes en la tabla ProductoFamilia y resetea su ID."""
    ProductoFamilia.objects.all().delete()
    print("Tabla ProductoFamilia limpiada.")

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto_familia';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('producto_familia', 'id_producto_familia'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('producto_familia', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE producto_familia AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_datos():
    """Lee los datos de la tabla articulo.dBF y asigna el CODIGO como ID"""
    reset_producto_familia()

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'articulo.DBF')

    # Abrir la tabla de Visual FoxPro
    table = DBF(dbf_path, encoding='latin-1')

    registros_crear = []
    
    for record in table:
        codigo = record['CODIGO']
        
        # Obtener los valores
        nombre_producto_familia = record['NOMBRE'].strip() if record['NOMBRE'] else ''
        
        comision_operario = record.get('COMISIONOP')
        if comision_operario is None or comision_operario == '':
            comision_operario = 0
        else:
            try:
                comision_operario = float(comision_operario)
            except:
                comision_operario = 0
        
        info_michelin_auto = record.get('XTRAXTORA') == 'T'
        info_michelin_camion = record.get('XTRAXTORC') == 'T'

        # Crear registro con ID explícito (el CODIGO del DBF)
        registros_crear.append(
            ProductoFamilia(
                id_producto_familia=codigo,  # ← Asignar el CODIGO como ID
                estatus_producto_familia=True,
                nombre_producto_familia=nombre_producto_familia,
                comision_operario=comision_operario,
                info_michelin_auto=info_michelin_auto,
                info_michelin_camion=info_michelin_camion
            )
        )

    # Crear todos los registros en lote
    ProductoFamilia.objects.bulk_create(registros_crear)
    
    print(f"Se han migrado {len(registros_crear)} registros de ProductoFamilia.")

if __name__ == '__main__':
    cargar_datos()
    print("Migración de ProductoFamilia completada.")
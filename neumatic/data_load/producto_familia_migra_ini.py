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
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('producto_familia', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        else:
            print(f"Motor {engine} - No se requiere reset automático de secuencia.")

def cargar_datos():
    """Lee los datos de la tabla articulo.dbf, asegura que el código sea consecutivo,
    migra los datos al modelo ProductoFamilia y elimina los registros marcados como pendientes."""
    reset_producto_familia()  # Eliminar datos existentes antes de migrar

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'articulo.DBF')

    # Abrir la tabla de Visual FoxPro usando dbfread y ordenarla por CODIGO
    table = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda r: r['CODIGO'])

    expected_codigo = 1  # El código esperado para asegurar consecutividad

    for record in table:
        codigo = record['CODIGO']

        # Revisar si el código es consecutivo
        while expected_codigo < codigo:
            # Insertar un registro pendiente si hay un salto en el código
            ProductoFamilia.objects.create(
                estatus_producto_familia=True,
                nombre_producto_familia="PENDIENTE POR ELIMINAR",
                comision_operario=0,  # Comisión por defecto
                info_michelin_auto=False,  # Valor por defecto
                info_michelin_camion=False  # Valor por defecto
            )
            expected_codigo += 1

        # Obtener los valores y manejar nulos
        nombre_producto_familia = record['NOMBRE'].strip()
        comision_operario = record['COMISIONOP'] if record['COMISIONOP'] else 0  # Si es nulo o vacío, asignar 0
        info_michelin_auto = record['XTRAXTORA'] if record['XTRAXTORA'] else False  # Si es nulo, asignar False
        info_michelin_camion = record['XTRAXTORC'] if record['XTRAXTORC'] else False  # Si es nulo, asignar False

        # Crear el registro actual
        ProductoFamilia.objects.create(
            estatus_producto_familia=True,
            nombre_producto_familia=nombre_producto_familia,
            comision_operario=comision_operario,
            info_michelin_auto=info_michelin_auto,
            info_michelin_camion=info_michelin_camion
        )

        expected_codigo += 1

    # Eliminar los registros marcados como "PENDIENTE POR ELIMINAR"
    ProductoFamilia.objects.filter(nombre_producto_familia="PENDIENTE POR ELIMINAR").delete()

if __name__ == '__main__':
    cargar_datos()
    print("Migración de ProductoFamilia completada.")

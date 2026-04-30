# neumatic\data_load\producto_modelo_migra.py
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

from apps.maestros.models.base_models import ProductoModelo

def reset_producto_modelo():
    """Elimina los datos existentes en la tabla ProductoModelo y resetea su ID en SQLite."""
    ProductoModelo.objects.all().delete()  # Eliminar los datos existentes
    
    # Reiniciar el autoincremento en SQLite
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto_modelo';")

def cargar_datos():
    """Lee los datos de la tabla modelos.dbf, asegura que el código sea consecutivo,
    migra los datos al modelo ProductoModelo y elimina los registros marcados como pendientes."""
    reset_producto_modelo()  # Eliminar datos existentes antes de migrar

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'modelos.DBF')

    # Abrir la tabla de Visual FoxPro usando dbfread y ordenarla por CODIGO
    table = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda r: r['CODIGO'])

    total_registros = len(table)
    print(f"Total de registros a procesar: {total_registros}")

    for record in table:
        codigo = record['CODIGO']
        nombre = record['NOMBRE'].strip()

        # Crear el registro actual
        ProductoModelo.objects.create(
            id_modelo = codigo,
            estatus_modelo=True,
            nombre_modelo=nombre
        )
    

if __name__ == '__main__':
    cargar_datos()
    print("Migración de ProductoModelo completada.")

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

def reset_tabla():
    """Elimina los datos existentes en la tabla y resetea su ID en SQLite."""
    MedidasEstados.objects.all().delete()  # Eliminar los datos existentes
    print("Tabla limpiada.")

    # Reiniciar el autoincremento en SQLite
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='medidas_estados';")
    print("Secuencia de ID reseteada.")

def cargar_datos():
    """Lee los datos de la tabla actividad.DBF, verifica consecutividad de códigos,
    migra los registros al modelo Actividad y añade pendientes si hay saltos en los códigos."""
    reset_tabla()  # Limpiar datos existentes

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'medidasestados.DBF')

    # Abrir la tabla de Visual FoxPro y ordenarla por CODIGO
    # table = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda r: r['CODIGO'])
    table = DBF(dbf_path, encoding='latin-1')

    # Filtrar los registros donde ESTADO sea igual a "P"
    filtered_records = [record for record in table if record['ESTADO'] == 'P']

    # Recorrer la tabla e insertar los registros
    for record in filtered_records:
        estatus_medida_estado = True
        stock_desde = record['DESDE']
        stock_hasta = record['HASTA']

        cai_value = record['CAI'].strip()
        producto_cai = None
        if cai_value:  # Verificar que CAI no esté vacío
            try:
                producto_cai = ProductoCai.objects.get(cai=cai_value)
            except ProductoCai.DoesNotExist:
                producto_cai = None

        # Buscar la instancia de ProductoEstado para id_estado
        producto_estado = None
        try:
            # Asumiendo que 3 es el valor del campo 'id' o un campo único en ProductoEstado
            producto_estado = ProductoEstado.objects.get(id_producto_estado=3)
        except ProductoEstado.DoesNotExist:
            producto_estado = None  # Asignar None si no se encuentra

        # Crear el registro actual
        MedidasEstados.objects.create(
             estatus_medida_estado=estatus_medida_estado,
             id_cai=producto_cai,  # Asignar el objeto ProductoCai o None
             id_estado=producto_estado,
             stock_desde=stock_desde,
             stock_hasta=stock_hasta
         )

    print(f"Se han migrado {len(table)} registros de MedidasEstados de forma exitosa.")

if __name__ == '__main__':
    cargar_datos()
    print("Migración de MedidasEstados completada.")


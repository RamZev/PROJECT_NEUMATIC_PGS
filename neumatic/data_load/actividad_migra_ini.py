# neumatic\data_load\actividad_migra.py
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

from apps.maestros.models.base_models import Actividad  # Asegúrate de que esta ruta sea correcta

def reset_actividad():
    """Elimina los datos existentes en la tabla Actividad y resetea su ID en SQLite."""
    Actividad.objects.all().delete()  # Eliminar los datos existentes
    print("Tabla Actividad limpiada.")

    # Reiniciar el autoincremento en SQLite
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='actividad';")
    print("Secuencia de ID reseteada.")

def cargar_datos():
    """Lee los datos de la tabla actividad.DBF, verifica consecutividad de códigos,
    migra los registros al modelo Actividad y añade pendientes si hay saltos en los códigos."""
    reset_actividad()  # Limpiar datos existentes

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'actividad.DBF')

    # Abrir la tabla de Visual FoxPro y ordenarla por CODIGO
    table = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda r: r['CODIGO'])

    expected_codigo = 1  # Código esperado para verificar consecutividad

    for record in table:
        codigo = record['CODIGO']
        nombre = record['NOMBRE'].strip()

        # Verificar si el código es consecutivo
        while expected_codigo < codigo:
            # Insertar registro pendiente si falta un código
            Actividad.objects.create(
                estatus_actividad=True,
                descripcion_actividad="PENDIENTE DE ELIMINACIÓN"
            )
            print(f"Se insertó registro pendiente para el código faltante: {expected_codigo}")
            expected_codigo += 1

        # Crear el registro actual
        Actividad.objects.create(
            estatus_actividad=True,
            descripcion_actividad=nombre
        )

        expected_codigo += 1

    # Opcional: Eliminar los registros pendientes si es necesario
    Actividad.objects.filter(descripcion_actividad="PENDIENTE DE ELIMINACIÓN").delete()

    print(f"Se han migrado {len(table)} registros de Actividad de forma exitosa.")

if __name__ == '__main__':
    cargar_datos()
    print("Migración de Actividad completada.")


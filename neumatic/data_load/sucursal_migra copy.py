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

from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.base_models import Localidad, Provincia 

def reset_sucursal():
    """Elimina los datos existentes en la tabla Sucursal y resetea su ID en SQLite."""
    Sucursal.objects.all().delete()  # Eliminar los datos existentes
    print("Tabla Sucursal limpiada.")

    # Reiniciar el autoincremento en SQLite
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='sucursal';")
    print("Secuencia de ID reseteada.")

def cargar_datos():
    """Lee los datos de la tabla sucursal.DBF, verifica consecutividad de ID,
    migra los registros al modelo Sucursal y añade pendientes si hay saltos en los códigos."""
    reset_sucursal()  # Limpiar datos existentes

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'sucursal.DBF')

    # Abrir la tabla de Visual FoxPro y ordenarla por ID
    table = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda r: r['ID'])

    # Obtener objetos de Localidad y Provincia
    localidad_default = Localidad.objects.get(id_localidad=1)  # Localidad con ID 1
    provincia_default = Provincia.objects.get(id_provincia=13)  # Provincia con ID 13

    expected_id = 1  # ID esperado para verificar consecutividad

    for record in table:
        sucursal_id = record['ID']
        nombre = record['NOMBRE'].strip()
        domicilio = record['DOMICILIO'].strip()
        telefono = record['TELEFONO'].strip()
        localidad = localidad_default
        provincia = provincia_default
        email = record['EMAIL'].strip()
        inicio_actividad = record['INICIOACT']
        codigo_michelin = record['MICHELIN']

        # Verificar si el ID es consecutivo
        while expected_id < sucursal_id:
            # Insertar registro pendiente si falta un ID
            Sucursal.objects.create(
                estatus_sucursal=True,
                nombre_sucursal="PENDIENTE DE ELIMINACIÓN",
                codigo_michelin=0,
                domicilio_sucursal="",
                id_localidad=localidad,
                id_provincia=provincia,
                telefono_sucursal="",
                email_sucursal="",
                inicio_actividad=None
            )
            print(f"Se insertó registro pendiente para el ID faltante: {expected_id}")
            expected_id += 1

        # Crear el registro actual
        Sucursal.objects.create(
            estatus_sucursal=True,
            nombre_sucursal=nombre,
            codigo_michelin=codigo_michelin,
            domicilio_sucursal=domicilio,
            id_localidad=localidad,
            id_provincia=provincia,
            telefono_sucursal=telefono,
            email_sucursal=email,
            inicio_actividad=inicio_actividad
        )

        expected_id += 1

    # Opcional: Eliminar los registros pendientes si es necesario
    Sucursal.objects.filter(nombre_sucursal="PENDIENTE DE ELIMINACIÓN").delete()

    print(f"Se han migrado {len(table)} registros de Sucursal de forma exitosa.")

if __name__ == '__main__':
    cargar_datos()
    print("Migración de Sucursal completada.")

# neumatic\data_load\numero_migra.py
import os
import sys
import django
import time  # Para medir el tiempo de procesamiento
import pandas as pd
from django.db import connection
from django.core.exceptions import ValidationError

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.numero_models import Numero
from apps.maestros.models.base_models import PuntoVenta
from apps.maestros.models.sucursal_models import Sucursal

def reset_numero():
    """Elimina los datos existentes en la tabla Numero y resetea su ID."""
    Numero.objects.all().delete()
    print("Tabla Numero limpiada.")
    
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='numero';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('numero', 'id_numero'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('numero', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE numero AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_datos():
    """Lee los datos del archivo Excel, migra los datos al modelo Numero."""
    reset_numero()  # Eliminar datos existentes antes de migrar

    # Ruta del archivo Excel
    excel_path = os.path.join(BASE_DIR, 'data_load', 'numeracion.xlsx')

    # Leer el archivo Excel
    df = pd.read_excel(excel_path, sheet_name='numeracion')

    total_registros = len(df)  # Número total de registros
    print(f"Total de registros a procesar: {total_registros}")

    for idx, row in df.iterrows():
        # Obtener los valores de las columnas
        sucursal_id = row['sucursal']
        comprobante = row['comprobante']
        punto_venta_excel = row['puntoventa']
        numero = row['numero']
        letra = row['letra']
        lineas = row['renglones']
        copias = row['copias']

        # Formatear el valor de PUNTOVENTA con ceros a la izquierda (5 caracteres)
        punto_venta_str = f"{int(punto_venta_excel):05d}"

        # Buscar el id_sucursal en el modelo Sucursal
        try:
            sucursal = Sucursal.objects.get(pk=sucursal_id)
        except Sucursal.DoesNotExist:
            print(f"Sucursal no encontrada para id {sucursal_id}. Saltando registro.")
            continue

        # Buscar el id_punto_venta en el modelo PuntoVenta
        try:
            # punto_venta = PuntoVenta.objects.get(
            #     id_sucursal=sucursal_id,
            #     punto_venta=punto_venta_str
            # )

            punto_venta = PuntoVenta.objects.filter(
                id_sucursal=sucursal_id,
                punto_venta=punto_venta_str
            ).first()  # Cambiamos get() por filter().first()

        except PuntoVenta.DoesNotExist:
            print(f"Punto de venta no encontrado para sucursal {sucursal_id} y punto de venta {punto_venta_str}")
            continue

        # Crear una instancia del modelo Numero
        numero_obj = Numero(
            id_sucursal=sucursal,  # Instancia de Sucursal
            comprobante=comprobante,
            id_punto_venta=punto_venta,  # Instancia de PuntoVenta
            numero=numero,
            letra=letra,
            lineas=lineas,
            copias=copias
        )

        # Validar y guardar la instancia
        try:
            numero_obj.full_clean()  # Validar los campos según las reglas del modelo
            numero_obj.save()
            print(f"Guardado: {numero_obj} comprobante {comprobante} numero {numero}")
        except ValidationError as e:
            print(f"Error de validación para la fila {idx} comprobante {comprobante} numero {numero}: {e}")

        # Mostrar mensaje cada 1000 registros procesados
        if (idx + 1) % 1000 == 0:
            print(f"{idx + 1} registros procesados...")

if __name__ == '__main__':
    start_time = time.time()  # Empezar el control de tiempo
    cargar_datos()
    end_time = time.time()  # Terminar el control de tiempo

    # Calcular el tiempo total en minutos y segundos
    elapsed_time = end_time - start_time
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60

    print(f"Migración de Numero completada.")
    print(f"Tiempo de procesamiento: {int(minutes)} minutos y {int(seconds)} segundos.")
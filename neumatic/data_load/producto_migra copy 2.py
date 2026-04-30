# neumatic\data_load\producto_migra.py
import os
import sys
import django
import time  # Para medir el tiempo de procesamiento
from dbfread import DBF
from django.db import connection

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.producto_models import Producto
from apps.maestros.models.base_models import ProductoFamilia
from apps.maestros.models.base_models import ProductoMarca
from apps.maestros.models.base_models import ProductoModelo

def reset_producto():
    """Elimina los datos existentes en la tabla Producto y resetea su ID en SQLite."""
    Producto.objects.all().delete()  # Eliminar los datos existentes
    
    # Reiniciar el autoincremento en SQLite
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto';")

def cargar_datos():
    """Lee los datos de la tabla lista.dbf, asegura que el código sea consecutivo,
    migra los datos al modelo Producto y elimina los registros marcados como pendientes."""
    reset_producto()  # Eliminar datos existentes antes de migrar

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'lista.DBF')

    # Abrir la tabla de Visual FoxPro usando dbfread y ordenarla por CODIGO
    table = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda r: r['CODIGO'])

    expected_codigo = 1  # El código esperado para asegurar consecutividad
    total_registros = len(table)  # Número total de registros

    print(f"Total de registros a procesar: {total_registros}")

    for idx, record in enumerate(table):
        codigo = record['CODIGO']

        # Revisar si el código es consecutivo
        while expected_codigo < codigo:
            # Insertar un registro pendiente si hay un salto en el código
            Producto.objects.create(
                estatus_producto=True,
                codigo_producto=9999999,
                tipo_producto="P",  # Valor temporal hasta que se corrija el código
                id_familia=ProductoFamilia.objects.get(pk=6),  # Usar instancia de ProductoFamilia
                id_marca=ProductoMarca.objects.get(pk=1),  # Usar instancia de ProductoMarca
                id_modelo=ProductoModelo.objects.get(pk=1),  # Usar instancia de ProductoModelo
                cai="",
                medida="",
                segmento="",
                nombre_producto="PENDIENTE POR ELIMINAR",
                unidad=1,
                fecha_fabricacion="",
                costo=0.0,
                alicuota_iva=0.0,
                precio=0.0,
                stock=1,
                minimo=1,
                descuento=0.0,
                despacho_1="",
                despacho_2="",
                descripcion_producto="",
                carrito=False
            )
            expected_codigo += 1

        # Obtener instancias relacionadas para ProductoFamilia, ProductoMarca y ProductoModelo
        try:
            familia = ProductoFamilia.objects.get(pk=record['ARTICULO'])
            marca = ProductoMarca.objects.get(pk=record['MARCA'])
            modelo = ProductoModelo.objects.get(pk=record['MODELO'])
        except ProductoFamilia.DoesNotExist:
            continue  # Saltar al siguiente registro si hay un error
        except ProductoMarca.DoesNotExist:
            continue
        except ProductoModelo.DoesNotExist:
            continue

        # Crear el registro actual
        Producto.objects.create(
            estatus_producto=True,
            codigo_producto=9999999,
            tipo_producto=record['TIPO'].strip(),
            id_familia=familia,  # Asignar la instancia de ProductoFamilia
            id_marca=marca,  # Asignar la instancia de ProductoMarca
            id_modelo=modelo,  # Asignar la instancia de ProductoModelo
            # id_cai
            cai=record['CODFABRICA'].strip(),
            medida=record['MEDIDA'].strip(),
            segmento=record['SEGMENTO'].strip(),
            nombre_producto=record['NOMBRE'].strip(),
            unidad=record['UNIDAD'],
            fecha_fabricacion=record['FECHA'].strip(),
            costo=record['COSTO'],
            alicuota_iva=record['IVA'],
            precio=record['PRECIO'],
            stock=record['STOCK'],
            minimo=record['MINIMO'],
            descuento=record['DESCUENTO'],
            despacho_1=record['DESPACHO1'].strip(),
            despacho_2=record['DESPACHO2'].strip(),
            descripcion_producto=record['DETALLE'].strip(),
            carrito=record['CARRITO']
        )

        expected_codigo += 1

        # Mostrar mensaje cada 100 registros procesados
        if (idx + 1) % 100 == 0:
            print(f"{idx + 1} registros procesados...")

    # Eliminar los registros marcados como "PENDIENTE POR ELIMINAR"
    Producto.objects.filter(nombre_producto="PENDIENTE POR ELIMINAR").delete()

if __name__ == '__main__':
    start_time = time.time()  # Empezar el control de tiempo
    cargar_datos()
    end_time = time.time()  # Terminar el control de tiempo

    # Calcular el tiempo total en minutos y segundos
    elapsed_time = end_time - start_time
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60

    print(f"Migración de Producto completada.")
    print(f"Tiempo de procesamiento: {int(minutes)} minutos y {int(seconds)} segundos.")

# neumatic\data_load\producto_marca_migra.py
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

from apps.maestros.models.base_models import ProductoMarca, Moneda

def reset_producto_marca():
    """Elimina los datos existentes en la tabla ProductoMarca y resetea su ID."""
    ProductoMarca.objects.all().delete()
    print("Tabla ProductoMarca limpiada.")

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto_marca';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('producto_marca', 'id_producto_marca'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('producto_marca', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE producto_marca AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def obtener_moneda_manual(id_moneda, nombre_moneda, cotizacion_moneda=1, simbolo_moneda="", ws_afip="", predeterminada=False):
    """Crea una instancia de Moneda manualmente sin consultar la BD"""
    return Moneda(
        id_moneda=id_moneda,
        estatus_moneda=True,
        nombre_moneda=nombre_moneda,
        cotizacion_moneda=cotizacion_moneda,
        simbolo_moneda=simbolo_moneda,
        ws_afip=ws_afip,
        predeterminada=predeterminada
    )

def cargar_datos():
    """Lee los datos de la tabla marcas.dBF y asigna el CODIGO como ID"""
    reset_producto_marca()

    # Crear instancias de moneda manualmente (sin consultar la BD)
    moneda_pesos = obtener_moneda_manual(1, "PESOS", 1, "$", "", True)
    moneda_dolar = obtener_moneda_manual(2, "DOLAR", 1, "U$S", "", False)
    moneda_otra = obtener_moneda_manual(4, "OTRA", 1, "", "", False)
    
    print("Monedas creadas manualmente")

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'marcas.DBF')

    # Abrir la tabla de Visual FoxPro
    table = DBF(dbf_path, encoding='latin-1')
    
    print("Tamaño de la Tabla:", len(table))

    registros_crear = []

    for record in table:
        codigo = record['CODIGO']
        
        # Obtener la instancia de moneda según el valor en el registro
        moneda = record['MONEDA'].strip() if record['MONEDA'] else ""

        # Determinar la instancia de moneda
        if moneda == "P":
            moneda_instancia = moneda_pesos
        elif moneda == "D":
            moneda_instancia = moneda_dolar
        else:
            moneda_instancia = moneda_otra

        # Crear registro con ID explícito (el CODIGO del DBF)
        registros_crear.append(
            ProductoMarca(
                id_producto_marca=codigo,
                estatus_producto_marca=True,
                nombre_producto_marca=record['NOMBRE'].strip(),
                principal=not bool(record['OTRAS']),
                info_michelin_auto=bool(record['XTRAXTORA']),
                info_michelin_camion=bool(record['XTRAXTORC']),
                id_moneda=moneda_instancia
            )
        )

    # Crear todos los registros en lote
    if registros_crear:
        ProductoMarca.objects.bulk_create(registros_crear)
        print(f"Se han migrado {len(registros_crear)} registros de ProductoMarca.")
    else:
        print("No se crearon registros.")

if __name__ == '__main__':
    cargar_datos()
    print("Migración de ProductoMarca completada.")
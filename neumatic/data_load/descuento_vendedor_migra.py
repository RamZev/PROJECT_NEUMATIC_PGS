# neumatic\data_load\descuento_vendedor_migra.py
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

from apps.maestros.models.descuento_vendedor_models import DescuentoVendedor 
from apps.maestros.models.base_models import ProductoMarca, ProductoFamilia

def reset_descuento_vendedor():
    """Elimina los datos existentes en la tabla DescuentoVendedor y resetea su ID."""
    DescuentoVendedor.objects.all().delete()
    print("Tabla DescuentoVendedor limpiada.")
    
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='descuento_vendedor';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('descuento_vendedor', 'id_descuento_vendedor'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('descuento_vendedor', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE descuento_vendedor AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_datos():
    """Lee los datos de la tabla descvend.DBF y migra los registros al modelo DescuentoVendedor"""
    reset_descuento_vendedor()

    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'descvend.DBF')

    # Abrir la tabla de Visual FoxPro
    table = DBF(dbf_path, encoding='latin-1')

    # Precargar marcas y familias para evitar el bug del driver
    marcas_dict = {m.id_producto_marca: m for m in ProductoMarca.objects.only('id_producto_marca')}
    familias_dict = {f.id_producto_familia: f for f in ProductoFamilia.objects.only('id_producto_familia')}
    
    registros_crear = []
    contador_id = 1  # ← Contador para ID manual
    registros_procesados = 0
    errores = 0

    for record in table:
        marca = int(record.get('MARCA', 0))
        familia = int(record.get('ARTICULO', 0))
        
        # Obtener instancias de los diccionarios precargados
        id_marca_instancia = marcas_dict.get(marca)
        id_familia_instancia = familias_dict.get(familia)
        
        if not id_marca_instancia:
            print(f"Advertencia: No se encontró ProductoMarca con ID {marca}. Saltando registro.")
            errores += 1
            continue
        
        if not id_familia_instancia:
            print(f"Advertencia: No se encontró ProductoFamilia con ID {familia}. Saltando registro.")
            errores += 1
            continue
        
        # Crear registro con ID manual
        registros_crear.append(
            DescuentoVendedor(
                id_descuento_vendedor=contador_id,  # ← Asignar ID manual
                estatus_descuento_vendedor=True,
                id_marca=id_marca_instancia,
                id_familia=id_familia_instancia,
                desc1=float(record.get('DESC1') or 0),    
                desc2=float(record.get('DESC2') or 0),    
                desc3=float(record.get('DESC3') or 0),    
                desc4=float(record.get('DESC4') or 0),    
                desc5=float(record.get('DESC5') or 0),    
                desc6=float(record.get('DESC6') or 0),    
                desc7=float(record.get('DESC7') or 0),    
                desc8=float(record.get('DESC8') or 0),    
                desc9=float(record.get('DESC9') or 0),    
                desc10=float(record.get('DESC10') or 0),
                desc11=float(record.get('DESC11') or 0),    
                desc12=float(record.get('DESC12') or 0),    
                desc13=float(record.get('DESC13') or 0),    
                desc14=float(record.get('DESC14') or 0),    
                desc15=float(record.get('DESC15') or 0),    
                desc16=float(record.get('DESC16') or 0),    
                desc17=float(record.get('DESC17') or 0),    
                desc18=float(record.get('DESC18') or 0),    
                desc19=float(record.get('DESC19') or 0),    
                desc20=float(record.get('DESC20') or 0),
                desc21=float(record.get('DESC21') or 0),    
                desc22=float(record.get('DESC22') or 0),    
                desc23=float(record.get('DESC23') or 0),    
                desc24=float(record.get('DESC24') or 0),    
                desc25=float(record.get('DESC25') or 0),
            )
        )
        contador_id += 1
        registros_procesados += 1

    # Crear todos los registros en lote
    if registros_crear:
        DescuentoVendedor.objects.bulk_create(registros_crear)
        print(f"Se han migrado {registros_procesados} registros de DescuentoVendedor de forma exitosa.")
        print(f"Errores: {errores}")
    else:
        print("No se crearon registros.")

if __name__ == '__main__':
    cargar_datos()
    print("Migración de Descuento Proveedor completada.")


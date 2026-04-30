# neumatic\data_load\producto_stock_migra.py
import os
import sys
import django
import time
from dbfread import DBF
from django.db import connection
from datetime import date
from django.db import transaction

# Configuración del entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

# Importación de los modelos
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.base_models import ProductoStock, ProductoDeposito

def reset_producto_stock():
    """Elimina todos los registros de ProductoStock y resetea la secuencia"""
    ProductoStock.objects.all().delete()
    print("Tabla ProductoStock limpiada.")
    
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto_stock';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('producto_stock', 'id_producto_stock'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('producto_stock', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE producto_stock AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def precargar_productos():
    """Precarga todos los productos en un diccionario usando values_list (evita el bug)"""
    productos = {}
    for p in Producto.objects.values_list('id_producto', flat=True):
        productos[p] = Producto(id_producto=p)
    print(f"📦 Productos precargados: {len(productos)}")
    return productos

def precargar_depositos():
    """Precarga todos los depósitos en un diccionario usando values_list (evita el bug)"""
    depositos = {}
    for d in ProductoDeposito.objects.values_list('id_producto_deposito', flat=True):
        depositos[d] = ProductoDeposito(id_producto_deposito=d)
    print(f"📦 Depósitos precargados: {len(depositos)}")
    return depositos

def migrar_producto_stock():
    """Migra datos desde el DBF a la tabla ProductoStock"""
    
    # Precargar relaciones
    print("Precargando relaciones...")
    productos = precargar_productos()
    depositos = precargar_depositos()
    
    # Configuración de rutas y archivo
    tabla_origen = 'stock.DBF'
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', tabla_origen)
    
    try:
        # Leer y ordenar el archivo DBF
        table = sorted(DBF(dbf_path, encoding='latin-1'), 
                     key=lambda r: (r['CODIGO'] or 0, r['DEPOSITO'] or 0))
        total_registros = len(table)
        print(f"\n{tabla_origen}: Total de registros a procesar: {total_registros}")
        
        # Variables para el procesamiento
        batch_size = 2000
        bulk_data = []
        registros_creados = 0
        errores = 0
        inicio = time.time()
        contador_id = 1  # ← Inicializar contador para IDs manuales

        # Procesar cada registro
        for idx, record in enumerate(table, 1):
            try:
                codigo = int(record.get('CODIGO', 0))
                deposito = int(record.get('DEPOSITO', 0))
                
                # Validar relaciones usando los diccionarios precargados
                producto = productos.get(codigo)
                deposito_obj = depositos.get(deposito)
                
                if not producto or not deposito_obj:
                    if not producto:
                        print(f"Registro {idx}: Producto {codigo} no encontrado")
                    if not deposito_obj:
                        print(f"Registro {idx}: Depósito {deposito} no encontrado")
                    errores += 1
                    continue
                
                # Crear instancia con ID manual
                bulk_data.append(ProductoStock(
                    id_producto_stock=contador_id,  # ← Asignar ID manual
                    id_producto=producto,
                    id_deposito=deposito_obj,
                    stock=record.get('STOCK', 0) or 0,
                    minimo=record.get('MINIMO', 0) or 0,
                    fecha_producto_stock=record.get('FECHA', date.today()) or date.today()
                ))
                contador_id += 1  # ← Incrementar contador
                
                # Insertar por lotes
                if len(bulk_data) >= batch_size:
                    with transaction.atomic():
                        ProductoStock.objects.bulk_create(bulk_data)
                    registros_creados += len(bulk_data)
                    bulk_data.clear()
                    print(f"Procesados {registros_creados} registros...")
                    
            except Exception as e:
                print(f"Registro {idx} Código {codigo}: Error - {str(e)}")
                errores += 1
                continue
        
        # Insertar los registros restantes
        if bulk_data:
            with transaction.atomic():
                ProductoStock.objects.bulk_create(bulk_data)
            registros_creados += len(bulk_data)
        
        # Resultados finales
        tiempo_total = time.time() - inicio
        print(f"\nMigración completada en {tiempo_total:.2f} segundos")
        print(f"Total registros creados: {registros_creados}")
        print(f"Total errores: {errores}")
        if total_registros > 0:
            print(f"Eficiencia: {(registros_creados/total_registros)*100:.2f}%")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {dbf_path}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == '__main__':
    # Paso 1: Resetear la tabla
    reset_producto_stock()
    
    # Paso 2: Migrar los datos
    migrar_producto_stock()
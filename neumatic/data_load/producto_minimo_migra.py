# neumatic\data_load\producto_minimo_migra.py
import os
import sys
import django
import time
from dbfread import DBF
from django.db import connection
from datetime import date
from django.db import transaction

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

# Importación de los modelos
from apps.maestros.models.producto_models import ProductoCai
from apps.maestros.models.base_models import ProductoMinimo, ProductoDeposito

def reset_producto_minimo():
    """Elimina los datos existentes en la tabla ProductoMinimo y resetea su ID."""
    ProductoMinimo.objects.all().delete()
    print("Tabla ProductoMinimo limpiada.")
    
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto_minimo';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('producto_minimo', 'id_producto_minimo'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('producto_minimo', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE producto_minimo AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def precargar_cai():
    """Precarga todos los CAI en un diccionario usando values_list (evita el bug)"""
    cai_dict = {}
    for c in ProductoCai.objects.values_list('id_cai', 'cai'):
        cai_dict[c[1]] = ProductoCai(id_cai=c[0])
    print(f"📦 CAI precargados: {len(cai_dict)}")
    return cai_dict

def precargar_depositos():
    """Precarga todos los depósitos en un diccionario usando values_list (evita el bug)"""
    depositos = {}
    for d in ProductoDeposito.objects.values_list('id_producto_deposito', flat=True):
        depositos[d] = ProductoDeposito(id_producto_deposito=d)
    print(f"📦 Depósitos precargados: {len(depositos)}")
    return depositos

# Tabla origen y modelo destino
tabla_origen = 'listamin.DBF'
modelo_dest = ProductoMinimo

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', tabla_origen)

def migrar_datos():
    """Migra los datos asignando IDs manualmente"""
    
    # Resetear tabla
    reset_producto_minimo()
    
    # Precargar relaciones
    print("Precargando relaciones...")
    cai_dict = precargar_cai()
    depositos_dict = precargar_depositos()
    
    # Abrir la tabla de Visual FoxPro
    table = DBF(dbf_path, encoding='latin-1')
    
    total_registros = len(table)
    print(f"{tabla_origen}: Total de registros a procesar: {total_registros}")
    
    # Variables para el procesamiento
    batch_size = 2000
    bulk_data = []
    registros_creados = 0
    errores = 0
    inicio = time.time()
    contador_id = 1  # ← Contador para IDs manuales
    
    for idx, record in enumerate(table, 1):
        try:
            cai = record.get('CAI', '').strip()
            deposito = int(record.get('DEPOSITO', 0))
            minimo = int(record.get('MINIMO', 0))
            
            # Validar claves foráneas usando diccionarios precargados
            id_cai_instancia = cai_dict.get(cai)
            id_deposito_instancia = depositos_dict.get(deposito)
            
            if not id_cai_instancia:
                print(f"Registro {idx}: CAI ({cai}) no encontrado. Omitiendo.")
                errores += 1
                continue
            
            if not id_deposito_instancia:
                print(f"Registro {idx}: Depósito ({deposito}) no encontrado. Omitiendo.")
                errores += 1
                continue
            
            # Preparar datos con ID manual
            bulk_data.append(ProductoMinimo(
                id_producto_minimo=contador_id,  # ← Asignar ID manual
                id_cai=id_cai_instancia,
                id_deposito=id_deposito_instancia,
                minimo=minimo,
            ))
            contador_id += 1
            registros_creados += 1
            
            # Insertar en bloque cuando alcanzamos el tamaño del lote
            if len(bulk_data) >= batch_size:
                ProductoMinimo.objects.bulk_create(bulk_data)
                bulk_data.clear()
                print(f"Insertados {registros_creados} registros...")
                
        except Exception as e:
            print(f"Registro {idx}: Error - {e}")
            errores += 1
            continue
    
    # Insertar los registros restantes
    if bulk_data:
        ProductoMinimo.objects.bulk_create(bulk_data)
    
    # Resultados finales
    tiempo_total = time.time() - inicio
    print(f"\n✅ Migración completada en {tiempo_total:.2f} segundos")
    print(f"📊 Total registros creados: {registros_creados}")
    print(f"❌ Total errores: {errores}")
    if total_registros > 0:
        print(f"📈 Eficiencia: {(registros_creados/total_registros)*100:.2f}%")

if __name__ == '__main__':
    migrar_datos()
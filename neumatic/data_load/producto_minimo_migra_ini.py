# neumatic\data_load\producto_minimo_migra.py
import os
import sys
import django
import time  # Para medir el tiempo de procesamiento
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

# Tabla origen y modelo destino
tabla_origen = 'listamin.DBF'
modelo_dest = ProductoMinimo

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', tabla_origen)

# Abrir la tabla de Visual FoxPro usando dbfread
table = DBF(dbf_path, encoding='latin-1')

total_registros = len(table)
print(f"{tabla_origen}: Total de registros a procesar: {total_registros}")

# Migrar los datos al modelo
registros_creados = 0
inicio = time.time()  # Registrar tiempo inicial

# Procesar registros en bloques
batch_size = 2000  # Tamaño del lote para inserciones en bloque
bulk_data = []  # Lista para acumular los registros a insertar
errores = 0  # Contador de errores
registros_creados = 0  # Contador de registros creados

for idx, record in enumerate(table):
    cai = record.get('CAI', '').strip()  # Obtener y limpiar el valor de CAI
    deposito = int(record.get('DEPOSITO', 0))  # Convertir DEPOSITO a entero
    #print("MÍNIMO***:", record.get('MINIMO', 0))
    #print("CAI***:", cai)
    minimo = int(record.get('MINIMO', 0))  # Convertir MINIMO a entero

    # Validar claves foráneas
    id_cai_instancia = ProductoCai.objects.filter(cai=cai).first()
    id_deposito_instancia = ProductoDeposito.objects.filter(id_producto_deposito=deposito).first()

    # Desglose de la validación
    # Validaciones independientes
    if not id_cai_instancia:
        print(f"Registro {idx + 1}: CAI ({cai}) no encontrado. Omitiendo registro.")
        errores += 1
        continue

    if not id_deposito_instancia:
        print(f"Registro {idx + 1}: Depósito ({deposito}) no encontrado. Omitiendo registro.")
        errores += 1
        continue

    # Preparar datos para bulk_create
    try:
        nuevo_registro = ProductoMinimo(
            id_cai=id_cai_instancia,
            id_deposito=id_deposito_instancia,
            minimo=minimo,
        )
        bulk_data.append(nuevo_registro)
        registros_creados += 1

        # Insertar en bloque cuando alcanzamos el tamaño del lote
        if len(bulk_data) >= batch_size:
            ProductoMinimo.objects.bulk_create(bulk_data)
            bulk_data.clear()  # Vaciar la lista para el siguiente lote
            print(f"Se insertaron {batch_size} registros en la base de datos.")

    except Exception as e:
        print(f"Registro {idx + 1}: Error al preparar datos para insertar - {e}")
        errores += 1
        continue

# Insertar los registros restantes
if bulk_data:
    ProductoMinimo.objects.bulk_create(bulk_data)
    print(f"Se insertaron los últimos {len(bulk_data)} registros en la base de datos.")

print(f"Total de registros creados: {registros_creados}")
print(f"Total de errores: {errores}")
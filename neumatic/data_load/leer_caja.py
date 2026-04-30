# neumatic\data_load\leer_caja.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from django.db import transaction
from datetime import date

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

print("BASE_DIR:", BASE_DIR)

dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'caja.DBF')
print("Ruta DBF:", dbf_path)

# Cargar y contar registros
table = DBF(dbf_path, encoding='latin-1')
record_count = len(table)
print(f"Total de registros en DBF: {record_count}")

if record_count > 0:
    # Mostrar estructura del primer registro
    first_record = list(table)[0]
    print("\nEstructura del primer registro:")
    for key, value in first_record.items():
        print(f"  {key}: {repr(value)} (tipo: {type(value).__name__})")
    
    print(f"\nCampos disponibles: {list(first_record.keys())}")
else:
    print("El archivo DBF está vacío")
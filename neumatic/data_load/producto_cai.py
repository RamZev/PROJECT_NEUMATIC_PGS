# neumatic\data_load\producto_cai_migra.py
import os
import sys
import django
from dbfread import DBF


# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import ProductoCai

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'lista.DBF')

# Abrir la tabla de Visual FoxPro usando dbfread
table = DBF(dbf_path, encoding='latin-1')

# Filtrar registros únicos por CODFABRICA y excluir blancos
unique_codfabrica = set()
filtered_records = []

for record in table:
    codfabrica = record.get('CODFABRICA', '').strip()
    if codfabrica and codfabrica not in unique_codfabrica:
        unique_codfabrica.add(codfabrica)
        filtered_records.append(record)

total_registros = len(filtered_records)
print(f"Total de registros únicos a procesar: {total_registros}")

for record in filtered_records:
    estatus_cai = True
    cai = record['CODFABRICA'].strip()
    descripcion_cai = record['CODFABRICA'].strip()
    
    # Crear el registro actual
    ProductoCai.objects.create(
        estatus_actividad=estatus_cai,
        cai=cai,
        descripcion_cai=descripcion_cai
    )

print("Migración completada exitosamente!")
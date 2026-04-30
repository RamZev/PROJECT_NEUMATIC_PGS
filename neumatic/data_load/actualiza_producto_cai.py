# neumatic\data_load\actualiza_producto_cai.py
import os
import sys
import django
import time
from dbfread import DBF
from django.db import transaction

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.producto_models import Producto, ProductoCai

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'lista.DBF')

def asignar_cai_a_productos():
    start_time = time.time()

    # Abrir la tabla DBF
    print("Cargando datos desde la tabla DBF...")
    table = DBF(dbf_path, encoding='latin-1')

    # Crear diccionario con datos DBF
    dbf_data = {
        record['CODIGO']: record['CODFABRICA'].strip()
        for record in table
        if record['CODFABRICA'] and record['CODFABRICA'].strip()
    }
    print(f"Total registros en lista.DBF con CAI válido: {len(dbf_data)}")

    # Obtener todos los CAIs únicos que necesitamos buscar
    cais_unicos = list(set(dbf_data.values()))
    
    # Pre-cargar todos los ProductoCai en un diccionario
    cai_dict = {pc.cai: pc for pc in ProductoCai.objects.filter(cai__in=cais_unicos)}
    print(f"CAIs encontrados en base de datos: {len(cai_dict)}")

    # Procesar productos en lotes
    batch_size = 500
    productos_actualizados = 0
    productos_a_actualizar = []
    productos_sin_cai = []

    # Obtener solo los IDs de productos que tienen correspondencia en DBF
    codigos_con_cai = list(dbf_data.keys())
    
    # Procesar por lotes
    for i in range(0, len(codigos_con_cai), batch_size):
        batch_codigos = codigos_con_cai[i:i + batch_size]
        
        # Usar values_list para obtener solo los IDs (evita campos problemáticos)
        productos_batch = Producto.objects.filter(
            id_producto__in=batch_codigos
        ).values_list('id_producto', flat=True)
        
        for producto_id in productos_batch:
            valor_cai = dbf_data.get(producto_id)
            
            if valor_cai and valor_cai in cai_dict:
                productos_a_actualizar.append({
                    'id': producto_id,
                    'cai': cai_dict[valor_cai]
                })
                productos_actualizados += 1
            else:
                productos_sin_cai.append(producto_id)
    
    # Realizar las actualizaciones por lotes
    for i in range(0, len(productos_a_actualizar), batch_size):
        batch = productos_a_actualizar[i:i + batch_size]
        with transaction.atomic():
            for item in batch:
                Producto.objects.filter(id_producto=item['id']).update(id_cai=item['cai'])
        print(f"Lote actualizado: {len(batch)} productos")

    # Mostrar estadísticas
    if productos_sin_cai:
        print(f"Productos sin CAI correspondiente: {len(productos_sin_cai)}")
        if len(productos_sin_cai) <= 10:
            print(f"Ejemplos: {productos_sin_cai[:10]}")

    print(f"Total productos actualizados: {productos_actualizados}")
    print(f"Proceso completado en {time.time() - start_time:.2f} segundos.")

if __name__ == '__main__':
    asignar_cai_a_productos()
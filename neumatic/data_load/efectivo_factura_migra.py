# neumatic\data_load\efectivo_factura_migra.py
import os
import sys
import django
from dbfread import DBF
from django.db import transaction
from decimal import Decimal

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.factura_models import Factura
from apps.ventas.models.caja_models import Caja

def safe_int(value, default=0):
    try:
        return int(float(value)) if value is not None and str(value).strip() else default
    except (ValueError, TypeError):
        return default

def safe_decimal(value, default=0.0):
    try:
        if value is not None and str(value).strip():
            return Decimal(str(value))
        return Decimal(str(default))
    except (ValueError, TypeError):
        return Decimal(str(default))

def efectivo_factura_migra():
    print("Iniciando migración de efectivo...", flush=True)
    
    # Leer DBF completo a memoria
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'mediopagos.DBF')
    print(f"Cargando DBF a memoria: {dbf_path}", flush=True)
    
    # Cargar todos los registros a una lista
    table = list(DBF(dbf_path, encoding='latin-1'))
    total_registros = len(table)
    print(f"Total registros cargados en memoria: {total_registros}", flush=True)
    
    # Filtrar y procesar en memoria
    print("Filtrando registros con FORMAPAGO=1...", flush=True)
    facturas_a_actualizar_dict = {}
    ids_facturas = []
    
    for i, record in enumerate(table):
        # Mostrar progreso cada 10,000 registros
        if i % 10000 == 0:
            print(f"  Procesados {i}/{total_registros} registros...", flush=True)
        
        formapago = safe_int(record.get('FORMAPAGO'))
        idventa = safe_int(record.get('IDVENTA'))
        
        if not (formapago == 1 and idventa > 0):
            continue
        
        caja_numero = safe_int(record.get('CAJA'))
        importe = safe_decimal(record.get('IMPORTE'))
        
        ids_facturas.append(idventa)
        facturas_a_actualizar_dict[idventa] = {
            'caja_numero': caja_numero,
            'importe': importe
        }
    
    print(f"Total de facturas a procesar (FORMAPAGO=1): {len(ids_facturas)}", flush=True)
    
    # Liberar memoria del DBF (opcional, ayuda al GC)
    del table
    
    # Cargar todas las facturas de una sola vez
    print("Cargando facturas desde la base de datos...", flush=True)
    facturas_existentes = Factura.objects.filter(pk__in=ids_facturas)
    
    # Crear caché de facturas
    facturas_cache = {factura.pk: factura for factura in facturas_existentes}
    print(f"Facturas encontradas en BD: {len(facturas_cache)}", flush=True)
    
    # Cargar caché de cajas
    print("Cargando caché de cajas...", flush=True)
    cajas_cache = {caja.numero_caja: caja for caja in Caja.objects.all() if caja.numero_caja}
    print(f"Cajas cargadas: {len(cajas_cache)}", flush=True)
    
    # Archivo .tag
    tag_file = os.path.join(BASE_DIR, 'data_load', 'efectivo_no_encontradas.tag')
    with open(tag_file, 'w', encoding='utf-8') as f:
        f.write("idventa\tcaja\timporte\n")
    
    # Preparar facturas para actualizar
    print("Preparando actualizaciones...", flush=True)
    facturas_para_actualizar = []
    no_encontrados = 0
    
    for idventa, datos in facturas_a_actualizar_dict.items():
        factura = facturas_cache.get(idventa)
        
        if not factura:
            with open(tag_file, 'a', encoding='utf-8') as f:
                f.write(f"{idventa}\t{datos['caja_numero']}\t{datos['importe']}\n")
            no_encontrados += 1
            continue
        
        # Asignar caja si existe
        caja_obj = cajas_cache.get(datos['caja_numero'])
        if caja_obj:
            factura.id_caja = caja_obj
        
        # Asignar efectivo_recibo
        factura.efectivo_recibo = datos['importe']
        facturas_para_actualizar.append(factura)
    
    print(f"Facturas a actualizar: {len(facturas_para_actualizar)}", flush=True)
    print(f"Facturas no encontradas: {no_encontrados}", flush=True)
    
    # Actualizar por lotes
    batch_size = 2000
    bloques_completados = 0
    total_actualizadas = 0
    
    print("Iniciando actualización por lotes...", flush=True)
    
    for i in range(0, len(facturas_para_actualizar), batch_size):
        bloque = facturas_para_actualizar[i:i+batch_size]
        with transaction.atomic():
            Factura.objects.bulk_update(bloque, ['id_caja', 'efectivo_recibo'])
        
        bloques_completados += 1
        total_actualizadas += len(bloque)
        print(f"Bloque {bloques_completados} completado - {len(bloque)} facturas guardadas - Total actualizadas: {total_actualizadas}", flush=True)
    
    # Resumen final
    print("\n" + "="*50, flush=True)
    print("MIGRACIÓN COMPLETADA", flush=True)
    print("="*50, flush=True)
    print(f"Total bloques procesados: {bloques_completados}", flush=True)
    print(f"Facturas actualizadas: {total_actualizadas}", flush=True)
    print(f"Facturas no encontradas: {no_encontrados}", flush=True)
    print(f"Archivo de no encontradas: {tag_file}", flush=True)
    print("="*50, flush=True)

if __name__ == '__main__':
    efectivo_factura_migra()
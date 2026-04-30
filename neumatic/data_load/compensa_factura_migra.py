# neumatic\data_load\compensa_factura_migra.py
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

def compensa_factura_migra():
    # Leer DBF
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'mediopagos.DBF')
    table = DBF(dbf_path, encoding='latin-1')
    
    # Cargar caché de cajas
    cajas_cache = {caja.numero_caja: caja for caja in Caja.objects.all() if caja.numero_caja}
    
    # Archivo .tag
    tag_file = os.path.join(BASE_DIR, 'data_load', 'compensa_no_encontradas.tag')
    with open(tag_file, 'w', encoding='utf-8') as f:
        f.write("idventa\tcaja\timporte\n")
    
    # Procesar registros
    facturas_a_actualizar = []
    batch_size = 2000
    actualizados = 0
    no_encontrados = 0

    for record in table:
        formapago = safe_int(record.get('FORMAPAGO'))
        idventa = safe_int(record.get('IDVENTA'))
        
        if not (formapago == 9 and idventa > 0):
            continue

        caja_numero = safe_int(record.get('CAJA'))
        importe = safe_decimal(record.get('IMPORTE'))

        try:
            factura = Factura.objects.get(pk=idventa)
        except Factura.DoesNotExist:
            # Solo escribir en .tag, nada en consola
            with open(tag_file, 'a', encoding='utf-8') as f:
                f.write(f"{idventa}\t{caja_numero}\t{importe}\n")
            no_encontrados += 1
            continue

        # Asignar caja si existe
        caja_obj = cajas_cache.get(caja_numero)
        if caja_obj:
            factura.id_caja = caja_obj
        
        # Asignar compensa_factura
        factura.compensa_factura = importe
        facturas_a_actualizar.append(factura)
        actualizados += 1

        # Guardar por lotes
        if len(facturas_a_actualizar) >= batch_size:
            with transaction.atomic():
                Factura.objects.bulk_update(facturas_a_actualizar, ['id_caja', 'compensa_factura'])
            facturas_a_actualizar = []

    # Guardar último lote
    if facturas_a_actualizar:
        with transaction.atomic():
            Factura.objects.bulk_update(facturas_a_actualizar, ['id_caja', 'compensa_factura'])

    # Resumen final en consola
    print(f"Facturas actualizadas: {actualizados}")
    print(f"Facturas no encontradas: {no_encontrados}")
    print(f"Archivo de no encontradas: {tag_file}")

if __name__ == '__main__':
    compensa_factura_migra()
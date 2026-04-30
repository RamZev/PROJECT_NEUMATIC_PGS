# neumatic\data_load\compra_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from django.db import transaction
from datetime import date
from django.conf import settings

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import ComprobanteCompra, ProductoDeposito, Provincia
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.proveedor_models import Proveedor
from apps.ventas.models.compra_models import Compra

# Configuración de logging
logging.basicConfig(
    filename='compra_migra.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def safe_int(value, default=0):
    """Conversión segura a entero"""
    try:
        return int(float(value)) if value is not None and str(value).strip() else default
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """Conversión segura a float"""
    try:
        return float(value) if value is not None and str(value).strip() else default
    except (ValueError, TypeError):
        return default

def safe_date(value, default=None):
    """Conversión segura para fechas de DBF"""
    try:
        return value if value else default
    except (ValueError, TypeError):
        return default

def reset_compra():
    """Elimina los datos existentes de manera controlada"""
    engine = settings.DATABASES['default']['ENGINE']
    
    try:
        if 'mssql' in engine or 'sql_server' in engine:
            with connection.cursor() as cursor:
                count = Compra.objects.count()
                if count > 0:
                    print(f"Eliminando {count:,} registros existentes...")
                cursor.execute("DELETE FROM compra")
                cursor.execute("DBCC CHECKIDENT ('compra', RESEED, 0);")
                logger.info(f"Eliminados {count} registros existentes de Compra (SQL Server)")
        else:
            with transaction.atomic():
                count = Compra.objects.count()
                Compra.objects.all().delete()
                logger.info(f"Eliminados {count} registros existentes")
                
                if 'sqlite' in connection.settings_dict['ENGINE']:
                    with connection.cursor() as cursor:
                        cursor.execute("DELETE FROM sqlite_sequence WHERE name='compra';")
    except Exception as e:
        logger.error(f"Error en reset_compra: {e}")
        raise

def cargar_datos_compra():
    """Migración optimizada de compras.DBF a modelo Compra"""
    try:
        start_time = time.time()
        reset_compra()

        # Precargar relaciones usando values_list (evita el bug del driver)
        print("Precargando relaciones...")
        
        sucursales_cache = {s[0]: s[0] for s in Sucursal.objects.values_list('id_sucursal')}
        depositos_cache = {d[0]: d[0] for d in ProductoDeposito.objects.values_list('id_producto_deposito')}
        proveedores_cache = {p[0]: p[0] for p in Proveedor.objects.values_list('id_proveedor')}
        provincias_cache = {p[0]: p[0] for p in Provincia.objects.values_list('id_provincia')}
        
        # Para comprobantes, necesitamos el código y el ID
        comprobantes_cache = {c[0]: c[1] for c in ComprobanteCompra.objects.values_list('codigo_comprobante_compra', 'id_comprobante_compra')}
        
        print(f"Sucursales: {len(sucursales_cache)}")
        print(f"Depósitos: {len(depositos_cache)}")
        print(f"Proveedores: {len(proveedores_cache)}")
        print(f"Provincias: {len(provincias_cache)}")
        print(f"Comprobantes: {len(comprobantes_cache)}")

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'compras.DBF')
        table = DBF(dbf_path, encoding='latin-1')
        total_registros = len(table)
        print(f"\nTotal registros en DBF: {total_registros}")
        
        batch_size = 1000
        compras_batch = []
        registros_procesados = 0
        total_regs = 0
        errores = 0
        contador_id = 1

        for idx, record in enumerate(table, 1):
            if idx % 1000 == 0:
                print(f"Procesando {idx}/{total_registros} registros...")

            try:
                # Obtener relaciones desde caché usando IDs
                sucursal_id = safe_int(record.get('SUCURSAL'))
                id_sucursal_id = sucursales_cache.get(sucursal_id)
                
                deposito_id = safe_int(record.get('DEPOSITO'))
                id_deposito_id = depositos_cache.get(deposito_id)
                
                proveedor_id = safe_int(record.get('PROVEEDOR'))
                id_proveedor_id = proveedores_cache.get(proveedor_id)
                
                compro = record.get('COMPRO', '').strip()
                id_comprobante_id = comprobantes_cache.get(compro)
                
                provincia_val = record.get('PROVINCIA', '').strip()
                id_provincia_id = provincias_cache.get(13) if provincia_val == 'S' else None

                # Crear instancia usando IDs directamente
                compra = Compra(
                    id_compra=contador_id,
                    estatus_comprabante=True,
                    id_sucursal_id=id_sucursal_id,
                    id_punto_venta_id=None,
                    id_deposito_id=id_deposito_id,
                    id_comprobante_compra_id=id_comprobante_id,
                    compro=compro,
                    letra_comprobante=record.get('LETRA', '').strip(),
                    numero_comprobante=safe_int(record.get('NUMERO')),
                    fecha_comprobante=safe_date(record.get('FECHA')),
                    id_proveedor_id=id_proveedor_id,
                    id_provincia_id=id_provincia_id,
                    condicion_comprobante=safe_int(record.get('CONDICION')),
                    fecha_registro=safe_date(record.get('REGISTRACION')),
                    fecha_vencimiento=safe_date(record.get('VENCIMIENTO')),
                    gravado=safe_float(record.get('GRAVADO')),
                    no_gravado=safe_float(record.get('NOGRAVADO')),
                    no_inscripto=safe_float(record.get('NOINSCRIPTO')),
                    exento=safe_float(record.get('EXENTO')),
                    retencion_iva=safe_float(record.get('RETIVA')),
                    retencion_ganancia=safe_float(record.get('RETGCIA')),
                    retencion_ingreso_bruto=safe_float(record.get('RETIB')),
                    sellado=safe_float(record.get('SELLO')),
                    percepcion_iva=safe_float(record.get('PERCEPCION')),
                    percepcion_ingreso_bruto=safe_float(record.get('PERCEPCIONIB')),
                    iva=safe_float(record.get('IVA')),
                    total=safe_float(record.get('TOTAL')),
                    entrega=safe_float(record.get('ENTREGA')),
                    documento_asociado=str(safe_int(record.get('AFECTADO'))),
                    alicuota_iva=safe_float(record.get('ALICIVA')),
                    observa_comprobante=record.get('OBSERVACION', '').strip()
                )
                contador_id += 1
                
                compras_batch.append(compra)
                registros_procesados += 1

                if len(compras_batch) >= batch_size:
                    Compra.objects.bulk_create(compras_batch)
                    total_regs += len(compras_batch)
                    print(f"✅ Lote guardado: {len(compras_batch)} registros - Total: {total_regs}")
                    compras_batch = []

            except Exception as e:
                errores += 1
                if errores <= 10:
                    print(f"❌ Error en registro {idx}: {str(e)[:100]}")
                    logger.error(f"Error en registro {idx}: {str(e)}")
                continue

        if compras_batch:
            Compra.objects.bulk_create(compras_batch)
            total_regs += len(compras_batch)
            print(f"✅ Último lote guardado: {len(compras_batch)} registros")

        elapsed_time = time.time() - start_time
        mins = int(elapsed_time // 60)
        secs = int(elapsed_time % 60)
        
        print(f"\n{'='*60}")
        print(f"RESUMEN DE MIGRACIÓN DE COMPRA")
        print(f"{'='*60}")
        print(f"Total registros en DBF: {total_registros}")
        print(f"Registros procesados: {registros_procesados}")
        print(f"✅ Registros creados: {total_regs}")
        print(f"❌ Errores: {errores}")
        print(f"⏱️ Tiempo total: {mins} min {secs} seg")
        print(f"{'='*60}")

    except Exception as e:
        logger.error(f"Error fatal: {str(e)}")
        print(f"\n❌ ERROR FATAL: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_compra()
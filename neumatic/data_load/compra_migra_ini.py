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
    try:
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

        # Precargar relaciones para optimización
        sucursales_cache = {s.pk: s for s in Sucursal.objects.all()}
        depositos_cache = {d.pk: d for d in ProductoDeposito.objects.all()}
        proveedores_cache = {p.pk: p for p in Proveedor.objects.all()}
        provincias_cache = {p.pk: p for p in Provincia.objects.all()}
        comprobantes_cache = {c.codigo_comprobante_compra: c for c in ComprobanteCompra.objects.all()}

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'compras.DBF')
        table = DBF(dbf_path, encoding='latin-1')
        
        # Procesamiento por lotes
        batch_size = 1000
        compras_batch = []
        registros_procesados = 0
        total_regs = 0
        errores = 0

        for idx, record in enumerate(table, 1):
            try:
                # Procesamiento seguro de campos
                codigo_origen = safe_int(record.get('ID'))
                if not codigo_origen:
                    logger.warning(f"Registro sin ID válido en posición {idx}")
                    continue

                # Manejo especial de PROVINCIA
                provincia_val = record.get('PROVINCIA', '').strip()
                id_provincia_instancia = provincias_cache.get(13) if provincia_val == 'S' else None

                # Obtener relaciones desde caché
                sucursal_id = safe_int(record.get('SUCURSAL'))
                id_sucursal_instancia = sucursales_cache.get(sucursal_id)
                
                deposito_id = safe_int(record.get('DEPOSITO'))
                id_deposito_instancia = depositos_cache.get(deposito_id)
                
                proveedor_id = safe_int(record.get('PROVEEDOR'))
                id_proveedor_instancia = proveedores_cache.get(proveedor_id)
                
                compro = record.get('COMPRO', '').strip()
                id_comprobante_compra_instancia = comprobantes_cache.get(compro)

                # Crear instancia de Compra
                compra = Compra(
                    id_compra=codigo_origen,
                    estatus_comprabante=True,
                    id_sucursal=id_sucursal_instancia,
                    id_punto_venta=None,
                    id_deposito=id_deposito_instancia,
                    id_comprobante_compra=id_comprobante_compra_instancia,
                    compro=compro,
                    letra_comprobante=record.get('LETRA', '').strip(),
                    numero_comprobante=safe_int(record.get('NUMERO')),
                    fecha_comprobante=safe_date(record.get('FECHA')),
                    id_proveedor=id_proveedor_instancia,
                    id_provincia=id_provincia_instancia,
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
                
                compras_batch.append(compra)
                registros_procesados += 1

                # Guardar por lotes
                if len(compras_batch) >= batch_size:
                    Compra.objects.bulk_create(compras_batch)
                    logger.info(f"Lote guardado: {len(compras_batch)} registros")
                    total_regs += len(compras_batch)
                    print(f"Lote guardado: {len(compras_batch)} registros - Acumulado: {total_regs} registros")
                    compras_batch = []

            except Exception as e:
                errores += 1
                logger.error(f"Error en registro {idx} (ID: {record.get('ID')}): {str(e)}")
                continue

        # Guardar últimos registros
        if compras_batch:
            Compra.objects.bulk_create(compras_batch)
            logger.info(f"Último lote guardado: {len(compras_batch)} registros")
            total_regs += len(compras_batch)

        # Resultados finales
        elapsed_time = time.time() - start_time
        logger.info(f"Migración completada. Registros: {registros_procesados}, Errores: {errores}")
        logger.info(f"Tiempo total: {elapsed_time:.2f} segundos")

        print(f"\nResumen:")
        print(f"Registros procesados: {registros_procesados}")
        print(f"Errores encontrados: {errores}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_compra: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_compra()
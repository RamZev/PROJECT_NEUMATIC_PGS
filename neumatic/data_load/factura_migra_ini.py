# neumatic\data_load\factura_migra.py
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

from apps.maestros.models.base_models import ComprobanteVenta, ProductoDeposito
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.cliente_models import Cliente
from apps.ventas.models.factura_models import Factura

# Configuración de logging
logging.basicConfig(
    filename='factura_migra.log',
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

def reset_factura():
    """Elimina los datos existentes de manera controlada"""
    try:
        with transaction.atomic():
            count = Factura.objects.count()
            Factura.objects.all().delete()
            logger.info(f"Eliminados {count} registros existentes")
            
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='factura';")
    except Exception as e:
        logger.error(f"Error en reset_factura: {e}")
        raise

def cargar_datos_factura():
    """Versión optimizada del proceso de migración"""
    try:
        start_time = time.time()
        reset_factura()

        # Precargar relaciones para optimización
        comprobantes_cache = {c.codigo_comprobante_venta: c for c in ComprobanteVenta.objects.all()}
        sucursales_cache = {s.pk: s for s in Sucursal.objects.all()}
        depositos_cache = {d.pk: d for d in ProductoDeposito.objects.all()}
        clientes_cache = {c.pk: c for c in Cliente.objects.all()}

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'facturas.DBF')
        table = DBF(dbf_path, encoding='latin-1')
        
        # Procesamiento por lotes
        batch_size = 1000
        facturas_batch = []
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

                # Obtener relaciones desde caché
                compro = record.get('COMPRO', '').strip()
                id_comprobante_venta_instancia = comprobantes_cache.get(compro)
                
                sucursal_id = safe_int(record.get('SUCURSAL'))
                id_sucursal_instancia = sucursales_cache.get(sucursal_id)
                
                deposito_id = safe_int(record.get('DEPOSITO'))
                id_deposito_instancia = depositos_cache.get(deposito_id)
                
                cliente_id = safe_int(record.get('CLIENTE'))
                id_cliente_instancia = clientes_cache.get(cliente_id)
                
                # Obtener vendedor desde el cliente (nuevo)
                id_vendedor_instancia = None
                if id_cliente_instancia and hasattr(id_cliente_instancia, 'id_vendedor'):
                    id_vendedor_instancia = id_cliente_instancia.id_vendedor

                # Crear instancia - AQUÍ ESTÁ LA CORRECCIÓN PRINCIPAL
                

                factura = Factura(
                    id_factura=codigo_origen,
                    id_orig=codigo_origen,
                    estatus_comprobante=bool(safe_int(record.get('TRUE', 0))),
                    id_sucursal=id_sucursal_instancia,
                    id_comprobante_venta=id_comprobante_venta_instancia,
                    compro=compro,
                    letra_comprobante=record.get('LETRA', '').strip(),
                    numero_comprobante=safe_int(record.get('NUMERO')),
                    remito=record.get('REMITO', '').strip(),
                    fecha_comprobante=record.get('FECHA', date.today()),
                    id_cliente=id_cliente_instancia,
                    id_vendedor=id_vendedor_instancia,
                    cuit=safe_int(record.get('CUIT')),
                    nombre_factura=record.get('NOMBRE', '').strip(),
                    condicion_comprobante=safe_int(record.get('CONDICION')),
                    gravado=safe_float(record.get('GRAVADO')),
                    exento=safe_float(record.get('EXENTO')),
                    iva=safe_float(record.get('IVA')),	
                    percep_ib=safe_float(record.get('PERCEPIB')),
                    total=safe_float(record.get('TOTAL')),
                    entrega=safe_float(record.get('ENTREGA')),
                    estado=record.get('ESTADO', '').strip(),
                    marca=record.get('MARCA', '').strip(),
                    fecha_pago=safe_date(record.get('FECHAPAGO')),
                    no_estadist=bool(safe_int(record.get('NOESTADIST', False))),
                    suc_imp=safe_int(record.get('SUCIMP')),
                    cae=safe_int(record.get('CAE')),
                    cae_vto=record.get('CAEVTO'),
                    observa_comprobante=record.get('OBSERVA', '').strip(),
                    stock_clie=bool(safe_int(record.get('STOCKCLIE', 0))),
                    id_deposito=id_deposito_instancia,
                    promo=bool(safe_int(record.get('PROMO', 0)))
                )  # ESTE ERA EL PARÉNTESIS QUE FALTABA
                
                facturas_batch.append(factura)
                registros_procesados += 1
                

                # Guardar por lotes
                if len(facturas_batch) >= batch_size:
                    Factura.objects.bulk_create(facturas_batch)
                    logger.info(f"Lote guardado: {len(facturas_batch)} registros")
                    total_regs = total_regs + len(facturas_batch)
                    print(f"Lote guardado: {len(facturas_batch)} registros - Acumulado:  {total_regs} registros")
                    facturas_batch = []

            except Exception as e:
                errores += 1
                logger.error(f"Error en registro {idx} (ID: {record.get('ID')}): {str(e)}")
                continue

        # Guardar últimos registros
        if facturas_batch:
            Factura.objects.bulk_create(facturas_batch)

        # Resultados finales
        elapsed_time = time.time() - start_time
        logger.info(f"Migración completada. Registros: {registros_procesados}, Errores: {errores}")
        logger.info(f"Tiempo total: {elapsed_time:.2f} segundos")

        print(f"\nResumen:")
        print(f"Registros procesados: {registros_procesados}")
        print(f"Errores encontrados: {errores}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_factura: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_factura()
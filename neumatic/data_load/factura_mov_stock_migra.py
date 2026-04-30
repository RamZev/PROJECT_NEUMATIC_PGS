# neumatic\data_load\factura_mov_stock_migra.py
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

from apps.maestros.models.base_models import ComprobanteVenta, ProductoDeposito, PuntoVenta
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.cliente_models import Cliente
from apps.ventas.models.factura_models import Factura

# Configuración de logging
logging.basicConfig(
    filename='movstock_migra.log',
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

def safe_str(value, default=""):
    """Conversión segura a string"""
    try:
        return str(value).strip() if value is not None else default
    except (ValueError, TypeError):
        return default

def reset_movstock_facturas():
    """Elimina solo los registros creados por movstock.DBF"""
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    print("\n🔄 Eliminando registros previos de movstock en Factura...")
    
    try:
        # Eliminar los registros específicos
        count = Factura.objects.filter(
            compro='MI',
            letra_comprobante='X',
            nombre_factura='DEBONA MARCELO Y VICTOR HUGO'
        ).delete()[0]
        print(f"✅ Eliminados {count} registros de movstock de Factura.")
        
        with connection.cursor() as cursor:
            if 'sqlite' in engine:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='factura';")
                print("Secuencia de ID reseteada (SQLite).")
            elif 'postgresql' in engine:
                cursor.execute("SELECT setval(pg_get_serial_sequence('factura', 'id_factura'), 1, false);")
                print("Secuencia de ID reseteada (PostgreSQL).")
            elif 'mssql' in engine or 'sql_server' in engine:
                cursor.execute("DBCC CHECKIDENT ('factura', RESEED, 0);")
                print("Secuencia de ID reseteada (SQL Server).")
            elif 'mysql' in engine:
                cursor.execute("ALTER TABLE factura AUTO_INCREMENT = 1;")
                print("Secuencia de ID reseteada (MySQL).")
            else:
                print(f"Motor {engine} no requiere reset manual de secuencia.")
        
        logger.info(f"Reset movstock: Eliminados {count} registros")
        
    except Exception as e:
        print(f"⚠️ Error al resetear: {e}")
        logger.error(f"Error en reset_movstock_facturas: {e}")

def verificar_duplicados_dbf(dbf_path):
    """Verifica si hay IDs duplicados en el archivo DBF y los lista todos"""
    table = DBF(dbf_path, encoding='latin-1')
    ids_vistos = set()
    duplicados = []
    todas_ocurrencias = {}  # Para guardar todas las ocurrencias de cada ID
    
    for idx, record in enumerate(table, 1):
        codigo_origen = safe_int(record.get('ID'))
        if codigo_origen:
            if codigo_origen not in todas_ocurrencias:
                todas_ocurrencias[codigo_origen] = []
            todas_ocurrencias[codigo_origen].append(idx)
            
            if codigo_origen in ids_vistos:
                duplicados.append((idx, codigo_origen))
            else:
                ids_vistos.add(codigo_origen)
    
    # Filtrar solo los IDs que tienen duplicados
    ids_duplicados = {id_val: posiciones for id_val, posiciones in todas_ocurrencias.items() if len(posiciones) > 1}
    
    return duplicados, len(ids_vistos), ids_duplicados

def cargar_datos_movstock():
    """Migración desde movstock.DBF al modelo Factura"""
    try:
        start_time = time.time()
        
        # Limpiar registros anteriores de este mismo script
        reset_movstock_facturas()

        # VERIFICAR DUPLICADOS EN EL ARCHIVO DBF
        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'movstock.DBF')
        duplicados_dbf, total_ids, ids_duplicados = verificar_duplicados_dbf(dbf_path)
        
        # LISTADO COMPLETO DE DUPLICADOS EN EL LOG
        if ids_duplicados:
            logger.warning("=== LISTADO COMPLETO DE DUPLICADOS EN ARCHIVO DBF ===")
            for id_dup, posiciones in sorted(ids_duplicados.items()):
                logger.warning(f"ID {id_dup} aparece {len(posiciones)} veces en posiciones: {posiciones}")
            logger.warning(f"Total de IDs duplicados: {len(ids_duplicados)}")
            logger.warning(f"Total de registros duplicados: {len(duplicados_dbf)}")
            
            print(f"\n=== DUPLICADOS ENCONTRADOS EN ARCHIVO DBF ===")
            for id_dup, posiciones in sorted(ids_duplicados.items()):
                print(f"ID {id_dup}: {len(posiciones)} ocurrencias - Posiciones: {posiciones}")
            print(f"Total IDs duplicados: {len(ids_duplicados)}")
            print(f"Total registros duplicados: {len(duplicados_dbf)}")
        else:
            logger.info("No se encontraron duplicados en el archivo DBF")
            print("No se encontraron duplicados en el archivo DBF")

        # Precargar cachés usando values_list (evita el bug del driver)
        print("\n🧠 Precargando relaciones...")
        
        sucursales_list = list(Sucursal.objects.values_list('id_sucursal', flat=True))
        sucursales_cache = {sid: sid for sid in sucursales_list}
        
        depositos_list = list(ProductoDeposito.objects.values_list('id_producto_deposito', flat=True))
        depositos_cache = {did: did for did in depositos_list}
        
        puntos_venta_list = list(PuntoVenta.objects.values_list('id_punto_venta', 'id_sucursal_id'))
        puntos_venta_cache = {}
        for pv_id, suc_id in puntos_venta_list:
            if suc_id not in puntos_venta_cache:
                puntos_venta_cache[suc_id] = pv_id
        
        print(f"Sucursales: {len(sucursales_cache)}")
        print(f"Depósitos: {len(depositos_cache)}")
        print(f"Puntos de venta: {len(puntos_venta_cache)}")

        # Obtener comprobante fijo: ID 6 (o el que corresponda después de la migración)
        try:
            comprobante_fijo = ComprobanteVenta.objects.get(pk=6)
            print(f"✅ Comprobante fijo encontrado: ID {comprobante_fijo.pk}")
        except ComprobanteVenta.DoesNotExist:
            # Buscar por código 'MI'
            comprobante_fijo = ComprobanteVenta.objects.filter(codigo_comprobante_venta='MI').first()
            if comprobante_fijo:
                print(f"✅ Comprobante 'MI' encontrado con ID {comprobante_fijo.pk}")
            else:
                logger.error("ComprobanteVenta con ID=6 o código 'MI' no existe. Migración cancelada.")
                raise

        # Cliente fijo: ID 30007
        try:
            cliente_fijo = Cliente.objects.get(pk=30007)
            print(f"✅ Cliente fijo encontrado: ID {cliente_fijo.pk}")
        except Cliente.DoesNotExist:
            logger.error("Cliente con ID=30007 no existe. Migración cancelada.")
            raise

        table = DBF(dbf_path, encoding='latin-1')

        batch_size = 1000
        facturas_batch = []
        registros_procesados = 0
        errores = 0

        for idx, record in enumerate(table, 1):
            try:
                # Validar y obtener ID (será el id_factura)
                codigo_origen = safe_int(record.get('ID'))
                if not codigo_origen:
                    logger.warning(f"Registro sin ID válido en posición {idx}")
                    continue

                # Obtener sucursal desde caché
                sucursal_id = safe_int(record.get('SUCURSAL'))
                if sucursal_id not in sucursales_cache:
                    logger.warning(f"Sucursal ID={sucursal_id} no encontrada en registro {idx}")
                    continue

                # Obtener PRIMER punto de venta asociado a la sucursal
                id_punto_venta_id = puntos_venta_cache.get(sucursal_id)
                if not id_punto_venta_id:
                    logger.warning(f"No se encontró PuntoVenta para Sucursal ID={sucursal_id} en registro {idx}")
                    continue

                # Obtener depósito desde caché
                deposito_id = safe_int(record.get('DEPOSITO'))
                if deposito_id not in depositos_cache:
                    logger.warning(f"Depósito ID={deposito_id} no encontrado en registro {idx}")
                    continue

                # Campos fijos
                compro_fijo = "MI"
                letra_fija = "X"
                numero_comprobante = safe_int(record.get('NUMERO'))
                fecha_comprobante = safe_date(record.get('FECHA'), date.today())
                observa = safe_str(record.get('DESCRIPCIO'))

                # Crear instancia de Factura usando IDs directamente
                factura = Factura(
                    id_factura=codigo_origen,
                    id_orig=codigo_origen,
                    estatus_comprobante=True,
                    id_sucursal_id=sucursal_id,
                    id_punto_venta_id=id_punto_venta_id,
                    id_deposito_id=deposito_id,
                    id_comprobante_venta_id=comprobante_fijo.pk,
                    compro=compro_fijo,
                    letra_comprobante=letra_fija,
                    numero_comprobante=numero_comprobante,
                    fecha_comprobante=fecha_comprobante,
                    id_cliente_id=30007,  # ID fijo
                    cuit=30692402363,
                    nombre_factura="DEBONA MARCELO Y VICTOR HUGO",
                    condicion_comprobante=2,
                    observa_comprobante=observa,
                    gravado=0.0,
                    exento=0.0,
                    iva=0.0,
                    percep_ib=0.0,
                    total=0.0,
                    entrega=0.0,
                    estado="",
                    marca="",
                    fecha_pago=None,
                    no_estadist=False,
                    suc_imp=0,
                    cae=0,
                    cae_vto=None,
                    stock_clie=False,
                    promo=False,
                )

                facturas_batch.append(factura)
                registros_procesados += 1

                # Guardar por lotes
                if len(facturas_batch) >= batch_size:
                    Factura.objects.bulk_create(facturas_batch)
                    logger.info(f"Lote guardado: {len(facturas_batch)} registros")
                    print(f"✅ Lote guardado: {len(facturas_batch)} registros - Total: {registros_procesados}")
                    facturas_batch = []

            except Exception as e:
                errores += 1
                logger.error(f"Error en registro {idx} (ID: {record.get('ID')}): {str(e)}")
                continue

        # Guardar últimos registros
        if facturas_batch:
            Factura.objects.bulk_create(facturas_batch)
            logger.info(f"Lote final guardado: {len(facturas_batch)} registros")
            print(f"✅ Lote final guardado: {len(facturas_batch)} registros")

        # Resultados finales
        elapsed_time = time.time() - start_time
        logger.info(f"Migración completada. Registros: {registros_procesados}, Errores: {errores}")
        logger.info(f"Tiempo total: {elapsed_time:.2f} segundos")

        print(f"\n{'='*60}")
        print(f"📊 RESUMEN DE MIGRACIÓN")
        print(f"{'='*60}")
        print(f"✅ Registros procesados: {registros_procesados}")
        print(f"❌ Errores encontrados: {errores}")
        print(f"⏱️ Tiempo total: {elapsed_time:.2f} segundos")
        print(f"{'='*60}")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_movstock: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_movstock()
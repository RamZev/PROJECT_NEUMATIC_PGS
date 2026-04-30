# neumatic\data_load\factura_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from datetime import date

# --- Configuración de Entorno Django ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import ComprobanteVenta, ProductoDeposito
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.cliente_models import Cliente
from apps.ventas.models.factura_models import Factura

# --- Configuración de Logging ---
logging.basicConfig(
    filename='factura_errores.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filemode='w'
)

BATCH_SIZE = 5000  

def safe_int(value, default=0):
    try:
        return int(float(value)) if value is not None and str(value).strip() else default
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    try:
        return float(value) if value is not None and str(value).strip() else default
    except (ValueError, TypeError):
        return default

def safe_date(value):
    return value if isinstance(value, date) else None

def reset_factura():
    from django.db import connection, transaction
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    try:
        with transaction.atomic():
            if 'sqlite3' in engine:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM factura")
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='factura'")
                print("✅ Tabla Factura reseteada (SQLite).")
            elif 'mssql' in engine or 'sql_server' in engine:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM factura")
                    cursor.execute("DBCC CHECKIDENT ('factura', RESEED, 0);")
                print("✅ Tabla Factura reseteada (SQL Server).")
            else:
                Factura.objects.all().delete()
    except Exception as e:
        print(f"⚠️ Error al resetear: {e}")

def precargar_relaciones():
    print("🧠 Precargando diccionarios de validación...")
    comprobantes = {c[0]: c[1] for c in ComprobanteVenta.objects.values_list('codigo_comprobante_venta', 'id_comprobante_venta')}
    sucursales = set(Sucursal.objects.values_list('id_sucursal', flat=True))
    depositos = set(ProductoDeposito.objects.values_list('id_producto_deposito', flat=True))
    clientes_vendedores = {c[0]: c[1] for c in Cliente.objects.values_list('id_cliente', 'id_vendedor_id')}
    return {
        'comprobantes': comprobantes,
        'sucursales': sucursales,
        'depositos': depositos,
        'clientes': clientes_vendedores
    }

def ejecutar_migracion():
    reset_factura()
    cache = precargar_relaciones()
    
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'facturas.DBF')
    table = DBF(dbf_path, encoding='latin-1', load=False) 
    total_dbf = len(table)
    
    print(f"\n🚀 Iniciando migración masiva...")
    print(f"📊 Total de registros en DBF: {total_dbf}")
    print("=" * 60)
    
    batch = []
    procesados_en_lote = 0
    total_creados = 0
    errores = 0
    start_time = time.time()

    for idx, record in enumerate(table):
        current_idx = idx + 1
        try:
            id_orig = safe_int(record.get('ID'))
            if not id_orig:
                continue

            compro_str = record.get('COMPRO', '').strip()
            id_compro_venta = cache['comprobantes'].get(compro_str)
            
            if not id_compro_venta:
                errores += 1
                continue

            cliente_id = safe_int(record.get('CLIENTE'))
            sucursal_id = safe_int(record.get('SUCURSAL'))
            deposito_id = safe_int(record.get('DEPOSITO'))

            obj = Factura(
                id_factura=id_orig,
                id_orig=id_orig,
                estatus_comprobante=bool(safe_int(record.get('TRUE', 0))),
                id_sucursal_id=sucursal_id if sucursal_id in cache['sucursales'] else None,
                id_comprobante_venta_id=id_compro_venta,
                compro=compro_str,
                letra_comprobante=record.get('LETRA', '').strip()[:1],
                numero_comprobante=safe_int(record.get('NUMERO')),
                remito=record.get('REMITO', '').strip()[:20],
                fecha_comprobante=safe_date(record.get('FECHA')),
                id_cliente_id=cliente_id if cliente_id in cache['clientes'] else None,
                id_vendedor_id=cache['clientes'].get(cliente_id),
                cuit=safe_int(record.get('CUIT')),
                nombre_factura=record.get('NOMBRE', '').strip()[:100],
                condicion_comprobante=safe_int(record.get('CONDICION')),
                gravado=safe_float(record.get('GRAVADO')),
                exento=safe_float(record.get('EXENTO')),
                iva=safe_float(record.get('IVA')),
                percep_ib=safe_float(record.get('PERCEPIB')),
                total=safe_float(record.get('TOTAL')),
                entrega=safe_float(record.get('ENTREGA')),
                estado=record.get('ESTADO', '').strip()[:2],
                marca=record.get('MARCA', '').strip()[:1],
                fecha_pago=safe_date(record.get('FECHAPAGO')),
                no_estadist=bool(safe_int(record.get('NOESTADIST', 0))),
                suc_imp=safe_int(record.get('SUCIMP')),
                cae=safe_int(record.get('CAE')),
                cae_vto=safe_date(record.get('CAEVTO')),
                observa_comprobante=record.get('OBSERVA', '').strip(),
                stock_clie=bool(safe_int(record.get('STOCKCLIE', 0))),
                id_deposito_id=deposito_id if deposito_id in cache['depositos'] else None,
                promo=bool(safe_int(record.get('PROMO', 0)))
            )
            
            batch.append(obj)
            procesados_en_lote += 1

            if len(batch) >= BATCH_SIZE:
                Factura.objects.bulk_create(batch)
                total_creados += len(batch)
                batch = []
                porcentaje = (current_idx / total_dbf) * 100
                print(f"✅ Lote Guardado | Progreso: {current_idx}/{total_dbf} ({porcentaje:.1f}%) | Total OK: {total_creados} | Errores: {errores}")

            elif current_idx % 500 == 0:
                porcentaje = (current_idx / total_dbf) * 100
                print(f"⏳ Leyendo... {current_idx}/{total_dbf} ({porcentaje:.1f}%) | En memoria: {len(batch)} | Errores: {errores}")

        except Exception as e:
            errores += 1
            mensaje = f"Error en Fila {current_idx} ID:{record.get('ID')}: {str(e)}"
            print(f"❌ {mensaje}")
            logging.info(mensaje)  # Usar logging.info directamente

    if batch:
        Factura.objects.bulk_create(batch)
        total_creados += len(batch)
        print(f"✅ Lote Final Guardado | Total Final OK: {total_creados}")

    total_time = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"🏁 MIGRACIÓN COMPLETADA")
    print(f"⏱️ Tiempo total: {int(total_time // 60)}m {int(total_time % 60)}s")
    print(f"✅ Registros insertados: {total_creados}")
    print(f"❌ Registros saltados/error: {errores}")
    print("=" * 60)

if __name__ == '__main__':
    ejecutar_migracion()
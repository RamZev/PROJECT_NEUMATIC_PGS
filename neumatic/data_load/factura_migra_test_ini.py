# neumatic\data_load\factura_migra_test.py
import os
import sys
import django
import time
import logging
from dbfread import DBF

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import ComprobanteVenta, ProductoDeposito
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.cliente_models import Cliente
from apps.ventas.models.factura_models import Factura

# Configurar logging solo para errores
error_log = logging.getLogger('errores')
error_handler = logging.FileHandler('factura_errores.log', mode='w')
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
error_log.addHandler(error_handler)
error_log.setLevel(logging.INFO)

total_regs = 20000

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

def reset_factura():
    """Elimina los datos existentes"""
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    try:
        if 'mssql' in engine or 'sql_server' in engine:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM factura")
                cursor.execute("DBCC CHECKIDENT ('factura', RESEED, 0);")
            print("Tabla Factura limpiada (SQL Server).")
        else:
            Factura.objects.all().delete()
    except Exception as e:
        print(f"Error en reset: {e}")

def precargar_relaciones():
    """Precarga relaciones usando values_list"""
    print("\nPrecargando relaciones...")
    
    comprobantes_list = list(ComprobanteVenta.objects.values_list('codigo_comprobante_venta', 'id_comprobante_venta'))
    comprobantes_cache = {codigo: id_combo for codigo, id_combo in comprobantes_list}
    
    sucursales_list = list(Sucursal.objects.values_list('id_sucursal', flat=True))
    sucursales_cache = {sid: sid for sid in sucursales_list}
    
    depositos_list = list(ProductoDeposito.objects.values_list('id_producto_deposito', flat=True))
    depositos_cache = {did: did for did in depositos_list}
    
    clientes_list = list(Cliente.objects.values_list('id_cliente', 'id_vendedor_id'))
    clientes_cache = {cid: vid for cid, vid in clientes_list}
    
    print(f"Comprobantes: {len(comprobantes_cache)}")
    print(f"Sucursales: {len(sucursales_cache)}")
    print(f"Depósitos: {len(depositos_cache)}")
    print(f"Clientes: {len(clientes_cache)}")
    
    return {
        'comprobantes': comprobantes_cache,
        'sucursales': sucursales_cache,
        'depositos': depositos_cache,
        'clientes': clientes_cache
    }

def procesar_registros(limite=total_regs):
    print("=" * 60)
    print(f"PROCESANDO PRIMEROS {limite} REGISTROS")
    print("=" * 60)
    
    reset_factura()
    cache = precargar_relaciones()
    
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'facturas.DBF')
    table = DBF(dbf_path, encoding='latin-1')
    
    facturas_creadas = 0
    errores = 0
    
    start_time = time.time()
    
    for idx, record in enumerate(table):
        if idx >= limite:
            break
        
        try:
            codigo = safe_int(record.get('ID'))
            if not codigo:
                error_log.info(f"Registro {idx+1}: ID inválido o vacío")
                errores += 1
                continue
            
            compro = record.get('COMPRO', '').strip()
            sucursal_id = safe_int(record.get('SUCURSAL'))
            deposito_id = safe_int(record.get('DEPOSITO'))
            cliente_id = safe_int(record.get('CLIENTE'))
            
            # Verificar relaciones
            id_comprobante = cache['comprobantes'].get(compro)
            if not id_comprobante:
                error_log.info(f"Reg {idx+1} ID:{codigo}: Comprobante '{compro}' no existe")
                errores += 1
                continue
            
            if sucursal_id and sucursal_id not in cache['sucursales']:
                error_log.info(f"Reg {idx+1} ID:{codigo}: Sucursal {sucursal_id} no existe")
                errores += 1
                continue
            
            if deposito_id and deposito_id not in cache['depositos']:
                error_log.info(f"Reg {idx+1} ID:{codigo}: Depósito {deposito_id} no existe")
                errores += 1
                continue
            
            cliente_vendedor = cache['clientes'].get(cliente_id) if cliente_id else None
            
            # Crear factura
            factura = Factura(
                id_factura=codigo,
                id_orig=codigo,
                estatus_comprobante=bool(safe_int(record.get('TRUE', 0))),
                id_sucursal_id=sucursal_id if sucursal_id in cache['sucursales'] else None,
                id_comprobante_venta_id=id_comprobante,
                compro=compro,
                letra_comprobante=record.get('LETRA', '').strip(),
                numero_comprobante=safe_int(record.get('NUMERO')),
                remito=record.get('REMITO', '').strip(),
                fecha_comprobante=record.get('FECHA'),
                id_cliente_id=cliente_id,
                id_vendedor_id=cliente_vendedor,
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
                fecha_pago=record.get('FECHAPAGO'),
                no_estadist=bool(safe_int(record.get('NOESTADIST', False))),
                suc_imp=safe_int(record.get('SUCIMP')),
                cae=safe_int(record.get('CAE')),
                cae_vto=record.get('CAEVTO'),
                observa_comprobante=record.get('OBSERVA', '').strip(),
                stock_clie=bool(safe_int(record.get('STOCKCLIE', 0))),
                id_deposito_id=deposito_id if deposito_id in cache['depositos'] else None,
                promo=bool(safe_int(record.get('PROMO', 0)))
            )
            
            factura.save()
            facturas_creadas += 1
            
            if (idx + 1) % 100 == 0:
                print(f"Procesados {idx+1}/{limite} - OK: {facturas_creadas} - Error: {errores}")
            
        except Exception as e:
            error_log.info(f"Reg {idx+1} ID:{record.get('ID')}: EXCEPCION - {str(e)[:150]}")
            errores += 1
            continue
    
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print(f"\n{'='*60}")
    print(f"📊 RESULTADOS FINALES")
    print(f"{'='*60}")
    print(f"✅ Facturas creadas: {facturas_creadas}")
    print(f"❌ Errores: {errores}")
    print(f"📊 Total procesados: {facturas_creadas + errores}")
    print(f"⏱️ Tiempo total: {minutes} min {seconds} seg")
    print(f"\n📁 Archivo de errores: factura_errores.log")

if __name__ == '__main__':
    procesar_registros(total_regs)
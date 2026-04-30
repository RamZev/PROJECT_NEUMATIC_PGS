# neumatic\data_load\factura_migra_diag.py
import os
import sys
import django
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

def diagnosticar():
    print("=" * 60)
    print("DIAGNÓSTICO DE MIGRACIÓN DE FACTURAS")
    print("=" * 60)
    
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'facturas.DBF')
    table = DBF(dbf_path, encoding='latin-1')
    
    # Mostrar primeros 10 registros
    print("\n📋 PRIMEROS 10 REGISTROS DEL DBF:")
    print("-" * 60)
    
    for i, record in enumerate(table):
        if i >= 10:
            break
        
        print(f"\n--- Registro {i+1} ---")
        print(f"  ID: {record.get('ID')}")
        print(f"  COMPRO: '{record.get('COMPRO', '').strip()}'")
        print(f"  SUCURSAL: {record.get('SUCURSAL')}")
        print(f"  DEPOSITO: {record.get('DEPOSITO')}")
        print(f"  CLIENTE: {record.get('CLIENTE')}")
        print(f"  NUMERO: {record.get('NUMERO')}")
        print(f"  LETRA: '{record.get('LETRA', '').strip()}'")
        print(f"  FECHA: {record.get('FECHA')}")
        print(f"  TOTAL: {record.get('TOTAL')}")
        print(f"  CAE: {record.get('CAE')}")
        print(f"  CUIT: {record.get('CUIT')}")
    
    print("\n" + "=" * 60)
    print("🔍 VERIFICANDO RELACIONES EN BASE DE DATOS")
    print("=" * 60)
    
    # Verificar comprobantes
    print("\n📌 Comprobantes disponibles:")
    comprobantes = ComprobanteVenta.objects.values_list('codigo_comprobante_venta', flat=True)[:10]
    for c in comprobantes:
        print(f"   - {c}")
    
    # Verificar sucursales
    print("\n📌 Sucursales disponibles:")
    sucursales = Sucursal.objects.values_list('id_sucursal', flat=True)[:10]
    for s in sucursales:
        print(f"   - {s}")
    
    # Verificar depósitos
    print("\n📌 Depósitos disponibles:")
    depositos = ProductoDeposito.objects.values_list('id_producto_deposito', flat=True)[:10]
    for d in depositos:
        print(f"   - {d}")
    
    # Verificar clientes
    print("\n📌 Clientes disponibles (primeros 10):")
    clientes = Cliente.objects.values_list('id_cliente', flat=True)[:10]
    for c in clientes:
        print(f"   - {c}")
    
    print("\n" + "=" * 60)
    print("🧪 PROBANDO CREACIÓN DE FACTURA PASO A PASO")
    print("=" * 60)
    
    # Probar con el primer registro
    table = DBF(dbf_path, encoding='latin-1')
    primer_registro = next(iter(table))
    
    print("\n📋 Datos del primer registro:")
    print(f"  ID: {primer_registro.get('ID')}")
    print(f"  COMPRO: '{primer_registro.get('COMPRO', '').strip()}'")
    print(f"  SUCURSAL: {primer_registro.get('SUCURSAL')}")
    
    # Probar cada paso
    try:
        codigo = int(float(primer_registro.get('ID', 0)))
        print(f"\n✅ Paso 1: ID convertido = {codigo}")
    except Exception as e:
        print(f"\n❌ Paso 1 falló: {e}")
    
    try:
        compro = primer_registro.get('COMPRO', '').strip()
        comprobante = ComprobanteVenta.objects.filter(codigo_comprobante_venta=compro).first()
        if comprobante:
            print(f"✅ Paso 2: Comprobante encontrado = {comprobante.id_comprobante_venta}")
        else:
            print(f"❌ Paso 2: Comprobante '{compro}' no encontrado")
    except Exception as e:
        print(f"❌ Paso 2 falló: {e}")
    
    try:
        sucursal_id = int(float(primer_registro.get('SUCURSAL', 0)))
        sucursal = Sucursal.objects.filter(id_sucursal=sucursal_id).first()
        if sucursal:
            print(f"✅ Paso 3: Sucursal encontrada = {sucursal.id_sucursal}")
        else:
            print(f"❌ Paso 3: Sucursal {sucursal_id} no encontrada")
    except Exception as e:
        print(f"❌ Paso 3 falló: {e}")
    
    try:
        cliente_id = int(float(primer_registro.get('CLIENTE', 0)))
        cliente = Cliente.objects.filter(id_cliente=cliente_id).first()
        if cliente:
            print(f"✅ Paso 4: Cliente encontrado = {cliente.id_cliente}")
        else:
            print(f"❌ Paso 4: Cliente {cliente_id} no encontrado")
    except Exception as e:
        print(f"❌ Paso 4 falló: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 PROBANDO CREACIÓN DE FACTURA COMPLETA")
    print("=" * 60)
    
    # Intentar crear una factura de prueba
    try:
        factura = Factura(
            id_factura=1,
            id_orig=1,
            estatus_comprobante=True,
            compro="001",
            letra_comprobante="A",
            numero_comprobante=1,
            fecha_comprobante="2024-01-01",
            condicion_comprobante=1
        )
        print("✅ Factura creada en memoria (sin guardar)")
    except Exception as e:
        print(f"❌ Error creando factura en memoria: {e}")

if __name__ == '__main__':
    diagnosticar()
# neumatic\data_load\vendedor_comision_migra.py
import os
import sys
import django
import time
from dbfread import DBF
from django.db import connection
from datetime import date

# Configuración inicial de Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.vendedor_models import Vendedor
from apps.maestros.models.base_models import ProductoMarca, ProductoFamilia
from apps.maestros.models.vendedor_comision_models import (VendedorComision, 
                                                           DetalleVendedorComision)

def reset_vendedor_comision():
    """Elimina los datos existentes en las tablas objetivo y resetea IDs"""
    DetalleVendedorComision.objects.all().delete()
    VendedorComision.objects.all().delete()
    print("Tablas VendedorComision y DetalleVendedorComision limpiadas.")
    
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='vendedor_comision';")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='detalle_vendedor_comision';")
            print("Secuencias de ID reseteadas (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('vendedor_comision', 'id_vendedor_comision'), 1, false);")
            cursor.execute("SELECT setval(pg_get_serial_sequence('detalle_vendedor_comision', 'id_detalle_vendedor_comision'), 1, false);")
            print("Secuencias de ID reseteadas (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('vendedor_comision', RESEED, 0);")
            cursor.execute("DBCC CHECKIDENT ('detalle_vendedor_comision', RESEED, 0);")
            print("Secuencias de ID reseteadas (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE vendedor_comision AUTO_INCREMENT = 1;")
            cursor.execute("ALTER TABLE detalle_vendedor_comision AUTO_INCREMENT = 1;")
            print("Secuencias de ID reseteadas (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def precargar_vendedores():
    """Precarga todos los vendedores en un diccionario usando values_list"""
    vendedores = {}
    for v in Vendedor.objects.values_list('id_vendedor', flat=True):
        vendedores[v] = Vendedor(id_vendedor=v)
    print(f"📦 Vendedores precargados: {len(vendedores)}")
    return vendedores

def precargar_marcas():
    """Precarga todas las marcas en un diccionario usando values_list"""
    marcas = {}
    for m in ProductoMarca.objects.values_list('id_producto_marca', flat=True):
        marcas[m] = ProductoMarca(id_producto_marca=m)
    print(f"📦 Marcas precargadas: {len(marcas)}")
    return marcas

def precargar_familias():
    """Precarga todas las familias en un diccionario usando values_list"""
    familias = {}
    for f in ProductoFamilia.objects.values_list('id_producto_familia', flat=True):
        familias[f] = ProductoFamilia(id_producto_familia=f)
    print(f"📦 Familias precargadas: {len(familias)}")
    return familias

def migrar_vendedor_comision():
    """Migra los vendedores únicos al modelo VendedorComision"""
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'vendedorcomision.DBF')
    table = DBF(dbf_path, encoding='latin-1')
    
    # Obtener vendedores únicos
    vendedores_unicos = {record['VENDEDOR'] for record in table}
    total_vendedores = len(vendedores_unicos)
    print(f"Total de vendedores únicos a procesar: {total_vendedores}")
    
    # Precargar vendedores
    vendedores_dict = precargar_vendedores()
    
    contador = 0
    registros_crear = []
    
    for vendedor_id in vendedores_unicos:
        # Verificar si existe el vendedor usando diccionario precargado
        vendedor = vendedores_dict.get(vendedor_id)
        
        if vendedor:
            registros_crear.append(
                VendedorComision(
                    id_vendedor_comision=vendedor_id,
                    id_vendedor=vendedor,
                    fecha_registro=date.today()
                )
            )
            contador += 1
        else:
            print(f"Vendedor con ID {vendedor_id} no encontrado. Omitiendo...")
    
    # Crear todos los registros en lote
    if registros_crear:
        VendedorComision.objects.bulk_create(registros_crear)
        print(f"Se migraron {contador} registros a VendedorComision")

def migrar_detalle_vendedor_comision():
    """Migra todos los registros al modelo DetalleVendedorComision"""
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'vendedorcomision.DBF')
    table = DBF(dbf_path, encoding='latin-1')
    
    total_registros = len(table)
    print(f"Total de registros a procesar en detalles: {total_registros}")
    
    # Precargar relaciones
    vendedores_comision_dict = {}
    for vc in VendedorComision.objects.values_list('id_vendedor_comision', flat=True):
        vendedores_comision_dict[vc] = VendedorComision(id_vendedor_comision=vc)
    
    marcas_dict = precargar_marcas()
    familias_dict = precargar_familias()
    
    contador_exitos = 0
    contador_omitidos = 0
    registros_crear = []
    contador_id = 1
    
    for idx, record in enumerate(table):
        vendedor_id = record['VENDEDOR']
        marca_id = record['MARCA']
        articulo_id = record['ARTICULO']
        comision = record['COMISION']
        
        # Buscar usando diccionarios precargados
        vendedor_comision = vendedores_comision_dict.get(vendedor_id)
        marca = marcas_dict.get(marca_id)
        familia = familias_dict.get(articulo_id)
        
        if not vendedor_comision:
            print(f"VendedorComision con ID {vendedor_id} no encontrado. Omitiendo...")
            contador_omitidos += 1
            continue
        
        if not marca:
            print(f"Marca con ID {marca_id} no encontrada. Omitiendo...")
            contador_omitidos += 1
            continue
        
        if not familia:
            print(f"Familia con ID {articulo_id} no encontrada. Omitiendo...")
            contador_omitidos += 1
            continue
        
        # Crear registro con ID manual
        registros_crear.append(
            DetalleVendedorComision(
                id_detalle_vendedor_comision=contador_id,
                id_vendedor_comision=vendedor_comision,
                id_marca=marca,
                id_familia=familia,
                comision_porcentaje=comision
            )
        )
        contador_id += 1
        contador_exitos += 1
        
        # Insertar en lotes
        if len(registros_crear) >= 500:
            DetalleVendedorComision.objects.bulk_create(registros_crear)
            registros_crear = []
            print(f"Procesados {contador_exitos} registros...")
    
    # Insertar registros restantes
    if registros_crear:
        DetalleVendedorComision.objects.bulk_create(registros_crear)
    
    print(f"\nResumen de migración:")
    print(f" - Registros exitosos: {contador_exitos}")
    print(f" - Registros omitidos: {contador_omitidos}")

if __name__ == '__main__':
    start_time = time.time()
    
    print("Iniciando migración de VendedorComision...")
    reset_vendedor_comision()
    migrar_vendedor_comision()
    
    print("\nIniciando migración de DetalleVendedorComision...")
    migrar_detalle_vendedor_comision()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    
    print(f"\nMigración completada en {int(minutes)} minutos y {int(seconds)} segundos")
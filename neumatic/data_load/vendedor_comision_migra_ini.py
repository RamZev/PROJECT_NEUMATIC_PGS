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

def reset_tablas():
    """Elimina los datos existentes en las tablas objetivo"""
    VendedorComision.objects.all().delete()
    DetalleVendedorComision.objects.all().delete()
    
    # Resetear secuencias en PostgreSQL (opcional)
    with connection.cursor() as cursor:
        pass
        #cursor.execute("ALTER SEQUENCE vendedor_comision_id_vendedor_comision_seq RESTART WITH 1;")
        #cursor.execute("ALTER SEQUENCE detalle_vendedor_comision_id_detalle_vendedor_comision_seq RESTART WITH 1;")

def migrar_vendedor_comision():
    """Migra los vendedores únicos al modelo VendedorComision"""
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'vendedorcomision.DBF')
    table = DBF(dbf_path, encoding='latin-1')
    
    # Obtener vendedores únicos
    vendedores_unicos = {record['VENDEDOR'] for record in table}
    total_vendedores = len(vendedores_unicos)
    print(f"Total de vendedores únicos a procesar: {total_vendedores}")
    
    contador = 0
    for vendedor_id in vendedores_unicos:
        try:
            # Verificar si existe el vendedor
            vendedor = Vendedor.objects.get(pk=vendedor_id)
            
            # Crear registro en VendedorComision
            VendedorComision.objects.create(
                id_vendedor_comision=vendedor_id,
                id_vendedor=vendedor,
                fecha_registro=date.today()
            )
            contador += 1
            
        except Vendedor.DoesNotExist:
            print(f"Vendedor con ID {vendedor_id} no encontrado en la base de datos. Omitiendo...")
    
    print(f"Se migraron {contador} registros a VendedorComision")

def migrar_detalle_vendedor_comision():
    """Migra todos los registros al modelo DetalleVendedorComision"""
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'vendedorcomision.DBF')
    table = DBF(dbf_path, encoding='latin-1')
    
    total_registros = len(table)
    print(f"Total de registros a procesar en detalles: {total_registros}")
    
    contador_exitos = 0
    contador_omitidos = 0
    
    for idx, record in enumerate(table):
        vendedor_id = record['VENDEDOR']
        marca_id = record['MARCA']
        articulo_id = record['ARTICULO']
        comision = record['COMISION']
        
        try:
            # Buscar el vendedor comision padre
            vendedor_comision = VendedorComision.objects.get(id_vendedor_comision=vendedor_id)
            
            # Buscar las relaciones
            marca = ProductoMarca.objects.get(id_producto_marca=marca_id)
            familia = ProductoFamilia.objects.get(id_producto_familia=articulo_id)
            
            # Crear el detalle
            DetalleVendedorComision.objects.create(
                id_vendedor_comision=vendedor_comision,
                id_marca=marca,
                id_familia=familia,
                comision_porcentaje=comision
            )
            contador_exitos += 1
            
        except VendedorComision.DoesNotExist:
            print(f"VendedorComision con ID {vendedor_id} no encontrado. Omitiendo registro...")
            contador_omitidos += 1
        except ProductoMarca.DoesNotExist:
            print(f"Marca con ID {marca_id} no encontrada para vendedor {vendedor_id}. Omitiendo registro...")
            contador_omitidos += 1
        except ProductoFamilia.DoesNotExist:
            print(f"Familia con ID {articulo_id} no encontrada para vendedor {vendedor_id}. Omitiendo registro...")
            contador_omitidos += 1
        
        # Mostrar progreso
        if (idx + 1) % 100 == 0:
            print(f"Procesados {idx + 1} registros...")
    
    print(f"\nResumen de migración:")
    print(f" - Registros exitosos: {contador_exitos}")
    print(f" - Registros omitidos: {contador_omitidos}")

if __name__ == '__main__':
    start_time = time.time()
    
    print("Iniciando migración de VendedorComision...")
    reset_tablas()
    migrar_vendedor_comision()
    
    print("\nIniciando migración de DetalleVendedorComision...")
    migrar_detalle_vendedor_comision()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    
    print(f"\nMigración completada en {int(minutes)} minutos y {int(seconds)} segundos")
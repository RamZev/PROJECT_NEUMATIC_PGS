# neumatic\data_load\cuenta_banco_migra.py
import json
import os
import sys
import django
from django.db import connection
from decimal import Decimal
from django.conf import settings

# Configuración del entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import CuentaBanco, Banco, Moneda

def reset_cuenta_banco():
    """Elimina los datos existentes en la tabla CuentaBanco y resetea su ID."""
    CuentaBanco.objects.all().delete()
    print("Tabla CuentaBanco limpiada.")
    
    # Detectar el motor de base de datos
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='cuenta_banco';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('cuenta_banco', 'id_cuenta_banco'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('cuenta_banco', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE cuenta_banco AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_cuentas_desde_json(ruta_json):
    """Carga las cuentas bancarias desde un archivo JSON."""
    
    # Precargar bancos usando values_list
    bancos_cache = {b[0]: b[0] for b in Banco.objects.values_list('id_banco')}
    print(f"Bancos precargados: {len(bancos_cache)}")
    
    # Precargar monedas usando values_list
    monedas_cache = {m[0]: m[0] for m in Moneda.objects.values_list('id_moneda')}
    print(f"Monedas precargadas: {len(monedas_cache)}")
    
    with open(ruta_json, 'r', encoding='utf-8') as file:
        cuentas = json.load(file)

    cuentas_creadas = 0
    errores = 0

    for item in cuentas:
        try:
            id_cuenta = item["id_cuenta_banco"]
            id_banco = item["id_banco_id"]
            id_moneda = item["id_moneda_id"]
            
            # Verificar si existen en el cache
            if id_banco not in bancos_cache:
                print(f"Advertencia: No existe banco con ID {id_banco}")
                errores += 1
                continue
                
            if id_moneda not in monedas_cache:
                print(f"Advertencia: No existe moneda con ID {id_moneda}")
                errores += 1
                continue

            # Crear instancias mínimas con solo el ID
            banco = Banco(id_banco=id_banco)
            moneda = Moneda(id_moneda=id_moneda)

            CuentaBanco.objects.create(
                id_cuenta_banco=id_cuenta,
                estatus_cuenta_banco=bool(item.get("estatus_cuenta_banco", True)),
                id_banco=banco,
                numero_cuenta=item["numero_cuenta"],
                tipo_cuenta=item["tipo_cuenta"],
                cbu=item["cbu"] if item["cbu"] else None,
                sucursal=item["sucursal"] if item["sucursal"] else None,
                codigo_postal=item["codigo_postal"] if item["codigo_postal"] else None,
                codigo_imputacion=item["codigo_imputacion"] if item["codigo_imputacion"] else None,
                tope_negociacion=Decimal(str(item.get("tope_negociacion", 0))),
                reporte_reques=item["reporte_reques"] if item["reporte_reques"] else None,
                id_moneda=moneda
            )
            cuentas_creadas += 1
            
        except Exception as e:
            print(f"Error creando cuenta: {str(e)}")
            errores += 1

    print(f"\nResumen:")
    print(f"Cuentas creadas: {cuentas_creadas}")
    print(f"Errores: {errores}")

if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'cuenta_banco.json')

    reset_cuenta_banco()
    cargar_cuentas_desde_json(ruta_json)
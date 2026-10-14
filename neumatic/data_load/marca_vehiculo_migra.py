# neumatic\data_load\marca_vehiculo_migra.py
import os
import sys
import json
import django
from django.db import connection
from django.conf import settings

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.vehiculo_models import MarcaVehiculo


def get_database_engine():
    """Detecta el motor de base de datos actual."""
    return settings.DATABASES['default']['ENGINE']


def reset_marca_vehiculo():
    """Elimina los datos existentes en la tabla MarcaVehiculo y resetea su ID."""
    MarcaVehiculo.objects.all().delete()
    print("Tabla MarcaVehiculo limpiada.")

    engine = get_database_engine()

    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='marca_vehiculo';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence('marca_vehiculo', "
                "'id_marca_vehiculo'), 1, false);"
            )
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('marca_vehiculo', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE marca_vehiculo AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")


def cargar_datos():
    """Lee marca_vehiculo.json, crea una MarcaVehiculo por cada entrada canónica.
    El id_marca_vehiculo se asigna secuencialmente desde 1 (enumerate).
    """
    reset_marca_vehiculo()

    json_path = os.path.join(BASE_DIR, 'data_load', 'marca_vehiculo.json')

    if not os.path.exists(json_path):
        print(f"❌ Error: No se encuentra el archivo {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        marcas_data = json.load(f)

    if not marcas_data:
        print("⚠️  El archivo JSON está vacío. No hay marcas para migrar.")
        return

    registros = []
    vistos = set()
    duplicados = 0

    for idx, item in enumerate(marcas_data, start=1):
        nombre = (item.get('marca_vehiculo') or "").strip().upper()

        if not nombre:
            print(f"⚠️  Entrada {idx}: marca_vehiculo vacía, se omite.")
            continue

        if nombre in vistos:
            duplicados += 1
            print(f"⚠️  Duplicado en JSON: '{nombre}' (entrada {idx}), se omite.")
            continue

        vistos.add(nombre)

        registros.append(
            MarcaVehiculo(
                id_marca_vehiculo=idx,
                estatus_marca_vehiculo=True,
                marca_vehiculo=nombre,
            )
        )

    if registros:
        MarcaVehiculo.objects.bulk_create(registros)

    print(f"✅ Se han migrado {len(registros)} marcas de forma exitosa.")
    if duplicados:
        print(f"   Duplicados salteados: {duplicados}")


def verificar_conexion():
    """Verifica que la conexión a la base de datos funciona."""
    try:
        with connection.cursor() as cursor:
            engine = get_database_engine()
            print(f"📋 Motor de base de datos: {engine}")

            if 'sqlite' in engine:
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()[0]
                print(f"✅ SQLite version: {version}")
            elif 'mssql' in engine or 'sql_server' in engine:
                cursor.execute("SELECT @@VERSION")
                version = cursor.fetchone()[0][:80]
                print(f"✅ SQL Server version: {version}...")
            elif 'postgresql' in engine:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0][:80]
                print(f"✅ PostgreSQL version: {version}...")
            elif 'mysql' in engine:
                cursor.execute("SELECT VERSION();")
                version = cursor.fetchone()[0]
                print(f"✅ MySQL version: {version}")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("MIGRACIÓN DE DATOS - MARCA VEHÍCULO")
    print("=" * 60)

    if verificar_conexion():
        cargar_datos()
        print("\n" + "=" * 60)
        print("✅ Migración de Marca Vehículo completada.")
        print("=" * 60)
    else:
        print("\n❌ No se pudo establecer conexión con la base de datos.")
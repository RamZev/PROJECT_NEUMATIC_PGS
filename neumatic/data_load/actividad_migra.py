# neumatic\data_load\actividad_migra.py
import os
import sys
import django
from dbfread import DBF
from django.db import connection
from django.conf import settings

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import Actividad

def get_database_engine():
    """Detecta el motor de base de datos actual"""
    return settings.DATABASES['default']['ENGINE']

def reset_actividad():
    """Elimina los datos existentes en la tabla Actividad y resetea su ID."""
    Actividad.objects.all().delete()
    print("Tabla Actividad limpiada.")
    
    engine = get_database_engine()
    
    # Reiniciar el autoincremento según el motor de base de datos
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            # SQLite: reiniciar secuencia
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='actividad';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            # PostgreSQL: reiniciar secuencia (usando el nombre correcto)
            cursor.execute("ALTER SEQUENCE actividad_id_actividad_seq RESTART WITH 1;")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            # SQL Server: reiniciar identity
            cursor.execute("DBCC CHECKIDENT ('actividad', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            # MySQL: reiniciar autoincremento
            cursor.execute("ALTER TABLE actividad AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_datos():
    """Lee los datos de la tabla actividad.DBF, verifica consecutividad de códigos,
    migra los registros al modelo Actividad y añade pendientes si hay saltos en los códigos."""
    reset_actividad()
    
    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'actividad.DBF')
    
    if not os.path.exists(dbf_path):
        print(f"❌ Error: No se encuentra el archivo {dbf_path}")
        return
    
    # Abrir la tabla de Visual FoxPro y ordenarla por CODIGO
    table = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda r: r['CODIGO'])
    
    expected_codigo = 1
    registros_creados = 0
    registros_pendientes = []
    
    for record in table:
        codigo = record['CODIGO']
        nombre = record['NOMBRE'].strip() if record['NOMBRE'] else ""
        
        # Verificar si el código es consecutivo
        while expected_codigo < codigo:
            # Guardar pendiente para crear después (mejor rendimiento)
            registros_pendientes.append(
                Actividad(
                    estatus_actividad=True,
                    descripcion_actividad="PENDIENTE DE ELIMINACIÓN"
                )
            )
            print(f"Registro pendiente para código faltante: {expected_codigo}")
            expected_codigo += 1
        
        # Crear el registro actual
        registros_pendientes.append(
            Actividad(
                estatus_actividad=True,
                descripcion_actividad=nombre
            )
        )
        registros_creados += 1
        expected_codigo += 1
    
    # Crear todos los registros en lote (más eficiente)
    if registros_pendientes:
        Actividad.objects.bulk_create(registros_pendientes)
    
    # Eliminar registros pendientes
    eliminados = Actividad.objects.filter(descripcion_actividad="PENDIENTE DE ELIMINACIÓN").delete()
    
    print(f"✅ Se han migrado {registros_creados} registros de Actividad de forma exitosa.")
    print(f"   Registros pendientes eliminados: {eliminados[0]}")

def verificar_conexion():
    """Verifica que la conexión a la base de datos funciona"""
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
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("MIGRACIÓN DE DATOS - ACTIVIDAD")
    print("=" * 60)
    
    if verificar_conexion():
        cargar_datos()
        print("\n" + "=" * 60)
        print("✅ Migración de Actividad completada.")
        print("=" * 60)
    else:
        print("\n❌ No se pudo establecer conexión con la base de datos.")
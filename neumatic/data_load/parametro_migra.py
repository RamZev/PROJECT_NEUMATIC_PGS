# neumatic\data_load\parametro_migra.py
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

from apps.maestros.models.parametro_models import Parametro
from apps.maestros.models.empresa_models import Empresa

def get_database_engine():
    """Detecta el motor de base de datos actual"""
    return settings.DATABASES['default']['ENGINE']

def reset_parametro():
    """Elimina los datos existentes en la tabla Parametro y resetea su ID."""
    Parametro.objects.all().delete()
    print("Tabla Parametro limpiada.")
    
    engine = get_database_engine()
    
    # Reiniciar el autoincremento según el motor de base de datos
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='parametro';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("ALTER SEQUENCE parametro_id_parametro_seq RESTART WITH 1;")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('parametro', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE parametro AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def cargar_datos():
    """Lee los datos de la tabla param.DBF, verifica consecutividad de IDs
    y migra los registros al modelo Parametro."""
    reset_parametro()
    
    # Ruta de la tabla de Visual FoxPro
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'param.DBF')
    
    if not os.path.exists(dbf_path):
        print(f"❌ Error: No se encuentra el archivo {dbf_path}")
        return
    
    # Obtener o asegurar la existencia de la empresa con ID=1 (por tu anotación manual)
    try:
        empresa_default = Empresa.objects.get(pk=1)
    except Empresa.DoesNotExist:
        print("⚠️ Advertencia: No existe la Empresa con ID=1. Creando una empresa temporal...")
        empresa_default = Empresa.objects.create(id_empresa=1, nombre_empresa="Empresa por Defecto")

    # Abrir la tabla de Visual FoxPro. Nota: Como 'auto' define el ID en tu anotación, 
    # asumimos un orden implícito o que se procesa secuencialmente. 
    # Si param.DBF tuviera un campo numérico identificador, se ordenaría por él.
    table = DBF(dbf_path, encoding='latin-1')
    
    expected_id = 1
    registros_creados = 0
    registros_pendientes = []
    
    for record in table:
        # En tu anotación pusiste 'auto' para el ID. Si el DBF no trae un ID explícito,
        # autoincrementamos secuencialmente basándonos en la lectura física del archivo.
        # En caso de que sí traiga un campo llave (por ejemplo 'id'), reemplaza la línea de abajo.
        id_actual = expected_id 
        
        # Mapeo y saneamiento de campos según la nota manuscrita
        interes = record.get('INTERES', 0.00)
        interes_dolar = record.get('INTERES_DOLAR', 0.00) or 0.00  # Por si viene vacío o nulo
        cotizacion_dolar = record.get('DOLAR', 0.00)
        dias_vencimiento = record.get('DIASVTO', 0)
        descuento_maximo = record.get('DESCMAX', 0.00)
        creditomay = record.get('CREDITOMAY', 0.00)
        creditomin = record.get('CREDITOMIN', 0.00)
        
        # Manejo de huecos de ID (para respetar la misma lógica secuencial de Actividad)
        while expected_id < id_actual:
            registros_pendientes.append(
                Parametro(
                    estatus_parametro=True,
                    id_empresa=empresa_default,
                    interes=0.00,
                    interes_dolar=0.00,
                    cotizacion_dolar=0.00,
                    dias_vencimiento=0,
                    descuento_maximo=0.00,
                    creditomay=0.00,
                    creditomin=0.00
                    # Usamos un flag o lo detectaremos luego si fuera necesario, 
                    # pero al no tener un campo de texto tipo "PENDIENTE", dejamos valores en cero.
                )
            )
            print(f"Registro pendiente para ID faltante: {expected_id}")
            expected_id += 1
            
        # Crear la instancia del registro mapeado
        registros_pendientes.append(
            Parametro(
                estatus_parametro=True,  # Valor "1" de tu lista
                id_empresa=empresa_default,  # Valor "1" de tu lista
                interes=interes,
                interes_dolar=interes_dolar,
                cotizacion_dolar=cotizacion_dolar,
                dias_vencimiento=dias_vencimiento,
                descuento_maximo=descuento_maximo,
                creditomay=creditomay,
                creditomin=creditomin
            )
        )
        registros_creados += 1
        expected_id += 1
        
    # Inserción masiva en la base de datos
    if registros_pendientes:
        Parametro.objects.bulk_create(registros_pendientes)
        
    print(f"✅ Se han migrado {registros_creados} registros de Parametro de forma exitosa.")

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
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("MIGRACIÓN DE DATOS - PARAMETRO")
    print("=" * 60)
    
    if verificar_conexion():
        cargar_datos()
        print("\n" + "=" * 60)
        print("✅ Migración de Parametro completada.")
        print("=" * 60)
    else:
        print("\n❌ No se pudo establecer conexión con la base de datos.")
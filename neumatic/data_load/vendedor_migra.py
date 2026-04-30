# neumatic\data_load\vendedor_migra.py
import os
import sys
import django
import time
from dbfread import DBF
from django.db import connection
from datetime import date

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

# Importación de los modelos
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.vendedor_models import Vendedor

def reset_vendedor():
    """Elimina los datos existentes en la tabla Vendedor y resetea su ID."""
    Vendedor.objects.all().delete()
    print("Tabla Vendedor limpiada.")
    
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='vendedor';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('vendedor', 'id_vendedor'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('vendedor', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE vendedor AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def precargar_sucursales():
    """Precarga todas las sucursales en un diccionario usando values_list (evita el bug)"""
    sucursales = {}
    for s in Sucursal.objects.values_list('id_sucursal', flat=True):
        sucursales[s] = Sucursal(id_sucursal=s)
    print(f"📦 Sucursales precargadas: {len(sucursales)}")
    return sucursales

# Resetear tabla
reset_vendedor()

# Precargar sucursales
sucursales_dict = precargar_sucursales()

tabla_origen = 'vendedor.DBF'

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', tabla_origen)

# Abrir la tabla de Visual FoxPro usando dbfread
table = DBF(dbf_path, encoding='latin-1')

# Rango de registros 
codigo_inicio = 1
codigo_final = None

# Nombre de variable id en la tabla origen
codigo_id = "CODIGO"

# Filtrar y ordenar la tabla DBF
table = sorted(
    [
        record
        for record in table
        if int(record.get(codigo_id, 0)) >= codigo_inicio and 
           (codigo_final is None or int(record.get(codigo_id, 0)) <= codigo_final)
    ],
    key=lambda record: int(record.get(codigo_id, 0))
)

total_registros = len(table)
print(f"Total de registros a procesar: {total_registros}")

# Contador para IDs manuales (por si acaso)
contador_id = 1
registros_creados = 0
errores = 0

# Procesar registros
for idx, record in enumerate(table, 1):
    id_origen = int(record.get(codigo_id, 0))
    print(f"Procesando vendedor con ID: {id_origen}")

    # Validar sucursal usando diccionario precargado
    pk_sucursal = int(record.get('SUCURSAL', 0))
    id_sucursal_instancia = sucursales_dict.get(pk_sucursal)
    
    if not id_sucursal_instancia:
        print(f"Sucursal con ID {pk_sucursal} no encontrada. Saltando registro.")
        errores += 1
        continue

    # Crear registro con ID manual
    try:
        Vendedor.objects.create(
            id_vendedor=id_origen,
            estatus_vendedor=True,
            nombre_vendedor=record.get('NOMBRE', '').strip() or "Sin nombre",
            domicilio_vendedor=record.get('DOMICILIO', '').strip() or "",
            email_vendedor="sin-email@dominio.com",
            telefono_vendedor="sin-telefono",
            pje_auto=float(record.get('PORCENTAJE') or 0),
            pje_camion=float(record.get('PJECAMION') or 0),
            vence_factura=int(record.get('DIASGRACIA', 0)),
            vence_remito=int(record.get('DIASRTOS', 0)),
            id_sucursal=id_sucursal_instancia,
            tipo_venta=record.get('TIPO', '').strip() or "",
            col_descuento=float(record.get('DESCOL') or 0),
            email_venta=bool(record.get('EMAILFAC', False)),
            info_saldo=bool(record.get('EMAILSDO', False)),
            info_estadistica=bool(record.get('EMAILEST', False)),
        )
        registros_creados += 1
        print(f"Vendedor con ID {id_origen} creado exitosamente.")
    except Exception as e:
        print(f"Error al crear vendedor con ID {id_origen}: {e}")
        errores += 1
        continue

print("\n📝 Resumen de migración:")
print(f"✅ Vendedores creados: {registros_creados}")
print(f"❌ Errores: {errores}")
print("La migración terminó con éxito!")
import os
import sys
import django
import json
from datetime import datetime

# Configurar Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import Provincia, Localidad
from apps.maestros.models.sucursal_models import Sucursal
from django.db import connection
from django.conf import settings

# Ruta del archivo JSON
json_path = 'D:/NEUMATIC_BAK/json_01/sucursal.json'

def reset_sucursal():
    """Elimina los datos existentes en la tabla Sucursal y resetea su ID."""
    Sucursal.objects.all().delete()
    print("✅ Tabla Sucursal limpiada.")
    
    engine = settings.DATABASES['default']['ENGINE']
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='sucursal';")
            print("✅ Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('sucursal', 'id_sucursal'), 1, false);")
            print("✅ Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('sucursal', RESEED, 0);")
            print("✅ Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE sucursal AUTO_INCREMENT = 1;")
            print("✅ Secuencia de ID reseteada (MySQL).")
        else:
            print(f"⚠️ Motor {engine} no requiere reset manual de secuencia.")

# Resetear la tabla antes de cargar
reset_sucursal()

# ==========================================
# CAMBIO PRINCIPAL: Leer el JSON como Array
# ==========================================
print(f"\n📂 Leyendo archivo: {json_path}")
with open(json_path, 'r', encoding='utf-8') as f:
    try:
        data_list = json.load(f)  # Carga todo el archivo como una lista de Python
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar el archivo JSON: {e}")
        sys.exit(1)

if not isinstance(data_list, list):
    print("❌ El archivo JSON no contiene una lista de registros.")
    sys.exit(1)

total_registros = len(data_list)
print(f"📊 Total de registros encontrados: {total_registros}\n")

# Contadores para estadísticas
creados = 0
omitidos = 0

# Procesar cada registro (ahora 'data' ya es un diccionario individual)
for idx, data in enumerate(data_list, start=1):
    
    # Extraer datos del JSON
    id_sucursal = data.get('id_sucursal')
    if id_sucursal is None:
        print(f"⚠️ Registro {idx}: falta 'id_sucursal', se omite.")
        omitidos += 1
        continue

    # Campos obligatorios (con valores por defecto si faltan)
    nombre_sucursal = data.get('nombre_sucursal', '').strip()
    codigo_michelin = data.get('codigo_michelin', 0)
    domicilio_sucursal = data.get('domicilio_sucursal', '').strip()
    codigo_postal = data.get('codigo_postal', '').strip()
    telefono_sucursal = data.get('telefono_sucursal', '').strip()
    email_sucursal = data.get('email_sucursal', '').strip()
    estatus_sucursal = data.get('estatus_sucursal', True)

    # Fecha de inicio de actividad
    inicio_actividad_str = data.get('inicio_actividad')
    if inicio_actividad_str:
        try:
            # Acepta formato ISO completo o solo fecha
            if 'T' in inicio_actividad_str:
                inicio_actividad = datetime.fromisoformat(inicio_actividad_str).date()
            else:
                inicio_actividad = datetime.strptime(inicio_actividad_str, '%Y-%m-%d').date()
        except ValueError:
            print(f"⚠️ Registro {idx}: formato de fecha inválido: {inicio_actividad_str}, se omite.")
            inicio_actividad = None
    else:
        inicio_actividad = None

    # Claves foráneas: provincia y localidad
    id_provincia = data.get('id_provincia_id')
    id_localidad = data.get('id_localidad_id')

    if id_provincia is None or id_localidad is None:
        print(f"⚠️ Registro {idx}: falta id_provincia_id o id_localidad_id, se omite.")
        omitidos += 1
        continue

    # Obtener objetos Provincia y Localidad
    try:
        provincia_obj = Provincia.objects.get(pk=id_provincia)
    except Provincia.DoesNotExist:
        print(f"❌ Registro {idx}: Provincia con id {id_provincia} no existe, se omite.")
        omitidos += 1
        continue

    try:
        localidad_obj = Localidad.objects.get(pk=id_localidad)
    except Localidad.DoesNotExist:
        print(f"❌ Registro {idx}: Localidad con id {id_localidad} no existe, se omite.")
        omitidos += 1
        continue

    # Crear el objeto Sucursal
    try:
        sucursal = Sucursal(
            id_sucursal=id_sucursal,
            estatus_sucursal=estatus_sucursal,
            nombre_sucursal=nombre_sucursal,
            codigo_michelin=codigo_michelin,
            domicilio_sucursal=domicilio_sucursal,
            codigo_postal=codigo_postal,
            telefono_sucursal=telefono_sucursal,
            email_sucursal=email_sucursal,
            inicio_actividad=inicio_actividad,
            id_provincia=provincia_obj,
            id_localidad=localidad_obj,
        )
        sucursal.save()
        creados += 1
        print(f"✅ Registro {idx}: Sucursal {id_sucursal} - {nombre_sucursal} creada.")
    except Exception as e:
        print(f"❌ Registro {idx}: Error al guardar Sucursal {id_sucursal}: {e}")
        omitidos += 1

# Resumen final
print("\n" + "="*50)
print(f"📊 PROCESO COMPLETADO")
print(f"   ✅ Registros creados: {creados}")
print(f"   ⚠️ Registros omitidos: {omitidos}")
print(f"   📦 Total procesados: {total_registros}")
print("="*50)
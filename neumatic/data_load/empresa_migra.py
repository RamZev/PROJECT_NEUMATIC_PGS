# neumatic\data_load\empresa_migra.py
import json
import os
import sys
import django
from django.db import connection
from django.conf import settings
from datetime import datetime

# Añadir el directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.empresa_models import Empresa
from apps.maestros.models.base_models import Localidad, Provincia, TipoIva

def reset_empresa():
    """Elimina los datos existentes en la tabla Empresa y resetea su ID."""
    Empresa.objects.all().delete()
    print("Tabla Empresa limpiada.")

    # Detectar el motor de base de datos
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='empresa';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('empresa', 'id_empresa'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('empresa', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE empresa AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

def parse_date(valor):
    """Convierte string a fecha o retorna None si es vacío o nulo."""
    if not valor:
        return None
    return datetime.strptime(valor, "%Y-%m-%d").date()

def parse_datetime(valor):
    """Convierte string a datetime o retorna None si es vacío o nulo."""
    if not valor:
        return None
    # Intentar con formato con microsegundos
    try:
        return datetime.strptime(valor, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        # Intentar con formato sin microsegundos
        return datetime.strptime(valor, "%Y-%m-%d %H:%M:%S")

def cargar_empresa_desde_json(ruta_json):
    """Carga los datos del archivo JSON e inserta los registros en la tabla Empresa."""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        try:
            Empresa.objects.create(
                id_empresa=item["id_empresa"],
                estatus_empresa=bool(item["estatus_empresa"]),
                nombre_fiscal=item["nombre_fiscal"],
                nombre_comercial=item["nombre_comercial"],
                domicilio_empresa=item["domicilio_empresa"],
                codigo_postal=item["codigo_postal"],
                cuit=item["cuit"],
                ingresos_bruto=item["ingresos_bruto"],
                inicio_actividad=parse_date(item["inicio_actividad"]),
                cbu=item["cbu"],
                cbu_alias=item["cbu_alias"],
                cbu_vence=parse_date(item["cbu_vence"]),
                telefono=item["telefono"],
                email_empresa=item["email_empresa"],
                web_empresa=item.get("web_empresa", ""),
                logo_empresa=item.get("logo_empresa"),
                ws_archivo_crt2=item.get("ws_archivo_crt2"),
                ws_archivo_key2=item.get("ws_archivo_key2"),
                ws_vence_h=parse_datetime(item.get("ws_vence_h")),
                ws_archivo_crt_p=item.get("ws_archivo_crt_p"),
                ws_archivo_key_p=item.get("ws_archivo_key_p"),
                ws_vence_p=parse_datetime(item.get("ws_vence_p")),
                ws_token_h=item.get("ws_token_h"),
                ws_sign_h=item.get("ws_sign_h"),
                ws_expiracion_h=parse_datetime(item.get("ws_expiracion_h")),
                ws_token_p=item.get("ws_token_p"),
                ws_sign_p=item.get("ws_sign_p"),
                ws_expiracion_p=parse_datetime(item.get("ws_expiracion_p")),
                ws_modo=item["ws_modo"],
                interes=item["interes"],
                interes_dolar=item["interes_dolar"],
                cotizacion_dolar=item["cotizacion_dolar"],
                dias_vencimiento=item["dias_vencimiento"],
                descuento_maximo=item["descuento_maximo"],
                id_localidad=Localidad.objects.get(pk=item["id_localidad_id"]),
                id_provincia=Provincia.objects.get(pk=item["id_provincia_id"]),
                id_iva=TipoIva.objects.get(pk=item["id_iva_id"]) if item.get("id_iva_id") else None,
            )
        except Exception as e:
            print(f"Error al cargar empresa ID {item['id_empresa']}: {e}")

    print(f"Se han migrado {len(data)} empresas con IDs explícitos.")

if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'empresa.json')

    reset_empresa()
    cargar_empresa_desde_json(ruta_json)
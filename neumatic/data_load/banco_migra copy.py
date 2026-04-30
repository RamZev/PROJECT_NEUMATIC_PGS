# neumatic\data_load\banco_migra.py
import json
import os
import sys
import django
from django.db import connection

# Configuración del entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import Banco  # Asegúrate de que esta es la ruta correcta

def reset_banco():
    """Elimina los datos existentes en la tabla Banco y resetea su ID en SQLite."""
    Banco.objects.all().delete()
    print("Tabla Banco limpiada.")

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='banco';")
    
    print("Secuencia de ID reseteada.")

def cargar_bancos_desde_json(ruta_json):
    """Carga los bancos desde un archivo JSON y los guarda en la base de datos."""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        bancos = json.load(file)

    for item in bancos:
        Banco.objects.create(
            codigo_banco=int(item["codigo_banco"]),
            nombre_banco=item["nombre_banco"],
            cuit_banco=int(item["cuit_banco"]),
            estatus_banco=True  # Valor por defecto True como solicitaste
        )

    print(f"Se han migrado {len(bancos)} bancos.")

if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'banco.json')

    reset_banco()
    cargar_bancos_desde_json(ruta_json)
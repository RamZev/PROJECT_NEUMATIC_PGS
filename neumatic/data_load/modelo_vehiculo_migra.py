# neumatic\data_load\modelo_vehiculo_migra.py
import json
import os
import sys
import django

# Configuración del entorno Django (mismo patrón que moneda_migra.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from django.db import transaction
from apps.maestros.models.vehiculo_models import MarcaVehiculo, ModeloVehiculo


def cargar_modelos(ruta_json):
    with open(ruta_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    creados = 0
    existentes = 0
    errores = 0

    with transaction.atomic():
        for item in data:
            id_marca = item['id_marca_vehiculo']
            modelos = item.get('modelos', [])

            try:
                marca = MarcaVehiculo.objects.get(id_marca_vehiculo=id_marca)
            except MarcaVehiculo.DoesNotExist:
                print(f"⚠️  Marca con id {id_marca} no existe. Se omite.")
                errores += 1
                continue

            for nombre_modelo in modelos:
                nombre_modelo = (nombre_modelo or '').strip()
                if not nombre_modelo:
                    continue

                obj, created = ModeloVehiculo.objects.get_or_create(
                    id_marca_vehiculo=marca,
                    modelo_vehiculo=nombre_modelo,
                    defaults={'estatus_modelo_vehiculo': True},
                )
                if created:
                    creados += 1
                else:
                    existentes += 1

    print("✅ Proceso finalizado:")
    print(f"   Modelos creados: {creados}")
    print(f"   Modelos ya existentes: {existentes}")
    print(f"   Errores (marcas faltantes): {errores}")


if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'modelo_vehiculo.json')
    cargar_modelos(ruta_json)
# neumatic\data_load\comprobante_compra_migra.py
import json
import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from django.db import connection
from django.core.exceptions import ValidationError
from django.conf import settings
from apps.maestros.models.base_models import ComprobanteCompra


def limpiar_tabla():
    """Elimina todos los registros de la tabla ComprobanteCompra."""
    ComprobanteCompra.objects.all().delete()
    print("Tabla ComprobanteCompra limpiada.")


def actualizar_secuencia_postgres(max_id):
    """Actualiza la secuencia de PostgreSQL al valor máximo + 1."""
    engine = settings.DATABASES['default']['ENGINE']
    if 'postgresql' in engine:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence('comprobante_compra', 'id_comprobante_compra'), %s, true);",
                [max_id + 1]
            )
            print(f"Secuencia de PostgreSQL actualizada al valor {max_id + 1}.")
    else:
        print("No es PostgreSQL, no se actualiza secuencia.")


def cargar_comprobantes_desde_json(ruta_json):
    """
    Carga los comprobantes de compra respetando los IDs originales del JSON.
    - usuario: toma del JSON, si es null → 'admin'
    - estacion: toma del JSON, si es null → 'ESTACION03'
    - id_user_id: toma del JSON, si es null → 1
    - id_user_update_id: igual que id_user_id
    """
    with open(ruta_json, 'r', encoding='utf-8') as file:
        comprobantes = json.load(file)

    creados = 0
    max_id = 0

    for item in comprobantes:
        try:
            usuario_val = item.get("usuario") or "admin"
            estacion_val = item.get("estacion") or "ESTACION03"
            id_user = item.get("id_user_id") or 1
            id_user_update = item.get("id_user_update_id") or 1

            ComprobanteCompra.objects.create(
                id_comprobante_compra=item.get("id_comprobante_compra"),  # ← ID original
                usuario=usuario_val,
                estacion=estacion_val,
                fcontrol=item.get("fcontrol"),
                fcontrol2=item.get("fcontrol2"),
                estatus_comprobante_compra=bool(item.get("estatus_comprobante_compra", True)),
                codigo_comprobante_compra=item.get("codigo_comprobante_compra", ""),
                nombre_comprobante_compra=item.get("nombre_comprobante_compra", ""),
                nombre_impresion=item.get("nombre_impresion", ""),
                mult_compra=int(item.get("mult_compra", 0)),
                mult_saldo=int(item.get("mult_saldo", 0)),
                mult_stock=int(item.get("mult_stock", 0)),
                mult_caja=int(item.get("mult_caja", 0)),
                libro_iva=bool(item.get("libro_iva", False)),
                codigo_afip_a=item.get("codigo_afip_a", ""),
                codigo_afip_b=item.get("codigo_afip_b", ""),
                codigo_afip_c=item.get("codigo_afip_c", ""),
                codigo_afip_m=item.get("codigo_afip_m", ""),
                remito=bool(item.get("remito", False)),
                retencion=bool(item.get("retencion", False)),
                id_user_id=id_user,
                id_user_update_id=id_user_update,
            )
            creados += 1
            id_actual = item.get("id_comprobante_compra", 0)
            if id_actual > max_id:
                max_id = id_actual

        except ValidationError as e:
            print(f"Error validando comprobante {item.get('nombre_comprobante_compra', 'Desconocido')}: {e}")
        except Exception as e:
            print(f"Error creando comprobante {item.get('nombre_comprobante_compra', 'Desconocido')}: {e}")

    print(f"✅ Se han migrado {creados} comprobantes de compra.")
    return max_id


if __name__ == '__main__':
    ruta_json = os.path.join(BASE_DIR, 'data_load', 'comprobante_compra.json')
    limpiar_tabla()
    max_id_insertado = cargar_comprobantes_desde_json(ruta_json)
    actualizar_secuencia_postgres(max_id_insertado)
    print("🎯 Migración completada.")
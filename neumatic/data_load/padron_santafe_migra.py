# neumatic/data_load/padron_santafe_migra.py
import os
import sys
import csv
from decimal import Decimal
from datetime import datetime
import time
import django
from django.db import connection
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.padron_models import PadronSantaFeIIBB

# Tamaño del lote
LOTE = 10000

def reset_tabla():
    PadronSantaFeIIBB.objects.all().delete()
    print("Tabla padron_santa_fe limpiada.")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval(pg_get_serial_sequence('padron_santa_fe', 'id_padron'), 1, false);")
            print("Secuencia reseteada (PostgreSQL).")
    except Exception as e:
        print(f"No se pudo resetear secuencia: {e}")

def parse_fecha(fecha_str):
    fecha_str = fecha_str.strip().zfill(8)
    return datetime.strptime(fecha_str, '%d%m%Y').date()

def parse_decimal(valor_str):
    if not valor_str:
        return Decimal('0.00')
    valor_str = valor_str.replace(',', '.')
    return Decimal(valor_str)

def cargar_datos():
    inicio = time.time()
    reset_tabla()
    
    archivo = os.path.join(BASE_DIR, 'data_load', 'padron', 'PARP_202609.csv')
    if not os.path.exists(archivo):
        print(f"Archivo no encontrado: {archivo}")
        return

    lote = []
    total_procesados = 0
    total_creados = 0
    errores = 0

    with open(archivo, 'r', encoding='latin-1') as f:
        reader = csv.reader(f, delimiter=';')
        # ⚠️ NO saltar encabezado (Santa Fe no tiene)

        for row in reader:
            if len(row) < 12:
                errores += 1
                continue
            try:
                fecha_publicacion = parse_fecha(row[0])
                fecha_vigencia_desde = parse_fecha(row[1])
                fecha_vigencia_hasta = parse_fecha(row[2])
                cuit = int(row[3].strip())
                tipo_contr = row[4].strip()
                if tipo_contr not in ('D', 'C'):
                    tipo_contr = None
                marca_alta = row[5].strip().upper() == 'S'
                marca_alicuota = row[6].strip().upper() == 'S'
                alicuota_percepcion = parse_decimal(row[7])
                alicuota_retencion = parse_decimal(row[8])
                nro_grupo_percepcion = row[9].strip() or '0'
                nro_grupo_retencion = row[10].strip() or '0'
                razon_social = row[11].strip()[:100]

                lote.append(
                    PadronSantaFeIIBB(
                        fecha_publicacion=fecha_publicacion,
                        fecha_vigencia_desde=fecha_vigencia_desde,
                        fecha_vigencia_hasta=fecha_vigencia_hasta,
                        cuit=cuit,
                        tipo_contr_insc=tipo_contr,
                        marca_alta_sujeto=marca_alta,
                        marca_alicuota=marca_alicuota,
                        alicuota_percepcion=alicuota_percepcion,
                        alicuota_retencion=alicuota_retencion,
                        nro_grupo_percepcion=nro_grupo_percepcion,
                        nro_grupo_retencion=nro_grupo_retencion,
                        razon_social=razon_social
                    )
                )
                total_procesados += 1
            except Exception as e:
                errores += 1
                print(f"Error en fila {row}: {e}")
                continue

            # Cuando el lote alcanza el tamaño definido, se guarda
            if len(lote) >= LOTE:
                PadronSantaFeIIBB.objects.bulk_create(lote)
                total_creados += len(lote)
                print(f"Procesados {total_procesados} registros (creados {total_creados})...")
                lote = []

        # Guardar el último lote (si quedan registros)
        if lote:
            PadronSantaFeIIBB.objects.bulk_create(lote)
            total_creados += len(lote)

    fin = time.time()
    print("\n" + "="*60)
    print(f"RESUMEN DE CARGA")
    print(f"Total procesados: {total_procesados}")
    print(f"Total creados: {total_creados}")
    print(f"Errores: {errores}")
    print(f"Tiempo total: {fin - inicio:.2f} segundos")
    print("="*60)
    print("Migración de Padrón Santa Fe completada exitosamente.")

if __name__ == '__main__':
    cargar_datos()
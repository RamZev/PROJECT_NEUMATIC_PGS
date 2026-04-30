# neumatic\data_load\retencion_recibo_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from decimal import Decimal

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

# Modelos
from apps.ventas.models.factura_models import Factura
from apps.ventas.models.caja_models import Caja
from apps.ventas.models.recibo_models import RetencionRecibo
from apps.maestros.models.base_models import CodigoRetencion  # ✅ AHORA ES CodigoRetencion

# Logging
logging.basicConfig(
    filename='retencion_recibo_migra.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def safe_int(value, default=0):
    """Conversión segura a entero"""
    try:
        return int(float(value)) if value is not None and str(value).strip() else default
    except (ValueError, TypeError):
        return default

def safe_decimal(value, default=0.0):
    """Conversión segura a Decimal"""
    try:
        if value is not None and str(value).strip():
            return Decimal(str(value))
        return Decimal(str(default))
    except (ValueError, TypeError):
        return Decimal(str(default))

def retencion_recibo_migra():
    """Migración desde mediopagos.DBF a RetencionRecibo usando CodigoRetencion(pk=5)"""
    try:
        start_time = time.time()
        print("<info>Iniciando migración desde mediopagos.DBF...</info>")

        # === 1. Instanciar CodigoRetencion con pk = 5 ===
        try:
            codigo_retencion_5 = CodigoRetencion.objects.get(pk=5)
            print(f"<success>CodigoRetencion ID=5 cargado: {getattr(codigo_retencion_5, 'descripcion', 'Sin descripción')}</success>")
        except ObjectDoesNotExist:
            print("<error>ERROR: No existe CodigoRetencion con ID = 5. Abortando.</error>")
            return

        # === 2. Cargar caché de Cajas por numero_caja ===
        cajas_cache = {caja.numero_caja: caja for caja in Caja.objects.all() if caja.numero_caja}
        print(f"<info>Cargadas {len(cajas_cache)} cajas</info>")

        # === 3. Leer archivo mediopagos.DBF ===
        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'mediopagos.DBF')
        table = DBF(dbf_path, encoding='latin-1')
        total_records = len(table)
        print(f"<info>Total registros en mediopagos.DBF: {total_records}</info>")

        # === 4. Filtrar: IDVENTA > 0 AND FORMAPAGO = 8 ===
        registros_filtrados = []
        for idx, record in enumerate(table, 1):
            idventa = safe_int(record.get('IDVENTA'))
            formapago = safe_int(record.get('FORMAPAGO'))
            if idventa > 0 and formapago == 8:
                registros_filtrados.append((idx, record))
        
        total_filtrados = len(registros_filtrados)
        print(f"<success>Registros filtrados (IDVENTA > 0 y FORMAPAGO = 8): {total_filtrados}</success>")
        if total_filtrados == 0:
            return

        # === 5. Archivo .tag para facturas no encontradas ===
        tag_file = os.path.join(BASE_DIR, 'data_load', 'retencion_recibo_migra.log')
        with open(tag_file, 'w', encoding='utf-8') as f:
            f.write("id_caja_detalle\tidventa\tid_caja\n")

        # === 6. Procesamiento ===
        batch_size = 2000
        retenciones_batch = []
        facturas_a_actualizar = []

        creados = 0
        actualizados_caja = 0
        no_encontrados = 0
        errores = 0

        for idx_dbf, record in registros_filtrados:
            try:
                caja_numero = safe_int(record.get('CAJA'))
                idventa = safe_int(record.get('IDVENTA'))
                importe = safe_decimal(record.get('IMPORTE'))

                # Instanciar Factura por pk
                try:
                    factura = Factura.objects.get(pk=idventa)
                except ObjectDoesNotExist:
                    no_encontrados += 1
                    with open(tag_file, 'a', encoding='utf-8') as f:
                        f.write(f"{idx_dbf}\t{idventa}\t{caja_numero}\n")
                    continue

                # Actualizar id_caja si está vacío
                caja_obj = cajas_cache.get(caja_numero)
                if caja_obj and not factura.id_caja:
                    factura.id_caja = caja_obj
                    facturas_a_actualizar.append(factura)
                    actualizados_caja += 1

                # Crear RetencionRecibo con CodigoRetencion(pk=5)
                retencion = RetencionRecibo(
                    id_factura=factura,
                    id_codigo_retencion=codigo_retencion_5,  # ✅ AHORA ES CodigoRetencion
                    certificado="Monto Resumen",
                    importe_retencion=importe,
                    fecha_retencion=date.today()
                )
                retenciones_batch.append(retencion)
                creados += 1

                # Guardar lotes
                if len(retenciones_batch) >= batch_size:
                    with transaction.atomic():
                        RetencionRecibo.objects.bulk_create(retenciones_batch)
                        retenciones_batch = []
                if len(facturas_a_actualizar) >= batch_size:
                    with transaction.atomic():
                        Factura.objects.bulk_update(facturas_a_actualizar, ['id_caja'])
                        facturas_a_actualizar = []

            except Exception as e:
                errores += 1
                if errores <= 5:
                    print(f"<error>Error en registro {idx_dbf}: {str(e)}</error>")

        # Guardar últimos lotes
        if retenciones_batch:
            with transaction.atomic():
                RetencionRecibo.objects.bulk_create(retenciones_batch)
        if facturas_a_actualizar:
            with transaction.atomic():
                Factura.objects.bulk_update(facturas_a_actualizar, ['id_caja'])

        # === Resumen final ===
        elapsed = time.time() - start_time
        print(f"\n<info>{'='*50}</info>")
        print("<info>RESUMEN FINAL</info>")
        print(f"<info>Registros procesados: {total_filtrados}</info>")
        print(f"<success>Retenciones creadas: {creados}</success>")
        print(f"<success>Facturas actualizadas (id_caja): {actualizados_caja}</success>")
        print(f"<warning>Facturas no encontradas: {no_encontrados}</warning>")
        print(f"<info>Tiempo total: {elapsed:.2f} segundos</info>")
        print(f"<info>Archivo de no encontradas: {tag_file}</info>")

    except Exception as e:
        print(f"<error>ERROR FATAL: {str(e)}</error>")
        raise

if __name__ == '__main__':
    retencion_recibo_migra()
# neumatic\data_load\deposito_recibo_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, transaction

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
from apps.ventas.models.recibo_models import DepositoRecibo
from apps.maestros.models.base_models import CuentaBanco, ConceptoBanco

# Logging
logging.basicConfig(
    filename='deposito_recibo_migra.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def reset_deposito_recibo():
    """Elimina los datos existentes de manera controlada"""
    try:
        print("<info>Iniciando reset de DepositoRecibo...</info>")
        with transaction.atomic():
            count = DepositoRecibo.objects.count()
            DepositoRecibo.objects.all().delete()
            logger.info(f"Eliminados {count} registros existentes de DepositoRecibo")
            print(f"<info>Eliminados {count} registros existentes de DepositoRecibo</info>")
            
            from django.conf import settings
            engine = settings.DATABASES['default']['ENGINE']
            
            with connection.cursor() as cursor:
                if 'sqlite' in engine:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='deposito_recibo';")
                    print("<info>Secuencia de ID reseteada (SQLite).</info>")
                elif 'postgresql' in engine:
                    cursor.execute("SELECT setval(pg_get_serial_sequence('deposito_recibo', 'id_deposito_recibo'), 1, false);")
                    print("<info>Secuencia de ID reseteada (PostgreSQL).</info>")
                elif 'mssql' in engine or 'sql_server' in engine:
                    cursor.execute("DBCC CHECKIDENT ('deposito_recibo', RESEED, 0);")
                    print("<info>Secuencia de ID reseteada (SQL Server).</info>")
                elif 'mysql' in engine:
                    cursor.execute("ALTER TABLE deposito_recibo AUTO_INCREMENT = 1;")
                    print("<info>Secuencia de ID reseteada (MySQL).</info>")
                else:
                    print(f"<info>Motor {engine} no requiere reset manual de secuencia.</info>")
                    
        print("<info>Reset de DepositoRecibo completado</info>")
    except Exception as e:
        logger.error(f"Error en reset_deposito_recibo: {e}")
        print(f"<error>ERROR en reset_deposito_recibo: {e}</error>")
        raise

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

def deposito_recibo_migra():
    """Migración desde mediopagos.DBF a DepositoRecibo"""
    try:
        start_time = time.time()
        print("<info>Iniciando migración desde mediopagos.DBF a DepositoRecibo...</info>")

        # === LIMPIEZA INICIAL ===
        reset_deposito_recibo()

        # === 1. Instanciar CuentaBanco(pk=1) y ConceptoBanco(pk=1) ===
        try:
            cuenta_banco_1 = CuentaBanco.objects.get(pk=1)
            print(f"<success>CuentaBanco ID=1 cargada: {getattr(cuenta_banco_1, 'descripcion', 'Sin descripción')}</success>")
        except ObjectDoesNotExist:
            print("<error>ERROR: No existe CuentaBanco con ID = 1. Abortando.</error>")
            return

        try:
            concepto_banco_1 = ConceptoBanco.objects.get(pk=1)
            print(f"<success>ConceptoBanco ID=1 cargado: {getattr(concepto_banco_1, 'descripcion', 'Sin descripción')}</success>")
        except ObjectDoesNotExist:
            print("<error>ERROR: No existe ConceptoBanco con ID = 1. Abortando.</error>")
            return

        # === 2. Cargar caché de Cajas por numero_caja ===
        cajas_cache = {caja.numero_caja: caja for caja in Caja.objects.all() if caja.numero_caja}
        print(f"<info>Cargadas {len(cajas_cache)} cajas</info>")

        # === 3. Leer archivo mediopagos.DBF ===
        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'mediopagos.DBF')
        table = DBF(dbf_path, encoding='latin-1')
        total_records = len(table)
        print(f"<info>Total registros en mediopagos.DBF: {total_records}</info>")

        # === 4. Filtrar: FORMAPAGO = 5 AND IDVENTA > 0 ===
        registros_filtrados = []
        for idx, record in enumerate(table, 1):
            formapago = safe_int(record.get('FORMAPAGO'))
            idventa = safe_int(record.get('IDVENTA'))
            if formapago == 5 and idventa > 0:
                registros_filtrados.append((idx, record))
        
        total_filtrados = len(registros_filtrados)
        print(f"<success>Registros filtrados (FORMAPAGO=5 y IDVENTA>0): {total_filtrados}</success>")
        if total_filtrados == 0:
            return

        # === 5. Archivo .tag para facturas no encontradas ===
        tag_file = os.path.join(BASE_DIR, 'data_load', 'deposito_no_encontradas.tag')
        with open(tag_file, 'w', encoding='utf-8') as f:
            f.write("id_caja_detalle\tidventa\tid_caja\n")

        # === 6. Procesamiento ===
        batch_size = 2000
        depositos_batch = []
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

                # === Instanciar Factura por pk (IDVENTA) ===
                try:
                    factura = Factura.objects.get(pk=idventa)
                except ObjectDoesNotExist:
                    no_encontrados += 1
                    with open(tag_file, 'a', encoding='utf-8') as f:
                        f.write(f"{idx_dbf}\t{idventa}\t{caja_numero}\n")
                    continue

                # === Actualizar id_caja si está vacío ===
                caja_obj = cajas_cache.get(caja_numero)
                if caja_obj and not factura.id_caja:
                    factura.id_caja = caja_obj
                    facturas_a_actualizar.append(factura)
                    actualizados_caja += 1

                # === Crear DepositoRecibo ===
                deposito = DepositoRecibo(
                    id_factura=factura,
                    id_cuenta_banco=cuenta_banco_1,
                    id_concepto_banco=concepto_banco_1,
                    fecha_deposito=date.today(),
                    importe_deposito=importe,
                    detalle_deposito="Resumen de depósito"
                )
                depositos_batch.append(deposito)
                creados += 1

                # Guardar lotes
                if len(depositos_batch) >= batch_size:
                    with transaction.atomic():
                        DepositoRecibo.objects.bulk_create(depositos_batch)
                        depositos_batch = []
                if len(facturas_a_actualizar) >= batch_size:
                    with transaction.atomic():
                        Factura.objects.bulk_update(facturas_a_actualizar, ['id_caja'])
                        facturas_a_actualizar = []

            except Exception as e:
                errores += 1
                if errores <= 5:
                    print(f"<error>Error en registro {idx_dbf}: {str(e)}</error>")

        # Guardar últimos lotes
        if depositos_batch:
            with transaction.atomic():
                DepositoRecibo.objects.bulk_create(depositos_batch)
        if facturas_a_actualizar:
            with transaction.atomic():
                Factura.objects.bulk_update(facturas_a_actualizar, ['id_caja'])

        # === Resumen final ===
        elapsed = time.time() - start_time
        print(f"\n<info>{'='*50}</info>")
        print("<info>RESUMEN FINAL</info>")
        print(f"<info>Registros procesados: {total_filtrados}</info>")
        print(f"<success>Depósitos creados: {creados}</success>")
        print(f"<success>Facturas actualizadas (id_caja): {actualizados_caja}</success>")
        print(f"<warning>Facturas no encontradas: {no_encontrados}</warning>")
        print(f"<info>Tiempo total: {elapsed:.2f} segundos</info>")
        print(f"<info>Archivo de no encontradas: {tag_file}</info>")

    except Exception as e:
        print(f"<error>ERROR FATAL: {str(e)}</error>")
        raise

if __name__ == '__main__':
    deposito_recibo_migra()
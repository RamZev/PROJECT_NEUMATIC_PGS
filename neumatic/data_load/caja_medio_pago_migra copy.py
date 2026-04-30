# neumatic\data_load\caja_medio_pago_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import transaction
from decimal import Decimal

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.caja_models import Caja
from apps.maestros.models.base_models import FormaPago

# Importar el modelo CajaMedioPago (ajusta la ruta según tu estructura)
# Si está en el mismo archivo que Caja, sería:
from apps.ventas.models.caja_models import CajaMedioPago

# Configuración de logging
logging.basicConfig(
    filename='caja_medio_pago_migra.log',
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

def cargar_datos_caja_medio_pago():
    """Migración optimizada de mediopagos.DBF a modelo CajaMedioPago"""
    try:
        start_time = time.time()
        
        print("Iniciando migración de CajaMedioPago...")

        # Precargar caches para optimización
        print("Cargando cachés...")
        
        # Cache de cajas por numero_caja
        cajas_cache = {}
        for caja in Caja.objects.all():
            if caja.numero_caja:
                cajas_cache[caja.numero_caja] = caja
        
        print(f"Cargadas {len(cajas_cache)} cajas en caché")
        
        # Cache de formas de pago
        formas_pago_cache = {fp.pk: fp for fp in FormaPago.objects.all()}
        print(f"Cargadas {len(formas_pago_cache)} formas de pago en caché")

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'mediopagos.DBF')
        print(f"Procesando archivo: {dbf_path}")
        
        table = DBF(dbf_path, encoding='latin-1')
        total_records = len(table)
        print(f"Total de registros en DBF: {total_records}")
        
        # Mostrar estructura del DBF
        print("\n=== ESTRUCTURA DEL DBF ===")
        for field in table.fields:
            print(f"  {field.name:12} | Tipo: {field.type} | Tamaño: {field.length}")

        # Procesamiento por lotes
        batch_size = 5000
        medios_pago_batch = []
        registros_procesados = 0
        total_regs = 0
        errores = 0
        cajas_no_encontradas = 0
        formas_pago_no_encontradas = 0
        duplicados = 0

        for idx, record in enumerate(table, 1):
            try:
                # ============================================
                # 1. OBTENER Y VALIDAR CAJA (RELACIÓN PRINCIPAL)
                # ============================================
                caja_numero = safe_int(record.get('CAJA'))
                
                if not caja_numero:
                    logger.warning(f"Registro {idx}: Campo CAJA vacío o inválido, omitiendo...")
                    continue
                
                # Buscar caja en el cache
                caja_obj = cajas_cache.get(caja_numero)
                
                if not caja_obj:
                    cajas_no_encontradas += 1
                    logger.warning(f"Registro {idx}: Caja número {caja_numero} no encontrada en sistema. Omitiendo...")
                    continue
                
                # ============================================
                # 2. OBTENER IDVENTAS
                # ============================================
                idventa_raw = record.get('IDVENTA')
                idventas_int = safe_int(idventa_raw) if idventa_raw and safe_int(idventa_raw) != 0 else None
                
                # ============================================
                # 3. OBTENER FORMA DE PAGO
                # ============================================
                forma_pago_id = safe_int(record.get('FORMAPAGO'))
                forma_pago_obj = None
                
                if forma_pago_id:
                    forma_pago_obj = formas_pago_cache.get(forma_pago_id)
                    if not forma_pago_obj:
                        formas_pago_no_encontradas += 1
                        logger.warning(f"Registro {idx}: Forma de pago ID {forma_pago_id} no encontrada. Usando NULL.")
                
                # ============================================
                # 4. OBTENER IMPORTE
                # ============================================
                importe_raw = record.get('IMPORTE')
                importe_decimal = safe_decimal(importe_raw, 0.0)
                
                # ============================================
                # 5. VERIFICAR SI EL REGISTRO YA EXISTE
                # ============================================
                # Buscar por combinación única
                existe = CajaMedioPago.objects.filter(
                    id_caja=caja_obj,
                    idventas=idventas_int,
                    id_forma_pago=forma_pago_obj,
                    importe=importe_decimal
                ).exists()
                
                if existe:
                    duplicados += 1
                    if duplicados % 100 == 0:
                        logger.debug(f"Registro {idx}: Ya existe en sistema, omitiendo...")
                    continue
                
                # ============================================
                # 6. CREAR OBJETO CAJA MEDIO PAGO
                # ============================================
                # Asumiendo que el modelo CajaMedioPago existe con estos campos:
                # id_caja_medio_pago (AutoField)
                # id_caja (ForeignKey a Caja)
                # idventas (IntegerField)
                # id_forma_pago (ForeignKey a FormaPago)
                # importe (DecimalField)
                
                caja_medio_pago = CajaMedioPago(
                    id_caja=caja_obj,
                    idventas=idventas_int,
                    id_forma_pago=forma_pago_obj,
                    importe=importe_decimal
                    # NOTA: No incluir created_at, updated_at, is_active
                    # ModeloBaseGenerico los maneja automáticamente si hereda de él
                )
                
                medios_pago_batch.append(caja_medio_pago)
                registros_procesados += 1

                # Mostrar progreso cada 5000 registros
                if registros_procesados % 5000 == 0:
                    print(f"Procesados: {registros_procesados}/{total_records} registros")
                    
                    # Mostrar ejemplo del último registro procesado
                    if registros_procesados <= 25000:  # Solo primeros 5 lotes
                        print(f"  Ejemplo: Caja {caja_numero} | IDVenta: {idventas_int} | FormaPago: {forma_pago_id} | Importe: {importe_decimal}")

                # Guardar por lotes
                if len(medios_pago_batch) >= batch_size:
                    with transaction.atomic():
                        CajaMedioPago.objects.bulk_create(medios_pago_batch)
                        print(f"Lote guardado: {len(medios_pago_batch)} registros")
                        total_regs += len(medios_pago_batch)
                        medios_pago_batch = []

            except Exception as e:
                errores += 1
                logger.error(f"Error en registro {idx} (Caja: {record.get('CAJA')}): {str(e)}")
                print(f"Error en registro {idx}: {str(e)}")
                continue

        # Guardar últimos registros
        if medios_pago_batch:
            with transaction.atomic():
                CajaMedioPago.objects.bulk_create(medios_pago_batch)
                print(f"Último lote guardado: {len(medios_pago_batch)} registros")
                total_regs += len(medios_pago_batch)

        # Resultados finales
        elapsed_time = time.time() - start_time
        
        print(f"\n=== RESUMEN FINAL ===")
        print(f"Total registros en DBF: {total_records}")
        print(f"Registros procesados exitosamente: {registros_procesados}")
        print(f"Cajas no encontradas (omitidas): {cajas_no_encontradas}")
        print(f"Formas de pago no encontradas: {formas_pago_no_encontradas}")
        print(f"Duplicados omitidos: {duplicados}")
        print(f"Errores encontrados: {errores}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")
        
        if cajas_no_encontradas > 0:
            print(f"\nADVERTENCIA: {cajas_no_encontradas} registros omitidos porque no se encontró la caja correspondiente.")
            print("Asegúrate de haber migrado las cajas primero con caja_migra.py")
        
        # Verificación simple
        if registros_procesados > 0:
            print(f"\n=== VERIFICACIÓN RÁPIDA ===")
            try:
                total_final = CajaMedioPago.objects.count()
                print(f"Total registros en base de datos: {total_final}")
                
                # Ver primeros 5 registros como ejemplo
                primeros = CajaMedioPago.objects.select_related('id_caja', 'id_forma_pago')[:5]
                print(f"\nPrimeros 5 registros migrados:")
                for i, medio_pago in enumerate(primeros, 1):
                    caja_num = medio_pago.id_caja.numero_caja if medio_pago.id_caja else "N/A"
                    forma_pago = medio_pago.id_forma_pago.descripcion if medio_pago.id_forma_pago else "N/A"
                    print(f"  {i}. Caja {caja_num} | Venta: {medio_pago.idventas} | {forma_pago} | ${medio_pago.importe}")
            except Exception as e:
                print(f"Nota: Error en verificación (no crítico): {e}")
                # Si el modelo no tiene los campos exactos, mostrar solo el conteo
                print(f"Registros migrados: {registros_procesados}")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_caja_medio_pago: {str(e)}")
        print(f"ERROR FATAL: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_caja_medio_pago()
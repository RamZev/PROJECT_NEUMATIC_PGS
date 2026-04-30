# neumatic\data_load\cajadetalle_migra.py
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

from apps.ventas.models.caja_models import Caja, CajaDetalle
from apps.maestros.models.base_models import FormaPago

# Configuración de logging
logging.basicConfig(
    filename='cajadetalle_migra.log',
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

def cargar_datos_cajadetalle():
    """Migración optimizada de cajadetalle.DBF a modelo CajaDetalle"""
    try:
        start_time = time.time()
        
        print("Iniciando migración de CajaDetalle...")
        print("NOTA: Campo de observación en DBF es 'OBSERVACIO' (10 chars)")

        # Precargar caches
        print("Cargando cachés...")
        
        cajas_cache = {}
        for caja in Caja.objects.all():
            if caja.numero_caja:
                cajas_cache[caja.numero_caja] = caja
        
        print(f"Cargadas {len(cajas_cache)} cajas en caché")
        
        formas_pago_cache = {fp.pk: fp for fp in FormaPago.objects.all()}
        print(f"Cargadas {len(formas_pago_cache)} formas de pago en caché")

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'cajadetalle.DBF')
        print(f"Procesando archivo: {dbf_path}")
        
        table = DBF(dbf_path, encoding='latin-1')
        total_records = len(table)
        print(f"Total de registros en DBF: {total_records}")
        
        # Mostrar estructura del DBF
        print("\n=== ESTRUCTURA DEL DBF ===")
        for field in table.fields:
            print(f"  {field.name:12} | Tipo: {field.type} | Tamaño: {field.length}")

        # Contadores
        batch_size = 5000
        detalles_batch = []
        registros_procesados = 0
        total_regs = 0
        errores = 0
        cajas_no_encontradas = 0
        formas_pago_no_encontradas = 0
        observaciones_con_valor = 0

        for idx, record in enumerate(table, 1):
            try:
                # 1. OBTENER CAJA
                caja_numero = safe_int(record.get('CAJA'))
                
                if not caja_numero:
                    continue
                
                caja_obj = cajas_cache.get(caja_numero)
                if not caja_obj:
                    cajas_no_encontradas += 1
                    continue
                
                # 2. OBTENER FORMA DE PAGO
                forma_pago_id = safe_int(record.get('FORMAPAGO'))
                forma_pago_obj = None
                
                if forma_pago_id:
                    forma_pago_obj = formas_pago_cache.get(forma_pago_id)
                    if not forma_pago_obj:
                        formas_pago_no_encontradas += 1
                
                # 3. VALORES NUMÉRICOS
                idventas_val = record.get('IDVENTAS')
                idventas_int = safe_int(idventas_val) if idventas_val and safe_int(idventas_val) != 0 else None
                
                idcompras_val = record.get('IDCOMPRAS')
                idcompras_int = safe_int(idcompras_val) if idcompras_val and safe_int(idcompras_val) != 0 else None
                
                idbancos_val = record.get('IDBANCOS')
                idbancos_int = safe_int(idbancos_val) if idbancos_val and safe_int(idbancos_val) != 0 else None
                
                importe_val = record.get('IMPORTE')
                importe_decimal = safe_decimal(importe_val, 0.0)
                
                # 4. TIPO DE MOVIMIENTO
                tipo_movimiento = 1 if importe_decimal >= Decimal('0') else 2
                
                # 5. OBSERVACIÓN - ¡CORREGIDO! Usar OBSERVACIO
                observacion_raw = record.get('OBSERVACIO')  # ¡CORRECCIÓN AQUÍ!
                observacion = ''
                
                if observacion_raw is not None:
                    observacion_str = str(observacion_raw)
                    
                    if observacion_str.strip():
                        observacion = observacion_str.strip()[:50]
                        observaciones_con_valor += 1
                        
                        # Mostrar primeras 5 observaciones como ejemplo
                        if observaciones_con_valor <= 5:
                            print(f"\nEjemplo observación {observaciones_con_valor}:")
                            print(f"  Registro: {idx}")
                            print(f"  Valor original: '{observacion_raw}'")
                            print(f"  Procesado: '{observacion}'")
                            print(f"  Longitud: {len(observacion)}")
                
                # 6. CREAR OBJETO
                caja_detalle = CajaDetalle(
                    id_caja=caja_obj,
                    idventas=idventas_int,
                    idcompras=idcompras_int,
                    idbancos=idbancos_int,
                    id_forma_pago=forma_pago_obj,
                    importe=importe_decimal,
                    tipo_movimiento=tipo_movimiento,
                    observacion=observacion
                )
                
                detalles_batch.append(caja_detalle)
                registros_procesados += 1

                # Progreso
                if registros_procesados % 5000 == 0:
                    print(f"Procesados: {registros_procesados}/{total_records} registros")
                    print(f"Observaciones con valor hasta ahora: {observaciones_con_valor}")

                # Guardar por lotes
                if len(detalles_batch) >= batch_size:
                    with transaction.atomic():
                        CajaDetalle.objects.bulk_create(detalles_batch)
                        print(f"Lote guardado: {len(detalles_batch)} registros")
                        total_regs += len(detalles_batch)
                        detalles_batch = []

            except Exception as e:
                errores += 1
                print(f"Error en registro {idx}: {str(e)}")
                continue

        # Guardar últimos registros
        if detalles_batch:
            with transaction.atomic():
                CajaDetalle.objects.bulk_create(detalles_batch)
                print(f"Último lote guardado: {len(detalles_batch)} registros")
                total_regs += len(detalles_batch)

        # Resultados finales
        elapsed_time = time.time() - start_time
        
        print(f"\n=== RESUMEN FINAL ===")
        print(f"Total registros en DBF: {total_records}")
        print(f"Registros procesados: {registros_procesados}")
        print(f"Cajas no encontradas: {cajas_no_encontradas}")
        print(f"Formas de pago no encontradas: {formas_pago_no_encontradas}")
        print(f"Observaciones con valor: {observaciones_con_valor}")
        print(f"Porcentaje con observación: {observaciones_con_valor/total_records*100:.2f}%")
        print(f"Errores: {errores}")
        print(f"Tiempo: {elapsed_time:.2f} segundos")
        
        # Log detallado
        logger.info(f"Campo de observación: OBSERVACIO")
        logger.info(f"Observaciones con valor encontradas: {observaciones_con_valor}")
        logger.info(f"Porcentaje: {observaciones_con_valor/total_records*100:.2f}%")
        logger.info(f"Total procesados: {registros_procesados}")
        
        if observaciones_con_valor == 0:
            print("\n¡ADVERTENCIA! Aún no se encontraron observaciones con valor.")
            print("Puede que realmente estén vacías o haya problemas de encoding.")
        else:
            print(f"\n¡ÉXITO! Se encontraron {observaciones_con_valor} observaciones con valor.")

    except Exception as e:
        print(f"ERROR FATAL: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_cajadetalle()
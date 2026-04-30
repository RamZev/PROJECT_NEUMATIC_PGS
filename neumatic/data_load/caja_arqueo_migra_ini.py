# neumatic\data_load\caja_arqueo_migra.py
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

from apps.ventas.models.caja_models import Caja, CajaArqueo

# Configuración de logging
logging.basicConfig(
    filename='caja_arqueo_migra.log',
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

def cargar_datos_caja_arqueo():
    """Migración optimizada de cajaarqueo.DBF a modelo CajaArqueo"""
    try:
        start_time = time.time()
        
        print("Iniciando migración de CajaArqueo...")

        # Precargar caches para optimización
        print("Cargando cachés...")
        
        # Cache de cajas por numero_caja
        cajas_cache = {}
        for caja in Caja.objects.all():
            if caja.numero_caja:
                cajas_cache[caja.numero_caja] = caja
        
        print(f"Cargadas {len(cajas_cache)} cajas en caché")

        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'cajaarqueo.DBF')
        print(f"Procesando archivo: {dbf_path}")
        
        table = DBF(dbf_path, encoding='latin-1')
        total_records = len(table)
        print(f"Total de registros en DBF: {total_records}")
        
        # Mostrar estructura del DBF
        print("\n=== ESTRUCTURA DEL DBF ===")
        for field in table.fields:
            print(f"  {field.name:10} | Tipo: {field.type} | Tamaño: {field.length}")

        # Procesamiento por lotes
        batch_size = 5000
        arqueos_batch = []
        registros_procesados = 0
        total_regs = 0
        errores = 0
        cajas_no_encontradas = 0
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
                # 2. PROCESAR CANTIDAD
                # ============================================
                cantidad_raw = record.get('CANTIDAD')
                cantidad_decimal = safe_decimal(cantidad_raw, 0)
                
                # Convertir a entero (decimal_places=0 en el modelo)
                cantidad_int = int(cantidad_decimal) if cantidad_decimal else None
                
                # ============================================
                # 3. PROCESAR VALOR UNITARIO
                # ============================================
                valor_raw = record.get('VALOR')
                valor_decimal = safe_decimal(valor_raw, 0)
                
                # ============================================
                # 4. PROCESAR DETALLE
                # ============================================
                detalle_raw = record.get('DETALLE', '')
                detalle = ''
                
                if detalle_raw is not None:
                    detalle_str = str(detalle_raw).strip()
                    if detalle_str:
                        # Limitar a 15 caracteres como máximo
                        detalle = detalle_str[:15]
                
                # ============================================
                # 5. CALCULAR TOTAL (cantidad * valor)
                # ============================================
                total_raw = record.get('TOTAL')
                total_decimal = None
                
                # Si existe el campo TOTAL en el DBF, usarlo
                if total_raw is not None:
                    total_decimal = safe_decimal(total_raw, 0)
                else:
                    # Calcular automáticamente si no existe
                    if cantidad_decimal and valor_decimal:
                        total_decimal = cantidad_decimal * valor_decimal
                    else:
                        total_decimal = Decimal('0')
                
                # ============================================
                # 6. VERIFICAR SI EL REGISTRO YA EXISTE
                # ============================================
                # Buscar por combinación única
                existe = CajaArqueo.objects.filter(
                    id_caja=caja_obj,
                    cantidad=cantidad_int,
                    valor=valor_decimal,
                    detalle=detalle
                ).exists()
                
                if existe:
                    duplicados += 1
                    if duplicados % 100 == 0:
                        logger.debug(f"Registro {idx}: Ya existe en sistema, omitiendo...")
                    continue
                
                # ============================================
                # 7. CREAR OBJETO CAJA ARQUEO
                # ============================================
                caja_arqueo = CajaArqueo(
                    id_caja=caja_obj,
                    cantidad=cantidad_int,
                    valor=valor_decimal,
                    detalle=detalle,
                    total=total_decimal
                    # NOTA: No incluir created_at, updated_at, is_active
                    # ModeloBaseGenerico los maneja automáticamente
                )
                
                arqueos_batch.append(caja_arqueo)
                registros_procesados += 1

                # Mostrar progreso cada 5000 registros
                if registros_procesados % 5000 == 0:
                    print(f"Procesados: {registros_procesados}/{total_records} registros")
                    
                    # Mostrar ejemplo del último registro procesado
                    if registros_procesados <= 25000:  # Solo primeros 5 lotes
                        print(f"  Ejemplo: Caja {caja_numero} | {detalle} | Cant: {cantidad_int} | Valor: {valor_decimal} | Total: {total_decimal}")

                # Guardar por lotes
                if len(arqueos_batch) >= batch_size:
                    with transaction.atomic():
                        CajaArqueo.objects.bulk_create(arqueos_batch)
                        print(f"Lote guardado: {len(arqueos_batch)} registros")
                        total_regs += len(arqueos_batch)
                        arqueos_batch = []

            except Exception as e:
                errores += 1
                logger.error(f"Error en registro {idx} (Caja: {record.get('CAJA')}): {str(e)}")
                print(f"Error en registro {idx}: {str(e)}")
                continue

        # Guardar últimos registros
        if arqueos_batch:
            with transaction.atomic():
                CajaArqueo.objects.bulk_create(arqueos_batch)
                print(f"Último lote guardado: {len(arqueos_batch)} registros")
                total_regs += len(arqueos_batch)

        # Resultados finales
        elapsed_time = time.time() - start_time
        
        print(f"\n=== RESUMEN FINAL ===")
        print(f"Total registros en DBF: {total_records}")
        print(f"Registros procesados exitosamente: {registros_procesados}")
        print(f"Cajas no encontradas (omitidas): {cajas_no_encontradas}")
        print(f"Duplicados omitidos: {duplicados}")
        print(f"Errores encontrados: {errores}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")
        
        if cajas_no_encontradas > 0:
            print(f"\nADVERTENCIA: {cajas_no_encontradas} registros omitidos porque no se encontró la caja correspondiente.")
            print("Asegúrate de haber migrado las cajas primero con caja_migra.py")
        
        # Mostrar estadísticas de datos procesados
        if registros_procesados > 0:
            print(f"\n=== ESTADÍSTICAS DE DATOS MIGRADOS ===")
            # Contar registros únicos por caja
            from django.db.models import Count
            stats = CajaArqueo.objects.values('id_caja__numero_caja').annotate(
                total_registros=Count('id_caja_arqueo')
            ).order_by('id_caja__numero_caja')[:10]  # Primeras 10 cajas
            
            print(f"Primeras 10 cajas con arqueos:")
            for stat in stats:
                print(f"  Caja {stat['id_caja__numero_caja']}: {stat['total_registros']} registros")
            
            # Total general
            total_final = CajaArqueo.objects.count()
            print(f"\nTotal registros en base de datos: {total_final}")

    except Exception as e:
        logger.error(f"Error fatal en cargar_datos_caja_arqueo: {str(e)}")
        print(f"ERROR FATAL: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos_caja_arqueo()
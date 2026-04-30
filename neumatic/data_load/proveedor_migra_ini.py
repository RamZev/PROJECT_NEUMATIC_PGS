import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from django.db import transaction
from collections import defaultdict
from datetime import datetime

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.proveedor_models import Proveedor
from apps.maestros.models.base_models import Provincia, Localidad, TipoIva, TipoRetencionIb

# Configurar logging
logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'proveedor_migra.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_progress(current, total, start_time, last_print_time):
    """Muestra el progreso de la migración"""
    elapsed = time.time() - start_time
    percent = (current / total) * 100
    speed = current / elapsed if elapsed > 0 else 0
    
    # Calcular tiempo estimado restante
    remaining = (total - current) / speed if speed > 0 else 0
    remaining_str = time.strftime("%H:%M:%S", time.gmtime(remaining))
    
    print(
        f"\rProgreso: {current:,}/{total:,} ({percent:.1f}%) | "
        f"Velocidad: {speed:.1f} reg/s | "
        f"Tiempo restante: {remaining_str}",
        end='', flush=True
    )
    return time.time()

def reset_proveedor():
    """Elimina los datos existentes en la tabla Proveedor y resetea su ID"""
    print("\nInicializando migración...")
    try:
        with transaction.atomic():
            count = Proveedor.objects.count()
            if count > 0:
                print(f"Eliminando {count:,} registros existentes...")
                Proveedor.objects.all().delete()
                logger.info(f"Eliminados {count} registros existentes de Proveedor")
            
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='proveedor';")
            print("Base de datos preparada para la migración.")
    except Exception as e:
        logger.error(f"Error en reset_proveedor: {e}")
        raise

def precargar_relaciones():
    """Precarga todas las relaciones necesarias en diccionarios para optimización"""
    print("\nPrecargando relaciones en memoria...")
    logger.info("Precargando relaciones en memoria...")
    
    relaciones = {
        'tipos_iva': defaultdict(
            lambda: None,
            {
                "CF": TipoIva.objects.get(pk=1),
                "EXE": TipoIva.objects.get(pk=2),
                "RMT": TipoIva.objects.get(pk=3),
                "RI": TipoIva.objects.get(pk=4)
            }
        ),
        'retenciones_ib': defaultdict(
            lambda: None,
            {str(r.pk): r for r in TipoRetencionIb.objects.all()}
        ),
        'localidades': defaultdict(list),
    }
    
    # Precargar valores por defecto con manejo de excepciones
    try:
        relaciones['default_localidad'] = Localidad.objects.get(pk=2349)
    except Localidad.DoesNotExist:
        logger.warning("Localidad con pk=2349 no encontrada. Se asignará None.")
        relaciones['default_localidad'] = None
    
    try:
        relaciones['default_provincia'] = Provincia.objects.get(pk=13)
    except Provincia.DoesNotExist:
        logger.warning("Provincia con pk=13 no encontrada. Se asignará None.")
        relaciones['default_provincia'] = None
    
    try:
        relaciones['default_tipo_iva'] = TipoIva.objects.get(pk=1)
    except TipoIva.DoesNotExist:
        logger.warning("TipoIva con pk=1 no encontrada. Se asignará None.")
        relaciones['default_tipo_iva'] = None
    
    try:
        relaciones['default_tipo_retencion_ib'] = None  # Cambiado a None para respetar null=True
    except TipoRetencionIb.DoesNotExist:
        logger.warning("TipoRetencionIb con pk=1 no encontrada. Se asignará None.")
        relaciones['default_tipo_retencion_ib'] = None
    
    for loc in Localidad.objects.select_related('id_provincia').all():
        relaciones['localidades'][loc.codigo_postal].append(loc)
    
    print("Relaciones precargadas en memoria.")
    logger.info("Relaciones precargadas en memoria")
    return relaciones

def procesar_lote(records, cache, batch_start):
    """Procesa un lote de registros y devuelve instancias válidas de Proveedor"""
    proveedores = []
    used_cuits = set()  # Para manejar la restricción UNIQUE de CUIT
    
    for idx, record in enumerate(records):
        try:
            # Convertir CODIGO a entero
            try:
                codigo_origen = int(float(record.get('CODIGO', 0)))
            except (ValueError, TypeError):
                logger.warning(f"Valor inválido en CODIGO: {record.get('CODIGO')}. Registro omitido.")
                continue

            # Obtener instancias desde caché
            tipo_iva = cache['tipos_iva'][record.get('IVA', '').strip() if record.get('IVA') else ''] or cache['default_tipo_iva']
            
            # Manejo de id_tipo_retencion_ib (permite None)
            retencion_ib_value = str(record.get('IDRETENCION', '')) if record.get('IDRETENCION') is not None else ''
            retencion_ib = cache['retenciones_ib'].get(retencion_ib_value, None)
            if not retencion_ib and retencion_ib_value:
                logger.warning(f"Tipo Retención IB no válido para registro {record.get('CODIGO')}: '{retencion_ib_value}'. Asignando None.")
            
            # Validar claves foráneas obligatorias
            if not tipo_iva:
                logger.warning(f"Tipo IVA no válido para registro {record.get('CODIGO')}. Registro omitido.")
                continue
            
            # Localidad y provincia
            localidad_value = str(record.get('LOCALIDAD', ''))[:5] if record.get('LOCALIDAD') is not None else ''
            localidad_list = cache['localidades'].get(localidad_value, [])
            if localidad_list:
                id_localidad = localidad_list[0]
                id_provincia = id_localidad.id_provincia
            else:
                id_localidad = cache['default_localidad']
                id_provincia = cache['default_provincia']
            
            # Validar localidad y provincia
            if not id_localidad or not id_provincia:
                logger.warning(f"Localidad o provincia no válidas para registro {record.get('CODIGO')}. Registro omitido.")
                continue

            # Manejo de CUIT con restricción UNIQUE
            cuit = int(str(record.get('CUIT', 0)) if record.get('CUIT') is not None else '0')
            current_count = batch_start + idx
            if cuit == 0 or cuit in used_cuits:
                cuit = 99999999999 - current_count  # Valor temporal único
            used_cuits.add(cuit)

            # Manejo de campos obligatorios con valores potencialmente None
            ib_numero = str(record.get('INGBRUTO', '')) if record.get('INGBRUTO') is not None else "000000000000000"
            ib_exento = record.get('EXENTOIB', False)
            ib_alicuota = float(record.get('ALICIB', 0.00)) if record.get('ALICIB') is not None else 0.00
            nombre = str(record.get('NOMBRE', ''))[:50] if record.get('NOMBRE') is not None else ''
            domicilio = str(record.get('DOMICILIO', ''))[:50] if record.get('DOMICILIO') is not None else ''
            codigo_postal = str(record.get('CODPOSTAL', ''))[:5] if record.get('CODPOSTAL') is not None else "00000"
            telefono = str(record.get('TELEFONO', ''))[:15] if record.get('TELEFONO') is not None else ''
            email = str(record.get('MAIL', ''))[:50] if record.get('MAIL') is not None else ''
            nota = str(record.get('NOTA', '')) if record.get('NOTA') is not None else ''

            # Crear instancia de Proveedor
            proveedor = Proveedor(
                id_proveedor=codigo_origen,
                estatus_proveedor=True,
                nombre_proveedor=nombre,
                domicilio_proveedor=domicilio,
                codigo_postal=codigo_postal,
                id_provincia=id_provincia,
                id_localidad=id_localidad,
                id_tipo_iva=tipo_iva,
                cuit=cuit,
                id_tipo_retencion_ib=retencion_ib,  # Puede ser None
                ib_numero=ib_numero,
                ib_exento=ib_exento,
                ib_alicuota=ib_alicuota,
                multilateral=record.get('MULTILATERAL', False),
                telefono_proveedor=telefono,
                movil_proveedor=None,
                email_proveedor=email,
                observacion_proveedor=nota
            )
            proveedores.append(proveedor)
            
        except Exception as e:
            logger.error(f"Error procesando registro {record.get('CODIGO', 'DESCONOCIDO')}: {str(e)}")
            continue
            
    return proveedores

def cargar_datos():
    """Función principal de migración con progreso visual"""
    try:
        start_time = time.time()
        last_print_time = start_time
        logger.info("Iniciando migración de proveedores")
        print("\nIniciando migración de proveedores...")
        
        # 1. Resetear datos existentes
        reset_proveedor()
        
        # 2. Precargar relaciones en memoria
        cache = precargar_relaciones()
        
        # 3. Configuración de procesamiento por lotes
        batch_size = 1000  # Tamaño del lote para bulk_create
        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'proveedor.DBF')
        total_registros = 0
        
        # 4. Procesamiento optimizado por lotes
        with transaction.atomic():
            # Leer el archivo DBF completo en memoria
            print("\nCargando archivo DBF en memoria...")
            try:
                records = list(DBF(dbf_path, encoding='latin-1'))
            except PermissionError as e:
                logger.error(f"Error de permisos al acceder al archivo: {e}")
                raise
            except Exception as e:
                logger.error(f"Error al cargar el archivo DBF: {e}")
                raise
            total_registros_dbf = len(records)
            print(f"DBF cargado. Total registros a procesar: {total_registros_dbf:,}")
            logger.info(f"DBF cargado en memoria. Total registros: {total_registros_dbf}")
            
            # Procesar en lotes de batch_size
            for i in range(0, total_registros_dbf, batch_size):
                batch_records = records[i:i + batch_size]
                proveedores_batch = procesar_lote(batch_records, cache, i)
                
                if proveedores_batch:
                    try:
                        Proveedor.objects.bulk_create(proveedores_batch)
                        total_registros += len(proveedores_batch)
                    except Exception as e:
                        logger.error(f"Error al guardar lote {i//batch_size + 1}: {str(e)}")
                        continue
                
                # Mostrar progreso cada 1,000 registros
                if i > 0 and i % 1000 == 0:
                    last_print_time = print_progress(i, total_registros_dbf, start_time, last_print_time)
                
                # Liberar memoria
                del batch_records
                del proveedores_batch
            
            # Mostrar progreso final
            print_progress(total_registros_dbf, total_registros_dbf, start_time, last_print_time)
            print()  # Nueva línea después del progreso
        
        # 5. Resultados finales
        elapsed_time = time.time() - start_time
        logger.info(
            f"Migración completada. "
            f"Total registros procesados: {total_registros}/{total_registros_dbf}. "
            f"Tiempo: {elapsed_time:.2f} segundos"
        )
        
        print(f"\n{'='*50}")
        print(f"Migración finalizada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Registros procesados: {total_registros:,}/{total_registros_dbf:,}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")
        print(f"Velocidad: {total_registros/elapsed_time:.1f} registros/segundo" if elapsed_time > 0 else "N/A")
        print(f"{'='*50}")
        
    except Exception as e:
        logger.error(f"Error crítico en cargar_datos: {str(e)}")
        print(f"\nERROR: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos()
# neumatic\data_load\proveedor_migra.py
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
from django.conf import settings

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
    Proveedor.objects.all().delete()
    print("Tabla Proveedor limpiada.")
    
    engine = settings.DATABASES['default']['ENGINE']
    
    try:
        with connection.cursor() as cursor:
            if 'sqlite' in engine:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='proveedor';")
                print("Secuencia de ID reseteada (SQLite).")
            elif 'postgresql' in engine:
                cursor.execute("SELECT setval(pg_get_serial_sequence('proveedor', 'id_proveedor'), 1, false);")
                print("Secuencia de ID reseteada (PostgreSQL).")
            elif 'mssql' in engine or 'sql_server' in engine:
                cursor.execute("DBCC CHECKIDENT ('proveedor', RESEED, 0);")
                print("Secuencia de ID reseteada (SQL Server).")
            elif 'mysql' in engine:
                cursor.execute("ALTER TABLE proveedor AUTO_INCREMENT = 1;")
                print("Secuencia de ID reseteada (MySQL).")
            else:
                print(f"Motor {engine} no requiere reset manual de secuencia.")
        
        logger.info("Tabla Proveedor limpiada y secuencia reseteada.")
        
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
        relaciones['default_tipo_retencion_ib'] = None
    except:
        relaciones['default_tipo_retencion_ib'] = None
    
    for loc in Localidad.objects.select_related('id_provincia').all():
        relaciones['localidades'][loc.codigo_postal].append(loc)
    
    print("Relaciones precargadas en memoria.")
    logger.info("Relaciones precargadas en memoria")
    return relaciones

def procesar_lote(records, cache, batch_start):
    """Procesa un lote de registros y devuelve instancias válidas de Proveedor"""
    proveedores = []
    used_cuits = set()
    
    for idx, record in enumerate(records):
        try:
            codigo_origen = int(float(record.get('CODIGO', 0)))
            
            # DEBUG: Mostrar primeros 5 registros
            if batch_start + idx < 5:
                print(f"\n[DEBUG] Registro {batch_start + idx + 1}:")
                print(f"  CODIGO: {codigo_origen}")
                print(f"  NOMBRE: {record.get('NOMBRE', '')}")
                print(f"  IVA: '{record.get('IVA', '')}'")
                print(f"  LOCALIDAD: '{record.get('LOCALIDAD', '')}'")
                print(f"  CUIT: {record.get('CUIT', '')}")
            
            # Obtener tipo_iva
            iva_value = record.get('IVA', '').strip() if record.get('IVA') else ''
            tipo_iva = cache['tipos_iva'].get(iva_value) or cache['default_tipo_iva']
            
            if not tipo_iva:
                logger.warning(f"Tipo IVA no válido para registro {codigo_origen}: '{iva_value}'")
                continue
            
            # Obtener localidad
            localidad_value = str(record.get('LOCALIDAD', ''))[:5] if record.get('LOCALIDAD') is not None else ''
            localidad_list = cache['localidades'].get(localidad_value, [])
            
            if localidad_list:
                id_localidad = localidad_list[0]
                id_provincia = id_localidad.id_provincia
            else:
                id_localidad = cache['default_localidad']
                id_provincia = cache['default_provincia']
            
            if not id_localidad or not id_provincia:
                logger.warning(f"Localidad o provincia no válidas para registro {codigo_origen}")
                continue
            
            # Obtener retencion_ib
            retencion_ib_value = str(record.get('IDRETENCION', '')) if record.get('IDRETENCION') is not None else ''
            retencion_ib = cache['retenciones_ib'].get(retencion_ib_value, None)
            
            # Manejo de CUIT
            cuit = int(str(record.get('CUIT', 0)) if record.get('CUIT') is not None else '0')
            current_count = batch_start + idx
            if cuit == 0 or cuit in used_cuits:
                cuit = 99999999999 - current_count
            used_cuits.add(cuit)
            
            # Crear proveedor
            proveedor = Proveedor(
                id_proveedor=codigo_origen,
                estatus_proveedor=True,
                nombre_proveedor=str(record.get('NOMBRE', ''))[:50] if record.get('NOMBRE') else '',
                domicilio_proveedor=str(record.get('DOMICILIO', ''))[:50] if record.get('DOMICILIO') else '',
                codigo_postal=str(record.get('CODPOSTAL', ''))[:5] if record.get('CODPOSTAL') else "00000",
                id_provincia=id_provincia,
                id_localidad=id_localidad,
                id_tipo_iva=tipo_iva,
                cuit=cuit,
                id_tipo_retencion_ib=retencion_ib,
                ib_numero=str(record.get('INGBRUTO', '')) if record.get('INGBRUTO') else "000000000000000",
                ib_exento=record.get('EXENTOIB', False),
                ib_alicuota=float(record.get('ALICIB', 0.00)) if record.get('ALICIB') else 0.00,
                multilateral=record.get('MULTILATERAL', False),
                telefono_proveedor=str(record.get('TELEFONO', ''))[:15] if record.get('TELEFONO') else '',
                movil_proveedor=None,
                email_proveedor=str(record.get('MAIL', ''))[:50] if record.get('MAIL') else '',
                observacion_proveedor=str(record.get('NOTA', '')) if record.get('NOTA') else ''
            )
            proveedores.append(proveedor)
            
            # DEBUG: Mostrar cuando se crea un proveedor
            if batch_start + idx < 5:
                print(f"  ✅ Proveedor {codigo_origen} creado correctamente")
            
        except Exception as e:
            logger.error(f"Error procesando registro {record.get('CODIGO', 'DESCONOCIDO')}: {str(e)}")
            if batch_start + idx < 5:
                print(f"  ❌ Error: {str(e)}")
            continue
            
    return proveedores

def cargar_datos():
    """Función principal de migración con progreso visual"""
    try:
        start_time = time.time()
        last_print_time = start_time
        logger.info("Iniciando migración de proveedores")
        print("\nIniciando migración de proveedores...")
        
        reset_proveedor()
        cache = precargar_relaciones()
        
        batch_size = 1000
        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'proveedor.DBF')
        total_registros = 0
        
        with transaction.atomic():
            print("\nCargando archivo DBF en memoria...")
            records = list(DBF(dbf_path, encoding='latin-1'))
            total_registros_dbf = len(records)
            print(f"DBF cargado. Total registros a procesar: {total_registros_dbf:,}")
            logger.info(f"DBF cargado en memoria. Total registros: {total_registros_dbf}")
            
            # Mostrar primeros registros del DBF
            print("\n[DEBUG] Primeros registros del DBF:")
            for i, record in enumerate(records[:3]):
                print(f"\nRegistro {i+1}:")
                for key, value in list(record.items())[:10]:
                    print(f"  {key}: {value}")
            
            for i in range(0, total_registros_dbf, batch_size):
                batch_records = records[i:i + batch_size]
                proveedores_batch = procesar_lote(batch_records, cache, i)
                
                if proveedores_batch:
                    Proveedor.objects.bulk_create(proveedores_batch)
                    total_registros += len(proveedores_batch)
                
                if i > 0 and i % 1000 == 0:
                    last_print_time = print_progress(i, total_registros_dbf, start_time, last_print_time)
                
                del batch_records
                del proveedores_batch
            
            print_progress(total_registros_dbf, total_registros_dbf, start_time, last_print_time)
            print()
        
        elapsed_time = time.time() - start_time
        logger.info(f"Migración completada. Total registros procesados: {total_registros}/{total_registros_dbf}. Tiempo: {elapsed_time:.2f} segundos")
        
        print(f"\n{'='*50}")
        print(f"Migración finalizada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Registros procesados: {total_registros:,}/{total_registros_dbf:,}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")
        print(f"{'='*50}")
        
    except Exception as e:
        logger.error(f"Error crítico en cargar_datos: {str(e)}")
        print(f"\nERROR: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos()# neumatic\data_load\proveedor_migra.py
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
from django.conf import settings

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
    engine = settings.DATABASES['default']['ENGINE']
    
    print("\nInicializando migración...")
    try:
        if 'mssql' in engine or 'sql_server' in engine:
            with connection.cursor() as cursor:
                count = Proveedor.objects.count()
                if count > 0:
                    print(f"Eliminando {count:,} registros existentes...")
                cursor.execute("DELETE FROM proveedor")
                cursor.execute("DBCC CHECKIDENT ('proveedor', RESEED, 0);")
                logger.info(f"Eliminados {count} registros existentes de Proveedor (SQL Server)")
            print("Base de datos preparada para la migración (SQL Server).")
        else:
            with transaction.atomic():
                count = Proveedor.objects.count()
                if count > 0:
                    print(f"Eliminando {count:,} registros existentes...")
                    Proveedor.objects.all().delete()
                    logger.info(f"Eliminados {count} registros existentes de Proveedor")
                
                if 'sqlite' in connection.settings_dict['ENGINE']:
                    with connection.cursor() as cursor:
                        cursor.execute("DELETE FROM sqlite_sequence WHERE name='proveedor';")
            print("Base de datos preparada para la migración (SQLite).")
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
        relaciones['default_tipo_retencion_ib'] = None
    except:
        relaciones['default_tipo_retencion_ib'] = None
    
    for loc in Localidad.objects.select_related('id_provincia').all():
        relaciones['localidades'][loc.codigo_postal].append(loc)
    
    print("Relaciones precargadas en memoria.")
    logger.info("Relaciones precargadas en memoria")
    return relaciones

def procesar_lote(records, cache, batch_start):
    """Procesa un lote de registros y devuelve instancias válidas de Proveedor"""
    proveedores = []
    used_cuits = set()
    
    for idx, record in enumerate(records):
        try:
            codigo_origen = int(float(record.get('CODIGO', 0)))
            
            # DEBUG: Mostrar primeros 5 registros
            if batch_start + idx < 5:
                print(f"\n[DEBUG] Registro {batch_start + idx + 1}:")
                print(f"  CODIGO: {codigo_origen}")
                print(f"  NOMBRE: {record.get('NOMBRE', '')}")
                print(f"  IVA: '{record.get('IVA', '')}'")
                print(f"  LOCALIDAD: '{record.get('LOCALIDAD', '')}'")
                print(f"  CUIT: {record.get('CUIT', '')}")
            
            # Obtener tipo_iva
            iva_value = record.get('IVA', '').strip() if record.get('IVA') else ''
            tipo_iva = cache['tipos_iva'].get(iva_value) or cache['default_tipo_iva']
            
            if not tipo_iva:
                logger.warning(f"Tipo IVA no válido para registro {codigo_origen}: '{iva_value}'")
                continue
            
            # Obtener localidad
            localidad_value = str(record.get('LOCALIDAD', ''))[:5] if record.get('LOCALIDAD') is not None else ''
            localidad_list = cache['localidades'].get(localidad_value, [])
            
            if localidad_list:
                id_localidad = localidad_list[0]
                id_provincia = id_localidad.id_provincia
            else:
                id_localidad = cache['default_localidad']
                id_provincia = cache['default_provincia']
            
            if not id_localidad or not id_provincia:
                logger.warning(f"Localidad o provincia no válidas para registro {codigo_origen}")
                continue
            
            # Obtener retencion_ib
            retencion_ib_value = str(record.get('IDRETENCION', '')) if record.get('IDRETENCION') is not None else ''
            retencion_ib = cache['retenciones_ib'].get(retencion_ib_value, None)
            
            # Manejo de CUIT
            cuit = int(str(record.get('CUIT', 0)) if record.get('CUIT') is not None else '0')
            current_count = batch_start + idx
            if cuit == 0 or cuit in used_cuits:
                cuit = 99999999999 - current_count
            used_cuits.add(cuit)
            
            # Crear proveedor
            proveedor = Proveedor(
                id_proveedor=codigo_origen,
                estatus_proveedor=True,
                nombre_proveedor=str(record.get('NOMBRE', ''))[:50] if record.get('NOMBRE') else '',
                domicilio_proveedor=str(record.get('DOMICILIO', ''))[:50] if record.get('DOMICILIO') else '',
                codigo_postal=str(record.get('CODPOSTAL', ''))[:5] if record.get('CODPOSTAL') else "00000",
                id_provincia=id_provincia,
                id_localidad=id_localidad,
                id_tipo_iva=tipo_iva,
                cuit=cuit,
                id_tipo_retencion_ib=retencion_ib,
                ib_numero=str(record.get('INGBRUTO', '')) if record.get('INGBRUTO') else "000000000000000",
                ib_exento=record.get('EXENTOIB', False),
                ib_alicuota=float(record.get('ALICIB', 0.00)) if record.get('ALICIB') else 0.00,
                multilateral=record.get('MULTILATERAL', False),
                telefono_proveedor=str(record.get('TELEFONO', ''))[:15] if record.get('TELEFONO') else '',
                movil_proveedor=None,
                email_proveedor=str(record.get('MAIL', ''))[:50] if record.get('MAIL') else '',
                observacion_proveedor=str(record.get('NOTA', '')) if record.get('NOTA') else ''
            )
            proveedores.append(proveedor)
            
            # DEBUG: Mostrar cuando se crea un proveedor
            if batch_start + idx < 5:
                print(f"  ✅ Proveedor {codigo_origen} creado correctamente")
            
        except Exception as e:
            logger.error(f"Error procesando registro {record.get('CODIGO', 'DESCONOCIDO')}: {str(e)}")
            if batch_start + idx < 5:
                print(f"  ❌ Error: {str(e)}")
            continue
            
    return proveedores

def cargar_datos():
    """Función principal de migración con progreso visual"""
    try:
        start_time = time.time()
        last_print_time = start_time
        logger.info("Iniciando migración de proveedores")
        print("\nIniciando migración de proveedores...")
        
        reset_proveedor()
        cache = precargar_relaciones()
        
        batch_size = 1000
        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'proveedor.DBF')
        total_registros = 0
        
        with transaction.atomic():
            print("\nCargando archivo DBF en memoria...")
            records = list(DBF(dbf_path, encoding='latin-1'))
            total_registros_dbf = len(records)
            print(f"DBF cargado. Total registros a procesar: {total_registros_dbf:,}")
            logger.info(f"DBF cargado en memoria. Total registros: {total_registros_dbf}")
            
            # Mostrar primeros registros del DBF
            print("\n[DEBUG] Primeros registros del DBF:")
            for i, record in enumerate(records[:3]):
                print(f"\nRegistro {i+1}:")
                for key, value in list(record.items())[:10]:
                    print(f"  {key}: {value}")
            
            for i in range(0, total_registros_dbf, batch_size):
                batch_records = records[i:i + batch_size]
                proveedores_batch = procesar_lote(batch_records, cache, i)
                
                if proveedores_batch:
                    Proveedor.objects.bulk_create(proveedores_batch)
                    total_registros += len(proveedores_batch)
                
                if i > 0 and i % 1000 == 0:
                    last_print_time = print_progress(i, total_registros_dbf, start_time, last_print_time)
                
                del batch_records
                del proveedores_batch
            
            print_progress(total_registros_dbf, total_registros_dbf, start_time, last_print_time)
            print()
        
        elapsed_time = time.time() - start_time
        logger.info(f"Migración completada. Total registros procesados: {total_registros}/{total_registros_dbf}. Tiempo: {elapsed_time:.2f} segundos")
        
        print(f"\n{'='*50}")
        print(f"Migración finalizada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Registros procesados: {total_registros:,}/{total_registros_dbf:,}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")
        print(f"{'='*50}")
        
    except Exception as e:
        logger.error(f"Error crítico en cargar_datos: {str(e)}")
        print(f"\nERROR: {str(e)}")
        raise

if __name__ == '__main__':
    cargar_datos()
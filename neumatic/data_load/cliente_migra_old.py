# neumatic\data_load\cliente_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from django.db import transaction
from datetime import date

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.cliente_models import Cliente, Vendedor, Sucursal
from apps.maestros.models.base_models import *
from apps.maestros.models.sucursal_models import Localidad, Provincia

# Configurar logging
logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'cliente_migra.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def reset_cliente():
    """Elimina los datos existentes en la tabla Cliente y resetea su ID en SQLite."""
    try:
        with transaction.atomic():
            count = Cliente.objects.count()
            Cliente.objects.all().delete()
            logger.info(f"Eliminados {count} registros existentes de Cliente")
            
            if 'sqlite' in connection.settings_dict['ENGINE']:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='cliente';")
    except Exception as e:
        logger.error(f"Error en reset_cliente: {e}")
        raise

def precargar_relaciones():
    """Precarga todas las relaciones necesarias en diccionarios para optimización"""
    relaciones = {
        'tipos_iva': {
            "CF": TipoIva.objects.get(pk=1),
            "EXE": TipoIva.objects.get(pk=2),
            "RMT": TipoIva.objects.get(pk=3),
            "RI": TipoIva.objects.get(pk=4)
        },
        'tipos_doc': {
            "CI": TipoDocumentoIdentidad.objects.get(pk=2),
            "CUIT": TipoDocumentoIdentidad.objects.get(pk=1),
            "DNI": TipoDocumentoIdentidad.objects.get(pk=5),
            "LC": TipoDocumentoIdentidad.objects.get(pk=6),
            "LE": TipoDocumentoIdentidad.objects.get(pk=6),
            "OTR": TipoDocumentoIdentidad.objects.get(pk=6)
        },
        'vendedores': {v.pk: v for v in Vendedor.objects.all()},
        'actividades': {a.pk: a for a in Actividad.objects.all()},
        'sucursales': {s.pk: s for s in Sucursal.objects.all()},
        'percepciones': {p.pk: p for p in TipoPercepcionIb.objects.all()},
        'localidades': {loc.codigo_postal: loc for loc in Localidad.objects.select_related('id_provincia').all()}
    }
    return relaciones

def procesar_registro(record, cache):
    """Procesa un registro individual con todas las validaciones y campos completos"""
    try:
        # Obtener instancias desde caché
        tipo_iva = cache['tipos_iva'].get(record.get('SITIVA', '').strip())
        tipo_doc = cache['tipos_doc'].get(record.get('TIPODOC', '').strip())
        vendedor = cache['vendedores'].get(int(record.get('VENDEDOR', 0))) if record.get('VENDEDOR') else None
        actividad = cache['actividades'].get(int(record.get('ACTIVIDAD', 0))) if record.get('ACTIVIDAD') else None
        sucursal = cache['sucursales'].get(int(record.get('SUCURSAL', 0))) if record.get('SUCURSAL') else None
        percepcion = cache['percepciones'].get(int(record.get('PERCEPIB', 0))) if record.get('PERCEPIB') else None
        
        # Localidad y provincia
        codigo_postal = str(record.get('CODPOSTAL', ''))[:4] or None
        localidad = cache['localidades'].get(codigo_postal)
        provincia = localidad.id_provincia if localidad else None

        # Manejar fechas
        fecha_alta = record.get('FECHAING')
        if not fecha_alta or str(fecha_alta).strip() == "":
            fecha_alta = None

        # Convertir CODIGO a entero
        try:
            codigo_origen = int(float(record.get('CODIGO', 0)))
        except ValueError:
            logger.warning(f"Valor inválido en CODIGO: {record.get('CODIGO')}. Registro omitido.")
            return None

        # Crear y retornar instancia de Cliente (sin guardar)
        return Cliente(
            id_cliente=codigo_origen,
            estatus_cliente=True,
            codigo_cliente=str(record.get('CODIGO')).strip(),
            nombre_cliente=record.get('NOMBRE', '').strip(),
            domicilio_cliente=record.get('DOMICILIO', '').strip(),
            codigo_postal=codigo_postal,
            id_localidad=localidad,
            id_provincia=provincia,
            tipo_persona=record.get('TIPOCLI', '').strip(),
            id_tipo_iva=tipo_iva,
            id_tipo_documento_identidad=tipo_doc,
            cuit=int(str(record.get('CUIT')).strip()) if record.get('CUIT') else 0,
            condicion_venta=int(record.get('CONVTA', 0)) if record.get('CONVTA') else 0,
            telefono_cliente=record.get('TELEFONO', '').strip() or '',
            fax_cliente=record.get('FAX', '').strip() or '',
            movil_cliente=record.get('MOVIL', '').strip() or '',
            email_cliente=record.get('MAIL', '').strip() or '',
            transporte_cliente=record.get('TRANSPORTE', '').strip() or '',
            id_vendedor=vendedor,
            fecha_nacimiento=record.get('FECHANAC') or None,
            fecha_alta=fecha_alta,
            sexo=int(record.get('SEXO', 0)) if record.get('SEXO') else 0,
            id_actividad=actividad,
            id_sucursal=sucursal,
            id_percepcion_ib=percepcion,
            vip=record.get('VIP', False) or False,
            sub_cuenta=int(record.get('SUBCUENTA')) if record.get('SUBCUENTA') else None,
            black_list=False
        )
        
    except Exception as e:
        logger.error(f"Error procesando registro: {e}")
        return None

def cargar_datos():
    """Función principal de migración con todas las optimizaciones"""
    try:
        start_time = time.time()
        logger.info("Iniciando migración de clientes")
        
        # 1. Resetear datos existentes
        reset_cliente()
        
        # 2. Precargar relaciones
        cache = precargar_relaciones()
        logger.info("Diccionarios de relaciones precargados")
        
        # 3. Configurar procesamiento por lotes
        batch_size = 1000
        clientes_batch = []
        registros_procesados = 0
        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'clientes.DBF')
        
        # 4. Procesar archivo DBF
        for record in DBF(dbf_path, encoding='latin-1'):
            try:
                cliente = procesar_registro(record, cache)
                if cliente:
                    clientes_batch.append(cliente)
                    registros_procesados += 1
                    
                    # Guardar por lotes
                    if len(clientes_batch) >= batch_size:
                        Cliente.objects.bulk_create(clientes_batch)
                        logger.info(f"Lote guardado: {len(clientes_batch)} registros")
                        clientes_batch = []
                        
            except Exception as e:
                logger.error(f"Error procesando registro: {e}")
                continue
                
        # Guardar últimos registros
        if clientes_batch:
            Cliente.objects.bulk_create(clientes_batch)
            logger.info(f"Último lote guardado: {len(clientes_batch)} registros")
            
        # 5. Resultados finales
        elapsed_time = time.time() - start_time
        logger.info(
            f"Migración completada. "
            f"Total registros: {registros_procesados}. "
            f"Tiempo: {elapsed_time:.2f} segundos"
        )
        
        print(f"\nMigración finalizada. Registros procesados: {registros_procesados}")
        print(f"Tiempo total: {elapsed_time:.2f} segundos")
        
    except Exception as e:
        logger.error(f"Error en cargar_datos: {e}")
        raise

if __name__ == '__main__':
    cargar_datos()
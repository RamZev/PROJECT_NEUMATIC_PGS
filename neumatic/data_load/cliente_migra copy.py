# neumatic\data_load\cliente_migra.py
import os
import sys
import django
import time  # Para medir el tiempo de procesamiento
from dbfread import DBF
from django.db import connection
from datetime import date
from django.db import transaction

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.cliente_models import Cliente, Vendedor, Sucursal
from apps.maestros.models.base_models import *
from apps.maestros.models.sucursal_models import Localidad, Provincia

def reset_cliente():
    """Elimina los datos existentes en la tabla Cliente y resetea su ID en SQLite."""
    Cliente.objects.all().delete()  # Eliminar los datos existentes
    
    # Reiniciar el autoincremento en SQLite
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='cliente';")

def obtener_instancia(modelo, valor, default=None):
    """Obtiene una instancia de modelo por pk o retorna None."""
    if not valor:
        return default
    try:
        return modelo.objects.get(pk=valor)
    except modelo.DoesNotExist:
        return default

def procesar_registro(record):
    """Procesa un registro individual de la tabla DBF."""
    tipos_iva = {
        "CF": 1,
        "EXE": 2,
        "RMT": 3,
        "RI": 4
    }
    
    tipos_doc_id = {
        "CI": 2,
        "CUIT": 1,
        "DNI":5,
        "LC":6,
        "LE":6
    }
    
    id_tipo_iva = tipos_iva[record.get('SITIVA').strip()]
    id_tipo_doc = tipos_doc_id[record.get('TIPODOC').strip()]
    
    try:
        # Claves foráneas
        id_tipo_iva_instancia = obtener_instancia(TipoIva, id_tipo_iva)
        id_tipo_documento_identidad_instancia = obtener_instancia(TipoDocumentoIdentidad, id_tipo_doc)
        id_vendedor_instancia = obtener_instancia(Vendedor, record.get('VENDEDOR'))
        id_actividad_instancia = obtener_instancia(Actividad, record.get('ACTIVIDAD'))
        id_sucursal_instancia = obtener_instancia(Sucursal, record.get('SUCURSAL'))
        id_percepcion_ib_instancia = obtener_instancia(TipoPercepcionIb, record.get('PERCEPIB'))

        # Localidad y provincia
        codigo_postal = str(record.get('CODPOSTAL', ''))[:4] or None
        localidad = Localidad.objects.filter(codigo_postal=codigo_postal).first() if codigo_postal else None
        id_localidad_instancia = localidad if localidad else None
        id_provincia_instancia = localidad.id_provincia if localidad else None

        # Manejar fecha alta
        fecha_alta = record.get('FECHAING')
        if not fecha_alta or str(fecha_alta).strip() == "":
            fecha_alta = None

        # Convertir CODIGO a entero, manejando valores decimales
        codigo_origen = record.get('CODIGO', 0)
        try:
            codigo_origen = int(float(codigo_origen))
        except ValueError:
            print(f"Advertencia: Valor inválido en CODIGO: {codigo_origen}. Registro omitido.")
            return

        # Crear cliente
        Cliente.objects.create(
            id_cliente=codigo_origen,
            estatus_cliente=True,
            codigo_cliente=str(record.get('CODIGO')).strip(),
            nombre_cliente=record.get('NOMBRE', '').strip(),
            domicilio_cliente=record.get('DOMICILIO', '').strip(),
            codigo_postal=codigo_postal,
            id_localidad=id_localidad_instancia,
            id_provincia=id_provincia_instancia,
            tipo_persona=record.get('TIPOCLI', '').strip(),
            id_tipo_iva=id_tipo_iva_instancia,
            id_tipo_documento_identidad=id_tipo_documento_identidad_instancia,
            cuit=int(str(record.get('CUIT')).strip()) if record.get('CUIT') else 0,
            condicion_venta=int(record.get('CONVTA', 0)) if record.get('CONVTA') else 0,
            telefono_cliente=record.get('TELEFONO', '').strip() or '',
            fax_cliente=record.get('FAX', '').strip() or '',
            movil_cliente=record.get('MOVIL', '').strip() or '',
            email_cliente=record.get('MAIL', '').strip() or '',
            transporte_cliente=record.get('TRANSPORTE', '').strip() or '',
            id_vendedor=id_vendedor_instancia,
            fecha_nacimiento=record.get('FECHANAC') or None,
            fecha_alta=fecha_alta,
            sexo=int(record.get('SEXO', 0)) if record.get('SEXO') else 0,
            id_actividad=id_actividad_instancia,
            id_sucursal=id_sucursal_instancia,
            id_percepcion_ib=id_percepcion_ib_instancia,
            vip=record.get('VIP', False) or False,
            sub_cuenta=int(record.get('SUBCUENTA')) if record.get('SUBCUENTA') else None,
            black_list=False,
        )
    except Exception as e:
        print(f"Error procesando el registro: {e}")

def cargar_datos():
    """Carga datos desde la tabla DBF al modelo Cliente."""
    reset_cliente()
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'clientes.DBF')
    table = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda x: x['CODIGO'])
    table = {record['CODIGO']: record for record in table}.values()

    registros_procesados = 0
    lote = 1000  # Procesar registros en lotes de 100

    for idx, record in enumerate(table):
        try:
            procesar_registro(record)
            registros_procesados += 1

            # Mostrar progreso cada 100 registros
            if registros_procesados % lote == 0:
                print(f"{registros_procesados} registros procesados y guardados.")

        except Exception as e:
            print(f"Error al procesar el registro {idx + 1}: {e}. Registro omitido.")

    print(f"Total de registros procesados: {registros_procesados}.")

if __name__ == '__main__':
    start_time = time.time()  # Empezar el control de tiempo
    cargar_datos()
    end_time = time.time()  # Terminar el control de tiempo

    # Calcular el tiempo total en minutos y segundos
    elapsed_time = end_time - start_time
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60

    print(f"Migración de Cliente completada.")
    print(f"Tiempo de procesamiento: {int(minutes)} minutos y {int(seconds)} segundos.")

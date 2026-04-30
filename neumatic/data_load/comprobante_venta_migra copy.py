import os
import sys
import django
from dbfread import DBF
from django.db import connection

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import ComprobanteVenta  # Asegúrate de que esta ruta sea la correcta

def cargar_comprobantes_desde_dbf(archivo_dbf):
    """Carga los datos de comprobantes desde un archivo DBF y los migra al modelo ComprobanteVenta."""
    
    # Abrir la tabla DBF y leer su contenido
    dbf_table = DBF(archivo_dbf, load=True)

    # Resetear la tabla ComprobanteVenta (eliminar los datos existentes)
    reset_comprobantes()

    # Iterar sobre cada registro de la tabla DBF
    for record in dbf_table:
        # Crear el registro en la base de datos
        ComprobanteVenta.objects.create(
            estatus_comprobante_venta=True,  # Asignar True por defecto
            codigo_comprobante_venta=record['CODIGO'].strip(),
            nombre_comprobante_venta=record['NOMBRE'].strip(),
            mult_venta=record['MULT_VEN'] if record['MULT_VEN'] is not None else 0,
            mult_saldo=record['MULT_CLI'] if record['MULT_CLI'] is not None else 0,
            mult_stock=record['MULT_STO'] if record['MULT_STO'] is not None else 0,
            mult_comision=record['MULT_COM'] if record['MULT_COM'] is not None else 0,
            mult_caja=record['MULT_CAJA'] if record['MULT_CAJA'] is not None else 0,
            mult_estadistica=record['MULT_STAD'] if record['MULT_STAD'] is not None else 0,
            libro_iva=record['LIBROIVA'] if record['LIBROIVA'] is not None else False,
            estadistica=record['ESTADISTIC'] if record['ESTADISTIC'] is not None else False,
            electronica=record['ELECTRONIC'] if record['ELECTRONIC'] is not None else False,
            presupuesto=record['PRESUPUEST'] if record['PRESUPUEST'] is not None else False,
            pendiente=record['PENDIENTE'] if record['PENDIENTE'] is not None else False,
            info_michelin_auto=record['XTRAXTORA'] if record['XTRAXTORA'] is not None else False,
            info_michelin_camion=record['XTRAXTORC'] if record['XTRAXTORC'] is not None else False,
            codigo_afip_a=record['CODCITIA'].strip() if record['CODCITIA'] is not None else '',
            codigo_afip_b=record['CODCITIB'].strip() if record['CODCITIB'] is not None else '',
            remito=record['REMITO'] if record['REMITO'] is not None else False,
            recibo=record['RECIBO'] if record['RECIBO'] is not None else False,
            manual=record['MANUAL'] if record['MANUAL'] is not None else False,
            mipyme=record['MIPYME'] if record['MIPYME'] is not None else False,
            ncr_ndb=record['NCR_NDB'] if record['NCR_NDB'] is not None else False,
        )

    print(f"Se han migrado {len(dbf_table)} comprobantes de forma exitosa.")

def reset_comprobantes():
    """Elimina los datos existentes en la tabla ComprobanteVenta y resetea su ID."""
    # Eliminar los datos existentes en la tabla
    ComprobanteVenta.objects.all().delete()

    # Reiniciar el autoincremento en la base de datos
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='comprobante_venta';")

    print("Datos de la tabla ComprobanteVenta eliminados y autoincremento reseteado.")

if __name__ == '__main__':
    # Ruta del archivo DBF
    archivo_dbf = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'codven.dbf')

    # Ejecutar la migración
    cargar_comprobantes_desde_dbf(archivo_dbf)

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

from apps.maestros.models.base_models import ComprobanteCompra

def cargar_comprobantes_compra_desde_dbf(archivo_dbf):
    """Carga los datos de comprobantes de compra desde un archivo DBF y los migra al modelo ComprobanteCompra."""
    
    # Abrir la tabla DBF y leer su contenido
    dbf_table = DBF(archivo_dbf, load=True)

    # Resetear la tabla ComprobanteCompra (eliminar los datos existentes)
    reset_comprobantes_compra()

    # Iterar sobre cada registro de la tabla DBF
    for record in dbf_table:
        # Crear el registro en la base de datos
        ComprobanteCompra.objects.create(
            estatus_comprobante_compra=True,  # Asignar True por defecto
            codigo_comprobante_compra=record['CODIGO'].strip(),
            nombre_comprobante_compra=record['NOMBRE'].strip(),
            mult_compra=record['MULT_COM'] if record['MULT_COM'] is not None else 0,
            mult_saldo=record['MULT_PRO'] if record['MULT_PRO'] is not None else 0,
            mult_stock=record['MULT_STO'] if record['MULT_STO'] is not None else 0,
            mult_caja=record['MULT_CAJA'] if record['MULT_CAJA'] is not None else 0,
            libro_iva=record['LIBROIVA'] if record['LIBROIVA'] is not None else False,
            codigo_afip_a=str(record['CODAFIP']).strip() if record['CODAFIP'] is not None else '',
            codigo_afip_b=str(record['CODAFIPB']).strip() if record['CODAFIPB'] is not None else '',
            codigo_afip_c=str(record['CODAFIPC']).strip() if record['CODAFIPC'] is not None else '',
            codigo_afip_m=''  # Asignar False (campo de tipo CharField, por lo que lo dejamos vacío)
        )

    print(f"Se han migrado {len(dbf_table)} comprobantes de compra de forma exitosa.")

def reset_comprobantes_compra():
    """Elimina los datos existentes en la tabla ComprobanteCompra y resetea su ID."""
    # Eliminar los datos existentes en la tabla
    ComprobanteCompra.objects.all().delete()

    # Detectar el motor de base de datos
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            # SQLite: reiniciar secuencia
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='comprobante_compra';")
            print("Autoincremento reseteado (SQLite).")
        elif 'mssql' in engine or 'sql_server' in engine:
            # SQL Server: reiniciar identity
            cursor.execute("DBCC CHECKIDENT ('comprobante_compra', RESEED, 0);")
            print("Autoincremento reseteado (SQL Server).")
        else:
            print(f"Motor {engine} - No se requiere reset automático de secuencia.")

    print("Datos de la tabla ComprobanteCompra eliminados.")

if __name__ == '__main__':
    # Ruta del archivo DBF
    archivo_dbf = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'codcom.dbf')

    # Ejecutar la migración
    cargar_comprobantes_compra_desde_dbf(archivo_dbf)

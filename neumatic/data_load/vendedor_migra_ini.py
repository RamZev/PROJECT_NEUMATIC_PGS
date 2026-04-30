import os
import sys
import django
import time  # Para medir el tiempo de procesamiento
from dbfread import DBF
from django.db import connection
from datetime import date

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

# Importación de los modelos
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.vendedor_models import Vendedor


tabla_origen = 'vendedor.DBF'

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', tabla_origen)

# Abrir la tabla de Visual FoxPro usando dbfread
table = DBF(dbf_path, encoding='latin-1')

# Rango de registros 
codigo_inicio = 1
codigo_final = None     # Hasta el final

# Nombre de variable id en la tabla origen
codigo_id = "CODIGO"

# Filtrar y ordenar la tabla DBF
table = sorted(
    [
        record
        for record in table
        if int(record.get(codigo_id, 0)) >= codigo_inicio and 
           (codigo_final is None or int(record.get(codigo_id, 0)) <= codigo_final)
    ],
    key=lambda record: int(record.get(codigo_id, 0))
)

total_registros = len(table)
print(f"Total de registros a procesar: {total_registros}")

# Datos de ajuste


# Ejemplos base para asignar valores 
''' 
    record.get('NOMBRE', '').strip(),   # String
    int(record.get('MICHELIN', 0)),     # Integer
    float(record.get('EXENTO') or 0)    # Float
    record.get('INICIOACT', None)       # Date
    bool(record.get('PROMO', False))    # Boolean
'''

# Procesar registros
for idx, record in enumerate(table):
    id_origen = int(record.get(codigo_id, 0))
    print(f"Procesando vendedor con ID: {id_origen}")

    # Validar sucursal
    pk_sucursal = int(record.get('SUCURSAL', 0))
    try:
        id_sucursal_instancia = Sucursal.objects.get(pk=pk_sucursal)
    except Sucursal.DoesNotExist:
        print(f"Sucursal con ID {pk_sucursal} no encontrada. Saltando registro.")
        continue

    # Evitar duplicados
    if Vendedor.objects.filter(id_vendedor=id_origen).exists():
        print(f"Vendedor con ID {id_origen} ya existe. Saltando registro.")
        continue

    # Crear registro
    try:
        Vendedor.objects.create(
            id_vendedor=id_origen,
            estatus_vendedor=True,
            nombre_vendedor=record.get('NOMBRE', '').strip(),
            domicilio_vendedor=record.get('DOMICILIO', '').strip(),
            email_vendedor="sin-email@dominio.com",
            telefono_vendedor="sin-telefono",
            pje_auto=float(record.get('PORCENTAJE') or 0),
            pje_camion=float(record.get('PJECAMION') or 0),
            vence_factura=int(record.get('DIASGRACIA', 0)),
            vence_remito=int(record.get('DIASRTOS', 0)),
            id_sucursal=id_sucursal_instancia,
            tipo_venta=record.get('TIPO', '').strip(),
            col_descuento=float(record.get('DESCOL') or 0),
            email_venta=bool(record.get('EMAILFAC', False)),
            info_saldo=bool(record.get('EMAILSDO', False)),
            info_estadistica=bool(record.get('EMAILEST', False)),
        )
        print(f"Vendedor con ID {id_origen} creado exitosamente.")
    except Exception as e:
        print(f"Error al crear vendedor con ID {id_origen}: {e}")
        continue
    
print("La migración terminó con éxito!")

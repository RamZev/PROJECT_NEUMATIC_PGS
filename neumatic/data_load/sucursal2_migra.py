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
from apps.maestros.models.base_models import Provincia, Localidad
from apps.maestros.models.sucursal_models import Sucursal

# Ruta de la tabla de Visual FoxPro
dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'sucursal.DBF')

# Abrir la tabla de Visual FoxPro usando dbfread
table = DBF(dbf_path, encoding='latin-1')

total_registros = len(table)
print(f"Total de registros a procesar: {total_registros}")

codigo_inicio = 1
# codigo_final = None
codigo_final = 10

# Filtrar y ordenal la tabla DBF
# Filtrar y ordenar la tabla DBF
table = sorted(
    [
        record
        for record in table
        if int(record.get('ID', 0)) >= codigo_inicio and 
           (codigo_final is None or int(record.get('ID', 0)) <= codigo_final)
    ],
    key=lambda record: int(record.get('ID', 0))
)

# Datos de ajuste
sucursales = {
    1: {"id_provincia": 13, "id_localidad": 2349, "codigo_postal": "3040"},
    2: {"id_provincia": 13, "id_localidad": 2202, "codigo_postal": "3000"},
    3: {"id_provincia": 6, "id_localidad": 2574, "codigo_postal": "3100"},
    4: {"id_provincia": 13, "id_localidad": 909, "codigo_postal": "2000"},
    5: {"id_provincia": 13, "id_localidad": 2289, "codigo_postal": "3018"},
    6: {"id_provincia": 13, "id_localidad": 1043, "codigo_postal": "2152"},
    7: {"id_provincia": 13, "id_localidad": 1170, "codigo_postal": "2300"},
    8: {"id_provincia": 13, "id_localidad": 5658, "codigo_postal": "3560"},
    9: {"id_provincia": 13, "id_localidad": 1043, "codigo_postal": "2152"},
    10: {"id_provincia": 13, "id_localidad": 2202, "codigo_postal": "3000"},
}

for idx, record in enumerate(table):
    # Extraer y procesar los datos según las reglas
    
    ##################################
    # Código ID origen y tabla destino
    
    # Obtener el código de la tabla origen
    codigo_origen = int(record.get("ID", 0))
    print("codigo_origen", codigo_origen)

    # Definir el marcador de posición (id)
    # nuevo_id = codigo_origen - 1
    # sql_consult = f"UPDATE sqlite_sequence SET seq = {nuevo_id} WHERE name = 'sucursal';"
    
    # Reiniciar el autoincremento en la tabla destino
    # with connection.cursor() as cursor:
    #     cursor.execute(sql_consult)
    ##################################
    
    pk_provincia = sucursales[idx+1]["id_provincia"]
    pk_localidad = sucursales[idx+1]["id_localidad"]
    
    Sucursal.objects.create(
        id_sucursal = codigo_origen,
        estatus_sucursal=True,
        nombre_sucursal = record.get('NOMBRE', '').strip(),
        codigo_michelin = int(record.get('MICHELIN', 0)),
        domicilio_sucursal = record.get('DOMICILIO', '').strip(),

        codigo_postal = sucursales[idx+1]["codigo_postal"],
        id_provincia = Provincia.objects.get(pk=pk_provincia),
        id_localidad = Localidad.objects.get(pk=pk_localidad),
        
        telefono_sucursal = record.get('TELEFONO', '').strip(),
        email_sucursal = record.get('EMAIL', '').strip(),
        inicio_actividad = record.get('INICIOACT', None)
            
    )
    
   
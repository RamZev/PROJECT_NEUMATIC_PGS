# neumatic\data_load\operario_migra.py
import os
import sys
import django
import time  # Para medir el tiempo de procesamiento
from dbfread import DBF
from django.db import connection
from datetime import date
from django.conf import settings  # ← NUEVA IMPORTACIÓN

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

# Importación de los modelos
from apps.maestros.models.base_models import Operario

# ============================================================
# FUNCIÓN RESET (NUEVA)
# ============================================================
def reset_operario():
    """Elimina los datos existentes en la tabla Operario y resetea su ID."""
    Operario.objects.all().delete()
    print("Tabla Operario limpiada.")

    # Detectar el motor de base de datos
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='operario';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('operario', 'id_operario'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('operario', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE operario AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

# ============================================================
# MIGRACIÓN PRINCIPAL
# ============================================================

# Tabla origen y modelo destino
tabla_origen = 'operario.DBF'
modelo_dest = Operario

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
print(f"{tabla_origen}: Total de registros a procesar: {total_registros}")

# ============================================================
# RESET ANTES DE PROCESAR (NUEVO)
# ============================================================
reset_operario()

# ============================================================
# PROCESAR REGISTROS
# ============================================================

for idx, record in enumerate(table):
    id_origen = int(record.get(codigo_id, 0))

    # Crear registro (ya no es necesario verificar duplicados porque la tabla está vacía)
    try:
        modelo_dest.objects.create(
            id_operario=id_origen,
            estatus_operario=True,
            nombre_operario=record.get('NOMBRE', '').strip(),
            telefono_operario="sin-telefono",
            email_operario="sin-email@dominio.com",
        )
        print(f"{tabla_origen} con ID {id_origen} creado exitosamente.")
    except Exception as e:
        print(f"Error al crear {tabla_origen} con ID {id_origen}: {e}")
        continue
    
print(f"La migración de la tabla {tabla_origen} terminó con éxito!")
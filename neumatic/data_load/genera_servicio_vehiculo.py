# neumatic/data_load/genera_servicio_vehiculo.py
import csv
import dbf
import os
from datetime import datetime

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_dbf = os.path.join(BASE_DIR, 'datavfox', 'vehiculo2.dbf') # Ajusta si el DBF está en otra ruta
ruta_csv_salida = os.path.join(BASE_DIR, 'servicio_vehiculo.csv')

def leer_campo(reg, campos_dbf, nombre, default=''):
    """Lee un campo del DBF de forma segura."""
    if nombre in campos_dbf:
        valor = getattr(reg, nombre)
        return str(valor).strip() if valor is not None else default
    return default

def formatear_fecha(fecha_str):
    """Convierte fechas de VFP (DD/MM/YYYY o datetime) a YYYY-MM-DD."""
    if not fecha_str or fecha_str == 'null':
        return ''
    try:
        # Si viene con formato de VFP (ej. 16/10/2026)
        if '/' in fecha_str:
            parts = fecha_str.split('/')
            if len(parts) == 3:
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
        # Si viene como string de datetime
        elif '-' in fecha_str:
            return fecha_str[:10] # Tomar solo YYYY-MM-DD
    except:
        pass
    return ''

print("Generando servicio_vehiculo.csv desde vehiculo2.dbf...")

try:
    tabla = dbf.Table(ruta_dbf, codepage='cp1252')
    
    with open(ruta_csv_salida, mode='w', encoding='utf-8', newline='') as f_out:
        escritor = csv.writer(f_out, delimiter=';')
        
        # Cabecera exacta del modelo Django ServicioVehiculo
        escritor.writerow([
            'id_servicio_vehiculo', 'estatus_servicio_vehiculo', 
            'id_cliente', 'id_vehiculo', 
            'kmxmes', 'proxima_visita', 'observaciones'
        ])
        
        with tabla:
            campos_dbf = tabla.field_names
            contador_vehiculo = 1  # Debe coincidir con el ID generado en vehiculo.csv
            contador_servicio = 1  # ID para el servicio
            
            for reg in tabla:
                # Validar si tiene marca asignada (misma regla que vehiculo.csv)
                id_marca = reg.ID_MARCA if 'ID_MARCA' in campos_dbf else (reg.id_marca if 'id_marca' in campos_dbf else 0)
                if id_marca == 0:
                    continue

                # Datos del DBF
                cliente = leer_campo(reg, campos_dbf, 'CLIENTE')
                kmxmes = leer_campo(reg, campos_dbf, 'KMXMES', leer_campo(reg, campos_dbf, 'KMUMES', ''))
                visita = leer_campo(reg, campos_dbf, 'VISITA')
                observacion = leer_campo(reg, campos_dbf, 'OBSERVACIO', leer_campo(reg, campos_dbf, 'OBSERVACION', ''))

                # Si el cliente está vacío, no podemos crear el servicio (el modelo requiere FK)
                if not cliente or cliente == '0':
                    contador_vehiculo += 1
                    continue

                # Corregir kilometraje negativo
                if kmxmes:
                    try:
                        kmxmes_int = int(kmxmes)
                        kmxmes = str(abs(kmxmes_int))
                    except ValueError:
                        kmxmes = ''

                # Formatear fecha
                proxima_visita = formatear_fecha(visita)

                escritor.writerow([
                    contador_servicio,
                    'True',          # estatus
                    int(cliente),    # id_cliente
                    contador_vehiculo, # id_vehiculo
                    kmxmes,
                    proxima_visita,
                    observacion
                ])
                
                contador_servicio += 1
                contador_vehiculo += 1

    print(f"✅ Archivo generado: {ruta_csv_salida} con {contador_servicio - 1} registros.")
    
except Exception as e:
    print(f"❌ Error al generar servicio_vehiculo.csv: {e}")
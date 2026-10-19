# neumatic/data_load/datavfox/generar_csv_finales_veh2.py
import csv
import dbf
import os
import re
from datetime import datetime

# =====================================================================
# CONFIGURACIÓN DE RUTAS
# =====================================================================
ruta_auditoria_marcas = 'auditoria_mapeo_marcas.csv'
ruta_auditoria_modelos = 'auditoria_modelos.csv'
ruta_dbf = 'vehiculo2.dbf'

ruta_csv_marca = 'marca_vehiculo.csv'
ruta_csv_modelo = 'modelo_vehiculo.csv'
ruta_csv_vehiculo = 'vehiculo.csv'

def limpiar_texto(texto):
    if not texto: return ''
    return str(texto).strip()

# =====================================================================
# 1. GENERAR marca_vehiculo.csv
# =====================================================================
print("1. Generando marca_vehiculo.csv...")
try:
    with open(ruta_auditoria_marcas, mode='r', encoding='utf-8') as f_in, \
         open(ruta_csv_marca, mode='w', encoding='utf-8', newline='') as f_out:
        
        lector = csv.reader(f_in)
        next(lector) # Saltar cabecera original
        escritor = csv.writer(f_out, delimiter=';')
        
        # Cabecera Django
        escritor.writerow(['id_marca_vehiculo', 'estatus_marca_vehiculo', 'marca_vehiculo'])
        
        for fila in lector:
            id_marca = fila[0]
            nombre_marca = fila[1]
            # Escribimos: ID, True, Nombre
            escritor.writerow([id_marca, 'True', nombre_marca])
    print("   ✅ marca_vehiculo.csv generado.")
except Exception as e:
    print(f"   ❌ Error generando marca_vehiculo.csv: {e}")

# =====================================================================
# 2. GENERAR modelo_vehiculo.csv
# =====================================================================
print("2. Generando modelo_vehiculo.csv...")
try:
    with open(ruta_auditoria_modelos, mode='r', encoding='utf-8') as f_in, \
         open(ruta_csv_modelo, mode='w', encoding='utf-8', newline='') as f_out:
        
        lector = csv.reader(f_in)
        next(lector) # Saltar cabecera
        escritor = csv.writer(f_out, delimiter=';')
        
        # Cabecera Django
        escritor.writerow(['id_modelo_vehiculo', 'id_marca_vehiculo', 'estatus_modelo_vehiculo', 'modelo_vehiculo'])
        
        registros_unicos = set() # Para evitar duplicar el mismo modelo base
        
        for fila in lector:
            id_modelo = fila[0]
            id_marca = fila[1]
            modelo_base = fila[3] # Columna 'Modelo Base'
            
            # Evitar duplicados (porque el CSV de auditoría tiene una fila por cada error original)
            if id_modelo not in registros_unicos:
                registros_unicos.add(id_modelo)
                escritor.writerow([id_modelo, id_marca, 'True', modelo_base])
    print("   ✅ modelo_vehiculo.csv generado.")
except Exception as e:
    print(f"   ❌ Error generando modelo_vehiculo.csv: {e}")

# =====================================================================
# 3. GENERAR vehiculo.csv desde el DBF
# =====================================================================
print("3. Generando vehiculo.csv desde el DBF...")
try:
    tabla = dbf.Table(ruta_dbf, codepage='cp1252')
    
    with open(ruta_csv_vehiculo, mode='w', encoding='utf-8', newline='') as f_out:
        escritor = csv.writer(f_out, delimiter=';')
        
        # Cabecera Django
        escritor.writerow([
            'id_vehiculo', 'estatus_vehiculo', 'tipo_vehiculo', 
            'id_marca_vehiculo', 'id_modelo_vehiculo', 'segmento', 
            'anio', 'patente', 'kmxmes', 'visita', 'exportado', 'observacion'
        ])
        
        with tabla:
            contador = 1
            # Obtenemos la lista exacta de nombres de campos en el DBF
            campos_dbf = tabla.field_names
            
            for reg in tabla:
                # Lectura segura de IDs
                id_marca = reg.ID_MARCA if 'ID_MARCA' in campos_dbf else (reg.id_marca if 'id_marca' in campos_dbf else 0)
                id_modelo = reg.ID_MODELO if 'ID_MODELO' in campos_dbf else (reg.id_modelo if 'id_modelo' in campos_dbf else 0)
                
                if id_marca == 0: continue # Ignorar si no tiene marca asignada
                
                # Función auxiliar para leer campos de forma segura y convertir MEMO a string
                def leer_campo(nombre, default=''):
                    if nombre in campos_dbf:
                        valor = getattr(reg, nombre)
                        return str(valor).strip() if valor is not None else default
                    return default

                # Extraer datos usando la función segura
                segmento = leer_campo('SEGMENTO')
                patente = leer_campo('PATENTE')
                anio = leer_campo('ANIO')
                kmxmes = leer_campo('KMXMES', leer_campo('KMUMES', '')) 
                visita = leer_campo('VISITA')
                exportado = leer_campo('EXPORTADO', 'False')
                # El campo se llama OBSERVACIO (truncado por VFP)
                observacion = leer_campo('OBSERVACIO', leer_campo('OBSERVACION', ''))

                # Normalizar el booleano de exportado
                exportado_bool = 'True' if exportado.lower() in ['true', 't', '1'] else 'False'
                    
                # Normalizar la fecha si viene de VFP como DD/MM/YYYY
                if '/' in visita:
                    try:
                        parts = visita.split('/')
                        if len(parts) == 3:
                            # VFP suele guardar como DD/MM/YYYY
                            visita = f"{parts[2]}-{parts[1]}-{parts[0]}"
                    except:
                        pass
                
                escritor.writerow([
                    contador,       # id_vehiculo
                    'True',         # estatus_vehiculo
                    1,              # tipo_vehiculo (default)
                    id_marca,       # id_marca_vehiculo
                    id_modelo,      # id_modelo_vehiculo
                    segmento[:3],   # segmento
                    anio,           # anio
                    patente,        # patente
                    kmxmes,         # kmxmes
                    visita,         # visita
                    exportado_bool, # exportado
                    observacion     # observacion
                ])
                contador += 1
    print(f"   ✅ vehiculo.csv generado con {contador - 1} registros.")
except Exception as e:
    print(f"   ❌ Error generando vehiculo.csv: {e}")

print("\n¡Proceso de generación de CSV finalizado!")
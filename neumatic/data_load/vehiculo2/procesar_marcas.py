import csv
import re
import dbf
import os
from thefuzz import fuzz

# =====================================================================
# 1. CONFIGURACIÓN INICIAL
# =====================================================================
ruta_csv_entrada = 'reporte_marcas.csv'
ruta_csv_unicas = 'auditoria_mapeo_marcas.csv'           
ruta_csv_detalle = 'auditoria_detalle_completo.csv'      
ruta_dbf = 'vehiculo2.dbf' # Asegúrate de que esté en la misma carpeta

ALIAS_MANUALES = {
    'VW': 'VOLKSWAGEN',
    'V.W.': 'VOLKSWAGEN',
    'WV': 'VOLKSWAGEN',             
    'VW 11180': 'VOLKSWAGEN',       
    'VW 17220': 'VOLKSWAGEN',       
    'VW AMAROK': 'VOLKSWAGEN',      
    'VW GOL': 'VOLKSWAGEN',         
    'VW R175': 'VOLKSWAGEN',        
    'VW SHARON': 'VOLKSWAGEN',      
    'VW TIGUAN': 'VOLKSWAGEN',      
    'VW UP': 'VOLKSWAGEN',          
    'VWW': 'VOLKSWAGEN',            
    'WV TAOS': 'VOLKSWAGEN',
    'MB': 'MERCEDES BENZ',
    'MBENZ': 'MERCEDES BENZ',       
    'MBEZ': 'MERCEDES BENZ',        
    'M BENZ': 'MERCEDES BENZ',
    'ME BENZ': 'MERCEDES BENZ',     
    'MERCEDEZ': 'MERCEDES BENZ',    
    'MECEDEZ': 'MERCEDES BENZ',     
    'MERDECEZ': 'MERCEDES BENZ',    
    'BMENZ': 'MERCEDES BENZ',
    'DOGGE': 'DODGE',               
    'DOGGE JOURNEY': 'DODGE',       
    'DOGE': 'DODGE',                
    'DODGGE': 'DODGE',  
    'F100': 'FORD',                 
    'BEIGING': 'BEIJING',           
    'BEIJINNG': 'BEIJING',          
    'BEIJING': 'BEIJING',
    'MINI': 'MINI COOPER',          
    'NIZZAN': 'NISSAN',             
    'RENO': 'RENAULT',              
    'RENSULD': 'RENAULT',           
    'REUAULD': 'RENAULT',           
    'RENUALD': 'RENAULT',           
    'REANULD': 'RENAULT',           
    'REANULT': 'RENAULT',           
    'REBAUKT': 'RENAULT',           
    'TO': 'TOYOTA',                 
    'VMW': 'BMW',                   
    'CRYSLER': 'CHRYSLER',          
    'CITROEN C3': 'CITROEN',
    'CITROEN C4': 'CITROEN',
    'CHEVROLET ONIX': 'CHEVROLET',
    'FORD RANGER': 'FORD',
    'TOYOTA HILUX': 'TOYOTA',
    'TOYOTA COROLLA': 'TOYOTA',
}

# =====================================================================
# 2. LEER Y LIMPIAR EL CSV
# =====================================================================
def limpiar_texto(texto):
    texto = str(texto).upper()
    texto = re.sub(r'[^A-Z0-9ÁÉÍÓÚÑ\s]', '', texto) 
    texto = re.sub(r'\s+', ' ', texto) 
    return texto.strip()

datos_originales = []
try:
    with open(ruta_csv_entrada, mode='r', encoding='cp1252') as f:
        lector = csv.reader(f)
        next(lector)
        for fila in lector:
            if len(fila) >= 2:
                datos_originales.append({'original': fila[0], 'cantidad': int(fila[1])})
except FileNotFoundError:
    print(f"❌ Error: No se encontró {ruta_csv_entrada}")
    exit()

datos_originales.sort(key=lambda x: x['cantidad'], reverse=True)

# =====================================================================
# 3. ALGORITMO DE AGRUPACIÓN
# =====================================================================
marcas_base = []
mapeo_final = {}

for item in datos_originales:
    orig = item['original']
    cant = item['cantidad']
    limpia = limpiar_texto(orig)
    
    if not limpia:
        nombre_base = 'DESCONOCIDO'
    elif limpia in ALIAS_MANUALES:
        nombre_base = ALIAS_MANUALES[limpia]
    elif limpia.startswith('VW ') or limpia.startswith('WV '):
        nombre_base = 'VOLKSWAGEN'
    else:
        nombre_base = None

    if nombre_base:
        mapeo_final[orig] = nombre_base
        encontrado = False
        for mb in marcas_base:
            if mb['nombre'] == nombre_base:
                mb['total'] += cant
                encontrado = True
                break
        if not encontrado:
            marcas_base.append({'nombre': nombre_base, 'total': cant})
        continue

    encontrado_por_subcadena = False
    for mb in marcas_base:
        if len(mb['nombre']) > 3 and mb['nombre'] in limpia:
            mapeo_final[orig] = mb['nombre']
            mb['total'] += cant
            encontrado_por_subcadena = True
            break
    if encontrado_por_subcadena:
        continue

    mejor_match = None
    mejor_score = 0
    for mb in marcas_base:
        score = fuzz.ratio(limpia, mb['nombre'])
        if score > mejor_score:
            mejor_score = score
            mejor_match = mb

    umbral = 85 if (mejor_match and len(mejor_match['nombre']) <= 3) else 75

    if mejor_match and mejor_score >= umbral:
        mapeo_final[orig] = mejor_match['nombre']
        mejor_match['total'] += cant
    else:
        mapeo_final[orig] = limpia
        marcas_base.append({'nombre': limpia, 'total': cant})

# =====================================================================
# 4. ASIGNAR IDs CONSECUTIVOS
# =====================================================================
marcas_base.sort(key=lambda x: x['nombre'])
for i, mb in enumerate(marcas_base, start=1):
    mb['id'] = i

# Diccionario indexado por el TEXTO LIMPIO (para cruzar con el DBF sin errores)
resultado_mapeo_limpio = {}
for orig, nombre_base in mapeo_final.items():
    id_asignado = 0
    for mb in marcas_base:
        if mb['nombre'] == nombre_base:
            id_asignado = mb['id']
            break
    resultado_mapeo_limpio[limpiar_texto(orig)] = id_asignado

# =====================================================================
# 5. GENERAR ARCHIVOS CSV (Auditoría)
# =====================================================================
print("🔍 Generando archivos de auditoría...")

datos_detalle = []
for item in datos_originales:
    orig = item['original']
    id_asig = resultado_mapeo_limpio[limpiar_texto(orig)]
    base_nombre = next((mb['nombre'] for mb in marcas_base if mb['id'] == id_asig), 'N/A')
    datos_detalle.append({'id': id_asig, 'base': base_nombre, 'original': orig, 'cantidad': item['cantidad']})

datos_detalle.sort(key=lambda x: (x['id'], -x['cantidad']))
with open(ruta_csv_detalle, mode='w', encoding='utf-8', newline='') as f:
    escritor = csv.writer(f)
    escritor.writerow(['ID Asignado', 'Marca Base Estandarizada', 'Marca Original en DBF', 'Cantidad'])
    for fila in datos_detalle:
        escritor.writerow([fila['id'], fila['base'], fila['original'], fila['cantidad']])

with open(ruta_csv_unicas, mode='w', encoding='utf-8', newline='') as f:
    escritor = csv.writer(f)
    escritor.writerow(['ID Asignado', 'Marca Base Estandarizada', 'Cantidad Total de Vehículos'])
    for mb in marcas_base:
        escritor.writerow([mb['id'], mb['nombre'], mb['total']])

print(f"✅ Auditorías guardadas.")

# =====================================================================
# 6. ACTUALIZAR EL DBF
# =====================================================================
if os.path.exists(ruta_dbf):
    print(f"\n⏳ Actualizando {ruta_dbf}...")
    
    # Abrimos la tabla con la codificación de Windows
    tabla = dbf.Table(ruta_dbf, codepage='cp1252')
    
    with tabla: # Abre en modo lectura/escritura
        contador = 0
        sin_match = 0
        for reg in tabla:
            # Leemos la marca del DBF y la pasamos por la misma función de limpieza
            marca_dbf = limpiar_texto(reg.MARCA)
            
            # Buscamos el ID asignado
            id_final = resultado_mapeo_limpio.get(marca_dbf, 0)
            
            if id_final > 0:
                # Escribe en el campo ID_MARCA del DBF
                dbf.write(reg, ID_MARCA=id_final)
                contador += 1
            else:
                # Si quedó en 0 (marca vacía o no encontrada)
                dbf.write(reg, ID_MARCA=0)
                sin_match += 1
                
    print(f"✅ ¡Proceso terminado!")
    print(f"   - Registros actualizados con ID: {contador}")
    print(f"   - Registros sin marca asignada (ID 0): {sin_match}")
else:
    print(f"❌ No se encontró {ruta_dbf}. Verifica la ruta.")
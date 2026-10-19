# neumatic\data_load\datavfox\crea_modelos_veh2.py
import csv
import dbf
import re
from collections import defaultdict

# =====================================================================
# 1. CONFIGURACIÓN
# =====================================================================
ruta_dbf = 'vehiculo2.dbf'
ruta_csv_modelos = 'reporte_modelos_por_marca.csv'

# Usamos la misma función de limpieza para evitar problemas con espacios
def limpiar_texto(texto):
    if not texto: return ''
    texto = str(texto).upper()
    texto = re.sub(r'[^A-Z0-9ÁÉÍÓÚÑ\s]', '', texto) 
    texto = re.sub(r'\s+', ' ', texto) 
    return texto.strip()

# =====================================================================
# 2. LEER EL DBF Y AGRUPAR
# =====================================================================
print(f"🔍 Leyendo {ruta_dbf} y extrayendo modelos...")

# Diccionario para contar: la clave será una tupla (id_marca, modelo)
conteo_modelos = defaultdict(int)
# Diccionario para guardar el nombre original de la marca (solo para referencia visual)
nombres_marcas = {}

try:
    tabla = dbf.Table(ruta_dbf, codepage='cp1252')
    with tabla:
        for reg in tabla:
            # Leer el ID de la marca (puede ser mayúscula o minúscula según VFP)
            id_m = reg.ID_MARCA if hasattr(reg, 'ID_MARCA') else reg.id_marca
            
            # Si la marca no fue asignada (ID 0), la saltamos
            if id_m == 0:
                continue
                
            marca_texto = limpiar_texto(reg.MARCA)
            modelo_texto = limpiar_texto(reg.MODELO)
            
            # Guardamos qué marca corresponde a ese ID para que el CSV sea legible
            if id_m not in nombres_marcas:
                nombres_marcas[id_m] = marca_texto
                
            if not modelo_texto:
                modelo_texto = "SIN MODELO / VACIO"
                
            # Sumamos 1 al contador de esta combinación (ID + Modelo)
            conteo_modelos[(id_m, modelo_texto)] += 1

except Exception as e:
    print(f"❌ Error al leer el DBF: {e}")
    exit()

# =====================================================================
# 3. GENERAR EL ARCHIVO CSV
# =====================================================================
print("📝 Generando el archivo CSV...")

# Preparamos la lista para exportar
datos_exportar = []
for (id_m, modelo), cantidad in conteo_modelos.items():
    datos_exportar.append({
        'id_marca': id_m,
        'marca_ref': nombres_marcas[id_m], # Nombre de la marca original
        'modelo': modelo,
        'cantidad': cantidad
    })

# Ordenamos: Primero por ID de Marca (ascendente), luego por Cantidad (descendente)
# Esto nos mostrará en cada marca, los modelos más usados primero.
datos_exportar.sort(key=lambda x: (x['id_marca'], -x['cantidad']))

# Escribimos el archivo CSV
with open(ruta_csv_modelos, mode='w', encoding='utf-8', newline='') as f:
    escritor = csv.writer(f)
    # Encabezados
    escritor.writerow(['ID Marca', 'Marca (Referencia)', 'Modelo', 'Cantidad'])
    
    for fila in datos_exportar:
        escritor.writerow([
            fila['id_marca'], 
            fila['marca_ref'], 
            fila['modelo'], 
            fila['cantidad']
        ])

print(f"✅ ¡Listo! Archivo generado: '{ruta_csv_modelos}'")
print("Ábrelo en Excel. Verás que los modelos están agrupados por el ID de su marca.")
# neumatic\data_load\datavfox\actualiza_modelos_veh2.py
import csv
import re
import dbf
import os
from collections import defaultdict
from thefuzz import fuzz

# =====================================================================
# 1. CONFIGURACIÓN
# =====================================================================
ruta_dbf = 'vehiculo2.dbf'
ruta_csv_auditoria = 'auditoria_modelos.csv'

ALIAS_MODELOS = {
    # CITROEN (39)
    (39, 'C 4'): 'C4',
    (39, 'C4 LONGE'): 'C4 LOUNGE',
    (39, 'C4 LOVEE'): 'C4 LOUNGE',
    (39, 'C4 LUNGE'): 'C4 LOUNGE',
    (39, 'C3 AIR CROSS'): 'C3 AIRCROSS',
    (39, 'AIRCROSS'): 'C3 AIRCROSS',
    (39, 'AIR CROSS'): 'C3 AIRCROSS',
    (39, 'CELYSEE'): 'ELYSEE',
    (39, 'CELYCEE'): 'ELYSEE',
    (39, 'CELISEE'): 'ELYSEE',
    (39, 'CEYSEE'): 'ELYSEE',
    (39, 'CEELYCE'): 'ELYSEE',
    (39, 'ELYSSIE'): 'ELYSEE',
    (39, 'CELYEE'): 'ELYSEE',
    (39, 'CELYSSE'): 'ELYSEE',
    (39, 'ELYCCE'): 'ELYSEE',
    (39, 'ELISEE'): 'ELYSEE',
    (39, 'PICAZZO'): 'PICASSO',
    # CHEVROLET (36)
    (36, 'CORSA CLASIC'): 'CORSA CLASSIC',
    (36, 'CORSA CLASICC'): 'CORSA CLASSIC',
    (36, 'CORSA CLSSIC'): 'CORSA CLASSIC',
    (36, 'CLASICC'): 'CLASSIC',
    (36, 'S 10'): 'S10',
    (36, 'TRACKET'): 'TRACKER',
    (36, 'TRAKER'): 'TRACKER',
    (36, 'TRAKET'): 'TRACKER',
    (36, 'TRACJER'): 'TRACKER',
    (36, 'ONYX'): 'ONIX',
    (36, 'ONIIX'): 'ONIX',
    (36, 'CRUCE'): 'CRUZE',
    (36, 'CRUZ'): 'CRUZE',
    (36, 'CRUSE'): 'CRUZE',
    (36, 'COBAL'): 'COBALT',
    (36, 'CPBALT'): 'COBALT',
    (36, 'COIAT'): 'COBALT',
    (36, 'SONIX'): 'SONIC',
    (36, 'SONI'): 'SONIC',
    (36, 'COSA'): 'CORSA',
    # FIAT (68)
    (68, 'CRONO'): 'CRONOS',
    (68, 'CRONOSS'): 'CRONOS',
    (68, 'CHRONOS'): 'CRONOS',
    (68, 'DUCATTO'): 'DUCATO',
    (68, 'KUBO'): 'QUBO',
    (68, 'CUBO'): 'QUBO',
    (68, 'MOBY'): 'MOBI',
    (68, 'MOVI'): 'MOBI',
    (68, 'ESTRADA'): 'STRADA',
    # FORD (70)
    (70, 'ECO SPORT'): 'ECOSPORT',
    (70, 'ECOSORT'): 'ECOSPORT',
    (70, 'ECOESPORT'): 'ECOSPORT',
    (70, 'ECOS SPORT'): 'ECOSPORT',
    (70, 'ECPSPORT'): 'ECOSPORT',
    (70, 'ECPOSPORT'): 'ECOSPORT',
    (70, 'RANGEWR'): 'RANGER',
    (70, 'RANGEER'): 'RANGER',
    (70, 'RENGER'): 'RANGER',
    (70, 'F 100'): 'F100',
    (70, 'MAVERIK'): 'MAVERICK',
    (70, 'MAVERIC'): 'MAVERICK',
    (70, 'TERRITORI'): 'TERRITORY',
    (70, 'TERRETORY'): 'TERRITORY',
    (70, 'TERROTIRITI'): 'TERRITORY',
    (70, 'ESCORD'): 'ESCORT',
    (70, 'ESCOR'): 'ESCORT',
    (70, 'FIESTA KINETIC'): 'FIESTA KINETIC',
    (70, 'FIESTA KINETIK'): 'FIESTA KINETIC',
    (70, 'FIESTA KINETICK'): 'FIESTA KINETIC',
    # MERCEDES BENZ (131)
    (131, 'SPRITER'): 'SPRINTER',
    (131, 'SPRINTEER'): 'SPRINTER',
    (131, 'SRINTER'): 'SPRINTER',
    (131, 'ATEO 1725'): 'ATEGO 1725',
    (131, 'ATEGO726'): 'ATEGO 1726',
    (131, 'ACELO'): 'ACCELO',
    (131, 'ACELLO'): 'ACCELO',
    (131, 'ACCELLO'): 'ACCELO',
    (131, 'ACELO 815'): 'ACCELO 815',
    (131, 'ACELO815'): 'ACCELO 815',
    (131, 'ACCELLO 815'): 'ACCELO 815',
    (131, 'ATRON'): 'ACTRON',
    (131, 'ATROM'): 'ACTRON',
    (131, 'ACTOR 2545'): 'ACTROS 2545',
    (131, 'ATROS'): 'ACTROS',
    # RENAULT (165)
    (165, 'KANGO'): 'KANGOO',
    (165, 'KANGGO'): 'KANGOO',
    (165, 'KANNGOO'): 'KANGOO',
    (165, 'DASTER'): 'DUSTER',
    (165, 'DUSTRER'): 'DUSTER',
    (165, 'DASTER OROCH'): 'DUSTER OROCH',
    (165, 'DSTER'): 'DUSTER',
    (165, 'DSTER OROCH'): 'DUSTER OROCH',
    (165, 'SANNDERO'): 'SANDERO',
    (165, 'SANDEO'): 'SANDERO',
    (165, 'SNDERO'): 'SANDERO',
    (165, 'ASNDERO'): 'SANDERO',
    (165, 'KWID'): 'KWID',
    (165, 'KIWD'): 'KWID',
    (165, 'KUID'): 'KWID',
    (165, 'KIDS'): 'KWID',
    (165, 'STEWAY'): 'STEPWAY',
    (165, 'STETWAY'): 'STEPWAY',
    (165, 'STEPWEY'): 'STEPWAY',
    (165, 'SPETWAY'): 'STEPWAY',
    (165, 'STEEPWAY'): 'STEPWAY',
    (165, 'OROCH'): 'OROCH',
    (165, 'OROSH'): 'OROCH',
    (165, 'ORCH'): 'OROCH',
    (165, 'OROSCH'): 'OROCH',
    (165, 'OROSK'): 'OROCH',
    (165, 'CAPTUR'): 'CAPTUR',
    (165, 'CACTUR'): 'CAPTUR',
    (165, 'CAPTOUR'): 'CAPTUR',
    (165, 'CAPTURE'): 'CAPTUR',
    (165, 'KAPTUR'): 'CAPTUR',
    # TOYOTA (197)
    (197, 'HILIUX'): 'HILUX',
    (197, 'HILUZ'): 'HILUX',
    (197, 'HILIX'): 'HILUX',
    (197, 'HAILUX'): 'HILUX',
    (197, 'HILX'): 'HILUX',
    (197, 'HIUX'): 'HILUX',
    (197, 'HULUX'): 'HILUX',
    (197, 'HILUC'): 'HILUX',
    (197, 'HLUX'): 'HILUX',
    (197, 'HILU'): 'HILUX',
    (197, 'HULIX'): 'HILUX',
    (197, 'COROLA'): 'COROLLA',
    (197, 'CORLLA'): 'COROLLA',
    (197, 'COROLL'): 'COROLLA',
    (197, 'COLLORA'): 'COROLLA',
    (197, 'ETHIOS'): 'ETIOS',
    (197, 'RAV 4'): 'RAV4',
    (197, 'RV4'): 'RAV4',
    (197, 'HAICE'): 'HIACE',
    (197, 'HIANCE'): 'HIACE',
    (197, 'IACE'): 'HIACE',
    # VOLKSWAGEN (208)
    (208, 'AMAROX'): 'AMAROK',
    (208, 'AMAROCK'): 'AMAROK',
    (208, 'AMROK'): 'AMAROK',
    (208, 'AMARAROK'): 'AMAROK',
    (208, 'GOLD'): 'GOL',
    (208, 'GOLD TREND'): 'GOL TREND',
    (208, 'GOL TREN'): 'GOL TREND',
    (208, 'GOLTREN'): 'GOL TREND',
    (208, 'GOLD TREN'): 'GOL TREND',
    (208, 'GOLTREND'): 'GOL TREND',
    (208, 'SURAM'): 'SURAN',
    (208, 'SHURAN'): 'SURAN',
    (208, 'RURAN'): 'SURAN',
    (208, 'SIROCO'): 'SCIROCCO',
    (208, 'CIROCCO'): 'SCIROCCO',
    (208, 'SAWEIRO'): 'SAVEIRO',
    (208, 'SABEIRO CROSS'): 'SAVEIRO CROSS',
    (208, 'CADY'): 'CADDY',
    (208, 'CADDI'): 'CADDY',
    (208, 'CADYY'): 'CADDY',
    (208, 'VENTO GL'): 'VENTO',
}

def limpiar_texto(texto):
    if not texto: return 'SIN MODELO'
    texto = str(texto).upper()
    texto = re.sub(r'[^A-Z0-9ÁÉÍÓÚÑ\s]', '', texto) 
    texto = re.sub(r'\s+', ' ', texto) 
    return texto.strip()

# =====================================================================
# 2. LEER EL DBF Y AGRUPAR
# =====================================================================
print(f"🔍 Leyendo {ruta_dbf} y agrupando modelos por marca...")

datos_por_marca = defaultdict(lambda: defaultdict(int))
nombres_marcas = {}

try:
    tabla = dbf.Table(ruta_dbf, codepage='cp1252')
    with tabla:
        for reg in tabla:
            id_m = reg.ID_MARCA if hasattr(reg, 'ID_MARCA') else reg.id_marca
            if id_m == 0: continue
            
            marca_texto = limpiar_texto(reg.MARCA)
            modelo_texto = limpiar_texto(reg.MODELO)
            
            if not modelo_texto or modelo_texto == marca_texto:
                modelo_texto = 'SIN MODELO / VACIO'
                
            nombres_marcas[id_m] = marca_texto
            datos_por_marca[id_m][modelo_texto] += 1
except Exception as e:
    print(f"❌ Error al leer el DBF: {e}")
    exit()

# =====================================================================
# 3. ALGORITMO DE AGRUPACIÓN POR MARCA (CON PROTECCIÓN DE NÚMEROS)
# =====================================================================
modelos_base_por_marca = defaultdict(list)
mapeo_final = {}

for id_m, modelos_dict in datos_por_marca.items():
    modelos_ordenados = sorted(modelos_dict.items(), key=lambda x: x[1], reverse=True)
    
    for modelo_orig, cant in modelos_ordenados:
        modelo_limpio = limpiar_texto(modelo_orig)
        
        if (id_m, modelo_limpio) in ALIAS_MODELOS:
            base_asignada = ALIAS_MODELOS[(id_m, modelo_limpio)]
        elif modelo_limpio == 'SIN MODELO / VACIO':
            base_asignada = 'SIN MODELO / VACIO'
        else:
            base_asignada = None
            
            # Búsqueda por subcadena (con protección de números)
            for mb in modelos_base_por_marca[id_m]:
                if len(mb['base']) > 2 and mb['base'] in modelo_limpio:
                    resto = modelo_limpio.replace(mb['base'], '').strip()
                    if any(char.isdigit() for char in resto):
                        continue 
                    base_asignada = mb['base']
                    break
            
            # Búsqueda Difusa (con protección de números)
            if not base_asignada:
                mejor_match = None
                mejor_score = 0
                for mb in modelos_base_por_marca[id_m]:
                    score = fuzz.ratio(modelo_limpio, mb['base'])
                    if score > mejor_score:
                        mejor_score = score
                        mejor_match = mb
                
                if mejor_match and mejor_score >= 82:
                    nums_new = ''.join(filter(str.isdigit, modelo_limpio))
                    nums_base = ''.join(filter(str.isdigit, mejor_match['base']))
                    if nums_new and nums_base and nums_new != nums_base:
                        pass 
                    else:
                        base_asignada = mejor_match['base']
            
            if not base_asignada:
                base_asignada = modelo_limpio
        
        mapeo_final[(id_m, modelo_orig)] = base_asignada
        existe_base = False
        for mb in modelos_base_por_marca[id_m]:
            if mb['base'] == base_asignada:
                mb['total'] += cant
                existe_base = True
                break
        if not existe_base:
            modelos_base_por_marca[id_m].append({'base': base_asignada, 'total': cant})

# =====================================================================
# 4. ASIGNAR IDs GLOBALES
# =====================================================================
todos_los_modelos = []
for id_m, bases in modelos_base_por_marca.items():
    for mb in bases:
        todos_los_modelos.append({
            'id_marca': id_m,
            'marca_ref': nombres_marcas[id_m],
            'modelo_base': mb['base'],
            'total': mb['total']
        })

todos_los_modelos.sort(key=lambda x: (x['id_marca'], x['modelo_base']))
id_modelo_asignado = {}
id_counter = 1

for tm in todos_los_modelos:
    tm['id_modelo'] = id_counter
    id_modelo_asignado[(tm['id_marca'], tm['modelo_base'])] = id_counter
    id_counter += 1

# =====================================================================
# 5. GENERAR CSV DE AUDITORÍA
# =====================================================================
print("📝 Generando archivo de auditoría...")

datos_detalle = []
for (id_m, modelo_orig), modelo_base in mapeo_final.items():
    cant_orig = datos_por_marca[id_m][modelo_orig]
    id_mod = id_modelo_asignado.get((id_m, modelo_base), 0)
    
    datos_detalle.append({
        'id_modelo': id_mod,
        'id_marca': id_m,
        'marca': nombres_marcas[id_m],
        'modelo_base': modelo_base,
        'modelo_orig': modelo_orig,
        'cantidad': cant_orig
    })

datos_detalle.sort(key=lambda x: (x['id_modelo'], -x['cantidad']))

with open(ruta_csv_auditoria, mode='w', encoding='utf-8', newline='') as f:
    escritor = csv.writer(f)
    escritor.writerow(['ID Modelo', 'ID Marca', 'Marca', 'Modelo Base', 'Modelo Original', 'Cantidad'])
    for fila in datos_detalle:
        escritor.writerow([
            fila['id_modelo'], fila['id_marca'], fila['marca'], 
            fila['modelo_base'], fila['modelo_orig'], fila['cantidad']
        ])

print(f"✅ Auditoría guardada en '{ruta_csv_auditoria}'.")
print(f"✅ Total de Modelos Base identificados: {len(todos_los_modelos)}")

## =====================================================================
# 6. ACTUALIZAR EL DBF
# =====================================================================
if os.path.exists(ruta_dbf):
    print(f"\n⏳ Actualizando {ruta_dbf} con los nuevos IDs de Modelo...")
    
    try:
        # La forma correcta de abrir con la versión actual de dbf
        tabla = dbf.Table(ruta_dbf, codepage='cp1252')
        
        # Diagnóstico de campos
        campo_id_m = 'ID_MARCA' if 'ID_MARCA' in tabla.field_names else 'id_marca'
        campo_id_mod = 'ID_MODELO' if 'ID_MODELO' in tabla.field_names else 'id_modelo'
        
        if campo_id_mod not in tabla.field_names:
            print("❌ ERROR CRÍTICO: No se encontró el campo 'id_modelo' en la tabla.")
            print("Ejecuta en VFP: 'ALTER TABLE vehiculo2 ADD COLUMN id_modelo I'")
        else:
            # El bloque 'with' se encarga de abrir en modo lectura/escritura automáticamente
            with tabla:
                contador = 0
                sin_match = 0
                
                for reg in tabla:
                    id_m = getattr(reg, campo_id_m)
                    
                    # Si no tiene marca, el modelo es 0
                    if id_m == 0:
                        dbf.write(reg, **{campo_id_mod: 0})
                        continue
                        
                    marca_dbf = limpiar_texto(reg.MARCA)
                    modelo_dbf = limpiar_texto(reg.MODELO)
                    
                    if not modelo_dbf or modelo_dbf == marca_dbf:
                        modelo_dbf = 'SIN MODELO / VACIO'
                        
                    # Doble cruce: buscar el modelo base, y luego su ID
                    modelo_base_asignado = mapeo_final.get((id_m, modelo_dbf))
                    id_final = id_modelo_asignado.get((id_m, modelo_base_asignado), 0)
                    
                    if id_final > 0:
                        dbf.write(reg, **{campo_id_mod: id_final})
                        contador += 1
                    else:
                        dbf.write(reg, **{campo_id_mod: 0})
                        sin_match += 1
                        
            print(f"\n✅ ¡Proceso terminado!")
            print(f"   - Registros actualizados con ID_Modelo: {contador}")
            print(f"   - Registros con modelo no encontrado (ID 0): {sin_match}")

    except dbf.DbfError as e:
        print(f"❌ ERROR de la librería DBF: {e}")
        print("💡 Solución: Asegúrate de que Visual FoxPro esté CERRADO y la tabla no esté en uso.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
else:
    print(f"❌ No se encontró el archivo {ruta_dbf}. Verifica que esté en la misma carpeta que el script.")
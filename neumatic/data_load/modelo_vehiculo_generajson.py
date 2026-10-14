# neumatic\data_load\modelo_vehiculo_generajson.py
import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def abrir_csv(path):
    """
    Abre un CSV probando codificaciones comunes en Windows.
    Devuelve un file-like listo para csv.DictReader.
    """
    for enc in ('utf-8-sig', 'utf-8', 'cp1252', 'latin-1'):
        try:
            with open(path, 'r', encoding=enc, newline='') as f:
                # Forzamos la lectura completa para detectar errores aquí
                contenido = f.read()
            # Devolvemos un iterador de líneas a partir del texto ya decodificado
            return contenido.splitlines()
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"No se pudo decodificar el archivo: {path}")


# 1. id_marca → nombre canónico  (desde marca_vehiculo.csv)
marcas_por_id = {}
for row in csv.DictReader(
    abrir_csv(os.path.join(BASE_DIR, 'data_load', 'marca_vehiculo.csv'))
):
    id_str = (row.get('id_marca_vehiculo') or '').strip()
    if not id_str:
        continue
    marcas_por_id[int(id_str)] = (row.get('marca_vehiculo') or '').strip().upper()

# 2. alias normalizado → id_marca  (desde marca_vehiculo.json)
with open(os.path.join(BASE_DIR, 'data_load', 'marca_vehiculo.json'),
          'r', encoding='utf-8') as f:
    marcas_data = json.load(f)

nombre_a_id = {v: k for k, v in marcas_por_id.items()}
ALIAS_TO_ID = {}
for item in marcas_data:
    canonico = item['marca_vehiculo'].strip().upper()
    id_marca = nombre_a_id.get(canonico)
    if id_marca is None:
        continue
    ALIAS_TO_ID[canonico] = id_marca
    for alias in item.get('aliases', []):
        key = " ".join(str(alias).strip().upper().split())
        ALIAS_TO_ID[key] = id_marca

# 3. agrupar modelos por id_marca  (desde vehiculo.csv)
modelos_por_id = {id_marca: set() for id_marca in marcas_por_id}

for row in csv.DictReader(
    abrir_csv(os.path.join(BASE_DIR, 'data_load', 'vehiculo.csv'))
):
    marca_norm = " ".join((row.get('marca') or '').upper().split())
    id_marca = ALIAS_TO_ID.get(marca_norm)
    if id_marca is None:
        continue
    modelo_norm = " ".join((row.get('modelo') or '').upper().split())
    if not modelo_norm:
        modelo_norm = "S/D"
    modelos_por_id[id_marca].add(modelo_norm)

# 4. JSON final
json_output = [
    {
        "id_marca_vehiculo": id_marca,
        "marca_vehiculo": marcas_por_id[id_marca],
        "modelos": sorted(modelos_por_id[id_marca]),
    }
    for id_marca in sorted(marcas_por_id.keys())
]

with open(os.path.join(BASE_DIR, 'data_load', 'modelo_vehiculo.json'),
          'w', encoding='utf-8') as f:
    json.dump(json_output, f, ensure_ascii=False, indent=2)

print(f"✅ modelo_vehiculo.json generado "
      f"({sum(len(i['modelos']) for i in json_output)} modelos, "
      f"{len(json_output)} marcas)")
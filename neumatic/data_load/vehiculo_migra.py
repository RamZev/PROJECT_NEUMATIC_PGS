# neumatic/data_load/vehiculo_migra.py
import os
import sys
import json
import django
from difflib import SequenceMatcher
from dbfread import DBF
from django.db import connection, transaction
from django.conf import settings

# --- Bootstrap Django ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.vehiculo_models import (
    Vehiculo, MarcaVehiculo, ModeloVehiculo
)

# --- Constantes ---
UMBRAL_FUZZY_MARCA = 0.85
UMBRAL_FUZZY_MODELO = 0.85
BATCH_SIZE = 1000
SEGMENTOS_VALIDOS = {" ", "H", "LT", "MM", "SUV", "VZ"}


# ============================================================
# Utilidades de matching
# ============================================================
def _norm(texto):
    """Normaliza: strip + upper + colapsa espacios internos."""
    if texto is None:
        return ""
    return " ".join(str(texto).strip().upper().split())


def _sim(a, b):
    return SequenceMatcher(None, a, b).ratio()


# ============================================================
# Índices en memoria
# ============================================================
def build_marca_lookup():
    """
    Retorna:
      exact:      {NOMBRE_UP: id_marca}
      alias:      {ALIAS_UP: id_marca}
      candidatos: [(NOMBRE_UP, id_marca), ...]  # para fuzzy
    """
    exact, candidatos = {}, []
    for m in MarcaVehiculo.objects.all().values(
            'id_marca_vehiculo', 'marca_vehiculo'):
        key = _norm(m['marca_vehiculo'])
        exact[key] = m['id_marca_vehiculo']
        candidatos.append((key, m['id_marca_vehiculo']))

    alias = {}
    json_path = os.path.join(BASE_DIR, 'data_load', 'marca_vehiculo.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            id_m = exact.get(_norm(item.get('marca_vehiculo')))
            if not id_m:
                continue
            for a in item.get('aliases', []):
                alias[_norm(a)] = id_m

    return exact, alias, candidatos


def build_modelo_lookup():
    """
    Retorna:
      exact:     {(id_marca, MODELO_UP): id_modelo}
      por_marca: {id_marca: [(MODELO_UP, id_modelo), ...]}
    """
    exact, por_marca = {}, {}
    for m in ModeloVehiculo.objects.all().values(
            'id_modelo_vehiculo', 'id_marca_vehiculo_id', 'modelo_vehiculo'):
        key = _norm(m['modelo_vehiculo'])
        id_m = m['id_marca_vehiculo_id']
        exact[(id_m, key)] = m['id_modelo_vehiculo']
        por_marca.setdefault(id_m, []).append((key, m['id_modelo_vehiculo']))
    return exact, por_marca


# ============================================================
# Matching
# ============================================================
def match_marca(valor, exact, alias, candidatos):
    key = _norm(valor)
    if not key:
        return None
    if key in exact:
        return exact[key]
    if key in alias:
        return alias[key]
    # Fuzzy sobre el universo de marcas canónicas
    mejor, mejor_score = None, 0.0
    for nombre, id_m in candidatos:
        s = _sim(key, nombre)
        if s > mejor_score:
            mejor_score, mejor = s, id_m
    return mejor if mejor_score >= UMBRAL_FUZZY_MARCA else None


def match_modelo(valor, id_marca, exact, por_marca):
    key = _norm(valor)
    if not key:
        return None
    if (id_marca, key) in exact:
        return exact[(id_marca, key)]
    # Fuzzy restringido a los modelos de la marca ya resuelta
    mejor, mejor_score = None, 0.0
    for nombre, id_mo in por_marca.get(id_marca, []):
        s = _sim(key, nombre)
        if s > mejor_score:
            mejor_score, mejor = s, id_mo
    return mejor if mejor_score >= UMBRAL_FUZZY_MODELO else None


# ============================================================
# Helpers de conversión
# ============================================================
def to_int(valor, default=None):
    try:
        if valor is None or valor == '':
            return default
        return int(valor)
    except (ValueError, TypeError):
        return default


def to_bool_sn(valor):
    if valor is None:
        return False
    return str(valor).strip().upper() in ('S', 'SI', 'SÍ', '1', 'T', 'TRUE')


def limpiar_memo(valor):
    if valor is None:
        return None
    s = str(valor).strip()
    return s if s else None


def limpiar_segmento(valor):
    s = (str(valor) if valor is not None else "").strip().upper()
    if not s:
        return " "
    return s if s in SEGMENTOS_VALIDOS else " "


# ============================================================
# Reset tabla
# ============================================================
def reset_vehiculo():
    Vehiculo.objects.all().delete()
    print("Tabla Vehiculo limpiada.")
    engine = settings.DATABASES['default']['ENGINE']
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='vehiculo';")
        elif 'postgresql' in engine:
            cursor.execute(
                "SELECT setval(pg_get_serial_sequence('vehiculo', "
                "'id_vehiculo'), 1, false);"
            )
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('vehiculo', RESEED, 0);")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE vehiculo AUTO_INCREMENT = 1;")


# ============================================================
# Migración principal
# ============================================================
def cargar_vehiculos():
    reset_vehiculo()

    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'VEHICULO.DBF')
    if not os.path.exists(dbf_path):
        print(f"❌ No se encuentra {dbf_path}")
        return

    print("📚 Construyendo índices de búsqueda...")
    exact_m, alias_m, cand_m = build_marca_lookup()
    exact_mo, por_marca_mo = build_modelo_lookup()
    print(f"   Marcas: {len(exact_m)} | Alias: {len(alias_m)} | "
          f"Modelos: {len(exact_mo)}")

    total = ok = omitidos_sin_marca = sin_modelo = 0
    marcas_fallidas = {}
    modelos_fallidos = {}
    batch = []

    # ignore_missing_memofile=False para que falle ruidosamente si falta el .FPT
    table = DBF(dbf_path, encoding='cp1252', ignore_missing_memofile=False)

    with transaction.atomic():
        for record in table:
            total += 1

            # -------- Marca --------
            marca_raw = record.get('MARCA')
            id_marca = match_marca(marca_raw, exact_m, alias_m, cand_m)
            if id_marca is None:
                omitidos_sin_marca += 1
                key = _norm(marca_raw)
                marcas_fallidas[key] = marcas_fallidas.get(key, 0) + 1
                continue

            # -------- Modelo (acotado a la marca) --------
            modelo_raw = record.get('MODELO')
            id_modelo = match_modelo(modelo_raw, id_marca, exact_mo, por_marca_mo)
            if id_modelo is None:
                sin_modelo += 1
                key = (id_marca, _norm(modelo_raw))
                modelos_fallidos[key] = modelos_fallidos.get(key, 0) + 1

            # -------- Construir instancia --------
            v = Vehiculo(
                estatus_vehiculo=True,
                tipo_vehiculo=to_int(record.get('TIPO'), 1) or 1,
                id_marca_vehiculo_id=id_marca,
                id_modelo_vehiculo_id=id_modelo,
                segmento=limpiar_segmento(record.get('SEGMENTO')),
                anio=to_int(record.get('ANIO')),
                patente=_norm(record.get('PATENTE'))[:7],
                kmxmes=to_int(record.get('KMXMES')),
                visita=record.get('VISITA'),
                observacion=limpiar_memo(record.get('OBSERVACIO')),
                exportado=to_bool_sn(record.get('EXPORTADO')),
            )
            batch.append(v)
            ok += 1

            if len(batch) >= BATCH_SIZE:
                Vehiculo.objects.bulk_create(batch, batch_size=BATCH_SIZE)
                batch = []
                print(f"   ... {ok:>7} migrados")

        if batch:
            Vehiculo.objects.bulk_create(batch, batch_size=BATCH_SIZE)

    # -------- Reporte final --------
    print("\n" + "=" * 60)
    print("RESUMEN MIGRACIÓN VEHÍCULO")
    print("=" * 60)
    print(f"  Total DBF:                  {total}")
    print(f"  Migrados OK:                {ok}")
    print(f"  Omitidos (marca no match):  {omitidos_sin_marca}")
    print(f"  Sin modelo asignado:        {sin_modelo}")

    if marcas_fallidas:
        print("\n🔍 Top 20 marcas sin match (considerar agregar alias):")
        for k, v in sorted(marcas_fallidas.items(), key=lambda x: -x[1])[:20]:
            print(f"   {v:>6}  '{k}'")

    if modelos_fallidos:
        print("\n🔍 Top 20 modelos sin match (considerar agregar al JSON):")
        for (id_m, k), v in sorted(modelos_fallidos.items(),
                                   key=lambda x: -x[1])[:20]:
            print(f"   {v:>6}  marca_id={id_m}  '{k}'")


# ============================================================
# Verificación de conexión
# ============================================================
def verificar_conexion():
    try:
        with connection.cursor() as cursor:
            engine = settings.DATABASES['default']['ENGINE']
            print(f"📋 Motor de base de datos: {engine}")
            if 'sqlite' in engine:
                cursor.execute("SELECT sqlite_version();")
                print(f"✅ SQLite: {cursor.fetchone()[0]}")
            elif 'postgresql' in engine:
                cursor.execute("SELECT version();")
                print(f"✅ PostgreSQL: {cursor.fetchone()[0][:80]}...")
            elif 'mssql' in engine or 'sql_server' in engine:
                cursor.execute("SELECT @@VERSION")
                print(f"✅ SQL Server: {cursor.fetchone()[0][:80]}...")
            elif 'mysql' in engine:
                cursor.execute("SELECT VERSION();")
                print(f"✅ MySQL: {cursor.fetchone()[0]}")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("MIGRACIÓN DE DATOS - VEHÍCULO")
    print("=" * 60)
    if verificar_conexion():
        cargar_vehiculos()
        print("\n" + "=" * 60)
        print("✅ Migración de Vehículo completada.")
        print("=" * 60)
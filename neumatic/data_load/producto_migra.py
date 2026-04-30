# neumatic\data_load\producto_migra.py
import os
import sys
import django
import time
from dbfread import DBF
from django.db import connection
from django.utils import timezone

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.producto_models import Producto
from apps.maestros.models.base_models import ProductoFamilia, ProductoMarca, ProductoModelo

def reset_producto():
    """Elimina los datos existentes y resetea la secuencia"""
    print("🔁 Reseteando tabla Producto...")
    Producto.objects.all().delete()
    print("Tabla Producto limpiada.")
    
    from django.conf import settings
    engine = settings.DATABASES['default']['ENGINE']
    
    with connection.cursor() as cursor:
        if 'sqlite' in engine:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='producto';")
            print("Secuencia de ID reseteada (SQLite).")
        elif 'postgresql' in engine:
            cursor.execute("SELECT setval(pg_get_serial_sequence('producto', 'id_producto'), 1, false);")
            print("Secuencia de ID reseteada (PostgreSQL).")
        elif 'mssql' in engine or 'sql_server' in engine:
            cursor.execute("DBCC CHECKIDENT ('producto', RESEED, 0);")
            print("Secuencia de ID reseteada (SQL Server).")
        elif 'mysql' in engine:
            cursor.execute("ALTER TABLE producto AUTO_INCREMENT = 1;")
            print("Secuencia de ID reseteada (MySQL).")
        else:
            print(f"Motor {engine} no requiere reset manual de secuencia.")

# def get_related_objects():
#     """Precarga objetos relacionados para optimización"""
#     familias = {str(f.pk): f for f in ProductoFamilia.objects.all()}
#     marcas = {str(m.pk): m for m in ProductoMarca.objects.all()}
#     modelos = {str(m.pk): m for m in ProductoModelo.objects.all()}
#     return familias, marcas, modelos

def get_related_objects():
    """Precarga objetos relacionados para optimización"""
    # Usar values_list para evitar cargar campos de texto problemáticos
    familias_ids = ProductoFamilia.objects.values_list('id_producto_familia', flat=True)
    marcas_ids = ProductoMarca.objects.values_list('id_producto_marca', flat=True)
    modelos_ids = ProductoModelo.objects.values_list('id_modelo', flat=True)
    
    # Crear objetos solo con el ID (sin leer otros campos)
    familias = {str(f_id): ProductoFamilia(id_producto_familia=f_id) for f_id in list(familias_ids)}
    marcas = {str(m_id): ProductoMarca(id_producto_marca=m_id) for m_id in list(marcas_ids)}
    modelos = {str(m_id): ProductoModelo(id_modelo=m_id) for m_id in list(modelos_ids)}
    
    print(f"📦 Familias cargadas: {len(familias)}")
    print(f"📦 Marcas cargadas: {len(marcas)}")
    print(f"📦 Modelos cargados: {len(modelos)}")
    
    return familias, marcas, modelos

def cargar_datos():
    """Carga los datos desde el DBF en lotes con progreso"""
    reset_producto()
    
    # Precargar objetos relacionados
    familias, marcas, modelos = get_related_objects()
    missing_relations = {'familias': set(), 'marcas': set(), 'modelos': set()}

    # Configuración de rutas y lectura de datos
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'lista.DBF')
    records = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda r: r['CODIGO'])
    total_registros = len(records)
    lote_size = 500  # Tamaño del lote para bulk_create
    
    print(f"\n📊 Total de registros a procesar: {total_registros:,}")
    print(f"⚡ Procesando en lotes de {lote_size} registros...\n")

    start_time = timezone.now()
    batch = []
    processed = 0
    skipped = 0

    for i, record in enumerate(records, 1):
        try:
            codigo = int(record['CODIGO'])
            
            # Verificar relaciones
            familia_id = str(record.get('ARTICULO', ''))
            marca_id = str(record.get('MARCA', ''))
            modelo_id = str(record.get('MODELO', ''))
            
            familia = familias.get(familia_id)
            marca = marcas.get(marca_id)
            modelo = modelos.get(modelo_id)
            
            if not all([familia, marca, modelo]):
                # Registrar relaciones faltantes
                if not familia:
                    missing_relations['familias'].add(familia_id)
                if not marca:
                    missing_relations['marcas'].add(marca_id)
                if not modelo:
                    missing_relations['modelos'].add(modelo_id)
                skipped += 1
                continue

            # Preparar datos con valores por defecto
            batch.append(Producto(
                id_producto=codigo,
                estatus_producto=True,
                codigo_producto=str(codigo).strip(),
                tipo_producto=record.get('TIPO', '').strip(),
                id_familia=familia,
                id_marca=marca,
                id_modelo=modelo,
                cai=record.get('CODFABRICA', '').strip(),
                medida=record.get('MEDIDA', '').strip(),
                segmento=record.get('SEGMENTO', '').strip(),
                nombre_producto=record.get('NOMBRE', 'Sin Nombre').strip(),
                unidad=record.get('UNIDAD', 0) or 0,
                fecha_fabricacion=record.get('FECHA', '').strip(),
                costo=record.get('COSTO', 0.00) or 0.00,
                alicuota_iva=record.get('IVA', 0.00) or 0.00,
                precio=record.get('PRECIO', 0.00) or 0.00,
                stock=record.get('STOCK', 0) or 0,
                minimo=record.get('MINIMO', 0) or 0,
                descuento=record.get('DESCUENTO', 0.00) or 0.00,
                despacho_1=record.get('DESPACHO1', '').strip(),
                despacho_2=record.get('DESPACHO2', '').strip(),
                descripcion_producto=record.get('DETALLE', '').strip(),
                carrito=record.get('CARRITO', False) or False
            ))

            # Procesar lote completo
            if len(batch) >= lote_size:
                Producto.objects.bulk_create(batch)
                processed += len(batch)
                batch = []
                
                # Mostrar progreso cada 500 registros
                if i % 500 == 0:
                    percent = (i / total_registros) * 100
                    print(f"🔄 Procesados: {i:,}/{total_registros:,} ({percent:.1f}%) | "
                          f"Insertados: {processed:,} | Saltados: {skipped:,}", end='\r')

        except Exception as e:
            print(f"\n⚠️ Error en registro {i}: {str(e)}")
            skipped += 1
            continue

    # Insertar último lote parcial
    if batch:
        Producto.objects.bulk_create(batch)
        processed += len(batch)

    # Estadísticas finales
    end_time = timezone.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n\n📝 Resumen de migración:")
    print(f"✅ Registros insertados: {processed:,}")
    print(f"⏭️ Registros saltados: {skipped:,}")
    print(f"⏱️ Tiempo total: {duration:.2f} segundos")
    print(f"🚀 Velocidad: {processed/duration:.1f} registros/segundo")
    
    # Mostrar relaciones faltantes si las hay
    if any(missing_relations.values()):
        print("\n⚠️ Relaciones faltantes detectadas:")
        for rel_type, ids in missing_relations.items():
            if ids:
                print(f"- {rel_type.capitalize()}: {', '.join(sorted(ids)[:5])}{'...' if len(ids)>5 else ''}")

if __name__ == '__main__':
    cargar_datos()
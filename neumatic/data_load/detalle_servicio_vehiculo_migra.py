# neumatic/data_load/detalle_servicio_vehiculo_migra.py
import os
import sys
import django
from django.db import connection
from django.conf import settings
import dbf
from decimal import Decimal

# Configurar entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

# Importar modelos necesarios
from apps.ventas.models.servicio_vehiculo_models import ServicioVehiculo, DetalleServicioVehiculo
from apps.maestros.models.vehiculo_models import Vehiculo
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.vendedor_models import Vendedor

# Ruta del archivo DBF (ajusta si es necesario)
ruta_dbf = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'trabvehi.dbf')

BATCH_SIZE = 1000

def reset_tabla():
    print("Limpiando tabla DetalleServicioVehiculo...")
    DetalleServicioVehiculo.objects.all().delete()
    engine = settings.DATABASES['default']['ENGINE']
    with connection.cursor() as cursor:
        if 'postgresql' in engine:
            cursor.execute("TRUNCATE TABLE detalle_servicio_vehiculo RESTART IDENTITY CASCADE;")
            print("Secuencia de ID reseteada (PostgreSQL).")

def construir_indices():
    """Crea diccionarios en memoria para acelerar las búsquedas y evitar consultas por cada fila."""
    print("📚 Construyendo índices de búsqueda...")
    
    # 1. Mapear Patente -> id_vehiculo
    # Excluimos patentes vacías o nulas
    vehiculos = Vehiculo.objects.exclude(patente='').exclude(patente__isnull=True).values('id_vehiculo', 'patente')
    patente_a_vehiculo = {v['patente'].strip().upper(): v['id_vehiculo'] for v in vehiculos}
    
    # 2. Mapear id_vehiculo -> id_servicio_vehiculo (el más reciente)
    # Ordenamos por ID descendente para que el primero que encuentre sea el último creado
    servicios = ServicioVehiculo.objects.order_by('-id_servicio_vehiculo').values('id_servicio_vehiculo', 'id_vehiculo_id')
    vehiculo_a_servicio = {}
    for s in servicios:
        if s['id_vehiculo_id'] not in vehiculo_a_servicio:
            vehiculo_a_servicio[s['id_vehiculo_id']] = s['id_servicio_vehiculo']

    # 3. Mapear Producto (ID o código) -> id_producto
    # Asumiendo que en el DBF guardan el ID numérico o el código. Mapeamos ambos.
    productos = Producto.objects.all().values('id_producto', 'codigo_producto')
    prod_map = {}
    for p in productos:
        prod_map[str(p['id_producto'])] = p['id_producto']
        if p['codigo_producto']:
            prod_map[str(p['codigo_producto']).strip().upper()] = p['id_producto']

    # 4. Mapear Vendedor -> id_vendedor
    vendedores = Vendedor.objects.all().values('id_vendedor', 'nombre_vendedor')
    vend_map = {}
    for v in vendedores:
        vend_map[str(v['id_vendedor'])] = v['id_vendedor']
        if v['nombre_vendedor']:
            vend_map[str(v['nombre_vendedor']).strip().upper()] = v['id_vendedor']

    print(f"   Patentes indexadas: {len(patente_a_vehiculo)}")
    print(f"   Servicios indexados: {len(vehiculo_a_servicio)}")
    print(f"   Productos indexados: {len(prod_map)}")
    print(f"   Vendedores indexados: {len(vend_map)}")
    
    return patente_a_vehiculo, vehiculo_a_servicio, prod_map, vend_map

def cargar_detalles():
    reset_tabla()
    patente_a_vehiculo, vehiculo_a_servicio, prod_map, vend_map = construir_indices()
    
    print(f"📂 Leyendo {ruta_dbf}...")
    
    try:
        tabla = dbf.Table(ruta_dbf, codepage='cp1252')
    except Exception as e:
        print(f"❌ Error al abrir el DBF: {e}")
        return

    batch = []
    contador = 0
    omitidos = 0

    with tabla:
        campos_dbf = tabla.field_names
        
        # Helper para leer campos del DBF de forma segura
        def leer(reg, nombre):
            if nombre in campos_dbf:
                val = getattr(reg, nombre)
                return str(val).strip() if val is not None else ''
            return ''

        for reg in tabla:
            # 1. Obtener la patente y buscar el servicio asociado
            patente = leer(reg, 'PATENTE').upper()
            
            if not patente:
                omitidos += 1
                continue
                
            id_vehiculo = patente_a_vehiculo.get(patente)
            if not id_vehiculo:
                # Si la patente no existe en nuestra tabla de vehículos, lo omitimos
                omitidos += 1
                continue
                
            id_servicio = vehiculo_a_servicio.get(id_vehiculo)
            if not id_servicio:
                # Si el vehículo no tiene un servicio asociado, lo omitimos
                omitidos += 1
                continue

            # 2. Obtener el Producto (puede venir como ID o Código)
            prod_raw = leer(reg, 'PRODUCTO') or leer(reg, 'CODPRODUCTO') or leer(reg, 'ID_PRODUCTO')
            id_producto = prod_map.get(prod_raw.upper())
            if not id_producto:
                omitidos += 1
                continue

            # 3. Obtener la cantidad (asegurando que sea un decimal válido)
            cant_raw = leer(reg, 'CANTIDAD')
            try:
                cantidad = Decimal(cant_raw) if cant_raw else Decimal('1.00')
                if cantidad <= 0: cantidad = Decimal('1.00')
            except:
                cantidad = Decimal('1.00')

            # 4. Obtener Vendedor (opcional)
            vend_raw = leer(reg, 'VENDEDOR') or leer(reg, 'ID_VENDEDOR')
            id_vendedor = vend_map.get(vend_raw.upper()) if vend_raw else None

            # 5. Obtener Exportado
            exportado_raw = leer(reg, 'EXPORTADO').lower()
            exportado = exportado_raw in ['true', 't', '1', 's', 'si']

            # 6. Crear la instancia del detalle
            detalle = DetalleServicioVehiculo(
                id_servicio_vehiculo_id=id_servicio,
                id_producto_id=id_producto,
                cantidad=cantidad,
                id_vendedor_id=id_vendedor,
                exportado=exportado
            )
            
            batch.append(detalle)
            contador += 1

            if len(batch) >= BATCH_SIZE:
                DetalleServicioVehiculo.objects.bulk_create(batch, batch_size=BATCH_SIZE)
                batch = []
                if contador % 5000 == 0:
                    print(f"   ... {contador} detalles migrados")

    # Insertar el último lote
    if batch:
        DetalleServicioVehiculo.objects.bulk_create(batch, batch_size=BATCH_SIZE)

    print(f"\n✅ Se migraron {contador} detalles correctamente.")
    print(f"⚠️ Se omitieron {omitidos} registros (por no encontrar patente, servicio o producto).")

if __name__ == '__main__':
    if os.path.exists(ruta_dbf):
        cargar_detalles()
    else:
        print(f"❌ No se encontró el archivo: {ruta_dbf}")
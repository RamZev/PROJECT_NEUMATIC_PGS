# neumatic\data_load\detalle_recibo_migra.py
import os
import sys
import django
import time
import logging
from dbfread import DBF
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

# --- Configuración de Entorno Django ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.recibo_models import DetalleRecibo
from apps.ventas.models.factura_models import Factura

# --- Configuración de Logging ---
# Limpiar handlers existentes
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configurar logging para archivo y consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('detalle_recibo_errores.log', mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

BATCH_SIZE = 5000  

def safe_int(value, default=0):
    """Convierte de forma segura a entero, manejando bytes y valores inválidos"""
    try:
        if value is None:
            return default
        # Manejar bytes
        if isinstance(value, bytes):
            # Limpiar bytes nulos y convertir a string
            cleaned = value.replace(b'\x00', b'').strip()
            if not cleaned:
                return default
            value = cleaned.decode('latin-1')
        # Convertir a string y limpiar
        str_value = str(value).strip()
        if not str_value:
            return default
        return int(float(str_value))
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """Convierte de forma segura a float, manejando bytes y valores inválidos"""
    try:
        if value is None:
            return default
        # Manejar bytes
        if isinstance(value, bytes):
            # Limpiar bytes nulos y convertir a string
            cleaned = value.replace(b'\x00', b'').strip()
            if not cleaned:
                return default
            value = cleaned.decode('latin-1')
        # Convertir a string y limpiar
        str_value = str(value).strip()
        if not str_value:
            return default
        return float(str_value)
    except (ValueError, TypeError):
        return default

def safe_decimal(value, max_digits=12, decimal_places=2):
    """Convierte de forma segura a Decimal y valida que no exceda el tamaño máximo"""
    try:
        if value is None:
            return Decimal('0.00')
        
        # Manejar bytes
        if isinstance(value, bytes):
            cleaned = value.replace(b'\x00', b'').strip()
            if not cleaned:
                return Decimal('0.00')
            value = cleaned.decode('latin-1')
        
        # Convertir a string y limpiar
        str_value = str(value).strip()
        if not str_value:
            return Decimal('0.00')
        
        # Convertir a Decimal
        decimal_value = Decimal(str_value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Validar que no exceda el máximo permitido
        max_value = Decimal('9' * (max_digits - decimal_places) + '.' + '9' * decimal_places)
        
        if abs(decimal_value) > max_value:
            raise ValueError(f"Valor {decimal_value} excede el máximo permitido {max_value}")
        
        return decimal_value
    except Exception as e:
        # Si hay error, retornar 0 y registrar el valor original para debugging
        logging.debug(f"Error convirtiendo a Decimal: valor original '{value}' - {str(e)}")
        return Decimal('0.00')

def safe_string(value, default=''):
    """Convierte de forma segura a string, manejando bytes"""
    try:
        if value is None:
            return default
        if isinstance(value, bytes):
            # Limpiar bytes nulos
            cleaned = value.replace(b'\x00', b'').strip()
            if not cleaned:
                return default
            return cleaned.decode('latin-1')
        return str(value).strip()
    except (ValueError, TypeError):
        return default

def reset_detalle_recibo():
    """Elimina los datos existentes en la tabla DetalleRecibo y resetea su ID"""
    from django.db import connection
    from django.conf import settings
    
    print("\nInicializando migración...")
    
    try:
        # Eliminar registros
        count = DetalleRecibo.objects.count()
        if count > 0:
            print(f"Eliminando {count:,} registros existentes...")
            DetalleRecibo.objects.all().delete()
            logging.info(f"Eliminados {count} registros existentes de DetalleRecibo")
        
        engine = settings.DATABASES['default']['ENGINE']
        
        with connection.cursor() as cursor:
            if 'sqlite' in engine:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='detalle_recibo';")
                print("Secuencia de ID reseteada (SQLite).")
            elif 'postgresql' in engine:
                cursor.execute("SELECT setval(pg_get_serial_sequence('detalle_recibo', 'id_detalle_recibo'), 1, false);")
                print("Secuencia de ID reseteada (PostgreSQL).")
            elif 'mssql' in engine or 'sql_server' in engine:
                cursor.execute("DBCC CHECKIDENT ('detalle_recibo', RESEED, 0);")
                print("Secuencia de ID reseteada (SQL Server).")
            elif 'mysql' in engine:
                cursor.execute("ALTER TABLE detalle_recibo AUTO_INCREMENT = 1;")
                print("Secuencia de ID reseteada (MySQL).")
            else:
                print(f"Motor {engine} no requiere reset manual de secuencia.")
        
        print("Base de datos preparada para la migración.")
        
    except Exception as e:
        logging.error(f"Error en reset_detalle_recibo: {e}")
        raise

def precargar_facturas():
    """Precarga todas las facturas en diccionarios para búsqueda rápida"""
    print("\nPrecargando facturas en memoria...")
    logging.info("Precargando facturas en memoria...")
    
    # Diccionario para búsqueda por compro + letra + numero
    facturas_por_comprobante = {}
    
    # Diccionario para búsqueda por número de recibo (numero_comprobante)
    facturas_por_recibo = {}
    
    # Cargar todas las facturas una sola vez
    todas_facturas = Factura.objects.all().values(
        'id_factura', 
        'compro', 
        'letra_comprobante', 
        'numero_comprobante'
    )
    
    total_facturas = todas_facturas.count()
    print(f"Cargando {total_facturas:,} facturas...")
    
    for factura in todas_facturas:
        # Clave para búsqueda por compro+letra+numero
        if factura['compro'] and factura['letra_comprobante'] and factura['numero_comprobante']:
            clave_comprobante = (
                factura['compro'].strip().upper(),
                factura['letra_comprobante'].strip().upper(),
                factura['numero_comprobante']
            )
            facturas_por_comprobante[clave_comprobante] = factura['id_factura']
        
        # Clave para búsqueda por recibo (numero_comprobante)
        if factura['numero_comprobante']:
            facturas_por_recibo[factura['numero_comprobante']] = factura['id_factura']
    
    print(f"✅ Facturas precargadas: {len(facturas_por_comprobante):,} para búsqueda por comprobante")
    print(f"✅ Facturas precargadas: {len(facturas_por_recibo):,} para búsqueda por recibo")
    logging.info(f"Facturas precargadas - Comprobante: {len(facturas_por_comprobante)}, Recibo: {len(facturas_por_recibo)}")
    
    return facturas_por_comprobante, facturas_por_recibo

def ejecutar_migracion():
    """Función principal de migración"""
    logging.info("=" * 60)
    logging.info("INICIO DE MIGRACIÓN DE DETALLE RECIBO")
    logging.info("=" * 60)
    
    # 1. Resetear datos existentes
    reset_detalle_recibo()
    
    # 2. Precargar facturas en memoria para búsqueda rápida
    facturas_por_comprobante, facturas_por_recibo = precargar_facturas()
    
    # 3. Configuración de procesamiento por lotes
    dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'RECIBOS.DBF')
    
    # Verificar que el archivo DBF existe
    if not os.path.exists(dbf_path):
        error_msg = f"No se encontró el archivo DBF en: {dbf_path}"
        logging.error(error_msg)
        print(f"\nERROR: {error_msg}")
        return
    
    # Leer el archivo DBF
    print(f"\n📂 Leyendo archivo DBF: {dbf_path}")
    table = DBF(dbf_path, encoding='latin-1', load=False)
    total_dbf = len(table)
    
    print(f"📊 Total de registros en DBF: {total_dbf:,}")
    logging.info(f"Total de registros en DBF: {total_dbf}")
    print("=" * 60)
    
    batch = []
    total_creados = 0
    errores = 0
    errores_detalle = []
    errores_por_desbordamiento = []  # Lista específica para errores de desbordamiento
    start_time = time.time()
    
    for idx, record in enumerate(table):
        current_idx = idx + 1
        
        try:
            # Obtener valores del registro DBF con funciones seguras
            compro = safe_string(record.get('COMPRO'), '').upper()
            letra = safe_string(record.get('LETRA'), '').upper()
            numero = safe_int(record.get('NUMERO'), 0)
            recibo = safe_int(record.get('RECIBO'), 0)
            
            # Obtener el valor original de cobrado para debugging
            cobrado_raw = record.get('COBRADO')
            cobrado_original = cobrado_raw
            if isinstance(cobrado_raw, bytes):
                # Limpiar bytes nulos para mostrar
                cobrado_original = cobrado_raw.replace(b'\x00', b'').strip()
                if cobrado_original:
                    try:
                        cobrado_original = cobrado_original.decode('latin-1')
                    except:
                        cobrado_original = str(cobrado_raw)
            
            # Convertir cobrado usando safe_decimal que valida el tamaño
            try:
                cobrado = safe_decimal(cobrado_raw, max_digits=12, decimal_places=2)
                # Verificar si el valor es demasiado grande (más de 10^10)
                if abs(cobrado) >= Decimal('10000000000'):  # 10^10
                    raise ValueError(f"Valor {cobrado} excede el límite de 10^10")
            except Exception as e:
                # Error específico de desbordamiento
                error_desbordamiento = {
                    'fila': current_idx,
                    'compro': compro,
                    'letra': letra,
                    'numero': numero,
                    'recibo': recibo,
                    'cobrado_original': cobrado_original,
                    'cobrado_convertido': str(cobrado) if 'cobrado' in locals() else 'No se pudo convertir',
                    'error': str(e)
                }
                errores_por_desbordamiento.append(error_desbordamiento)
                errores += 1
                mensaje_error = (f"Fila {current_idx}: DESBORDAMIENTO CAMPO NUMÉRICO - "
                               f"COMPRO='{compro}', LETRA='{letra}', NUMERO={numero}, "
                               f"RECIBO={recibo}, COBRADO_RAW='{cobrado_original}'")
                errores_detalle.append(mensaje_error)
                logging.warning(mensaje_error)
                continue
            
            # Validar que los campos requeridos no estén vacíos
            if not compro or not letra or numero == 0:
                errores += 1
                mensaje_error = f"Fila {current_idx}: Campos incompletos - COMPRO='{compro}', LETRA='{letra}', NUMERO={numero}"
                errores_detalle.append(mensaje_error)
                logging.warning(mensaje_error)
                continue
            
            # Buscar id_factura (por compro + letra + numero)
            clave_comprobante = (compro, letra, numero)
            id_factura = facturas_por_comprobante.get(clave_comprobante)
            
            if not id_factura:
                errores += 1
                mensaje_error = f"Fila {current_idx}: No se encontró Factura con COMPRO='{compro}', LETRA='{letra}', NUMERO={numero}"
                errores_detalle.append(mensaje_error)
                logging.warning(mensaje_error)
                continue
            
            # Buscar id_factura_cobrada (por recibo)
            id_factura_cobrada = None
            if recibo > 0:
                id_factura_cobrada = facturas_por_recibo.get(recibo)
                if not id_factura_cobrada:
                    mensaje_error = f"Fila {current_idx}: No se encontró Factura Cobrada con RECIBO={recibo}"
                    errores_detalle.append(mensaje_error)
                    logging.warning(mensaje_error)
                    # Continuamos aunque no se encuentre la factura cobrada
            
            # Crear instancia de DetalleRecibo
            detalle_recibo = DetalleRecibo(
                id_factura_id=id_factura,
                id_factura_cobrada_id=id_factura_cobrada if id_factura_cobrada else None,
                monto_cobrado=cobrado,
                saldo_factura=0.00,  # Valor por defecto
                observaciones_recibo=None  # No hay campo equivalente en origen
            )
            batch.append(detalle_recibo)
            
            # Guardar lote
            if len(batch) >= BATCH_SIZE:
                DetalleRecibo.objects.bulk_create(batch)
                total_creados += len(batch)
                batch = []
                porcentaje = (current_idx / total_dbf) * 100
                elapsed = time.time() - start_time
                speed = total_creados / elapsed if elapsed > 0 else 0
                print(f"✅ Lote Guardado | Progreso: {current_idx:,}/{total_dbf:,} ({porcentaje:.1f}%) | Total OK: {total_creados:,} | Errores: {errores} | Velocidad: {speed:.1f} reg/s")
            
            # Feedback visual cada 500 registros
            elif current_idx % 500 == 0:
                porcentaje = (current_idx / total_dbf) * 100
                print(f"⏳ Leyendo... {current_idx:,}/{total_dbf:,} ({porcentaje:.1f}%) | En memoria: {len(batch)} | Errores: {errores}")
        
        except Exception as e:
            errores += 1
            mensaje_error = f"Fila {current_idx}: EXCEPCION GENERAL - {str(e)}"
            errores_detalle.append(mensaje_error)
            logging.error(mensaje_error)
            continue
    
    # Guardar registros finales
    if batch:
        DetalleRecibo.objects.bulk_create(batch)
        total_creados += len(batch)
        print(f"✅ Lote Final Guardado | Total Final OK: {total_creados:,}")
    
    total_time = time.time() - start_time
    
    # Guardar informe detallado de errores de desbordamiento
    if errores_por_desbordamiento:
        with open('desbordamientos_detalle.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"REGISTROS CON DESBORDAMIENTO NUMÉRICO (Total: {len(errores_por_desbordamiento)})\n")
            f.write("=" * 80 + "\n\n")
            for err in errores_por_desbordamiento:
                f.write(f"Fila: {err['fila']}\n")
                f.write(f"  COMPRO: '{err['compro']}'\n")
                f.write(f"  LETRA: '{err['letra']}'\n")
                f.write(f"  NUMERO: {err['numero']}\n")
                f.write(f"  RECIBO: {err['recibo']}\n")
                f.write(f"  COBRADO (original): {err['cobrado_original']}\n")
                f.write(f"  COBRADO (convertido): {err['cobrado_convertido']}\n")
                f.write(f"  Error: {err['error']}\n")
                f.write("-" * 80 + "\n")
        
        print(f"\n⚠️ Se generó el archivo 'desbordamientos_detalle.txt' con {len(errores_por_desbordamiento)} registros que causaron desbordamiento")
    
    # Guardar resumen de errores al final
    if errores_detalle:
        logging.info("=" * 60)
        logging.info(f"RESUMEN DE ERRORES ({len(errores_detalle)} errores):")
        logging.info("=" * 60)
        for err in errores_detalle[:100]:  # Mostrar primeros 100 errores
            logging.info(err)
        if len(errores_detalle) > 100:
            logging.info(f"... y {len(errores_detalle) - 100} errores más")
    
    print("\n" + "=" * 60)
    print(f"🏁 MIGRACIÓN COMPLETADA")
    print(f"⏱️ Tiempo total: {int(total_time // 60)}m {int(total_time % 60)}s")
    print(f"✅ Registros insertados: {total_creados:,}")
    print(f"❌ Registros con error: {errores:,}")
    print(f"📊 Total procesados: {total_creados + errores:,}/{total_dbf:,}")
    print(f"📈 Tasa de éxito: {(total_creados/total_dbf*100):.2f}%")
    print("=" * 60)
    
    logging.info("=" * 60)
    logging.info(f"MIGRACIÓN COMPLETADA")
    logging.info(f"Tiempo total: {int(total_time // 60)}m {int(total_time % 60)}s")
    logging.info(f"Registros insertados: {total_creados}")
    logging.info(f"Registros con error: {errores}")
    logging.info("=" * 60)
    
    # Cerrar handlers de logging
    for handler in logging.root.handlers[:]:
        handler.close()
    
    print(f"\n📁 Revisa los archivos generados:")
    print(f"   - 'detalle_recibo_errores.log' para todos los errores")
    print(f"   - 'desbordamientos_detalle.txt' para detalles de los desbordamientos numéricos")

if __name__ == '__main__':
    ejecutar_migracion()
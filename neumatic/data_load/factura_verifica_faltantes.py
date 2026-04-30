import os
import sys
import django
import time
import logging
from dbfread import DBF
from django.db import connection
from django.db import transaction
from datetime import date

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.ventas.models.factura_models import Factura

# Configuración de logging
logging.basicConfig(
    filename='factura_migra2.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def verificar_registros_faltantes():
    """Verifica qué registros del DBF no se migraron correctamente"""
    try:
        start_time = time.time()
        
        # 1. Obtener todos los IDs migrados
        ids_migrados = set(Factura.objects.values_list('id_factura', flat=True))
        logger.info(f"Total IDs migrados: {len(ids_migrados)}")
        
        # 2. Procesar el archivo DBF completo
        dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'facturas.DBF')
        table = DBF(dbf_path, encoding='latin-1')
        
        registros_faltantes = 0
        total_registros_dbf = 0
        max_id_dbf = 0
        
        # 3. Configurar archivo para detalles de registros faltantes
        with open('registros_faltantes_detalle.log', 'w') as detalle_file:
            detalle_file.write("ID,COMPRO,NUMERO,FECHA,CLIENTE\n")
            
            for record in table:
                try:
                    id_registro = int(record['ID'])
                    total_registros_dbf += 1
                    
                    if id_registro > max_id_dbf:
                        max_id_dbf = id_registro
                    
                    # Verificar si el ID existe en los migrados
                    if id_registro not in ids_migrados:
                        registros_faltantes += 1
                        # Escribir detalles del registro faltante
                        detalle_file.write(
                            f"{id_registro},"
                            f"{record.get('COMPRO', '')},"
                            f"{record.get('NUMERO', '')},"
                            f"{record.get('FECHA', '')},"
                            f"{record.get('CLIENTE', '')}\n"
                        )
                        
                except (ValueError, KeyError) as e:
                    logger.error(f"Error procesando registro: {str(e)}")
                    continue
        
        # 4. Resultados finales
        max_id_migrado = max(ids_migrados) if ids_migrados else 0
        
        logger.info("\n=== RESULTADOS DE VERIFICACIÓN ===")
        logger.info(f"Total registros en DBF: {total_registros_dbf}")
        logger.info(f"Total registros migrados: {len(ids_migrados)}")
        logger.info(f"Registros faltantes: {registros_faltantes}")
        logger.info(f"Máximo ID en DBF: {max_id_dbf}")
        logger.info(f"Máximo ID migrado: {max_id_migrado}")
        logger.info(f"Tiempo total: {time.time() - start_time:.2f} segundos")
        
        print("\nResumen de verificación:")
        print(f"Registros en DBF: {total_registros_dbf}")
        print(f"Registros migrados: {len(ids_migrados)}")
        print(f"Registros faltantes: {registros_faltantes}")
        print(f"Detalles en 'registros_faltantes_detalle.log'")
        
        if registros_faltantes > 0:
            print("\n¡ADVERTENCIA! Se encontraron registros faltantes")
            print("Revise el archivo 'registros_faltantes_detalle.log' para detalles")
        
    except Exception as e:
        logger.error(f"Error en verificar_registros_faltantes: {str(e)}")
        raise

if __name__ == '__main__':
    verificar_registros_faltantes()
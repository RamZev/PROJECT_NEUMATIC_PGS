import os
import sys
import django
import time  # Para medir el tiempo de procesamiento
from dbfread import DBF
from django.db import connection
from datetime import date

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.base_models import ComprobanteVenta, ProductoDeposito
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.cliente_models import Cliente
from apps.ventas.models.factura_models import Factura

def reset_factura():
	"""Elimina los datos existentes en la tabla Factura y resetea su ID en SQLite."""
	# Factura.objects.all().delete()
	
	with connection.cursor() as cursor:
		pass
		# cursor.execute("DELETE FROM sqlite_sequence WHERE name='factura';")

def cargar_datos_factura():
	"""Lee los datos de la tabla factura.DBF y migra los datos al modelo Factura."""
	reset_factura()

	# Ruta de la tabla de Visual FoxPro
	dbf_path = os.path.join(BASE_DIR, 'data_load', 'datavfox', 'facturas.DBF')

	# Abrir la tabla de Visual FoxPro usando dbfread
	# table = DBF(dbf_path, encoding='latin-1')
	table = sorted(DBF(dbf_path, encoding='latin-1'), key=lambda x: x['ID'])
		
	# codigo_inicio = 1498293
	#codigo_inicio = 1550327
	codigo_inicio = 1
	
	# Filtrar los registros a partir del código inicial
	table = [record for record in table if int(record['ID']) >= codigo_inicio]
	total_registros = len(table)
	print(f"Total de registros a procesar: {total_registros}")

	print("Inicio del ciclo for****")
	
	for idx, record in enumerate(table):
		# Extraer y procesar los datos según las reglas
		
		# Obtener el ID del comprobante de venta del registro origen
		compro = record.get('COMPRO', None)
		compro_id = ComprobanteVenta.objects.filter(codigo_comprobante_venta=compro).first() if compro else None
		
		if compro_id:
			compro_id = compro_id.id_comprobante_venta
		else:
			compro_id = None
  
		if compro_id:
			try:
				id_comprobante_venta_instancia = ComprobanteVenta.objects.get(pk=compro_id)
			except (ComprobanteVenta.DoesNotExist, ValueError):
				id_comprobante_venta_instancia = None
		else:
			id_comprobante_venta_instancia = None
		
		# Obtener instancias predeterminadas para claves foráneas
		sucursal_id = record.get('SUCURSAL', None)
		try:
			id_sucursal_instancia = Sucursal.objects.get(pk=sucursal_id)
		except (Sucursal.DoesNotExist, ValueError):
			id_sucursal_instancia = None

		deposito_id = record.get('DEPOSITO', None)
		try:
			id_deposito_instancia = ProductoDeposito.objects.get(pk=deposito_id)
		except (ProductoDeposito.DoesNotExist, ValueError):
			id_deposito_instancia = None
		
		# Obtener el ID del cliente del registro origen
		cliente_id = record.get('CLIENTE', None)
		try:
			id_cliente_instancia = Cliente.objects.get(pk=cliente_id)
		except (Cliente.DoesNotExist, ValueError):
			id_cliente_instancia = None
		
		codigo_origen = record.get('ID', 0)
		Factura.objects.create(
			id_factura=int(codigo_origen),
			id_orig=int(codigo_origen),
			estatus_comprobante=bool(record.get('TRUE', False)),
			id_sucursal=id_sucursal_instancia,
			id_comprobante_venta=id_comprobante_venta_instancia,
			compro=record.get('COMPRO', '').strip(),
			letra_comprobante=record.get('LETRA', '').strip(),
			numero_comprobante=int(record.get('NUMERO', 0)),
			remito=record.get('REMITO', '').strip(),
			fecha_comprobante=record.get('FECHA', date.today()),
			id_cliente=id_cliente_instancia,
			cuit=record.get('CUIT', 0),
			condicion_comprobante=int(record.get('CONDICION', 0)),
			# gravado=float(record.get('GRAVADO', 0)),
			gravado=float(record.get('GRAVADO') or 0),
			exento=float(record.get('EXENTO') or 0),
			iva=float(record.get('IVA') or 0),
			percep_ib = float(record.get('PERCEPIB', 0)) if record.get('PERCEPIB') is not None else 0,
			total=float(record.get('TOTAL', 0)),
			entrega = float(record.get('ENTREGA', 0)) if record.get('ENTREGA') is not None else 0,
			estado=record.get('ESTADO', '').strip(),
			marca=record.get('MARCA', '').strip(),
			fecha_pago=record.get('FECHA_PAGO', None),  # Se usa el nombre correcto del campo
			no_estadist=bool(record.get('NO_ESTADIST', False)),  # Se usa el nombre correcto del campo
			suc_imp=int(record.get('SUC_IMP', 0)),  # Se usa el nombre correcto del campo
			cae=record.get('CAE', 0),
			cae_vto=record.get('CAE_VTO', None),  # Se usa el nombre correcto del campo
			observa_comprobante=record.get('OBSERVACIONES', '').strip(),
			stock_clie=bool(record.get('STOCKCLIE', False)),  # Se usa el nombre correcto del campo
			id_deposito=id_deposito_instancia,
			promo=bool(record.get('PROMO', False))
		)
		
		# Mostrar mensaje cada 100 registros procesados
		if (idx + 1) % 1000 == 0:
			print(f"{idx + 1} registros procesados...")

if __name__ == '__main__':
	start_time = time.time()  # Empezar el control de tiempo
	cargar_datos_factura()
	end_time = time.time()  # Terminar el control de tiempo

	# Calcular el tiempo total en minutos y segundos
	elapsed_time = end_time - start_time
	minutes = elapsed_time // 60
	seconds = elapsed_time % 60

	print(f"Migración de Factura completada.")
	print(f"Tiempo de procesamiento: {int(minutes)} minutos y {int(seconds)} segundos.")

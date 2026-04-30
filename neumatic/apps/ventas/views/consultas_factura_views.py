# neumatic\apps\ventas\views\consultas_factura_views.py
from asyncio.log import logger
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from datetime import date, timedelta
import traceback
import json

from apps.maestros.models.base_models import (
	ProductoStock,
	ProductoMinimo,
	ComprobanteVenta,
	Banco
)
from apps.ventas.models.factura_models import Factura, DetalleFactura
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.cliente_models import Cliente
from apps.maestros.models.base_models import ComprobanteVenta
from apps.maestros.models.descuento_vendedor_models import DescuentoVendedor, DescuentoRevendedor
from apps.maestros.models.numero_models import Numero
from apps.maestros.models.valida_models import Valida


def buscar_producto(request):
	# Capturar parámetros de la solicitud
	medida = request.GET.get('medida', '')
	nombre = request.GET.get('nombre', '')
	cai = request.GET.get('cai', '')
	filtro_marca = request.GET.get('filtro_marca', 'primeras')  # Valor por defecto
	id_cliente = request.GET.get('id_cliente', None)
	
	
	# Obtener el vendedor asociado al cliente
	vendedor = None
	col_descuento = 0  # Valor por defecto
	tipo_venta = None
	if id_cliente:
		cliente = Cliente.objects.filter(id_cliente=id_cliente).select_related("id_vendedor").first()
		if cliente and cliente.id_vendedor:
			vendedor = cliente.id_vendedor
			col_descuento = vendedor.col_descuento  # Obtener columna de descuento
			tipo_venta = vendedor.tipo_venta 
			
			print("col_descuento", col_descuento)

	# Realizar la consulta inicial
	# productos = Producto.objects.all()
	productos = Producto.objects.filter(estatus_producto=True)

	# Aplicar filtros dinámicamente
	if medida:
		productos = productos.filter(medida__icontains=medida)
	if nombre:
		productos = productos.filter(nombre_producto__icontains=nombre)
	if cai:
		productos = productos.filter(id_cai__descripcion_cai__icontains=cai)
		
	# Aplicar filtro de marcas o stock
	if filtro_marca == "primeras":
		productos = productos.filter(id_marca__principal=True)
	elif filtro_marca == "otras":
		print("Entró a otras")
		productos = productos.filter(id_marca__principal__in=[False, None])
	elif filtro_marca == "stock":
		print("stock")
		productos = productos.annotate(total_stock=Sum("productostock__stock")).filter(total_stock__gt=0)

	# Preparar los datos de respuesta usando lista por comprensión
	resultados = []
	for producto in productos:
		# Filtrar los descuentos del vendedor por marca y familia
		dv = None
		if col_descuento > 0:
			dv = DescuentoVendedor.objects.filter(
				id_marca=producto.id_marca.id_producto_marca, 
				id_familia=producto.id_familia.id_producto_familia
			).first()
		
		# Obtener el valor del campo dinámico usando getattr
		descuento = 0
		if dv and col_descuento > 0:
			descuento_field = f"desc{col_descuento}"
			descuento = getattr(dv, descuento_field, 0)  # Devuelve 0 si el campo no existe

		# NUEVO: Descuento de revendedor (solo si tipo_venta == "R")
		descuento_revendedor = 0
		
		# print("tipo_venta:", tipo_venta)
		# print("producto.id_marca.id_producto_marca:", producto.id_marca.id_producto_marca)
		# print("producto.id_familia.id_producto_familia:", producto.id_familia.id_producto_familia)
		if tipo_venta == "R":  # Solo para revendedores
			dr = DescuentoRevendedor.objects.filter(
				id_marca=producto.id_marca.id_producto_marca,
				id_familia=producto.id_familia.id_producto_familia,
				estatus_descuento_revendedor=True
			).first()
			
			if dr and dr.descuento:
				# print("tipo_venta2:", tipo_venta)
				descuento_revendedor = float(dr.descuento)
		# Descuento de revendedor FIN

		resultados.append({
			'id': producto.id_producto,
			'codigo': producto.codigo_producto,
			'marca': producto.id_marca.nombre_producto_marca if producto.id_marca else 'Sin marca',
			'medida': producto.medida,
			'cai': producto.id_cai.descripcion_cai if producto.id_cai else 'Sin CAI',
			'nombre': producto.nombre_producto,
			'precio': producto.precio,
			'stock': ProductoStock.objects.filter(id_producto=producto).aggregate(total_stock=Sum('stock'))['total_stock'] or 0,
			'minimo': producto.minimo,
			'id_marca': producto.id_marca.id_producto_marca if producto.id_marca else None,
			'id_familia': producto.id_familia.id_producto_familia if producto.id_familia else None,
			'descuento_vendedor': descuento,
			'descuento_revendedor': descuento_revendedor,
			'id_alicuota_iva': producto.id_alicuota_iva_id if producto.id_alicuota_iva else None,
			'alicuota_iva': producto.alicuota_iva,
			'tipo_producto': producto.tipo_producto,
			'obliga_operario': producto.obliga_operario,
		})

	print("Productos:", resultados)
	# Devolver los resultados como JSON
	return JsonResponse(resultados, safe=False)

def detalle_producto(request, id_producto):
	producto = get_object_or_404(Producto, id_producto=id_producto)

	# Obtener stock por depósito
	stock_por_deposito = ProductoStock.objects.filter(id_producto=producto).select_related('id_deposito')
	stock_data = [
		{
			'deposito': stock.id_deposito.nombre_producto_deposito,
			'stock': stock.stock
		}
		for stock in stock_por_deposito
	]
	
	# print("stock_por_deposito", stock_por_deposito)
	
	# Obtener mínimos por depósito (usando id_cai)
	minimos_por_deposito = ProductoMinimo.objects.filter(id_cai=producto.id_cai).select_related('id_deposito')
	minimos_data = [
		{
			'deposito': minimo.id_deposito.nombre_producto_deposito,
			'minimo': minimo.minimo
		}
		for minimo in minimos_por_deposito
	]

	return JsonResponse({'stock': stock_data, 'minimos': minimos_data})


def validar_documento(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		print("Validando!")
		
		nro_doc_identidad = data.get('nro_doc_identidad')
		print(nro_doc_identidad)

		# Busca el documento en el modelo Cliente
		try:
			agenda = Cliente.objects.filter(cuit=nro_doc_identidad).first()
			
			if agenda:
				print("Aquí es cliente:", agenda.nombre_cliente)
				print("Aquí es domicilio:", agenda.domicilio_cliente)
				
				response_data = {
					'exists': True,
					'nombre_receptor': agenda.nombre_cliente,
					'domicilio_receptor': agenda.domicilio_cliente
				}
			else:
				response_data = {
					'exists': False
				}
		except Exception as e:
			print(f"Error al validar documento: {e}")
			response_data = {
				'exists': False,
				'error': 'Error al validar el documento'
			}

		return JsonResponse(response_data)

	
# Búsqueda en Agenda para la ventana Modal de Factura
def buscar_agenda(request):
	busqueda_general = request.GET.get('busqueda_general', '')
	print("Entro a buscar el Cliente")

	try:
		id_cliente = int(busqueda_general)
		clientes = Cliente.objects.filter(
			Q(id_cliente=id_cliente) |
			Q(cuit=id_cliente) |
			Q(nombre_cliente__icontains=busqueda_general)
		)
	except ValueError:
		clientes = Cliente.objects.filter(
			Q(nombre_cliente__icontains=busqueda_general)
		)

	resultados = clientes.values(
		'id_cliente',
		'cuit',
		'nombre_cliente',
		'domicilio_cliente',
		'codigo_postal',
		'movil_cliente',
		'email_cliente',
		'id_vendedor',
		'id_vendedor__nombre_vendedor',
		'id_vendedor__tipo_venta',
		'id_tipo_iva__nombre_iva',
		'id_tipo_iva__discrimina_iva',        
		'condicion_venta',
		'id_sucursal',
		'vip',
		'mayorista',
		'sub_cuenta',
		'observaciones_cliente',
		'black_list',
		'black_list_motivo',
	)

	#print("resultados", resultados)

	return JsonResponse(list(resultados), safe=False)


def buscar_cliente(request):
	busqueda = request.GET.get('busqueda', '').strip()
	
	# print("busqueda", busqueda)

	# Si el input está vacío, no hacer búsqueda
	if not busqueda:
		return JsonResponse({'error': 'No se proporcionó un criterio de búsqueda'}, status=400)

	try:
		# Intentamos convertir a entero para buscar por ID o CUIT
		busqueda_num = int(busqueda)
		cliente = Cliente.objects.filter(
			Q(id_cliente=busqueda_num) | Q(cuit=busqueda_num)
		).first()
	except ValueError:
		# Si no es un número, devolvemos error
		return JsonResponse({'error': 'Solo se permiten valores numéricos'}, status=400)

	if cliente:
		response_data = {
			'id_cliente': cliente.id_cliente,
			'cuit': cliente.cuit,
			'nombre': cliente.nombre_cliente,
			'direccion': cliente.domicilio_cliente,
			'movil': cliente.movil_cliente,
			'email': cliente.email_cliente,
			'id_vendedor': cliente.id_vendedor.id_vendedor if cliente.id_vendedor else None,
			'nombre_vendedor': cliente.id_vendedor.nombre_vendedor if cliente.id_vendedor else "Sin asignar",
			'tipo_venta': cliente.id_vendedor.tipo_venta,
			'nombre_iva': cliente.id_tipo_iva.nombre_iva,
			'discrimina_iva': cliente.id_tipo_iva.discrimina_iva,
			'condicion_venta': cliente.condicion_venta,
			'id_sucursal': cliente.id_sucursal.id_sucursal,
			'vip': cliente.vip,
			'mayorista': cliente.mayorista,
			'sub_cuenta': cliente.sub_cuenta,
			'observaciones': cliente.observaciones_cliente,
			'black_list': cliente.black_list,
			'black_list_motivo': cliente.black_list_motivo
		}
	else:
		response_data = {'error': 'No se encontraron resultados'}
		
	print("response_data", response_data)

	return JsonResponse(response_data)


def datos_comprobante(request, pk):
	try:
		comprobante = ComprobanteVenta.objects.get(pk=pk)
		
		# print("Entramos a la vista:", comprobante.compro_asociado)
		
		return JsonResponse({
			'codigo': comprobante.codigo_comprobante_venta,
			'es_remito': comprobante.remito,
			'es_pendiente': comprobante.pendiente,
			'es_presupuesto': comprobante.presupuesto,
			'compro_asociado': comprobante.compro_asociado
		})
	except ComprobanteVenta.DoesNotExist:
		return JsonResponse({'error': 'Comprobante no encontrado'}, status=404)
	

# Obtener número de comprobante
@require_GET
def obtener_numero_comprobante(request):
	# Obtener parámetros de la solicitud
	id_sucursal = request.GET.get('id_sucursal')
	id_punto_venta = request.GET.get('id_punto_venta')
	comprobante = request.GET.get('comprobante')
	letra = request.GET.get('letra')

	if not all([id_sucursal, id_punto_venta, comprobante, letra]):
		return JsonResponse({'error': 'Faltan parámetros requeridos'}, status=400)

	try:
		# Obtener el último número registrado
		ultimo_numero = Numero.objects.filter(
			id_sucursal=id_sucursal,
			id_punto_venta=id_punto_venta,
			comprobante=comprobante,
			letra=letra
		).order_by('-numero').first()
		

		# Si no hay registros, devolver un mensaje específico
		if not ultimo_numero:
			return JsonResponse({
				'success': False,
				'message': '*No se puede obtener la numeración de este comprobante, consulte al Administrador del Sistema!',
			})

		numero_referencial = ultimo_numero.numero + 1
		numero_definitivo = numero_referencial  # Por defecto son iguales

		return JsonResponse({
			'numero_referencial': numero_referencial,
			'numero_definitivo': numero_definitivo,
			'success': True
		})

	except Exception as e:
		return JsonResponse({
			'error': str(e),
			'success': False
		}, status=500)


def validar_vencimientos_cliente(request, cliente_id):
	try:
		cliente = Cliente.objects.filter(pk=cliente_id).first()
		if not cliente:
			return JsonResponse({'error': 'Cliente no encontrado', 'requiere_autorizacion': False}, status=404)

		# 1. Primero buscar factura en cuenta corriente 
		factura_antigua = Factura.objects.filter(
			id_cliente_id=cliente_id,
			condicion_comprobante=2,
			total__gt=0
		).exclude(
			total=F('entrega')
		).select_related('id_vendedor', 'id_comprobante_venta'
		).order_by('fecha_comprobante').first()

		if factura_antigua:
			dias_credito = factura_antigua.id_vendedor.vence_factura if factura_antigua.id_vendedor else 0
			fecha_vencimiento = factura_antigua.fecha_comprobante + timedelta(days=dias_credito)
			dias_vencidos = (date.today() - fecha_vencimiento).days

			return JsonResponse({
				'requiere_autorizacion': dias_vencidos > 0,
				'datos_comprobante': {
					'tipo_comprobante': factura_antigua.id_comprobante_venta.nombre_comprobante_venta if factura_antigua.id_comprobante_venta else 'N/A',
					'letra_comprobante': factura_antigua.letra_comprobante or 'N/A',
					'numero_comprobante': factura_antigua.numero_comprobante or 'N/A',
					'fecha_comprobante': factura_antigua.fecha_comprobante.strftime('%d/%m/%Y') if factura_antigua.fecha_comprobante else 'N/A',
					'dias_credito': dias_credito,
					'fecha_vencimiento': fecha_vencimiento.strftime('%d/%m/%Y') if fecha_vencimiento else 'N/A',
					'dias_vencidos': dias_vencidos,
					'monto_pendiente': float((factura_antigua.total or 0) - (factura_antigua.entrega or 0)),
					'vendedor': factura_antigua.id_vendedor.nombre_vendedor if factura_antigua.id_vendedor else 'No asignado'
				}
			})

		# 2. Solo si no hay factura pendiente, buscar remito (nueva lógica)
		remito_pendiente = Factura.objects.filter(
			id_cliente_id=cliente_id,
			estado="",
			id_comprobante_venta__mult_venta=0,
			id_comprobante_venta__mult_stock__lt=0
		).select_related('id_vendedor', 'id_comprobante_venta'
		).order_by('fecha_comprobante').first()

		if remito_pendiente:
			dias_credito = remito_pendiente.id_vendedor.vence_remito if remito_pendiente.id_vendedor else 0
			fecha_vencimiento = remito_pendiente.fecha_comprobante + timedelta(days=dias_credito)
			dias_vencidos = (date.today() - fecha_vencimiento).days

			return JsonResponse({
				'requiere_autorizacion': dias_vencidos > 0,
				'datos_comprobante': {
					'tipo_comprobante': remito_pendiente.id_comprobante_venta.nombre_comprobante_venta if remito_pendiente.id_comprobante_venta else 'N/A',
					'letra_comprobante': remito_pendiente.letra_comprobante or 'N/A',
					'numero_comprobante': remito_pendiente.numero_comprobante or 'N/A',
					'fecha_comprobante': remito_pendiente.fecha_comprobante.strftime('%d/%m/%Y') if remito_pendiente.fecha_comprobante else 'N/A',
					'dias_credito': dias_credito,
					'fecha_vencimiento': fecha_vencimiento.strftime('%d/%m/%Y') if fecha_vencimiento else 'N/A',
					'dias_vencidos': dias_vencidos,
					'monto_pendiente': 0,  # Remitos no tienen monto pendiente
					'vendedor': remito_pendiente.id_vendedor.nombre_vendedor if remito_pendiente.id_vendedor else 'No asignado'
				}
			})

		# Si no hay ningún documento pendiente
		return JsonResponse({'requiere_autorizacion': False})
	
	except Exception as e:
		print(f"Error completo en validar_vencimientos_cliente - Cliente ID: {cliente_id}: {str(e)}", exc_info=True)
		return JsonResponse({
			'error': 'Error interno al validar vencimientos',
			'requiere_autorizacion': True,  # Importante: fallar hacia la seguridad
			'detalle_error': str(e),
			'cliente_id': cliente_id  # Para debugging
		}, status=500)

	
@require_POST
def valida_autorizacion(request):
	if request.method != 'POST':
		return JsonResponse({'valido': False, 'mensaje': 'Método no permitido'}, status=405)
	
	try:
		data = json.loads(request.body)
		codigo = str(data.get('codigo', '')).strip()
		cliente_id = data.get('cliente_id')
		sucursal_id = data.get('sucursal_id')
		fecha_comprobante = data.get('fecha_comprobante')
		
		'''
		print("Datos recibidos:")
		print(f"Código: {codigo}")
		print(f"Cliente ID: {cliente_id}")
		print(f"Sucursal ID: {sucursal_id}")
		print(f"Fecha Comprobante: {fecha_comprobante}")
		'''

		# Validación básica del código
		if not codigo.isdigit() or int(codigo) <= 0:
			return JsonResponse({
				'valido': False,
				'mensaje': 'El código debe ser un entero positivo'
			}, status=400)

		# Buscar autorización
		try:
			autorizacion = Valida.objects.get(
				id_valida=int(codigo),
				estatus_valida=True
			)
			print("Autorización encontrada:", autorizacion)
		except Valida.DoesNotExist:
			return JsonResponse({
				'valido': False,
				'mensaje': 'Autorización no encontrada o inactiva'
			}, status=404)

		# Validar coincidencias (versión optimizada)
		errores = []
		
		# Comparación de sucursal (usa id_sucursal_id para evitar JOIN innecesario)
		if str(autorizacion.id_sucursal_id) != str(sucursal_id):
			errores.append(f'Sucursal no coincide (BD: {autorizacion.id_sucursal_id} vs Recibido: {sucursal_id})')
			
		# Comparación de cliente (usa id_cliente_id)
		if str(autorizacion.id_cliente_id) != str(cliente_id):
			errores.append(f'Cliente no coincide (BD: {autorizacion.id_cliente_id} vs Recibido: {cliente_id})')
			
		# Comparación de fecha (formato YYYY-MM-DD)
		if fecha_comprobante:
			fecha_bd = autorizacion.fecha_valida.strftime('%Y-%m-%d') if autorizacion.fecha_valida else None
			if fecha_bd != fecha_comprobante:
				errores.append(f'Fecha no coincide (BD: {fecha_bd} vs Recibido: {fecha_comprobante})')

		if errores:
			print("Errores de validación:", errores)
			return JsonResponse({
				'valido': False,
				'mensaje': ' | '.join(errores),
				'detalle': {
					'sucursal_bd': autorizacion.id_sucursal_id,
					'cliente_bd': autorizacion.id_cliente_id,
					'fecha_bd': autorizacion.fecha_valida.strftime('%Y-%m-%d') if autorizacion.fecha_valida else None
				}
			}, status=403)

		return JsonResponse({
			'valido': True,
			'mensaje': 'Autorización validada exitosamente',
			'datos_autorizacion': {
				'codigo': autorizacion.id_valida,
				'sucursal': autorizacion.id_sucursal_id,
				'cliente': autorizacion.id_cliente_id,
				'fecha': autorizacion.fecha_valida.strftime('%Y-%m-%d') if autorizacion.fecha_valida else None
			}
		})

	except Exception as e:
		print(f"Error interno: {str(e)}", exc_info=True)
		return JsonResponse({
			'valido': False,
			'mensaje': f'Error interno: {str(e)}'
		}, status=500)
		

@require_GET
@login_required
def verificar_remito(request):
	comprobante_remito = request.GET.get('comprobante_remito', '').strip()
	remito = request.GET.get('remito', '').strip()
	
	if not comprobante_remito or not remito:
		return JsonResponse(
			{'error': 'comprobante_remito y remito son requeridos'},
			status=400
		)

	try:
		# Búsqueda optimizada con first()
		factura = Factura.objects.filter(
			compro=comprobante_remito,
			numero_comprobante=remito,
		).filter(
			Q(estado="") | Q(estado__isnull=True)
		).select_related('id_comprobante_venta').only(
			'id_factura',
			'id_comprobante_venta__pendiente'
		).first()
		
		# print("factura.estado:", factura.estado, factura.compro, factura.numero_comprobante)
						
		if not factura:
			return JsonResponse({
				'existe': False,
				'id_factura': None,
				'pendiente': None,
				'detalles': []
			})


		# Obtener los detalles relacionados
		detalles = DetalleFactura.objects.filter(
			id_factura=factura.id_factura
		).select_related('id_producto').values(
			'id_producto',
			'id_producto__medida',
			'id_producto__tipo_producto',
			'id_producto__obliga_operario',
			'producto_venta',
			'cantidad',
			'precio',
			'precio_lista',
			'desc_vendedor',
			'descuento',
			'no_gravado',
			'gravado',
			'alic_iva',
			'iva',
			'total',
			'id_producto__id_alicuota_iva__alicuota_iva'
		)
		
		# Convertir el QuerySet a lista y asegurar valores decimales como float
		detalles_lista = []
		for detalle in detalles:
			detalle_dict = {
				'id_producto': detalle['id_producto'],
				'medida': detalle['id_producto__medida'],
				'nombre': detalle['producto_venta'],
				'cantidad': float(detalle['cantidad']),
				'precio': float(detalle['precio']),
				'precio_lista': float(detalle['precio_lista']),
				'desc_vendedor': float(detalle['desc_vendedor']),
				'descuento': float(detalle['descuento']),
				'gravado': float(detalle['gravado']),
				'no_gravado': float(detalle['no_gravado']),
				'alic_iva': float(detalle.get('id_producto__id_alicuota_iva__alicuota_iva', detalle['alic_iva'])),
				'iva': float(detalle['iva']),
				'total': float(detalle['total']),
				'tipo_producto': detalle['id_producto__tipo_producto'],
				'obliga_operario': detalle['id_producto__obliga_operario']
			}
			detalles_lista.append(detalle_dict)

		print(detalles_lista)

		return JsonResponse({
			'existe': True,
			'id_factura': factura.id_factura,
			'pendiente': factura.id_comprobante_venta.pendiente,
			'detalles': detalles_lista  # Convertimos el QuerySet a lista
		})

	except Exception as e:
		return JsonResponse(
			{'error': f'Error en el servidor: {str(e)}'},
			status=500
		)


# validar_deudas_cliente
@require_GET
@login_required
def validar_deudas_cliente(request, cliente_id):
	if not Cliente.objects.filter(id_cliente=cliente_id).exists():
		return JsonResponse({
			'success': True,
			'has_debts': False,
			'facturas_pendientes': [],
			'message': 'Cliente no encontrado o sin deudas pendientes'
		}, status=200)

	facturas_pendientes = Factura.objects.filter(
		id_cliente_id=cliente_id,
		id_comprobante_venta__mult_saldo__isnull=False,
		total__gt=F('entrega')
	).exclude(
		id_comprobante_venta__mult_saldo=0
	).select_related('id_comprobante_venta').values(
		'id_factura',
		'letra_comprobante',
		'numero_comprobante',
		'fecha_comprobante',
		'total',
		'entrega',
		'id_comprobante_venta__nombre_comprobante_venta'
	)

	resultados = []
	for factura in facturas_pendientes:
		factura_dict = {
			'id_factura': factura['id_factura'],
			'tipo_comprobante': factura['id_comprobante_venta__nombre_comprobante_venta'],
			'letra_comprobante': factura['letra_comprobante'] or 'N/A',
			'numero_comprobante': factura['numero_comprobante'] or 'N/A',
			'fecha_comprobante': factura['fecha_comprobante'].strftime('%d/%m/%Y') if factura['fecha_comprobante'] else 'N/A',
			'total': float(factura['total']),
			'entrega': float(factura['entrega']),
			'monto_pendiente': float(factura['total'] - factura['entrega']),
		}
		resultados.append(factura_dict)

	has_debts = len(resultados) > 0

	# print("resultados", resultados)

	return JsonResponse({
		'success': True,
		'has_debts': has_debts,
		'facturas_pendientes': resultados,
		'message': 'No hay deudas pendientes' if not has_debts else 'Facturas pendientes encontradas'
	}, status=200)


# Obtener número de comprobante: caso si letra de comprobante previo
@require_GET
def obtener_numero_comprobante2(request):
	# Obtener parámetros de la solicitud
	id_sucursal = request.GET.get('id_sucursal')
	id_punto_venta = request.GET.get('id_punto_venta')
	comprobante = request.GET.get('comprobante')

	if not all([id_sucursal, id_punto_venta, comprobante]):
		return JsonResponse({'error': 'Faltan parámetros requeridos'}, status=400)

	try:
		# Obtener número referencial (último número + 1)
		ultimo_numero = Numero.objects.filter(
			id_sucursal=id_sucursal,
			id_punto_venta=id_punto_venta,
			comprobante=comprobante
		).order_by('-numero').first()

		# Si no hay registros, devolver un mensaje específico (igual que en la primera vista)
		if not ultimo_numero:
			return JsonResponse({
				'success': False,
				'message': 'No se puede obtener la numeración de este comprobante, consulte al Administrador del Sistema!',
			})

		numero_referencial = ultimo_numero.numero + 1
		letra = ultimo_numero.letra
		numero_definitivo = numero_referencial  # Por defecto son iguales

		return JsonResponse({
			'numero_referencial': numero_referencial,
			'numero_definitivo': numero_definitivo,
			'letra': letra,
			'success': True
		})

	except Exception as e:
		return JsonResponse({
			'error': str(e),
			'success': False
		}, status=500)


# Obtener el último número de comprobante
@require_GET
def obtener_numero_comprobante3(request):
	# Obtener parámetros de la solicitud
	id_sucursal = request.GET.get('id_sucursal')
	id_punto_venta = request.GET.get('id_punto_venta')
	comprobante = request.GET.get('comprobante')
	# id_discrimina_iva = request.GET.get('id_discrimina_iva') == 'on' 
	id_discrimina_iva = request.GET.get('id_discrimina_iva')

	if not all([id_sucursal, id_punto_venta, comprobante, id_discrimina_iva]):
		return JsonResponse({'error': 'Faltan parámetros requeridos'}, status=400)

	try:
		if id_discrimina_iva == "false":
			id_discrimina_iva = False
		else:
			id_discrimina_iva = True

		# Buscar en ComprobanteVenta los códigos AFIP
		comprobante_data = ComprobanteVenta.objects.filter(
			codigo_comprobante_venta=comprobante
		).first()

		if not comprobante_data:
			return JsonResponse({
				'success': False,
				'message': 'No se encontró la configuración AFIP para este comprobante, consulte al Administrador del Sistema!',
			})

		codigo_afip_a = comprobante_data.codigo_afip_a
		codigo_afip_b = comprobante_data.codigo_afip_b

		print("codigo_afip_a", codigo_afip_a)
		print("codigo_afip_b", codigo_afip_b)

		# Validar que los códigos AFIP A y B no estén vacíos
		if not codigo_afip_a or not codigo_afip_b:
			return JsonResponse({
				'success': False,
				'message': 'La configuración AFIP para este comprobante está incompleta, consulte al Administrador del Sistema!',
			})

		letra = ""
		comprobante = ""
		if codigo_afip_a != codigo_afip_b:
			# Caso codigo_afip_a, codigo_afip_b
			if id_discrimina_iva:
				comprobante = codigo_afip_a
				print("codigo_afip_a ***", codigo_afip_a)
			else:
				# comprobante = codigo_afip_a
				comprobante = codigo_afip_b
				print("codigo_afip_b ***", codigo_afip_b)
		else:
			# Caso NO codigo_afip_a, codigo_afip_b
			comprobante = codigo_afip_a
		
		print("========")
		print("Comprobante", comprobante)
		print("========")

		# print("codigo_afip_definitivo", codigo_afip_a)
		# print("id_sucusal", id_sucursal)
		# print("id_punto_venta", id_punto_venta)
		
		# Obtener número referencial (último número + 1)
		ultimo_numero = Numero.objects.filter(
			id_sucursal=id_sucursal,
			id_punto_venta=id_punto_venta,
			comprobante=comprobante
		).order_by('-numero').first()

		# Si no hay registros, devolver un mensaje específico (igual que en la primera vista)
		if not ultimo_numero:
			return JsonResponse({
				'success': False,
				'message': 'No se puede obtener la numeración de este comprobante, consulte al Administrador del Sistema!',
			})

		numero_referencial = ultimo_numero.numero + 1
		letra = ultimo_numero.letra
		numero_definitivo = numero_referencial

		return JsonResponse({
			'numero_referencial': numero_referencial,
			'numero_definitivo': numero_definitivo,
			'letra': letra,
			'success': True
		})

	except Exception as e:
		return JsonResponse({
			'error': str(e),
			'success': False
		}, status=500)


@require_GET
def buscar_banco(request):
	codigo_banco = request.GET.get('codigo_banco', '').strip()

	print("Código banco recibido:", codigo_banco)

	if not codigo_banco:
		return JsonResponse({'error': 'No se proporcionó un código de banco'}, status=400)

	try:
		codigo_banco = int(codigo_banco)
		banco = Banco.objects.filter(codigo_banco=codigo_banco, estatus_banco=True).first()
		
		if banco:
			print("Banco encontrado:", banco.nombre_banco, banco.id_banco)
			return JsonResponse({
				'id_banco': banco.id_banco,
				'nombre_banco': banco.nombre_banco,
				'success': True
			})
		else:
			print("Banco no encontrado para código:", codigo_banco)
			return JsonResponse({
				'error': 'Banco no encontrado',
				'success': False
			}, status=404)

	except ValueError:
		print("Error: Código de banco no numérico:", codigo_banco)
		return JsonResponse({
			'error': 'El código de banco debe ser numérico',
			'success': False
		}, status=400)
	except Exception as e:
		print("Error en buscar_banco:", str(e))
		print("Traceback:", traceback.format_exc())
		return JsonResponse({
			'error': f'Error en el servidor: {str(e)}',
			'traceback': traceback.format_exc(),
			'success': False
		}, status=500)


@require_GET
def buscar_codigo_banco(request):
	id_banco = request.GET.get('id_banco')
	try:
		if not id_banco:
			return JsonResponse({'success': False, 'error': 'Parámetro id_banco requerido'})
		banco = Banco.objects.get(id_banco=id_banco, estatus_banco=True)
		return JsonResponse({
			'success': True,
			'codigo_banco': banco.codigo_banco
		})
	except Banco.DoesNotExist:
		return JsonResponse({'success': False, 'error': 'Banco no encontrado'})


@require_GET
def obtener_libro_iva(request):
	id_comprobante = request.GET.get('id')
	try:
		comprobante = ComprobanteVenta.objects.get(pk=id_comprobante)
		print('libro_iva', comprobante.libro_iva)
		return JsonResponse({'libro_iva': comprobante.libro_iva})
	except ComprobanteVenta.DoesNotExist:
		return JsonResponse({'error': 'No encontrado'}, status=404)


@require_GET
def buscar_factura(request):
	try:
		id_cliente = request.GET.get('id_cliente')
		compro = request.GET.get('id_comprobante_asociado')
		numero = request.GET.get('numero_comprobante')

		# Validación más explícita
		if not id_cliente or not numero:
			return JsonResponse(
				{'error': 'Se requieren id_cliente y numero_comprobante'},
				status=400
			)

		try:
			id_cliente = int(id_cliente)  # Conversión temprana
		except ValueError:
			return JsonResponse(
				{'error': 'id_cliente debe ser un número entero'},
				status=400
			)

		facturas = Factura.objects.filter(
			id_cliente_id=id_cliente,
			numero_comprobante__iexact=numero.strip(),
			compro = compro.strip(),
			id_comprobante_venta__libro_iva=True
		).select_related('id_comprobante_venta')

		resultados = [{
			'id': f.id_factura,
			'numero_comprobante': f.numero_comprobante,
			'fecha': f.fecha_comprobante.strftime('%Y-%m-%d') if f.fecha_comprobante else None,
			'total': str(f.total),
			'comprobante_nombre': f.id_comprobante_venta.nombre_comprobante_venta if f.id_comprobante_venta else None,
			'libro_iva': f.id_comprobante_venta.libro_iva if f.id_comprobante_venta else False
		} for f in facturas]

		return JsonResponse({
			'facturas': resultados,
			'count': len(resultados)
		})

	except Exception as e:
		logger.error(f"Error en buscar_factura: {str(e)}")  # Loggear en producción
		return JsonResponse(
			{'error': 'Error interno del servidor'},
			status=500
		)
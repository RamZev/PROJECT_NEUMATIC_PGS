# neumatic\apps\datatools\views\consulta_facturas_views.py
import os
import json
import glob
from datetime import date
from io import BytesIO
from decimal import Decimal

from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.db.models import Q, OuterRef, Exists
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors

from apps.maestros.models.cliente_models import Cliente
from apps.ventas.models.factura_models import Factura, DetalleFactura
from apps.maestros.models.producto_models import Producto, ProductoStock
from apps.maestros.models.base_models import ProductoDeposito
from apps.ventas.models.venta_models import StockCliente


class ConsultaFacturasClienteView(TemplateView):
	template_name = 'datatools/consulta_factura_form.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		buscar_por = self.request.GET.get('buscar_por', '').strip()
		facturas = []
		detalles_factura = {}
		cliente = None
		error = None

		if buscar_por:
			try:
				# Buscar cliente por ID, CUIT o nombre
				if buscar_por.isdigit():
					print("Entró a buscar ConsultaFacturasClienteView")
					
					# Si es numérico, buscar por ID o CUIT
					if len(buscar_por) == 11:  # Asumiendo que CUIT tiene 11 dígitos
						cliente = Cliente.objects.filter(
							Q(cuit=int(buscar_por))
						).first()
					else:
						cliente = Cliente.objects.filter(
							Q(id_cliente=int(buscar_por))
						).first()
						
					if not cliente and len(buscar_por) < 11:
						# Si no se encontró por ID, intentar por CUIT aunque no tenga 11 dígitos
						cliente = Cliente.objects.filter(
							Q(cuit=int(buscar_por))
						).first()
				else:
					# Búsqueda por nombre (no numérico)
					cliente = Cliente.objects.filter(
						Q(nombre_cliente__icontains=buscar_por)
					).first()
				
				if cliente:
					facturas = Factura.objects.filter(
						id_cliente=cliente,
						id_comprobante_venta__libro_iva=True
					).select_related(
						'id_comprobante_venta',
						'id_cliente'
					).order_by('-fecha_comprobante')

					# Paginación
					paginator = Paginator(facturas, 10)  # 10 facturas por página
					page_number = self.request.GET.get('page')
					page_obj = paginator.get_page(page_number)
					
					# Pre-cargar detalles para las facturas encontradas
					if facturas:
						facturas_ids = [f.id_factura for f in facturas]
						detalles = DetalleFactura.objects.filter(
							id_factura__in=facturas_ids
						).select_related('id_producto')
						
						# Organizar detalles por factura
						detalles_factura = {
							factura.id_factura: [
								d for d in detalles 
								if d.id_factura_id == factura.id_factura
							] 
							for factura in facturas
						}
				else:
					error = "No se encontró ningún cliente con ese criterio de búsqueda"
			
			except ValueError as ve:
				error = f"Error en el formato de búsqueda: {str(ve)}"
			except Exception as e:
				error = f"Error inesperado al realizar la búsqueda: {str(e)}"
		
		context.update({
			'cliente': cliente,
			'facturas': page_obj,  # Ahora contiene solo las facturas de la página actual
			'page_obj': page_obj,
			'detalles_factura': detalles_factura,
			'buscar_por': buscar_por,
			'error': error,
			'fecha': timezone.now()  
		})

		# context['fecha'] = timezone.now()
		# print(context)

		return context
	
	def get(self, request, *args, **kwargs):
		# Manejo personalizado para mostrar errores
		try:
			return super().get(request, *args, **kwargs)
		except Exception as e:
			return render(request, self.template_name, {
				'error': f"Error al procesar la solicitud: {str(e)}"
			})


class ConsultaProductosView(TemplateView):
	template_name = 'datatools/consulta_productos_form.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		usuario = self.request.user
		
		#-- Parámetros de búsqueda.
		medida = self.request.GET.get('medida', '').strip()
		nombre = self.request.GET.get('nombre', '').strip()
		cai = self.request.GET.get('cai', '').strip()
		filtro_marca = self.request.GET.get('filtro_marca', 'primeras')
		
		error = None
		page_obj = None
		
		if any([medida, nombre, cai]):
			try:
				# ========== FILTRADO PRINCIPAL ==========
				#-- Construir filtros base.
				filters = Q()
				
				if medida:
					filters &= Q(medida__icontains=medida)
				if nombre:
					filters &= Q(nombre_producto__icontains=nombre)
				if cai:
					filters &= Q(id_cai__cai__icontains=cai)
				
				# ========== FILTRO PARA VENDEDORES ==========
				if usuario.id_vendedor:
					#-- Buscar IDs de los estados "Disponible" y "Ofertas".
					from apps.maestros.models.base_models import ProductoEstado
					
					#-- Buscar estado "Disponible".
					try:
						estado_disponibles = ProductoEstado.objects.get(
							nombre_producto_estado__iexact="disponibles"
						)
						estado_disponibles_id = estado_disponibles.id_producto_estado
					except ProductoEstado.DoesNotExist:
						estado_disponibles_id = None
					
					#-- Buscar estado "Ofertas".
					try:
						estado_ofertas = ProductoEstado.objects.get(
							nombre_producto_estado__iexact="ofertas"
						)
						estado_ofertas_id = estado_ofertas.id_producto_estado
					except ProductoEstado.DoesNotExist:
						estado_ofertas_id = None
					
					#-- Crear filtro para estados permitidos.
					estado_filters = Q(id_producto_estado__isnull=True)  #-- NULL siempre permitido
					
					if estado_disponibles_id:
						estado_filters |= Q(id_producto_estado=estado_disponibles_id)
					
					if estado_ofertas_id:
						estado_filters |= Q(id_producto_estado=estado_ofertas_id)
					filters &= estado_filters
				
				# ============== FILTROS DE MARCAS ===============
				if filtro_marca == "primeras":
					filters &= Q(id_marca__principal=True)
				elif filtro_marca == "otras":
					filters &= Q(id_marca__principal=False)
				
				# ========== FILTRO DE STOCK OPTIMIZADO ==========
				#-- Usar EXISTS subquery que es más eficiente que annotate.
				if filtro_marca == "stock":
					#-- Subquery: productos que tienen al menos un registro con stock > 0.
					stock_subquery = ProductoStock.objects.filter(
						id_producto=OuterRef('pk'),
						stock__gt=0
					)
					
					#-- Aplicar filtro con EXISTS.
					productos = Producto.objects.filter(
						filters & Exists(stock_subquery)
					)
				else:
					#-- Sin filtro de stock.
					productos = Producto.objects.filter(filters)
				
				#-- Select related y ordenar.
				productos = productos.select_related(
					'id_marca', 'id_cai', 'id_familia', 'id_alicuota_iva', 'id_producto_estado'
				).order_by('nombre_producto')
				
				#-- Paginación.
				paginator = Paginator(productos, 10)
				page_number = self.request.GET.get('page')
				page_obj = paginator.get_page(page_number)
				
				# ========== CÁLCULO DE STOCK DETALLADO (solo página actual) ==========
				if page_obj and page_obj.object_list:
					#-- IDs de productos en esta página.
					productos_pagina_ids = [p.id_producto for p in page_obj]
					
					# ============= OBTENER CANTIDADES EN TRÁNSITO =============
					#-- Obtener sumatoria de cantidades en tránsito por producto.
					transito_data = DetalleFactura.objects.filter(
						id_producto__in=productos_pagina_ids,
						id_factura__id_comprobante_venta__codigo_comprobante_venta='RM',
						id_factura__estado__in=['', None]  # vacío o NULL
					).values('id_producto').annotate(
						total_transito=Sum('cantidad')
					)
					
					#-- Convertir a diccionario para acceso rápido: {producto_id: cantidad_en_transito}.
					transito_dict = {
						item['id_producto']: item['total_transito'] 
						for item in transito_data
					}
					
					#-- Obtener depósitos.
					depositos = ProductoDeposito.objects.all()
					
					#-- Obtener stock para estos productos específicos.
					stock_data = ProductoStock.objects.filter(
						id_producto__in=productos_pagina_ids
					).values('id_producto', 'id_deposito', 'stock')
					
					#-- Organizar stock en diccionario.
					stock_dict = {}
					for item in stock_data:
						pid = item['id_producto']
						did = item['id_deposito']
						
						if pid not in stock_dict:
							stock_dict[pid] = {}
						
						stock_dict[pid][did] = item['stock']
					
					#-- Calcular stock total y por depósito para cada producto.
					for producto in page_obj:
						producto.stock_total = 0
						producto.stock_por_deposito_list = []
						
						# Stock de este producto
						producto_stock = stock_dict.get(producto.id_producto, {})
						
						#-- Sumar por depósito.
						for deposito in depositos:
							stock = producto_stock.get(deposito.id_producto_deposito, 0)
							producto.stock_total += stock
							
							producto.stock_por_deposito_list.append({
								'deposito': deposito.nombre_producto_deposito,
								'stock': stock
							})
						
						#-- Cantidad en tránsito.
						producto.cantidad_transito = transito_dict.get(producto.id_producto, 0)
						
						#-- Calcular precio con descuento.
						producto.precio_descuento = producto.precio * (1 - (producto.descuento or 0) / 100) if producto.descuento else producto.precio
			
			except Exception as e:
				error = f"Error al realizar la búsqueda: {str(e)}"
				page_obj = None
		
		context.update({
			'productos': page_obj.object_list if page_obj else [],
			'page_obj': page_obj,
			'medida': medida,
			'nombre': nombre,
			'cai': cai,
			'filtro_marca': filtro_marca,
			'error': error,
			'fecha': timezone.now()
		})
		return context


# === NUEVAS VISTAS ===
def obtener_proximo_correlativo(factura_id):
	"""
	Obtiene el próximo número correlativo para los archivos JSON de una factura
	Formato: sc_{factura_id}_{correlativo}.json donde correlativo es 01, 02, 03...
	"""
	# Obtener el BASE_DIR del proyecto (carpeta neumatic/)
	base_dir = settings.BASE_DIR
	
	# Construir ruta completa a data/json
	json_dir = os.path.join(base_dir, 'data', 'json')
	
	# Asegurar que el directorio existe
	os.makedirs(json_dir, exist_ok=True)
	
	# Patrón de búsqueda: sc_{factura_id}_*
	patron = f"sc_{factura_id}_*.json"
	ruta_patron = os.path.join(json_dir, patron)
	
	# Buscar archivos existentes
	archivos_existentes = glob.glob(ruta_patron)
	
	if not archivos_existentes:
		# Si no hay archivos, empezar con 01
		return "01"
	
	# Extraer números de los archivos existentes y encontrar el máximo
	numeros = []
	for archivo in archivos_existentes:
		nombre_archivo = os.path.basename(archivo)
		# Extraer el número: sc_123_01.json -> 01
		try:
			partes = nombre_archivo.split('_')
			if len(partes) >= 3:
				numero_str = partes[2].split('.')[0]  # Tomar "01" de "01.json"
				numeros.append(int(numero_str))
		except (ValueError, IndexError):
			continue
	
	if not numeros:
		return "01"
	
	# Encontrar el máximo y sumar 1
	max_numero = max(numeros)
	siguiente_numero = max_numero + 1
	
	# Formatear con 2 dígitos: 1 -> "01", 9 -> "09", 10 -> "10"
	return f"{siguiente_numero:02d}"


def stock_cliente_detalle(request, factura_id):
	"""Vista para mostrar el stock del cliente y gestionar retiros"""
	factura = get_object_or_404(Factura, id_factura=factura_id)
	stock_items = StockCliente.objects.filter(id_factura=factura).select_related('id_producto')
	
	# Calcular saldo para cada item en la vista
	for item in stock_items:
		cantidad = float(item.cantidad or 0)
		retirado = float(item.retirado or 0)
		item.saldo = cantidad - retirado
		item.tiene_saldo = item.saldo > 0
	
	context = {
		'factura': factura,
		'stock_items': stock_items,
		'cliente_nombre': factura.id_cliente.nombre_cliente,
	}
	
	return render(request, 'datatools/stock_cliente_detalle.html', context)


@csrf_exempt
@transaction.atomic
def generar_entrega_cliente(request, factura_id):
	"""Vista para procesar los retiros y generar entrega"""
	if request.method == 'POST':
		try:
			factura = get_object_or_404(Factura, id_factura=factura_id)
			cliente = factura.id_cliente
			
			datos_entrega = {
				'cliente_id': cliente.id_cliente,
				'cliente_nombre': cliente.nombre_cliente,
				'cliente_direccion': getattr(cliente, 'direccion', 'No especificada'),
				'factura_id': factura.id_factura,
				'factura_numero': factura.numero_comprobante,
				'fecha_entrega': date.today().strftime('%d/%m/%Y'),
				'fecha_entrega_iso': date.today().isoformat(),
				'productos': [],
				'total_items': 0
			}
			
			# Procesar retiros
			items_procesados = []
			for key, value in request.POST.items():
				if key.startswith('retirar_'):
					stock_id = key.replace('retirar_', '')
					cantidad_retirar = float(value) if value else 0
					
					if cantidad_retirar > 0:
						stock_item = StockCliente.objects.select_for_update().get(
							id_stock_cliente=stock_id,
							id_factura=factura
						)
						
						# Calcular saldo disponible
						# saldo = (stock_item.cantidad or 0) - (stock_item.retirado or 0)
						cantidad = stock_item.cantidad or Decimal('0')
						retirado = stock_item.retirado or Decimal('0')
						saldo = cantidad - retirado
						
						if cantidad_retirar <= saldo:
							# Actualizar retirado y fecha_retiro
							nuevo_retirado = (stock_item.retirado or 0) + cantidad_retirar
							stock_item.retirado = nuevo_retirado
							stock_item.fecha_retiro = date.today()
							stock_item.save()
							
							# Agregar a datos de entrega
							producto_data = {
								'stock_id': stock_item.id_stock_cliente,
								'producto_id': stock_item.id_producto.id_producto,
								'producto_nombre': stock_item.id_producto.nombre_producto,
								'medida': getattr(stock_item.id_producto, 'medida', 'N/A'),
								'cantidad_original': float(stock_item.cantidad or 0),
								'retirado_anterior': float(stock_item.retirado or 0) - cantidad_retirar,
								'cantidad_retirada': cantidad_retirar,
								'retirado_total': nuevo_retirado,
								'saldo_restante': saldo - cantidad_retirar
							}
							datos_entrega['productos'].append(producto_data)
							datos_entrega['total_items'] += cantidad_retirar
							items_procesados.append(stock_id)
						else:
							return JsonResponse({
								'success': False,
								'error': f'No se puede retirar {cantidad_retirar}. Saldo disponible: {saldo}'
							})
			
			if not datos_entrega['productos']:
				return JsonResponse({
					'success': False,
					'error': 'No hay cantidades válidas para retirar'
				})
			
			# GENERAR ARCHIVO JSON CON NOMBRE CORRELATIVO
			correlativo = obtener_proximo_correlativo(factura_id)
			json_filename = f"sc_{factura_id}_{correlativo}.json"
			
			# Ruta completa del archivo JSON
			json_dir = os.path.join(settings.BASE_DIR, 'data', 'json')
			os.makedirs(json_dir, exist_ok=True)  # Asegurar que existe
			json_path = os.path.join(json_dir, json_filename)
			
			# Guardar JSON
			with open(json_path, 'w', encoding='utf-8') as f:
				json.dump(datos_entrega, f, indent=2, ensure_ascii=False)
			
			print(f"✅ JSON guardado: {json_path}")  # Para debug
			
			# Guardar datos en session para el PDF
			request.session['ultima_entrega'] = datos_entrega
			request.session['json_filename'] = json_filename  # Guardar nombre para referencia
			
			return JsonResponse({
				'success': True,
				'message': f'Entrega generada: {len(datos_entrega["productos"])} productos, {datos_entrega["total_items"]} unidades',
				'pdf_url': f'/stock/cliente/{factura_id}/descargar-pdf/',
				'json_filename': json_filename,
				'total_unidades': datos_entrega['total_items']
			})
			
		except StockCliente.DoesNotExist:
			return JsonResponse({
				'success': False,
				'error': 'Uno de los productos no existe en el stock'
			})
		except Exception as e:
			return JsonResponse({
				'success': False,
				'error': f'Error del sistema: {str(e)}'
			})
	
	return JsonResponse({'success': False, 'error': 'Método no permitido'})


def generar_pdf_entrega(datos_entrega):
	response = HttpResponse(content_type='application/pdf')
	
	cliente_nombre_limpio = datos_entrega.get('cliente_nombre', 'Cliente').replace(' ', '_')
	filename = f"recibo_entrega_{cliente_nombre_limpio}.pdf"
	response['Content-Disposition'] = f'inline; filename="{filename}"'
	
	buffer = BytesIO()
	doc = SimpleDocTemplate(buffer, pagesize=A4)
	elements = []
	
	styles = getSampleStyleSheet()
	
	title_style = ParagraphStyle(
		'CustomTitle',
		parent=styles['Heading1'],
		fontSize=16,
		textColor=colors.darkblue,
		spaceAfter=25,
		alignment=1,
		fontName='Helvetica-Bold'
	)
	
	title = Paragraph("RECIBO DE ENTREGA DE PRODUCTOS", title_style)
	elements.append(title)
	
	# Información del cliente
	info_data = [
		[Paragraph(f"<b>Cliente:</b> {datos_entrega.get('cliente_nombre', 'No especificado')}", styles['Normal']),
		Paragraph(f"<b>Factura N°:</b> {datos_entrega.get('factura_numero', 'N/A')}", styles['Normal'])],
		[Paragraph(f"<b>Dirección:</b> {datos_entrega.get('cliente_direccion', 'No especificada')}", styles['Normal']),
		Paragraph(f"<b>Fecha de Entrega:</b> {datos_entrega.get('fecha_entrega', 'N/A')}", styles['Normal'])]
	]
	
	info_table = Table(info_data, colWidths=[doc.width/2]*2)
	info_table.setStyle(TableStyle([
		('ALIGN', (0, 0), (-1, -1), 'LEFT'),
		('VALIGN', (0, 0), (-1, -1), 'TOP'),
		('BOTTOMPADDING', (0, 0), (-1, -1), 8),
		('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
		('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.whitesmoke]),
	]))
	elements.append(info_table)
	elements.append(Spacer(1, 20))
	
	# Tabla de productos
	if datos_entrega.get('productos'):
		data = [[
			Paragraph('<b>Producto</b>', styles['Normal']),
			Paragraph('<b>Cant. Original</b>', styles['Normal']),
			Paragraph('<b>Retirado Anterior</b>', styles['Normal']),
			Paragraph('<b>Retiro Actual</b>', styles['Normal']),
			Paragraph('<b>Total Retirado</b>', styles['Normal']),
			Paragraph('<b>Saldo Restante</b>', styles['Normal'])
		]]
		
		for producto in datos_entrega['productos']:
			data.append([
				producto['producto_nombre'],
				f"{producto['cantidad_original']:.2f}",
				f"{producto['retirado_anterior']:.2f}",
				Paragraph(f"<b>{producto['cantidad_retirada']:.2f}</b>", styles['Normal']),
				f"{producto['retirado_total']:.2f}",
				f"{producto['saldo_restante']:.2f}"
			])
		
		table = Table(data, colWidths=[doc.width*0.3, doc.width*0.14, doc.width*0.14, 
									doc.width*0.14, doc.width*0.14, doc.width*0.14])
		table.setStyle(TableStyle([
			('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
			('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
			('ALIGN', (0, 0), (-1, -1), 'CENTER'),
			('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
			('FONTSIZE', (0, 0), (-1, 0), 9),
			('BOTTOMPADDING', (0, 0), (-1, 0), 10),
			('BACKGROUND', (0, 1), (-1, -1), colors.beige),
			('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
			('FONTSIZE', (0, 1), (-1, -1), 8),
			('GRID', (0, 0), (-1, -1), 0.5, colors.black),
			('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
		]))
		elements.append(table)
	
	# Resumen total
	elements.append(Spacer(1, 25))
	total_style = ParagraphStyle(
		'TotalStyle',
		parent=styles['Heading2'],
		fontSize=12,
		textColor=colors.darkgreen,
		alignment=1
	)
	total_text = Paragraph(
		f"<b>TOTAL UNIDADES ENTREGADAS: {datos_entrega.get('total_items', 0):.2f}</b>", 
		total_style
	)
	elements.append(total_text)
	
	# Firmas
	elements.append(Spacer(1, 40))
	firmas_data = [
		['', ''],
		['_________________________', '_________________________'],
		['Firma del Cliente', 'Firma del Entregador'],
		['', ''],
		['Aclaración: ___________________', 'Nombre: ___________________']
	]
	
	firmas_table = Table(firmas_data, colWidths=[doc.width/2]*2)
	firmas_table.setStyle(TableStyle([
		('ALIGN', (0, 0), (-1, -1), 'CENTER'),
		('FONTSIZE', (0, 0), (-1, -1), 9),
		('VALIGN', (0, 0), (-1, -1), 'TOP'),
	]))
	elements.append(firmas_table)
	
	doc.build(elements)
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	
	return response


def descargar_pdf_entrega(request, factura_id):
	"""Vista para descargar el PDF de entrega"""
	datos_entrega = request.session.get('ultima_entrega', {})
	
	if not datos_entrega:
		# Crear datos de ejemplo si no hay en session
		factura = get_object_or_404(Factura, id_factura=factura_id)
		datos_entrega = {
			'cliente_nombre': factura.id_cliente.nombre_cliente,
			'fecha_entrega': date.today().strftime('%d/%m/%Y'),
			'productos': [],
			'total_items': 0
		}
	
	return generar_pdf_entrega(datos_entrega)


class CrearStockClienteView(View):
	def post(self, request, id_factura):
		factura = get_object_or_404(Factura, id_factura=id_factura)

		print("Entró a crear stock cliente")
		
		# Verificar si ya existe stock para esta factura
		if StockCliente.objects.filter(id_factura=factura).exists():
			print("Ya existe stock para esta factura***")
			messages.warning(request, "No se pudo realizar la operación, el Documento ya tiene stock generado")
		else:
			detalles = DetalleFactura.objects.filter(id_factura=factura, cantidad__gt=0)
			if not detalles.exists():
				print("No hay detalles con cantidad válida")
				messages.error(request, "La factura no tiene productos con cantidad válida para generar stock.")
			else:
				with transaction.atomic():
					for detalle in detalles:
						StockCliente.objects.create(
							id_factura=factura,
							id_producto=detalle.id_producto,
							cantidad=detalle.cantidad,
							retirado=0,
							numero=0,  # o define lógica de numeración si aplica
							comentario="Generado desde factura"
						)
					# Opcional: marcar la bandera en la factura
					factura.stock_clie = True
					factura.save(update_fields=['stock_clie'])
					
				messages.success(request, "Stock del cliente generado exitosamente.")
		
		# Redirigir de vuelta a la búsqueda, manteniendo el parámetro
		buscar_por = request.GET.get('buscar_por', '')
		page = request.GET.get('page', '')
		url = f"{reverse('consulta_facturas_cliente')}?buscar_por={buscar_por}"
		if page:
			url += f"&page={page}"
		return redirect(url)


class AdministrarStockClienteView(TemplateView):
	template_name = 'datatools/stock_cliente_detalle.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		id_factura = self.kwargs['id_factura']
		factura = get_object_or_404(Factura, id_factura=id_factura)
		
		# Obtener los registros de StockCliente con el producto relacionado
		stock_items = StockCliente.objects.filter(id_factura=factura).select_related('id_producto')

		# ✅ NUEVO: calcular el saldo (cantidad - retirado) en Python
		stock_items_con_saldo = []
		for item in stock_items:
			cantidad = item.cantidad or 0
			retirado = item.retirado or 0
			item.saldo = cantidad - retirado  # Añadimos un atributo dinámico
			stock_items_con_saldo.append(item)
		
		if not stock_items.exists():
			messages.info(self.request, "No se ha asociado stock al cliente en esta factura.")
		
		context.update({
			'factura': factura,
			'stock_items': stock_items,
			'cliente_nombre': factura.nombre_factura or factura.id_cliente.nombre_cliente if factura.id_cliente else "Desconocido"
		})
		return context


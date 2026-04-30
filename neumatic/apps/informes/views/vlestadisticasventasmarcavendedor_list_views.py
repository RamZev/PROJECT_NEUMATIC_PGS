# neumatic\apps\informes\views\vlestadisticasventasmarcavendedor_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static
from decimal import Decimal

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLEstadisticasVentasMarcaVendedor
from ..forms.buscador_vlestadisticasventasmarcavendedor_forms import BuscadorEstadisticasVentasMarcaVendedorForm
from utils.utils import deserializar_datos, formato_argentino, normalizar, format_date, raw_to_dict
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Estadísticas de Ventas por Marca y Familia por Vendedor"
	
	#-- Modelo.
	model = VLEstadisticasVentasMarcaVendedor
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorEstadisticasVentasMarcaVendedorForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	model_string = model.__name__.lower()
	
	#-- Vistas del CRUD del modelo.
	list_view_name = f"{model_string}_list"  # <== vlventacompro_list
	
	#-- Plantilla base.
	template_list = f'{app_label}/maestro_informe.html'
	
	#-- Vista del home del proyecto.
	home_view_name = "home"
	
	#-- Archivo JavaScript específico.
	js_file = None
	
	# #-- URL de la vista que genera el .zip con los informes.
	# url_zip = f"{model_string}_informe_generado"
	
	#-- URL de la vista que genera la salida a pantalla.
	url_pantalla = f"{model_string}_vista_pantalla"
	
	#-- URL de la vista que genera el .pdf.
	url_pdf = f"{model_string}_vista_pdf"
	
	#-- URL de la vista que genera el Excel.
	url_excel = f"{model_string}_vista_excel"
	
	#-- URL de la vista que genera el CSV.
	url_csv = f"{model_string}_vista_csv"
	
	#-- Plantilla Vista Preliminar Pantalla.
	reporte_pantalla = f"informes/reportes/{model_string}_list.html"
	
	#-- Establecer las columnas del reporte y sus atributos.
	table_info = {
		"id_marca_id": {
			"label": "ID Marca",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_producto_marca": {
			"label": "Marca",
			"col_width_pdf": 75,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_familia_id": {
			"label": "ID Familia",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_producto_familia": {
			"label": "Familia",
			"col_width_pdf": 75,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_modelo_id": {
			"label": "ID Modelo",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_modelo": {
			"label": "Modelo",
			"col_width_pdf": 75,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"comprobante": {
			"label": "Comprobante",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"fecha_comprobante": {
			"label": "Fecha",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_cliente_id": {
			"label": "Cliente",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_producto_id": {
			"label": "Código",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"nombre_producto": {
			"label": "Descripción",
			"col_width_pdf": 200,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"medida": {
			"label": "Medida",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"cantidad": {
			"label": "Cantidad",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"precio": {
			"label": "Precio",
			"col_width_pdf": 75,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"descuento": {
			"label": "Desc.",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"total": {
			"label": "Total",
			"col_width_pdf": 75,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"comision": {
			"label": "Comisión",
			"col_width_pdf": 75,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_sucursal_id": {
			"label": "Sucursal",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
}


class VLEstadisticasVentasMarcaVendedorInformeView(InformeFormView):
	config = ConfigViews  #-- Ahora la configuración estará disponible en self.config.
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_list
	
	extra_context = {
		"master_title": f'Informes - {ConfigViews.model._meta.verbose_name_plural}',
		"home_view_name": ConfigViews.home_view_name,
		"buscador_template": f"{ConfigViews.app_label}/buscador_{ConfigViews.model_string}.html",
		"js_file": ConfigViews.js_file,
		"url_pantalla": ConfigViews.url_pantalla,
		"url_pdf": ConfigViews.url_pdf,
	}
	
	def obtener_queryset(self, cleaned_data):
		sucursal = cleaned_data.get('sucursal', None)
		marca = cleaned_data.get('marca', None)
		vendedor = cleaned_data.get('vendedor', None)
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		comision = cleaned_data.get("comision", None)
		
		id_sucursal = sucursal.id_sucursal if sucursal else None
		id_marca = marca.id_producto_marca if marca else None
		id_vendedor = vendedor.id_vendedor if vendedor else None
		
		queryset = VLEstadisticasVentasMarcaVendedor.objects.obtener_datos(
			id_marca,
			id_vendedor,
			fecha_desde,
			fecha_hasta,
			id_sucursal=id_sucursal
		)
		
		#-- Calcular comisión solo si hay registros y se ha indiciado el parámetro.
		for obj in queryset:
			obj.comision = round(Decimal((obj.total * comision / 100)), 2) if comision else 0
		
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		sucursal = cleaned_data.get('sucursal', None)
		marca = cleaned_data.get('marca', None)
		vendedor = cleaned_data.get('vendedor', None)
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		comision = cleaned_data.get("comision", None)
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {
			"Sucursal": f"[{sucursal.id_sucursal}] {sucursal.nombre_sucursal}" if sucursal else "Todas",
			"Marca": f"[{marca.id_producto_marca}] {marca.nombre_producto_marca}" if marca else "Todas",
			"Vendedor": f"[{vendedor.id_vendedor}] {vendedor.nombre_vendedor}" if vendedor else "Todos",
		}
		param_right = {
			"Desde": fecha_desde.strftime("%d/%m/%Y"),
			"Hasta": fecha_hasta.strftime("%d/%m/%Y"),
			"Comisión": f"{formato_argentino(comision)}%" if comision else "0%"
		}
		
		# **************************************************
		#-- Convertir QUERYSET a LISTA DE DICCIONARIOS al inicio (optimización clave).
		queryset_list = [raw_to_dict(obj) for obj in queryset]
		
		grouped_data = {}
		tg_cantidad = 0
		tg_total = Decimal('0')
		tg_comision = Decimal('0')
		
		for obj in queryset_list:
			#-- Agrupar los objetos por Familia.
			id_familia = obj['id_familia_id']
			if id_familia not in grouped_data:
				grouped_data[id_familia] = {
					'familia': obj['nombre_producto_familia'],
					'modelos': {},
					'stf_cantidad': 0,
					'stf_total': Decimal('0'),
					'stf_comision': Decimal('0')
				}
			
			#-- Agrupar los objetos por Modelos de la Familia.
			id_modelo = obj['id_modelo_id']
			if id_modelo not in grouped_data[id_familia]['modelos']:
				grouped_data[id_familia]['modelos'][id_modelo] = {
					'modelo': obj['nombre_modelo'],
					'detalle': [],
					'stm_cantidad': 0,
					'stm_total': Decimal('0'),
					'stm_comision': Decimal('0')
				}
			
			#-- Añadir el detalle al grupo.
			grouped_data[id_familia]["modelos"][id_modelo]["detalle"].append(obj)
			
			#-- Acumular totales por Familia.
			cantidad = obj['cantidad']
			total = Decimal(str(obj['total']))
			comision = Decimal(str(obj['comision']))
			
			grouped_data[id_familia]['stf_cantidad'] += cantidad
			grouped_data[id_familia]['stf_total'] += total
			grouped_data[id_familia]['stf_comision'] += comision
			
			#-- Acumular totales por Modelo.
			grouped_data[id_familia]['modelos'][id_modelo]['stm_cantidad'] += cantidad
			grouped_data[id_familia]['modelos'][id_modelo]['stm_total'] += total
			grouped_data[id_familia]['modelos'][id_modelo]['stm_comision'] += comision
			
			#-- Acumular totales generales.
			tg_cantidad += cantidad
			tg_total += total
			tg_comision += comision
		
		#-- Convertir los datos agrupados a un formato serializable:
		for familia_data in grouped_data.values():
			#-- Convertir totales por Familia a float.
			familia_data['stf_total'] = float(familia_data['stf_total'])
			familia_data['stf_comision'] = float(familia_data['stf_comision'])
			
			for modelo_data in familia_data['modelos'].values():
				# #-- Se convierte cada detalle a diccionario usando raw_to_dict.
				# modelo_data['detalle'] = [raw_to_dict(detalle) for detalle in modelo_data['detalle']]
				#-- Convertir totales por Modelo a float.
				modelo_data['stm_total'] = float(modelo_data['stm_total'])
				modelo_data['stm_comision'] = float(modelo_data['stm_comision'])
		
		# **************************************************
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": grouped_data,
			"tg_cantidad": tg_cantidad,
			"tg_total": float(tg_total),
			"tg_comision": float(tg_comision),
			"parametros_i": param_left,
			"parametros_d": param_right,
			'fecha_hora_reporte': fecha_hora_reporte,
			'titulo': ConfigViews.report_title,
			'css_url': static('css/reportes.css'),
		}
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		form = kwargs.get("form") or self.get_form()
		
		context["form"] = form
		if form.errors:
			context["data_has_errors"] = True
		return context


def vlestadisticasventasmarcavendedor_vista_pantalla(request):
	#-- Obtener el token de la querystring.
	token = request.GET.get("token")
	
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Obtener el contexto(datos) previamente guardados en la sesión.
	contexto_reporte = deserializar_datos(request.session.pop(token, None))
	
	if not contexto_reporte:
		return HttpResponse("Contexto no encontrado o expirado", status=400)
	
	#-- Generar el listado a pantalla.
	return render(request, ConfigViews.reporte_pantalla, contexto_reporte)


def vlestadisticasventasmarcavendedor_vista_pdf(request):
	#-- Obtener el token de la querystring.
	token = request.GET.get("token")
	
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Obtener el contexto(datos) previamente guardados en la sesión.
	# contexto_reporte = deserializar_datos(request.session.pop(token, None))
	contexto_reporte = deserializar_datos(request.session.get(token, None))
	
	if not contexto_reporte:
		return HttpResponse("Contexto no encontrado o expirado", status=400)
	
	#-- Generar el PDF usando ReportLab
	pdf_file = generar_pdf(contexto_reporte)
	
	#-- Preparar la respuesta HTTP.
	response = HttpResponse(pdf_file, content_type="application/pdf")
	response["Content-Disposition"] = f'inline; filename="{normalizar(ConfigViews.report_title)}.pdf"'
	
	return response


class CustomPDFGenerator(PDFGenerator):
	#-- Método que se puede sobreescribir/extender según requerimientos.
	def _get_header_bottom_left(self, context):
		"""Personalización del Header-bottom-left"""
		
		params = context.get("parametros_i", {})
		return "<br/>".join([f"<b>{k}:</b> {v}" for k, v in params.items()])
	
	#-- Método que se puede sobreescribir/extender según requerimientos.
	def _get_header_bottom_right(self, context):
		"""Añadir información adicional específica para este reporte"""
		
		params = context.get("parametros_d", {})
		return "<br/>".join([f"<b>{k}:</b> {v}" for k, v in params.items()])


def generar_pdf(contexto_reporte):
	#-- Crear instancia del generador personalizado.
	generator = CustomPDFGenerator(contexto_reporte, pagesize=landscape(A4), body_font_size=7)
	
	#-- Construir datos de la tabla:
	
	#-- Títulos de las columnas de la tabla (headers).
	headers_titles = [value['label'] for value in ConfigViews.table_info.values() if value['pdf']]
	headers_titles.insert(0, "")
	
	#-- Extraer Ancho de las columnas de la tabla.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	col_widths.insert(0, 10)
	blank_cols = [""] * 10
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (3,0), (4,-1), 'RIGHT'),
		('ALIGN', (7,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	for familia_id, familia_data in contexto_reporte.get("objetos", {}).items():
		#-- Datos agrupado por Familia.
		table_data.append([f"Familia: {familia_data['familia']}", ""] + blank_cols)
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		current_row += 1
		
		for modelo_id, modelo_data in familia_data["modelos"].items():
			#-- Datos agrupado por Modelo.
			table_data.append(["", f"Modelo: {modelo_data['modelo']}"] + blank_cols)
			#-- Aplicar estilos a la fila de agrupación (fila actual).
			table_style_config.extend([
				('SPAN', (1,current_row), (-1,current_row)),
				('FONTNAME', (1,current_row), (-1,current_row), 'Helvetica-Bold')
			])
			current_row += 1
			
			#-- Agregar filas del detalle.
			for obj in modelo_data['detalle']:
				
				table_data.append([
					"",
					obj['comprobante'],
					format_date(obj['fecha_comprobante']),
					obj['id_cliente_id'],
					obj['id_producto_id'],
					Paragraph(str(obj['nombre_producto']), generator.styles['CellStyle']),
					obj['medida'],
					formato_argentino(obj['cantidad']),
					formato_argentino(obj['precio']),
					f"{formato_argentino(obj['descuento'])}%" if obj['descuento'] != 0 else "",
					formato_argentino(obj['total']),
					formato_argentino(obj['comision'])
				])
				
				current_row += 1
			
			#-- Fila subtotal por Modelo.
			table_data.append(
				[""]*6 + 
				[
					"Total por Modelo:", 
					formato_argentino(modelo_data["stm_cantidad"]), 
					"", "", 
					formato_argentino(modelo_data["stm_total"]), 
					formato_argentino(modelo_data["stm_comision"])
				]
			)
			#-- Aplicar estilos a la fila de total (fila actual).
			table_style_config.extend([
				('ALIGN', (0,current_row), (-1,current_row), 'RIGHT'),
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
				# ('LINEABOVE', (8,current_row), (-1,current_row), 0.5, colors.black),
			])
			current_row += 1
		
		#-- Fila subtotal por Familia.
		table_data.append(
			[""]*6 + 
			[
				"Total por Familia:", 
				formato_argentino(familia_data["stf_cantidad"]), 
				"", "", 
				formato_argentino(familia_data["stf_total"]), 
				formato_argentino(familia_data["stf_comision"])
			]
		)
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (0,current_row), (-1,current_row), 'RIGHT'),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			# ('LINEABOVE', (8,current_row), (-1,current_row), 0.5, colors.black),
		])
		current_row += 1
		
		#-- Fila divisoria.
		table_data.append(["", ""] + blank_cols)
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
	
	#-- Fila Total General.
	tg_cantidad = contexto_reporte.get("tg_cantidad", 0)
	tg_total = contexto_reporte.get("tg_total", 0)
	tg_comision = contexto_reporte.get("tg_comision", 0)
	
	table_data.append(
		[""]*6 + 
		[
			"Total por Marca:", 
			formato_argentino(tg_cantidad), 
			"", "", 
			formato_argentino(tg_total), 
			formato_argentino(tg_comision)
		]
	)
	
	#-- Aplicar estilos a la fila de total (fila actual).
	table_style_config.extend([
		('ALIGN', (0,-1), (-1,-1), 'RIGHT'),
		('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
		# ('LINEABOVE', (0,-1), (-1,-1), 0.5, colors.black),  #-- Línea superior.
		# ('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.black),  #-- Línea inferior.
	])
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlestadisticasventasmarcavendedor_vista_excel(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	# ---------------------------------------------
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	# ---------------------------------------------
	
	#-- Instanciar la vista y obtener el queryset.
	view_instance = VLEstadisticasVentasMarcaVendedorInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Filtrar los headers de las columnas.
	headers_titles = {field: ConfigViews.table_info[field] for field in ConfigViews.table_info if ConfigViews.table_info[field]['excel']}
	
	helper = ExportHelper(
		queryset=queryset,
		table_info=headers_titles,
		report_title=ConfigViews.report_title
	)
	excel_data = helper.export_to_excel()
	
	response = HttpResponse(
		excel_data,
		content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
	)
	#-- Inline permite visualizarlo en el navegador si el navegador lo soporta.
	response["Content-Disposition"] = f'inline; filename="{ConfigViews.report_title}.xlsx"'
	
	return response


def vlestadisticasventasmarcavendedor_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLEstadisticasVentasMarcaVendedorInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Filtrar los headers de las columnas.
	headers_titles = {field: ConfigViews.table_info[field] for field in ConfigViews.table_info if ConfigViews.table_info[field]['csv']}
	
	#-- Usar el helper para exportar a CSV.
	helper = ExportHelper(
		queryset=queryset,
		table_info=headers_titles,
		report_title=ConfigViews.report_title
	)
	csv_data = helper.export_to_csv()
	
	response = HttpResponse(csv_data, content_type="text/csv; charset=utf-8")
	response["Content-Disposition"] = f'inline; filename="{ConfigViews.report_title}.csv"'
	
	return response

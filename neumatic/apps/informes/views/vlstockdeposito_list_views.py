# neumatic\apps\informes\views\vlstockdeposito_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLStockDeposito
from ..forms.buscador_vlstockdeposito_forms import BuscadorStockDepositoForm
from utils.utils import deserializar_datos, formato_argentino_entero, normalizar
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Stock en Depósitos de Clientes"
	
	#-- Modelo.
	model = VLStockDeposito
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorStockDepositoForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	model_string = model.__name__.lower()
	
	#-- Vistas del CRUD del modelo.
	list_view_name = f"{model_string}_list"
	
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
		"id_familia_id": {
			"label": "Id Familia",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_producto_familia": {
			"label": "Familia",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_modelo_id": {
			"label": "Id Modelo",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_modelo": {
			"label": "Modelo",
			"col_width_pdf": 0,
			"pdf": False,
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
		"medida": {
			"label": "Medida",
			"col_width_pdf": 70,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"cai": {
			"label": "CAI",
			"col_width_pdf": 105,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"nombre_producto": {
			"label": "Descripción",
			"col_width_pdf": 220,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_marca_id": {
			"label": "Id Marca",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_producto_marca": {
			"label": "Marca",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"stock": {
			"label": "En Stock",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
	}


class VLStockDepositoInformeView(InformeFormView):
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
		sucursal = cleaned_data.get("sucursal", None)
		
		id_sucursal = sucursal.id_sucursal if sucursal else None
		
		return VLStockDeposito.objects.obtener_datos(id_sucursal)
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando, calculando subtotales y totales generales, etc,
		tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		sucursal = cleaned_data.get("sucursal", None)
		
		param_left = {}
		param_right = {
			"Sucursal": f"[{sucursal.id_sucursal}] {sucursal.nombre_sucursal}" if sucursal else "Todas",
		}
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		# **************************************************
		#-- Estructura para agrupar datos por número de comprobante (optimizado).
		#-- (Sin necesidad de serializar).
		datos_por_familia = {}
		tg_stock = 0
		for obj in queryset:
			#-- Agrupar los objetos por Familia.
			id_familia = obj.id_familia_id
			if id_familia not in datos_por_familia:
				datos_por_familia[id_familia] = {
					'familia': obj.nombre_producto_familia,
					'modelos': {},
					'stf_stock': 0,
				}
			
			#-- Agrupar los objetos por Modelos de la Familia.
			id_modelo = obj.id_modelo_id
			if id_modelo not in datos_por_familia[id_familia]['modelos']:
				datos_por_familia[id_familia]['modelos'][id_modelo] = {
					'modelo': obj.nombre_modelo,
					'detalle': [],
					'stm_stock': 0,
				}
			
			#-- Crear el diccionario con los datos del detalle.
			detalle_data = {
				"codigo": obj.id_producto_id,
				"medida": obj.medida,
				"cai": obj.cai,
				"descripcion": obj.nombre_producto,
				"marca": obj.nombre_producto_marca,
				"stock": obj.stock,
			}
			#-- Agregar el detalle a la lista del comprobante.
			datos_por_familia[id_familia]['modelos'][id_modelo]["detalle"].append(detalle_data)
			
			#-- Acumular totales por Familia.
			datos_por_familia[id_familia]['stf_stock'] += obj.stock
			
			#-- Acumular totales por Modelo.
			datos_por_familia[id_familia]['modelos'][id_modelo]['stm_stock'] += obj.stock
			
			#-- Acumular totales generales.
			tg_stock += obj.stock
		# **************************************************
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": datos_por_familia,
			"tg_stock": tg_stock,
			"parametros_i": param_left,
			"parametros_d": param_right,
			'fecha_hora_reporte': fecha_hora_reporte,
			'titulo': ConfigViews.report_title,
			'css_url': static('css/reportes.css')
		}
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		form = kwargs.get("form") or self.get_form()
		context["form"] = form
		
		return context


def vlstockdeposito_vista_pantalla(request):
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


def vlstockdeposito_vista_pdf(request):
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
	generator = CustomPDFGenerator(contexto_reporte, pagesize=portrait(A4), body_font_size=7)
	
	#-- Construir datos de la tabla:
	
	#-- Obtener los títulos de las columnas (headers).
	headers_titles = [value['label'] for value in ConfigViews.table_info.values() if value['pdf']]
	headers_titles.insert(0, "")
	
	#-- Extrae los anchos de las columnas de la estructura ConfigViews.table_info.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	col_widths.insert(0, 10)
	blank_cols = [""] * 5
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (6,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	objetos = contexto_reporte.get("objetos", {})
	
	for familia_data in objetos.values():
		
		#-- Datos agrupado por Familia.
		table_data.append([f"Familia: {familia_data['familia']}", ""] + blank_cols)
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		#---------------------
		
		for modelo_data in familia_data["modelos"].values():
			
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
					obj['codigo'],
					obj['medida'],
					obj['cai'] if obj['cai'] else "",
					Paragraph(str(obj['descripcion']), generator.styles['CellStyle']),
					Paragraph(str(obj['marca']), generator.styles['CellStyle']),
					formato_argentino_entero(obj['stock']),
				])
				current_row += 1
			
			#-- Fila subtotal por Modelo.
			table_data.append(
				[""]*5 + 
				[
					"Sub Total Modelo:", 
					formato_argentino_entero(modelo_data["stm_stock"]), 
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
			[""]*5 + 
			[
				"Sub Total Familia:", 
				formato_argentino_entero(familia_data["stf_stock"]), 
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
	tg_stock = contexto_reporte.get("tg_stock", 0)
	
	table_data.append(
		[""]*5 + 
		[
			"Total General:", 
			formato_argentino_entero(tg_stock), 
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


def vlstockdeposito_vista_excel(request):
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
	view_instance = VLStockDepositoInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Extraer Títulos de las columnas (headers).
	headers = {field: ConfigViews.table_info[field] for field in ConfigViews.table_info if ConfigViews.table_info[field]['excel'] }
	
	helper = ExportHelper(
		queryset=queryset,
		table_info=headers,
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


def vlstockdeposito_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLStockDepositoInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Extraer Títulos de las columnas (headers).
	headers = {field: ConfigViews.table_info[field] for field in ConfigViews.table_info if ConfigViews.table_info[field]['csv'] }
	
	#-- Usar el helper para exportar a CSV.
	helper = ExportHelper(
		queryset=queryset,
		table_info=headers,
		report_title=ConfigViews.report_title
	)
	csv_data = helper.export_to_csv()
	
	response = HttpResponse(csv_data, content_type="text/csv; charset=utf-8")
	response["Content-Disposition"] = f'inline; filename="{ConfigViews.report_title}.csv"'
	
	return response

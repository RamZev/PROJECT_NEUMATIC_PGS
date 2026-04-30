# apps\informes\views\vlstockfecha_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLStockFecha
from ..forms.buscador_vlstockfecha_forms import BuscadorStockFechaForm
from utils.utils import deserializar_datos, formato_argentino_entero, normalizar, raw_to_dict
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Listado de Stock a Fecha"
	
	#-- Modelo.
	model = VLStockFecha
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorStockFechaForm
	
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
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_cai_id": {
			"label": "Id CAI",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"cai": {
			"label": "CAI",
			"col_width_pdf": 90,
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
		"nombre_producto": {
			"label": "Descripción",
			"col_width_pdf": 280,
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
			"col_width_pdf": 180,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"stock": {
			"label": "Stock",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
	}


class VLStockFechaInformeView(InformeFormView):
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
		id_producto_desde = cleaned_data.get('id_producto_desde', None)
		id_producto_hasta = cleaned_data.get('id_producto_hasta', None)
		fecha = cleaned_data.get("fecha")
		
		queryset = VLStockFecha.objects.obtener_datos(
			id_producto_desde,
			id_producto_hasta,
			fecha=fecha,
		)
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		id_producto_desde = cleaned_data.get('id_producto_desde', None)
		id_producto_hasta = cleaned_data.get('id_producto_hasta', None)
		fecha = cleaned_data.get("fecha")
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		producto = "Todos"
		if id_producto_desde and id_producto_hasta:
			producto = f"Desde: {id_producto_desde} - Hasta: {id_producto_hasta}"
		elif id_producto_desde:
			producto = f"Desde: {id_producto_desde}"
		elif id_producto_hasta:
			producto = f"Hasta: {id_producto_hasta}"
		
		param_left = {}
		param_right = {
			"Producto": producto,
			"Fecha": fecha.strftime("%d/%m/%Y") if fecha else "No especificada",
		}
		
		# **************************************************
		
		#-- Convertir QUERYSET a LISTA DE DICCIONARIOS al inicio (optimización clave).
		queryset_list = [raw_to_dict(obj) for obj in queryset]
		
		grouped_data = {}
		
		for obj in queryset_list:
			#-- Agrupar los objetos por Familia.
			id_familia = obj['id_familia_id']
			if id_familia not in grouped_data:
				grouped_data[id_familia] = {
					'familia': obj['nombre_producto_familia'],
					'modelos': {},
				}
			
			#-- Agrupar los objetos por Modelos de la Familia.
			id_modelo = obj['id_modelo_id']
			if id_modelo not in grouped_data[id_familia]['modelos']:
				grouped_data[id_familia]['modelos'][id_modelo] = {
					'modelo': obj['nombre_modelo'],
					'detalle': [],
				}
			
			#-- Añadir el detalle.
			grouped_data[id_familia]["modelos"][id_modelo]["detalle"].append(obj)
			
			
		# **************************************************
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": grouped_data,
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
		if form.errors:
			context["data_has_errors"] = True
		return context


def vlstockfecha_vista_pantalla(request):
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


def vlstockfecha_vista_pdf(request):
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
		"""Personalización del Header-bottom-right"""
		
		params = context.get("parametros_d", {})
		return "<br/>".join([f"<b>{k}:</b> {v}" for k, v in params.items()])


def generar_pdf(contexto_reporte):
	#-- Crear instancia del generador personalizado.
	generator = CustomPDFGenerator(contexto_reporte, pagesize=landscape(A4), body_font_size=8)
	
	valorizado = contexto_reporte.get("valorizado", False)
	
	#-- Construir datos de la tabla:
	
	#-- Títulos de las columnas de la tabla (headers) filtrados.
	headers_titles = [value['label'] for value in ConfigViews.table_info.values() if value['pdf']]
	headers_titles.insert(0, "")
	
	#-- Extraer Ancho de las columnas de la tabla filtrados.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	col_widths.insert(0, 10)
	blank_cols = [""] * 6
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (6,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	for familia_data in contexto_reporte.get("objetos", {}).values():
		
		#-- Datos agrupado por Familia.
		table_data.append([f"Familia: {familia_data['familia']}"] + blank_cols)
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		
		for modelo_data in familia_data["modelos"].values():
			
			#-- Datos agrupado por Modelo.
			table_data.append(["", f"Modelo: {modelo_data['modelo']}"] + blank_cols[:-1])
			
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
					obj['id_producto_id'],
					obj['cai'] if obj['cai'] else "",
					obj['medida'],
					Paragraph(str(obj['nombre_producto']), generator.styles['CellStyle']),
					Paragraph(str(obj['nombre_producto_marca']), generator.styles['CellStyle']),
					formato_argentino_entero(obj['stock']),
				])
				
				current_row += 1
		
		#-- Fila divisoria.
		table_data.append([""] + blank_cols)
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlstockfecha_vista_excel(request):
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
	view_instance = VLStockFechaInformeView()
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


def vlstockfecha_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLStockFechaInformeView()
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

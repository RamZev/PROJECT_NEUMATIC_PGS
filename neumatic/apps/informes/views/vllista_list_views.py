# neumatic\apps\informes\views\vllista_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLLista
from ..forms.buscador_vllista_forms import BuscadorListaForm
from utils.utils import deserializar_datos, formato_argentino, normalizar, raw_to_dict
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Lista de Precios"
	
	#-- Modelo.
	model = VLLista
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorListaForm
	
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
		"id_producto": {
			"label": "Código",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True,
			"protected": True  #-- No se pueda editar en el Excel.
		},
		"id_cai_id": {
			"label": "Id CAI",  #-- Cuidado! Si se cambia el label se debe cambiar también en el método post() de la vista ProcesarActualizacionView.
			"col_width_pdf": 0,
			"pdf": False,
			"excel": False,
			"csv": True,
			"protected": True
		},
		"cai": {
			"label": "CAI",
			"col_width_pdf": 110,
			"pdf": True,
			"excel": True,
			"csv": False
		},
		"tipo_producto": {
			"label": "Tipo Producto",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True,
			"protected": True
		},
		"medida": {
			"label": "Medida",
			"col_width_pdf": 70,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"segmento": {
			"label": "Segmento",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"unidad": {
			"label": "Unidad",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
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
			"excel": False,
			"csv": False
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
			"excel": False,
			"csv": False
		},
		"nombre_producto": {
			"label": "Descripción",
			"col_width_pdf": 230,
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
			"excel": False,
			"csv": False
		},
		"precio": {
			"label": "Precio",
			"col_width_pdf": 60,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"costo": {
			"label": "Costo",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"descuento": {
			"label": "Desc.",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_alicuota_iva_id": {
			"label": "Id Alíc. IVA",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": False,
			"csv": True
		},
		"alicuota_iva": {
			"label": "Alic. IVA",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": False
		},
		"minimo": {
			"label": "Mínimo",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"despacho_1": {
			"label": "Despacho 1",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"despacho_2": {
			"label": "Despacho 2",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"fecha_fabricacion": {
			"label": "Fecha Fabricación",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_producto_estado_id": {
			"label": "Id Estado",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_producto_estado": {
			"label": "Estado",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": False,
			"csv": False
		},
		"descripcion_producto": {
			"label": "Descripción Producto",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"carrito": {
			"label": "Carrito",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"obliga_operario": {
			"label": "Obliga Operario",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"iva_exento": {
			"label": "IVA Exento",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
	}


class VLListaInformeView(InformeFormView):
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
		id_familia_desde = cleaned_data.get('id_familia_desde', None)
		id_familia_hasta = cleaned_data.get('id_familia_hasta', None)
		id_marca_desde = cleaned_data.get('id_marca_desde', None)
		id_marca_hasta = cleaned_data.get('id_marca_hasta', None)
		id_modelo_desde = cleaned_data.get('id_modelo_desde', None)
		id_modelo_hasta = cleaned_data.get('id_modelo_hasta', None)
		
		queryset = VLLista.objects.obtener_datos(
			id_familia_desde,
			id_familia_hasta,
			id_marca_desde,
			id_marca_hasta,
			id_modelo_desde,
			id_modelo_hasta
		)
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		id_familia_desde = cleaned_data.get('id_familia_desde', None)
		id_familia_hasta = cleaned_data.get('id_familia_hasta', None)
		id_marca_desde = cleaned_data.get('id_marca_desde', None)
		id_marca_hasta = cleaned_data.get('id_marca_hasta', None)
		id_modelo_desde = cleaned_data.get('id_modelo_desde', None)
		id_modelo_hasta = cleaned_data.get('id_modelo_hasta', None)
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		familia = "Todas"
		if id_familia_desde and id_familia_hasta:
			familia = f"Desde: {id_familia_desde} - Hasta: {id_familia_hasta}"
		elif id_familia_desde:
			familia = f"Desde: {id_familia_desde}"
		elif id_familia_hasta:
			familia = f"Hasta: {id_familia_hasta}"
		
		marca = "Todas"
		if id_marca_desde and id_marca_hasta:
			marca = f"Desde: {id_marca_desde} - Hasta: {id_marca_hasta}"
		elif id_marca_desde:
			marca = f"Desde: {id_marca_desde}"
		elif id_marca_hasta:
			marca = f"Hasta: {id_marca_hasta}"
		
		modelo = "Todos"
		if id_modelo_desde and id_modelo_hasta:
			modelo = f"Desde: {id_modelo_desde} - Hasta: {id_modelo_hasta}"
		elif id_modelo_desde:
			modelo = f"Desde: {id_modelo_desde}"
		elif id_modelo_hasta:
			modelo = f"Hasta: {id_modelo_hasta}"
		
		
		param_left = {}
		param_right = {
			"Familia": familia,
			"Marca": marca,
			"Modelo": modelo,
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
					'detalle': [],
				}
			
			#-- Añadir el detalle.
			grouped_data[id_familia]["detalle"].append(obj)
			
		# **************************************************
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": grouped_data,
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


def vllista_vista_pantalla(request):
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


def vllista_vista_pdf(request):
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
		('ALIGN', (6,0), (6,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	for familia_id, familia_data in contexto_reporte.get("objetos", {}).items():
		
		#-- Datos agrupado por Familia.
		table_data.append([f"Familia: {familia_data['familia']}"] + blank_cols)
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		#---------------------
		
		#-- Agregar filas del detalle.
		for obj in familia_data['detalle']:
			
			table_data.append([
				"",
				obj['id_producto'],
				obj['cai'] if obj['cai'] else "",
				obj['medida'],
				Paragraph(str(obj['nombre_producto']), generator.styles['CellStyle']),
				Paragraph(str(obj['nombre_producto_marca']), generator.styles['CellStyle']),
				formato_argentino(obj['precio'])
			])
			
			current_row += 1
		
		#-- Fila divisoria.
		table_data.append([""] + blank_cols)
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vllista_vista_excel(request):
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
	view_instance = VLListaInformeView()
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


def vllista_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLListaInformeView()
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

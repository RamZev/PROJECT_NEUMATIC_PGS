# neumatic\apps\informes\views\descuentovendedor_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.maestros.models.descuento_vendedor_models import DescuentoVendedor
from ..forms.buscador_descuentovendedor_forms import BuscadorDescuentoVendedorForm
from utils.utils import deserializar_datos, normalizar, raw_to_dict
from utils.helpers.export_helpers import ExportHelper, PDFGenerator, add_row_table


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Descuento Vendedor"
	
	#-- Modelo.
	model = DescuentoVendedor
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorDescuentoVendedorForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	model_string = model.__name__.lower()
	
	#-- Plantilla base.
	template_list = f'{app_label}/maestro_informe.html'
	
	#-- Vista del home del proyecto.
	home_view_name = "home"
	
	#-- Archivo JavaScript específico.
	js_file = None
	
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
		"estatus_descuento_vendedor": {
			"label": "Estatus",
			"col_width_pdf": 30,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_marca_id": {
			"label": "ID Marca",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_marca__nombre_producto_marca": {
			"label": "Marca",
			"col_width_pdf": 100,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_familia_id": {
			"label": "ID Familia",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_familia__nombre_producto_familia": {
			"label": "Familia",
			"col_width_pdf": 120,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"desc1": {
			"label": "Col1",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc2": {
			"label": "Col2",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc3": {
			"label": "Col3",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc4": {
			"label": "Col4",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc5": {
			"label": "Col5",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc6": {
			"label": "Col6",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc7": {
			"label": "Col7",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc8": {
			"label": "Col8",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc9": {
			"label": "Col9",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc10": {
			"label": "Col10",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc11": {
			"label": "Col11",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc12": {
			"label": "Col12",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc13": {
			"label": "Col13",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc14": {
			"label": "Col14",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc15": {
			"label": "Col15",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc16": {
			"label": "Col16",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc17": {
			"label": "Col17",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc18": {
			"label": "Col18",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc19": {
			"label": "Col19",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc20": {
			"label": "Col20",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc21": {
			"label": "Col21",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc22": {
			"label": "Col22",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc23": {
			"label": "Col23",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc24": {
			"label": "Col24",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"desc25": {
			"label": "Col25",
			"col_width_pdf": 23,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
	}


class DescuentoVendedorInformeView(InformeFormView):
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
		estatus = cleaned_data.get('estatus', 'activos')
		id_marca_desde = cleaned_data.get('id_marca_desde', None)
		id_marca_hasta = cleaned_data.get('id_marca_hasta', None)
		id_familia_desde = cleaned_data.get('id_familia_desde', None)
		id_familia_hasta = cleaned_data.get('id_familia_hasta', None)

		#-- Crear el queryset base con select_related.
		queryset = ConfigViews.model.objects.select_related(
			"id_marca", "id_familia"
		)
		
		#-- Aplicar filtros.
		if estatus == "activos":
			queryset = queryset.filter(estatus_descuento_vendedor=True)
		elif estatus == "inactivos":
			queryset = queryset.filter(estatus_descuento_vendedor=False)
		
		if id_marca_desde and id_marca_hasta:
			#-- Filtrar por rango de marcas (ambos límites).
			marcas_ids = range(id_marca_desde, id_marca_hasta + 1)
			queryset = queryset.filter(id_marca_id__in=marcas_ids)
		elif id_marca_desde:
			#-- Filtrar por marcas desde el límite inferior.
			queryset = queryset.filter(id_marca_id__gte=id_marca_desde)
		elif id_marca_hasta:
			#-- Filtrar por marcas hasta el límite superior.
			queryset = queryset.filter(id_marca_id__lte=id_marca_hasta)		
		
		if id_familia_desde and id_familia_hasta:
			#-- Filtrar por rango de familias (ambos límites).
			familias_ids = range(id_familia_desde, id_familia_hasta + 1)
			queryset = queryset.filter(id_familia_id__in=familias_ids)
		elif id_familia_desde:
			#-- Filtrar por familias desde el límite inferior.
			queryset = queryset.filter(id_familia_id__gte=id_familia_desde)
		elif id_familia_hasta:
			#-- Filtrar por familias hasta el límite superior.
			queryset = queryset.filter(id_familia_id__lte=id_familia_hasta)
		
		#-- Ordenar el queryset.
		queryset = queryset.order_by("id_marca__nombre_producto_marca", "id_familia__nombre_producto_familia")
		
		#-- Usar values() para obtener directamente los datos necesarios.
		queryset = queryset.values(
			'estatus_descuento_vendedor',
			'id_marca_id',
			'id_marca__nombre_producto_marca',
			'id_familia_id',
			'id_familia__nombre_producto_familia',
			'desc1', 'desc2', 'desc3', 'desc4', 'desc5', 'desc6', 'desc7', 'desc8', 'desc9', 'desc10', 
			'desc11', 'desc12', 'desc13', 'desc14', 'desc15', 'desc16', 'desc17', 'desc18', 'desc19',
			'desc20', 'desc21', 'desc22', 'desc23', 'desc24', 'desc25'
		)
		
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		estatus = cleaned_data.get('estatus', 'activos')
		id_marca_desde = cleaned_data.get('id_marca_desde', None)
		id_marca_hasta = cleaned_data.get('id_marca_hasta', None)
		id_familia_desde = cleaned_data.get('id_familia_desde', None)
		id_familia_hasta = cleaned_data.get('id_familia_hasta', None)
		
		marca = "Todas"
		if id_marca_desde and id_marca_hasta:
			marca = f"Desde: {id_marca_desde} - Hasta: {id_marca_hasta}"
		elif id_marca_desde:
			marca = f"Desde: {id_marca_desde}"
		elif id_marca_hasta:
			marca = f"Hasta: {id_marca_hasta}"
		
		familia = "Todas"
		if id_familia_desde and id_familia_hasta:
			familia = f"Desde: {id_familia_desde} - Hasta: {id_familia_hasta}"
		elif id_familia_desde:
			familia = f"Desde: {id_familia_desde}"
		elif id_familia_hasta:
			familia = f"Hasta: {id_familia_hasta}"
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {}
		param_right = {
			"Estatus": estatus.capitalize(),
			"Marca": marca,
			"Familia": familia,
		}
		
		# **************************************************
		
		#-- Convertir QUERYSET a LISTA DE DICCIONARIOS al inicio (optimización clave).
		queryset_list = [raw_to_dict(obj) for obj in queryset]
		
		# **************************************************
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": queryset_list,
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
		
		return context


def descuentovendedor_vista_pantalla(request):
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


def descuentovendedor_vista_pdf(request):
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
	
	#-- Extraer los campos de las columnas de la tabla (headers).
	table_info = ConfigViews.table_info
	fields = [ field for field in table_info if table_info[field]['pdf']]
	
	#-- Extraer Títulos de las columnas de la tabla (headers).
	headers_titles = [value['label'] for value in table_info.values() if value['pdf']]
	
	#-- Extraer Ancho de las columnas de la tabla.
	col_widths = [value['col_width_pdf'] for value in table_info.values() if value['pdf']]
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (3,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Agregar los datos a la tabla.
	objetos = contexto_reporte.get("objetos", [])
	add_row_table(table_data, objetos, fields, table_info, generator)
	
	return generator.generate(table_data, col_widths, table_style_config)		


def descuentovendedor_vista_excel(request):
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
	view_instance = DescuentoVendedorInformeView()
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


def descuentovendedor_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = DescuentoVendedorInformeView()
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

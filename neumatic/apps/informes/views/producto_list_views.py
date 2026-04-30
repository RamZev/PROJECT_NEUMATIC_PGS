# neumatic\apps\informes\views\producto_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.maestros.models.producto_models import Producto
from ..forms.buscador_producto_forms import BuscadorProductoForm
from utils.utils import deserializar_datos, normalizar
from utils.helpers.export_helpers import ExportHelper, PDFGenerator, add_row_table


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Reporte de Productos"
	
	#-- Modelo.
	model = Producto
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorProductoForm
	
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
		"estatus_producto": {
			"label": "Estatus",
			"col_width_pdf": 40,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		'id_producto': {
			"label": "Código",
			"col_width_pdf": 45,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_cai_id": {
			"label": "Id. CAI",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_cai__cai": {
			"label": "CAI",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		'medida': {
			"label": "Medida",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		'nombre_producto': {
			"label": "Descripción",
			"col_width_pdf": 220,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_familia_id": {
			"label": "Id. Familia",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_familia__nombre_producto_familia": {
			"label": "Familia",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_modelo_id": {
			"label": "Id. Modelo",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_modelo__nombre_modelo": {
			"label": "Modelo",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		'id_marca_id': {
			"label": "Id. Marca",
			"col_width_pdf": 0,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		'id_marca__nombre_producto_marca': {
			"label": "Marca",
			"col_width_pdf": 140,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		'unidad': {
			"label": "Unidad",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		'precio': {
			"label": "Precio",
			"col_width_pdf": 70,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"tipo_producto": {
			"label": "Tipo Producto",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"segmento": {
			"label": "Segmento",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"fecha_fabricacion": {
			"label": "Fecha Fabricación",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"costo": {
			"label": "Costo",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"id_alicuota_iva_id": {
			"label": "Id. Alícuota IVA",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_alicuota_iva__alicuota_iva": {
			"label": "Alícuota IVA",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True,
			"type": "decimal"
		},
		"minimo": {
			"label": "Mínimo",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"descuento": {
			"label": "Descuento",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"despacho_1": {
			"label": "Despacho 1",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"despacho_2": {
			"label": "Despacho 2",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"carrito": {
			"label": "Carrito",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
	}


class ProductoInformeView(InformeFormView):
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
		id_familia_desde = cleaned_data.get('id_familia_desde')
		id_familia_hasta = cleaned_data.get('id_familia_hasta')
		id_marca_desde = cleaned_data.get('id_marca_desde')
		id_marca_hasta = cleaned_data.get('id_marca_hasta')
		id_modelo_desde = cleaned_data.get('id_modelo_desde')
		id_modelo_hasta = cleaned_data.get('id_modelo_hasta')
		
		#-- Crear el queryset base con select_related.
		queryset = ConfigViews.model.objects.select_related(
			"id_cai", "id_familia", "id_modelo", "id_marca", "id_alicuota_iva"
		)
		
		#-- Aplicar filtros.
		if estatus == "activos":
			queryset = queryset.filter(estatus_producto=True)
		elif estatus == "inactivos":
			queryset = queryset.filter(estatus_producto=False)
		
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
		
		if id_modelo_desde and id_modelo_hasta:
			#-- Filtrar por rango de modelos (ambos límites).
			modelos_ids = range(id_modelo_desde, id_modelo_hasta + 1)
			queryset = queryset.filter(id_modelo_id__in=modelos_ids)
		elif id_modelo_desde:
			#-- Filtrar por modelos desde el límite inferior.
			queryset = queryset.filter(id_modelo_id__gte=id_modelo_desde)
		elif id_modelo_hasta:
			#-- Filtrar por modelos hasta el límite superior.
			queryset = queryset.filter(id_modelo_id__lte=id_modelo_hasta)
		
		queryset = queryset.order_by('id_producto')
		
		#-- Usar values() para obtener directamente los datos necesarios.
		queryset = queryset.values(
			'estatus_producto',
			'id_producto',
			'id_cai_id',
			'id_cai__cai',
			'medida',
			'nombre_producto',
			'id_familia_id',
			'id_familia__nombre_producto_familia',
			'id_modelo_id',
			'id_modelo__nombre_modelo',
			'id_marca_id',
			'id_marca__nombre_producto_marca',
			'unidad',
			'precio',
			'tipo_producto',
			'segmento',
			'fecha_fabricacion',
			'costo',
			'id_alicuota_iva_id',
			'id_alicuota_iva__alicuota_iva',
			'minimo',
			'descuento',
			'despacho_1',
			'despacho_2',
			'carrito',
		)
		
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		estatus = cleaned_data.get('estatus', 'activos')
		id_familia_desde = cleaned_data.get('id_familia_desde')
		id_familia_hasta = cleaned_data.get('id_familia_hasta')
		id_marca_desde = cleaned_data.get('id_marca_desde')
		id_marca_hasta = cleaned_data.get('id_marca_hasta')
		id_modelo_desde = cleaned_data.get('id_modelo_desde')
		id_modelo_hasta = cleaned_data.get('id_modelo_hasta')
		
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
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {
			"Estatus": estatus.capitalize(),
		}
		param_right = {
			"Familia": familia,
			"Modelo": modelo,
			"Marca": marca,
		}
		
		# **************************************************
		
		#-- Convertir el queryset a lista de diccionarios.
		queryset_list = list(queryset)
		
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


def producto_vista_pantalla(request):
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


def producto_vista_pdf(request):
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
		('ALIGN', (1,0), (1,-1), 'RIGHT'),
		('ALIGN', (-1,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Agregar los datos a la tabla.
	objetos = contexto_reporte.get("objetos", [])
	add_row_table(table_data, objetos, fields, table_info, generator)
	
	return generator.generate(table_data, col_widths, table_style_config)		


def producto_vista_excel(request):
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
	view_instance = ProductoInformeView()
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


def producto_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = ProductoInformeView()
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

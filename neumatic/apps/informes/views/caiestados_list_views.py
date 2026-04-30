# neumatic\apps\informes\views\caiestados_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static
from django.db.models import OuterRef, Subquery
from django.core.cache import cache

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.maestros.models.base_models import MedidasEstados, ProductoCai, ProductoEstado
from apps.maestros.models.producto_models import Producto
from ..forms.buscador_caiestados_forms import BuscadorCaiEstadosForm
from utils.utils import deserializar_datos, normalizar, raw_to_dict
from utils.helpers.export_helpers import ExportHelper, PDFGenerator, add_row_table


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Reporte de CAIs Estados"
	
	#-- Modelo.
	model = MedidasEstados
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorCaiEstadosForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	# model_string = model.__name__.lower()
	model_string = "caiestados"
	
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
		"estatus_medida_estado": {
			"label": "Estatus",
			"col_width_table": 1,
			"col_width_pdf": 40,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": False,
			"csv": False
		},
		"cai_valor": {
			"label": "CAI",
			"col_width_pdf": 100,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"protected": True
		},
		"medida_valor": {
			"label": "Medida",
			"col_width_pdf": 70,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"protected": True
		},
		"nombre_producto_valor": {
			"label": "Descripción Producto",
			"col_width_pdf": 220,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"protected": True
		},
		"stock_desde": {
			"label": "Stock Desde",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "int"
		},
		"stock_hasta": {
			"label": "Stock Hasta",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"type": "int"
		},
		"estado_valor": {
			"label": "Estado",
			"col_width_pdf": 40,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
			"protected": True
		},
	}


class CaiEstadosInformeView(InformeFormView):
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
		medida = cleaned_data.get('medida', '').strip()
		nombre_producto = cleaned_data.get('nombre_producto', '').strip()
		
		#-- Base del queryset según estatus.
		if estatus:
			match estatus:
				case "activos":
					queryset = ConfigViews.model.objects.filter(estatus_medida_estado=True)
				case "inactivos":
					queryset = ConfigViews.model.objects.filter(estatus_medida_estado=False)
				case "todos":
					queryset = ConfigViews.model.objects.all()
		
		#-- Subquery para obtener el producto relacionado.
		producto_subquery = Producto.objects.filter(
			id_cai=OuterRef('id_cai')
		).values('medida', 'nombre_producto')[:1]
		
		#-- Aplicar filtros si existen.
		if medida:
			queryset = queryset.filter(id_cai__producto__medida__icontains=medida)
		
		if nombre_producto:
			queryset = queryset.filter(id_cai__producto__nombre_producto__icontains=nombre_producto)
		
		#-- ANNOTATE + SELECT_RELATED + DISTINCT: MÁXIMA EFICIENCIA (UNA SOLA CONSULTA).
		queryset = queryset.annotate(
			cai_valor=Subquery(
				ProductoCai.objects.filter(id_cai=OuterRef('id_cai')).values('cai')[:1]
			),
			medida_valor=Subquery(producto_subquery.values('medida')),
			nombre_producto_valor=Subquery(producto_subquery.values('nombre_producto')),
			estado_valor=Subquery(
				ProductoEstado.objects.filter(id_producto_estado=OuterRef('id_estado')).values('nombre_producto_estado')[:1]
			)
		).select_related(
			'id_cai',
			'id_estado'
		).distinct().order_by("cai_valor", "medida_valor", "nombre_producto_valor")
		
		return queryset
		
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		estatus = cleaned_data.get('estatus', 'activos')
		medida = cleaned_data.get('medida', '').strip()
		nombre_producto = cleaned_data.get('nombre_producto', '').strip()
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {
			"Medida": medida if medida else "Todas",
			"Descripción Producto": nombre_producto if nombre_producto else "Todos",
		}
		param_right = {
			"Estatus": estatus.capitalize(),
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


def caiestados_vista_pantalla(request):
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


def caiestados_vista_pdf(request):
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
		('ALIGN', (4,0), (5,-1), 'RIGHT'),
	]
	
	#-- Agregar los datos a la tabla.
	objetos = contexto_reporte.get("objetos", [])
	add_row_table(table_data, objetos, fields, table_info, generator)
	
	return generator.generate(table_data, col_widths, table_style_config)		


def caiestados_vista_excel(request):
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
	view_instance = CaiEstadosInformeView()
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


def caiestados_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = CaiEstadosInformeView()
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


# neumatic\apps\informes\views\proveedor_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

from django.db.models.functions import Lower
from django.db.models import Q

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.maestros.models.proveedor_models import Proveedor
from ..forms.buscador_proveedor_forms import BuscadorProveedorForm
from utils.utils import deserializar_datos, normalizar
from utils.helpers.export_helpers import ExportHelper, PDFGenerator, add_row_table
from entorno.constantes_base import ORDEN_CHOICES


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Reporte de Proveedores"
	
	#-- Modelo.
	model = Proveedor
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorProveedorForm
	
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
		"estatus_proveedor": {
			"label": "Estatus",
			"col_width_pdf": 30,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_proveedor": {
			"label": "Código",
			"col_width_pdf": 40,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"nombre_proveedor":{
			"label": "Nombre Proveedor",
			"col_width_pdf": 190,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"domicilio_proveedor": {
			"label": "Domicilio",
			"col_width_pdf": 160,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_localidad__nombre_localidad": {
			"label": "Localidad",
			"col_width_pdf": 140,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"codigo_postal": {
			"label": "C.P.",
			"col_width_pdf": 40,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_tipo_iva__codigo_iva": {
			"label": "IVA",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"cuit": {
			"label": "CUIT",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"telefono_proveedor": {
			"label": "Teléfono",
			"col_width_pdf": 100,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
	}


class ProveedorInformeView(InformeFormView):
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
		orden = cleaned_data.get('orden', 'nombre')
		desde = cleaned_data.get('desde', '').lower()
		hasta = cleaned_data.get('hasta', '').lower()
		
		#-- Crear el queryset base con select_related.
		queryset = ConfigViews.model.objects.select_related(
			"id_localidad", "id_tipo_iva"
		)
		
		#-- Aplicar filtros.
		if estatus == "activos":
			queryset = queryset.filter(estatus_proveedor=True)
		elif estatus == "inactivos":
			queryset = queryset.filter(estatus_proveedor=False)
		
		#-- Aplicar filtros por rango según orden.
		if orden == 'nombre':
			#-- Anotar para búsqueda insensible a mayúsculas/minúsculas
			queryset = queryset.annotate(nombre_lower=Lower('nombre_proveedor'))
			
			if desde and hasta:
				#-- Filtrar proveedores cuyos nombres comienzan con letras en el rango desde-hasta.
				queryset = queryset.filter(
					Q(nombre_lower__gte=desde) &                 #-- Nombres mayor o igual a "desde".
					Q(nombre_lower__lt=chr(ord(hasta[0]) + 1))   #-- Menor que la siguiente letra de "hasta".
				)
			elif desde:
				#-- Filtrar solo proveedores mayores o iguales a "desde".
				queryset = queryset.filter(nombre_lower__gte=desde)
			elif hasta:
				#-- Filtrar solo proveedores menores que la siguiente letra de "hasta".
				queryset = queryset.filter(nombre_lower__lt=chr(ord(hasta[0]) + 1))
			
			#-- Ordenar por nombre.
			queryset = queryset.order_by('nombre_proveedor')
		
		elif orden == 'codigo':
			if desde and hasta:
				queryset = queryset.filter(id_proveedor__range=(desde, hasta))
			elif desde:
				queryset = queryset.filter(id_proveedor__gte=desde)
			elif hasta:
				queryset = queryset.filter(id_proveedor__lte=hasta)

			#-- Ordenar por código.
			queryset = queryset.order_by('id_proveedor')
		
		#-- Usar values() para obtener directamente los datos necesarios.
		queryset = queryset.values(
			"estatus_proveedor",
			"id_proveedor",
			"nombre_proveedor",
			"domicilio_proveedor",
			"id_localidad__nombre_localidad",
			"codigo_postal",
			"id_tipo_iva__codigo_iva",
			"cuit",
			"telefono_proveedor",
		)
		
		return queryset

	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		estatus = cleaned_data.get('estatus', 'activos')
		orden = cleaned_data.get('orden', 'nombre')
		desde = cleaned_data.get('desde', '').lower()
		hasta = cleaned_data.get('hasta', '').lower()
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {
			"Estatus": estatus.capitalize(),
		}
		param_right = {
			"Ordenado por": dict(ORDEN_CHOICES).get(orden, "nombre"),
		}
		if desde and hasta:
			param_right.update({
				"Desde": desde,
				"Hasta": hasta,
				}
			)
		
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


def proveedor_vista_pantalla(request):
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


def proveedor_vista_pdf(request):
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
		('ALIGN', (1,0), (1,-1), 'RIGHT'),
	]
	
	#-- Agregar los datos a la tabla.
	objetos = contexto_reporte.get("objetos", [])
	add_row_table(table_data, objetos, fields, table_info, generator)
	
	return generator.generate(table_data, col_widths, table_style_config)		


def proveedor_vista_excel(request):
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
	view_instance = ProveedorInformeView()
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


def proveedor_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = ProveedorInformeView()
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

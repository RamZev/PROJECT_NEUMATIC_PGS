# neumatic\apps\informes\views\vltabladinamicadetalleventas_list_views.py

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
from apps.informes.models import VLTablaDinamicaDetalleVentas
from ..forms.buscador_vltabladinamicadetalleventas_forms import BuscadorTablaDinamicaDetalleVentasForm
from utils.utils import deserializar_datos, formato_argentino, normalizar, format_date, raw_to_dict
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Tablas Dinámicas de Ventas - Detalle de Ventas por Productos"
	
	#-- Modelo.
	model = VLTablaDinamicaDetalleVentas
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorTablaDinamicaDetalleVentasForm
	
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
		"id_factura_id": {
			"label": "ID Factura",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"comprobante": {
			"label": "Comprobante",
			"col_width_pdf": 65,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": True,
			"excel": False,
			"csv": False
		},
		"nombre_comprobante_venta": {
			"label": "Comprobante",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"letra_comprobante": {
			"label": "Letra",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"numero_comprobante": {
			"label": "Núnero",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"remito": {
			"label": "Remito",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"fecha_comprobante": {
			"label": "Fecha",
			"col_width_pdf": 35,
			"pdf_paragraph": False,
			"date_format": True,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"condicion_comprobante": {
			"label": "Condición",
			"col_width_pdf": 40,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_cliente_id": {
			"label": "Cliente",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_cliente": {
			"label": "Nombre Cliente",
			"col_width_pdf": 120,
			"pdf_paragraph": True,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"sitiva": {
			"label": "SITIVA",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"cuit": {
			"label": "CUIT",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"mayorista": {
			"label": "Mayorista",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"codigo_postal": {
			"label": "Cód. Postal",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_localidad": {
			"label": "Localidad",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_provincia": {
			"label": "Provincia",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_vendedor": {
			"label": "Vendedor",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"reventa": {
			"label": "Rvta.",
			"col_width_pdf": 25,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_producto_id": {
			"label": "Producto",
			"col_width_pdf": 30,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"cai": {
			"label": "CAI",
			"col_width_pdf": 60,
			"pdf_paragraph": True,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"nombre_producto": {
			"label": "Descripción",
			"col_width_pdf": 160,
			"pdf_paragraph": True,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"nombre_producto_marca": {
			"label": "Marca",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_producto_familia": {
			"label": "Familia",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"segmento": {
			"label": "Segmento",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"cantidad": {
			"label": "Cantidad",
			"col_width_pdf": 35,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"costo": {
			"label": "Costo",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"precio": {
			"label": "Precio",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"descuento": {
			"label": "Descuento",
			"col_width_pdf": 35,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"gravado": {
			"label": "Gravado",
			"col_width_pdf": 55,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"no_gravado": {
			"label": "No Gravado",
			"col_width_pdf": 55,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"alic_iva": {
			"label": "Alíc. IVA",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"iva": {
			"label": "IVA",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"total": {
			"label": "Total",
			"col_width_pdf": 55,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"no_estadist": {
			"label": "No_Estadist",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_user_id": {
			"label": "Operador",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_sucursal": {
			"label": "Sucursal",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_operario_id": {
			"label": "Cód. Operario",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_operario": {
			"label": "Operario",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"promo": {
			"label": "Promo",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": False,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_marketing_origen": {
			"label": "Conoció en",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
	}


class VLTablaDinamicaDetalleVentasInformeView(InformeFormView):
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
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		comprobantes_impositivos = cleaned_data.get('comprobantes_impositivos', True)
		
		queryset = VLTablaDinamicaDetalleVentas.objects.obtener_datos(
			fecha_desde, 
			fecha_hasta, 
			comprobantes_impositivos=comprobantes_impositivos,
		)
		
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		comprobantes_impositivos = cleaned_data.get('comprobantes_impositivos', True)
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {
			"Solo Comprobantes Impositivos": "Si" if comprobantes_impositivos else "No",
		}
		param_right = {
			"Desde": fecha_desde.strftime("%d/%m/%Y"),
			"Hasta": fecha_hasta.strftime("%d/%m/%Y"),
		}
		
		# **************************************************
		
		# **************************************************
		
		#-- Convertir cada objeto del queryset a un diccionario.
		objetos_serializables = [raw_to_dict(item) for item in queryset]
		
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": objetos_serializables,
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


def vltabladinamicadetalleventas_vista_pantalla(request):
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


def vltabladinamicadetalleventas_vista_pdf(request):
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
	generator = CustomPDFGenerator(contexto_reporte, pagesize=landscape(A4))
	
	#-- Construir datos de la tabla:
	
	#-- Extraer los campos de las columnas de la tabla (headers).
	fields = [ field for field in ConfigViews.table_info if ConfigViews.table_info[field]['pdf']]
	
	#-- Extraer Títulos de las columnas de la tabla (headers).
	headers_titles = [value['label'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	#-- Extraer Ancho de las columnas de la tabla.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (4,0), (4,-1), 'RIGHT'),
		('ALIGN', (7,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Agregar los datos a la tabla.
	for obj in contexto_reporte.get("objetos", []):
		row = []
		
		for field in fields:
			value = obj[field]
			
			if ConfigViews.table_info[field]['pdf_paragraph']:
				row.append(Paragraph(str(value) if value else "", generator.styles['CellStyle']))
			else:
				if ConfigViews.table_info[field]['date_format']:
					row.append(format_date(value) if value else "")
				elif isinstance(obj[field], (float, Decimal)):
					row.append(formato_argentino(value))
				else:
					row.append(value if value else "")
		
		table_data.append(row)
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vltabladinamicadetalleventas_vista_excel(request):
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
	view_instance = VLTablaDinamicaDetalleVentasInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Extraer Títulos de las columnas (headers).
	headers = {field: ConfigViews.table_info[field] for field in ConfigViews.table_info if ConfigViews.table_info[field]['excel'] }
	
	#-- Usar el helper para exportar a Excel.
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


def vltabladinamicadetalleventas_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLTablaDinamicaDetalleVentasInformeView()
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

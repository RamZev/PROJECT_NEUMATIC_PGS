# neumatic\apps\informes\views\vlsaldosclientes_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

#-- Para generar el PDF (ReportLab).
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLSaldosClientes
from ..forms.buscador_vlsaldosclientes_forms import BuscadorSaldosClientesForm
from utils.utils import deserializar_datos, format_date, normalizar, raw_to_dict
from apps.maestros.templatetags.custom_tags import formato_es_ar
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Saldos de Clientes"
	
	#-- Modelo.
	model = VLSaldosClientes
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorSaldosClientesForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	model_string = model.__name__.lower()
	
	# Vistas del CRUD del modelo
	list_view_name = f"{model_string}_list"  # <== vlventacompro_list
	
	#-- Plantilla base.
	template_list = f'{app_label}/maestro_informe.html'
	
	#-- Vista del home del proyecto.
	home_view_name = "home"
	
	#-- Archivo JavaScript específico.
	js_file = "js/filtros_saldos_clientes.js"
	
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
		"id_cliente_id": {
			"label": "Cliente",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"nombre_cliente": {
			"label": "Nombre",
			"col_width_pdf": 180,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"domicilio_cliente": {
			"label": "Domicilio",
			"col_width_pdf": 180,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"codigo_postal": {
			"label": "C.P.",
			"col_width_pdf": 30,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"nombre_localidad": {
			"label": "Localidad",
			"col_width_pdf": 100,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"telefono_cliente": {
			"label": "Teléfono",
			"col_width_pdf": 60,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_vendedor_id": {
			"label": "Vendedor",
			"col_width_pdf": 40,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_vendedor": {
			"label": "Nombre",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"saldo": {
			"label": "Saldo",
			"col_width_pdf": 60,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"primer_fact_impaga": {
			"label": "1er. Comp. Pend.",
			"col_width_pdf": 60,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"ultimo_pago": {
			"label": "Último Pago",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"sub_cuenta": {
			"label": "Sub Cuenta",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
	}


class VLSaldosClientesInformeView(InformeFormView):
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
		fecha_hasta = cleaned_data.get('fecha_hasta')
		vendedor = cleaned_data.get('vendedor', None)
		
		id_vendedor = vendedor.id_vendedor if vendedor else None
		
		queryset = VLSaldosClientes.objects.obtener_saldos_clientes(fecha_hasta, id_vendedor)
		
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		fecha_hasta = cleaned_data.get('fecha_hasta')
		vendedor = cleaned_data.get('vendedor')
		
		param_left = {}
		param_right = {
			"Hasta": fecha_hasta.strftime("%d/%m/%Y"),
		}
		
		if vendedor:
			param_right["Clientes del vendedor"] = f"[{vendedor.id_vendedor}] {vendedor.nombre_vendedor}" if vendedor else "Todos los Vendedores"
		else:
			param_right["Listado"] = "Todos los Clientes"
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")		
		
		#-- Convertir cada objeto del queryset a un diccionario.
		objetos_serializables = [raw_to_dict(item) for item in queryset]
		
		#-- Calcular el saldo total.
		saldo_total = sum(item.get('saldo', 0) for item in objetos_serializables)
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": objetos_serializables,
			'saldo_total': saldo_total,
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


def vlsaldosclientes_vista_pantalla(request):
	#-- Obtener el token de la querystring.
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Obtener el contexto(datos) previamente guardados en la sesión.
	# contexto_reporte = request.session.pop(token, None)
	contexto_reporte = deserializar_datos(request.session.pop(token, None))
	
	if not contexto_reporte:
		return HttpResponse("Contexto no encontrado o expirado", status=400)
	
	#-- Generar el listado a pantalla.
	return render(request, ConfigViews.reporte_pantalla, contexto_reporte)


def vlsaldosclientes_vista_pdf(request):
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
	
	#-- Obtener los títulos de las columnas (headers).
	header_data = [value['label'] for value in ConfigViews.table_info.values() if value['pdf']]
	table_data = [header_data]
	
	#-- Extrae los anchos de las columnas de la estructura ConfigViews.table_info.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	for obj in contexto_reporte.get("objetos", []):
		
		row = [
			obj.get("id_cliente_id", ""),
			Paragraph(str(obj.get("nombre_cliente", "")), generator.styles['CellStyle']),
			Paragraph(str(obj.get("domicilio_cliente", "")), generator.styles['CellStyle']),
			obj.get("codigo_postal") or "",
			Paragraph(str(obj.get("nombre_localidad") or ""), generator.styles['CellStyle']),
			obj.get("telefono_cliente") or "",
			formato_es_ar(obj.get("saldo", 0)),
			format_date(obj.get("primer_fact_impaga", "")),
			format_date(obj.get("ultimo_pago", "")),
			obj.get("sub_cuenta", "")
		]
		table_data.append(row)
		
	#-- Agregar fila de total.
	saldo_total = contexto_reporte.get("saldo_total", 0)
	total_row = ["", "", "", "", "", "Total Pendiente:", 
				formato_es_ar(saldo_total), "", "", ""]
	table_data.append(total_row)
	
	#-- Configuración específica de la tabla de datos:
	
	#-- Estilos específicos adicionales de la tabla.
	table_style_config = [
		('ALIGN', (6,0), (6,-1), 'RIGHT'),
		('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
		('LINEABOVE', (0, len(table_data)-1), (-1, len(table_data)-1), 0.5, colors.black),
		('FONTNAME', (0, len(table_data)-1), (-1, len(table_data)-1), 'Helvetica-Bold')
	]
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlsaldosclientes_vista_excel(request):
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
	view_instance = VLSaldosClientesInformeView()
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


def vlsaldosclientes_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLSaldosClientesInformeView()
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

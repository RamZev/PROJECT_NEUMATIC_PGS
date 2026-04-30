# neumatic\apps\informes\views\vlventasinestadistica_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLVentaSinEstadistica
from ..forms.buscador_vlventasinestadistica_forms import BuscadorVentaSinEstadisticaForm
from utils.utils import deserializar_datos, formato_argentino, normalizar, format_date, raw_to_dict
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Comprobantes sin Estadísticas"
	
	#-- Modelo.
	model = VLVentaSinEstadistica
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorVentaSinEstadisticaForm
	
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
		"fecha_comprobante": {
			"label": "Fecha",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"comprobante": {
			"label": "Comprobante",
			"col_width_pdf": 75,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_cliente_id": {
			"label": "Cliente",
			"col_width_pdf": 35,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"nombre_cliente": {
			"label": "Nombre",
			"col_width_pdf": 190,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"total": {
			"label": "Importe",
			"col_width_pdf": 65,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_vendedor_id": {
			"label": "Cód. Vendedor",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_vendedor": {
			"label": "Vendedor",
			"col_width_pdf": 130,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"sub_cuenta": {
			"label": "Sub-Cta.",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_sucursal_id": {
			"label": "Cód. Suc.",
			"col_width_pdf": 30,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_sucursal": {
			"label": "Sucursal",
			"col_width_pdf": 120,
			"pdf": False,
			"excel": True,
			"csv": True
		},
	}


class VLVentaSinEstadisticaInformeView(InformeFormView):
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
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		orden = cleaned_data.get('orden')
		
		id_sucursal = sucursal.id_sucursal if sucursal else None
		
		queryset = VLVentaSinEstadistica.objects.obtener_datos(
			fecha_desde, 
			fecha_hasta, 
			id_sucursal=id_sucursal,
			orden=orden
		)
		
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		sucursal = cleaned_data.get('sucursal', None)
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		orden = cleaned_data.get('orden')
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {
			"Sucursal": f"[{sucursal.id_sucursal}] {sucursal.nombre_sucursal}" if sucursal else "Todas",
			"Ordenado por": "Nombre Cliente" if orden == "nombre" else "Código Cliente",
		}
		param_right = {
			"Desde": fecha_desde.strftime("%d/%m/%Y"),
			"Hasta": fecha_hasta.strftime("%d/%m/%Y"),
		}
		
		# **************************************************
		#-- Estructura para agrupar datos por cliente.
		datos_por_cliente = {}
		total_general = float(0)
		
		for obj in queryset:
			#-- Identificar al cliente.
			cliente_id = obj.id_cliente_id
			
			#-- Si el cliente aún no está en el diccionario, se inicializa.
			if cliente_id not in datos_por_cliente:
				datos_por_cliente[cliente_id] = {
					"comprobantes": [],
					"total_cliente": float(0),
				}
			
			#-- Añadir el detalle al grupo.
			datos_por_cliente[cliente_id]["comprobantes"].append(raw_to_dict(obj))
			
			#-- Acumular totales.
			datos_por_cliente[cliente_id]["total_cliente"] += float(obj.total)
			total_general += float(obj.total)
		
		# **************************************************
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": datos_por_cliente,
			"total_general": total_general,
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


def vlventasinestadistica_vista_pantalla(request):
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


def vlventasinestadistica_vista_pdf(request):
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
	
	#-- Extraer Títulos de las columnas de la tabla (headers).
	headers_titles = [value['label'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	#-- Extraer Ancho de las columnas de la tabla.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (2,0), (2,-1), 'RIGHT'),
		('ALIGN', (4,0), (4,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	
	for obj in contexto_reporte.get("objetos", {}).values():
		#-- Agregar filas del detalle.
		for comprobante in obj['comprobantes']:
			table_data.append([
				format_date(comprobante['fecha_comprobante']),
				comprobante['comprobante'],
				comprobante['id_cliente_id'],
				Paragraph(str(comprobante['nombre_cliente']), generator.styles['CellStyle']),
				formato_argentino(comprobante['total']),
				Paragraph(str(comprobante['nombre_vendedor']), generator.styles['CellStyle']),
				comprobante['sub_cuenta']
			])
			current_row += 1
			
		#-- Fila Total por Cliente.
		table_data.append(["", "", "", "Total Cliente:", formato_argentino(obj['total_cliente'])])
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			('ALIGN', (3,current_row), (4,current_row), 'RIGHT'),
			# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
		])
		
		current_row += 1
		
		#-- Fila divisoria.
		table_data.append(["", "", "", "", "", "", ""])
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
	
	#-- Fila Total General.
	table_data.append(["", "", "", "Total General:", formato_argentino(contexto_reporte.get('total_general'))])
	
	#-- Aplicar estilos a la fila de total (fila actual).
	table_style_config.extend([
		('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
		('ALIGN', (3,current_row), (4,current_row), 'RIGHT'),
		# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
	])
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlventasinestadistica_vista_excel(request):
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
	view_instance = VLVentaSinEstadisticaInformeView()
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


def vlventasinestadistica_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLVentaSinEstadisticaInformeView()
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

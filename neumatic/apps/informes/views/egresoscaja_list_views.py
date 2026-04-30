# neumatic\apps\informes\views\egresoscaja_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static
from django.db.models import F, Value
from django.db.models.functions import Concat, Substr, Cast, LPad
from django.db.models import Value, CharField

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.ventas.models.caja_models import CajaDetalle
from ..forms.buscador_egresoscaja_forms import BuscadorEgresosCajaForm
from utils.utils import deserializar_datos, normalizar, format_date, formato_argentino
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Egresos de Caja"
	
	#-- Modelo.
	# model = CajaDetalle
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorEgresosCajaForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	# model_string = model.__name__.lower()
	model_string = "egresoscaja"
	
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
		"numero_caja_formateado": {
			"label": "Caja",
			"col_width_pdf": 60,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
		},
		"id_caja__fecha_caja": {
			"label": "Fecha Caja",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": '%d/%m/%Y',
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"observacion": {
			"label": "Detalle",
			"col_width_pdf": 200,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"importe": {
			"label": "Importe",
			"col_width_pdf": 80,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_caja__id_sucursal": {
			"label": "ID Suc.",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_caja__id_sucursal__nombre_sucursal": {
			"label": "Sucursal",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
	}


class EgresosCajaInformeView(InformeFormView):
	config = ConfigViews  #-- Ahora la configuración estará disponible en self.config.
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_list
	
	extra_context = {
		"master_title": f'Informes - {ConfigViews.report_title}',
		"home_view_name": ConfigViews.home_view_name,
		"buscador_template": f"{ConfigViews.app_label}/buscador_{ConfigViews.model_string}.html",
		"js_file": ConfigViews.js_file,
		"url_pantalla": ConfigViews.url_pantalla,
		"url_pdf": ConfigViews.url_pdf,
	}
	
	def obtener_queryset(self, cleaned_data):
		sucursal = cleaned_data.get("sucursal")
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		
		#-- Iniciar el queryset.
		queryset = CajaDetalle.objects.select_related(
			'id_caja'
		).filter(
			#--Aplicar filtros obligatorios.
			tipo_movimiento=2,
			id_caja__fecha_caja__range=(fecha_desde, fecha_hasta)
		)
		
		if sucursal:
			#--Aplicar filtros opcionales.
			queryset = queryset.filter(
				id_caja__id_sucursal=sucursal,
			)
		
		queryset = queryset.annotate(
			#-- Convertir número a texto con ceros.
			numero_texto=LPad(
				Cast(F('id_caja__numero_caja'), CharField()),
				8,
				Value('0')
			)
		).annotate(
			#-- Crear el formato final.
			numero_caja_formateado=Concat(
				Substr(F('numero_texto'), 1, 2),
				Value('-'),
				Substr(F('numero_texto'), 3, 8)
			)
		).values(
			'numero_caja_formateado',
			'id_caja__fecha_caja',
			'observacion',
			'importe',
			'id_caja__id_sucursal',
			'id_caja__id_sucursal__nombre_sucursal',
		).order_by('id_caja__fecha_caja', 'numero_caja_formateado')
		
		return list(queryset)
		
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		sucursal = cleaned_data.get("sucursal")
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {}
		param_right = {
			"Sucursal": f"[{sucursal.id_sucursal}] {sucursal.nombre_sucursal}" if sucursal else "Todas",
			"Fecha desde": fecha_desde.strftime("%d/%m/%Y"),
			"Fecha hasta": fecha_hasta.strftime("%d/%m/%Y"),
		}
		
		# **************************************************
		
		datos_estructurados = {}
		total_general = 0.0
		for item in queryset:
			# caja = item['id_caja__numero_caja']
			caja = item['numero_caja_formateado']
			if caja not in datos_estructurados:
				datos_estructurados[caja] = {
					'egresos': [],
					'subtotal': 0.0
				}
			datos_estructurados[caja]['egresos'].append(item)
			datos_estructurados[caja]['subtotal'] += float(item['importe'] or 0.0)
			total_general += float(item['importe'] or 0.0)
		
		# **************************************************
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": datos_estructurados,
			"total_general": total_general,
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


def egresoscaja_vista_pantalla(request):
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


def egresoscaja_vista_pdf(request):
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
	
	#-- Extrae los anchos de las columnas de la estructura ConfigViews.table_info.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (3,0), (3,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	
	for datos in contexto_reporte.get("objetos", []).values():
		
		#-- Agregar filas del detalle.
		egreso_anterior = None
		
		for egreso in datos['egresos']:
			if egreso['numero_caja_formateado'] != egreso_anterior:
				table_data.append([
					egreso['numero_caja_formateado'],
					format_date(egreso['id_caja__fecha_caja']),
					Paragraph(str(egreso['observacion']), generator.styles['CellStyle']),
					formato_argentino(egreso['importe']),
				])
			else:
				table_data.append([
					'',
					'',
					Paragraph(str(egreso['observacion']), generator.styles['CellStyle']),
					formato_argentino(egreso['importe']),
				])
			egreso_anterior = egreso['numero_caja_formateado']
			current_row += 1
		
		#-- Fila Total por Caja.
		table_data.append([f"Total a la Fecha:", "", "", formato_argentino(datos['subtotal'])])
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			('SPAN', (0,current_row), (-2,current_row)),
			('ALIGN', (0,current_row), (-1,current_row), 'RIGHT'),
			# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
		])
		
		current_row += 1
		
		#-- Fila divisoria.
		table_data.append(["", "", "", ""])
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
	
	#-- Fila Total General.
	table_data.append(["Total de Egresos:", "", "",  formato_argentino(contexto_reporte.get('total_general'))])
	
	#-- Aplicar estilos a la fila de total (fila actual).
	table_style_config.extend([
		('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
		('SPAN', (0,current_row), (-2,current_row)),
		('ALIGN', (0,current_row), (-1,current_row), 'RIGHT'),
		# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
	])
	
	return generator.generate(table_data, col_widths, table_style_config)


def egresoscaja_vista_excel(request):
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
	view_instance = EgresosCajaInformeView()
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


def egresoscaja_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = EgresosCajaInformeView()
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

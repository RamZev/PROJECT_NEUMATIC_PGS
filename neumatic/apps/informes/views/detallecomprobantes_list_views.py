# neumatic\apps\informes\views\detallecomprobantes_list_views.py

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
from apps.ventas.models.factura_models import Factura
from apps.ventas.models.caja_models import Caja
from ..forms.buscador_detallecomprobantes_forms import BuscadorDetalleComprobantesForm
from utils.utils import deserializar_datos, normalizar, format_date, formato_argentino, format_user_display
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Comprobantes de Venta"
	
	#-- Modelo.
	# model = Factura
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorDetalleComprobantesForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	# model_string = model.__name__.lower()
	model_string = "detallecomprobantes"
	
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
		"id_factura": {
			"label": "ID",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True,
		},
		"id_comprobante_venta__nombre_comprobante_venta": {
			"label": "Compro",
			"col_width_pdf": 80,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True,
		},
		"comprobante_completo": {
			"label": "Comprobante",
			"col_width_pdf": 70,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"fecha_comprobante": {
			"label": "Fecha",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_cliente": {
			"label": "Cód.",
			"col_width_pdf": 40,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_cliente__nombre_cliente": {
			"label": "Cliente",
			"col_width_pdf": 220,
			"pdf_paragraph": True,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"condicion_comprobante": {
			"label": "Condición",
			"col_width_pdf": 40,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"total_calculado": {
			"label": "Total",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"contado": {
			"label": "Contado",
			"col_width_pdf": 70,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": False,
			"csv": False
		},
		"cta_cte": {
			"label": "Cta. Cte.",
			"col_width_pdf": 70,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": False,
			"csv": False
		},
		"id_user__iniciales": {
			"label": "Op.",
			"col_width_pdf": 30,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_sucursal": {
			"label": "ID Suc.",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_sucursal__nombre_sucursal": {
			"label": "Sucursal",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"no_estadist": {
			"label": "No Estadística",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
	}


class DetalleComprobantesInformeView(InformeFormView):
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
		caja = cleaned_data.get('caja', 0)
		
		caja_obj = Caja.objects.filter(numero_caja=caja).first()
		
		queryset = Factura.objects.select_related(
			'id_comprobante_venta',
			'id_cliente',
			'id_sucursal',
			'id_user'
		).filter(
			no_estadist=False,
			id_caja=caja_obj,
		).exclude(
			id_comprobante_venta__mult_caja=0
		).annotate(
			#-- Convertir número a texto con ceros.
			numero_texto=LPad(
				Cast(F('numero_comprobante'), CharField()),
				12,
				Value('0')
			)
		).annotate(
			#-- Crear el formato final.
			comprobante_completo=Concat(
				F('letra_comprobante'),
				Value('  '),
				Substr(F('numero_texto'), 1, 4),
				Value('-'),
				Substr(F('numero_texto'), 5, 8)
			)
		).annotate(
			total_calculado=F('total') * F('id_comprobante_venta__mult_caja')			
		).values(
			'id_factura',
			'id_comprobante_venta__nombre_comprobante_venta',
			'comprobante_completo',
			'fecha_comprobante',
			'id_cliente',
			'id_cliente__nombre_cliente',
			'condicion_comprobante',
			'total_calculado',
			'id_user__iniciales',
			'id_sucursal',
			'id_sucursal__nombre_sucursal',
			'no_estadist',
		).order_by('id_comprobante_venta__nombre_comprobante_venta', 'comprobante_completo')
		
		return list(queryset)
		
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		caja = cleaned_data.get('caja', 0)
		caja_obj = Caja.objects.filter(numero_caja=caja).first()
		
		usuario_caja = format_user_display(caja_obj.id_user)
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {
			"Sucursal": f"[{caja_obj.id_sucursal.id_sucursal}] {caja_obj.id_sucursal.nombre_sucursal}" if caja_obj else "",
			"Usuario": usuario_caja,
		}
		param_right = {
			"Número de Caja": f"{str(caja_obj.numero_caja).zfill(8)[:2]}-{str(caja_obj.numero_caja).zfill(8)[2:]}" if caja_obj else "",
			"Fecha de Caja": caja_obj.fecha_caja.strftime("%d/%m/%Y") if caja_obj.fecha_caja else "",
		}
		
		# **************************************************
		
		datos_estructurados = {}
		total_contado = 0.0
		total_cta_cte = 0.0
		for item in queryset:
			compro = item['id_comprobante_venta__nombre_comprobante_venta']
			if compro not in datos_estructurados:
				datos_estructurados[compro] = {
					'comprobantes': [],
					'subtotal_contado': 0.0,
					'subtotal_cta_cte': 0.0
				}
			datos = {
				'id_comprobante_venta__nombre_comprobante_venta': item['id_comprobante_venta__nombre_comprobante_venta'],
				'comprobante_completo': item['comprobante_completo'],
				'fecha_comprobante': item['fecha_comprobante'],
				'id_cliente': item['id_cliente'],
				'id_cliente__nombre_cliente': item['id_cliente__nombre_cliente'],
				'condicion_comprobante': item['condicion_comprobante'],
				'contado': float(item['total_calculado'] or 0.0) if item['condicion_comprobante'] == 1 else 0.0,
				'cta_cte': float(item['total_calculado'] or 0.0) if item['condicion_comprobante'] == 2 else 0.0,
				'id_user__iniciales': item['id_user__iniciales'],
				'id_sucursal': item['id_sucursal'],
				'id_sucursal__nombre_sucursal': item['id_sucursal__nombre_sucursal'],
			}
			datos_estructurados[compro]['comprobantes'].append(datos)
			datos_estructurados[compro]['subtotal_contado'] += float(item['total_calculado'] or 0.0) if item['condicion_comprobante'] == 1 else 0.0
			datos_estructurados[compro]['subtotal_cta_cte'] += float(item['total_calculado'] or 0.0) if item['condicion_comprobante'] == 2 else 0.0
			total_contado += float(item['total_calculado'] or 0.0) if item['condicion_comprobante'] == 1 else 0.0
			total_cta_cte += float(item['total_calculado'] or 0.0) if item['condicion_comprobante'] == 2 else 0.0

		# **************************************************
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": datos_estructurados,
			"total_contado": total_contado,
			"total_cta_cte": total_cta_cte,
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


def detallecomprobantes_vista_pantalla(request):
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


def detallecomprobantes_vista_pdf(request):
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
	headers_titles.insert(0, "")
	
	#-- Extrae los anchos de las columnas de la estructura ConfigViews.table_info.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	col_widths.insert(0, 10)
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (3,0), (3,-1), 'RIGHT'),
		('ALIGN', (5,0), (6,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	
	for compro, datos in contexto_reporte.get("objetos", []).items():
		#-- Datos agrupado por Tipo de Comprobante.
		table_data.append([
			f"{compro.upper()}",
			"", "", "", "", "", "", ""
		])
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		
		#-- Agregar filas del detalle.
		for comprobante in datos['comprobantes']:
			table_data.append([
				'',
				format_date(comprobante['fecha_comprobante']),
				comprobante['comprobante_completo'],
				comprobante['id_cliente'],
				Paragraph(str(comprobante['id_cliente__nombre_cliente']), generator.styles['CellStyle']),
				formato_argentino(comprobante['contado']),
				formato_argentino(comprobante['cta_cte']),
				comprobante['id_user__iniciales'],
			])
			current_row += 1
		
		#-- Fila Total por Tipo de Comprobante.
		table_data.append([
			f"Totales Comprobante {compro.upper()}:",
			"", "", "", "",
			formato_argentino(datos['subtotal_contado']),
			formato_argentino(datos['subtotal_cta_cte']),
			""
		])
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			('SPAN', (0,current_row), (-4,current_row)),
			('ALIGN', (0,current_row), (-1,current_row), 'RIGHT'),
			# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
		])
		
		current_row += 1
		
		#-- Fila divisoria.
		table_data.append(["", "", "", "", "", "", "", ""])
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
	
	#-- Fila Total General.
	table_data.append([
		"Total General:",
		"", "", "", "",
		formato_argentino(contexto_reporte.get('total_contado')),
		formato_argentino(contexto_reporte.get('total_cta_cte')),
		""
	])
	
	#-- Aplicar estilos a la fila de total (fila actual).
	table_style_config.extend([
		('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
		('SPAN', (0,current_row), (-4,current_row)),
		('ALIGN', (0,current_row), (-1,current_row), 'RIGHT'),
		# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
	])
	
	return generator.generate(table_data, col_widths, table_style_config)


def detallecomprobantes_vista_excel(request):
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
	view_instance = DetalleComprobantesInformeView()
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


def detallecomprobantes_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = DetalleComprobantesInformeView()
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

# neumatic\apps\informes\views\chequefecha_list_views.py

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
from apps.ventas.models.recibo_models import ChequeRecibo
from ..forms.buscador_chequesfecha_forms import BuscadorChequesFechaForm
from utils.utils import deserializar_datos, normalizar, format_date, formato_argentino
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Detalle de Cheques por fecha"
	
	#-- Modelo.
	# model = ChequeRecibo
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorChequesFechaForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	# model_string = model.__name__.lower()
	model_string = "chequesfecha"
	
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
		"id_factura__id_caja__numero_caja": {
			"label": "Caja",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_factura__id_caja__fecha_caja": {
			"label": "Fecha Caja",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_factura__id_caja__id_user__iniciales": {
			"label": "Usuario",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"comprobante_completo": {
			"label": "Comprobante",
			"col_width_pdf": 60,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"codigo_banco": {
			"label": "Cód. Bco.",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
		},
		"id_banco__nombre_banco": {
			"label": "Nombre Banco",
			"col_width_pdf": 220,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"sucursal": {
			"label": "Suc.",
			"col_width_pdf": 30,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"codigo_postal": {
			"label": "C. P.",
			"col_width_pdf": 30,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"fecha_cheque1": {
			"label": "Fecha",
			"col_width_pdf": 50,
			"pdf_paragraph": False,
			"date_format": '%d/%m/%Y',
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"numero_cheque_recibo": {
			"label": "Número",
			"col_width_pdf": 60,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"importe_cheque": {
			"label": "Importe",
			"col_width_pdf": 60,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"electronico": {
			"label": "Electrónico",
			"col_width_pdf": 30,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True
		},
	}


class ChequesFechaInformeView(InformeFormView):
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
		
		queryset = ChequeRecibo.objects.select_related(
			'id_factura_id_caja',
			'id_factura__id_comprobante_venta',
			'id_banco',
			'id_factura__id_caja__id_user'
		).filter(
			id_factura__id_caja__fecha_caja__range=(fecha_desde, fecha_hasta)
		).exclude(
			id_factura__id_comprobante_venta__mult_caja=0
		)
		
		#-- Aplicar filtros opcionales.
		if sucursal:
			queryset = queryset.filter(
				id_factura__id_sucursal=sucursal
			)
		
		queryset = queryset.annotate(
			#-- Convertir número a texto con ceros.
			numero_texto=LPad(
				Cast(F('id_factura__numero_comprobante'), CharField()),
				12,
				Value('0')
			)
		).annotate(
			#-- Crear el formato final.
			comprobante_completo=Concat(
				F('id_factura__id_comprobante_venta__codigo_comprobante_venta'),
				Value('  '),
				Substr(F('numero_texto'), 1, 4),
				Value('-'),
				Substr(F('numero_texto'), 5, 8)
			)
		).values(
			'id_factura__id_caja__numero_caja',
			'id_factura__id_caja__fecha_caja',
			'codigo_banco',
			'id_banco__nombre_banco',
			'sucursal',
			'codigo_postal',
			'numero_cheque_recibo',
			'fecha_cheque1',
			'importe_cheque',
			'comprobante_completo',
			'electronico',
			'id_factura__id_caja__id_user__iniciales'
		).order_by(
			'id_factura__id_caja__fecha_caja',
			'id_factura__id_caja__numero_caja',
			'electronico',
			'comprobante_completo'
		)
		
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
			"Fecha Desde": fecha_desde.strftime("%d/%m/%Y") if fecha_desde else "N/A",
			"Fecha Hasta": fecha_hasta.strftime("%d/%m/%Y") if fecha_hasta else "N/A",
		}
		
		# **************************************************
		
		datos_estructurados = {}
		total_general = 0.0
		
		for registro in queryset:
			numero_caja = registro['id_factura__id_caja__numero_caja']
			fecha_caja = registro['id_factura__id_caja__fecha_caja']
			operador_caja = registro['id_factura__id_caja__id_user__iniciales']
			
			if numero_caja not in datos_estructurados:
				datos_estructurados[numero_caja] = {
					'fecha_caja': fecha_caja,
					'operador_caja': operador_caja,
					'subtotal_caja': 0.0,
					'electronico': {
						'cheques': [],
						'subtotal_cheque': 0.0
					},
					'fisico': {
						'cheques': [],
						'subtotal_cheque': 0.0
					}
				}
				
			#-- Determinar el tipo de cheque.
			es_electro = registro['electronico'] == True
			tipo_cheque = 'electronico' if es_electro else 'fisico'
			
			importe_cheque = float(registro['importe_cheque'] or 0.0)
			datos_estructurados[numero_caja][tipo_cheque]['cheques'].append(registro)
			datos_estructurados[numero_caja][tipo_cheque]['subtotal_cheque'] += importe_cheque
			datos_estructurados[numero_caja]['subtotal_caja'] += importe_cheque
			total_general += importe_cheque
		
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


def chequesfecha_vista_pantalla(request):
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


def chequesfecha_vista_pdf(request):
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
		('ALIGN', (2,0), (2,-1), 'RIGHT'),
		('ALIGN', (4,0), (5,-1), 'RIGHT'),
		('ALIGN', (7,0), (8,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	objetos = contexto_reporte.get("objetos", {})
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	for caja, datos_caja in objetos.items():
		#-- Fila de agrupación por Caja.
		caja_formateada = f"{caja.zfill(8)[:2]}-{caja.zfill(8)[2:]}"
		table_data.append([
			f"CAJA : {caja_formateada}  [{format_date(datos_caja['fecha_caja'])}]  [{datos_caja['operador_caja']}]",
			"", "", "", "", "", "", "", ""
		])
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		
		#-- Datos agrupado por tipo de cheque (electrónico/Físico).
		if datos_caja.get('fisico', {}).get('cheques'):
			table_data.append([
				"",
				"Cheques Físicos",
				"", "", "", "", "", "", ""
			])
			
			#-- Aplicar estilos a la fila de agrupación (fila actual).
			table_style_config.extend([
				('SPAN', (1,current_row), (-1,current_row)),
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
			])
			
			current_row += 1
		
			#-- Agregar filas del detalle.
			for cheque in datos_caja['fisico']['cheques']:
				table_data.append([
					'',
					cheque['comprobante_completo'],
					cheque['codigo_banco'],
					Paragraph(str(cheque['id_banco__nombre_banco']), generator.styles['CellStyle']) if cheque['id_banco__nombre_banco'] else '',
					cheque['sucursal'],
					cheque['codigo_postal'],
					format_date(cheque['fecha_cheque1']),
					cheque['numero_cheque_recibo'],
					formato_argentino(cheque['importe_cheque']),
				])
				current_row += 1
			
			#-- Fila Total por tipo de cheque.
			table_data.append(["", "", "", "", "", "", "", f"Total Cheques Físicos:", formato_argentino(datos_caja['fisico']['subtotal_cheque'])])
			
			#-- Aplicar estilos a la fila de total (fila actual).
			table_style_config.extend([
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
				# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
			])
			
			current_row += 1
		
		if datos_caja.get('electronico', {}).get('cheques'):
			table_data.append([
				"",
				"Cheques Electrónicos",
				"", "", "", "", "", "", ""
			])
			
			#-- Aplicar estilos a la fila de agrupación (fila actual).
			table_style_config.extend([
				('SPAN', (1,current_row), (-1,current_row)),
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
			])
			
			current_row += 1
		
			#-- Agregar filas del detalle.
			for cheque in datos_caja['electronico']['cheques']:
				table_data.append([
					'',
					cheque['comprobante_completo'],
					cheque['codigo_banco'],
					Paragraph(str(cheque['id_banco__nombre_banco']), generator.styles['CellStyle']) if cheque['id_banco__nombre_banco'] else '',
					cheque['sucursal'],
					cheque['codigo_postal'],
					format_date(cheque['fecha_cheque1']),
					cheque['numero_cheque_recibo'],
					formato_argentino(cheque['importe_cheque']),
				])
				current_row += 1
			
			#-- Fila Total por tipo de cheque.
			table_data.append(["", "", "", "", "", "", "", f"Total Cheques Electrónicos:", formato_argentino(datos_caja['electronico']['subtotal_cheque'])])
			
			#-- Aplicar estilos a la fila de total (fila actual).
			table_style_config.extend([
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
				# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
			])
			
			current_row += 1
		
		#-- Total por Caja.
		table_data.append(["", "", "", "", "", "", "", f"Total Caja {caja_formateada}:", formato_argentino(datos_caja['subtotal_caja'])])
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
		])
		current_row += 1
		
		#-- Fila divisoria.
		table_data.append(["", "", "", "", "", "", "", "", ""])
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
	
	#-- Fila Total General.
	table_data.append(["", "", "", "", "", "", "", "Total General:", formato_argentino(contexto_reporte.get('total_general'))])
	
	#-- Aplicar estilos a la fila de total (fila actual).
	table_style_config.extend([
		('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
		# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
	])
	
	return generator.generate(table_data, col_widths, table_style_config)		


def chequesfecha_vista_excel(request):
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
	view_instance = ChequesFechaInformeView()
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


def chequesfecha_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = ChequesFechaInformeView()
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

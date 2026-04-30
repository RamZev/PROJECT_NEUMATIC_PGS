# neumatic\apps\informes\views\vlventacompro_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from decimal import Decimal
from django.templatetags.static import static
from collections import defaultdict

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLVentaCompro
from ..forms.buscador_vlventacompro_forms import BuscadorVentaComproForm
from utils.utils import deserializar_datos, formato_argentino, format_date, normalizar
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Ventas por Comprobantes"
	
	#-- Modelo.
	model = VLVentaCompro
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorVentaComproForm
	
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
		"comprobante": {
			"label": "Comprobante",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"fecha_comprobante": {
			"label": "Fecha",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"condicion": {
			"label": "Condición",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
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
		"contado": {
			"label": "Contado",
			"col_width_pdf": 70,
			"pdf": True,
			"excel": False,
			"csv": False
		},
		"cta_cte": {
			"label": "Cta. Cte.",
			"col_width_pdf": 70,
			"pdf": True,
			"excel": False,
			"csv": False
		},
		"gravado": {
			"label": "Gravado",
			"col_width_pdf": 40,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"iva": {
			"label": "IVA",
			"col_width_pdf": 40,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"percep_ib": {
			"label": "Percep. IB",
			"col_width_pdf": 40,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"total": {
			"label": "Total",
			"col_width_pdf": 70,
			"pdf": False,
			"excel": True,
			"csv": True
		},
	}


class VLVentaComproInformeView(InformeFormView):
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
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		sucursal = cleaned_data.get("sucursal")
		
		return VLVentaCompro.objects.obtener_venta_compro(fecha_desde, fecha_hasta, sucursal)
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		solo_totales_comprobante = cleaned_data.get("solo_totales_comprobante", False)
		sucursal = cleaned_data.get('sucursal', None)
		
		param_left = {
			"Sucursal": f"[{sucursal.id_sucursal}] {sucursal.nombre_sucursal}" if sucursal else "Todas",
		}
		param_right = {
			"Desde": fecha_desde.strftime("%d/%m/%Y"),
			"Hasta": fecha_hasta.strftime("%d/%m/%Y"),
		}
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")		
		
		#-- Agrupar y estructurar datos del queryset.
		datos_agrupados = []
		totales_generales = {"contado": Decimal(0), "cta_cte": Decimal(0)}
		agrupados = defaultdict(lambda: {
			"comprobantes": [],
			"subtotal": {
				"contado": {"gravado": Decimal(0), "iva": Decimal(0), "percep_ib": Decimal(0), "total": Decimal(0)},
				"cta_cte": {"gravado": Decimal(0), "iva": Decimal(0), "percep_ib": Decimal(0), "total": Decimal(0)},
			},
		})
		
		for item in queryset:
			tipo = item.nombre_comprobante_venta
			condicion = "contado" if item.condicion == "Contado" else "cta_cte"
			monto_total = Decimal(item.total)
			
			agrupados[tipo]["comprobantes"].append({
				"comprobante": item.comprobante,
				"fecha": item.fecha_comprobante,
				"condicion": item.condicion,
				"cliente_id": item.id_cliente_id,
				"cliente_nombre": item.nombre_cliente,
				"gravado": Decimal(item.gravado),
				"iva": Decimal(item.iva),
				"percep_ib": Decimal(item.percep_ib),
				"total": monto_total,
			})
			
			agrupados[tipo]["subtotal"][condicion]["gravado"] += Decimal(item.gravado)
			agrupados[tipo]["subtotal"][condicion]["iva"] += Decimal(item.iva)
			agrupados[tipo]["subtotal"][condicion]["percep_ib"] += Decimal(item.percep_ib)
			agrupados[tipo]["subtotal"][condicion]["total"] += monto_total
			totales_generales[condicion] += monto_total
		
		for tipo, datos in agrupados.items():
			datos_agrupados.append({"tipo": tipo, **datos})
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": datos_agrupados,
			"total_general": totales_generales,
			"solo_totales_comprobante": solo_totales_comprobante,
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


def vlventacompro_vista_pantalla(request):
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


def vlventacompro_vista_pdf(request):
	#-- Obtener el token de la querystring.
	token = request.GET.get("token")
	
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Obtener el contexto(datos) previamente guardados en la sesión.
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
		('ALIGN', (3,0), (3,-1), 'RIGHT'),
		('ALIGN', (5,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	for obj in contexto_reporte.get("objetos", []):
		#-- Datos agrupado por.
		table_data.append([
			obj['tipo'],
			"", "", "", "", "", ""
		])
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		
		#-- Agregar filas del detalle.
		for compro in obj['comprobantes']:
			table_data.append([
				compro['comprobante'],
				format_date(compro['fecha']),
				compro['condicion'],
				compro['cliente_id'],
				Paragraph(str(compro['cliente_nombre']), generator.styles['CellStyle']),
				formato_argentino(compro['total']) if compro['condicion'] == 'Contado' else formato_argentino(Decimal(0)),
				formato_argentino(compro['total']) if compro['condicion'] == 'Cta. Cte.' else formato_argentino(Decimal(0)),
			])
			current_row += 1
			
		#-- Fila Sub Total 1 por comprobante.
		table_data.append(
			[
				"", "", "", "", "Sub Total:", 
				formato_argentino(obj['subtotal']['contado']['total']),
				formato_argentino(obj['subtotal']['cta_cte']['total'])
			]
		)
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (4,current_row), (-1,current_row), 'RIGHT'),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			('LINEABOVE', (5,current_row), (-1,current_row), 0.5, colors.black),
		])
		
		current_row += 1
		
		#-- Fila Sub Total 2 por comprobante.
		table_data.append(
			[
				"", "", "", "", "Gravado:", 
				formato_argentino(obj['subtotal']['contado']['gravado']),
				formato_argentino(obj['subtotal']['cta_cte']['gravado'])
			]
		)
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (4,current_row), (-1,current_row), 'RIGHT'),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
		])
		
		current_row += 1
		
		#-- Fila Sub Total 3 por comprobante.
		table_data.append(
			[
				"", "", "", "", "I.V.A.:", 
				formato_argentino(obj['subtotal']['contado']['iva']),
				formato_argentino(obj['subtotal']['cta_cte']['iva'])
			]
		)
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (4,current_row), (-1,current_row), 'RIGHT'),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
		])
		
		current_row += 1
		
		#-- Fila Sub Total 4 por comprobante.
		table_data.append(
			[
				"", "", "", "", "Percepción IB:", 
				formato_argentino(obj['subtotal']['contado']['percep_ib']),
				formato_argentino(obj['subtotal']['cta_cte']['percep_ib'])
			]
		)
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (4,current_row), (-1,current_row), 'RIGHT'),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
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
	table_data.append(
		["", "", "", "", "Total General:", 
			formato_argentino(contexto_reporte['total_general']['contado']),
			formato_argentino(contexto_reporte['total_general']['cta_cte'])
		]
	)
	
	#-- Aplicar estilos a la fila de total (fila actual).
	table_style_config.extend([
		('ALIGN', (4,current_row), (-1,current_row), 'RIGHT'),
		('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
		# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
	])
	
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlventacompro_vista_excel(request):
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
	view_instance = VLVentaComproInformeView()
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


def vlventacompro_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLVentaComproInformeView()
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

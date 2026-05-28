# neumatic\apps\informes\views\vlresumenctactevendedor_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLResumenCtaCte
from ..forms.buscador_vlresumenctactevendedor_forms import BuscadorResumenCtaCteVendedorForm
from utils.utils import deserializar_datos, formato_argentino, format_date, normalizar
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Resumen de Cuenta Corriente"
	
	#-- Modelo.
	model = VLResumenCtaCte
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorResumenCtaCteVendedorForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	# model_string = model.__name__.lower()
	model_string = 'vlresumenctactevendedor'
	
	# Vistas del CRUD del modelo
	list_view_name = f"{model_string}_list"  # <== vlventacompro_list
	
	#-- Plantilla base.
	template_list = f'{app_label}/maestro_informe.html'
	
	#-- Vista del home del proyecto.
	home_view_name = "home"
	
	#-- Archivo JavaScript específico.
	js_file = "js/filtros_resumen_cta_cte.js"
	
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
			"label": "ID Cliente",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"razon_social": {
			"label": "Razón Social",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_comprobante_venta": {
			"label": "Comprobante",
			"col_width_pdf": 100,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"numero": {
			"label": "Número",
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
		"remito": {
			"label": "Remito",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"condicion": {
			"label": "Cond. Venta",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"debe": {
			"label": "Debe",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"haber": {
			"label": "Haber",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"saldo_acumulado": {
			"label": "Saldo",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"marca": {
			"label": "Marca",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"no_estadist": {
			"label": "No Estadíst.",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
			"id_vendedor_id": {
			"label": "ID Vendedor",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_vendedor": {
			"label": "Nombre Vendedor",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		}
	}


class VLResumenCtaCteVendedorInformeView(InformeFormView):
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
		resumen_pendiente = cleaned_data.get('resumen_pendiente')
		condicion_venta = cleaned_data.get('condicion_venta')
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		vendedor = cleaned_data.get('vendedor', None)
		
		if resumen_pendiente:
			queryset, total_general = VLResumenCtaCte.objects.obtener_fact_pendientes_vendedor(vendedor.id_vendedor)
		else:
			if condicion_venta == "0":
				queryset, total_general = VLResumenCtaCte.objects.obtener_resumen_cta_cte_vendedor(vendedor.id_vendedor, fecha_desde, fecha_hasta, 1, 2)
			else:
				queryset, total_general = VLResumenCtaCte.objects.obtener_resumen_cta_cte_vendedor(vendedor.id_vendedor, fecha_desde, fecha_hasta, condicion_venta, condicion_venta)
			
		#-- Guardar el total general como atributo de la instancia para su uso posterior.
		self.total_general = total_general
		
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		resumen_pendiente = cleaned_data.get('resumen_pendiente', None)
		condicion_venta = cleaned_data.get('condicion_venta', None)
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		vendedor = cleaned_data.get('vendedor', None)
		observaciones = cleaned_data.get("observaciones", None)
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")		
		
		param_left = {
			"Vendedor": f"[{vendedor.id_vendedor}] {vendedor.nombre_vendedor}" if vendedor else None
		}
		param_right = {
		}
		if resumen_pendiente:
			#-- Reporte Resumen de Cuenta Pendiente.
			
			#-- Plantilla Vista Preliminar Pantalla.
			ConfigViews.reporte_pantalla = 'informes/reportes/vlfacturas_pendientes_vendedor_list.html'
			
			param_left["Tipo Reporte"] = "Resumen de Cuenta Pendiente"
		else:
			#-- Reporte Resumen de Cuenta Corriente.
			
			#-- Plantilla Vista Preliminar Pantalla.
			ConfigViews.reporte_pantalla = 'informes/reportes/vlresumenctactevendedor_list.html'
			
			cond_vta = {
				"0": "Ambos",
				"1": "Contado",
				"2": "Cta. Cte.",
			}
			param_left["Condición"] = cond_vta[condicion_venta]
			
			param_right["Desde"] = fecha_desde.strftime("%d/%m/%Y")
			param_right["Hasta"] = fecha_hasta.strftime("%d/%m/%Y")
			
		#------------------------------------------------------------------------------
		grouped_data = {}
		
		for obj in queryset:
			#-- Agrupar por Cliente.
			cliente = obj.razon_social
			if cliente not in grouped_data:
				grouped_data[cliente] = {
					'cliente_id': obj.id_cliente_id,
					'datos': [],
				}
			
			#-- Serializar cada objeto en un diccionario plano.
			obj_serializado = {
				'nombre_comprobante_venta': obj.nombre_comprobante_venta,
				'numero_comprobante': obj.numero_comprobante,
				'numero': obj.numero,
				'fecha_comprobante': obj.fecha_comprobante,
				'remito': obj.remito,
				'condicion_comprobante': obj.condicion_comprobante,
				'condicion': obj.condicion,
				'total': float(obj.total),
				'entrega': float(obj.entrega),
				'debe': float(obj.debe),
				'haber': float(obj.haber),
				'saldo_acumulado': float(obj.saldo_acumulado),
				'intereses': float(obj.intereses),
				'marca': obj.marca,
				'no_estadist': obj.no_estadist,
				'saldo_anterior': float(obj.saldo_anterior),
			}
			
			#-- Añadir el detalle al grupo.
			grouped_data[cliente]["datos"].append(obj_serializado)
			
			#-- Acumular el total por cliente usando el saldo acumulado del último registro de cada cliente.
			grouped_data[cliente]["total_cliente"] = float(obj.saldo_acumulado)
		
		#-- Usar el total_general guardado.
		total_general = getattr(self, 'total_general', float('0.00'))
		
		# ------------------------------------------------------------------------------
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": grouped_data,
			'intereses_total': 0.0,
			'total_general': float(total_general),
			'observaciones': observaciones,
			"parametros_i": param_left,
			"parametros_d": param_right,
			"resumen_pendiente": resumen_pendiente,
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


def vlresumenctactevendedor_vista_pantalla(request):
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


def vlresumenctactevendedor_vista_pdf(request):
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
	resumen_pendiente = contexto_reporte.get('resumen_pendiente', None)
	
	#-- Crear instancia del generador personalizado.
	generator = CustomPDFGenerator(contexto_reporte, pagesize=portrait(A4), body_font_size=7)
	
	#-- Construir datos de la tabla:
	headers = [
		("", 10),
		("Comprobante", 100),
		("Número", 65),
		("Fecha", 45),
		("Remito", 60)
	]
	
	if resumen_pendiente:
		headers.extend([
			("Total Comp.", 70),
			("Entrega", 70),
			("Saldo", 70),
			("Intereses",70),
			("",5),
			("",5),
		])
		#-- Estilos específicos adicionales iniciales de la tabla.
		table_style_config = [
			('ALIGN', (5,0), (-1,-1), 'RIGHT'),
		]
	else:
		headers.extend([
			("Cond. Venta", 40),
			("Debe", 70),
			("Haber", 70),
			("Saldo", 70),
			("",5),
			("",5),
		])
		#-- Estilos específicos adicionales iniciales de la tabla.
		table_style_config = [
			('ALIGN', (6,0), (-1,-1), 'RIGHT'),
		]
	
	#-- Extraer Títulos de las columnas de la tabla (headers).
	headers_titles = [value[0] for value in headers]
	
	#-- Extraer Ancho de las columnas de la tabla.
	col_widths = [value[1] for value in headers]
	
	table_data = [headers_titles]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	
	for cliente, cliente_data in contexto_reporte.get("objetos", {}).items():
		
		#-- Datos agrupado por Cliente.
		table_data.append([f"Cliente: [{cliente_data['cliente_id']}] {cliente}", "", "", "", "", "", "", "", "", "", ""])
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
	
		if resumen_pendiente:
			
			#-- Agregar filas del detalle.
			for dato in cliente_data['datos']:
				table_data.append([
					'',
					dato['nombre_comprobante_venta'],
					dato['numero'],
					format_date(dato['fecha_comprobante']),
					dato['remito'],
					formato_argentino(dato['total']),
					formato_argentino(dato['entrega']),
					formato_argentino(dato['saldo_acumulado']),
					formato_argentino(dato['intereses']),
					dato['marca'],
					dato['no_estadist']
				])
				
				current_row += 1
			
		else:
			#-- Agregar Saldo Anterior.
			table_data.append([
				"", "", "", "", "", "", "", 
				"Saldo Anterior:",
				formato_argentino(cliente_data['datos'][0]['saldo_anterior']),
				"",	""
			])
			
			#-- Aplicar estilos a la fila de agrupación (fila actual).
			table_style_config.extend([
				# ('SPAN', (0,current_row), (-1,current_row)),
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
			])
			
			current_row += 1
			
			#-- Agregar filas del detalle.
			for dato in cliente_data['datos']:
				table_data.append([
					'',
					dato['nombre_comprobante_venta'],
					dato['numero'],
					format_date(dato['fecha_comprobante']),
					dato['remito'],
					dato['condicion'],
					formato_argentino(dato['debe']),
					formato_argentino(dato['haber']),
					formato_argentino(dato['saldo_acumulado']),
					dato['marca'],
					dato['no_estadist']
				])
				
				current_row += 1
		
		#-- Fila Total Intereses.
		table_data.append(
			[
				"", "", "", "", "", "", "",
				"Total Intereses:", 
				formato_argentino(contexto_reporte['intereses_total']),
				"",
				""
			]
		)
		
		#-- Aplicar estilos a la fila actual.
		table_style_config.extend([
			('ALIGN', (5,-current_row), (-1,current_row), 'RIGHT'),
			('FONTNAME', (5,current_row), (-1,current_row), 'Helvetica-Bold'),
			# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
			# ('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.black),
		])
		
		current_row += 1
	
		#-- Fila Total Cliente.
		table_data.append(
			[
				"", "", "", "", "", "", "",
				f"Total Cliente: {cliente}:", 
				formato_argentino(cliente_data['total_cliente']),
				"",
				""
			]
		)
		
		#-- Aplicar estilos a la fila actual.
		table_style_config.extend([
			('ALIGN', (5,-current_row), (-1,current_row), 'RIGHT'),
			('FONTNAME', (5,current_row), (-1,current_row), 'Helvetica-Bold'),
			# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.black),
		])
		
		current_row += 1
	
	#-- Fila Total General.
	table_data.append(
		[
			"", "", "", "", "", "", "", 
			"Total General:", 
			formato_argentino(contexto_reporte['total_general']),
			"",
			""
		]
	)
	
	#-- Aplicar estilos a la fila actual.
	table_style_config.extend([
		('ALIGN', (5,current_row), (-1,current_row), 'RIGHT'),
		('FONTNAME', (5,current_row), (-1,current_row), 'Helvetica-Bold'),
		# ('LINEABOVE', (0,-2), (-1,-2), 0.5, colors.black),
	])
	
	current_row += 1
	
	#-- Fila divisoria.
	table_data.append(["", "", "", "", "", "", "", "", "", "", ""])
	
	current_row += 1
	
	#-- Observaciones (Título).
	table_data.append(["Observaciones:", "", "", "", "", "", "", "", "", "", ""])
	
	#-- Aplicar estilos a la fila actual.
	table_style_config.extend([
		('SPAN', (0,current_row), (-1,current_row)),
		('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
	])
	
	current_row += 1
	
	#-- Observaciones (Contenido).
	table_data.append([Paragraph(str(contexto_reporte['observaciones']), generator.styles['CellStyle']), "", "", "", "", "", "", "", "", "", ""])
	
	#-- Aplicar estilos a la fila actual.
	table_style_config.extend([
		('SPAN', (0,current_row), (-1,current_row)),
		# ('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
	])
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlresumenctactevendedor_vista_excel(request):
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
	view_instance = VLResumenCtaCteVendedorInformeView()
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


def vlresumenctactevendedor_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLResumenCtaCteVendedorInformeView()
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

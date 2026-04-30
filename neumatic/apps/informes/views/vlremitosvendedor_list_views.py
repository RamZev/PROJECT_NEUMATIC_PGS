# neumatic\apps\informes\views\vlremitosvendedor_list_views.py

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
from apps.informes.models import VLRemitosVendedor
from ..forms.buscador_vlremitosvendedor_forms import BuscadorRemitosVendedorForm
from utils.utils import deserializar_datos, formato_argentino, format_date, normalizar
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Remitos por Vendedor"
	
	#-- Modelo.
	model = VLRemitosVendedor
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorRemitosVendedorForm
	
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
		"id_cliente_id": {
			"label": "Cliente",
			"col_width_pdf": 30,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_cliente": {
			"label": "Nombre",
			"col_width_pdf": 180,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"fecha_comprobante": {
			"label": "Fecha",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"comprobante": {
			"label": "Comprobante",
			"col_width_pdf": 70,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"nombre_producto": {
			"label": "Descripción",
			"col_width_pdf": 200,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"medida": {
			"label": "Medida",
			"col_width_pdf": 50,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"cantidad": {
			"label": "Cantidad",
			"col_width_pdf": 60,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"precio": {
			"label": "Precio",
			"col_width_pdf": 70,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"total": {
			"label": "Total",
			"col_width_pdf": 70,
			"pdf": True,
			"excel": True,
			"csv": True
		},
	}


class VLRemitosVendedorInformeView(InformeFormView):
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
		vendedor = cleaned_data.get("vendedor", None)
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		
		return VLRemitosVendedor.objects.obtener_remitos_vendedor(vendedor.id_vendedor, fecha_desde, fecha_hasta)
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando, calculando subtotales y totales generales, etc,
		tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		vendedor = cleaned_data.get("vendedor")
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		
		param_left = {
			"Vendedor": f"[{vendedor.id_vendedor}] {vendedor.nombre_vendedor}" if vendedor else "Todos",
		}
		param_right = {
			"Desde": fecha_desde.strftime("%d/%m/%Y"),
			"Hasta": fecha_hasta.strftime("%d/%m/%Y"),
		}
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		# **************************************************
		#-- Estructura para agrupar datos por cliente.
		datos_por_cliente = {}
		total_general = Decimal(0)
		
		for obj in queryset:
			#-- Identificar al cliente.
			cliente_id = obj.id_cliente_id
			nombre_cliente = obj.nombre_cliente.strip()  #-- Limpieza en caso de espacios extras.
			
			#-- Si el cliente aún no está en el diccionario, se inicializa.
			if cliente_id not in datos_por_cliente:
				datos_por_cliente[cliente_id] = {
					"id_cliente": cliente_id,
					"cliente": nombre_cliente,
					"comprobantes": {},
					"total_cliente": Decimal(0),
				}
			
			#-- Agrupar por comprobante dentro del cliente.
			num_comprobante = obj.numero_comprobante
			if num_comprobante not in datos_por_cliente[cliente_id]["comprobantes"]:
				datos_por_cliente[cliente_id]["comprobantes"][num_comprobante] = {
					"fecha": obj.fecha_comprobante.strftime("%d/%m/%Y"),
					"fecha_order": obj.fecha_comprobante,    # Para ordenar por fecha
					"numero_comprobante": num_comprobante,   # Para ordenar por número
					"comprobante": obj.comprobante,
					"productos": [],
					"total_comprobante": Decimal(0),
				}
			
			#-- Crear el diccionario con los datos requeridos para el reporte.
			producto_data = {
				"fecha": obj.fecha_comprobante.strftime("%d/%m/%Y"),
				"comprobante": obj.comprobante,
				"descripcion": obj.nombre_producto,
				"medida": obj.medida,
				"cantidad": obj.cantidad,
				"precio": obj.precio,
				"total": obj.total,
			}
			
			#-- Agregar el producto a la lista del comprobante y acumular totales.
			datos_por_cliente[cliente_id]["comprobantes"][num_comprobante]["productos"].append(producto_data)
			datos_por_cliente[cliente_id]["comprobantes"][num_comprobante]["total_comprobante"] += obj.total
			datos_por_cliente[cliente_id]["total_cliente"] += obj.total
			total_general += obj.total
		
		#-- Convertir la estructura de diccionarios a listas ordenadas para iterar en el template.
		datos = []
		for cliente_info in datos_por_cliente.values():
			#-- Convertir comprobantes (diccionario) a lista y ordenarlos por (fecha, número de comprobante).
			comprobantes_list = list(cliente_info["comprobantes"].values())
			comprobantes_list.sort(key=lambda x: (x["fecha_order"], x["numero_comprobante"]))
			cliente_info["comprobantes"] = comprobantes_list
			
			datos.append(cliente_info)
		
		#-- Ordenar la lista de datos por el nombre del cliente.
		datos.sort(key=lambda x: x["cliente"])
		# **************************************************
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": datos,
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


def vlremitosvendedor_vista_pantalla(request):
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


def vlremitosvendedor_vista_pdf(request):
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
		('ALIGN', (4,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	
	for obj in contexto_reporte.get("objetos", []):
		#-- Datos agrupado por.
		table_data.append([
			f"Cliente: [{obj['id_cliente']}] {obj['cliente']}",
			"", "", "", "", "", ""
		])
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		
		#-- Agregar filas del detalle.
		for comprobante in obj['comprobantes']:
			for producto in comprobante['productos']:
				table_data.append([
					format_date(producto['fecha']),
					producto['comprobante'],
					Paragraph(str(producto['descripcion']), generator.styles['CellStyle']),
					producto['medida'],
					formato_argentino(producto['cantidad']),
					formato_argentino(producto['precio']),
					formato_argentino(producto['total'])
				])
				current_row += 1
			
			#-- Fila Total por comprobante.
			table_data.append(["", "", "", "", "", "Total Comprobante:", formato_argentino(comprobante['total_comprobante'])])
			
			#-- Aplicar estilos a la fila de total (fila actual).
			table_style_config.extend([
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
				# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
			])
			
			current_row += 1
		
		#-- Fila Total por Cliente.
		table_data.append(["", "", "", "", "", "Total Cliente:", formato_argentino(obj['total_cliente'])])
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
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
	table_data.append(["", "", "", "", "", "Total General:", formato_argentino(contexto_reporte.get('total_general'))])
	
	#-- Aplicar estilos a la fila de total (fila actual).
	table_style_config.extend([
		('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
		# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
	])
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlremitosvendedor_vista_excel(request):
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
	view_instance = VLRemitosVendedorInformeView()
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


def vlremitosvendedor_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLRemitosVendedorInformeView()
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

# neumatic\apps\informes\views\vlmercaderiaporcliente_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static
from django.forms.models import model_to_dict

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLMercaderiaPorCliente
from apps.maestros.models.cliente_models import Cliente
from ..forms.buscador_vlmercaderiaporcliente_forms import BuscadorMercaderiaPorClienteForm
from utils.utils import deserializar_datos, formato_argentino, normalizar
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Mercadería por Cliente"
	
	#-- Modelo.
	model = VLMercaderiaPorCliente
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorMercaderiaPorClienteForm
	
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
		"nombre_comprobante_venta": {
			"label": "Comprobante",
			"col_width_pdf": 40,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"numero": {
			"label": "Número",
			"col_width_pdf": 40,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"fecha_comprobante": {
			"label": "Fecha",
			"col_width_pdf": 40,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_producto_marca": {
			"label": "Marca",
			"col_width_pdf": 140,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"medida": {
			"label": "Medida",
			"col_width_pdf": 60,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_producto_id": {
			"label": "Código",
			"col_width_pdf": 40,
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
		"cantidad": {
			"label": "Cantidad",
			"col_width_pdf": 60,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"precio": {
			"label": "Precio",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"descuento": {
			"label": "Desc.",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"total": {
			"label": "Total",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
	}


class VLMercaderiaPorClienteInformeView(InformeFormView):
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
		id_cliente = cleaned_data.get('id_cliente', None)
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		
		queryset = VLMercaderiaPorCliente.objects.obtener_mercaderia_por_cliente(id_cliente, fecha_desde, fecha_hasta)
		
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		id_cliente = cleaned_data.get('id_cliente', None)
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		
		cliente = Cliente.objects.filter(pk=id_cliente).first() if id_cliente else None
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")		
		
		param_left = {
			"Cliente": f"[{cliente.id_cliente}] {cliente}" if cliente else ""
		}
		param_right = {
			"Desde": fecha_desde.strftime("%d/%m/%Y"),
			"Hasta": fecha_hasta.strftime("%d/%m/%Y"),
		}
		
		# ------------------------------------------------------------------------------
		#-- Agrupar los objetos por el número de comprobante.
		grouped_data = {}
		for obj in queryset:
			comprobante_num = obj.numero_comprobante  # Este es el campo que agrupa los datos
			if comprobante_num not in grouped_data:
				grouped_data[comprobante_num] = []
			grouped_data[comprobante_num].append(obj)
		
		#-- Convertir cada objeto del queryset a un diccionario.
		for comprobante_num, productos in grouped_data.items():
			grouped_data[comprobante_num] = [model_to_dict(producto) for producto in productos]
		
		# ------------------------------------------------------------------------------
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": grouped_data,
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
		if form.errors:
			context["data_has_errors"] = True
		return context


def vlmercaderiaporcliente_vista_pantalla(request):
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


def vlmercaderiaporcliente_vista_pdf(request):
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
	
	#-- Construir datos de la tabla:
	
	#-- Extraer Títulos de las columnas de la tabla (headers).
	headers_titles = [value['label'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	#-- Extraer Ancho de las columnas de la tabla.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (4,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	
	for comprobante_num, productos in contexto_reporte.get("objetos", {}).items():
		#-- Datos agrupado por.
		primer_producto = productos[0]
		table_data.append([
			f"{primer_producto['nombre_comprobante_venta']}  {primer_producto['numero']}  {primer_producto['fecha_comprobante'].strftime('%d/%m/%Y')}",
			"", "", "", "", "", ""
		])
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		
		#-- Agregar filas del detalle.
		for producto in productos:
			table_data.append([
				Paragraph(str(producto.get('nombre_producto_marca', '')), generator.styles['CellStyle']),
				producto.get('medida', ''),
				producto.get('id_producto_id', ''),
				Paragraph(str(producto.get('nombre_producto', '')), generator.styles['CellStyle']),
				formato_argentino(producto.get('cantidad', 0)),
				formato_argentino(producto.get('precio', 0)),
				formato_argentino(producto.get('descuento', 0)),
				formato_argentino(producto.get('total', 0))
			])
			current_row += 1
			
		#-- Fila divisoria.
		table_data.append(["", "", "", "", "", "", ""])
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlmercaderiaporcliente_vista_excel(request):
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
	view_instance = VLMercaderiaPorClienteInformeView()
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
	# Inline permite visualizarlo en el navegador si el navegador lo soporta.
	response["Content-Disposition"] = f'inline; filename="{ConfigViews.report_title}.xlsx"'
	
	return response


def vlmercaderiaporcliente_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLMercaderiaPorClienteInformeView()
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

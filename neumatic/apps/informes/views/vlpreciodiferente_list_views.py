# neumatic\apps\informes\views\vlpreciodiferente_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLPrecioDiferente
from ..forms.buscador_vlpreciodiferente_forms import BuscadorPrecioDiferenteForm
from utils.utils import deserializar_datos, formato_argentino, normalizar
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Diferencias de Precios en Facturación"
	
	#-- Modelo.
	model = VLPrecioDiferente
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorPrecioDiferenteForm
	
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
		"id_vendedor_id": {
			"label": "Cód. Vendedor",
			"col_width_pdf": 30,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_vendedor": {
			"label": "Vendedor",
			"col_width_pdf": 80,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"comprobante": {
			"label": "Comprobante",
			"col_width_pdf": 80,
			"pdf": True,
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
		"id_cliente_id": {
			"label": "Cliente",
			"col_width_pdf": 30,
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
		"id_producto_id": {
			"label": "Código",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"nombre_producto": {
			"label": "Detalle",
			"col_width_pdf": 180,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"cantidad": {
			"label": "Cantidad",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"precio": {
			"label": "Facturado",
			"col_width_pdf": 60,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"precio_lista": {
			"label": "Lista",
			"col_width_pdf": 60,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"diferencia": {
			"label": "Diferencia",
			"col_width_pdf": 60,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"descuento": {
			"label": "Bonif.",
			"col_width_pdf": 40,
			"pdf": True,
			"excel": True,
			"csv": True
		},
	}


class VLPrecioDiferenteInformeView(InformeFormView):
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
		id_vendedor_desde = cleaned_data.get("id_vendedor_desde")
		id_vendedor_hasta = cleaned_data.get("id_vendedor_hasta")
		comprobantes = cleaned_data.get("comprobantes")
		dif_mayor = cleaned_data.get("operario") or 0
		orden = cleaned_data.get('orden')
		
		#-- Convertir a lista explícitamente.
		codigos_comprobantes = list(comprobantes.values_list('codigo_comprobante_venta', flat=True)) if comprobantes else []
		
		return VLPrecioDiferente.objects.obtener_datos(
			fecha_desde,
			fecha_hasta,
			id_vendedor_desde,
			id_vendedor_hasta,
			codigos_comprobantes,
			dif_mayor,
			orden
		)
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando, calculando subtotales y totales generales, etc,
		tal como se requiere para el listado. Si APLICA!
		"""
		
		#-- Parámetros del listado.
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		id_vendedor_desde = cleaned_data.get("id_vendedor_desde")
		id_vendedor_hasta = cleaned_data.get("id_vendedor_hasta")
		comprobantes = cleaned_data.get("comprobantes")
		dif_mayor = cleaned_data.get("dif_mayor") or 0
		orden = cleaned_data.get('orden')
		
		#-- Obtener los códigos de comprobantes.
		codigos_comprobantes = ", ".join(list(comprobantes.values_list('codigo_comprobante_venta', flat=True)) if comprobantes else [])
		
		param_left = {
			"Vendedor": f"Desde: {id_vendedor_desde} - Hasta: {id_vendedor_hasta}",
			"Ordenado por": "Nombre Vendedor" if orden == "nombre" else "Código Vendedor",
			"Comprobantes": codigos_comprobantes,
		}
		param_right = {
			"Desde": fecha_desde.strftime("%d/%m/%Y"),
			"Hasta": fecha_hasta.strftime("%d/%m/%Y"),
			"Diferencias Superiores a": formato_argentino(dif_mayor),
		}
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		# **************************************************
		#-- Estructura para agrupar datos por Vendedor.
		datos_por_vendedor = {}
		
		for obj in queryset:
			#-- Identificar al Vendedor.
			vendedor_id = obj.id_vendedor_id
			nombre_vendedor = obj.nombre_vendedor.strip()  #-- Limpieza en caso de espacios extras.
			
			#-- Si el Vendedor aún no está en el diccionario, se inicializa.
			if vendedor_id not in datos_por_vendedor:
				datos_por_vendedor[vendedor_id] = {
					"id_vendedor": vendedor_id,
					"vendedor": nombre_vendedor,
					"detalle": []
				}
			
			#-- Crear el diccionario con los datos del detalle del Vendedor.
			detalle_data = {
				"comprobante": obj.comprobante,
				"fecha": obj.fecha_comprobante.strftime("%d/%m/%Y"),
				"id_cliente_id": obj.id_cliente_id,
				"nombre_cliente": obj.nombre_cliente,
				"id_producto_id": obj.id_producto_id,
				"nombre_producto": obj.nombre_producto,
				"cantidad": obj.cantidad,
				"precio": obj.precio,
				"precio_lista": obj.precio_lista,
				"diferencia": obj.diferencia,
				"descuento": obj.descuento,
			}
			
			#-- Agregar el detalle a la lista de detalles.
			datos_por_vendedor[vendedor_id]["detalle"].append(detalle_data)
		
		#-- Convertir a lista los datos para iterar con más facilidad en la plantilla.
		datos_por_vendedor = list(datos_por_vendedor.values())
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": datos_por_vendedor,
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


def vlpreciodiferente_vista_pantalla(request):
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


def vlpreciodiferente_vista_pdf(request):
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
	
	#-- Extraer Títulos de las columnas de la tabla (headers).
	headers_titles = [value['label'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	#-- Extraer Ancho de las columnas de la tabla.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (2,0), (2,-1), 'RIGHT'),
		('ALIGN', (4,0), (4,-1), 'RIGHT'),
		('ALIGN', (6,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	for vendedor in contexto_reporte.get("objetos", []):
		#-- Datos agrupado por.
		table_data.append([
			f"Vendedor: [{vendedor['id_vendedor']}] {vendedor['vendedor']}",
			"", "", "", "", "", "", "", "", "", ""
		])
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		
		#-- Agregar filas del detalle.
		for det in vendedor['detalle']:
			table_data.append([
				det['comprobante'],
				det['fecha'],
				det['id_cliente_id'],
				Paragraph(str(det['nombre_cliente']), generator.styles['CellStyle']),
				det['id_producto_id'],
				Paragraph(str(det['nombre_producto']), generator.styles['CellStyle']),
				formato_argentino(det['cantidad']),
				formato_argentino(det['precio']),
				formato_argentino(det['precio_lista']),
				formato_argentino(det['diferencia']),
				f"{formato_argentino(det['descuento'])}%"
			])
			current_row += 1
		
		#-- Fila divisoria.
		table_data.append(["", "", "", "", "", "", "", "", "", "", ""])
		table_style_config.append(
			# ('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
			('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlpreciodiferente_vista_excel(request):
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
	view_instance = VLPrecioDiferenteInformeView()
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


def vlpreciodiferente_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLPrecioDiferenteInformeView()
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

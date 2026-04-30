# neumatic\apps\informes\views\vlestadisticasventasprovincia_list_views.py

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
from apps.informes.models import VLEstadisticasVentasProvincia
from apps.maestros.models.vendedor_models import Vendedor
from apps.maestros.models.base_models import Provincia
from ..forms.buscador_vlestadisticasventasprovincia_forms import BuscadorEstadisticasVentasProvinciaForm
from utils.utils import deserializar_datos, formato_argentino, normalizar, raw_to_dict
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Estadísticas de Ventas por Provincia"
	
	#-- Modelo.
	model = VLEstadisticasVentasProvincia
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorEstadisticasVentasProvinciaForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	model_string = model.__name__.lower()
	
	#-- Vistas del CRUD del modelo.
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
	reporte_pantalla = f"informes/reportes/{model_string}_producto_list.html"
	
	# #-- Establecer las columnas del reporte y sus anchos(en punto).
	# header_data = {
	# 	"id_producto_id": (40, "Código"),
	# 	"cai": (70, "CAI"),
	# 	"nombre_producto": (200, "Descripción"),
	# 	"nombre_producto_familia": (50, "Familia"),
	# 	"nombre_modelo": (50, "Modelo"),
	# 	"nombre_producto_marca": (50, "Marca"),
	# 	"cantidad": (50, "Cantidad"),
	# 	"porcentaje_cantidad": (50, "% Cant"),
	# 	"total": (75, "Total"),
	# 	"porcentaje_total": (50, "% Total")
	# }


class VLEstadisticasVentasProvinciaInformeView(InformeFormView):
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
		vendedor = cleaned_data.get('vendedor', None)
		provincia = cleaned_data.get('provincia', None)
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		id_marca_desde = cleaned_data.get('id_marca_desde')
		id_marca_hasta = cleaned_data.get('id_marca_hasta')
		agrupar = cleaned_data.get('agrupar', None)
		mostrar = cleaned_data.get('mostrar', None)
		
		id_sucursal = sucursal.id_sucursal if sucursal else None
		id_vendedor = vendedor.id_vendedor if vendedor else None
		id_provincia = provincia.id_provincia if provincia else None
		
		queryset = VLEstadisticasVentasProvincia.objects.obtener_datos(
			fecha_desde,
			fecha_hasta,
			id_marca_desde,
			id_marca_hasta,
			agrupar,
			mostrar,
			id_sucursal=id_sucursal,
			id_vendedor=id_vendedor,
			id_provincia=id_provincia
		)
		
		#-- Calcular totales solo si hay registros.
		if queryset:
			total_cantidad = sum(float(obj.cantidad) for obj in queryset)
			total_importes = sum(float(obj.total) for obj in queryset)
			
			#-- Agregar porcentajes a cada objeto.
			for obj in queryset:
				obj.porcentaje_cantidad = (float(obj.cantidad) / total_cantidad * 100) if total_cantidad else 0
				obj.porcentaje_total = (float(obj.total) / total_importes * 100) if total_importes else 0
		
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		sucursal = cleaned_data.get('sucursal', None)
		vendedor = cleaned_data.get('vendedor', None)
		provincia = cleaned_data.get('provincia', None)
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		id_marca_desde = cleaned_data.get('id_marca_desde')
		id_marca_hasta = cleaned_data.get('id_marca_hasta')
		agrupar = cleaned_data.get('agrupar', None)
		mostrar = cleaned_data.get('mostrar', None)
		
		vendedor = Vendedor.objects.filter(pk=vendedor.id_vendedor).first() if vendedor else None
		provincia = Provincia.objects.filter(pk=provincia.id_provincia).first() if provincia else None
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {
			"Sucursal": f"[{sucursal.id_sucursal}] {sucursal.nombre_sucursal}" if sucursal else "Todas",
			"Vendedor": f"[{vendedor.id_vendedor}] {vendedor.nombre_vendedor}" if vendedor else "Todos",
			"Provincia": f"[{provincia.id_provincia}] {provincia.nombre_provincia}" if provincia else "Todas",
			"Agrupado por": agrupar,
			"Mostrar por": mostrar
		}
		param_right = {
			"Desde": fecha_desde.strftime("%d/%m/%Y"),
			"Hasta": fecha_hasta.strftime("%d/%m/%Y"),
			"Marca Desde": id_marca_desde,
			"Marca Hasta": id_marca_hasta
		}
		
		# **************************************************
		#-- Convertir QUERYSET a LISTA DE DICCIONARIOS al inicio (optimización clave).
		queryset_list = [raw_to_dict(obj) for obj in queryset]
		
		#-- Agrupar los objetos por el número de comprobante.
		grouped_data = {}
		total_cantidad = 0
		total_porcentaje_cantidad = Decimal('0')
		total_importe = Decimal('0')
		total_porcentaje_total = Decimal('0')
		
		for obj in queryset_list:
			id_provincia = obj['id_provincia']  #-- Campo que agrupa los datos.
			if id_provincia not in grouped_data:
				grouped_data[id_provincia] = {
					'provincia': obj['nombre_provincia'],
					'detalle': [],
					'subtotal_cantidad': 0,
					'subtotal_porcentaje_cantidad': Decimal(0),
					'subtotal_importe': Decimal(0),
					'subtotal_porcentaje_importe': Decimal(0)
				}
			#-- Añadir el detalle al grupo.
			grouped_data[id_provincia]['detalle'].append(obj)
			
			#-- Calcular el subtotal por provincia.
			cantidad = obj['cantidad']
			porcentaje_cantidad = Decimal(str(obj['porcentaje_cantidad']))
			total = Decimal(str(obj['total']))
			porcentaje_total = Decimal(str(obj['porcentaje_total']))
			
			grouped_data[id_provincia]['subtotal_cantidad'] += cantidad
			grouped_data[id_provincia]['subtotal_porcentaje_cantidad'] += porcentaje_cantidad
			grouped_data[id_provincia]['subtotal_importe'] += total
			grouped_data[id_provincia]['subtotal_porcentaje_importe'] += porcentaje_total
			
			#-- Acumular totales generales.
			total_cantidad += cantidad
			total_porcentaje_cantidad += porcentaje_cantidad
			total_importe += total
			total_porcentaje_total += porcentaje_total
		
		#-- Convertir los datos agrupados a un formato serializable:
		for data in grouped_data.values():
			data['subtotal_porcentaje_cantidad'] = float(data['subtotal_porcentaje_cantidad'])
			data['subtotal_importe'] = float(data['subtotal_importe'])
			data['subtotal_porcentaje_importe'] = float(data['subtotal_porcentaje_importe'])
		
		# **************************************************
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": grouped_data,
			"total_cantidad": float(total_cantidad),
			"total_porcentaje_cantidad": float(total_porcentaje_cantidad),
			"total_importe": float(total_importe),
			"total_porcentaje_importe": float(total_porcentaje_total),
			"agrupar": agrupar,
			"mostrar": mostrar,
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


def vlestadisticasventasprovincia_vista_pantalla(request):
	#-- Obtener el token de la querystring.
	token = request.GET.get("token")
	
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Obtener el contexto(datos) previamente guardados en la sesión.
	contexto_reporte = deserializar_datos(request.session.pop(token, None))
	
	if not contexto_reporte:
		return HttpResponse("Contexto no encontrado o expirado", status=400)
	
	#-- Generar el listado a pantalla.
	agrupar = contexto_reporte.get("agrupar", None)
	match agrupar:
		case "Producto":
			ConfigViews.reporte_pantalla = f"informes/reportes/{ConfigViews.model_string}_producto_list.html"
		case "Familia":
			ConfigViews.reporte_pantalla = f"informes/reportes/{ConfigViews.model_string}_familia_list.html"
		case "Modelo":
			ConfigViews.reporte_pantalla = f"informes/reportes/{ConfigViews.model_string}_modelo_list.html"
		case "Marca":
			ConfigViews.reporte_pantalla = f"informes/reportes/{ConfigViews.model_string}_marca_list.html"
	
	return render(request, ConfigViews.reporte_pantalla, contexto_reporte)


def vlestadisticasventasprovincia_vista_pdf(request):
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
	agrupar = contexto_reporte.get("agrupar", None)
	mostrar = contexto_reporte.get("mostrar", None)
	
	#-- Crear instancia del generador personalizado.
	if agrupar == "Producto":
		generator = CustomPDFGenerator(contexto_reporte, pagesize=landscape(A4), body_font_size=7)
	else:
		generator = CustomPDFGenerator(contexto_reporte, pagesize=portrait(A4), body_font_size=7)
	
	#-- Construir datos de la tabla:
	
	#-- Títulos de las columnas de la tabla (headers).
	headers, blank_cols = headers_titles(agrupar, mostrar, "pdf")
	
	headers_tit = [value['label'] for value in headers.values()]
	
	#-- Extraer Ancho de las columnas de la tabla.
	col_widths = [value['col_width_pdf'] for value in headers.values()]
	
	table_data = [headers_tit]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (0,0), (0,-1), 'RIGHT'),
		('ALIGN', (-2,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	for id_provincia, datos in contexto_reporte.get("objetos", {}).items():
		
		#-- Datos agrupado por.
		table_data.append([f"Provincia: {datos['provincia']}"] + blank_cols)
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		#---------------------
		
		#-- Agregar filas del detalle.
		for obj in datos['detalle']:
			
			row = []
			
			#-- Construir fila según agrupamiento.
			if agrupar == "Producto":
				row.extend([
					obj['id_producto_id'],
					Paragraph(str(obj['nombre_producto']), generator.styles['CellStyle']),
					Paragraph(str(obj['nombre_producto_familia']), generator.styles['CellStyle']),
					Paragraph(str(obj['nombre_modelo']), generator.styles['CellStyle']),
					Paragraph(str(obj['nombre_producto_marca']), generator.styles['CellStyle'])
				])
			
			elif agrupar == "Familia":
				row.extend([
					Paragraph(str(obj['nombre_producto_familia']), generator.styles['CellStyle']),
					Paragraph(str(obj['nombre_producto_marca']), generator.styles['CellStyle'])
				])
			
			elif agrupar == "Modelo":
				row.extend([
					Paragraph(str(obj['nombre_modelo']), generator.styles['CellStyle']),
					Paragraph(str(obj['nombre_producto_marca']), generator.styles['CellStyle'])
				])
			
			elif agrupar == "Marca":
				row.extend([
					Paragraph(str(obj['nombre_producto_marca']), generator.styles['CellStyle'])
				])
			
			#-- Agregar valores comunes.
			row.extend([
				formato_argentino(obj['cantidad']) if mostrar == "Cantidad" else formato_argentino(obj['total']),
				formato_argentino(obj['porcentaje_cantidad']) if mostrar == "Cantidad" else formato_argentino(obj['porcentaje_total'])
			])
			
			table_data.append(row)
			
			current_row += 1
			
		#-- Fila Total agrupación.
		
		if mostrar == "Cantidad":
			subtotal = datos['subtotal_cantidad']
			porcentaje = datos['subtotal_porcentaje_cantidad']
		else:
			subtotal = datos['subtotal_importe']
			porcentaje = datos['subtotal_porcentaje_importe']
		
		table_data.append(blank_cols + ["Sub Total:", formato_argentino(subtotal), formato_argentino(porcentaje)])
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (-3,current_row), (-1,current_row), 'RIGHT'),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
		])
		
		current_row += 1
		
		#-- Fila divisoria.
		table_data.append(["", ""] + blank_cols)
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1

		
	#-- Fila Total General.
	if mostrar == "Cantidad":
		total_gen = contexto_reporte.get("total_cantidad", 0)
		total_gen_porcentaje = contexto_reporte.get("total_porcentaje_cantidad", 0)
	else:
		total_gen = contexto_reporte.get("total_importe", 0)
		total_gen_porcentaje = contexto_reporte.get("total_porcentaje_importe", 0)
	
	table_data.append(blank_cols + ["Total General:", formato_argentino(total_gen), formato_argentino(total_gen_porcentaje)])
	
	#-- Aplicar estilos a la fila de total (fila actual).
	table_style_config.extend([
		('ALIGN', (-3,-1), (-1,-1), 'RIGHT'),
		('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
		('LINEABOVE', (0,-1), (-1,-1), 0.5, colors.black),  #-- Línea superior.
		# ('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.black),  #-- Línea inferior.
	])
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlestadisticasventasprovincia_vista_excel(request):
	token = request.GET.get("token")
	
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	# ---------------------------------------------
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	agrupar = cleaned_data.get("agrupar", None)
	mostrar = cleaned_data.get("mostrar", None)
	# ---------------------------------------------
	
	#-- Instanciar la vista y obtener el queryset.
	view_instance = VLEstadisticasVentasProvinciaInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	headers, blank_cols = headers_titles(agrupar, mostrar, "excel")
	
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


def vlestadisticasventasprovincia_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	agrupar = cleaned_data.get("agrupar", None)
	mostrar = cleaned_data.get("mostrar", None)
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLEstadisticasVentasProvinciaInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Usar el helper para exportar a CSV.
	headers, blank_cols = headers_titles(agrupar, mostrar, "csv")
	
	helper = ExportHelper(
		queryset=queryset,
		table_info=headers,
		report_title=ConfigViews.report_title
	)
	csv_data = helper.export_to_csv()
	
	response = HttpResponse(csv_data, content_type="text/csv; charset=utf-8")
	response["Content-Disposition"] = f'inline; filename="{ConfigViews.report_title}.csv"'
	
	return response


def headers_titles(agrupar, mostrar, destino):
	headers = {}
	blank_cols = []
	
	if destino != "pdf":
		headers.update({
			"nombre_provincia": {
				"label": "Provincia",
				"col_width_pdf": 0,
				"pdf": True,
				"excel": True,
				"csv": True
			},
		})
	
	if agrupar == "Producto":
		headers.update({
			"id_producto_id": {
				"label": "Código",
				"col_width_pdf": 50,
				"pdf": True,
				"excel": True,
				"csv": True
			},
			"nombre_producto": {
				"label": "Descripción",
				"col_width_pdf": 240,
				"pdf": True,
				"excel": True,
				"csv": True
			},
			"nombre_producto_familia": {
				"label": "Familia",
				"col_width_pdf": 150,
				"pdf": True,
				"excel": True,
				"csv": True
			},
			"nombre_modelo": {
				"label": "Modelo",
				"col_width_pdf": 150,
				"pdf": True,
				"excel": True,
				"csv": True
			},
		})
		blank_cols = ["", "", "", ""]
	elif agrupar == "Familia":
		headers.update({
			"nombre_producto_familia": {
				"label": "Familia",
				"col_width_pdf": 200,
				"pdf": True,
				"excel": True,
				"csv": True
			}
		})
		blank_cols = [""]
		
	elif agrupar == "Modelo":
		headers.update({
			"nombre_modelo": {
				"label": "Modelo",
				"col_width_pdf": 200,
				"pdf": True,
				"excel": True,
				"csv": True
			}
		})
		blank_cols = [""]
		
	elif agrupar == "Marca":
		blank_cols = []
	
	headers.update({
		"nombre_producto_marca": {
			"label": "Marca",
			"col_width_pdf": 110,
			"pdf": True,
			"excel": True,
			"csv": True
		},
	})
	
	if mostrar == "Cantidad":
		headers.update({
			"cantidad": {
				"label": "Cantidad",
				"col_width_pdf": 60,
				"pdf": True,
				"excel": True,
				"csv": True
			},
			"porcentaje_cantidad": {
				"label": "Porcentaje",
				"col_width_pdf": 50,
				"pdf": True,
				"excel": True,
				"csv": True
			},
		})
	else:
		headers.update({
			"total": {
				"label": "Total",
				"col_width_pdf": 60,
				"pdf": True,
				"excel": True,
				"csv": True
			},
			"porcentaje_total": {
				"label": "Porcentaje",
				"col_width_pdf": 50,
				"pdf": True,
				"excel": True,
				"csv": True
			}
		})
	
	return headers, blank_cols

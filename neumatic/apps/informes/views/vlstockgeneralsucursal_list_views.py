# neumatic\apps\informes\views\vlstockgeneralsucursal_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph

from .report_views_generics import *
from apps.informes.models import VLStockGeneralSucursal
from apps.maestros.models.sucursal_models import Sucursal
from ..forms.buscador_vlstockgeneralsucursal_forms import BuscadorStockGeneralSucursalForm
from utils.utils import deserializar_datos, formato_argentino_entero, normalizar, raw_to_dict
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Listado de Stock General"
	
	#-- Modelo.
	model = VLStockGeneralSucursal
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorStockGeneralSucursalForm
	
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
	reporte_pantalla = f"informes/reportes/{model_string}_list.html"
	
	#-- Establecer las columnas del reporte y sus atributos.
	table_info = {
		"id_familia_id": {
			"label": "Id Familia",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_producto_familia": {
			"label": "Familia",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_modelo_id": {
			"label": "Id Modelo",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_modelo": {
			"label": "Modelo",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"id_producto_id": {
			"label": "Código",
			"col_width_pdf": 35,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_cai_id": {
			"label": "Id CAI",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"cai": {
			"label": "CAI",
			"col_width_pdf": 70,
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
		"nombre_producto": {
			"label": "Descripción",
			"col_width_pdf": 170,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"id_marca_id": {
			"label": "Id Marca",
			"col_width_pdf": 0,
			"pdf": False,
			"excel": True,
			"csv": True
		},
		"nombre_producto_marca": {
			"label": "Marca",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
	}


class VLStockGeneralSucursalInformeView(InformeFormView):
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
		id_familia_desde = cleaned_data.get('id_familia_desde', None)
		id_familia_hasta = cleaned_data.get('id_familia_hasta', None)
		id_marca_desde = cleaned_data.get('id_marca_desde', None)
		id_marca_hasta = cleaned_data.get('id_marca_hasta', None)
		id_modelo_desde = cleaned_data.get('id_modelo_desde', None)
		id_modelo_hasta = cleaned_data.get('id_modelo_hasta', None)
		sucursales_seleccionadas = cleaned_data.get('sucursales', [])
		
		tipo_salida = self.request.GET.get('tipo_salida')
		
		if tipo_salida in ["pantalla", "pdf_preliminar"]:
			queryset = VLStockGeneralSucursal.objects.obtener_datos(
				id_familia_desde,
				id_familia_hasta,
				id_marca_desde,
				id_marca_hasta,
				id_modelo_desde,
				id_modelo_hasta,
				sucursales_seleccionadas
			)
		else:
			queryset = VLStockGeneralSucursal.objects.obtener_datos_tabulares(
				id_familia_desde,
				id_familia_hasta,
				id_marca_desde,
				id_marca_hasta,
				id_modelo_desde,
				id_modelo_hasta,
				Sucursal.objects.filter(estatus_sucursal=True)
			)
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		id_familia_desde = cleaned_data.get('id_familia_desde', None)
		id_familia_hasta = cleaned_data.get('id_familia_hasta', None)
		id_marca_desde = cleaned_data.get('id_marca_desde', None)
		id_marca_hasta = cleaned_data.get('id_marca_hasta', None)
		id_modelo_desde = cleaned_data.get('id_modelo_desde', None)
		id_modelo_hasta = cleaned_data.get('id_modelo_hasta', None)
		sucursales_seleccionadas = cleaned_data.get('sucursales', [])
		
		tipo_salida = self.request.GET.get('tipo_salida')
		
		if tipo_salida in ["pantalla", "pdf_preliminar"]:
			
			fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			
			familia = "Todas"
			if id_familia_desde and id_familia_hasta:
				familia = f"Desde: {id_familia_desde} - Hasta: {id_familia_hasta}"
			elif id_familia_desde:
				familia = f"Desde: {id_familia_desde}"
			elif id_familia_hasta:
				familia = f"Hasta: {id_familia_hasta}"
			
			marca = "Todas"
			if id_marca_desde and id_marca_hasta:
				marca = f"Desde: {id_marca_desde} - Hasta: {id_marca_hasta}"
			elif id_marca_desde:
				marca = f"Desde: {id_marca_desde}"
			elif id_marca_hasta:
				marca = f"Hasta: {id_marca_hasta}"
			
			modelo = "Todos"
			if id_modelo_desde and id_modelo_hasta:
				modelo = f"Desde: {id_modelo_desde} - Hasta: {id_modelo_hasta}"
			elif id_modelo_desde:
				modelo = f"Desde: {id_modelo_desde}"
			elif id_modelo_hasta:
				modelo = f"Hasta: {id_modelo_hasta}"
			
			#-- Estructura para mapeo de columnas.
			sucursales_info = _sucursal_info(sucursales_seleccionadas)
			
			param_left = {
				"Sucursal(es)": ", ".join([s['nombre'] for s in sucursales_info]),
			}
			param_right = {
				"Familia": familia,
				"Marca": marca,
				"Modelo": modelo,
			}
			
			# **************************************************
			
			#-- Convertir QUERYSET a LISTA DE DICCIONARIOS al inicio (optimización clave).
			queryset_list = [raw_to_dict(obj) for obj in queryset]
			
			grouped_data = {}
			
			#-- Inicializar totales generales.
			total_general = {
				**{sucursal['nombre']: 0 for sucursal in sucursales_info},
				'otras_suc': 0,
				'stock_total': 0
			}
			
			for obj in queryset_list:
				#-- Agrupar por Familia.
				id_familia = obj['id_familia_id']
				if id_familia not in grouped_data:
					grouped_data[id_familia] = {
						'familia': obj['nombre_producto_familia'],
						'modelos': {},
						'stf': {
							**{sucursal['nombre']: 0 for sucursal in sucursales_info},
							'otras_suc': 0,
							'stock_total': 0
						}
					}
				
				#-- Agrupar por Modelo dentro de Familia.
				id_modelo = obj['id_modelo_id']
				if id_modelo not in grouped_data[id_familia]['modelos']:
					grouped_data[id_familia]['modelos'][id_modelo] = {
						'modelo': obj['nombre_modelo'],
						'detalle': [],
						'stm': {
							**{sucursal['nombre']: 0 for sucursal in sucursales_info},
							'otras_suc': 0,
							'stock_total': 0
						},
					}
				
				#-- Crear registro de detalle con stocks por sucursal.
				detalle = {
					'id_producto_id': obj['id_producto_id'],
					'id_cai_id': obj['id_cai_id'],
					'cai': obj['cai'],
					'medida': obj['medida'],
					'nombre_producto': obj['nombre_producto'],
					'nombre_producto_marca': obj['nombre_producto_marca'],
					'stocks': {},
					'otras_suc': obj.get('otras_suc', 0),
					'stock_total': obj.get('stock_total', 0)
				}
				
				#-- Procesar stocks por sucursal y acumular totales.
				for sucursal in sucursales_info:
					stock = obj.get(sucursal['columna'], 0)
					detalle['stocks'][sucursal['nombre']] = stock
					
					#-- Acumular subtotales por modelo.
					grouped_data[id_familia]['modelos'][id_modelo]['stm'][sucursal['nombre']] += stock
					
					#-- Acumular subtotales por familia.
					grouped_data[id_familia]['stf'][sucursal['nombre']] += stock
					
					#-- Acumular total general.
					total_general[sucursal['nombre']] += stock
				
				#-- Procesar otras sucursales y stock total.
				otras_suc = obj.get('otras_suc', 0)
				stock_total = obj.get('stock_total', 0)
				
				#-- Acumular para modelo.
				grouped_data[id_familia]['modelos'][id_modelo]['stm']['otras_suc'] += otras_suc
				grouped_data[id_familia]['modelos'][id_modelo]['stm']['stock_total'] += stock_total
				
				#-- Acumular para familia.
				grouped_data[id_familia]['stf']['otras_suc'] += otras_suc
				grouped_data[id_familia]['stf']['stock_total'] += stock_total
				
				#-- Acumular total general.
				total_general['otras_suc'] += otras_suc
				total_general['stock_total'] += stock_total
				
				grouped_data[id_familia]['modelos'][id_modelo]['detalle'].append(detalle)
				
			# **************************************************
			
			#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
			return {
				"objetos": grouped_data,
				"sucursales_info": sucursales_info,
				"total_general": total_general,
				"parametros_i": param_left,
				"parametros_d": param_right,
				'fecha_hora_reporte': fecha_hora_reporte,
				'titulo': ConfigViews.report_title,
				'css_url': static('css/reportes.css')
			}
		
		else:
			#-- Convertir QUERYSET a LISTA DE DICCIONARIOS al inicio (optimización clave).
			queryset_list = [raw_to_dict(obj) for obj in queryset]
			
			#-- Estructura para mapeo de columnas.
			sucursales = Sucursal.objects.filter(estatus_sucursal=True)
			
			sucursales_info = _sucursal_info(sucursales)
			
			#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
			return {
				"objetos": queryset_list,
				"sucursales_info": sucursales_info,
			}
			
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		form = kwargs.get("form") or self.get_form()
		
		context["form"] = form
		if form.errors:
			context["data_has_errors"] = True
		return context


def vlstockgeneralsucursal_vista_pantalla(request):
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


def vlstockgeneralsucursal_vista_pdf(request):
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
	
	#-- Agregar las sucursales seleccionadas a ConfigViews.table_info.
	sucursales_info = contexto_reporte.get("sucursales_info", [])
	table_info = _extend_table_info(sucursales_info, "pdf")
	
	#-- Construir datos de la tabla:
	
	#-- Títulos de las columnas de la tabla (headers) filtrados.
	headers_titles = [value['label'] for value in table_info.values() if value['pdf']]
	headers_titles.insert(0, "")
	
	#-- Extraer Ancho de las columnas de la tabla filtrados.
	col_widths = [value['col_width_pdf'] for value in table_info.values() if value['pdf']]
	
	col_widths.insert(0, 10)
	blank_cols = [""] * (5 + len(sucursales_info) + 2)  #-- 5 columnas fijas + las de sucursales + Otras Suc y Stock Total.
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (6,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	for familia_data in contexto_reporte.get("objetos", {}).values():
		
		#-- Datos agrupado por Familia.
		table_data.append([f"Familia: {familia_data['familia']}"] + blank_cols)
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
		])
		
		current_row += 1
		#---------------------
		
		for modelo_data in familia_data["modelos"].values():
		
			#-- Datos agrupado por Modelo.
			table_data.append(["", f"Modelo: {modelo_data['modelo']}"] + blank_cols[:-1])
			
			#-- Aplicar estilos a la fila de agrupación (fila actual).
			table_style_config.extend([
				('SPAN', (1,current_row), (-1,current_row)),
				('FONTNAME', (1,current_row), (-1,current_row), 'Helvetica-Bold')
			])
			
			current_row += 1
			#---------------------
			#-- Agregar filas del detalle.
			for obj in modelo_data['detalle']:
				
				row_data = [
					"",
					obj['id_producto_id'],
					Paragraph(str(obj['cai']), generator.styles['CellStyle']) if obj['cai'] else "",
					Paragraph(str(obj['medida']), generator.styles['CellStyle']),
					Paragraph(str(obj['nombre_producto']), generator.styles['CellStyle']),
					Paragraph(str(obj['nombre_producto_marca']), generator.styles['CellStyle'])
				]
				
				#-- Agregar stocks por sucursal.
				row_data.extend([
					formato_argentino_entero(obj['stocks'][sucursal['nombre']]) for sucursal in sucursales_info
				])
				
				#-- Agregar otras sucursales y total.
				row_data.extend([
					formato_argentino_entero(obj['otras_suc']),
					formato_argentino_entero(obj['stock_total'])
				])
				
				table_data.append(row_data)
				current_row += 1
			
			#-- Fila subtotal por Modelo.
			row_data = [""]*5 + ["Total Modelo:"] + [
				formato_argentino_entero(modelo_data['stm'][sucursal['nombre']]) for sucursal in sucursales_info
			] + [
				formato_argentino_entero(modelo_data['stm']['otras_suc']),
				formato_argentino_entero(modelo_data['stm']['stock_total'])
			]
			table_data.append(row_data)
			
			#-- Aplicar estilos a la fila de total (fila actual).
			table_style_config.extend([
				('ALIGN', (0,current_row), (-1,current_row), 'RIGHT'),
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
				# ('LINEABOVE', (8,current_row), (-1,current_row), 0.5, colors.black),
			])
			current_row += 1
			
		#-- Fila subtotal por Familia.
		row_data = [""]*5 + ["Total Familia:"] + [
			formato_argentino_entero(familia_data['stf'][sucursal['nombre']]) for sucursal in sucursales_info
		] + [
			formato_argentino_entero(familia_data['stf']['otras_suc']),
			formato_argentino_entero(familia_data['stf']['stock_total'])
		]
		table_data.append(row_data)
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (0,current_row), (-1,current_row), 'RIGHT'),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			# ('LINEABOVE', (8,current_row), (-1,current_row), 0.5, colors.black),
		])
		current_row += 1

		#-- Fila divisoria.
		table_data.append([""] + blank_cols)
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
	
	#-- Fila Total General.
	total_general = contexto_reporte.get("total_general", {})
	row_data = [""]*5 + ["Total Genral:"] + [
		formato_argentino_entero(total_general.get(sucursal['nombre'], 0)) for sucursal in sucursales_info
	] + [
		formato_argentino_entero(total_general.get('otras_suc', 0)),
		formato_argentino_entero(total_general.get('stock_total', 0))
	]
	table_data.append(row_data)
	
	#-- Aplicar estilos a la fila de total (fila actual).
	table_style_config.extend([
		('ALIGN', (0,-1), (-1,-1), 'RIGHT'),
		('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
		# ('LINEABOVE', (0,-1), (-1,-1), 0.5, colors.black),  #-- Línea superior.
		# ('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.black),  #-- Línea inferior.
	])
	
	return generator.generate(table_data, col_widths, table_style_config)		


def vlstockgeneralsucursal_vista_excel(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Obtener el contexto(datos) previamente guardados en la sesión.
	contexto_reporte = deserializar_datos(request.session.pop(token, None))
	sucursales_info = contexto_reporte.get("sucursales_info", [])
	
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista y obtener el queryset.
	view_instance = VLStockGeneralSucursalInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Agregar las sucursales seleccionadas a ConfigViews.table_info.
	table_info = _extend_table_info(sucursales_info, "excel")
	
	#-- Filtrar los headers de las columnas.
	headers_titles = {field: table_info[field] for field in table_info if table_info[field]['excel']}
	
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


def vlstockgeneralsucursal_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Obtener el contexto(datos) previamente guardados en la sesión.
	contexto_reporte = deserializar_datos(request.session.pop(token, None))
	sucursales_info = contexto_reporte.get("sucursales_info", [])
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLStockGeneralSucursalInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Agregar las sucursales seleccionadas a ConfigViews.table_info.
	table_info = _extend_table_info(sucursales_info, "csv")
	
	#-- Filtrar los headers de las columnas.
	headers_titles = {field: table_info[field] for field in table_info if table_info[field]['csv']}
	
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


def _sucursal_info(sucursales):
	info = [
		{
			'nombre': sucursal.nombre_sucursal[:5],			 	#-- Nombre corto de la sucursal.
			'columna': f'stock_suc_{sucursal.id_sucursal}',		#-- Nombre real de la columna.
			'id': sucursal.id_sucursal
		}
		for sucursal in sucursales
	]
	return info


def _extend_table_info(sucursales_info, salida="pantalla"):
	table_info = ConfigViews.table_info.copy()
	
	for suc in sucursales_info:
		table_info.update({
			f"{suc['columna']}": {
				"label": f"{suc['nombre']}",
				"col_width_pdf": 40,
				"pdf": True,
				"excel": True,
				"csv": True
			}}
		)
	
	if salida in ["pantalla", "pdf"]:
		table_info.update({
			"otras_suc": {
				"label": "Otras Suc.",
				"col_width_pdf": 45,
				"pdf": True,
				"excel": True,
				"csv": True
			}
		})
	
	table_info.update({
		"stock_total": {
			"label": "Stock Total",
			"col_width_pdf": 45,
			"pdf": True,
			"excel": True,
			"csv": True
		}
	})
	
	return table_info
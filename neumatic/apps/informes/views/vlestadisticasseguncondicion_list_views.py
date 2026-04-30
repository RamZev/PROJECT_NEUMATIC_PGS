# neumatic\apps\informes\views\vlestadisticasseguncondicion_list_views.py

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
from apps.informes.models import VLEstadisticasSegunCondicion
from ..forms.buscador_vlestadisticasseguncondicion_forms import BuscadorEstadisticasSegunCondicionForm
from utils.utils import deserializar_datos, formato_argentino, normalizar, raw_to_dict
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Ventas Según Condición"
	
	#-- Modelo.
	model = VLEstadisticasSegunCondicion
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorEstadisticasSegunCondicionForm
	
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
	# 	"nombre_producto_familia": (80, "Familia"),
	# 	"nombre_producto_marca": (60, "Marca"),
	# 	"nombre_modelo": (60, "Modelo"),
	# 	"id_producto_id": (40, "Código"),
	# 	"nombre_producto": (180, "Descripción"),
	# 	"costo": (60, "Costo"),
	# 	"cantidad_m": (30, "Cantidad"),
	# 	"importe_m": (60, "Importe"),
	# 	"ganancia_m": (60, "Ganancia"),
	# 	"cantidad_r": (30, "Cantidad"),
	# 	"importe_r": (60, "Importe"),
	# 	"ganancia_r": (60, "Ganancia"),
	# 	"cantidad_e": (30, "Cantidad"),
	# 	"importe_e": (60, "Importe"),
	# 	"ganancia_e": (60, "Ganancia")
	# }


class VLEstadisticasSegunCondicionInformeView(InformeFormView):
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
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		id_marca_desde = cleaned_data.get('id_marca_desde')
		id_marca_hasta = cleaned_data.get('id_marca_hasta')
		agrupar = cleaned_data.get('agrupar', None)
		
		id_sucursal = sucursal.id_sucursal if sucursal else None
		
		queryset = VLEstadisticasSegunCondicion.objects.obtener_datos(
			fecha_desde,
			fecha_hasta,
			id_marca_desde,
			id_marca_hasta,
			agrupar,
			id_sucursal=id_sucursal
		)
		
		return queryset
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		sucursal = cleaned_data.get('sucursal', None)
		fecha_desde = cleaned_data.get('fecha_desde')
		fecha_hasta = cleaned_data.get('fecha_hasta')
		id_marca_desde = cleaned_data.get('id_marca_desde')
		id_marca_hasta = cleaned_data.get('id_marca_hasta')
		agrupar = cleaned_data.get('agrupar', None)
		imprimir_importes = cleaned_data.get('imprimir_importes', False)
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {
			"Sucursal": f"[{sucursal.id_sucursal}] {sucursal.nombre_sucursal}" if sucursal else "Todas",
			"Agrupado por": agrupar,
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
		tg_cantidad_m = 0
		tg_importe_m = Decimal('0')
		tg_ganancia_m = Decimal('0')
		tg_cantidad_r = 0
		tg_importe_r = Decimal('0')
		tg_ganancia_r = Decimal('0')
		tg_cantidad_e = 0
		tg_importe_e = Decimal('0')
		tg_ganancia_e = Decimal('0')
		
		match agrupar:
			case "Producto":
				#-- Agrupar por producto.
				for obj in queryset_list:
					familia = obj['nombre_producto_familia']  #-- Campo que agrupa los datos.
					if familia not in grouped_data:
						grouped_data[familia] = {
							'modelos': {},
							'stf_cantidad_m': 0,
							'stf_importe_m': Decimal('0'),
							'stf_ganancia_m': Decimal('0'),
							'stf_cantidad_r': 0,
							'stf_importe_r': Decimal('0'),
							'stf_ganancia_r': Decimal('0'),
							'stf_cantidad_e': 0,
							'stf_importe_e': Decimal('0'),
							'stf_ganancia_e': Decimal('0'),
						}
					
					#-- Agrupar los objetos por Modelos de la Familia.
					modelo = obj['nombre_modelo']
					if modelo not in grouped_data[familia]['modelos']:
						grouped_data[familia]['modelos'][modelo] = {
							'detalle': [],
							'stm_cantidad_m': 0,
							'stm_importe_m': Decimal('0'),
							'stm_ganancia_m': Decimal('0'),
							'stm_cantidad_r': 0,
							'stm_importe_r': Decimal('0'),
							'stm_ganancia_r': Decimal('0'),
							'stm_cantidad_e': 0,
							'stm_importe_e': Decimal('0'),
							'stm_ganancia_e': Decimal('0'),
						}
					
					#-- Añadir el detalle al grupo.
					grouped_data[familia]["modelos"][modelo]["detalle"].append(obj)
					
					#-- Acumular totales por Familia.
					#-- Conversión directa a Decimal (optimización).
					cantidad_m = obj['cantidad_m']
					importe_m = Decimal(str(obj['importe_m']))
					ganancia_m = Decimal(str(obj['ganancia_m']))
					cantidad_r = obj['cantidad_r']
					importe_r = Decimal(str(obj['importe_r']))
					ganancia_r = Decimal(str(obj['ganancia_r']))
					cantidad_e = obj['cantidad_e']
					importe_e = Decimal(str(obj['importe_e']))
					ganancia_e = Decimal(str(obj['ganancia_e']))
					
					grouped_data[familia]['stf_cantidad_m'] += cantidad_m
					grouped_data[familia]['stf_importe_m'] += importe_m
					grouped_data[familia]['stf_ganancia_m'] += ganancia_m
					grouped_data[familia]['stf_cantidad_r'] += cantidad_r
					grouped_data[familia]['stf_importe_r'] += importe_r
					grouped_data[familia]['stf_ganancia_r'] += ganancia_r
					grouped_data[familia]['stf_cantidad_e'] += cantidad_e
					grouped_data[familia]['stf_importe_e'] += importe_e
					grouped_data[familia]['stf_ganancia_e'] += ganancia_e
					
					#-- Acumular totales por Modelo.
					grouped_data[familia]['modelos'][modelo]['stm_cantidad_m'] += cantidad_m
					grouped_data[familia]['modelos'][modelo]['stm_importe_m'] += importe_m
					grouped_data[familia]['modelos'][modelo]['stm_ganancia_m'] += ganancia_m
					grouped_data[familia]['modelos'][modelo]['stm_cantidad_r'] += cantidad_r
					grouped_data[familia]['modelos'][modelo]['stm_importe_r'] += importe_r
					grouped_data[familia]['modelos'][modelo]['stm_ganancia_r'] += ganancia_r
					grouped_data[familia]['modelos'][modelo]['stm_cantidad_e'] += cantidad_e
					grouped_data[familia]['modelos'][modelo]['stm_importe_e'] += importe_e
					grouped_data[familia]['modelos'][modelo]['stm_ganancia_e'] += ganancia_e
					
					#-- Acumular totales generales.
					tg_cantidad_m += cantidad_m
					tg_importe_m += importe_m
					tg_ganancia_m += ganancia_m
					tg_cantidad_r += cantidad_r
					tg_importe_r += importe_r
					tg_ganancia_r += ganancia_r
					tg_cantidad_e += cantidad_e
					tg_importe_e += importe_e
					tg_ganancia_e += ganancia_e
				
				#-- Convertir los datos agrupados a un formato serializable:
				for familia_data in grouped_data.values():
					familia_data['stf_importe_m'] = float(familia_data['stf_importe_m'])
					familia_data['stf_ganancia_m'] = float(familia_data['stf_ganancia_m'])
					familia_data['stf_importe_r'] = float(familia_data['stf_importe_r'])
					familia_data['stf_ganancia_r'] = float(familia_data['stf_ganancia_r'])
					familia_data['stf_importe_e'] = float(familia_data['stf_importe_e'])
					familia_data['stf_ganancia_e'] = float(familia_data['stf_ganancia_e'])
					
					for modelo_data in familia_data['modelos'].values():
						modelo_data['stm_importe_m'] = float(modelo_data['stm_importe_m'])
						modelo_data['stm_ganancia_m'] = float(modelo_data['stm_ganancia_m'])
						modelo_data['stm_importe_r'] = float(modelo_data['stm_importe_r'])
						modelo_data['stm_ganancia_r'] = float(modelo_data['stm_ganancia_r'])
						modelo_data['stm_importe_e'] = float(modelo_data['stm_importe_e'])
						modelo_data['stm_ganancia_e'] = float(modelo_data['stm_ganancia_e'])
				
			case "Familia":
				#-- Agrupar por familia.
				for obj in queryset_list:
					familia = obj['nombre_producto_familia']  #-- Campo que agrupa los datos.
					if familia not in grouped_data:
						grouped_data[familia] = {
							'detalle': [],
							'stf_cantidad_m': 0,
							'stf_importe_m': Decimal('0'),
							'stf_ganancia_m': Decimal('0'),
							'stf_cantidad_r': 0,
							'stf_importe_r': Decimal('0'),
							'stf_ganancia_r': Decimal('0'),
							'stf_cantidad_e': 0,
							'stf_importe_e': Decimal('0'),
							'stf_ganancia_e': Decimal('0'),
						}
					
					#-- Añadir el detalle al grupo.
					grouped_data[familia]["detalle"].append(obj)
					
					#-- Acumular totales por Familia.
					cantidad_m = obj['cantidad_m']
					importe_m = Decimal(str(obj['importe_m']))
					ganancia_m = Decimal(str(obj['ganancia_m']))
					cantidad_r = obj['cantidad_r']
					importe_r = Decimal(str(obj['importe_r']))
					ganancia_r = Decimal(str(obj['ganancia_r']))
					cantidad_e = obj['cantidad_e']
					importe_e = Decimal(str(obj['importe_e']))
					ganancia_e = Decimal(str(obj['ganancia_e']))
					
					grouped_data[familia]['stf_cantidad_m'] += cantidad_m
					grouped_data[familia]['stf_importe_m'] += importe_m
					grouped_data[familia]['stf_ganancia_m'] += ganancia_m
					grouped_data[familia]['stf_cantidad_r'] += cantidad_r
					grouped_data[familia]['stf_importe_r'] += importe_r
					grouped_data[familia]['stf_ganancia_r'] += ganancia_r
					grouped_data[familia]['stf_cantidad_e'] += cantidad_e
					grouped_data[familia]['stf_importe_e'] += importe_e
					grouped_data[familia]['stf_ganancia_e'] += ganancia_e
					
					#-- Acumular totales generales.
					tg_cantidad_m += cantidad_m
					tg_importe_m += importe_m
					tg_ganancia_m += ganancia_m
					tg_cantidad_r += cantidad_r
					tg_importe_r += importe_r
					tg_ganancia_r += ganancia_r
					tg_cantidad_e += cantidad_e
					tg_importe_e += importe_e
					tg_ganancia_e += ganancia_e
				
				#-- Convertir los datos agrupados a un formato serializable:
				for familia_data in grouped_data.values():
					familia_data['stf_importe_m'] = float(familia_data['stf_importe_m'])
					familia_data['stf_ganancia_m'] = float(familia_data['stf_ganancia_m'])
					familia_data['stf_importe_r'] = float(familia_data['stf_importe_r'])
					familia_data['stf_ganancia_r'] = float(familia_data['stf_ganancia_r'])
					familia_data['stf_importe_e'] = float(familia_data['stf_importe_e'])
					familia_data['stf_ganancia_e'] = float(familia_data['stf_ganancia_e'])
			
			case "Modelo":
				#-- Agrupar por modelo.
				for obj in queryset_list:
					marca = obj['nombre_producto_marca']  #-- Campo que agrupa los datos.
					if marca not in grouped_data:
						grouped_data[marca] = {
							'detalle': [],
							'stm_cantidad_m': 0,
							'stm_importe_m': Decimal('0'),
							'stm_ganancia_m': Decimal('0'),
							'stm_cantidad_r': 0,
							'stm_importe_r': Decimal('0'),
							'stm_ganancia_r': Decimal('0'),
							'stm_cantidad_e': 0,
							'stm_importe_e': Decimal('0'),
							'stm_ganancia_e': Decimal('0'),
						}
					
					#-- Añadir el detalle al grupo.
					grouped_data[marca]["detalle"].append(obj)
					
					#-- Acumular totales por Familia.
					cantidad_m = obj['cantidad_m']
					importe_m = Decimal(str(obj['importe_m']))
					ganancia_m = Decimal(str(obj['ganancia_m']))
					cantidad_r = obj['cantidad_r']
					importe_r = Decimal(str(obj['importe_r']))
					ganancia_r = Decimal(str(obj['ganancia_r']))
					cantidad_e = obj['cantidad_e']
					importe_e = Decimal(str(obj['importe_e']))
					ganancia_e = Decimal(str(obj['ganancia_e']))
					
					grouped_data[marca]['stm_cantidad_m'] += cantidad_m
					grouped_data[marca]['stm_importe_m'] += importe_m
					grouped_data[marca]['stm_ganancia_m'] += ganancia_m
					grouped_data[marca]['stm_cantidad_r'] += cantidad_r
					grouped_data[marca]['stm_importe_r'] += importe_r
					grouped_data[marca]['stm_ganancia_r'] += ganancia_r
					grouped_data[marca]['stm_cantidad_e'] += cantidad_e
					grouped_data[marca]['stm_importe_e'] += importe_e
					grouped_data[marca]['stm_ganancia_e'] += ganancia_e
					
					#-- Acumular totales generales.
					tg_cantidad_m += cantidad_m
					tg_importe_m += importe_m
					tg_ganancia_m += ganancia_m
					tg_cantidad_r += cantidad_r
					tg_importe_r += importe_r
					tg_ganancia_r += ganancia_r
					tg_cantidad_e += cantidad_e
					tg_importe_e += importe_e
					tg_ganancia_e += ganancia_e
				
				#-- Convertir los datos agrupados a un formato serializable:
				for marca_data in grouped_data.values():
					marca_data['stm_importe_m'] = float(marca_data['stm_importe_m'])
					marca_data['stm_ganancia_m'] = float(marca_data['stm_ganancia_m'])
					marca_data['stm_importe_r'] = float(marca_data['stm_importe_r'])
					marca_data['stm_ganancia_r'] = float(marca_data['stm_ganancia_r'])
					marca_data['stm_importe_e'] = float(marca_data['stm_importe_e'])
					marca_data['stm_ganancia_e'] = float(marca_data['stm_ganancia_e'])
				
			case "Marca":
				
				#-- Acumular totales generales.
				for obj in queryset_list:
					tg_cantidad_m += obj['cantidad_m']
					tg_importe_m += Decimal(str(obj['importe_m']))
					tg_ganancia_m += Decimal(str(obj['ganancia_m']))
					tg_cantidad_r += obj['cantidad_r']
					tg_importe_r += Decimal(str(obj['importe_r']))
					tg_ganancia_r += Decimal(str(obj['ganancia_r']))
					tg_cantidad_e += obj['cantidad_e']
					tg_importe_e += Decimal(str(obj['importe_e']))
					tg_ganancia_e += Decimal(str(obj['ganancia_e']))
				
		# **************************************************
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": grouped_data,
			"tg_cantidad_m": tg_cantidad_m,
			"tg_importe_m": float(tg_importe_m),
			"tg_ganancia_m": float(tg_ganancia_m),
			"tg_cantidad_r": tg_cantidad_r,
			"tg_importe_r": float(tg_importe_r),
			"tg_ganancia_r": float(tg_ganancia_r),
			"tg_cantidad_e": tg_cantidad_e,
			"tg_importe_e": float(tg_importe_e),
			"tg_ganancia_e": float(tg_ganancia_e),
			"agrupar": agrupar,
			"imprimir_importes": imprimir_importes,
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


def vlestadisticasseguncondicion_vista_pantalla(request):
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


def vlestadisticasseguncondicion_vista_pdf(request):
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
	imprimir_importes = contexto_reporte.get("imprimir_importes", False)
	
	#-- Crear instancia del generador personalizado.
	generator = CustomPDFGenerator(contexto_reporte, pagesize=landscape(A4))
	
	#-- Construir datos de la tabla:
	
	#-- Títulos de las columnas de la tabla (headers).
	headers, blank_cols = headers_titles(agrupar, "pdf")
	
	headers_tit_line1 = [""] + blank_cols + ["MOSTRADOR", "", "", "", "REVENTA", "", "", "", "E-COMERCE", "", "", ""]
	
	headers_tit_line2 = [value['label'] for value in headers.values()]
	
	#-- Extraer Ancho de las columnas de la tabla.
	col_widths = [value['col_width_pdf'] for value in headers.values()]
	
	if agrupar != "Marca":
		headers_tit_line2.insert(0, "")
		col_widths.insert(0, 10)
	
	table_data = [headers_tit_line1, headers_tit_line2]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		#-- Estilos para la primera línea de encabezados.
		('SPAN', (-12,0), (-9,0)),  # MOSTRADOR
		('SPAN', (-8,0), (-5,0)),   # REVENTA
		('SPAN', (-4,0), (-1,0)),   # E-COMERCE
		('ALIGN', (0,0), (-1,0), 'CENTER'),
		('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
		
		#-- Estilos para la segunda línea de encabezados.
		('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
		
		#-- Bordes izquierdos para separar secciones.
		('LINEBEFORE', (-12,0), (-12,1), 1, colors.white),  # Después de columnas de agrupamiento
		('LINEBEFORE', (-8,0), (-8,1), 1, colors.white),    # Después de MOSTRADOR
		('LINEBEFORE', (-4,0), (-4,1), 1, colors.white),    # Después de REVENTA
		
		#-- Alineación de datos numéricos.
		('ALIGN', (-12,1), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 2 porque el header tien 2 líneas (0 y 1)).
	current_row = 2
	
	#-- Agregar los datos a la tabla.
	if agrupar == "Producto":
		for familia, familia_data in contexto_reporte.get("objetos", {}).items():
			
			#-- Datos agrupado por.
			table_data.append([f"Familia: {familia}"] + [""]*14)
			
			#-- Aplicar estilos a la fila de agrupación (fila actual).
			table_style_config.extend([
				('SPAN', (0,current_row), (-1,current_row)),
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
			])
			
			current_row += 1
			#---------------------
			
			for modelo, modelo_data in familia_data["modelos"].items():
				
				#-- Datos agrupado por.
				table_data.append(["", f"Modelo: {modelo}"] + [""]*13)
				
				#-- Aplicar estilos a la fila de agrupación (fila actual).
				table_style_config.extend([
					('SPAN', (1,current_row), (-1,current_row)),
					('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
				])
				
				current_row += 1
				
				#-- Agregar filas del detalle.
				for obj in modelo_data['detalle']:
					
					table_data.append([
						"",
						obj['id_producto_id'],
						Paragraph(str(obj['nombre_producto']), generator.styles['CellStyle']),
						
						formato_argentino(obj['cantidad_m']),
						formato_argentino(obj['importe_m']) if imprimir_importes else "",
						formato_argentino(obj['costo_m']) if imprimir_importes else "",
						formato_argentino(obj['ganancia_m']) if imprimir_importes else "",
						
						formato_argentino(obj['cantidad_r']),
						formato_argentino(obj['importe_r']) if imprimir_importes else "",
						formato_argentino(obj['costo_r']) if imprimir_importes else "",
						formato_argentino(obj['ganancia_r']) if imprimir_importes else "",
						
						formato_argentino(obj['cantidad_e']),
						formato_argentino(obj['importe_e']) if imprimir_importes else "",
						formato_argentino(obj['costo_e']) if imprimir_importes else "",
						formato_argentino(obj['ganancia_e']) if imprimir_importes else ""
					])
					
					current_row += 1
					
				#-- Fila Totales por Modelo.
				
				table_data.append(
					blank_cols + [f"Sub Total {modelo}:",
					formato_argentino(modelo_data["stm_cantidad_m"]),
					formato_argentino(modelo_data["stm_importe_m"]) if imprimir_importes else "",
					"",
					formato_argentino(modelo_data["stm_ganancia_m"]) if imprimir_importes else "",
				
					formato_argentino(modelo_data["stm_cantidad_r"]),
					formato_argentino(modelo_data["stm_importe_r"]) if imprimir_importes else "",
					"",
					formato_argentino(modelo_data["stm_ganancia_r"]) if imprimir_importes else "",
					
					formato_argentino(modelo_data["stm_cantidad_e"]),
					formato_argentino(modelo_data["stm_importe_e"]) if imprimir_importes else "",
					"",
					formato_argentino(modelo_data["stm_ganancia_e"]) if imprimir_importes else "",
					]
				)
				
				#-- Aplicar estilos a la fila de total (fila actual).
				table_style_config.extend([
					('ALIGN', (-13,current_row), (-1,current_row), 'RIGHT'),
					('FONTNAME', (-13,current_row), (-1,current_row), 'Helvetica-Bold'),
					# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
				])
				
				current_row += 1
			
			#-- Fila Totales por Familia.
			
			table_data.append(
				blank_cols + [f"Sub Total {familia}:",
				formato_argentino(familia_data["stf_cantidad_m"]),
				formato_argentino(familia_data["stf_importe_m"]) if imprimir_importes else "",
				"",
				formato_argentino(familia_data["stf_ganancia_m"]) if imprimir_importes else "",
			
				formato_argentino(familia_data["stf_cantidad_r"]),
				formato_argentino(familia_data["stf_importe_r"]) if imprimir_importes else "",
				"",
				formato_argentino(familia_data["stf_ganancia_r"]) if imprimir_importes else "",
				
				formato_argentino(familia_data["stf_cantidad_e"]),
				formato_argentino(familia_data["stf_importe_e"]) if imprimir_importes else "",
				"",
				formato_argentino(familia_data["stf_ganancia_e"]) if imprimir_importes else "",
				]
			)
			
			#-- Aplicar estilos a la fila de total (fila actual).
			table_style_config.extend([
				('ALIGN', (-13,current_row), (-1,current_row), 'RIGHT'),
				('FONTNAME', (-13,current_row), (-1,current_row), 'Helvetica-Bold'),
				# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
			])
			
			current_row += 1
			
			#-- Fila divisoria.
			table_data.append(blank_cols + [""]*13)
			table_style_config.append(
				('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
			)
			current_row += 1
			
		#-- Fila Totales Generales.
		table_data.append(
			blank_cols + ["Totales Generales:", 
				formato_argentino(contexto_reporte.get("tg_cantidad_m")),
				formato_argentino(contexto_reporte.get("tg_importe_m")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_m")) if imprimir_importes else "",
			
				formato_argentino(contexto_reporte.get("tg_cantidad_r")),
				formato_argentino(contexto_reporte.get("tg_importe_r")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_r")) if imprimir_importes else "",
				
				formato_argentino(contexto_reporte.get("tg_cantidad_e")),
				formato_argentino(contexto_reporte.get("tg_importe_e")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_e")) if imprimir_importes else "",
				]
			)
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (-13,-1), (-1,-1), 'RIGHT'),
			('FONTNAME', (-13,-1), (-1,-1), 'Helvetica-Bold'),
			# ('LINEABOVE', (0,-1), (-1,-1), 0.5, colors.black),  #-- Línea superior.
			# ('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.black),  #-- Línea inferior.
		])
		
	elif agrupar == "Familia":
		for familia, familia_data in contexto_reporte.get("objetos", {}).items():
			
			#-- Datos agrupado por.
			table_data.append([f"Familia: {familia}"] + [""]*13)
			
			#-- Aplicar estilos a la fila de agrupación (fila actual).
			table_style_config.extend([
				('SPAN', (0,current_row), (-1,current_row)),
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
			])
			
			current_row += 1
			#---------------------
			
			#-- Agregar filas del detalle.
			for obj in familia_data['detalle']:
				
				table_data.append([
					"",
					Paragraph(str(obj['nombre_producto_marca']), generator.styles['CellStyle']),
					
					formato_argentino(obj['cantidad_m']),
					formato_argentino(obj['importe_m']) if imprimir_importes else "",
					formato_argentino(obj['costo_m']) if imprimir_importes else "",
					formato_argentino(obj['ganancia_m']) if imprimir_importes else "",
					
					formato_argentino(obj['cantidad_r']),
					formato_argentino(obj['importe_r']) if imprimir_importes else "",
					formato_argentino(obj['costo_r']) if imprimir_importes else "",
					formato_argentino(obj['ganancia_r']) if imprimir_importes else "",
					
					formato_argentino(obj['cantidad_e']),
					formato_argentino(obj['importe_e']) if imprimir_importes else "",
					formato_argentino(obj['costo_e']) if imprimir_importes else "",
					formato_argentino(obj['ganancia_e']) if imprimir_importes else ""
				])
				
				current_row += 1
				
			#-- Fila Totales por Familia.
			
			table_data.append(
				blank_cols + [f"Sub Total {familia}:",
				formato_argentino(familia_data["stf_cantidad_m"]),
				formato_argentino(familia_data["stf_importe_m"]) if imprimir_importes else "",
				"",
				formato_argentino(familia_data["stf_ganancia_m"]) if imprimir_importes else "",
			
				formato_argentino(familia_data["stf_cantidad_r"]),
				formato_argentino(familia_data["stf_importe_r"]) if imprimir_importes else "",
				"",
				formato_argentino(familia_data["stf_ganancia_r"]) if imprimir_importes else "",
				
				formato_argentino(familia_data["stf_cantidad_e"]),
				formato_argentino(familia_data["stf_importe_e"]) if imprimir_importes else "",
				"",
				formato_argentino(familia_data["stf_ganancia_e"]) if imprimir_importes else "",
				]
			)
			
			#-- Aplicar estilos a la fila de total (fila actual).
			table_style_config.extend([
				('ALIGN', (-13,current_row), (-1,current_row), 'RIGHT'),
				('FONTNAME', (-13,current_row), (-1,current_row), 'Helvetica-Bold'),
				# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
			])
			
			current_row += 1
			
			#-- Fila divisoria.
			table_data.append(blank_cols + [""]*13)
			table_style_config.append(
				('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
			)
			current_row += 1
			
		#-- Fila Totales Generales.
		table_data.append(
			blank_cols + ["Totales Generales:", 
				formato_argentino(contexto_reporte.get("tg_cantidad_m")),
				formato_argentino(contexto_reporte.get("tg_importe_m")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_m")) if imprimir_importes else "",
			
				formato_argentino(contexto_reporte.get("tg_cantidad_r")),
				formato_argentino(contexto_reporte.get("tg_importe_r")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_r")) if imprimir_importes else "",
				
				formato_argentino(contexto_reporte.get("tg_cantidad_e")),
				formato_argentino(contexto_reporte.get("tg_importe_e")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_e")) if imprimir_importes else "",
				]
			)
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (-13,-1), (-1,-1), 'RIGHT'),
			('FONTNAME', (-13,-1), (-1,-1), 'Helvetica-Bold'),
			# ('LINEABOVE', (0,-1), (-1,-1), 0.5, colors.black),  #-- Línea superior.
			# ('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.black),  #-- Línea inferior.
		])
		
	elif agrupar == "Modelo":
		for marca, marca_data in contexto_reporte.get("objetos", {}).items():
			
			#-- Datos agrupado por.
			table_data.append([f"Marca: {marca}"] + [""]*13)
			
			#-- Aplicar estilos a la fila de agrupación (fila actual).
			table_style_config.extend([
				('SPAN', (0,current_row), (-1,current_row)),
				('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold')
			])
			
			current_row += 1
			#---------------------
			
			#-- Agregar filas del detalle.
			for obj in marca_data['detalle']:
				
				table_data.append([
					"",
					Paragraph(str(obj['nombre_modelo']), generator.styles['CellStyle']),
					
					formato_argentino(obj['cantidad_m']),
					formato_argentino(obj['importe_m']) if imprimir_importes else "",
					formato_argentino(obj['costo_m']) if imprimir_importes else "",
					formato_argentino(obj['ganancia_m']) if imprimir_importes else "",
					
					formato_argentino(obj['cantidad_r']),
					formato_argentino(obj['importe_r']) if imprimir_importes else "",
					formato_argentino(obj['costo_r']) if imprimir_importes else "",
					formato_argentino(obj['ganancia_r']) if imprimir_importes else "",
					
					formato_argentino(obj['cantidad_e']),
					formato_argentino(obj['importe_e']) if imprimir_importes else "",
					formato_argentino(obj['costo_e']) if imprimir_importes else "",
					formato_argentino(obj['ganancia_e']) if imprimir_importes else ""
				])
				
				current_row += 1
				
			#-- Fila Totales por Familia.
			
			table_data.append(
				blank_cols + [f"Sub Total {marca}:",
				formato_argentino(marca_data["stm_cantidad_m"]),
				formato_argentino(marca_data["stm_importe_m"]) if imprimir_importes else "",
				"",
				formato_argentino(marca_data["stm_ganancia_m"]) if imprimir_importes else "",
			
				formato_argentino(marca_data["stm_cantidad_r"]),
				formato_argentino(marca_data["stm_importe_r"]) if imprimir_importes else "",
				"",
				formato_argentino(marca_data["stm_ganancia_r"]) if imprimir_importes else "",
				
				formato_argentino(marca_data["stm_cantidad_e"]),
				formato_argentino(marca_data["stm_importe_e"]) if imprimir_importes else "",
				"",
				formato_argentino(marca_data["stm_ganancia_e"]) if imprimir_importes else "",
				]
			)
			
			#-- Aplicar estilos a la fila de total (fila actual).
			table_style_config.extend([
				('ALIGN', (-13,current_row), (-1,current_row), 'RIGHT'),
				('FONTNAME', (-13,current_row), (-1,current_row), 'Helvetica-Bold'),
				# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.black),
			])
			
			current_row += 1
			
			#-- Fila divisoria.
			table_data.append(blank_cols + [""]*13)
			table_style_config.append(
				('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
			)
			current_row += 1
			
		#-- Fila Totales Generales.
		table_data.append(
			blank_cols + ["Totales Generales:", 
				formato_argentino(contexto_reporte.get("tg_cantidad_m")),
				formato_argentino(contexto_reporte.get("tg_importe_m")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_m")) if imprimir_importes else "",
			
				formato_argentino(contexto_reporte.get("tg_cantidad_r")),
				formato_argentino(contexto_reporte.get("tg_importe_r")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_r")) if imprimir_importes else "",
				
				formato_argentino(contexto_reporte.get("tg_cantidad_e")),
				formato_argentino(contexto_reporte.get("tg_importe_e")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_e")) if imprimir_importes else "",
				]
			)
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (-13,-1), (-1,-1), 'RIGHT'),
			('FONTNAME', (-13,-1), (-1,-1), 'Helvetica-Bold'),
			# ('LINEABOVE', (0,-1), (-1,-1), 0.5, colors.black),  #-- Línea superior.
			# ('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.black),  #-- Línea inferior.
		])
		
	elif agrupar == "Marca":
		
		o = contexto_reporte.get("objetos", {})
		print(type(o))
		
		#-- Agregar filas del detalle.
		for obj in contexto_reporte.get("objetos", {}):
			
			table_data.append([
				Paragraph(str(obj['nombre_producto_marca']), generator.styles['CellStyle']),
				
				formato_argentino(obj['cantidad_m']),
				formato_argentino(obj['importe_m']) if imprimir_importes else "",
				formato_argentino(obj['costo_m']) if imprimir_importes else "",
				formato_argentino(obj['ganancia_m']) if imprimir_importes else "",
				
				formato_argentino(obj['cantidad_r']),
				formato_argentino(obj['importe_r']) if imprimir_importes else "",
				formato_argentino(obj['costo_r']) if imprimir_importes else "",
				formato_argentino(obj['ganancia_r']) if imprimir_importes else "",
				
				formato_argentino(obj['cantidad_e']),
				formato_argentino(obj['importe_e']) if imprimir_importes else "",
				formato_argentino(obj['costo_e']) if imprimir_importes else "",
				formato_argentino(obj['ganancia_e']) if imprimir_importes else ""
			])
			
			current_row += 1
		
		#-- Fila divisoria.
		table_data.append(blank_cols + [""]*13)
		table_style_config.append(
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		)
		current_row += 1
		
		#-- Fila Totales Generales.
		table_data.append(
			blank_cols + ["Totales Generales:", 
				formato_argentino(contexto_reporte.get("tg_cantidad_m")),
				formato_argentino(contexto_reporte.get("tg_importe_m")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_m")) if imprimir_importes else "",
			
				formato_argentino(contexto_reporte.get("tg_cantidad_r")),
				formato_argentino(contexto_reporte.get("tg_importe_r")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_r")) if imprimir_importes else "",
				
				formato_argentino(contexto_reporte.get("tg_cantidad_e")),
				formato_argentino(contexto_reporte.get("tg_importe_e")) if imprimir_importes else "",
				"",
				formato_argentino(contexto_reporte.get("tg_ganancia_e")) if imprimir_importes else "",
				]
			)
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('ALIGN', (-13,-1), (-1,-1), 'RIGHT'),
			('FONTNAME', (-13,-1), (-1,-1), 'Helvetica-Bold'),
			# ('LINEABOVE', (0,-1), (-1,-1), 0.5, colors.black),  #-- Línea superior.
			# ('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.black),  #-- Línea inferior.
		])
		
	return generator.generate(table_data, col_widths, table_style_config, repeat_rows=2)


def vlestadisticasseguncondicion_vista_excel(request):
	token = request.GET.get("token")
	
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	# ---------------------------------------------
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	agrupar = cleaned_data.get("agrupar", None)
	# ---------------------------------------------
	
	#-- Instanciar la vista y obtener el queryset.
	view_instance = VLEstadisticasSegunCondicionInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	headers, blank_cols = headers_titles(agrupar, "excel")
	
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


def vlestadisticasseguncondicion_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	agrupar = cleaned_data.get("agrupar", None)
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLEstadisticasSegunCondicionInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Usar el helper para exportar a CSV.
	headers, blank_cols = headers_titles(agrupar, "csv")
	
	helper = ExportHelper(
		queryset=queryset,
		table_info=headers,
		report_title=ConfigViews.report_title
	)
	csv_data = helper.export_to_csv()
	
	response = HttpResponse(csv_data, content_type="text/csv; charset=utf-8")
	response["Content-Disposition"] = f'inline; filename="{ConfigViews.report_title}.csv"'
	
	return response


def headers_titles(agrupar, destino):
	headers = {}
	blank_cols = []
	
	if agrupar == "Producto":
		if destino != "pdf":
			headers.update({
				"nombre_producto_familia": {
					"label": "Familia",
					"col_width_pdf": 0,
					"pdf": True,
					"excel": True,
					"csv": True
				},
				"nombre_modelo": {
					"label": "Modelo",
					"col_width_pdf": 0,
					"pdf": True,
					"excel": True,
					"csv": True
				},
			})
		
		headers.update({
			"id_producto_id": {
				"label": "Código",
				"col_width_pdf": 30,
				"pdf": True,
				"excel": True,
				"csv": True
			},
			"nombre_producto": {
				"label": "Descripción",
				"col_width_pdf": 185,
				"pdf": True,
				"excel": True,
				"csv": True
			},
		})
		blank_cols = ["", ""]
		
	elif agrupar == "Familia":
		if destino != "pdf":
			headers.update({
				"nombre_producto_familia": {
					"label": "Familia",
					"col_width_pdf": 110,
					"pdf": True,
					"excel": True,
					"csv": True
				},
			})
		
		headers.update({
			"nombre_producto_marca": {
				"label": "Marca",
				"col_width_pdf": 180,
				"pdf": True,
				"excel": True,
				"csv": True
			}
		})
		blank_cols = [""]
		
	elif agrupar == "Modelo":
		if destino != "pdf":
			headers.update({
				"nombre_producto_marca": (110, "Marca"),
				"nombre_producto_marca": {
					"label": "Marca",
					"col_width_pdf": 110,
					"pdf": True,
					"excel": True,
					"csv": True
				},
			})
		
		headers.update({
			"nombre_modelo": {
				"label": "Modelo",
				"col_width_pdf": 180,
				"pdf": True,
				"excel": True,
				"csv": True
			}
		})
		blank_cols = [""]
		
	elif agrupar == "Marca":
		headers.update({
			"nombre_producto_marca": {
				"label": "Marca",
				"col_width_pdf": 110,
				"pdf": True,
				"excel": True,
				"csv": True
			},
		})
		blank_cols = []
	
	headers.update({
		"cantidad_m": {
			"label": "Cantidad" if destino=="pdf" else "cantidad_mostrador",
			"col_width_pdf": 35,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"importe_m": {
			"label": "Venta" if destino=="pdf" else "venta_mostrador",
			"col_width_pdf": 55,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"costo_m": {
			"label": "Costo" if destino=="pdf" else "costo_mostrador",
			"col_width_pdf": 55,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"ganancia_m": {
			"label": "Ganancia" if destino=="pdf" else "ganancia_mostrador",
			"col_width_pdf": 55,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		
		"cantidad_r": {
			"label": "Cantidad" if destino=="pdf" else "cantidad_reventa",
			"col_width_pdf": 35,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"importe_r": {
			"label": "Venta" if destino=="pdf" else "venta_reventa",
			"col_width_pdf": 55,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"costo_r": {
			"label": "Costo" if destino=="pdf" else "costo_reventa",
			"col_width_pdf": 55,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"ganancia_r": {
			"label": "Ganancia" if destino=="pdf" else "ganancia_reventa",
			"col_width_pdf": 55,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		
		"cantidad_e": {
			"label": "Cantidad" if destino=="pdf" else "cantidad_e-comerce",
			"col_width_pdf": 35,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"importe_e": {
			"label": "Venta" if destino=="pdf" else "venta_e-comerce",
			"col_width_pdf": 55,
			"pdf": True,
			"excel": True,
			"csv": True

		},
		"costo_e": {
			"label": "Costo" if destino=="pdf" else "costo_e-comerce",
			"col_width_pdf": 55,
			"pdf": True,
			"excel": True,
			"csv": True

		},
		"ganancia_e": {
			"label": "Ganancia" if destino=="pdf" else "ganancia_e-comerce",
			"col_width_pdf": 55,
			"pdf": True,
			"excel": True,
			"csv": True

		},
	})

	return headers, blank_cols

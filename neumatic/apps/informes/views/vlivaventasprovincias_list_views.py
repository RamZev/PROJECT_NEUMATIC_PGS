# neumatic\apps\informes\views\vlivaventasprovincias_list_views.py

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
from apps.informes.models import VLIVAVentasProvincias
from apps.maestros.models.empresa_models import Empresa
from ..forms.buscador_vlivaventasprovincias_forms import BuscadorVLIVAVentasProvinciasForm
from utils.utils import deserializar_datos, serializar_queryset, formato_argentino, normalizar
from utils.helpers.export_helpers import ExportHelper, PDFGenerator
from entorno.constantes_base import MESES


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Total de Ventas por Provincias"
	
	#-- Modelo.
	model = VLIVAVentasProvincias
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorVLIVAVentasProvinciasForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	model_string = model.__name__.lower()
	
	# Vistas del CRUD del modelo
	list_view_name = f"{model_string}_list"
	
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
		"nombre_provincia": {
			"label": "Provincia",
			"col_width_pdf": 120,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"gravado": {
			"label": "Gravado",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"exento": {
			"label": "Exento",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"iva": {
			"label": "I.V.A.",
			"col_width_pdf": 80,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"percep_ib": {
			"label": "Percep. IB",
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


class VLIVAVentasProvinciasInformeView(InformeFormView):
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
		sucursal = cleaned_data.get("sucursal")
		anno = cleaned_data.get("anno")
		mes = cleaned_data.get("mes")
		
		id_sucursal = sucursal.id_sucursal if sucursal else None
		
		return VLIVAVentasProvincias.objects.obtener_datos(id_sucursal, anno, mes)
	
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		anno = cleaned_data.get("anno") or 0
		mes = cleaned_data.get("mes")
		
		MESES_DICT = dict(MESES)
		
		param = {
			"Mes": MESES_DICT[mes],
			"Año": anno,
		}
		
		empresa = Empresa.objects.get(pk=1)
		datos_empresa = {
			"cuit": empresa.cuit,
			"empresa": empresa.nombre_fiscal,
			"domicilio": empresa.domicilio_empresa,
			"cp": empresa.codigo_postal,
			"provincia": empresa.id_provincia.nombre_provincia,
			"localidad": empresa.id_localidad.nombre_localidad,
			"sit_iva": empresa.id_iva.nombre_iva
		}
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")		
		
		# **************************************************
		#-- Inicializar los totales como Decimals.
		total_gravado = Decimal(0)
		total_exento = Decimal(0)
		total_iva = Decimal(0)
		total_percep_ib = Decimal(0)
		total_total = Decimal(0)
		
		#-- Iterar sobre cada objeto en el queryset y acumular los totales.
		for obj in queryset:
			total_gravado   += obj.gravado
			total_exento    += obj.exento
			total_iva       += obj.iva
			total_percep_ib += obj.percep_ib
			total_total     += obj.total
		# **************************************************
		
		#-- Serializar el queryset.
		queryset_serializado = serializar_queryset(queryset)
		
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": queryset_serializado,
			"total_gravado": total_gravado,
			"total_exento": total_exento,
			"total_iva": total_iva,
			"total_percep_ib": total_percep_ib,
			"total_total": total_total,
			"parametros": param,
			"datos_empresa": datos_empresa,
			'fecha_hora_reporte': fecha_hora_reporte,
			'titulo': ConfigViews.report_title,
			'logo_url': None,
			'logo_path': None,
			'css_url': static('css/reportes.css'),
		}
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		form = kwargs.get("form") or self.get_form()
		
		context["form"] = form
		if form.errors:
			context["data_has_errors"] = True
		return context


def vlivaventasprovincias_vista_pantalla(request):
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


def vlivaventasprovincias_vista_pdf(request):
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
		
		empresa = context.get('datos_empresa')
		
		return f"""{empresa['empresa']} <br/>
				   {empresa['domicilio']} <br/>
				   <strong>C.P.:</strong> {empresa['cp']} {empresa['provincia']} - {empresa['localidad']} <br/>
				   {empresa['sit_iva']}  <strong>C.U.I.T.:</strong> {empresa['cuit']}"""
	
	#-- Método que se puede sobreescribir/extender según requerimientos.
	# def _get_header_bottom_right(self, context):
	# 	"""Añadir información adicional específica para este reporte"""
	# 	base_content = super()._get_header_bottom_right(context)
	# 	saldo_total = context.get("saldo_total", 0)
	# 	return f"""
	# 		{base_content}<br/>
	# 		<b>Total General:</b> {formato_es_ar(saldo_total)}
	# 	"""
	pass


def generar_pdf(contexto_reporte):
	#-- Crear instancia del generador personalizado.
	generator = CustomPDFGenerator(contexto_reporte, pagesize=portrait(A4))
	
	#-- Construir datos de la tabla:
	
	#-- Extraer Títulos de las columnas de la tabla (headers).
	headers_titles = [value['label'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	#-- Extraer Ancho de las columnas de la tabla.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('FONTSIZE', (0,0), (-1,-1), 8),
		('LEADING', (0,0), (-1,-1), 10),
		('ALIGN', (1,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Agregar los datos a la tabla.
	for obj in contexto_reporte.get("objetos", []):
		table_data.append([
			obj['nombre_provincia'],
			formato_argentino(obj['gravado']),
			formato_argentino(obj['exento']),
			formato_argentino(obj['iva']),
			formato_argentino(obj['percep_ib']),
			formato_argentino(obj['total'])
		])
	
	#-- Fila de Totales.
	total_gravado = contexto_reporte.get('total_gravado')
	total_exento = contexto_reporte.get('total_exento')
	total_iva = contexto_reporte.get('total_iva')
	total_percep_ib = contexto_reporte.get('total_percep_ib')
	total_total = contexto_reporte.get('total_total')
	
	table_data.append(["Totales:", 
		formato_argentino(total_gravado),
		formato_argentino(total_exento),
		formato_argentino(total_iva),
		formato_argentino(total_percep_ib),
		formato_argentino(total_total),
	])
	
	#-- Aplicar estilos a la fila de total (fila actual).
	table_style_config.extend([
		('ALIGN', (0,-1), (-1,-1), 'RIGHT'),
		('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
		('LINEABOVE', (0,-1), (-1,-1), 0.5, colors.black),
	])
		
	return generator.generate(table_data, col_widths, table_style_config)		


def vlivaventasprovincias_vista_excel(request):
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
	view_instance = VLIVAVentasProvinciasInformeView()
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


def vlivaventasprovincias_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = VLIVAVentasProvinciasInformeView()
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

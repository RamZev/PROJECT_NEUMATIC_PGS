# neumatic\apps\informes\views\planillacaja_list_views.py

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.templatetags.static import static
from django.forms import model_to_dict
from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce

#-- ReportLab:
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Paragraph
from reportlab.platypus import LongTable, TableStyle, Spacer

from .report_views_generics import *
from apps.ventas.models.caja_models import Caja
from apps.ventas.models.caja_models import CajaDetalle
from apps.ventas.models.factura_models import Factura
from apps.ventas.models.recibo_models import ChequeRecibo, TarjetaRecibo, DepositoRecibo, RetencionRecibo
from ..forms.buscador_planillacaja_forms import BuscadorPlanillaCajaForm
from utils.utils import deserializar_datos, normalizar, formato_argentino, format_user_display
from utils.helpers.export_helpers import ExportHelper, PDFGenerator


class ConfigViews:
	
	#-- Título del reporte.
	report_title = "Planilla de Caja"
	
	#-- Modelo.
	# model = Factura
	
	#-- Formulario asociado al modelo.
	form_class = BuscadorPlanillaCajaForm
	
	#-- Aplicación asociada al modelo.
	app_label = "informes"
	
	#-- Nombre del modelo en minúsculas.
	# model_string = model.__name__.lower()
	model_string = "planillacaja"
	
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
		"caja": {
			"label": "Caja",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True,
		},
		"idventas": {
			"label": "ID Ventas",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True,
		},
		"comprobante": {
			"label": "Comprobante",
			"col_width_pdf": 0,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": False,
			"excel": True,
			"csv": True,
		},
		"descripcion": {
			"label": "Descripción",
			"col_width_pdf": 250,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True,
		},
		"ingresos": {
			"label": "Ingresos",
			"col_width_pdf": 60,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
		"egresos": {
			"label": "egresos",
			"col_width_pdf": 60,
			"pdf_paragraph": False,
			"date_format": None,
			"pdf": True,
			"excel": True,
			"csv": True
		},
	}


class PlanillaCajaInformeView(InformeFormView):
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
		caja = cleaned_data.get('caja', 0)
		
		caja_obj = Caja.objects.filter(numero_caja=caja).first()
		
		queryset = CajaDetalle.objects.filter(
			id_caja=caja_obj,
		).values(
			'tipo_movimiento',
			'idventas',
			'importe',
			'observacion',
		).order_by('idventas', 'tipo_movimiento')
		
		#---------------------------------------------------------------------------------
		datos_estructurados = {}
		for item in queryset:
			id_venta = item['idventas']
			
			if id_venta is None or id_venta < 0:
				#-- Ingreso/Egreso.
				mov = item['tipo_movimiento']
				grupo = "INGRESOS DE CAJA" if mov == 1 else "EGRESOS DE CAJA"
				if grupo not in datos_estructurados:
					datos_estructurados[grupo] = {
						'comprobantes': [],
						'subtotal_ingresos': 0.0,
						'subtotal_egresos': 0.0
					}
				
				#-- Preparar los datos.
				datos = {
					'caja': caja,
					'idventas': "",
					'comprobante': grupo,
					'descripcion': item['observacion'],
					'ingresos': float(item['importe'] or 0.0) if mov == 1 else 0.0,
					'egresos': float(item['importe'] or 0.0) if mov == 2 else 0.0,
				}
				datos_estructurados[grupo]['comprobantes'].append(datos)
				datos_estructurados[grupo]['subtotal_ingresos'] += float(item['importe'] or 0.0) if mov == 1 else 0.0
				datos_estructurados[grupo]['subtotal_egresos'] += float(item['importe'] or 0.0) if mov == 2 else 0.0
				
			else:
				#-- Obtener datos del comprobante.
				comprobante = Factura.objects.select_related('id_cliente', 'id_comprobante_venta').filter(id_factura=id_venta).first()
				if comprobante:
					compro = comprobante.id_comprobante_venta.nombre_comprobante_venta
					if compro not in datos_estructurados:
						datos_estructurados[compro] = {
							'comprobantes': [],
							'subtotal_ingresos': 0.0,
							'subtotal_egresos': 0.0
						}
					
					#-- Preparar los datos.
					datos = {
						'caja': caja,
						'idventas': item['idventas'],
						'comprobante': compro,
						'descripcion': f"{comprobante.letra_numero_comprobante_formateado} - {comprobante.id_cliente.nombre_cliente}",
						'ingresos': float(item['importe'] or 0.0) if item['importe'] >= 0 else 0.0,
						'egresos': float(item['importe'] or 0.0) if item['importe'] < 0 else 0.0,
					}
					datos_estructurados[compro]['comprobantes'].append(datos)
					datos_estructurados[compro]['subtotal_ingresos'] += float(item['importe'] or 0.0) if item['importe'] >= 0 else 0.0
					datos_estructurados[compro]['subtotal_egresos'] += float(item['importe'] or 0.0) if item['importe'] < 0 else 0.0
		#---------------------------------------------------------------------------------
		return datos_estructurados
		
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Aquí se estructura el contexto para el reporte, agrupando los comprobantes,
		calculando subtotales y totales generales, tal como se requiere para el listado.
		"""
		
		#-- Parámetros del listado.
		caja = cleaned_data.get('caja', 0)
		caja_obj = Caja.objects.filter(numero_caja=caja).first()
		
		usuario_apertura_caja = format_user_display(caja_obj.id_user)
		usuario_cierre_caja = format_user_display(caja_obj.id_usercierre)
		
		fecha_hora_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		
		param_left = {
			"Sucursal": f"[{caja_obj.id_sucursal.id_sucursal}] {caja_obj.id_sucursal.nombre_sucursal}" if caja_obj else "",
			"Usuario apertura": usuario_apertura_caja,
			"Usuario cierre": usuario_cierre_caja,
		}
		param_right = {
			"Número de Caja": f"{str(caja_obj.numero_caja).zfill(8)[:2]}-{str(caja_obj.numero_caja).zfill(8)[2:]}" if caja_obj else "",
			"Fecha de Caja": caja_obj.fecha_caja.strftime("%d/%m/%Y") if caja_obj.fecha_caja else "",
		}
		
		# **************************************************
		
		#-- Determinar resumen montos.
		resumen_montos = {}
		#-- Total en Cheques.
		cheques = ChequeRecibo.objects.filter(
			id_factura__id_caja__id_caja=caja_obj.id_caja
		).aggregate(
			importe_cheques=Coalesce(Sum('importe_cheque'), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2))
		)
		resumen_montos['cheques'] = cheques['importe_cheques']
		
		#-- Total en Tarjetas.
		tarjeta_credito = TarjetaRecibo.objects.filter(
			id_factura__id_caja__id_caja=caja_obj.id_caja
		).aggregate(
			importe_tarjetas=Coalesce(Sum('importe_tarjeta'), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2))
		)
		resumen_montos['tarjeta_credito'] = tarjeta_credito['importe_tarjetas']
		
		#-- Total en Depósitos.
		depositos = DepositoRecibo.objects.filter(
			id_factura__id_caja__id_caja=caja_obj.id_caja
		).aggregate(
			importe_depositos=Coalesce(Sum('importe_deposito'), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2))
		)
		resumen_montos['depositos'] = depositos['importe_depositos']
		
		#-- Total en Retenciones.
		retenciones = RetencionRecibo.objects.filter(
			id_factura__id_caja__id_caja=caja_obj.id_caja
		).aggregate(
			importe_retencion=Coalesce(Sum('importe_retencion'), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2))
		)
		resumen_montos['retenciones'] = retenciones['importe_retencion']
		
		#-- Total Compensa Facturas.
		compensa_facturas = Factura.objects.filter(
			id_caja=caja_obj.id_caja
		).aggregate(
			compensa_facturas=Coalesce(Sum('compensa_factura'), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2))
		)
		resumen_montos['compensa_facturas'] = compensa_facturas['compensa_facturas']
		
		#-- Otros Montos (que están faltando).
		resumen_montos['tarjeta_debito'] = 0.0
		resumen_montos['mercado_pago'] = 0.0
		resumen_montos['dolares'] = 0.0
		
		#-- Serializar el objeto caja.
		caja_obj_serialized = model_to_dict(caja_obj) if caja_obj else {}
		
		# **************************************************
		#-- Se retorna un contexto que será consumido tanto para la vista en pantalla como para la generación del PDF.
		return {
			"objetos": queryset,
			"caja": caja_obj_serialized,
			"resumen_montos": resumen_montos,
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


def planillacaja_vista_pantalla(request):
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


def planillacaja_vista_pdf(request):
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
	
	#-- Obtener datos del contexto.
	caja = contexto_reporte.get("caja", {})
	resumen_montos = contexto_reporte.get("resumen_montos", {})
	
	#-- Crear una lista para almacenar todos los elementos del PDF.
	elements = []
	
	# =========================================================================
	# 1ra. Tabla: Datos del Encabezado de Caja
	# =========================================================================
	#-- Encabezado de la tabla.
	estado_caja = "CERRADA" if caja.get("caja_cerrada") else "ABIERTA"
	header_caja_data = [["CAJA " + estado_caja]]
	
	#-- Crear tabla de encabezado de caja.
	#-- Calcular el ancho total de la tabla basado en los anchos de las columnas que se van a mostrar en el PDF.
	width = sum(v["col_width_pdf"] for v in ConfigViews.table_info.values() if v["pdf"])
	tabla_caja = LongTable(header_caja_data, colWidths=[width])
	tabla_caja_style = TableStyle([
		('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
		('ALIGN', (0, 0), (-1, -1), 'CENTER'),
		('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
		('FONTSIZE', (0, 0), (-1, -1), 8),
		('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
		('BOX', (0, 0), (-1, 0), 0.5, colors.black),
		('TOPPADDING', (0, 0), (-1, -1), 2),
		('BOTTOMPADDING', (0, 0), (-1, -1), 1),
	])
	tabla_caja.setStyle(tabla_caja_style)
	
	#-- Cuerpo de la tabla de caja.
	cuerpo_caja_data = [
		["Saldo Anterior:", formato_argentino(caja.get("saldo_anterior", 0) or 0), "", ""],
		["Ingresos en Efectivo:", formato_argentino(caja.get("ingresos", 0) or 0), "Recuento Dinero:", formato_argentino(caja.get("recuento", 0) or 0)],
		["Egresos en Efectivo:", formato_argentino(caja.get("egresos", 0) or 0), "Diferencia de Caja:", formato_argentino(caja.get("diferencia", 0) or 0)],
		["Saldo Actual:", formato_argentino(caja.get("saldo", 0) or 0), "", ""]
	]
	
	tabla_cuerpo_caja = LongTable(cuerpo_caja_data, colWidths=[100, 85, 100, 85])
	tabla_cuerpo_caja_style = TableStyle([
		('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
		('FONTSIZE', (0, 0), (-1, -1), 7),
		('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
		('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
		('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
		('TOPPADDING', (0, 0), (-1, -1), 2),
		('BOTTOMPADDING', (0, 0), (-1, -1), 2),
		('LEADING', (0,0), (-1,-1), 8),
		('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.grey),
	])
	tabla_cuerpo_caja.setStyle(tabla_cuerpo_caja_style)
	
	# =========================================================================
	# 2da. Tabla: Datos del Resumen de Caja
	# =========================================================================
	#-- Encabezado de la tabla de resumen.
	header_resumen_data = [["RESUMEN DE MEDIOS DE PAGO"]]
	
	tabla_resumen = LongTable(header_resumen_data, colWidths=[width])
	tabla_resumen.setStyle(tabla_caja_style)
	
	#-- Cuerpo de la tabla de resumen.
	cuerpo_resumen_data = [
		["Tarjeta Crédito:", formato_argentino(resumen_montos.get("tarjeta_credito", 0) or 0), "Retenciones:", formato_argentino(resumen_montos.get("retenciones", 0) or 0)],
		["Tarjeta Débito:", formato_argentino(resumen_montos.get("tarjeta_debito", 0) or 0), "Compensa Facturas:", formato_argentino(resumen_montos.get("compensa_facturas", 0) or 0)],
		["Depósitos:", formato_argentino(resumen_montos.get("depositos", 0) or 0), "Mercado Pago:", formato_argentino(resumen_montos.get("mercado_pago", 0) or 0)],
		["Cheques:", formato_argentino(resumen_montos.get("cheques", 0) or 0), "Dólares:", formato_argentino(resumen_montos.get("dolares", 0) or 0)]
	]
	
	if caja.get("observacion_caja"):
		cuerpo_resumen_data.append(
			["Observaciones:", Paragraph(caja.get("observacion_caja"), generator.styles['CellStyle']), "", ""]
		)
	
	tabla_cuerpo_resumen = LongTable(cuerpo_resumen_data, colWidths=[100, 85, 100, 85])
	tabla_cuerpo_resumen_style = TableStyle([
		('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
		('FONTSIZE', (0, 0), (-1, -1), 7),
		('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
		('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
		('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
		('TOPPADDING', (0, 0), (-1, -1), 2),
		('BOTTOMPADDING', (0, 0), (-1, -1), 2),
		('LEADING', (0,0), (-1,-1), 8),
		('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.grey),
		('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Añadir alineación vertical
	])
	
	#-- Si existe observación, agregar el span para que ocupe 3 columnas.
	if caja.get("observacion_caja"):
		fila_observacion = len(cuerpo_resumen_data) - 1
		tabla_cuerpo_resumen_style.add('SPAN', (1, fila_observacion), (3, fila_observacion))
		tabla_cuerpo_resumen_style.add('ALIGN', (1, fila_observacion), (3, fila_observacion), 'LEFT')
		tabla_cuerpo_resumen_style.add('VALIGN', (1, fila_observacion), (3, fila_observacion), 'TOP')

	tabla_cuerpo_caja.setStyle(tabla_cuerpo_caja_style)
	tabla_cuerpo_resumen.setStyle(tabla_cuerpo_resumen_style)

	# =========================================================================
	# 3ra. Tabla: Tabla principal (Detalle de Caja)
	# =========================================================================
	#-- Construir datos de la tabla principal:
	
	#-- Obtener los títulos de las columnas (headers).
	headers_titles = [value['label'] for value in ConfigViews.table_info.values() if value['pdf']]
	headers_titles.insert(0, "")
	
	#-- Extrae los anchos de las columnas de la estructura ConfigViews.table_info.
	col_widths = [value['col_width_pdf'] for value in ConfigViews.table_info.values() if value['pdf']]
	col_widths.insert(0, 10)
	
	table_data = [headers_titles]
	
	#-- Estilos específicos adicionales iniciales de la tabla.
	table_style_config = [
		('ALIGN', (-2,0), (-1,-1), 'RIGHT'),
	]
	
	#-- Contador de filas (empezamos en 1 porque la 0 es el header).
	current_row = 1
	
	#-- Agregar los datos a la tabla.
	for grupo, datos in contexto_reporte.get("objetos", {}).items():
		# Datos agrupado por Tipo de Comprobante.
		table_data.append([
			f"{grupo.upper()}",
			"", "", "",
		])
		
		#-- Aplicar estilos a la fila de agrupación (fila actual).
		table_style_config.extend([
			('SPAN', (0,current_row), (-1,current_row)),
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			('TOPPADDING', (0,current_row), (-1,current_row), 3)
		])
		
		current_row += 1
		
		#-- Agregar filas del detalle.
		for comprobante in datos['comprobantes']:
			table_data.append([
				'',
				Paragraph(str(comprobante['descripcion']), generator.styles['CellStyle']),
				formato_argentino(comprobante['ingresos']) if comprobante['ingresos'] != 0 else "",
				formato_argentino(comprobante['egresos']) if comprobante['egresos'] != 0 else ""
			])
			current_row += 1
		
		#-- Fila Total por Tipo de Comprobante.
		table_data.append([
			f"Totales:",
			"",
			formato_argentino(datos['subtotal_ingresos']) if datos['subtotal_ingresos'] != 0 else "",
			formato_argentino(datos['subtotal_egresos']) if datos['subtotal_egresos'] != 0 else ""
		])
		
		#-- Aplicar estilos a la fila de total (fila actual).
		table_style_config.extend([
			('FONTNAME', (0,current_row), (-1,current_row), 'Helvetica-Bold'),
			('SPAN', (0,current_row), (1,current_row)),
			('ALIGN', (0,current_row), (-1,current_row), 'RIGHT'),
			# ('LINEABOVE', (0,current_row), (-1,current_row), 0.5, colors.gray),
			('LINEBELOW', (0,current_row), (-1,current_row), 0.5, colors.gray),
		])
		
		current_row += 1
	
	#-- Crear la tabla principal.
	table = generator._create_table(table_data, col_widths, table_style_config)
	
	# =========================================================================
	# Agregar todos los elementos en orden
	# =========================================================================
	
	#-- Agregar tabla de encabezado de caja.
	elements.append(tabla_caja)
	elements.append(tabla_cuerpo_caja)
	
	#-- Agregar espacio entre tablas.
	elements.append(Spacer(1, 12))
	
	#-- Agregar tabla de resumen.
	elements.append(tabla_resumen)
	elements.append(tabla_cuerpo_resumen)
	
	#-- Agregar más espacio antes de la tabla principal.
	elements.append(Spacer(1, 20))
	
	#-- Agregar tabla principal.
	elements.append(table)
	
	# =========================================================================
	# Construir el documento con todos los elementos
	# =========================================================================
	
	# NOTA: Aquí necesitas modificar la clase CustomPDFGenerator para aceptar
	# elementos preconstruidos. Podrías agregar un método como este:
	
	#-------------------------------------------------------------------
	# En la clase CustomPDFGenerator:
	# def generate_with_elements(self, elements):
	#     self.doc.build(elements)
	#     pdf = self.buffer.getvalue()
	#     self.buffer.close()
	#     return pdf
	# pdf = generator.generate_with_elements(elements)
	
	#-------------------------------------------------------------------
	# Si no quieres modificar la clase, puedes construir manualmente:
	generator.doc.build(elements)
	pdf = generator.buffer.getvalue()
	generator.buffer.close()
	#-------------------------------------------------------------------
	
	return pdf


def planillacaja_vista_excel(request):
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
	view_instance = PlanillaCajaInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Extraer los comprobantes del queryset estructurado.
	extracted_comprobantes = []

	for item in queryset.values():
		if 'comprobantes' in item:
			extracted_comprobantes.extend(item['comprobantes'])
	
	#-- Filtrar los headers de las columnas.
	headers_titles = {field: ConfigViews.table_info[field] for field in ConfigViews.table_info if ConfigViews.table_info[field]['excel']}
	
	helper = ExportHelper(
		queryset=extracted_comprobantes,
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


def planillacaja_vista_csv(request):
	token = request.GET.get("token")
	if not token:
		return HttpResponse("Token no proporcionado", status=400)
	
	#-- Recuperar los parámetros de filtrado desde la cache.
	data = cache.get(token)
	if not data or "cleaned_data" not in data:
		return HttpResponse("Datos no encontrados o expirados", status=400)
	
	cleaned_data = data["cleaned_data"]
	
	#-- Instanciar la vista para reejecutar la consulta y obtener el queryset.
	view_instance = PlanillaCajaInformeView()
	view_instance.request = request
	queryset = view_instance.obtener_queryset(cleaned_data)
	
	#-- Extraer los comprobantes del queryset estructurado.
	extracted_comprobantes = []
	
	for item in queryset.values():
		if 'comprobantes' in item:
			extracted_comprobantes.extend(item['comprobantes'])
	
	#-- Filtrar los headers de las columnas.
	headers_titles = {field: ConfigViews.table_info[field] for field in ConfigViews.table_info if ConfigViews.table_info[field]['csv']}
	
	#-- Usar el helper para exportar a CSV.
	helper = ExportHelper(
		queryset=extracted_comprobantes,
		table_info=headers_titles,
		report_title=ConfigViews.report_title
	)
	csv_data = helper.export_to_csv()
	
	response = HttpResponse(csv_data, content_type="text/csv; charset=utf-8")
	response["Content-Disposition"] = f'inline; filename="{ConfigViews.report_title}.csv"'
	
	return response

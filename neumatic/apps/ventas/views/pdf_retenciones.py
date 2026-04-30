# neumatic\apps\ventas\views\pdf_retenciones.py
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from datetime import date, datetime

from os import path
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.units import mm

from ..models.compra_models import Compra, DetalleCompra
from apps.maestros.models.empresa_models import Empresa
from utils.utils import formato_argentino


class PDFRetencionView(View):
	
	def get(self, request, pk):
		comprobante = Compra.objects.filter(pk=pk).first()
		
		if comprobante.id_comprobante_compra.retencion:
			return self._generar_pdf_retencion(comprobante)
		
		elif comprobante.id_comprobante_compra.remito:
			return self._generar_pdf_remito(comprobante)
		
	def _generar_pdf_retencion(self, retencion):
		#-- Obtener datos principales.
		empresa = Empresa.objects.first()
		proveedor = retencion.id_proveedor
		
		if not empresa:
			return HttpResponse("No se encontraron datos de empresa configurados", status=400)
		
		buffer = BytesIO()
		c = canvas.Canvas(buffer, pagesize=portrait(A4))
		width, height = portrait(A4)
		margin = 10*mm
		y_position = height - margin
		
		#-- HEADER TOP ----------------------------------------------------------------------------
		
		#-- Dibujar recuadro header top left.
		header_top_height = 35*mm
		c.setLineWidth(0.5)
		y_header_top = y_position - header_top_height
		c.rect(margin, y_header_top, width - 2*margin, header_top_height)
		
		#-- Línea vertical divisoria.
		x_divisoria = 50*mm
		c.line(x_divisoria, y_position, x_divisoria, y_position - header_top_height)
		
		#-- Configuración inicial del logo.
		logo_path = path.join(settings.BASE_DIR, 'static', 'img', 'api.jpg')
		logo_width = 40*mm
		logo_height = 22*mm
		y_position -= 10*mm  # Margen superior adicional
		
		#-- Posicionar el logo.
		try:
			c.drawImage(
				logo_path, 
				x=margin,
				y=y_position -15*mm,
				width=logo_width,
				height=logo_height,
				preserveAspectRatio=True
			)
		except:
			print("Logo no cargado - espacio reservado se mantiene")
		
		y_text_left = y_position - 20*mm
		titulo = "PROVINCIA DE SANTA FE"
		c.setFont("Helvetica", 6)
		c.drawCentredString((margin+x_divisoria)/2, y_text_left, titulo)
		
		#-- Mostrar datos del certificado en el header-top-right.
		#-- Dibujar recuadro título.
		box_heigth = 7*mm
		y_position = y_position + 10*mm - box_heigth
		
		c.setFillGray(0.85)
		c.rect(x_divisoria, y_position, width - margin - x_divisoria, box_heigth, fill=1)
		c.setFillGray(0.0)
		
		y_text_right = y_position + 2*mm
		x_text_right = x_divisoria + 15*mm
		x_title_centred = x_divisoria + ( (width - margin - x_divisoria) / 2 )
		
		titulo = "Certificado de Reteción Impuesto Ingresos Brutos"
		# certificado = f"Certificado Nº: {retencion.numero_comprobante}"
		certificado = f"Certificado Nº: {retencion.compro} {retencion.letra_comprobante} {retencion.numero_comprobante_formateado if retencion.numero_comprobante else ''}"
		fecha_registro = f"Fecha de Retención: {retencion.fecha_registro.strftime('%d/%m/%Y') if retencion.fecha_registro else ''}"
		
		c.setFont("Helvetica-Bold", 10)
		c.drawCentredString(x_title_centred, y_text_right, titulo)
		
		y_text_right -= 10*mm
		c.drawString(x_text_right, y_text_right, certificado)
		
		y_text_right -= 10*mm
		c.drawString(x_text_right, y_text_right, fecha_registro)
		
		#-- A - DATOS DEL AGENTE DE RETENCIÓN -----------------------------------------------------
		
		#-- Dibujar recuadro título.
		box_heigth = 7*mm
		y_position = y_header_top - box_heigth - 2*mm
		
		c.setFillGray(0.85)
		c.rect(margin, y_position, width - 2*margin, box_heigth, fill=1)
		c.setFillGray(0.0)
		
		x_text_left = margin + 5*mm
		x_text_right = width - margin - 5*mm
		y_text_left = y_position + 2*mm
		
		c.setFont("Helvetica-Bold", 10)
		titulo = "A - Datos del Agente de Retención"
		c.drawString(x_text_left, y_text_left, titulo)
		
		#-- Dibujar recuadro datos.
		box_heigth = 20*mm
		y_position = y_position - box_heigth
		c.rect(margin, y_position, width - 2*margin, box_heigth)
		
		nombre_empresa = f"{empresa.nombre_fiscal}" if empresa and empresa.nombre_fiscal else ""
		cuit_empresa = f"{empresa.cuit_formateado}" if empresa and empresa.cuit_formateado else ""
		domicilio = f"{empresa.domicilio_empresa}.   C.P.: {empresa.codigo_postal} - {empresa.id_localidad} - {empresa.id_provincia}"
		
		y_text_left -= 8*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawString(x_text_left, y_text_left, "Apellido y Nombre o Denominación:")
		c.setFont("Helvetica", 9)
		c.drawString(x_text_left + 56*mm, y_text_left, nombre_empresa)
		
		y_text_left -= 5*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawString(x_text_left, y_text_left, "C.U.I.T. Nº:")
		c.drawRightString(x_text_right - 20*mm, y_text_left, "Nº DE INSCRIPCIÓN:")
		c.setFont("Helvetica", 9)
		c.drawString(x_text_left + 18*mm, y_text_left, cuit_empresa)
		c.drawRightString(x_text_right, y_text_left, "921-7463518")
		
		y_text_left -= 5*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawString(x_text_left, y_text_left, "Domicilio:")
		c.setFont("Helvetica", 9)
		c.drawString(x_text_left + 16*mm, y_text_left, domicilio)
		
		#-- B - DATOS DEL SUJETO RETENIDO ---------------------------------------------------------
		
		#-- Dibujar recuadro título.
		box_heigth = 7*mm
		y_position = y_position - box_heigth - 2*mm
		
		c.setFillGray(0.85)
		c.rect(margin, y_position, width - 2*margin, box_heigth, fill=1)
		c.setFillGray(0.0)
		
		x_text_left = margin + 5*mm
		y_text_left = y_position + 2*mm
		
		c.setFont("Helvetica-Bold", 10)
		titulo = "B - Datos del Sujeto de Retención"
		c.drawString(x_text_left, y_text_left, titulo)
		
		#-- Dibujar recuadro datos.
		box_heigth = 20*mm
		y_position = y_position - box_heigth
		c.rect(margin, y_position, width - 2*margin, box_heigth)
		
		nombre_proveedor = f"{proveedor.nombre_proveedor}" if proveedor and proveedor.nombre_proveedor else ""
		cuit_proveedor = f"{proveedor.cuit_formateado}" if proveedor and proveedor.cuit_formateado else ""
		numero_inscripcion = f"{proveedor.ib_numero}" if proveedor and proveedor.ib_numero else ""
		domicilio_proveedor = f"{proveedor.domicilio_proveedor}.   C.P.: {proveedor.codigo_postal} - {proveedor.id_localidad} - {proveedor.id_provincia} " if proveedor and proveedor.domicilio_proveedor else ""
		
		y_text_left -= 8*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawString(x_text_left, y_text_left, "Apellido y Nombre o Denominación:")
		c.setFont("Helvetica", 9)
		c.drawString(x_text_left + 56*mm, y_text_left, nombre_proveedor)
		
		y_text_left -= 5*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawString(x_text_left, y_text_left, "C.U.I.T. Nº:")
		c.drawRightString(x_text_right - 20*mm, y_text_left, "Nº DE INSCRIPCIÓN:")
		c.setFont("Helvetica", 9)
		c.drawString(x_text_left + 18*mm, y_text_left, cuit_proveedor)
		c.drawRightString(x_text_right, y_text_left, numero_inscripcion)
		
		y_text_left -= 5*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawString(x_text_left, y_text_left, "Domicilio:")
		c.setFont("Helvetica", 9)
		c.drawString(x_text_left + 16*mm, y_text_left, domicilio_proveedor)
		
		#-- C - DATOS DE LA RETENCIÓN PRACTICADA --------------------------------------------------
		
		#-- Dibujar recuadro título.
		box_heigth = 7*mm
		y_position = y_position - box_heigth - 2*mm
		
		c.setFillGray(0.85)
		c.rect(margin, y_position, width - 2*margin, box_heigth, fill=1)
		c.setFillGray(0.0)
		
		x_text_left = margin + 5*mm
		y_text_left = y_position + 2*mm
		
		c.setFont("Helvetica-Bold", 10)
		titulo = "C - Datos de la Retención Practicada"
		c.drawString(x_text_left, y_text_left, titulo)
		
		#-- Dibujar recuadro datos 1.
		box_heigth = 10*mm
		y_position = y_position - box_heigth
		
		c.rect(margin, y_position, width - 2*margin, box_heigth)
		
		y_text_left -= 8*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawString(x_text_left, y_text_left, "Disposición:")
		c.drawRightString(x_text_right - 20*mm, y_text_left, "Fecha de Retención:")
		c.setFont("Helvetica", 9)
		c.drawString(x_text_left + 20*mm, y_text_left, "Art. 2 - (Res. Gral. 15/97 y modif.)")
		fecha_retencion = f"{retencion.fecha_registro.strftime('%d/%m/%Y') if retencion.fecha_registro else ''}"
		c.drawRightString(x_text_right, y_text_left, fecha_retencion)
		
		#-- Dibujar recuadro datos 2.
		box_heigth = 15*mm
		y_position = y_position - box_heigth
		
		c.rect(margin, y_position, width - 2*margin, box_heigth)
		
		comprobante = f"{retencion.id_comprobante_venta if retencion.id_comprobante_venta else ''}"
		numero_comprobante = f"{retencion.numero_comprobante_venta_formateado if retencion.numero_comprobante_venta else ''}"
		total_comprobante_venta = f"{formato_argentino(retencion.total_comprobante_venta)}"
		fecha_comprobante = f"{retencion.fecha_comprobante.strftime('%d/%m/%Y') if retencion.fecha_comprobante else ''}"
		
		y_text_left -= 10*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawString(x_text_left, y_text_left, "Comprobante que origina la retención:")
		c.drawRightString(x_text_right - 23*mm, y_text_left, "Nº Comprobante:")
		c.setFont("Helvetica", 9)
		c.drawString(x_text_left + 60*mm, y_text_left, comprobante)
		c.drawRightString(x_text_right, y_text_left, numero_comprobante)
		
		y_text_left -= 5*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawString(x_text_left, y_text_left, "Monto del comprobante que origina la retención:")
		c.drawRightString(x_text_right - 17*mm, y_text_left, "Fecha del Comprobante:")
		c.setFont("Helvetica", 9)
		c.drawString(x_text_left + 75*mm, y_text_left, total_comprobante_venta)
		c.drawRightString(x_text_right, y_text_left, fecha_comprobante)
		
		#-- Dibujar recuadro datos 3.
		box_heigth = 15*mm
		y_position = y_position - box_heigth
		
		c.rect(margin, y_position, width - 2*margin, box_heigth)
		
		monto_imponible = f"{formato_argentino(retencion.exento)}"
		alicuota = f"{formato_argentino(retencion.alicuota_iva)}%"
		
		y_text_left -= 10*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawString(x_text_left, y_text_left, "Monto Imponible:")
		c.drawCentredString(width/2 - 12*mm, y_text_left, "Alicuota:")
		c.drawRightString(x_text_right, y_text_left, "(-) Der. Reg. e Insp.")
		
		c.setFont("Helvetica", 9)
		c.drawString(x_text_left + 27*mm, y_text_left, monto_imponible)
		c.drawCentredString(width/2, y_text_left, alicuota)
		
		y_text_left -= 5*mm
		c.setFont("Helvetica-Bold", 9)
		c.drawRightString(x_text_right, y_text_left, f"MONTO RETENCIÓN: {formato_argentino(retencion.retencion_ingreso_bruto)}")
		c.setFont("Helvetica", 9)
		
		#-- Líneas finales ------------------------------------------------------------------------
		
		cant = 95
		fecha_impresion = f"Fecha de Impresión: {date.today().strftime('%d/%m/%Y')}"
		
		linea1 = "Firma del Agente de Retención: ".ljust(cant, '_')
		linea2 = "Aclaración: ".ljust(cant, '_')
		linea3 = "Cargo: ".ljust(cant, '_')
		
		c.setFont("Courier", 9)
		y_text_left -= 10*mm
		c.drawString(x_text_left, y_text_left, fecha_impresion)
		
		y_text_left -= 15*mm
		c.drawString(x_text_left, y_text_left, linea1)
		
		y_text_left -= 15*mm
		c.drawString(x_text_left, y_text_left, linea2)
		
		y_text_left -= 15*mm
		c.drawString(x_text_left, y_text_left, linea3)
		c.setFont("Helvetica", 9)
		#------------------------------------------------------------------------------------------

		c.showPage()
		c.save()
		
		buffer.seek(0)
		response = HttpResponse(buffer, content_type='application/pdf')
		file = f"Retencion_{retencion.compro}_{retencion.letra_comprobante}_{retencion.numero_comprobante_formateado if retencion.numero_comprobante else ''}"
		response['Content-Disposition'] = f'inline; filename="{file}.pdf"'
		return response
	
	def _generar_pdf_remito(self, remito):
		"""Se generan Remitos Sin formato para imprimir en formatos pre-impresos."""
		
		#-- Obtener datos principales.
		detalle_remito = DetalleCompra.objects.filter(id_compra=remito)
		
		proveedor = remito.id_proveedor
		
		buffer = BytesIO()
		c = canvas.Canvas(buffer, pagesize=portrait(A4))
		width, height = portrait(A4)
		margin = 10*mm
		
		#-- Posicionamiento inicial.
		y_position = height - margin
		
		#-- Ajuste inicial
		y_position -= 24*mm
		
		#-- Mostrar datos del Remito en la parte derecha.
		x_datos_remito = 150*mm
		
		c.setFont("Helvetica-Bold", 12)
		nombre_comprobante = remito.id_comprobante_compra.nombre_impresion if remito.id_comprobante_compra.nombre_impresion else remito.id_comprobante_compra.nombre_comprobante_compra
		c.drawString(x_datos_remito, y_position, nombre_comprobante)
		
		c.setFont("Helvetica-Bold", 10)
		y_position -= 10*mm
		c.drawString(x_datos_remito, y_position, f"{datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")}")
		
		
		#-- Datos del Proveedor. -------------------------------------------------------------------------------
		x_text_left = margin + 5*mm
		x_data_left = x_text_left + 11*mm
		x_text_right = 95*mm
		x_data_right = x_text_right + 1*mm
		
		y_position -= 26*mm
		font_size = 9
		paragraph_style = ParagraphStyle(
			name='Normal',
			fontName='Helvetica',
			fontSize=font_size,
			leading=10,
			textColor=colors.black,
		)
		
		c.setFont("Helvetica-Bold", font_size)
		c.drawString(x_text_left, y_position, "Cuenta")
		c.setFont("Helvetica", font_size)
		c.drawString(x_data_left, y_position, f": {proveedor.id_proveedor}")
		c.setFont("Helvetica-Bold", font_size)
		c.drawRightString(x_text_right, y_position, "Ap. y Nombre/Razón Social:")
		c.setFont("Helvetica", font_size)
		
		parrafo_proveedor = Paragraph(f"{proveedor.nombre_proveedor}", paragraph_style)
		max_width = 100*mm
		w, h = parrafo_proveedor.wrap(max_width, 20*mm)
		line_height = font_size  # o paragraph_style.leading
		parrafo_proveedor.drawOn(c, x_data_right, y_position - (h - line_height))
		
		y_position = y_position - h - 2
		c.setFont("Helvetica-Bold", font_size)
		c.drawString(x_text_left, y_position, "I.V.A.")
		c.setFont("Helvetica", font_size)
		c.drawString(x_data_left, y_position, f": {proveedor.id_tipo_iva.nombre_iva if proveedor.id_tipo_iva else ''}")
		c.setFont("Helvetica-Bold", font_size)
		c.drawRightString(x_text_right, y_position, "Domicilio:")
		c.setFont("Helvetica", font_size)
		c.drawString(x_data_right, y_position, f" {proveedor.domicilio_proveedor}")
		
		y_position -= 4*mm
		c.setFont("Helvetica-Bold", font_size)
		# c.drawString(x_text_left, y_position, proveedor.nombre_tipo_documento_identidad)
		c.drawString(x_text_left, y_position, "C.U.I.T.")
		c.setFont("Helvetica", font_size)
		c.drawString(x_data_left, y_position, f": {proveedor.cuit_formateado}")
		c.setFont("Helvetica-Bold", font_size)
		c.drawRightString(x_text_right, y_position, "Localidad:")
		c.setFont("Helvetica", font_size)
		c.drawString(x_data_right, y_position, f" {proveedor.id_localidad} - {proveedor.id_provincia}")
		
		#-- Imprimir el detalle del comprobante. -------------------------------------------------------------
		
		#-- Estilo de párrafo para la tabla.
		paragraph_style_normal = ParagraphStyle(
			name='Normal',
			fontName='Helvetica',
			fontSize=7,
			leading=8,
			textColor=colors.black,
			alignment=TA_LEFT,
		)
		
		#-- Información de las columnas de la tabla.
		table_info = [
			("CAI", 25*mm),
			("Medida", 30*mm),
			("Descripción", 120*mm),
			("Cantidad", 15*mm),
		]
		
		#-- Establecer estilos iniciales de la tabla
		table_style = [
			#-- Estilo general.
			('FONTSIZE', (0, 0), (-1, -1), 7),
			('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
			('TOPPADDING', (0, 0), (-1, -1), 0),
			('BOTTOMPADDING', (0, 0), (-1, -1), 0),
			('LEADING', (0, 0), (-1, -1), 8),
			
			#-- Estilo Headers.
			# ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#BDBDBD")),  # Gris claro para el encabezado
			# ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
			# ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
			# ('TOPPADDING', (0, 0), (-1, 0), 3),
			# ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
			# #-- Solo borde exterior del header:
			# ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
			# ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
			# ('LINEBEFORE', (0, 0), (0, 0), 0.5, colors.black),
			# ('LINEAFTER', (-1, 0), (-1, 0), 0.5, colors.black),
			
			#-- Estilo específicos.
			('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
			# ('TOPPADDING', (0, 1), (-1, -1), 2),
		]
		
		#-- Extraer encabezados y ancho de columnas.
		headers = [header for header, width in table_info]
		col_widths = [width for header, width in table_info]
		
		#-- Tabla Sin Encabezados.
		detail_data = []
		
		#-- Establecer un contador de filas agregadas a la tabla (empezando en 0 porque no hay header).
		current_row = 0
		
		#-- Agregar los datos a la tabla.
		for detalle in detalle_remito:
			detail_data.append([
				Paragraph(str(detalle.id_producto.id_cai if detalle.id_producto and detalle.id_producto.id_cai else ""), style=paragraph_style_normal),
				str(detalle.id_producto.medida if detalle.id_producto else ""),
				Paragraph(str(detalle.id_producto.nombre_producto if detalle.id_producto else ""), style=paragraph_style_normal),
				formato_argentino(detalle.cantidad)
			])
			current_row += 1
			if detalle.id_producto.despacho_1 or detalle.id_producto.despacho_2:
				numero_despacho = detalle.id_producto.despacho_1 if detalle.id_producto.despacho_1 else detalle.id_producto.despacho_2
				detail_data.append([
					"",
					"",
					f"Nº Despacho: {numero_despacho}",
					"",
					"",
					"",
					"",
					""
				])
				current_row += 1
		
		#-- Agregar una línea de detalle en blaco como separador.
		detail_data.append([
			"",
			"",
			"",
			""
		])
		current_row += 1
		
		#-- Agregar Observaciones si las tiene.
		if remito.observa_comprobante:
			detail_data.append([
				Paragraph(f"Observaciones: {remito.observa_comprobante}", style=paragraph_style_normal),
				"",
				"",
				""
			])
			
			#-- Aplicar estilos a la fila actual.
			table_style.extend([
				('SPAN', (0,current_row), (-1,current_row)),
			])
			current_row += 1
		
		#-- Crear la tabla con sus parámetros.
		tabla = Table(detail_data, colWidths=col_widths, style=table_style, repeatRows=1)
		
		#-- Dibujar tabla.
		y_table = height - 100*mm  # posición fija debajo del recuadro proveedor
		tabla.wrapOn(c, width - 2*margin, height)
		tabla.drawOn(c, margin, y_table - tabla._height)
		
		#-- Depósito y Nro. Control. ---------
		y_position = 35*mm
		c.setFont("Helvetica", 7)
		c.drawString(x_text_left, y_position, f"Depósito: {remito.id_deposito.id_producto_deposito}")
		
		y_position -= 4*mm
		c.drawString(x_text_left, y_position, f"Control: {remito}")
		#-------------------------------------
		
		c.showPage()
		c.save()
		
		buffer.seek(0)
		response = HttpResponse(buffer, content_type='application/pdf')
		file = f"{remito.compro}_{remito.letra_comprobante}_{remito.numero_comprobante_formateado}"
		response['Content-Disposition'] = f'inline; filename="{file}.pdf"'
		return response

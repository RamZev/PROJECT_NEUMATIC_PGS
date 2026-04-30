# neumatic\apps\ventas\views\genera_pdf.py
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from datetime import date, datetime, timedelta

from os import path
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.units import mm

from ..models.factura_models import Factura, DetalleFactura, SerialFactura
from ..models.recibo_models import DetalleRecibo, RetencionRecibo, DepositoRecibo, TarjetaRecibo, ChequeRecibo
from apps.maestros.models.empresa_models import Empresa
from apps.maestros.models.base_models import Leyenda
from utils.utils import formato_argentino, numero_a_letras, obtener_logo


class GeneraPDFView(View):
	# def get(self, request, model_string, pk):
	# 	method_name = f"generar_pdf_{model_string.lower()}"
	# 	if hasattr(self, method_name):
	# 		method = getattr(self, method_name)
	# 		return method(request, pk)
	# 	return self.generar_pdf_default(model_string, pk)
	
	def get(self, request, pk):
		
		comprobante = Factura.objects.filter(pk=pk).first()
		compro = comprobante.id_comprobante_venta.codigo_comprobante_venta
		electronicos = ("FF", "CF", "DF", "FR", "FC", "CE", "DE", "FT")
		manuales = ("FA", "NC", "ND")
		presupuestos = ("PR",)
		
		facturas = electronicos + manuales + presupuestos
		recibos = ("RB", "RR", "RC", "RE", "RS", "RN")
		remitos = ("RF", "RD", "RT", "RM", "DM", "MR", "MD", "MS", "MM", "MI")
		
		if compro in facturas:
			return self._generar_pdf_factura(comprobante)
		
		elif compro in recibos:
			return self._generar_pdf_recibo(comprobante)
		
		elif compro in remitos:
			return self._generar_pdf_remito(comprobante)
	
	def _generar_pdf_factura(self, factura):
		#-- Obtener datos principales.
		detalles = DetalleFactura.objects.filter(id_factura=factura)
		
		empresa = Empresa.objects.first()
		cliente = factura.id_cliente  # No necesitas consulta adicional
		vendedor = factura.id_vendedor
		seriales = SerialFactura.objects.filter(id_factura=factura)
		
		#-- Obtener la ruta del logo de forma segura.
		logo_url, logo_path = obtener_logo()
		
		#-- Determinar las difrerentes alícuotas de IVA.
		iva = {}
		for detalle in detalles:
			if detalle.alic_iva not in iva:
				iva[detalle.alic_iva] = 0
			iva[detalle.alic_iva] += detalle.iva
		
		if not empresa:
			return HttpResponse("No se encontraron datos de empresa configurados", status=400)

		buffer = BytesIO()
		c = canvas.Canvas(buffer, pagesize=portrait(A4))
		width, height = portrait(A4)
		margin = 10*mm
		
		y_position = height - margin
		
		#-- Dibujar recuadro header top.
		header_top_height = 36*mm
		c.setLineWidth(0.6)
		y_header_top = y_position - header_top_height
		c.rect(margin, y_header_top, width - 2*margin, header_top_height)
		
		#-- Reacuadro para la letra y código AFIP del comprobante.
		area_box = 10*mm
		x_line = width/2 + 20*mm
		x_letter_box = x_line-5*mm
		y_letter_box = y_position - area_box
		c.rect(x_letter_box, y_letter_box, area_box, area_box)
		
		c.setFont("Helvetica-Bold", 16)
		c.drawCentredString(x_line, y_letter_box+4*mm, factura.letra_comprobante)
		c.setFont("Helvetica", 6)
		
		cod = ""
		if factura.letra_comprobante == 'A':
			cod = f"Cód.{factura.id_comprobante_venta.codigo_afip_a}"
		elif factura.letra_comprobante == 'B':
			cod = f"Cód.{factura.id_comprobante_venta.codigo_afip_b}"
		
		c.drawCentredString(x_line, y_letter_box+1*mm, cod)
		c.setFont("Helvetica", 8)
		
		#-- Línea vertical divisoria.
		c.line(x_line, y_position-area_box, x_line, y_position - header_top_height)
		
		#-- Configuración inicial del logo.
		logo_width = 30*mm
		logo_height = 12*mm
		
		#-- Posicionamiento inicial.
		y_position = height - margin
		y_position -= 10*mm  # Margen superior adicional

		#-- Posicionar el logo.
		try:
			c.drawImage(
				logo_path,
				x=margin + 5*mm,
				y=y_position -5*mm,
				width=logo_width,
				height=logo_height,
				preserveAspectRatio=True
			)
		except:
			print("Logo no cargado - espacio reservado se mantiene")
		
		
		#-- Mostrar los datos de la empresa en el header-top-left. -------------------------------------------
		c.setFont("Helvetica", 8)
		x_text_left = margin + 5*mm
		y_text_left = y_position - logo_height
		c.drawString(x_text_left, y_text_left, f"Razón Social: {empresa.nombre_fiscal}")
		
		y_text_left -= 3*mm
		c.setFont("Helvetica-Bold", 8)
		c.drawString(x_text_left, y_text_left, f"Sucursal: {factura.id_sucursal.nombre_sucursal}")
		c.setFont("Helvetica", 8)
		
		y_text_left -= 3*mm
		domicilio = f"{factura.id_sucursal.domicilio_sucursal} - {factura.id_sucursal.id_localidad} - {factura.id_sucursal.id_provincia}" if factura.id_sucursal else ''
		c.drawString(x_text_left, y_text_left, f"Domicilio: {domicilio}")
		
		y_text_left -= 3*mm
		c.drawString(x_text_left, y_text_left, f"e-Mail: {factura.id_sucursal.email_sucursal}")
		
		y_text_left -= 3*mm
		c.drawString(x_text_left, y_text_left, f"Teléfono: {factura.id_sucursal.telefono_sucursal}")
		
		
		#-- Mostrar datos del recibo en el header-top-right. -------------------------------------------------
		y_text_right = y_position + 3*mm
		x_text_right = width/2 + 20*mm + 10*mm
		
		c.setFont("Helvetica-Bold", 10)
		nombre_comprobante = factura.id_comprobante_venta.tipo_comprobante if factura.id_comprobante_venta.tipo_comprobante else factura.id_comprobante_venta.nombre_comprobante_venta
		c.drawString(x_text_right, y_text_right, nombre_comprobante)
		
		y_text_right -= 4*mm
		c.drawString(x_text_right, y_text_right, f"Comprobante Nro.: {factura.numero_comprobante_formateado}")
		
		y_text_right -= 4*mm
		c.drawString(x_text_right, y_text_right, f"Fecha: {factura.fecha_comprobante.strftime('%d/%m/%Y')}")
		
		c.setFont("Helvetica", 8)
		y_text_right = y_position - logo_height - 3*mm
		c.drawString(x_text_right, y_text_right, f"I.V.A.: {empresa.id_iva.nombre_iva}")
		
		y_text_right -= 3*mm
		c.drawString(x_text_right, y_text_right, f"CUIT: {empresa.cuit_formateado}")
		
		y_text_right -= 3*mm
		c.drawString(x_text_right, y_text_right, f"Ingresos Brutos: {empresa.ingresos_bruto}")
		
		y_text_right -= 3*mm
		c.drawString(x_text_right, y_text_right, f"Inicio de Actividades: {empresa.inicio_actividad.strftime('%d/%m/%Y')}")
		
		
		#-- Dibujar recuadro para Documentos de Crédito Electrónicos (FCE) -----------------------------------
		c.setFont("Helvetica-Bold", 8)
		box_heigth = 6*mm
		y_box = y_header_top - box_heigth - 1*mm
		
		doc_fce = ("FC", "FT", "CE", "DE" )
		if factura.compro.upper() in doc_fce:
			c.rect(margin, y_box, width - 2*margin, box_heigth)
			fecha_vcto = ""
			if factura.fecha_comprobante and empresa.dias_vencimiento:
				fecha_vcto = (factura.fecha_comprobante + timedelta(days=empresa.dias_vencimiento)).strftime("%d/%m/%Y")
			
			c.drawString(x_text_left, y_box + 2*mm, f"Fecha de Vencimiento para el pago: {fecha_vcto}")
			
			c.drawString(x_text_right, y_box + 2*mm, f"CBU del Emisor: {empresa.cbu}")
			
			y_box = y_box - box_heigth - 1*mm
			y_text_left -= 7*mm
		
		#-- Dibujar recuadro Condición de Venta. -------------------------------------------------------------
		c.rect(margin, y_box, width - 2*margin, box_heigth)
		c.drawString(x_text_left, y_box + 2*mm, f"Condición de Venta: {factura.condicion_venta}")
		
		#-- Si es Factura Remito/FCE MIPYME.
		fac_rto = ("FR", "FT")
		nd_nc = ("CF", "DF", "NC", "ND", "CE", "DE")
		if factura.compro.upper() in fac_rto:
			c.drawString(x_text_right, y_box + 2*mm, f"REMITO: {factura.comprobante_remito} {factura.remito}")
		
		#-- Si es Nota de Crédito/Débito.
		elif factura.compro.upper() in nd_nc:
			compro_asoc = Factura.objects.filter(pk=factura.id_comprobante_asociado).first()
			compro_asoc = compro_asoc.compro_letra_numero_comprobante_formateado if compro_asoc else ""
			c.drawString(x_text_right - 10*mm, y_box + 2*mm, f"COMPROBANTE ASOCIADO: {compro_asoc}")
		
		c.setFont("Helvetica", 8)
		
		
		#-- Dibujar recuadro Datos del Cliente. --------------------------------------------------------------
		box_heigth = 15*mm
		y_box = y_box - box_heigth - 1*mm
		c.rect(margin, y_box, width - 2*margin, box_heigth)
		
		x_data_left = x_text_left + 10*mm
		x_text_right = 92*mm
		x_data_right = x_text_right + 1*mm
		
		y_text_left -= 14*mm
		
		c.setFont("Helvetica-Bold", 8)
		c.drawString(x_text_left, y_text_left, "Cuenta")
		c.setFont("Helvetica", 8)
		c.drawString(x_data_left, y_text_left, f": {cliente.id_cliente}")
		c.setFont("Helvetica-Bold", 8)
		c.drawRightString(x_text_right, y_text_left, "Ap. y Nombre/Razón Social:")
		c.setFont("Helvetica", 8)
		c.drawString(x_data_right, y_text_left, f" {cliente.nombre_cliente}")
		
		y_text_left -= 4*mm
		c.setFont("Helvetica-Bold", 8)
		c.drawString(x_text_left, y_text_left, "I.V.A.")
		c.setFont("Helvetica", 8)
		c.drawString(x_data_left, y_text_left, f": {cliente.id_tipo_iva.nombre_iva if cliente.id_tipo_iva else ''}")
		c.setFont("Helvetica-Bold", 8)
		c.drawRightString(x_text_right, y_text_left, "Domicilio:")
		c.setFont("Helvetica", 8)
		c.drawString(x_data_right, y_text_left, f" {cliente.domicilio_cliente}")
		
		y_text_left -= 4*mm
		c.setFont("Helvetica-Bold", 8)
		# c.drawString(x_text_left, y_text_left, "C.U.I.T.")
		c.drawString(x_text_left, y_text_left, f"{cliente.nombre_tipo_documento_identidad}")
		c.setFont("Helvetica", 8)
		c.drawString(x_data_left, y_text_left, f": {cliente.cuit_formateado}")
		c.setFont("Helvetica-Bold", 8)
		c.drawRightString(x_text_right, y_text_left, "Localidad:")
		c.setFont("Helvetica", 8)
		c.drawString(x_data_right, y_text_left, f" {cliente.id_localidad} - {cliente.id_provincia}")
		
		
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
		paragraph_style_bold = ParagraphStyle(
			name='Normal',
			fontName='Helvetica-Bold',
			fontSize=7,
			leading=8,
			textColor=colors.black,
			alignment=TA_LEFT,
		)
		
		#-- Información de las columnas de la tabla.
		table_info = [
			("CAI", 20*mm),
			("Medida", 20*mm),
			("Descripción", 70*mm),
			("Cantidad", 10*mm),
			("Precio", 20*mm),
			("Alíc. IVA", 12*mm),
			("Desc.", 13*mm),
			("Sub Total", 25*mm)
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
			('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#BDBDBD")),  # Gris claro para el encabezado
			('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
			('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
			('TOPPADDING', (0, 0), (-1, 0), 3),
			('BOTTOMPADDING', (0, 0), (-1, 0), 3),
			#-- Solo borde exterior del header:
			('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.black),
			('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
			('LINEBEFORE', (0, 0), (0, 0), 0.5, colors.black),
			('LINEAFTER', (-1, 0), (-1, 0), 0.5, colors.black),
			
			#-- Estilo específicos.
			('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
			('TOPPADDING', (0, 1), (-1, -1), 2),
		]
		
		#-- Extraer encabezados y ancho de columnas.
		headers = [header for header, width in table_info]
		col_widths = [width for header, width in table_info]
		
		#-- Agregar los Encabezados a la tabla.
		detail_data = [headers]
		
		#-- Establecer un contador de filas agregadas a la tabla (empezando en 1 porque la 0 es el header).
		current_row = 1
		
		#-- Agregar los datos a la tabla.
		for detalle in detalles:
			detail_data.append([
				Paragraph(str(detalle.id_producto.id_cai if detalle.id_producto and detalle.id_producto.id_cai else ""), style=paragraph_style_normal),
				str(detalle.id_producto.medida if detalle.id_producto else ""),
				Paragraph(str(detalle.producto_venta if detalle.producto_venta else ""), style=paragraph_style_normal),
				formato_argentino(detalle.cantidad),
				f"{formato_argentino(detalle.precio)}",
				f"{formato_argentino(detalle.alic_iva)}%",
				f"{formato_argentino(detalle.descuento)}%" if detalle.descuento else "",
				f"{formato_argentino(detalle.total)}"
			])
			current_row += 1
			if (detalle.id_producto.despacho_1 or detalle.id_producto.despacho_2) and factura.compro != "PR":
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
			"",
			"",
			"",
			"",
			""
		])
		current_row += 1
		
		#-- Agregar Seriales si los tiene.
		if seriales:
			s = ""
			for serial in seriales:
				s += serial.producto_serial + " / "
			
			s = s[:-2]
			
			detail_data.append([
				Paragraph(f"Nº Serie: {s}", style=paragraph_style_normal),
				"",
				"",
				"",
				"",
				"",
				"",
				""
			])
			
			#-- Aplicar estilos a la fila actual.
			table_style.extend([
				('SPAN', (0,current_row), (-1,current_row)),
			])
			current_row += 1
		
		#-- Agregar Observaciones si las tiene.
		if factura.observa_comprobante:
			detail_data.append([
				Paragraph(f"Observaciones: {factura.observa_comprobante}", style=paragraph_style_normal),
				"",
				"",
				"",
				"",
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
		y_table = y_box - 1*mm  # posición fija debajo del recuadro cliente
		tabla.wrapOn(c, width - 2*margin, height)
		tabla.drawOn(c, margin, y_table - tabla._height)
		
		
		#-- Totales y datos adicionales. -------------------------------------------------------------
		
		#-- Dibujar recuadro Tatales.
		height_total_box = 35*mm
		width_box_left = 125*mm
		y_total_box = 82*mm - height_total_box
		
		y_sign_line = y_total_box + 5*mm
		y_text = 77*mm
		
		c.rect(margin, y_total_box, width - 2*margin, height_total_box)
		
		x_divider_line = margin + width_box_left
		c.line(x_divider_line, y_total_box+height_total_box, x_divider_line, y_total_box)
		
		if factura.compro != "PR":
			#-- Textos parte izquierda del recuadro Totales.
			x_text_left = margin + 5*mm
			
			#-- Vendedor.
			c.setFont("Helvetica-Bold", 8)
			c.drawString(x_text_left, y_text, "Vendedor:")
			c.setFont("Helvetica", 8)
			c.drawString(x_text_left+15*mm, y_text, f"[{vendedor.id_vendedor}] {vendedor.nombre_vendedor}")
			
			#-- Id. Depósito(almacén).
			deposito = str(factura.id_deposito.id_producto_deposito).zfill(2) if factura.id_deposito else ""
			c.drawRightString(x_divider_line-2*mm, y_text, f"Nro.: {deposito}")
			
			#-- Leyendas. -------------------
			y_leyenda = y_text - 3*mm
			c.setFont("Helvetica", 7)
			
			leyenda = Leyenda.objects.filter(nombre_leyenda__iexact="retiro conforme").first()
			parrafo = Paragraph(leyenda.leyenda, style=paragraph_style_normal)
			max_width = width_box_left - 2*mm
			w, h = parrafo.wrap(max_width, 10*mm)
			parrafo.drawOn(c, x_text_left, y_leyenda - h)
			
			y_leyenda -= h
			
			if factura.stock_clie:
				leyenda = Leyenda.objects.filter(nombre_leyenda__iexact="stock cliente").first()
				parrafo = Paragraph(leyenda.leyenda, style=paragraph_style_bold)
				w, h = parrafo.wrap(max_width, 10*mm)
				parrafo.drawOn(c, x_text_left, y_leyenda - h)
				
				y_leyenda -= h
			
			if factura.no_estadist:
				leyenda = Leyenda.objects.filter(nombre_leyenda__iexact="no estadísticas").first()
				parrafo = Paragraph(leyenda.leyenda, style=paragraph_style_bold)
				w, h = parrafo.wrap(max_width, 10*mm)
				parrafo.drawOn(c, x_text_left, y_leyenda - h)
				
				y_leyenda -= h
			
			if factura.letra_comprobante == "B":
				alic_monto = ""
				for alic, monto in iva.items():
					alic_monto += f"{formato_argentino(alic)}% = ${formato_argentino(monto)}; "
				alic_monto = alic_monto[:-2]
				
				reg = Leyenda.objects.filter(nombre_leyenda__iexact="régimen transparencia").first()
				leyenda = reg.leyenda
				leyenda += f"<br/>IVA Contenido: {alic_monto}"
				
				parrafo = Paragraph(leyenda, style=paragraph_style_bold)
				w, h = parrafo.wrap(max_width, 10*mm)
				parrafo.drawOn(c, x_text_left, y_leyenda - h)
				
				y_leyenda -= h
			#--------------------------------
			
			#-- Recibí Conforme.
			line_size = 50*mm
			x_sign_line = margin + (width_box_left/2 - line_size/2)
			c.line(x_sign_line, y_sign_line, x_sign_line+line_size, y_sign_line)
			c.drawCentredString(x_sign_line+line_size/2, y_total_box+2*mm, "Recibí Conforme")
		
		
		#-- Textos y Montos parte derecha del recuadro Totales.
		x_amount = width - margin - 2*mm
		x_text_right = x_divider_line + 35*mm
		
		if factura.letra_comprobante == 'A' or factura.compro == 'PR':
			
			y_text_right = y_text
			c.setFont("Helvetica-Bold", 8)
			c.drawRightString(x_text_right, y_text, "Gravado :")
			c.setFont("Helvetica", 8)
			
			c.drawRightString(x_amount, y_text_right, f"${formato_argentino(factura.gravado)}")
			
			y_text_right -= 4*mm
			c.setFont("Helvetica-Bold", 8)
			c.drawRightString(x_text_right, y_text_right, "Exento :")
			c.setFont("Helvetica", 8)
			c.drawRightString(x_amount, y_text_right, f"${formato_argentino(factura.exento)}")
			
			for alic, monto in iva.items():
				y_text_right -= 4*mm
				c.setFont("Helvetica-Bold", 8)
				c.drawRightString(x_text_right, y_text_right, f"I.V.A. {formato_argentino(alic)}% :")
				c.setFont("Helvetica", 8)
				c.drawRightString(x_amount, y_text_right, f"${formato_argentino(monto)}")
			
			y_text_right -= 4*mm
			c.setFont("Helvetica-Bold", 8)
			c.drawRightString(x_text_right, y_text_right, "IIBB PERCEPCIÓN :")
			c.setFont("Helvetica", 8)
			c.drawRightString(x_amount, y_text_right, f"${formato_argentino(factura.percep_ib)}")
			
			y_text_right -= 4*mm
			c.setFont("Helvetica-Bold", 8)
			c.drawRightString(x_text_right, y_text_right, "TOTAL :", charSpace=2)
			c.drawRightString(x_amount, y_text_right, f"${formato_argentino(factura.total)}")
			c.setFont("Helvetica", 8)
			
		else:
			y_text_right = y_sign_line
			c.setFont("Helvetica-Bold", 8)
			c.drawRightString(x_text_right, y_text_right, "TOTAL :", charSpace=2)
			c.drawRightString(x_amount, y_text_right, formato_argentino(factura.total))
			c.setFont("Helvetica", 8)
		
		
		if factura.compro != "PR":
			#-- QR, Logo ARCA y datos del CAE.
			
			#-- Código QR.
			x_qr = margin + 2*mm
			y_qr = margin
			
			c.drawImage(path.join(settings.BASE_DIR, 'static', 'img', 'qr.png'), x_qr, y_qr, width=35*mm, height=35*mm, preserveAspectRatio=True)
			
			#-- Logo ARCA.
			x_arca = x_qr+40*mm
			y_arca = y_qr+5*mm
			c.drawImage(path.join(settings.BASE_DIR, 'static', 'img', 'arca.png'), x_arca, y_arca, width=30*mm, height=30*mm, preserveAspectRatio=True)
			
			#-- Datos del CAE.
			x_cae = 150*mm
			y_cae = 35*mm
			
			c.setFont("Helvetica-Bold", 10)
			c.drawRightString(x_cae, y_cae, "CAE Nº :")
			cae = str(factura.cae if factura.cae else "")
			cae_vto = str(factura.cae_vto  if factura.cae_vto else "")
			c.drawString(x_cae+2*mm, y_cae, cae)
			
			c.drawRightString(x_cae, y_cae-5*mm, "Vencimiento CAE :")
			c.drawString(x_cae+2*mm, y_cae-5*mm, cae_vto)
			
			#-- Nro. Control (compro + letra + número).
			c.setFont("Helvetica", 8)
			c.drawCentredString(x_cae, y_qr+10*mm, f"Ctrl.: {factura.compro_letra_numero_comprobante_formateado}")
			
			#-- Cadenas.
			c.setFont("Helvetica-BoldOblique", 8)
			c.drawString(x_arca, y_qr, "Comprobante Autorizado")
			c.setFont("Helvetica", 8)
			
			c.setFont("Helvetica", 10)
			c.drawCentredString(x_cae, y_qr, "ORIGINAL / DUPLICADO")
		
		
		c.showPage()
		c.save()
		
		buffer.seek(0)
		response = HttpResponse(buffer, content_type='application/pdf')
		file = f"{factura.compro}_{factura.letra_comprobante}_{factura.numero_comprobante_formateado}"
		response['Content-Disposition'] = f'inline; filename="{file}.pdf"'
		return response
	
	def _generar_pdf_recibo(self, recibo):
		#-- Obtener datos principales.
		detalle_recibo = DetalleRecibo.objects.filter(id_factura=recibo)
		retenciones = RetencionRecibo.objects.filter(id_factura=recibo)
		depositos = DepositoRecibo.objects.filter(id_factura=recibo)
		tarjetas = TarjetaRecibo.objects.filter(id_factura=recibo)
		cheques = ChequeRecibo.objects.filter(id_factura=recibo)
		
		empresa = Empresa.objects.first()
		cliente = recibo.id_cliente  # No necesitas consulta adicional
		usuario = recibo.id_user
		
		usuario = f"{usuario.first_name} {usuario.last_name}" if usuario.first_name or usuario.last_name else str(usuario)
		
		#-- Obtener la ruta del logo de forma segura.
		logo_url, logo_path = obtener_logo()
		
		if not empresa:
			return HttpResponse("No se encontraron datos de empresa configurados", status=400)
		
		buffer = BytesIO()
		c = canvas.Canvas(buffer, pagesize=portrait(A4))
		width, height = portrait(A4)
		margin = 10*mm
		
		y_position = height - margin
		
		#-- Dibujar recuadro header top left.
		header_top_height = 35*mm
		c.setLineWidth(0.5)
		y_header_top = y_position - header_top_height
		c.rect(margin, y_header_top, width - 2*margin, header_top_height)
		
		#-- Línea vertical divisoria.
		c.line(width/2, y_position, width/2, y_position - header_top_height)
		
		#-- Configuración inicial del logo.
		logo_width = 30*mm
		logo_height = 12*mm
		
		#-- Posicionamiento inicial.
		y_position = height - margin
		y_position -= 10*mm  # Margen superior adicional

		#-- Posicionar el logo.
		try:
			c.drawImage(
				logo_path, 
				x=margin + 5*mm,
				y=y_position -5*mm,
				width=logo_width,
				height=logo_height,
				preserveAspectRatio=True
			)
		except:
			print("Logo no cargado - espacio reservado se mantiene")
		
		#-- Mostrar los datos de la empresa en el header-top-left.
		c.setFont("Helvetica", 8)
		x_text_left = margin + 5*mm
		y_text_left = y_position - logo_height
		c.drawString(x_text_left, y_text_left, empresa.nombre_fiscal)
		
		y_text_left -= 3*mm
		c.drawString(x_text_left, y_text_left, empresa.domicilio_empresa)
		
		y_text_left -= 3*mm
		c.drawString(x_text_left, y_text_left, f"C.P.: ({empresa.codigo_postal})  {empresa.id_localidad} - {empresa.id_provincia}")
		
		y_text_left -= 3*mm
		c.drawString(x_text_left, y_text_left, f"I.V.A.: {empresa.id_iva}    C.U.I.T.: {empresa.cuit_formateado}")
		
		
		#-- Mostrar datos del recibo en el header-top-right.
		y_text_right = y_position
		x_text_right = width/2 + 5*mm
		
		c.setFont("Helvetica-Bold", 10)
		nombre_comprobante = recibo.id_comprobante_venta.tipo_comprobante if recibo.id_comprobante_venta.tipo_comprobante else recibo.id_comprobante_venta.nombre_comprobante_venta
		c.drawString(x_text_right, y_text_right, nombre_comprobante)
		
		y_text_right -= 4*mm
		c.drawString(x_text_right, y_text_right, f"Nro.: {recibo.letra_numero_comprobante_formateado}")
		
		c.setFont("Helvetica", 8)
		y_text_right -= 4*mm
		c.drawString(x_text_right, y_text_right, f"Fecha: {recibo.fecha_comprobante.strftime('%d/%m/%Y')}")
		
		c.drawString(x_text_right, y_text_left, f"Control: {recibo.compro_letra_numero_comprobante_formateado}")
		
		
		#-- Dibujar recuadro header bottom.
		header_bottom_heigth = 15*mm
		y_header_bottom = y_header_top - header_bottom_heigth - 1*mm
		c.rect(margin, y_header_bottom, width - 2*margin, header_bottom_heigth)
		
		y_text = y_header_bottom + header_bottom_heigth - 4*mm
		c.drawString(x_text_left, y_text, "Se ha recibido de:")
		
		c.drawString(x_text_right, y_text, "La suma de:")
		
		y_text -= 3*mm
		c.drawString(x_text_left, y_text, f"{cliente.nombre_cliente}  [{cliente.id_cliente}]")
		
		c.setFont("Helvetica-Bold", 8)
		c.drawString(x_text_right, y_text, f"${formato_argentino(recibo.total)}")
		c.setFont("Helvetica", 8)
		
		y_text -= 3*mm
		c.drawString(x_text_left, y_text, f"{cliente.domicilio_cliente}    C.P.: {cliente.codigo_postal}")
		
		y_text -= 3*mm
		c.drawString(x_text_left, y_text, f"I.V.A.: {cliente.id_tipo_iva}    {cliente.nombre_tipo_documento_identidad}: {cliente.cuit_formateado}")

		
		#-- Mostrar detalle del recibo si existe.
		c.setFont("Helvetica", 7)
		y_detail = y_header_bottom - 5*mm
		
		if detalle_recibo:
			c.drawString(x_text_left, y_detail, "Por el pago de los siguientes Comprobantes:")
			y_detail -= 6*mm
			
			c.rect(margin, y_detail-1.5*mm, width - 2*margin, 5*mm)
			
			x_comprobante = x_text_left
			x_numero = x_text_left + 45*mm
			x_fecha = x_numero + 25*mm
			x_importe = x_fecha + 50*mm
			x_saldo = x_importe + 30*mm
			x_pago = x_saldo + 25*mm
			
			c.setFont("Helvetica-Bold", 7)
			c.drawString(x_comprobante, y_detail, "Comprobante")
			c.drawString(x_numero, y_detail, "Número")
			c.drawString(x_fecha, y_detail, "Fecha")
			c.drawRightString(x_importe, y_detail, "Importe Original")
			c.drawRightString(x_saldo, y_detail, "Saldo Pendiente")
			c.drawRightString(x_pago, y_detail, "Su Pago")
			c.setFont("Helvetica", 7)
			
			y_detail -= 5*mm
			for detalle in detalle_recibo:
				c.drawString(x_comprobante, y_detail, detalle.id_factura_cobrada.id_comprobante_venta.nombre_comprobante_venta)
				c.drawString(x_numero, y_detail, f"{detalle.id_factura_cobrada.letra_comprobante}  {detalle.id_factura_cobrada.numero_comprobante_formateado}")
				c.drawString(x_fecha, y_detail, detalle.id_factura_cobrada.fecha_comprobante.strftime("%d/%m/%Y"))
				c.drawRightString(x_importe, y_detail, f"${formato_argentino(detalle.id_factura_cobrada.total)}")
				saldo = detalle.id_factura_cobrada.total - (detalle.id_factura_cobrada.entrega - detalle.monto_cobrado)
				c.drawRightString(x_saldo, y_detail, f"${formato_argentino(saldo)}")
				c.drawRightString(x_pago, y_detail, f"${formato_argentino(detalle.monto_cobrado)}")
				c.drawString(x_pago + 1*mm, y_detail, "CANCELADA" if saldo == detalle.monto_cobrado else "A CUENTA")
				
				y_detail -= 4*mm
			
			y_detail -= 4*mm
		
		
		#-- Medios de Pago.
		table_cols = ["Medio de Pago", "Número", "Fecha", "Cuotas", "Importe"]
		cols_width = [70*mm, 30*mm, 15*mm, 15*mm, 25*mm]
		
		table_data = [table_cols]
		
		if recibo.efectivo_recibo:
			table_data.append(["EFECTIVO"] + 3*[""] + [f"${formato_argentino(recibo.efectivo_recibo)}"])
		
		if retenciones:
			table_data.append(["Retenciones:"] + 4*[""])
			for retencion in retenciones:
				row = [
					retencion.id_codigo_retencion,
					retencion.certificado,
					retencion.fecha_retencion.strftime("%d/%m/%Y"),
					"",
					f"${formato_argentino(retencion.importe_retencion)}"
				]
				table_data.append(row)
		
		if depositos:
			table_data.append(["Depósitos:"] + 4*[""])
			for deposito in depositos:
				cta_bco = f"{deposito.id_cuenta_banco.numero_cuenta}-{deposito.id_cuenta_banco.id_banco.nombre_banco}" if deposito.id_cuenta_banco else ""
				row = [
					cta_bco,
					"",
					deposito.fecha_deposito.strftime("%d/%m/%Y"),
					"",
					f"${formato_argentino(deposito.importe_deposito)}"
				]
				table_data.append(row)
		
		if tarjetas:
			table_data.append(["Tarjetas:"] + 4*[""])
			for tarjeta in tarjetas:
				row = [
					tarjeta.id_tarjeta,
					tarjeta.cupon,
					date.today().strftime("%d/%m/%Y"),
					tarjeta.cuotas or "",
					f"${formato_argentino(tarjeta.importe_tarjeta)}"
				]
				table_data.append(row)
		
		if cheques:
			table_data.append(["Cheques:"] + 4*[""])
			for cheque in cheques:
				row = [
					cheque.id_banco,
					cheque.numero_cheque_recibo,
					cheque.fecha_cheque1.strftime("%d/%m/%Y"),
					"",
					f"${formato_argentino(cheque.importe_cheque)}"
				]
				table_data.append(row)
		
		table = Table(table_data, colWidths=cols_width)
		
		#-- Aplica estilo a la tabla.
		table.setStyle(TableStyle([
			# ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),  # Encabezado gris claro
			# ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
			# ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
			('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
			('FONTSIZE', (0, 0), (-1, -1), 7),
			('TOPPADDING', (0,0), (-1,-1), 0),
			('BOTTOMPADDING', (0, 0), (-1, -1), 0),
			('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
			('ALIGN', (1, 0), (1, -1), 'LEFT'),
			# ('LINEABOVE', (0,0), (-1,0), 0.5, colors.black),
			('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
			('ALIGN', (1, 0), (1, -1), 'RIGHT'),
			('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
		]))
		
		#-- Determinar la posición de la tabla.
		y_detail -= 15*mm
		
		#-- Dibuja la tabla en el canvas.
		if len(table_data) > 1:
			c.drawString(x_text_left, y_detail, "Según los siguientes Medios de Pago:")
			
			y_detail -= 5*mm
			
			table.wrapOn(c, width - 2*margin, 200*mm)
			table.drawOn(c, margin, y_detail - table._height)
			y_base_tabla = y_detail - table._height  # base de la tabla
		else:
			y_base_tabla = y_detail  # si no hay tabla, usa y_detail como base		
		
		#-- Mostrar cifra en letras como párrafo.
		cifra_letras = f"Son pesos: {numero_a_letras(recibo.total).upper()}."
		letras_style = ParagraphStyle(
			'letras',
			fontName='Helvetica-Bold',
			fontSize=8,
			leading=10,
			leftIndent=0,
			rightIndent=0,
			spaceBefore=0,
			spaceAfter=0,
		)
		observ_style = ParagraphStyle(
			'observ',
			fontName='Helvetica',
			fontSize=8,
			leading=10,
			leftIndent=0,
			rightIndent=0,
			spaceBefore=0,
			spaceAfter=0,
		)
		#-- Distancia fija debajo de la tabla.
		distancia = 30*mm
		
		#-- Posición para la cifra en letras.
		y_text = y_base_tabla - distancia
		
		letras_para = Paragraph(cifra_letras, letras_style)
		w, h = letras_para.wrap(width - 2*margin - 70*mm, 30*mm)
		letras_para.drawOn(c, margin + 5*mm, y_text - h)
		
		#-- Línea para firma justo a la derecha de la cifra en letras.
		x_inicio = width - 70*mm
		x_fin = width - margin - 5*mm
		
		y_linea = y_text - h + 2  #-- Se ajusta +2 para que la línea quede alineada con la base del texto.
		
		#-- Dibuja la línea para firma y el usuario que recibe el pago.
		c.line(x_inicio, y_linea, x_fin, y_linea)
		c.drawCentredString(x_inicio+((x_fin - x_inicio)/2), y_linea-4*mm, usuario)
		
		#-- Observaciones si las tiene.
		if recibo.observa_comprobante:
			y_text -= (h + 10*mm)
			
			c.setFont("Helvetica-Bold", 8)
			c.drawString(x_text_left, y_text, "Observaciones:")
			c.setFont("Helvetica", 8)
			
			y_text -= 1*mm
			observ_para = Paragraph(recibo.observa_comprobante, observ_style)
			w, h = observ_para.wrap(width - 2*margin-10*mm, 40*mm)
			observ_para.drawOn(c, margin + 5*mm, y_text - h)
		
		
		c.showPage()
		c.save()
		
		buffer.seek(0)
		response = HttpResponse(buffer, content_type='application/pdf')
		file = f"{recibo.compro}_{recibo.letra_comprobante}_{recibo.numero_comprobante_formateado}"
		response['Content-Disposition'] = f'inline; filename="{file}.pdf"'
		return response
	
	def _generar_pdf_remito(self, remito):
		"""Se generan Remitos Sin formato para imprimir en formatos pre-impresos."""
		#-- Obtener datos principales.
		detalle_remito = DetalleFactura.objects.filter(id_factura=remito)
		
		cliente = remito.id_cliente  # No necesitas consulta adicional
		
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
		nombre_comprobante = remito.id_comprobante_venta.tipo_comprobante if remito.id_comprobante_venta.tipo_comprobante else remito.id_comprobante_venta.nombre_comprobante_venta
		c.drawString(x_datos_remito, y_position, nombre_comprobante)
		
		c.setFont("Helvetica-Bold", 10)
		y_position -= 10*mm
		c.drawString(x_datos_remito, y_position, f"{datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")}")
		
		
		#-- Datos del Cliente. -------------------------------------------------------------------------------
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
		c.drawString(x_data_left, y_position, f": {cliente.id_cliente}")
		c.setFont("Helvetica-Bold", font_size)
		c.drawRightString(x_text_right, y_position, "Ap. y Nombre/Razón Social:")
		c.setFont("Helvetica", font_size)
		
		parrafo_cliente = Paragraph(f"{cliente.nombre_cliente}", paragraph_style)
		max_width = 100*mm
		w, h = parrafo_cliente.wrap(max_width, 20*mm)
		line_height = font_size  # o paragraph_style.leading
		parrafo_cliente.drawOn(c, x_data_right, y_position - (h - line_height))
		
		y_position = y_position - h - 2
		c.setFont("Helvetica-Bold", font_size)
		c.drawString(x_text_left, y_position, "I.V.A.")
		c.setFont("Helvetica", font_size)
		c.drawString(x_data_left, y_position, f": {cliente.id_tipo_iva.nombre_iva if cliente.id_tipo_iva else ''}")
		c.setFont("Helvetica-Bold", font_size)
		c.drawRightString(x_text_right, y_position, "Domicilio:")
		c.setFont("Helvetica", font_size)
		c.drawString(x_data_right, y_position, f" {cliente.domicilio_cliente}")
		
		y_position -= 4*mm
		c.setFont("Helvetica-Bold", font_size)
		c.drawString(x_text_left, y_position, cliente.nombre_tipo_documento_identidad)
		c.setFont("Helvetica", font_size)
		c.drawString(x_data_left, y_position, f": {cliente.cuit_formateado}")
		c.setFont("Helvetica-Bold", font_size)
		c.drawRightString(x_text_right, y_position, "Localidad:")
		c.setFont("Helvetica", font_size)
		c.drawString(x_data_right, y_position, f" {cliente.id_localidad} - {cliente.id_provincia}")
		
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
				Paragraph(str(detalle.producto_venta if detalle.producto_venta else ""), style=paragraph_style_normal),
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
		y_table = height - 100*mm  # posición fija debajo del recuadro cliente
		tabla.wrapOn(c, width - 2*margin, height)
		tabla.drawOn(c, margin, y_table - tabla._height)
		
		#-- Depósito y Nro. Control. ---------
		y_position = 35*mm
		c.setFont("Helvetica", 7)
		c.drawString(x_text_left, y_position, f"Depósito: {remito.id_deposito.id_producto_deposito}")
		
		y_position -= 4*mm
		c.drawString(x_text_left, y_position, f"Control: {remito.compro_letra_numero_comprobante_formateado}")
		#-------------------------------------
		
		c.showPage()
		c.save()
		
		buffer.seek(0)
		response = HttpResponse(buffer, content_type='application/pdf')
		file = f"{remito.compro}_{remito.letra_comprobante}_{remito.numero_comprobante_formateado}"
		response['Content-Disposition'] = f'inline; filename="{file}.pdf"'
		return response

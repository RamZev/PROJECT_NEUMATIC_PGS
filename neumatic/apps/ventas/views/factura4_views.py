# neumatic\apps\ventas\views\factura_views.py
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db import transaction
from django.db.models import F
from django.db import DatabaseError
from django.utils import timezone
from django.utils.safestring import mark_safe

import json

from .msdt_views_generics import *
from ..models.factura_models import Factura
from ...maestros.models.numero_models import Numero
from ..forms.factura_forms import FacturaForm, DetalleFacturaFormSet
from ..forms.factura_forms import SerialFacturaFormSet
from ...maestros.models.base_models import ProductoStock, ComprobanteVenta, Operario
from ...maestros.models.valida_models import Valida
from ...maestros.models.cliente_models import Cliente
# OJO: es nuevo 25/08/2025
from ...maestros.models.empresa_models import Empresa
from ...maestros.models.base_models import AlicuotaIva

from entorno.constantes_base import TIPO_VENTA

modelo = Factura

#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
model_string = modelo.__name__.lower()   # Cuando el modelo es una sola palabra.

#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
#model_string = "color"

#-- Usar esta forma para personalizar el nombre de la plantilla y las vistas
model_string2 = "movimiento_interno"

formulario = FacturaForm

template_form = f"{model_string}_form.html"
home_view_name = "home"
list_view_name = f"{model_string2}_list"
create_view_name = f"{model_string2}_create"
update_view_name = f"{model_string2}_update"
delete_view_name = f"{model_string2}_delete"


# @method_decorator(login_required, name='dispatch')
class MovimientoInternoListView(MaestroDetalleListView):
	model = modelo
	template_name = f"ventas/maestro_detalle_list.html"
	context_object_name = 'objetos'
	tipo_comprobante = 'interno'  # Nuevo atributo de clase

	search_fields = [
	 'id_factura',
	 'compro',
	 'numero_comprobante',
	 'cuit',
	 'id_cliente__nombre_cliente' #separar por guión bajo doble "__"
	]

	ordering = ['-id_factura']

 	#-- Encabezado de la Tabla.
	table_headers = {
		'id_factura': (1, 'ID'),
		'compro': (1, 'Compro'),
		'letra_comprobante': (1, 'Letra'),
		'numero_comprobante': (1, 'Nro Comp'),
		'fecha_comprobante': (1, 'fecha'),
		'cuit': (1, 'CUIT'),
		'id_cliente': (3, 'Cliente'),
		'total': (2, 'Total'),
		'opciones': (1, 'Opciones'),
	}

	#-- Columnas de la Tabla.
	table_data = [
		{'field_name': 'id_factura', 'date_format': None},
		{'field_name': 'compro', 'date_format': None},
		{'field_name': 'letra_comprobante', 'date_format': None},
		{'field_name': 'numero_comprobante', 'date_format': None},
  		{'field_name': 'fecha_comprobante', 'date_format': 'd/m/Y'},
		{'field_name': 'cuit', 'date_format': None},
		{'field_name': 'id_cliente', 'date_format': None},
		{'field_name': 'total', 'date_format': None, 'decimal_places': 2},
	]

	#cadena_filtro = "Q(nombre_color__icontains=text)"
	extra_context = {
		#"master_title": model._meta.verbose_name_plural,
		"master_title": "Movimiento Interno",
		"home_view_name": home_view_name,
		"list_view_name": list_view_name,
		"create_view_name": create_view_name,
		"update_view_name": update_view_name,
		"delete_view_name": delete_view_name,
		"table_headers": table_headers,
		"table_data": table_data,
		"model_string_for_pdf": "factura",  # ¡Solución clave aquí!
		"model_string": model_string,
	}

	def get_queryset(self):
		# Obtener el queryset base
		queryset = super().get_queryset()

		# Obtener el usuario actual
		user = self.request.user

		# Si el usuario no es superusuario, filtrar por sucursal
		if not user.is_superuser:
				queryset = queryset.filter(id_sucursal=user.id_sucursal)
		
		# 2. NUEVO FILTRO: Movimento Interno
		queryset = queryset.filter(
            id_comprobante_venta__interno=True
		)

		# Aplicar búsqueda y ordenación
		query = self.request.GET.get('busqueda', None)
		if query:
				search_conditions = Q()
				for field in self.search_fields:
						search_conditions |= Q(**{f"{field}__icontains": query})
				queryset = queryset.filter(search_conditions)

		return queryset.order_by(*self.ordering)
 

	def get_context_data(self, **kwargs):
		# Obtener el contexto base
		context = super().get_context_data(**kwargs)
		
		# Agregar model_string al contexto
		context['model_string'] = model_string  # Esto devolverá 'factura'
		
		# Mantener todos los valores de extra_context
		if hasattr(self, 'extra_context'):
				context.update(self.extra_context)
				
		return context

# @method_decorator(login_required, name='dispatch')
class MovimientoInternoCreateView(MaestroDetalleCreateView):
	model = modelo
	list_view_name = list_view_name
	form_class = formulario
	template_name = f"ventas/{template_form}"
	success_url = reverse_lazy(list_view_name) # Nombre de la url.
	tipo_comprobante = 'interno'  # Nuevo atributo de clase

	#-- Indicar el permiso que requiere para ejecutar la acción:
	# Obtener el nombre de la aplicación a la que pertenece el modelo.
	app_label = model._meta.app_label
	# Indicar el permiso eN el formato: <app_name>.<permiso>_<modelo>
	permission_required = f"{app_label}.add_{model.__name__.lower()}"

	# print("Entro a la vista")

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)

		# print("Entro a get_context_data")

		# Pasar variables adicionales al contexto
		usuario = self.request.user
		data['cambia_precio_descripcion'] = usuario.cambia_precio_descripcion
		data['tipo_venta'] = TIPO_VENTA

		if self.request.POST:
			data['formset_detalle'] = DetalleFacturaFormSet(self.request.POST)
			data['formset_serial'] = SerialFacturaFormSet(self.request.POST)
		else:
			data['formset_detalle'] = DetalleFacturaFormSet(instance=self.object)
			data['formset_serial'] = SerialFacturaFormSet(instance=self.object)

		data['is_edit'] = False  # Indicar que es una edición

		# Obtener todos los comprobantes con sus valores libro_iva
		libro_iva_dict = {str(c.id_comprobante_venta): c.libro_iva for c in ComprobanteVenta.objects.all()}
		data['libro_iva_dict'] = json.dumps(libro_iva_dict)

		# Obtener todos los comprobantes con sus valores mult_venta
		mult_venta_dict = {str(c.id_comprobante_venta): c.mult_venta for c in ComprobanteVenta.objects.all()}
		data['mult_venta_dict'] = json.dumps(mult_venta_dict)

		# Obtener todos los comprobantes con sus valores electronica
		electronica_dict = {str(c.id_comprobante_venta): c.electronica for c in ComprobanteVenta.objects.all()}
		data['electronica_dict'] = json.dumps(electronica_dict)

		# Obtener todos los comprobantes con sus valores manual
		manual_dict = {str(c.id_comprobante_venta): c.manual for c in ComprobanteVenta.objects.all()}
		data['manual_dict'] = json.dumps(manual_dict)

		# Obtener todos los comprobantes con sus valores tipo_comprobante
		tipo_comprobante_dict = {str(c.id_comprobante_venta): c.tipo_comprobante for c in ComprobanteVenta.objects.all()}
		data['tipo_comprobante_dict'] = mark_safe(json.dumps(tipo_comprobante_dict, ensure_ascii=False))
		
		# Obtener todos los comprobantes con sus valores mipyme
		mipyme_dict = {str(c.id_comprobante_venta): c.mipyme for c in ComprobanteVenta.objects.all()}
		data['mipyme_dict'] = json.dumps(mipyme_dict)

		# Obtener todos los comprobantes con sus valores ncr_ndb
		ncr_ndb_dict = {str(c.id_comprobante_venta): c.ncr_ndb for c in ComprobanteVenta.objects.all()}
		data['ncr_ndb_dict'] = json.dumps(ncr_ndb_dict)

		# Obtener todos los comprobantes con sus valores remito
		remito_dict = {str(c.id_comprobante_venta): c.remito for c in ComprobanteVenta.objects.all()}
		data['remito_dict'] = json.dumps(remito_dict)

		# Obtener todos los comprobantes con sus valores compro_asociado
		compro_asociado_dict = {str(c.id_comprobante_venta): c.compro_asociado for c in ComprobanteVenta.objects.all()}
		data['compro_asociado_dict'] = json.dumps(compro_asociado_dict)
		
		# Obtener todos los comprobantes con sus valores interno
		interno_dict = {str(c.id_comprobante_venta): c.interno for c in ComprobanteVenta.objects.all()}
		data['interno_dict'] = json.dumps(interno_dict)

		# Obtener id_cliente del primer cliente con el filtro cliente_empresa=True
		first_id = Cliente.objects.filter(cliente_empresa=True).values_list('id_cliente', flat=True).first()
		data['cliente_empresa_id'] = str(first_id) if first_id is not None else ''
		
		# Obtener todos los operarios con sus id
		operario_dict = {str(o.id_operario): o.nombre_operario for o in Operario.objects.all()}
		data['operario_dict'] = json.dumps(operario_dict)

		# Tipo de Comprobante
		data['tipo_comprobante'] = self.tipo_comprobante
		
		#-- Título de la página.
		data['titulo'] = "Crear Comprobante"

		return data

	def form_valid(self, form):
		context = self.get_context_data()
		formset_detalle = context['formset_detalle']
		formset_serial = context['formset_serial']

		if not all([formset_detalle.is_valid(), formset_serial.is_valid()]):
			return self.form_invalid(form)

		try:
			with transaction.atomic():
				# 0. REGLA: Validación y actualización de datos del cliente
				cliente_obj = form.cleaned_data['id_cliente']  # Esto es un objeto Cliente
				cliente_id = cliente_obj.id_cliente  # Accede al campo id_cliente del modelo
				
				if cliente_id:
					try:
						cliente = Cliente.objects.get(id_cliente=cliente_id)
						movil_factura = form.cleaned_data.get('movil_factura', '').strip()
						email_factura = form.cleaned_data.get('email_factura', '').strip()
						
						updates = {}
						
						# Lógica para el teléfono móvil
						if movil_factura:  # Solo si se ingresó un valor en el formulario
							if not cliente.movil_cliente:
								# Caso 1: No tiene móvil registrado -> actualizar movil_cliente
								updates['movil_cliente'] = movil_factura
								form.instance.movil_factura = movil_factura
							elif cliente.movil_cliente != movil_factura:
								# Caso 2: Tiene móvil diferente -> guardar en telefono_cliente
								updates['telefono_cliente'] = movil_factura
								form.instance.movil_factura = movil_factura
						
						# Lógica para el email
						if email_factura:  # Solo si se ingresó un email en el formulario
							if not cliente.email_cliente:
								# Caso 1: No tiene email registrado -> actualizar email_cliente
								updates['email_cliente'] = email_factura
								form.instance.email_factura = email_factura
							elif cliente.email_cliente != email_factura:
								# Caso 2: Tiene email diferente -> guardar en email2_cliente
								updates['email2_cliente'] = email_factura
								form.instance.email_factura = email_factura
						
						# Aplicar actualizaciones si hay cambios
						if updates:
							Cliente.objects.filter(id_cliente=cliente_id).update(**updates)
					
					except Cliente.DoesNotExist:
						pass				
				
				# 1. Validación mínima necesaria
				deposito = form.cleaned_data.get('id_deposito')
				if not deposito:
						form.add_error('id_deposito', 'Debe seleccionar un depósito')
						return self.form_invalid(form)

				# 2. Validación para documentos pendientes
				comprobante_venta = form.cleaned_data['id_comprobante_venta']
				if comprobante_venta.pendiente:
						comprobante_remito = form.cleaned_data.get('comprobante_remito')
						remito = form.cleaned_data.get('remito')
						
						if not all([comprobante_remito, remito]):
								form.add_error(None, 'Para este tipo de comprobante debe especificar el documento asociado')
								return self.form_invalid(form)

				# 3. Numeración - Inicio  ----------------------->
				sucursal = form.cleaned_data['id_sucursal']
				punto_venta = form.cleaned_data['id_punto_venta']
				comprobante = form.cleaned_data['compro']
				fecha_comprobante = form.cleaned_data['fecha_comprobante']
				numero_plantilla = form.cleaned_data['numero_comprobante']
				print("numero_plantilla:", numero_plantilla)

				# ←←← SIMULACIÓN DE ERROR - AGREGA ESTAS LÍNEAS →→→
				# from django.core.exceptions import ValidationError
				# raise ValidationError("🚨 ERROR DE PRUEBA: Este es un mensaje de error simulado")
				# ←←← FIN DE SIMULACIÓN →→→
				
				# Determinamos id_discrimina_iva basado en el tipo de IVA (Regla: True solo si id_tipo_iva == 4)
				cliente = form.cleaned_data['id_cliente']
				id_discrimina_iva = (cliente.id_tipo_iva.discrimina_iva)
				
				# Obtener configuración AFIP del comprobante
				comprobante_data = ComprobanteVenta.objects.filter(
					codigo_comprobante_venta=comprobante
				).first()

				if not comprobante_data:
					form.add_error(None, 'No se encontró la configuración AFIP para este comprobante')
					return self.form_invalid(form)

				# Determinar el tipo de numeración basado en comprobante_data
				if comprobante_data.electronica:
					tipo_numeracion = 'electronica'
				elif not comprobante_data.electronica and comprobante_data.libro_iva:
					tipo_numeracion = 'manual'
					print("Entró")
				elif comprobante_data.remito:
					tipo_numeracion = 'automatica'
				elif comprobante_data.interno:
					tipo_numeracion = 'automatica'
				else:
					pass
					# form.add_error(None, 'Tipo de numeración no válido')
					# return self.form_invalid(form)

				# Determinar comprobante AFIP y letra
				codigo_afip_a = comprobante_data.codigo_afip_a
				codigo_afip_b = comprobante_data.codigo_afip_b

				if codigo_afip_a != codigo_afip_b:
					if id_discrimina_iva:
						comprobante_afip = codigo_afip_a
						letra = 'A'
					else:
						comprobante_afip = codigo_afip_b
						letra = 'B'
				else:
					comprobante_afip = codigo_afip_a
					# Buscar si ya existe un número para esta combinación
					numero_existente = Numero.objects.filter(
						id_sucursal=sucursal,
						id_punto_venta=punto_venta,
						comprobante=comprobante_afip
					).first()
					
					if numero_existente:
						letra = numero_existente.letra
						print("if numero_existente", letra)
					else:
						letra = "X"

				# Manejar la numeración según el tipo
				if tipo_numeracion == 'electronica':
					#------------------------------------------->
					# Facturación Electrónica
					from datetime import datetime, timedelta
					
					# Obtener token, sign y expiration
					token, sign, expiration = self.obtener_token_afiparca()

					# Datos de autenticación por defecto
					datos_auth= {
						'token': token,
						'sign': sign,
						'cuit': '30692402363'
					}

					# FeCabReq
					cant_reg = 1
					punto_venta_obj = form.cleaned_data['id_punto_venta']
					punto_venta_valor = punto_venta_obj.punto_venta
					pto_vta = f"{int(punto_venta_valor):04d}"
					cbte_tipo = comprobante_afip

					# FECAEDetRequest
					concepto = 3

					cliente_obj = form.cleaned_data['id_cliente']
					doc_tipo = cliente_obj.id_tipo_documento_identidad.ws_afip
					doc_nro = cliente_obj.cuit
					# Números que deben ser btenidos por el ws
					# Temporalmente se usa el que está en la plantilla
					cbte_desde = str(numero_plantilla)[-8:]
					cbte_hasta = cbte_desde
					
					fecha_comprobante = form.cleaned_data['fecha_comprobante']
					# Formatear fecha comprobante
					cbte_fch = fecha_comprobante.strftime('%Y%m%d')
					
					# Importes generales
					imp_total = form.cleaned_data['total']
					imp_tot_conc = form.cleaned_data['exento']
					imp_neto = form.cleaned_data['gravado']
					imp_op_ex = '0.00'
					imp_trib = '0.00'
					imp_iva = form.cleaned_data['iva']

					# Fechas de Servicio y vencimiento
					fecha_vto = fecha_comprobante + timedelta(days=30)
					fch_vto_pago = fecha_vto.strftime('%Y%m%d')
					
					# Moneda, tipo de cambio y forma de pago
					mon_id = 'PES'
					mon_cotiz = '1.000'
					can_mis_mon_ext = 'N'

					# Condición de IVA del receptor
					condicion_iva_receptor_id = cliente_obj.id_tipo_iva.codigo_afip_responsable

					# Diccionario del IVA
					# Obtener todas las alícuotas activas
					alicuotas = AlicuotaIva.objects.filter(
						estatus_alicuota_iva=True
					).values('codigo_alicuota', 'alicuota_iva')
					
					# Crear diccionario {código: porcentaje}
					diccionario_alicuotas = {}
					for alicuota in alicuotas:
						try:
							codigo = int(alicuota['codigo_alicuota'])
							diccionario_alicuotas[codigo] = alicuota['alicuota_iva']
						except (ValueError, TypeError):
							# Saltar códigos no válidos
							continue

					## print("diccionario_alicuotas", diccionario_alicuotas)
					
					# Recorrer cada alícuota del diccionario
					datos_impuestos = []
    
					# Crear diccionario de mapeo: porcentaje -> código AFIP
					mapeo_porcentaje_a_codigo = {}
					for codigo, porcentaje in diccionario_alicuotas.items():
						# Convertir Decimal a float para comparación
						mapeo_porcentaje_a_codigo[float(porcentaje)] = codigo
					
					print("Mapeo porcentaje->código:", mapeo_porcentaje_a_codigo)
					
					# Diccionario para acumular por código AFIP
					acumuladores = {}
					
					# Recorrer todos los items del detalle
					for form_detalle in formset_detalle:
						detalle_data = form_detalle.cleaned_data
						
						# Obtener valores del item
						porcentaje_iva = float(detalle_data.get('alic_iva', 0))
						gravado = float(detalle_data.get('gravado', 0) or 0)
						iva = float(detalle_data.get('iva', 0) or 0)
						
						print(f"Procesando: {porcentaje_iva}% -> gravado: {gravado}, iva: {iva}")
						
						# Encontrar el código AFIP que corresponde a este porcentaje
						codigo_afip = None
						for porcentaje, codigo in mapeo_porcentaje_a_codigo.items():
							# Comparar con tolerancia para decimales
							if abs(porcentaje - porcentaje_iva) < 0.1:
								codigo_afip = codigo
								break
						
						if codigo_afip is not None:
							if codigo_afip not in acumuladores:
								acumuladores[codigo_afip] = {'iva_base_imp': 0.0, 'iva_importe': 0.0}
							
							acumuladores[codigo_afip]['iva_base_imp'] += gravado
							acumuladores[codigo_afip]['iva_importe'] += iva
					
					# Convertir a la estructura final
					for codigo, montos in acumuladores.items():
						datos_impuestos.append({
							'iva_id': str(codigo),
							'iva_base_imp': f"{montos['iva_base_imp']:.2f}",
							'iva_importe': f"{montos['iva_importe']:.2f}"
						})
					
					print("Datos impuestos finales:", datos_impuestos)

					# Datos de cabecera del comprobante por defecto
					datos_comprobante = {
						'cant_reg': cant_reg,
						'pto_vta': pto_vta,
						'cbte_tipo': cbte_tipo,
						'concepto': concepto,
						'doc_tipo': doc_tipo,
						'doc_nro': doc_nro,
						'cbte_desde': cbte_desde,
						'cbte_hasta': cbte_hasta,
						'cbte_fch': cbte_fch,
						'imp_total': imp_total,
						'imp_tot_conc': imp_tot_conc,
						'imp_neto': imp_neto,
						'imp_op_ex': imp_op_ex,
						'imp_trib': imp_trib,
						'imp_iva': imp_iva,
						'fch_serv_desde': cbte_fch,
						'fch_serv_hasta': cbte_fch,
						'fch_vto_pago': fch_vto_pago,
						'mon_id': mon_id,
						'mon_cotiz': mon_cotiz,
						'can_mis_mon_ext': can_mis_mon_ext,
						'condicion_iva_receptor_id': condicion_iva_receptor_id
					}

					datos_cliente = {
						'nombre': 'CLIENTE GENERICO',
						'domicilio': 'DIRECCION GENERICA 123',
						'localidad': 'CIUDAD',
						'cp': '1000'
					}

					# Si no se proporcionan impuestos, usar uno por defecto
					# datos_impuestos = [{
					# 		'iva_id': '5',
					# 		'iva_base_imp': '82.64',
					# 		'iva_importe': '17.36'
					# 	}]

					# Generar el XML
					xml_content = self.generar_xml_afiparca(
						datos_auth, 
						datos_comprobante, 
						datos_cliente,
						datos_impuestos
						)

					# Guardar en archivo prueba.xml
					from pathlib import Path

					# Establecer el nombre del archivo
					
					nuevo_numero = str(numero_plantilla)[-8:]
					archivo_xml = f"{comprobante_afip}_{pto_vta}_{nuevo_numero}_Solicitud.xml"
					# print(archivo_xml)

					# === Construir ruta: neumatic/xml_afiparca/prueba.xml ===
					BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
					xml_dir = BASE_DIR / "xml_afiparca"

					# Asegurar que la carpeta exista
					xml_dir.mkdir(exist_ok=True, parents=True)  # `parents=True` por si hay subcarpetas

					xml_path = xml_dir / archivo_xml

					try:
						with open(xml_path, 'w', encoding='utf-8') as f:
							f.write(xml_content)
						print(f"✅ Archivo XML guardado en: {xml_path.resolve()}")
					except Exception as e:
						print(f"❌ Error al guardar el archivo: {e}")

					print(f"Archivo {archivo_xml} creado con éxito.")

					#------------------------------------------->
					
					# Caso auxiliar: Usar el número proporcionado por el usuario
					nuevo_numero = numero_plantilla
					
					# Actualizar el modelo Numero con este número (si es mayor al actual)
					numero_obj, created = Numero.objects.select_for_update(nowait=True).get_or_create(
						id_sucursal=sucursal,
						id_punto_venta=punto_venta,
						comprobante=comprobante_afip,
						letra=letra,
						defaults={'numero': numero_plantilla}  # Valor inicial
					)
					
					# Si ya existe, actualizar solo si el número manual es mayor
					if not created and numero_plantilla > numero_obj.numero:
						Numero.objects.filter(pk=numero_obj.pk).update(numero=numero_plantilla)
					
					# Validar que el número manual no sea menor que el actual
					elif not created and numero_plantilla <= numero_obj.numero:
						form.add_error('numero_comprobante', 
									f'Error: El número {numero_plantilla} debe ser mayor al último usado ({numero_obj.numero})')
						return self.form_invalid(form)

				elif tipo_numeracion == 'manual':
					print("tipo_numeracion**:", tipo_numeracion)
					nuevo_numero = numero_plantilla
				
				elif tipo_numeracion == 'automatica':
					print("tipo_numeracion***:", tipo_numeracion)
					# Bloquear y obtener/crear el número
					numero_obj, created = Numero.objects.select_for_update(nowait=True).get_or_create(
						id_sucursal=sucursal,
						id_punto_venta=punto_venta,
						comprobante=comprobante_afip,
						letra=letra,
						defaults={'numero': 0}
					)

					nuevo_numero = numero_obj.numero + 1
					Numero.objects.filter(pk=numero_obj.pk).update(numero=F('numero') + 1)

				# Asignar valores definicitivo
				form.instance.numero_comprobante = nuevo_numero
				form.instance.letra_comprobante = letra
				form.instance.compro = comprobante
				print("comprobante:", comprobante)
				form.instance.full_clean()
				# Final 3. Numeración (nueva versión) ----------------------->

				# Condición de Venta
				condicion_comprobante = form.cleaned_data['condicion_comprobante']
				if condicion_comprobante == 1:
					# Venta de contado
					form.instance.entrega = form.instance.total  # Asignar el total a entrega
					form.instance.estado = "C"  # Marcar como cobrado ("C")

				# Verificación de Nota de Crédito
				comprobante_venta = form.cleaned_data['id_comprobante_venta']
				if comprobante_venta.libro_iva and comprobante_venta.mult_venta < 0:
					try:
						# 1. Obtener el documento asociado
						id_comprobante_asociado = form.cleaned_data['id_comprobante_asociado']
						documento_asociado = Factura.objects.select_for_update().get(id_factura=id_comprobante_asociado)
						
						# 2. Sumar el total de la NC al campo entrega del documento asociado
						nuevo_entrega = documento_asociado.entrega + form.instance.total
						actualizaciones = {'entrega': nuevo_entrega}
						
						# 3. Verificar si se completó el pago
						if nuevo_entrega >= documento_asociado.total:
							actualizaciones['estado'] = 'C'  # Marcamos como cobrado
						
						# 4. Actualizar el documento asociado
						Factura.objects.filter(id_factura=id_comprobante_asociado).update(**actualizaciones)
						
						# 5. Cerrar la Nota de Crédito
						form.instance.entrega = form.instance.total  # Asignar el total a entrega
						form.instance.estado = "C"  # Marcar como cobrado ("C")
						
					except Factura.DoesNotExist:
						form.add_error('id_comprobante_asociado', 'El documento asociado no existe')
						return self.form_invalid(form)
					except Exception as e:
						form.add_error(None, f'Error al procesar nota de crédito: {str(e)}')
						return self.form_invalid(form)

				# 4. Guardado en el modelo Factura
				self.object = form.save()

				# 5. ACTUALIZACIÓN DEL DOCUMENTO ASOCIADO (PARTE CLAVE)
				if comprobante_venta.pendiente:
						try:
							# Buscar el documento asociado (remito) con estado NULL o vacío
							documento_asociado = Factura.objects.filter(
									Q(compro=form.cleaned_data['comprobante_remito']) &
									Q(numero_comprobante=form.cleaned_data['remito']) &
									(Q(estado="") | Q(estado__isnull=True))
							).select_for_update().first()
							
							if documento_asociado:
									# Actualización directa y eficiente
									Factura.objects.filter(pk=documento_asociado.pk).update(
											estado="F"
									)
									print(f"Documento {documento_asociado.compro}-{documento_asociado.numero_comprobante} actualizado a estado 'F'")
							else:
									print("Advertencia: No se encontró el documento asociado para actualizar")
						except Exception as e:
							print(f"Error al actualizar documento asociado: {str(e)}")
							# No hacemos return para no impedir la creación de la factura principal

				# 6. ACTUALIZACIÓN DE LA AUTORIZACIÓN (NUEVO)
				if form.cleaned_data.get('id_valida'):  # Si tiene autorización asociada
					autorizacion = form.cleaned_data['id_valida']
					Valida.objects.filter(pk=autorizacion.pk).update(
							hs=timezone.now().time(),
							estatus_valida=False,
							# fecha_uso=timezone.now().date()  # Campo adicional para auditoría
					)
					print(f"Autorización {autorizacion.id_valida} marcada como utilizada")

				# 7. Guardado en el modelo Detallefactura y DetalleSerial
				formset_detalle.instance = self.object
				detalles = formset_detalle.save()
				
				formset_serial.instance = self.object 
				formset_serial.save() 						

				# 8. Actualización de inventario
				for detalle in detalles:
					# Solo actualizamos si es producto físico (tipo_producto = "P")
					# print("entró al bucle detalles!!!")
	
					if (hasattr(detalle.id_producto, 'tipo_producto') and 
						detalle.id_producto.tipo_producto == "P" and 
						detalle.cantidad):
						
						# Actualización segura con bloqueo
						# print("mult_stock", self.object.id_comprobante_venta.mult_stock)
						
						''' Código Original Ricardo
						ProductoStock.objects.select_for_update().filter(
								id_producto=detalle.id_producto,
								id_deposito=deposito
						).update(
								#stock=F('stock') - detalle.cantidad,
								stock=F('stock') + (detalle.cantidad * self.object.id_comprobante_venta.mult_stock),
								fecha_producto_stock=fecha_comprobante
						)
						'''
						#-- Código Modificado por Leoncio (para que se active el signal).
						producto_stocks = ProductoStock.objects.select_for_update().filter(
							id_producto=detalle.id_producto,
							id_deposito=deposito
						)
						
						for producto_stock in producto_stocks:
							producto_stock.stock += (detalle.cantidad * self.object.id_comprobante_venta.mult_stock)
							producto_stock.fecha_producto_stock = fecha_comprobante
							producto_stock.save()
				
				# Mensaje de confirmación de la creación de la factura y redirección
				messages.success(self.request, f"Documento {nuevo_numero} creado correctamente")
				return redirect(self.get_success_url())

						
		except DatabaseError as e:
			messages.error(self.request, "Error de concurrencia: Intente nuevamente")
			return self.form_invalid(form)
		except Exception as e:
			messages.error(self.request, f"Error inesperado: {str(e)}")
			return self.form_invalid(form)
		
	def form_invalid(self, form):
		print("Entro a form_invalid")
		print("Errores del formulario principal:", form.errors)

		context = self.get_context_data()
		formset_detalle = context['formset_detalle']

		if formset_detalle:
			print("Errores del formset:", formset_detalle.errors)

		return super().form_invalid(form)


	def get_success_url(self):
		return reverse(list_view_name)

	def get_initial(self):
		initial = super().get_initial()
		usuario = self.request.user  # Obtener el usuario autenticado

		# Establecer valores iniciales basados en el usuario
		initial['id_sucursal'] = usuario.id_sucursal
		initial['id_punto_venta'] = usuario.id_punto_venta
		initial['cambia_precio_descripcion'] = usuario.cambia_precio_descripcion
		#initial['jerarquia'] = usuario.jerarquia

		return initial

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['tipo_comprobante'] = self.tipo_comprobante  # Pasar tipo al formulario
		kwargs['usuario'] = self.request.user  # Pasar el usuario autenticado

		return kwargs

	def obtener_token_afiparca(self):
		from afip import Afip
		from pathlib import Path

		# Obteber Datos del modelo Empresa
		empresa = Empresa.objects.first()

		if not empresa:
			raise ValueError("No se encontró configuración de empresa")
		else:
			print("se instancio empresa y tenemos el primer registro!!!")

		BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent  # Sube 4 niveles
		cert_dir = BASE_DIR / "certif"

		# Certificado (Puede estar guardado en archivos, DB, etc)
		# cert = (cert_dir / "MAASDEMO.crt").read_text()
		# key = (cert_dir / "MAASDEMO.key").read_text()

		# Certificado
		cert = empresa.ws_archivo_crt2
		# Clave privada
		key = empresa.ws_archivo_key2
		# CUIT
		tax_id = empresa.cuit
		print("CUIT de la empresa:", tax_id)

		# CUIT del certificado (Mario)
		# Es temporal porque los certificados 
		# Son de mario y no de Debona
		tax_id = 20207882950

		# Instanciamos la clase Afip con las credenciales
		afip = Afip({
			"CUIT": tax_id,
			"cert": cert,
			"key": key
		})

		# Esta URL la podes encontrar en el manual del web service
		WSDL_TEST = "https://fwshomo.afip.gov.ar/wsct/CTService?wsdl"

		# URL al archivo WSDL de produccion
		#
		# Esta URL la podes encontrar en el manual del web service
		WSDL = "https://serviciosjava.afip.gob.ar/wsct/CTService?wsdl"

		# URL del Web service de produccion
		#
		# Esta URL la podes encontrar en el manual del web service
		URL = "https://serviciosjava.afip.gob.ar/wsct/CTService"

		# URL del Web service de test
		#
		# Esta URL la podes encontrar en el manual del web service
		URL_TEST = "https://fwshomo.afip.gov.ar/wsct/CTService"

		# Seterar en true si el web service requiere usar soap v1.2
		#
		# Si no estas seguro de que necesita v1.2 proba con ambas opciones
		soapV1_2 = True

		# Nombre del web service.
		#
		# El nombre por el cual se llama al web service en ARCA.
		# Esto lo podes encontrar en el manual correspondiente.
		# Por ej. el de factura electronica se llama "wsfe", el de
		# comprobantes T se llama "wsct"
		# servicio = "wsct"
		servicio = "wsfe"

		# A partir de aca ya no debes cambiar ninguna variable

		# Preparamos las opciones para el web service
		options = {
		"WSDL": WSDL,
		"WSDL_TEST": WSDL_TEST,
		"URL": URL,
		"URL_TEST": URL_TEST,
		"soapV1_2": soapV1_2
		}

		# Consumimos el web service con el objeto sfip
		genericWebService = afip.webService(servicio, options)

		# Obtenemos el Token Authorizataion
		ta = genericWebService.getTokenAuthorization()
		
		print('token', ta['token'])
		print('sign', ta['sign'])
		print('expiration', ta['expiration'])

		token = ta['token']
		sign = ta['sign']
		expiration = ta['expiration']

		return token, sign, expiration

	def generar_xml_afiparca(self, auth, comprobante, cliente, impuestos):
		from xml.etree.ElementTree import Element, SubElement, tostring
		from xml.dom import minidom

		# Namespaces
		SOAP_ENV = "http://schemas.xmlsoap.org/soap/envelope/"
		FE_NS = "http://ar.gov.afip.dif.FEV1/"

		# === Envelope con namespaces correctos ===
		envelope = Element(f"{{{SOAP_ENV}}}Envelope")
		envelope.set("xmlns:soap", SOAP_ENV)
		envelope.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
		envelope.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
		envelope.set("soap:encodingStyle", SOAP_ENV + "encoding/")

		# Header
		header = SubElement(envelope, "soap:Header")

		# Body
		body = SubElement(envelope, "soap:Body")

		# FECAESolicitar (con namespace correcto)
		fe_cae_solicitar = SubElement(body, "FECAESolicitar")
		fe_cae_solicitar.set("xmlns", FE_NS)  # Así se pone el xmlns en el elemento

		# === Auth ===
		auth_node = SubElement(fe_cae_solicitar, "Auth")
		SubElement(auth_node, "Token").text = auth['token']
		SubElement(auth_node, "Sign").text = auth['sign']
		SubElement(auth_node, "Cuit").text = auth['cuit']

		# === FeCAEReq ===
		fe_cae_req = SubElement(fe_cae_solicitar, "FeCAEReq")

		# FeCabReq
		cab = SubElement(fe_cae_req, "FeCabReq")
		SubElement(cab, "CantReg").text = str(comprobante.get('cant_reg', '1'))
		SubElement(cab, "PtoVta").text = str(comprobante.get('pto_vta', '0001'))
		SubElement(cab, "CbteTipo").text = str(comprobante.get('cbte_tipo', '001'))

		# FeDetReq
		det_req = SubElement(fe_cae_req, "FeDetReq")
		det = SubElement(det_req, "FECAEDetRequest")

		# Campos directos
		fields = {
			'Concepto': 'concepto',
			'DocTipo': 'doc_tipo',
			'DocNro': 'doc_nro',
			'CbteDesde': 'cbte_desde',
			'CbteHasta': 'cbte_hasta',
			'CbteFch': 'cbte_fch',
			'ImpTotal': 'imp_total',
			'ImpTotConc': 'imp_tot_conc',
			'ImpNeto': 'imp_neto',
			'ImpOpEx': 'imp_op_ex',
			'ImpTrib': 'imp_trib',
			'ImpIVA': 'imp_iva',
			'FchServDesde': 'fch_serv_desde',
			'FchServHasta': 'fch_serv_hasta',
			'FchVtoPago': 'fch_vto_pago',
			'MonId': 'mon_id',
			'MonCotiz': 'mon_cotiz',
			'CanMisMonExt': 'can_mis_mon_ext',
			'CondicionIVAReceptorId': 'condicion_iva_receptor_id',
		}
		for tag, key in fields.items():
			SubElement(det, tag).text = str(comprobante.get(key, '0.00' if 'Imp' in key else ''))

		# IVA - Usamos tus claves tal cual
		iva_node = SubElement(det, "Iva")
		if impuestos:
			for imp in impuestos:
				alic = SubElement(iva_node, "AlicIva")
				SubElement(alic, "Id").text = str(imp.get('iva_id', '0'))
				SubElement(alic, "BaseImp").text = str(imp.get('iva_base_imp', '0.00'))
				SubElement(alic, "Importe").text = str(imp.get('iva_importe', '0.00'))
		# Si no hay impuestos, AFIP espera <Iva></Iva> o <Iva/>, ya está cubierto

		# === Pretty print ===
		raw = tostring(envelope, encoding='utf-8')
		parsed = minidom.parseString(raw)
		return '\n'.join([line for line in parsed.toprettyxml(indent="    ").splitlines() if line.strip()])	

# @method_decorator(login_required, name='dispatch')
class MovimientoInternoUpdateView(MaestroDetalleUpdateView):
	model = modelo
	list_view_name = list_view_name
	form_class = formulario
	template_name = f"ventas/{template_form}"
	success_url = reverse_lazy(list_view_name) # Nombre de la url.
	tipo_comprobante = 'interno'  # Nuevo atributo de clase

	#-- Indicar el permiso que requiere para ejecutar la acción:
	# Obtener el nombre de la aplicación a la que pertenece el modelo.
	app_label = model._meta.app_label
	# Indicar el permiso eN el formato: <app_name>.<permiso>_<modelo>
	permission_required = f"{app_label}.change_{model.__name__.lower()}"

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		usuario = self.request.user
		data['cambia_precio_descripcion'] = usuario.cambia_precio_descripcion
		data['tipo_venta'] = TIPO_VENTA
		# data['tipo_doc_ident'] = TipoDocumentoIdentidad.objects.filter(estatus_tipo_documento=True)

		if self.request.POST:
			data['formset_detalle'] = DetalleFacturaFormSet(self.request.POST, instance=self.object)
			data['formset_serial'] = SerialFacturaFormSet(self.request.POST, instance=self.object)
		else:
			data['formset_detalle'] = DetalleFacturaFormSet(instance=self.object)
			data['formset_serial'] = SerialFacturaFormSet(instance=self.object)

		data['is_edit'] = True  # Indicar que es una edición

		# Obtener todos los comprobantes con sus valores libro_iva
		libro_iva_dict = {str(c.id_comprobante_venta): c.libro_iva for c in ComprobanteVenta.objects.all()}
		data['libro_iva_dict'] = json.dumps(libro_iva_dict)

		# Obtener todos los comprobantes con sus valores mult_venta
		mult_venta_dict = {str(c.id_comprobante_venta): c.mult_venta for c in ComprobanteVenta.objects.all()}
		data['mult_venta_dict'] = json.dumps(mult_venta_dict)

		# Obtener todos los comprobantes con sus valores electronica
		electronica_dict = {str(c.id_comprobante_venta): c.electronica for c in ComprobanteVenta.objects.all()}
		data['electronica_dict'] = json.dumps(electronica_dict)

		# Obtener todos los comprobantes con sus valores manual
		manual_dict = {str(c.id_comprobante_venta): c.manual for c in ComprobanteVenta.objects.all()}
		data['manual_dict'] = json.dumps(manual_dict)

		# Obtener todos los comprobantes con sus valores tipo_comprobante
		tipo_comprobante_dict = {str(c.id_comprobante_venta): c.tipo_comprobante for c in ComprobanteVenta.objects.all()}
		data['tipo_comprobante_dict'] = mark_safe(json.dumps(tipo_comprobante_dict, ensure_ascii=False))
		
		# Obtener todos los comprobantes con sus valores mipyme
		mipyme_dict = {str(c.id_comprobante_venta): c.mipyme for c in ComprobanteVenta.objects.all()}
		data['mipyme_dict'] = json.dumps(mipyme_dict)

		# Obtener todos los comprobantes con sus valores ncr_ndb
		ncr_ndb_dict = {str(c.id_comprobante_venta): c.ncr_ndb for c in ComprobanteVenta.objects.all()}
		data['ncr_ndb_dict'] = json.dumps(ncr_ndb_dict)

		# Obtener todos los comprobantes con sus valores remito
		remito_dict = {str(c.id_comprobante_venta): c.remito for c in ComprobanteVenta.objects.all()}
		data['remito_dict'] = json.dumps(remito_dict)

		# Obtener todos los comprobantes con sus valores compro_asociado
		compro_asociado_dict = {str(c.id_comprobante_venta): c.compro_asociado for c in ComprobanteVenta.objects.all()}
		data['compro_asociado_dict'] = json.dumps(compro_asociado_dict)
		
		# Obtener todos los comprobantes con sus valores interno
		interno_dict = {str(c.id_comprobante_venta): c.interno for c in ComprobanteVenta.objects.all()}
		data['interno_dict'] = json.dumps(interno_dict)

		# Obtener id_cliente del primer cliente con el filtro cliente_empresa=True
		first_id = Cliente.objects.filter(cliente_empresa=True).values_list('id_cliente', flat=True).first()
		data['cliente_empresa_id'] = str(first_id) if first_id is not None else ''
		
		# Obtener todos los operarios con sus id
		operario_dict = {str(o.id_operario): o.nombre_operario for o in Operario.objects.all()}
		data['operario_dict'] = json.dumps(operario_dict)

		# Tipo de Comprobante
		data['tipo_comprobante'] = self.tipo_comprobante
		
		#-- Título de la página.
		data['titulo'] = "Ver Comprobante"
		
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		formset_detalle = context['formset_detalle']
		formset_serial = context['formset_serial']

		if formset_detalle.is_valid():
			try:
				with transaction.atomic():
					self.object = form.save()
					formset_detalle.instance = self.object
					formset_detalle.save()

				messages.success(self.request, "El Documento se ha actualizado correctamente.")
				return super().form_valid(form)
			except Exception as e:
				messages.error(self.request, f"Error al actualizar la factura: {str(e)}")
				return self.form_invalid(form)
		else:
			messages.error(self.request, "Error en el detalle de la factura. Revise los datos.")
			return self.form_invalid(form)

	def form_invalid(self, form):
		print("Entro a form_invalid")
		print("Errores del formulario principal:", form.errors)

		context = self.get_context_data()
		formset_detalle = context['formset_detalle']

		if formset_detalle:
			print("Errores del formset:", formset_detalle.errors)

		return super().form_invalid(form)

	def get_success_url(self):
		return self.success_url

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['tipo_comprobante'] = self.tipo_comprobante  # Pasar tipo al formulario
		kwargs['usuario'] = self.request.user  # Pasar el usuario autenticado

		return kwargs


# @method_decorator(login_required, name='dispatch')
class MovimientoInternoDeleteView(MaestroDetalleDeleteView):
	model = modelo
	list_view_name = list_view_name
	template_name = "base_confirm_delete.html"
	success_url = reverse_lazy(list_view_name) # Nombre de la url.

	#-- Indicar el permiso que requiere para ejecutar la acción:
	# Obtener el nombre de la aplicación a la que pertenece el modelo.
	app_label = model._meta.app_label
	# Indicar el permiso en el formato: <app_name>.<permiso>_<modelo>
	permission_required = f"{app_label}.delete_{model.__name__.lower()}"

	extra_context = {
		"accion": f"Eliminar {model._meta.verbose_name}",
		"list_view_name" : list_view_name,
		"mensaje": "Estás seguro que deseas eliminar el Registro"
	}

	# Sobrescritura del método Post
	def post(self, request, *args, **kwargs):
		"""
		Sobrescribe el método post para añadir validación específica
		sin afectar el flujo general de otras vistas
		"""
		self.object = self.get_object()
		
		# Validación exclusiva para Factura (no afecta otros modelos)
		if hasattr(self.object, 'id_comprobante_venta') and self.object.id_comprobante_venta.electronica:
			messages.error(
				request,
				f"No se puede eliminar {self.object}: Comprobante electrónico",
				extra_tags='modal_error'  # Etiqueta para identificación en JS
			)
			return redirect(self.success_url)
			
		# Comportamiento normal para otros casos
		try:
			with transaction.atomic():
				return super().post(request, *args, **kwargs)
				
		except ProtectedError:
			messages.error(request, "No se puede eliminar (existen relaciones asociadas)")
			return redirect(self.success_url)
			
		except Exception as e:
			messages.error(request, f"Error inesperado: {str(e)}")
			return redirect(self.success_url)

# ------------------------------------------------------------------------------

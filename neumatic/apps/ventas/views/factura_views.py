# neumatic\apps\ventas\views\factura_views.py
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db import transaction
from django.db.models import F
from django.db import DatabaseError
from django.utils import timezone
from django.utils.safestring import mark_safe

from datetime import datetime, timedelta
import time

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
from apps.ventas.models.caja_models import Caja, CajaDetalle
from ...maestros.models.descuento_vendedor_models import DescuentoRevendedor

from entorno.constantes_base import TIPO_VENTA

from services.fe_arca import FacturadorARCA

modelo = Factura

#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
model_string = modelo.__name__.lower()   # Cuando el modelo es una sola palabra.

#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
#model_string = "color"

formulario = FacturaForm

template_form = f"{model_string}_form.html"
home_view_name = "home"
list_view_name = f"{model_string}_list"
create_view_name = f"{model_string}_create"
update_view_name = f"{model_string}_update"
delete_view_name = f"{model_string}_delete"

# @method_decorator(login_required, name='dispatch')
class FacturaListView(MaestroDetalleListView):
	model = modelo
	template_name = f"ventas/maestro_detalle_list.html"
	context_object_name = 'objetos'
	tipo_comprobante = 'electronico'  # Nuevo atributo de clase

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
		# 'numero_comprobante_formateado': (1, 'Nro Comp'),
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
		# {'field_name': 'numero_comprobante_formateado', 'date_format': None},
  		{'field_name': 'fecha_comprobante', 'date_format': 'd/m/Y'},
		{'field_name': 'cuit', 'date_format': None},
		{'field_name': 'id_cliente', 'date_format': None},
		{'field_name': 'total', 'date_format': None, 'decimal_places': 2},
	]

	#cadena_filtro = "Q(nombre_color__icontains=text)"
	extra_context = {
		#"master_title": model._meta.verbose_name_plural,
		"master_title": "Comprobantes Electrónicos",
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
		# if not user.is_superuser:
		if not (user.is_superuser or user.jerarquia == "A"):
				queryset = queryset.filter(id_sucursal=user.id_sucursal)
		
		# 2. NUEVO FILTRO: Comprobantes electrónicos o remitos
		queryset = queryset.filter(
			Q(id_comprobante_venta__electronica=True) |
			Q(id_comprobante_venta__remito=True),
			id_comprobante_venta__recibo=False,
			id_comprobante_venta__presupuesto=False
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

		# =========================================================
		# ALERTA DE CAJA - Solo para FacturaListView
		# =========================================================
		try:
			from datetime import date
			from apps.ventas.models.caja_models import Caja
			
			usuario = self.request.user
			
			fecha_actual = date.today()
			
			# Solo validar si el usuario tiene sucursal asignada
			if usuario.id_sucursal:
				# Verificar si existe caja para hoy
				caja_hoy = Caja.objects.filter(
					id_sucursal=usuario.id_sucursal,
					fecha_caja=fecha_actual
				).first()
				
				if not caja_hoy:
					context['alerta_vista'] = {
						'tipo': 'error',
						'titulo': '⚠️ No hay caja disponible',
						'mensaje': f'No existe caja para la sucursal y fecha {fecha_actual.strftime("%d/%m/%Y")}.',
						'accion': 'Debe crear una caja antes de generar comprobantes.'
					}
				elif caja_hoy.caja_cerrada:
					context['alerta_vista'] = {
						'tipo': 'error',
						'titulo': '⚠️ Caja cerrada',
						'mensaje': f'La caja de la sucursal para fecha {fecha_actual.strftime("%d/%m/%Y")} se encuentra CERRADA.',
						'accion': 'Debe abrir la caja antes de generar comprobantes.'
					}

				else:
					print("✅ CASO: Caja OK - No se crea alerta")
			else:
				print("⚠️ Usuario sin sucursal asignada")
				
		except Exception as e:
			import traceback
			traceback.print_exc()
		
		if 'alerta_vista' in context:
			print(f"📤 Contenido de alerta_vista: {context['alerta_vista']}")
		# =========================================================
		
		# Mantener todos los valores de extra_context
		if hasattr(self, 'extra_context'):
				context.update(self.extra_context)
				
		return context

# @method_decorator(login_required, name='dispatch')
class FacturaCreateView(MaestroDetalleCreateView):
	model = modelo
	list_view_name = list_view_name
	form_class = formulario
	template_name = f"ventas/{template_form}"
	success_url = reverse_lazy(list_view_name) # Nombre de la url.
	tipo_comprobante = 'electronico'  # Nuevo atributo de clase

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

		# Obtener los descuentos de revendedor
		descuento_revendedor_dict = {}
		descuentos = DescuentoRevendedor.objects.filter(estatus_descuento_revendedor=True)

		for desc in descuentos:
			# Crear una clave compuesta "marca_id-familia_id" para búsqueda rápida
			key = f"{desc.id_marca_id}-{desc.id_familia_id}"
			descuento_revendedor_dict[key] = float(desc.descuento)

		data['descuento_revendedor_dict'] = json.dumps(descuento_revendedor_dict)

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

				# =========================================================
				# VALIDACIÓN DE CAJA ABIERTA PARA COMPROBANTES CON MULT_CAJA ≠ 0
				# =========================================================
				comprobante_venta = form.cleaned_data['id_comprobante_venta']

				if comprobante_venta.mult_caja != 0:
					sucursal = form.cleaned_data['id_sucursal']
					fecha_comprobante = form.cleaned_data['fecha_comprobante']
					
					# 1. Verificar si existe una caja para esta sucursal y fecha (abierta o cerrada)
					caja = Caja.objects.filter(
						id_sucursal=sucursal,
						fecha_caja=fecha_comprobante
					).first()
					
					# 2. Validar existencia de caja
					if not caja:
						messages.error(
							self.request,
							f"❌ No existe caja para la sucursal '{sucursal}' y fecha {fecha_comprobante.strftime('%d/%m/%Y')}. "
							f"Debe crear una caja antes de generar este comprobante."
						)
						return redirect(self.list_view_name)  # Redirige a la lista
					
					# 3. Validar si la caja está abierta
					if caja.caja_cerrada:
						messages.error(
							self.request,
							f"❌ La caja de la sucursal '{sucursal}' para la fecha {fecha_comprobante.strftime('%d/%m/%Y')} "
							f"se encuentra CERRADA. Debe abrir la caja antes de generar este comprobante."
						)
						return redirect(self.list_view_name)  # Redirige a la lista
					
					# 4. Si pasó ambas validaciones, la caja existe y está abierta
					# (El código continúa normalmente)
				# =========================================================

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
					print("tipo_numeracion = 'electronica'")
				elif comprobante_data.manual:
					tipo_numeracion = 'manual'
					print("tipo_numeracion = 'manual'")
				else:
					tipo_numeracion = 'automatica'
					print("tipo_numeracion = 'automatica'")
									
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
				# ============================================
				# BLOQUE PARA COMPROBANTES ELECTRÓNICOS
				# ============================================
				if tipo_numeracion == 'electronica':
					#------------------------------------------->
				

					from datetime import datetime, timedelta
					from pathlib import Path
					import time
					
					# Obtener token y sign
					token, sign, expiration = self.obtener_token_afiparca()

					# Obtener empresa
					empresa = Empresa.objects.first()
					
					# FeCabReq
					cant_reg = 1
					punto_venta_obj = form.cleaned_data['id_punto_venta']
					punto_venta_valor = punto_venta_obj.punto_venta
					punto_venta_entero = int(punto_venta_valor)
					
					pto_vta = f"{punto_venta_entero:04d}"
					# cbte_tipo = comprobante_afip
					cbte_tipo = f"{int(comprobante_afip):03d}"

					# Crear facturador
					arca = FacturadorARCA(empresa=empresa)
					
					# ============================================
					# 1. OBTENER EL NÚMERO DE ARCA
					# ============================================
					cae_obtenido = False
					for intento in range(4):
						if intento > 0:
							print(f"🔄 Reintento #{intento + 1} por error 10016")
						
						# Obtener el próximo número de ARCA
						proximo_numero, ultimo_numero = arca.obtener_proximo_numero(
							punto_venta_entero,
							int(cbte_tipo), 
							token, 
							sign, 
							empresa.cuit
						)
						
						# ============================================
						# 2. MOSTRAR EL NÚMERO ASIGNADO POR ARCA
						# ============================================
						print("=" * 60)
						print("📊 NÚMERO ASIGNADO POR ARCA")
						print(f"   Tipo de comprobante: {cbte_tipo}")
						print(f"   Punto de venta: {punto_venta_entero}")
						print(f"   Número ARCA: {proximo_numero}")
						print("=" * 60)
						
						# Formar el número de comprobante (10 dígitos)
						pv_2d = f"{punto_venta_entero:02d}"
						num_8d = f"{proximo_numero:08d}"
						nuevo_numero = f"{pv_2d}{num_8d}"
						
						print(f"✅ Número formado para el documento: {nuevo_numero}")
						
						# ===== PARA EL XML DE ARCA, USAR NÚMERO COMO ENTERO =====
						cbte_desde = str(proximo_numero)
						cbte_hasta = cbte_desde
						
						# FECAEDetRequest
						concepto = 3
						cliente_obj = form.cleaned_data['id_cliente']
						doc_tipo = cliente_obj.id_tipo_documento_identidad.ws_afip
						doc_nro = cliente_obj.cuit
						
						fecha_comprobante = form.cleaned_data['fecha_comprobante']
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

						# ============================================
						# CÁLCULO DE IMPUESTOS (IVA)
						# ============================================
						alicuotas = AlicuotaIva.objects.filter(
							estatus_alicuota_iva=True
						).values('codigo_alicuota', 'alicuota_iva')
						
						diccionario_alicuotas = {}
						for alicuota in alicuotas:
							try:
								codigo = int(alicuota['codigo_alicuota'])
								diccionario_alicuotas[codigo] = alicuota['alicuota_iva']
							except (ValueError, TypeError):
								continue

						mapeo_porcentaje_a_codigo = {}
						for codigo, porcentaje in diccionario_alicuotas.items():
							mapeo_porcentaje_a_codigo[float(porcentaje)] = codigo
						
						acumuladores = {}
						
						for form_detalle in formset_detalle:
							detalle_data = form_detalle.cleaned_data
							porcentaje_iva = float(detalle_data.get('alic_iva', 0))
							gravado = float(detalle_data.get('gravado', 0) or 0)
							iva = float(detalle_data.get('iva', 0) or 0)
							
							codigo_afip = None
							for porcentaje, codigo in mapeo_porcentaje_a_codigo.items():
								if abs(porcentaje - porcentaje_iva) < 0.1:
									codigo_afip = codigo
									break
							
							if codigo_afip is not None:
								if codigo_afip not in acumuladores:
									acumuladores[codigo_afip] = {'iva_base_imp': 0.0, 'iva_importe': 0.0}
								acumuladores[codigo_afip]['iva_base_imp'] += gravado
								acumuladores[codigo_afip]['iva_importe'] += iva
						
						datos_impuestos = []
						for codigo, montos in acumuladores.items():
							datos_impuestos.append({
								'iva_id': str(codigo),
								'iva_base_imp': f"{montos['iva_base_imp']:.2f}",
								'iva_importe': f"{montos['iva_importe']:.2f}"
							})

						# ============================================
						# VERIFICAR COHERENCIA DE VALORES
						# ============================================
						total_gravado_calc = sum(float(item['iva_base_imp']) for item in datos_impuestos)
						total_iva_calc = sum(float(item['iva_importe']) for item in datos_impuestos)
						imp_tot_conc_float = float(imp_tot_conc)
						
						imp_neto = total_gravado_calc
						imp_iva = total_iva_calc
						imp_total = imp_neto + imp_iva + imp_tot_conc_float
						
						print(f"✅ Valores recalculados - Neto: {imp_neto:.2f}, IVA: {imp_iva:.2f}, Total: {imp_total:.2f}")

						# Datos de cabecera del comprobante
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

						# Datos del cliente
						datos_cliente = {
							'nombre': cliente_obj.nombre_cliente or cliente_obj.nombre_fantasia or 'CLIENTE GENERICO',
							'domicilio': cliente_obj.domicilio_cliente or 'DIRECCION GENERICA 123',
							'localidad': cliente_obj.id_localidad.nombre_localidad if cliente_obj.id_localidad else 'CIUDAD',
							'cp': cliente_obj.codigo_postal or '1000'
						}

						################
						# ============================================
						# OBTENER COMPROBANTE ASOCIADO PARA NC/ND
						# ============================================
						comprobante_asociado_data = None
						cbte_tipo_nc = int(comprobante_afip)

						# =========================================================
						# 🔍 DEBUG: VER TODOS LOS DATOS DEL FORMULARIO
						# =========================================================
						print("=" * 60)
						print("#" * 60)
						print("🔍 DEBUG - CONTENIDO DE form.cleaned_data")
						print("=" * 60)
						for key, value in form.cleaned_data.items():
							print(f"   {key}: {value}")
						print("=" * 60)

						# 🔍 DEBUG ESPECÍFICO PARA id_comprobante_asociado
						print(f"🔍 form.cleaned_data.get('id_comprobante_asociado'): {form.cleaned_data.get('id_comprobante_asociado')}")
						print(f"🔍 form.cleaned_data.get('id_id_comprobante_asociado'): {form.cleaned_data.get('id_id_comprobante_asociado')}")
						print("#" * 60)
						print("=" * 60)
						# =========================================================
						

						if cbte_tipo_nc in [2, 3]:  # Nota de Crédito (3) o Nota de Débito (2)
							id_comprobante_asociado = form.cleaned_data.get('id_comprobante_asociado')
							
							if id_comprobante_asociado:
								try:
									factura_asociada = Factura.objects.get(id_factura=id_comprobante_asociado)
									
									nro_completo = int(factura_asociada.numero_comprobante)  # 2100000032
									
									# ✅ NUEVO CÓDIGO
									# Extraer punto de venta (primeros 2 dígitos) y formatear a 4 dígitos
									pto_vta_asoc = f"{int(str(nro_completo)[:2]):04d}"  # "0021"
									
									# Extraer número secuencial (últimos 8 dígitos) y formatear a 8 dígitos
									nro_secuencial = int(str(nro_completo)[2:])  # 32
									nro_asoc = f"{nro_secuencial:08d}"  # "00000032"
									
									# Obtener código AFIP del comprobante asociado
									comprobante_asociado_obj = factura_asociada.id_comprobante_venta
									
									codigo_afip_a_asoc = comprobante_asociado_obj.codigo_afip_a
									codigo_afip_b_asoc = comprobante_asociado_obj.codigo_afip_b
									
									cliente_asociado = factura_asociada.id_cliente
									id_discrimina_iva_asoc = cliente_asociado.id_tipo_iva.discrimina_iva
									
									if codigo_afip_a_asoc != codigo_afip_b_asoc:
										if id_discrimina_iva_asoc:
											comprobante_asociado_codigo = codigo_afip_a_asoc
										else:
											comprobante_asociado_codigo = codigo_afip_b_asoc
									else:
										comprobante_asociado_codigo = codigo_afip_a_asoc
									
									# Obtener CUIT de la empresa
									empresa = Empresa.objects.first()
									cuit_empresa = str(empresa.cuit) if empresa else "30692402363"
									
									comprobante_asociado_data = {
										'tipo': str(comprobante_asociado_codigo),  # "001"
										'pto_vta': pto_vta_asoc,                   # "0021"
										'nro': nro_asoc,                           # "00000032"
										'cuit': cuit_empresa,                      # "30692402363"
										'fecha': factura_asociada.fecha_comprobante.strftime('%Y%m%d')  # "20260623"
									}
									
									print(f"✅ Comprobante asociado: {comprobante_asociado_data}")
									
								except Factura.DoesNotExist:
									print(f"⚠️ Factura no encontrada: {id_comprobante_asociado}")
									form.add_error('id_comprobante_asociado', 'El comprobante asociado no existe')
									return self.form_invalid(form)
							else:
								print("⚠️ No hay comprobante asociado para NC/ND")
								form.add_error('id_comprobante_asociado', 'Debe seleccionar un comprobante asociado')
								return self.form_invalid(form)
							
						# =========================================================
						# 🔍 PRINT DE DEPURACIÓN - AGREGAR AQUÍ
						# =========================================================
						print(f"🔍 VALOR DE comprobante_asociado_data: {comprobante_asociado_data}")
						print(f"🔍 cbte_tipo_nc: {cbte_tipo_nc}")
						print(f"🔍 ¿Es NC/ND? {cbte_tipo_nc in [2, 3]}")
						# =========================================================
						################

						# Generar el XML
						xml_content = self.generar_xml_afiparca(
							auth={
								'token': token,
								'sign': sign,
								'cuit': str(empresa.cuit)
							},
							comprobante=datos_comprobante,
							cliente=datos_cliente,
							impuestos=datos_impuestos,
							comprobante_asociado=comprobante_asociado_data 
						)

						# ============================================
						# ENVIAR SOLICITUD DE CAE A ARCA
						# ============================================
						print(f"\n🚀 ENVIANDO SOLICITUD DE CAE A ARCA ({arca.entorno.upper()})...")
						respuesta = arca.enviar_solicitud_cae(xml_content)
						print(f"✅ Respuesta recibida")
						
						# Procesar respuesta usando el método de arca
						resultado = arca.procesar_respuesta_cae(respuesta)
						
						# ============================================
						# GUARDAR XML DE RESPUESTA
						# ============================================
						BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
						xml_dir = BASE_DIR / "xml_afiparca"
						xml_dir.mkdir(exist_ok=True, parents=True)

						# Guardar XML de solicitud
						archivo_xml = f"{cbte_tipo}_{pto_vta}_{proximo_numero:08d}_Solicitud.xml"
						xml_path = xml_dir / archivo_xml
						
						with open(xml_path, 'w', encoding='utf-8') as f:
							f.write(xml_content)
						print(f"✅ XML Solicitud guardado en: {xml_path.resolve()}")
						
						# Guardar XML de respuesta formateado
						archivo_respuesta = xml_dir / f"{cbte_tipo}_{pto_vta}_{proximo_numero:08d}_Respuesta.xml"
						with open(archivo_respuesta, 'w', encoding='utf-8') as f:
							f.write(arca.formatear_xml(respuesta))
						print(f"✅ XML Respuesta guardado en: {archivo_respuesta}")
						
						# ============================================
						# VERIFICAR RESULTADO Y ACTUALIZAR CAMPOS
						# ============================================
						if resultado['aprobado']:
							print("=" * 60)
							print("✅ COMPROBANTE APROBADO POR ARCA")
							print(f"   CAE: {resultado['cae']}")
							print(f"   Vencimiento: {resultado['vencimiento']}")
							print(f"   Número asignado: {nuevo_numero}")
							print("=" * 60)

							# ===== ASIGNAR VALORES AL MODELO FACTURA =====
							form.instance.numero_comprobante = nuevo_numero
							form.instance.cae = int(resultado['cae'])
							form.instance.cae_vto = datetime.strptime(resultado['vencimiento'], '%Y%m%d').date()

														# =========================================================
							# ACTUALIZAR MODELO NUMERO (CORREGIDO)
							# =========================================================
							try:
								numero_obj, created = Numero.objects.select_for_update(nowait=True).get_or_create(
									id_sucursal=sucursal,
									id_punto_venta=punto_venta,
									comprobante=comprobante_afip,
									letra=letra,
									defaults={
										'numero': int(nuevo_numero),  # ← Guardar 2100000028
										'lineas': 1,
										'copias': 1
									}
								)

								if created:
									print(f"✅ Nuevo registro en Numero: {comprobante_afip}-{letra} = {nuevo_numero}")
								else:
									# ✅ AHORA GUARDA EL NÚMERO COMPLETO
									Numero.objects.filter(pk=numero_obj.pk).update(numero=int(nuevo_numero))
									print(f"✅ Numero actualizado: {comprobante_afip}-{letra} = {nuevo_numero}")

							except Exception as e:
								print(f"⚠️ Error al actualizar Numero: {str(e)}")

							# =========================================================
							# MOSTRAR EVENTOS/OBSERVACIONES DE ARCA
							# =========================================================
							if resultado['eventos']:
								print("\n📢 Eventos/Observaciones de ARCA:")
								for evento in resultado['eventos']:
									print(f"   • {evento}")

							cae_obtenido = True
							break  # Salir del bucle de reintentos
												
						# ============================================
						# 4. MANEJO DE ERRORES DE ARCA
						# ============================================
						# Si hay error 10016, reintentar
						if any("10016" in error for error in resultado.get('errores', [])):
							print(f"⚠️ Error 10016 detectado, reintentando...")
							if intento < 3:
								espera = 0.5 * (intento + 1)
								print(f"⏳ Esperando {espera}s...")
								time.sleep(espera)
								continue
						
						# Otros errores - mostrar y salir
						print("\n" + "=" * 60)
						print("❌ ERRORES DE ARCA:")
						print("=" * 60)
						for error in resultado.get('errores', []):
							print(f"   • {error}")
							form.add_error(None, f"Error ARCA: {error}")
						
						# Si no hay errores en la lista, mostrar el resultado completo
						if not resultado.get('errores'):
							print(f"   • Resultado completo: {resultado}")
							form.add_error(None, f"Error ARCA sin detalle: {resultado}")
						
						# Guardar archivo de error para debug
						archivo_error = xml_dir / f"{cbte_tipo}_{pto_vta}_{proximo_numero:08d}_ERROR.txt"
						with open(archivo_error, 'w', encoding='utf-8') as f:
							f.write("RESPUESTA COMPLETA:\n")
							f.write(f"  aprobado: {resultado.get('aprobado')}\n")
							f.write(f"  errores: {resultado.get('errores', [])}\n")
							f.write(f"  cae: {resultado.get('cae')}\n")
							f.write(f"  vencimiento: {resultado.get('vencimiento')}\n")
							f.write(f"  eventos: {resultado.get('eventos', [])}\n")
							f.write(f"\nRESPUESTA XML:\n{respuesta}\n")
						print(f"📄 Error guardado en: {archivo_error}")
						
						return self.form_invalid(form)
					
					# ===== FIN BUCLE DE REINTENTOS =====
					
					if not cae_obtenido:
						print("=" * 60)
						print("❌ ERROR: No se pudo obtener CAE después de 4 intentos")
						print("=" * 60)
						form.add_error(None, "No se pudo obtener CAE después de 4 intentos")
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

				# Asignar valores definiitivos
				form.instance.numero_comprobante = nuevo_numero
				form.instance.letra_comprobante = letra
				form.instance.compro = comprobante
				print("comprobante:", comprobante)
				form.instance.full_clean()
				# Final 3. Numeración (nueva versión) ----------------------->

				# Condición de Venta
				condicion_comprobante = form.cleaned_data['condicion_comprobante']
				comprobante_venta_obj = form.cleaned_data['id_comprobante_venta']
				if condicion_comprobante == 1 and not comprobante_venta_obj.remito:
					# Venta de contado
					form.instance.entrega = form.instance.total  # Asignar el total a entrega
					form.instance.estado = "C"  # Marcar como cobrado ("C")

					# =========================================================
					# VALIDAR CAJA Y REGISTRAR EN CajaDetalle PARA VENTA DE CONTADO
					# =========================================================
					usuario = self.request.user
					monto_factura = form.instance.total
					fecha_comprobante = form.cleaned_data['fecha_comprobante']
					
					# Buscar caja ABIERTA (caja_cerrada=False) con fecha coincidente
					caja_activa = Caja.objects.filter(
						id_sucursal=usuario.id_sucursal,
						caja_cerrada=False,  # Caja abierta
						fecha_caja=fecha_comprobante  # Fecha debe coincidir
					).first()
					
					if not caja_activa:
						# No hay caja activa para factura de contado
						messages.error(
							self.request,
							"❌ No hay caja activa para registrar la venta de contado. "
							"Active una caja antes de crear una factura de contado."
						)
						return redirect(self.list_view_name)  # Redirecciona a la lista de facturas
					# =========================================================

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

				# =========================================================
				# NUEVA LÓGICA: Asignación de id_caja basado en mult_caja (CAJA ABIERTA)
				# =========================================================
				comprobante_venta = form.cleaned_data['id_comprobante_venta']

				# Solo procesar si mult_caja es distinto de cero
				if comprobante_venta.mult_caja != 0:
					try:
						# Obtener valores del documento
						sucursal = form.cleaned_data['id_sucursal']
						fecha_comprobante = form.cleaned_data['fecha_comprobante']
						
						# Buscar Caja ABIERTA específica
						caja_encontrada = Caja.objects.get(
							id_sucursal=sucursal,
							fecha_caja=fecha_comprobante,
							caja_cerrada=False  # SOLO CAJAS ABIERTAS
						)
						
						# Asignar id_caja al modelo Factura
						self.object.id_caja = caja_encontrada
						self.object.save(update_fields=['id_caja'])  # Solo actualizar este campo
						
						print(f"DEBUG - Caja ABIERTA #{caja_encontrada.id_caja} asignada a factura #{self.object.id_factura}")
						
					except Caja.DoesNotExist:
						# Esto no debería ocurrir gracias a la validación temprana
						messages.error(
							self.request,
							f"❌ Error: No se encontró caja ABIERTA para la sucursal {sucursal} "
							f"y fecha {fecha_comprobante.strftime('%d/%m/%Y')}."
						)
						raise DatabaseError("Caja abierta no encontrada después de validación temprana")
						
					except Exception as e:
						messages.error(
							self.request,
							f"❌ Error al asignar caja: {str(e)}"
						)
						raise DatabaseError(f"Error en asignación de caja: {str(e)}")
				# =========================================================

				# =========================================================
				# REGISTRAR EN CAJA DETALLE PARA VENTA DE CONTADO (DESPUÉS DE GUARDAR)
				# =========================================================
				if condicion_comprobante == 1:
					try:
						usuario = self.request.user
						fecha_comprobante = form.cleaned_data['fecha_comprobante']
						
						# Buscar caja ABIERTA nuevamente (en contexto de transacción)
						caja_activa = Caja.objects.filter(
							id_sucursal=usuario.id_sucursal,
							caja_cerrada=False,  # Caja abierta
							fecha_caja=fecha_comprobante  # Fecha debe coincidir
						).first()
						
						if caja_activa:
							# Importar FormaPago para el campo id_forma_pago
							from apps.maestros.models.base_models import FormaPago
							forma_pago_efectivo = FormaPago.objects.get(id_forma_pago=1)
							
							# Crear detalle de caja
							CajaDetalle.objects.create(
								id_caja=caja_activa,
								idventas=self.object.id_factura,
								tipo_movimiento=1,  # 1 para Ingreso
								id_forma_pago=forma_pago_efectivo,
								importe=self.object.total,  # Total de la factura
								observacion=f"Factura #{self.object.numero_comprobante}"
							)
							
							messages.info(
								self.request,
								f'💰 Se registró venta de contado de ${self.object.total:.2f} '
								f'en la Caja #{caja_activa.numero_caja}'
							)
						else:
							# Esto no debería pasar porque ya validamos arriba, pero por seguridad
							messages.warning(
								self.request,
								f'⚠️ Venta de contado de ${self.object.total:.2f} no se registró en caja '
								f'(caja no disponible para fecha {fecha_comprobante.strftime("%d/%m/%Y")})'
							)
							
					except FormaPago.DoesNotExist:
						messages.warning(
							self.request,
							f'⚠️ No se encontró forma de pago efectivo (ID 1) para registrar en caja'
						)
					except Exception as e:
						print(f"DEBUG - ERROR al crear CajaDetalle para factura: {str(e)}")
						# Continuar sin registrar en caja pero mostrar advertencia
						messages.warning(
							self.request,
							f'⚠️ No se pudo registrar en caja: {str(e)}'
						)
				# =========================================================

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
				if form.cleaned_data.get('id_valida'):
					autorizacion = form.cleaned_data['id_valida']
					Valida.objects.filter(pk=autorizacion.pk).update(
						hs=timezone.now().time(),
						estatus_valida=False,
						numero_comprobante=int(nuevo_numero),  # ← CAMBIO AQUÍ
					)
					print(f"Autorización {autorizacion.id_valida} marcada como utilizada con número {nuevo_numero}")				

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
		print("Entro a form_invalid***")
		print("Errores del formulario principal:", form.errors)

		context = self.get_context_data()
		formset_detalle = context['formset_detalle']
		formset_serial = context['formset_serial']

		if formset_detalle:
			print("Errores del formset detalle:")
			for i, form_d in enumerate(formset_detalle):
				print(f"Form {i}:", form_d.errors)
				print("Non field errors:", form_d.non_field_errors())

		if formset_serial:
			print("Errores del formset serial:")
			for i, form_s in enumerate(formset_serial):
				print(f"Form {i}:", form_s.errors)

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
		"""
		Obtiene token y sign de ARCA usando FacturadorARCA
		"""
		try:
			# Obtener la empresa
			empresa = Empresa.objects.first()
			if not empresa:
				raise ValueError("No se encontró configuración de empresa")
			
			# Crear facturador con la empresa
			arca = FacturadorARCA(empresa=empresa)
			
			# Obtener token y sign (usa caché automáticamente)
			token, sign = arca.obtener_token_sign()
			
			print(f"✅ Token ARCA obtenido correctamente ({arca.entorno})")
			return token, sign, None  # ARCA no usa expiration separado
			
		except Exception as e:
			print(f"❌ Error al obtener token ARCA: {str(e)}")
			raise


	def generar_xml_afiparca(self, auth, comprobante, cliente, impuestos,  comprobante_asociado=None):
		# =========================================================
		# 🔍 DEBUG - VER QUÉ RECIBE LA FUNCIÓN
		# =========================================================
		print("=" * 60)
		print("🔍 DENTRO DE generar_xml_afiparca")
		print(f"🔍 comprobante_asociado: {comprobante_asociado}")
		print(f"🔍 tipo de comprobante: {comprobante.get('cbte_tipo')}")
		print("=" * 60)
		# =========================================================


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

		# === Envelope con namespaces correctos ===
		# envelope = Element(f"{{{SOAP_ENV}}}Envelope")
		# envelope.set("xmlns:ns0", SOAP_ENV)  # Cambiado de soap a ns0
		# envelope.set("xmlns:soap", SOAP_ENV)
		# envelope.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
		# envelope.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
		# envelope.set("soap:encodingStyle", SOAP_ENV + "encoding/")

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

		# =========================================================
		# CBTEASOC PARA NC/ND
		# =========================================================
		cbte_tipo = int(comprobante.get('cbte_tipo', '0'))

		if cbte_tipo in [2, 3] and comprobante_asociado:
			# Primero crear CbtesAsoc
			cbtes_asoc_node = SubElement(det, "CbtesAsoc")
			# Luego crear CbteAsoc dentro de CbtesAsoc
			cbte_asoc_node = SubElement(cbtes_asoc_node, "CbteAsoc")
			
			SubElement(cbte_asoc_node, "Tipo").text = str(comprobante_asociado.get('tipo', '001'))
			SubElement(cbte_asoc_node, "PtoVta").text = str(comprobante_asociado.get('pto_vta', '0021'))
			SubElement(cbte_asoc_node, "Nro").text = str(comprobante_asociado.get('nro', '00000000'))
			SubElement(cbte_asoc_node, "CbteFch").text = str(comprobante_asociado.get('fecha', ''))
			SubElement(cbte_asoc_node, "Cuit").text = auth['cuit']

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
class FacturaUpdateView(MaestroDetalleUpdateView):
	model = modelo
	list_view_name = list_view_name
	form_class = formulario
	template_name = f"ventas/{template_form}"
	success_url = reverse_lazy(list_view_name) # Nombre de la url.
	tipo_comprobante = 'electronico'  # Nuevo atributo de clase

	#-- Indicar el permiso que requiere para ejecutar la acción:
	# Obtener el nombre de la aplicación a la que pertenece el modelo.
	app_label = model._meta.app_label
	# Indicar el permiso eN el formato: <app_name>.<permiso>_<modelo>
	permission_required = f"{app_label}.change_{model.__name__.lower()}"

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['request'] = self.request  # Asegura que el token CSRF esté disponible 11/07/2025
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
		print("Entro a form_invalid$$$")
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
class FacturaDeleteView(MaestroDetalleDeleteView):
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

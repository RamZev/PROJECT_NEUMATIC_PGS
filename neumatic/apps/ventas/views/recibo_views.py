# neumatic\apps\ventas\views\recibo_views.py
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.db import transaction
from django.db.models import F
from django.db import DatabaseError
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
import json

from .msdt_views_generics import *

from apps.maestros.models.base_models import ComprobanteVenta
from ...maestros.models.numero_models import Numero
from ..models.factura_models import Factura
from ..models.caja_models import Caja, CajaDetalle
from ..models.recibo_models import (
	DetalleRecibo,
	RetencionRecibo,
	DepositoRecibo,
	TarjetaRecibo,
	ChequeRecibo
)
from ..forms.recibo_forms import (
	FacturaReciboForm,
	DetalleReciboFormSet,
	RetencionReciboFormSet,
	DepositoReciboFormSet,
	TarjetaReciboFormSet,
	ChequeReciboFormSet,
	RetencionReciboForm,
	RetencionReciboInputForm,
	DepositoReciboInputForm,
	TarjetaReciboInputForm,
	ChequeReciboInputForm
)
# Importar Formas de Pago para Caja
from apps.maestros.models.base_models import FormaPago

modelo = Factura
model_string = "recibo"  # Usamos "recibo" aunque el modelo sea Factura, para las URLs
formulario = FacturaReciboForm

template_form = f"{model_string}_form.html"
home_view_name = "home"
list_view_name = f"{model_string}_list"
create_view_name = f"{model_string}_create"
update_view_name = f"{model_string}_update"
delete_view_name = f"{model_string}_delete"


class ReciboListView(MaestroDetalleListView):
	model = modelo
	template_name = f"ventas/maestro_detalle_list.html"
	context_object_name = 'objetos'

	search_fields = [
		'id_factura',
		'numero_comprobante',
		'cuit',
		'id_cliente__nombre_cliente'
	]

	ordering = ['-id_factura']

	table_headers = {
		'id_factura': (1, 'ID'),
		'compro': (1, 'Compro'),
		'letra_comprobante': (1, 'Letra'),
		'numero_comprobante': (1, 'Nro Comp'),
		'fecha_comprobante': (1, 'Fecha'),
		'cuit': (1, 'CUIT'),
		'id_cliente': (3, 'Cliente'),
		'total': (2, 'Total'),
		'opciones': (1, 'Opciones'),
	}

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

	extra_context = {
		"master_title": "Recibos",
		"home_view_name": home_view_name,
		"list_view_name": list_view_name,
		"create_view_name": create_view_name,
		"update_view_name": update_view_name,
		"delete_view_name": delete_view_name,
		"table_headers": table_headers,
		"table_data": table_data,
		"model_string_for_pdf": "factura",  # ¡Solución clave aquí!,
		"model_string": model_string,
	}

	def get_queryset(self):
		queryset = super().get_queryset()
		user = self.request.user

		# if not user.is_superuser:
		if not (user.is_superuser or user.jerarquia == "A"):
			queryset = queryset.filter(id_sucursal=user.id_sucursal)

		# Filtrar solo facturas con recibos asociados
		queryset = queryset.filter(
		id_comprobante_venta__recibo=True
		).distinct()

		query = self.request.GET.get('busqueda', None)
		if query:
			search_conditions = Q()
			for field in self.search_fields:
				search_conditions |= Q(**{f"{field}__icontains": query})
			queryset = queryset.filter(search_conditions)

		return queryset.order_by(*self.ordering)

	# ===== NUEVO MÉTODO A AGREGAR =====
	def get_context_data(self, **kwargs):
		"""Agrega alerta de caja al contexto para deshabilitar botón Nuevo"""
		# Obtener el contexto base
		context = super().get_context_data(**kwargs)
		
		# =========================================================
		# ALERTA DE CAJA - Copiado exactamente de FacturaListView
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
						'accion': 'Debe crear una caja antes de generar recibos.'
					}
				elif caja_hoy.caja_cerrada:
					context['alerta_vista'] = {
						'tipo': 'error',
						'titulo': '⚠️ Caja cerrada',
						'mensaje': f'La caja de la sucursal para fecha {fecha_actual.strftime("%d/%m/%Y")} se encuentra CERRADA.',
						'accion': 'Debe abrir la caja antes de generar recibos.'
					}
				else:
					print("✅ CASO: Caja OK - No se crea alerta")
			else:
				print("⚠️ Usuario sin sucursal asignada")
				
		except Exception as e:
			import traceback
			traceback.print_exc()
		
		# Mantener todos los valores de extra_context
		if hasattr(self, 'extra_context'):
			context.update(self.extra_context)
			
		return context
	# ===== FIN DEL NUEVO MÉTODO =====


class ReciboCreateView(MaestroDetalleCreateView):
	model = modelo
	list_view_name = list_view_name
	form_class = formulario
	template_name = f"ventas/{template_form}"
	success_url = reverse_lazy(list_view_name)
	
	app_label = model._meta.app_label
	permission_required = f"{app_label}.add_{model.__name__.lower()}"

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		usuario = self.request.user

		if self.request.POST:
			data['formset_recibo'] = DetalleReciboFormSet(self.request.POST, prefix='detallerecibo_set')
			print(f"Prefijo de formset_recibo (POST): {data['formset_recibo'].prefix}")
			data['formset_retencion'] = RetencionReciboFormSet(self.request.POST)
			data['formset_deposito'] = DepositoReciboFormSet(self.request.POST)
			data['formset_tarjeta'] = TarjetaReciboFormSet(self.request.POST)
			data['formset_cheque'] = ChequeReciboFormSet(self.request.POST)
		else:
			data['formset_recibo'] = DetalleReciboFormSet(queryset=DetalleRecibo.objects.none(), prefix='detallerecibo_set')
			print(f"Prefijo de formset_recibo (GET): {data['formset_recibo'].prefix}")
			data['formset_retencion'] = RetencionReciboFormSet(queryset=RetencionRecibo.objects.none())
			data['formset_deposito'] = DepositoReciboFormSet(queryset=DepositoRecibo.objects.none())
			data['formset_tarjeta'] = TarjetaReciboFormSet(queryset=TarjetaRecibo.objects.none())
			data['formset_cheque'] = ChequeReciboFormSet(queryset=ChequeRecibo.objects.none())

		data['form_retencion_input'] = RetencionReciboForm()
		data['form_deposito_input'] = DepositoReciboInputForm()
		data['form_tarjeta_input'] = TarjetaReciboInputForm()
		data['form_cheque_input'] = ChequeReciboInputForm()
		data['is_edit'] = False
		
		#-- Título de la página.
		data['titulo'] = "Crear Recibo"

		# Obtener todos los comprobantes con sus valores manual
		manual_dict = {str(c.id_comprobante_venta): c.manual for c in ComprobanteVenta.objects.all()}
		data['manual_dict'] = json.dumps(manual_dict)
		
		return data

	def form_valid(self, form):
		caja_activa = None

		# 1. OBTENER EFECTIVO DEL FORMULARIO
		efectivo_recibo = form.cleaned_data.get('efectivo_recibo', 0.0)
		print(f"DEBUG - efectivo_recibo obtenido: {efectivo_recibo}")
		
		# 2. VALIDAR CAJA SOLO SI HAY EFECTIVO
		if efectivo_recibo > 0:
			usuario = self.request.user
			print(f"DEBUG - Usuario: {usuario}")
			print(f"DEBUG - ID Sucursal usuario: {usuario.id_sucursal}")

			fecha_comprobante = form.cleaned_data.get('fecha_comprobante')
			
			caja_activa = Caja.objects.filter(
				id_sucursal=usuario.id_sucursal,
				caja_cerrada=False,  # Caja no cerrada
				fecha_caja=fecha_comprobante
			).first()
			
			print(f"DEBUG - Caja activa encontrada: {caja_activa}")

			if not caja_activa:
				# No hay caja activa para registrar efectivo
				print("DEBUG - NO HAY CAJA ACTIVA, MOSTRANDO ERROR")
				messages.error(
					self.request,
					"❌ No hay caja activa para registrar el efectivo. "
					"Active una caja antes de crear un recibo con efectivo."
					"Verifique la Fecha de Comprobante y Fecha de Caja."
				)
				return redirect(self.list_view_name)

		# 3. OBTENER CONTEXTO Y VALIDAR FORMSETS
		context = self.get_context_data()
		context['form'] = form
		formsets = [
			context['formset_recibo'],
			context['formset_retencion'],
			context['formset_deposito'],
			context['formset_tarjeta'],
			context['formset_cheque']
		]

		# 4. VALIDAR FORMSETS
		for i, formset in enumerate(formsets):
			if not formset.is_valid():
				print(f"Formset {i} no es válido. Errores:", formset.errors)
				print(f"Management form errores:", formset.management_form.errors)
				return self.form_invalid(form)

		try:
			with transaction.atomic():
				###########################
				# ============================================================
				# 5. NUMERACIÓN CONDICIONAL (según manual del comprobante)
				# ============================================================
				comprobante_venta = form.cleaned_data.get('id_comprobante_venta')
				if not comprobante_venta:
					form.add_error('id_comprobante_venta', 'Debe seleccionar un comprobante de venta')
					return self.form_invalid(form)

				# Determinar tipo de numeración (igual que en factura_views)
				if comprobante_venta.electronica:
					tipo_numeracion = 'electronica'   # (no aplica a recibos, se tratará como automática)
				elif comprobante_venta.manual:
					tipo_numeracion = 'manual'
				else:
					tipo_numeracion = 'automatica'

				nuevo_numero = None

				if tipo_numeracion == 'manual':
					# Obtener el número ingresado por el usuario
					numero_ingresado = form.cleaned_data.get('numero_comprobante')
					if not numero_ingresado:
						form.add_error('numero_comprobante', 'Debe ingresar un número de comprobante')
						return self.form_invalid(form)

					# Validar unicidad: compro + letra_comprobante + numero_comprobante
					compro = form.cleaned_data['compro']
					letra = form.cleaned_data['letra_comprobante']

					existe = Factura.objects.filter(
						compro=compro,
						letra_comprobante=letra,
						numero_comprobante=numero_ingresado
					).exists()
					# Si se desea filtrar por sucursal/punto de venta, descomentar:
					# id_sucursal=form.cleaned_data['id_sucursal'],
					# id_punto_venta=form.cleaned_data['id_punto_venta']

					if existe:
						form.add_error(
							'numero_comprobante',
							f'El número {numero_ingresado} ya existe para el comprobante {compro} y letra {letra}'
						)
						return self.form_invalid(form)

					nuevo_numero = numero_ingresado

				else:
					###############################
					# Numeración automática
					sucursal = form.cleaned_data['id_sucursal']
					punto_venta = form.cleaned_data['id_punto_venta']
					comprobante = form.cleaned_data['compro']
					letra = form.cleaned_data['letra_comprobante']

					# ------------------------------------------------------------------
					# Resolver el código de búsqueda en `Numero` a partir de los códigos
					# AFIP del ComprobanteVenta. Los recibos tienen codigo_afip_a ==
					# codigo_afip_b, por lo que RB, RR y RC comparten secuencia.
					# ------------------------------------------------------------------
					codigo_afip_a = comprobante_venta.codigo_afip_a
					codigo_afip_b = comprobante_venta.codigo_afip_b

					if not codigo_afip_a or not codigo_afip_b:
						form.add_error(None, 'La configuración AFIP del comprobante está incompleta.')
						return self.form_invalid(form)

					if codigo_afip_a != codigo_afip_b:
						comprobante_afip = codigo_afip_a
					else:
						comprobante_afip = codigo_afip_a

					numero_obj, created = Numero.objects.select_for_update(nowait=True).get_or_create(
						id_sucursal=sucursal,
						id_punto_venta=punto_venta,
						comprobante=comprobante_afip,
						letra=letra,
						defaults={'numero': 0}
					)

					nuevo_numero = numero_obj.numero + 1
					Numero.objects.filter(pk=numero_obj.pk).update(numero=F('numero') + 1)
					###############################


				# Asignar el número al modelo
				form.instance.numero_comprobante = nuevo_numero
				form.instance.full_clean()
				###########################

				# Calcular Total Pagado = Total Cobrado − Resto a Cobrar
				# (lo efectivamente aplicado a facturas; el remanente queda a favor del cliente)
				total_cobrado = form.cleaned_data.get('total_cobrado', 0.0)
				resto_cobrar  = form.cleaned_data.get('resto_cobrar', 0.0)
				total_pagado  = total_cobrado - resto_cobrar

				form.instance.entrega = total_pagado

				print('total_cobrado:', total_cobrado)
				print('resto_cobrar :', resto_cobrar)
				print('total_pagado :', total_pagado)

				# ---- TRAZABILIDAD DE CABECERA DEL RECIBO ----
				print("=" * 60)
				print("📋 VALORES QUE SE VAN A GUARDAR EN LA CABECERA DEL RECIBO")
				print(f"  compro                : {form.cleaned_data.get('compro')}")
				print(f"  letra_comprobante     : {form.cleaned_data.get('letra_comprobante')}")
				print(f"  numero_comprobante    : {form.instance.numero_comprobante}")
				print(f"  total (Importe)       : {form.instance.total}")
				print(f"  entrega (Total Cobrado): {form.instance.entrega}")
				print(f"  efectivo_recibo       : {form.cleaned_data.get('efectivo_recibo')}")
				print(f"  compensa_factura      : {form.cleaned_data.get('compensa_factura')}")
				print(f"  id_cliente            : {form.cleaned_data.get('id_cliente')}")
				print("=" * 60)
				# ---- FIN TRAZABILIDAD ----


				# 8. Guardar el formulario principal
				self.object = form.save()
				
				# 9. REGISTRAR EN CAJA SOLO SI HAY EFECTIVO
				if efectivo_recibo > 0:
					usuario = self.request.user
					fecha_comprobante = form.cleaned_data.get('fecha_comprobante')
					
					# IMPORTANTE: Corrección del campo - usar caja_cerrada en lugar de estado
					caja_activa = Caja.objects.filter(
						id_sucursal=usuario.id_sucursal,
						caja_cerrada=False,  
						fecha_caja=fecha_comprobante
					).first()
					
					if caja_activa:
						print(f"DEBUG - Registrando en caja #{caja_activa.numero_caja}")
						
						# Quitar cálculo de totales de caja si no lo quieres
						# caja_activa.ingresos += efectivo_recibo
						# caja_activa.saldo = caja_activa.saldoanterior + caja_activa.ingresos - caja_activa.egresos
						# caja_activa.save()
						
						# Importar FormaPago para el campo id_forma_pago
						
						forma_pago_efectivo = FormaPago.objects.get(id_forma_pago=1)
						
						# Crear detalle de caja con campos correctos según el modelo
						CajaDetalle.objects.create(
							id_caja=caja_activa,
							idventas=self.object.id_factura,
							tipo_movimiento=1,  # 1 para ingresos
							id_forma_pago=forma_pago_efectivo,  # Campo requerido
							importe=efectivo_recibo,  # Cambiar valor por importe si ese es el nombre real
							observacion=f"Recibo #{self.object.numero_comprobante}"
						)
						
						messages.info(
							self.request,
							f'💰 Se registró efectivo de ${efectivo_recibo:.2f} '
							f'en la Caja #{caja_activa.numero_caja}'
						)

				# ===== NUEVO: ASIGNAR id_caja SI CORRESPONDE =====
				if caja_activa:
					self.object.id_caja = caja_activa
					self.object.save(update_fields=['id_caja'])
					print(f"DEBUG - Caja #{caja_activa.id_caja} asignada a recibo #{self.object.id_factura}")

				# 10. Guardar los formsets
				for formset in formsets:
					formset.instance = self.object
					formset.save()
				
				# 11. Actualizar el campo entrega en Factura
				# ---- TRAZABILIDAD DE FACTURAS COBRADAS ----
				print("=" * 60)
				print("📋 FACTURAS QUE SE VAN A ACTUALIZAR (entrega += monto_cobrado)")

				for detalle in self.object.detalles_recibo.filter(monto_cobrado__gt=0):
					###
					print(f"  id_factura_cobrada = {detalle.id_factura_cobrada_id} "
											f"| monto_cobrado = {detalle.monto_cobrado} "
											f"| entrega_actual_factura = {detalle.id_factura_cobrada.entrega} "
											f"| nuevo_entrega = {detalle.id_factura_cobrada.entrega + detalle.monto_cobrado}")
					###

					factura = detalle.id_factura_cobrada
					if factura:
						print("actualizando monto de entrega en Factura")
						factura.entrega += detalle.monto_cobrado
						factura.save()

				print("=" * 60)
				# ---- FIN TRAZABILIDAD ----
				
				# ---- TRAZABILIDAD DE CONFIRMACIÓN ----
				print("=" * 60)
				print(f"✅ RECIBO GUARDADO. ID = {self.object.id_factura}")
				print(f"  total   = {self.object.total}")
				print(f"  entrega = {self.object.entrega}")
				print(f"  id_caja = {self.object.id_caja}")
				print("=" * 60)
				# ---- FIN TRAZABILIDAD ----
				
				messages.success(self.request, "Recibo creado correctamente")
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
		formset_recibo = context['formset_recibo']

		if formset_recibo:
			print("Errores del formset:", formset_recibo.errors)

		# Usar render() en lugar de super().form_invalid()
		context['form'] = form
		return render(self.request, self.template_name, context)
		# return render(self.request, self.template_name, context)
	
	def get_success_url(self):
		return reverse(list_view_name)
	
	def get_initial(self):
		initial = super().get_initial()
		usuario = self.request.user

		initial['id_sucursal'] = usuario.id_sucursal
		initial['id_punto_venta'] = usuario.id_punto_venta

		return initial
	
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['usuario'] = self.request.user
		return kwargs


class ReciboUpdateView(MaestroDetalleUpdateView):
	model = modelo
	list_view_name = list_view_name
	form_class = formulario
	template_name = f"ventas/{template_form}"
	success_url = reverse_lazy(list_view_name)
	
	app_label = model._meta.app_label
	permission_required = f"{app_label}.change_{model.__name__.lower()}"

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		
		if self.request.POST:
			data['formset_recibo'] = DetalleReciboFormSet(self.request.POST, instance=self.object)
			data['formset_retencion'] = RetencionReciboFormSet(self.request.POST, instance=self.object)
			data['formset_deposito'] = DepositoReciboFormSet(self.request.POST, instance=self.object)
			data['formset_tarjeta'] = TarjetaReciboFormSet(self.request.POST, instance=self.object)
			data['formset_cheque'] = ChequeReciboFormSet(self.request.POST, instance=self.object)
		else:
			data['formset_recibo'] = DetalleReciboFormSet(
				instance=self.object,
				initial=[
					{
						'id_detalle_recibo': detalle.id_detalle_recibo,
						'id_factura': detalle.id_factura,
						'id_factura_cobrada': detalle.id_factura_cobrada_id,
						'monto_cobrado': detalle.monto_cobrado,
						'comprobante': detalle.id_factura_cobrada.id_comprobante_venta.nombre_comprobante_venta,
						'letra_comprobante': detalle.id_factura_cobrada.letra_comprobante,
						'numero_comprobante': detalle.id_factura_cobrada.numero_comprobante,
						'fecha_comprobante': detalle.id_factura_cobrada.fecha_comprobante.strftime('%d/%m/%Y'),
						'total': detalle.id_factura_cobrada.total,
						'entrega': detalle.id_factura_cobrada.entrega,
						'saldo_factura': detalle.saldo_factura,
						'entrega': detalle.id_factura_cobrada.total - (detalle.saldo_factura or 0),
					} for detalle in DetalleRecibo.objects.filter(id_factura=self.object).select_related('id_factura_cobrada__id_comprobante_venta')
				]
			)
			data['formset_retencion'] = RetencionReciboFormSet(instance=self.object)
			data['formset_deposito'] = DepositoReciboFormSet(instance=self.object)
			data['formset_tarjeta'] = TarjetaReciboFormSet(instance=self.object)
			data['formset_cheque'] = ChequeReciboFormSet(instance=self.object)

		# Usar RetencionReciboInputForm para la fila de inserción
		data['form_retencion_input'] = RetencionReciboInputForm()
		data['form_deposito_input'] = DepositoReciboInputForm()
		data['form_tarjeta_input'] = TarjetaReciboInputForm()
		data['form_cheque_input'] = ChequeReciboInputForm()
		data['is_edit'] = True
		
		#-- Título de la página.
		data['titulo'] = "Ver Recibo"

		# Obtener todos los comprobantes con sus valores manual
		manual_dict = {str(c.id_comprobante_venta): c.manual for c in ComprobanteVenta.objects.all()}
		data['manual_dict'] = json.dumps(manual_dict)
		
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		formsets = [
			context['formset_recibo'],
			context['formset_retencion'],
			context['formset_deposito'],
			context['formset_tarjeta'],
			context['formset_cheque']
		]

		if not all([formset.is_valid() for formset in formsets]):
			return self.form_invalid(form)

		try:
			with transaction.atomic():
				self.object = form.save()
				
				for formset in formsets:
					formset.instance = self.object
					formset.save()

				messages.success(self.request, "Recibo actualizado correctamente")
				return redirect(self.get_success_url())

		except Exception as e:
			messages.error(self.request, f"Error al actualizar: {str(e)}")
			return self.form_invalid(form)
		
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['usuario'] = self.request.user  # Pasar el usuario autenticado

		return kwargs

class ReciboDeleteView(MaestroDetalleDeleteView):
	model = modelo
	list_view_name = list_view_name
	template_name = "base_confirm_delete.html"
	success_url = reverse_lazy(list_view_name)
	
	app_label = model._meta.app_label
	permission_required = f"{app_label}.delete_{model.__name__.lower()}"

	extra_context = {
		"accion": "Eliminar Recibo",
		"list_view_name": list_view_name,
		"mensaje": "¿Estás seguro que deseas eliminar este Recibo?"
	}
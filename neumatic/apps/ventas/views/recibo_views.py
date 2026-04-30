# neumatic\apps\ventas\views\recibo_views.py
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.db import transaction
from django.db.models import F
from django.db import DatabaseError
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q

from .msdt_views_generics import *

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

		if not user.is_superuser:
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
		
		return data

	def form_valid(self, form):
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
		context = self._get_context_with_preserved_data(form)
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
				# 5. Obtener datos para la numeración
				sucursal = form.cleaned_data['id_sucursal']
				punto_venta = form.cleaned_data['id_punto_venta']
				comprobante = form.cleaned_data['compro']
				letra = form.cleaned_data['letra_comprobante']

				# 6. Obtener o crear el número en el modelo Numero
				numero_obj, created = Numero.objects.select_for_update(
					nowait=True
				).get_or_create(
					id_sucursal=sucursal,
					id_punto_venta=punto_venta,
					comprobante=comprobante,
					letra=letra,
					defaults={'numero': 0}
				)

				# 7. Calcular el nuevo número y actualizar el modelo Numero
				nuevo_numero = numero_obj.numero + 1
				Numero.objects.filter(pk=numero_obj.pk).update(numero=F('numero') + 1)
				form.instance.numero_comprobante = nuevo_numero
				form.instance.full_clean()

				# Asignar total_cobrado a entrega
				total_cobrado = form.cleaned_data.get('total_cobrado', 0.0)
				print('total_cobrado:', total_cobrado)
				form.instance.entrega = total_cobrado
				
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
						from apps.maestros.models.base_models import FormaPago
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
					
				# 10. Guardar los formsets
				for formset in formsets:
					formset.instance = self.object
					formset.save()
				
				# 11. Actualizar el campo entrega en Factura
				for detalle in self.object.detalles_recibo.filter(monto_cobrado__gt=0):
					factura = detalle.id_factura_cobrada
					if factura:
						print("actualizando monto de entrega en Factura")
						factura.entrega += detalle.monto_cobrado
						factura.save()
				
				messages.success(self.request, "Recibo creado correctamente")
				return redirect(self.get_success_url())

		except DatabaseError as e:
			messages.error(self.request, "Error de concurrencia: Intente nuevamente")
			return self.form_invalid(form)
		except Exception as e:
			messages.error(self.request, f"Error inesperado: {str(e)}")
			return self.form_invalid(form)

	def _get_context_with_preserved_data(self, form):
		"""Obtener contexto con datos del formulario preservados"""
		context = self.get_context_data()
		context['form'] = form
		return context
	
	def _return_with_preserved_data(self, form):
		"""Retornar al formulario con datos preservados"""
		context = self._get_context_with_preserved_data(form)
		return render(self.request, self.template_name, context)
	
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
		initial['cambia_precio_descripcion'] = usuario.cambia_precio_descripcion

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
						'saldo': detalle.id_factura_cobrada.total - detalle.id_factura_cobrada.entrega,
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
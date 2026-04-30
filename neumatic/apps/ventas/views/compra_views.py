# neumatic\apps\ventas\views\compra_views.py
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db import transaction
from django.utils import timezone
import json

# Importar tus vistas genéricas base
from .msdt_views_generics import *
from ..models.compra_models import Compra
from ..forms.compra_forms import CompraForm, DetalleCompraFormSet
from ...maestros.models.base_models import ProductoStock, ComprobanteCompra
from ...maestros.models.producto_models import Producto

# Configuración del modelo
modelo = Compra
model_string = modelo.__name__.lower()  # "compra"
formulario = CompraForm
template_form = f"{model_string}_form.html"

# Nombres de vistas (deben coincidir con tus URLs)
home_view_name = "home"
list_view_name = f"{model_string}_list"
create_view_name = f"{model_string}_create"
update_view_name = f"{model_string}_update"
delete_view_name = f"{model_string}_delete"


# ==============================================================================
# LIST VIEW
# ==============================================================================
class CompraListView(MaestroDetalleListView):
	model = modelo
	template_name = f"ventas/maestro_detalle_list.html"
	context_object_name = 'objetos'
	search_fields = [
		'id_compra',
		'compro',
		'numero_comprobante',
		'id_proveedor__nombre_proveedor',
	]
	ordering = ['-id_compra']
	
	# Encabezado de la tabla
	table_headers = {
		'id_compra': (1, 'ID'),
		'compro': (1, 'Compro'),
		'letra_comprobante': (1, 'Letra'),
		'numero_comprobante': (1, 'Nro Comp'),
		'fecha_comprobante': (1, 'Fecha'),
		'id_proveedor': (4, 'Proveedor'),
		'total': (2, 'Total'),
		'opciones': (1, 'Opciones'),
	}
	
	# Columnas de la tabla
	table_data = [
		{'field_name': 'id_compra', 'date_format': None},
		{'field_name': 'compro', 'date_format': None},
		{'field_name': 'letra_comprobante', 'date_format': None},
		{'field_name': 'numero_comprobante', 'date_format': None},
		{'field_name': 'fecha_comprobante', 'date_format': 'd/m/Y'},
		{'field_name': 'id_proveedor', 'date_format': None},
		{'field_name': 'total', 'date_format': None, 'decimal_places': 2},
	]
	
	extra_context = {
		"master_title": "Compras - Remitos",
		"home_view_name": home_view_name,
		"list_view_name": list_view_name,
		"create_view_name": create_view_name,
		"update_view_name": update_view_name,
		"delete_view_name": delete_view_name,
		"table_headers": table_headers,
		"table_data": table_data,
		"model_string": model_string,
	}
	
	def get_queryset(self):
		queryset = super().get_queryset()
		user = self.request.user
		
		# 🔥 FILTRAR POR COMPROBANTES CON REMITO = TRUE
		queryset = queryset.filter(id_comprobante_compra__remito=True)
		
		# Filtrar por sucursal si no es superusuario
		if not user.is_superuser:
			queryset = queryset.filter(id_sucursal=user.id_sucursal)
		
		# Aplicar búsqueda
		query = self.request.GET.get('busqueda', None)
		if query:
			search_conditions = Q()
			for field in self.search_fields:
				search_conditions |= Q(**{f"{field}__icontains": query})
			queryset = queryset.filter(search_conditions)
		
		return queryset.order_by(*self.ordering)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['model_string'] = model_string
		if hasattr(self, 'extra_context'):
			context.update(self.extra_context)
		return context


# ==============================================================================
# CREATE VIEW
# ==============================================================================
class CompraCreateView(MaestroDetalleCreateView):
	model = modelo
	list_view_name = list_view_name
	form_class = formulario
	template_name = f"ventas/{template_form}"
	success_url = reverse_lazy(list_view_name)
	
	# Permiso
	app_label = model._meta.app_label
	permission_required = f"{app_label}.add_{model.__name__.lower()}"
	
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		usuario = self.request.user
		data['cambia_precio_descripcion'] = usuario.cambia_precio_descripcion  # Ajusta si aplica
		
		if self.request.POST:
			data['formset_detalle'] = DetalleCompraFormSet(self.request.POST)
		else:
			data['formset_detalle'] = DetalleCompraFormSet(instance=self.object)
		
		data['is_edit'] = False
		
		# Diccionarios para frontend (similares a factura)
		libro_iva_dict = {str(c.id_comprobante_compra): c.libro_iva for c in ComprobanteCompra.objects.all()}
		data['libro_iva_dict'] = json.dumps(libro_iva_dict)
		
		mult_compra_dict = {str(c.id_comprobante_compra): c.mult_compra for c in ComprobanteCompra.objects.all()}
		data['mult_compra_dict'] = json.dumps(mult_compra_dict)
		
		# DICCIONARIO DE CÓDIGOS DE COMPROBANTES
		comprobante_codigos = {
			str(c.id_comprobante_compra): c.codigo_comprobante_compra 
			for c in ComprobanteCompra.objects.all()
		}
		data['comprobante_codigos'] = json.dumps(comprobante_codigos)
		
		# Si necesitas datos de ComprobanteCompra, descomenta:
		# tipo_comp_compra_dict = {str(c.id_comprobante_compra): c.nombre_comprobante_compra for c in ComprobanteCompra.objects.all()}
		# data['tipo_comp_compra_dict'] = mark_safe(json.dumps(tipo_comp_compra_dict, ensure_ascii=False))
		
		#-- Título de la página.
		data['titulo'] = "Crear Comprobante"
		
		return data
	
	######
	def form_valid(self, form):
		context = self.get_context_data()
		formset_detalle = context['formset_detalle']
		
		if not formset_detalle.is_valid():
			return self.form_invalid(form)
		
		try:
			with transaction.atomic():
				# 1. Validación básica de depósito
				deposito = form.cleaned_data.get('id_deposito')
				if not deposito:
					form.add_error('id_deposito', 'Debe seleccionar un depósito')
					return self.form_invalid(form)
				
				# 🔥 ELIMINAR TODA LA LÓGICA DE NUMERACIÓN COMPLEJA
				# Los campos vienen directamente del formulario
				
				# 2. Guardar Compra
				self.object = form.save()
				
				# 3. Guardar Detalles
				formset_detalle.instance = self.object
				detalles = formset_detalle.save()
				
				# 4. Actualizar Stock
				for detalle in detalles:
					if (hasattr(detalle.id_producto, 'tipo_producto') and
						detalle.id_producto.tipo_producto == "P" and
						detalle.cantidad):
						
						# A. ACTUALIZAR INVENTARIO (EXISTENTE)
						''' Código Original Ricardo
						ProductoStock.objects.select_for_update().filter(
							id_producto=detalle.id_producto,
							id_deposito=deposito
						).update(
							stock=F('stock') + (detalle.cantidad * self.object.id_comprobante_compra.mult_stock),
							fecha_producto_stock=form.cleaned_data['fecha_comprobante']
						)
						'''
						#-- Código Modificado por Leoncio (para que se active el signal).
						producto_stocks = ProductoStock.objects.select_for_update().filter(
							id_producto=detalle.id_producto,
							id_deposito=deposito
						)
						
						for producto_stock in producto_stocks:
							producto_stock.stock += (detalle.cantidad * self.object.id_comprobante_compra.mult_stock)
							producto_stock.fecha_producto_stock = form.cleaned_data['fecha_comprobante']
							producto_stock.save()
						
						# B. NUEVO: ACTUALIZAR DESPACHOS EN PRODUCTO
						if hasattr(detalle, 'despacho') and detalle.despacho:
							producto_obj = detalle.id_producto
							
							# Actualizar campos de despacho según la lógica requerida
							Producto.objects.filter(id_producto=producto_obj.id_producto).update(
								despacho_2=producto_obj.despacho_1,  # 1. Pasar despacho_1 a despacho_2
								despacho_1=detalle.despacho          # 2. Reemplazar despacho_1 por despacho del detalle
							)
				
				messages.success(self.request, f"Compra {self.object.numero_comprobante} creada correctamente")
				return redirect(self.get_success_url())
		
		except Exception as e:
			messages.error(self.request, f"Error inesperado: {str(e)}")
			return self.form_invalid(form)
	######
	
	def form_invalid(self, form):
		print("Errores del formulario principal:", form.errors)
		context = self.get_context_data()
		formset_detalle = context['formset_detalle']
		if formset_detalle:
			print("Errores del formset detalle:")
			for i, form_d in enumerate(formset_detalle):
				print(f"Form {i}:", form_d.errors)
		
		return super().form_invalid(form)
	
	def get_success_url(self):
		return reverse(list_view_name)
	
	def get_initial(self):
		initial = super().get_initial()
		usuario = self.request.user
		initial['id_sucursal'] = usuario.id_sucursal
		initial['id_punto_venta'] = usuario.id_punto_venta
		initial['fecha_comprobante'] = timezone.now().date()
		initial['fecha_registro'] = timezone.now().date()
		return initial
	
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['usuario'] = self.request.user
		return kwargs


# ==============================================================================
# UPDATE VIEW
# ==============================================================================
class CompraUpdateView(MaestroDetalleUpdateView):
	model = modelo
	list_view_name = list_view_name
	form_class = formulario
	template_name = f"ventas/{template_form}"
	success_url = reverse_lazy(list_view_name)
	
	app_label = model._meta.app_label
	permission_required = f"{app_label}.change_{model.__name__.lower()}"
	
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['request'] = self.request
		usuario = self.request.user
		data['cambia_precio_descripcion'] = usuario.cambia_precio_descripcion
		
		if self.request.POST:
			data['formset_detalle'] = DetalleCompraFormSet(self.request.POST, instance=self.object)
		else:
			data['formset_detalle'] = DetalleCompraFormSet(instance=self.object)
		
		data['is_edit'] = True
		
		# Mismos diccionarios que en CreateView
		libro_iva_dict = {str(c.id_comprobante_compra): c.libro_iva for c in ComprobanteCompra.objects.all()}
		data['libro_iva_dict'] = json.dumps(libro_iva_dict)
		
		mult_compra_dict = {str(c.id_comprobante_compra): c.mult_compra for c in ComprobanteCompra.objects.all()}
		data['mult_compra_dict'] = json.dumps(mult_compra_dict)
		
		# DICCIONARIO DE CÓDIGOS DE COMPROBANTES
		comprobante_codigos = {
			str(c.id_comprobante_compra): c.codigo_comprobante_compra 
			for c in ComprobanteCompra.objects.all()
		}
		data['comprobante_codigos'] = json.dumps(comprobante_codigos)
		
		#-- Título de la página.
		data['titulo'] = "Crear Comprobante"
		
		return data
	
	def form_valid(self, form):
		context = self.get_context_data()
		formset_detalle = context['formset_detalle']
		
		if formset_detalle.is_valid():
			try:
				with transaction.atomic():
					self.object = form.save()
					formset_detalle.instance = self.object
					formset_detalle.save()
					messages.success(self.request, "La Compra se ha actualizado correctamente.")
					return super().form_valid(form)
			except Exception as e:
				messages.error(self.request, f"Error al actualizar la compra: {str(e)}")
				return self.form_invalid(form)
		else:
			messages.error(self.request, "Error en el detalle de la compra. Revise los datos.")
			return self.form_invalid(form)
	
	def form_invalid(self, form):
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
		kwargs['usuario'] = self.request.user
		return kwargs


# ==============================================================================
# DELETE VIEW
# ==============================================================================
class CompraDeleteView(MaestroDetalleDeleteView):
	model = modelo
	list_view_name = list_view_name
	template_name = "base_confirm_delete.html"
	success_url = reverse_lazy(list_view_name)
	
	app_label = model._meta.app_label
	permission_required = f"{app_label}.delete_{model.__name__.lower()}"
	
	extra_context = {
		"accion": f"Eliminar {model._meta.verbose_name}",
		"list_view_name": list_view_name,
		"mensaje": "Estás seguro que deseas eliminar el Registro"
	}
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		try:
			with transaction.atomic():
				return super().post(request, *args, **kwargs)
		except Exception as e:
			messages.error(request, f"Error inesperado: {str(e)}")
			return redirect(self.success_url)
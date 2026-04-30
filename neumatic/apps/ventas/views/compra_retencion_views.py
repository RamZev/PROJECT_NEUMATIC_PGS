# neumatic\apps\ventas\views\compra_retencion_views.py
from django.urls import reverse_lazy
from .views_generics import *
from ..models.compra_models import Compra
from ..forms.compra_retencion_forms import CompraRetencionForm


class ConfigViews():
	#-- Modelo.
	model = Compra
	
	#-- Formulario asociado al modelo.
	form_class = CompraRetencionForm
	
	#-- Aplicación asociada al modelo.
	app_label = model._meta.app_label
	
	#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	model_string = model.__name__.lower()  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	
	#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
	#model_string = "tipo_cambio"
	
	#-- Permisos.
	permission_add = f"{app_label}.add_{model.__name__.lower()}"
	permission_change = f"{app_label}.change_{model.__name__.lower()}"
	permission_delete = f"{app_label}.delete_{model.__name__.lower()}"
	
	#-- Vistas del CRUD del modelo.
	list_view_name = f"{model_string}_retencion_list"
	create_view_name = f"{model_string}_retencion_create"
	update_view_name = f"{model_string}_retencion_update"
	delete_view_name = f"{model_string}_retencion_delete"
	
	#-- Plantilla para crear o actualizar el modelo.
	template_form = f"{app_label}/{model_string}_retencion_form.html"
	
	#-- Plantilla para confirmar eliminación de un registro.
	template_delete = "base_confirm_delete.html"
	
	#-- Plantilla de la lista del CRUD.
	template_list = f'{app_label}/maestro_list.html'
	
	#-- Contexto de los datos de la lista.
	context_object_name	= 'objetos'
	
	# Vista del home del proyecto
	home_view_name = "home"
	
	#-- Nombre de la url.
	success_url = reverse_lazy(list_view_name)


class DataViewList():
	search_fields = [
		'id_compra',
		'compro',
		'numero_comprobante',
		'id_proveedor__nombre_proveedor',
	]	
	ordering = ['-id_compra']
	
	paginate_by = 8
	  
	table_headers = {
		'id_compra': (1, 'ID'),
		'compro': (1, 'Compro'),
		'letra_comprobante': (1, 'Letra'),
		'numero_comprobante_formateado': (1, 'Número'),
		'fecha_comprobante': (1, 'Fecha'),
		'id_proveedor': (4, 'Proveedor'),
		'total': (2, 'Total'),
		'acciones': (1, 'Opciones'),
	}
	
	table_data = [
		{'field_name': 'id_compra', 'date_format': None},
		{'field_name': 'compro', 'date_format': None},
		{'field_name': 'letra_comprobante', 'date_format': None},
		{'field_name': 'numero_comprobante_formateado', 'date_format': None},
		{'field_name': 'fecha_comprobante', 'date_format': 'd/m/Y'},
		{'field_name': 'id_proveedor', 'date_format': None},
		{'field_name': 'total', 'date_format': None, 'decimal_places': 2},
	]


class CompraRetencionListView(MaestroListView):
	model = ConfigViews.model
	template_name = ConfigViews.template_list
	context_object_name = ConfigViews.context_object_name
	
	search_fields = DataViewList.search_fields
	ordering = DataViewList.ordering
	
	extra_context = {
		# "master_title": ConfigViews.model._meta.verbose_name_plural,
		"master_title": "Compras - Retención",
		"home_view_name": ConfigViews.home_view_name,
		"list_view_name": ConfigViews.list_view_name,
		"create_view_name": ConfigViews.create_view_name,
		"update_view_name": ConfigViews.update_view_name,
		"delete_view_name": ConfigViews.delete_view_name,
		"table_headers": DataViewList.table_headers,
		"table_data": DataViewList.table_data,
	}
	
	def get_queryset(self):
		queryset = super().get_queryset()
		user = self.request.user
		
		#-- Filtrar Compra por retenciones.
		queryset = queryset.filter(id_comprobante_compra__retencion=True)
		
		#-- Filtrar por sucursal si no es superusuario.
		if not user.is_superuser:
			queryset = queryset.filter(id_sucursal=user.id_sucursal)
		
		#-- Aplicar búsqueda si hay un término de búsqueda.
		query = self.request.GET.get('busqueda')
		if query:
			search_conditions = Q()
			for field in self.search_fields:
				search_conditions |= Q(**{f"{field}__icontains": query})
			
			queryset = queryset.filter(search_conditions)
			
		queryset = queryset.order_by(*self.ordering)
		
		return queryset


class CompraRetencionCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add
	
	def get_initial(self):
		initial = super().get_initial()
		#-- Asignar la sucursal del usuario autenticado como valor inicial.
		initial['id_sucursal'] = self.request.user.id_sucursal
		return initial


class CompraRetencionUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class CompraRetencionDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

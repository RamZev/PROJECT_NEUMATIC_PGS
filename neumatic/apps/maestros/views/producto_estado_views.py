# apps\maestros\views\producto_estado_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import ProductoEstado
from ..forms.producto_estado_forms import ProductoEstadoForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = ProductoEstado
	
	#-- Formulario asociado al modelo.
	form_class = ProductoEstadoForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = "producto_estado"
	
	#-- Registros protegidos (no se pueden modificar ni eliminar).
	REGISTROS_PROTEGIDOS = [1, 3, 4, 5]  #-- IDs de los estados "DISPONIBLES", "FALTANTES", "OFERTAS", "POCAS".


class DataViewList():
	search_fields = [
		'id_producto_estado',
		'estado_producto',
		'nombre_producto_estado'
	]
	
	ordering = ['estado_producto']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_producto_estado': (1, 'Estatus'),
		'id_producto_estado': (1, 'ID'),
		'estado_producto': (2, 'Estado Producto'),
		'nombre_producto_estado': (3, 'Nombre'),
		'color_bar': (3, 'Color'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_producto_estado', 'date_format': None},
		{'field_name': 'id_producto_estado', 'date_format': None},
		{'field_name': 'estado_producto', 'date_format': None},
		{'field_name': 'nombre_producto_estado', 'date_format': None},
		{'field_name': 'color_bar', 'date_format': None},
	]


class ProductoEstadoListView(MaestroListView):
	model = ConfigViews.model
	template_name = ConfigViews.template_list
	context_object_name = ConfigViews.context_object_name
	search_fields = DataViewList.search_fields
	ordering = DataViewList.ordering
	
	extra_context = {
		"master_title": ConfigViews.model._meta.verbose_name_plural,
		"home_view_name": ConfigViews.home_view_name,
		"list_view_name": ConfigViews.list_view_name,
		"create_view_name": ConfigViews.create_view_name,
		"update_view_name": ConfigViews.update_view_name,
		"detail_view_name": ConfigViews.detail_view_name,
		"delete_view_name": ConfigViews.delete_view_name,
		"table_headers": DataViewList.table_headers,
		"table_data": DataViewList.table_data,
	}


class ProductoEstadoCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add
	
	def get_form_kwargs(self):
		"""Pasar los registros protegidos al formulario"""
		kwargs = super().get_form_kwargs()
		kwargs['registros_protegidos'] = ConfigViews.REGISTROS_PROTEGIDOS
		return kwargs


class ProductoEstadoUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change
	
	def get_form_kwargs(self):
		"""Pasar los registros protegidos al formulario"""
		kwargs = super().get_form_kwargs()
		kwargs['registros_protegidos'] = ConfigViews.REGISTROS_PROTEGIDOS
		return kwargs


class ProductoEstadoDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class ProductoEstadoDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete
	
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		
		#--- Verificar si es un registro protegido.
		if self.object.pk in ConfigViews.REGISTROS_PROTEGIDOS:
			mensaje = f"No se puede eliminar el estado {self.object.nombre_producto_estado} porque está protegido."
			messages.error(request, mensaje)
			return redirect(self.success_url)
		
		#-- Si no está protegido, proceder con la eliminación normal.
		return super().post(request, *args, **kwargs)

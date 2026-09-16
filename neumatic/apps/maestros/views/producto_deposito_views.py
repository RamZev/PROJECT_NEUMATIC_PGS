# neumatic\apps\maestros\views\producto_deposito_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import ProductoDeposito
from ..forms.producto_deposito_forms import ProductoDepositoForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = ProductoDeposito
	
	#-- Formulario asociado al modelo.
	form_class = ProductoDepositoForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = "producto_deposito"


class DataViewList():
	search_fields = [
		'nombre_producto_deposito',
		'id_sucursal__nombre_sucursal'
	]
	
	ordering = [
		'id_sucursal__nombre_sucursal',
		'nombre_producto_deposito'
	]
	
	paginate_by = 8
	
	table_headers = {
		'estatus_producto_deposito': (1, 'Estatus'),
		'id_producto_deposito': (1, 'Id. Depósito'),
		'nombre_producto_deposito': (4, 'Depósito'),
		'id_sucursal': (4, 'Sucursal'),
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_producto_deposito', 'date_format': None},
		{'field_name': 'id_producto_deposito', 'date_format': None},
		{'field_name': 'nombre_producto_deposito', 'date_format': None},
		{'field_name': 'id_sucursal', 'date_format': None},
	]


class ProductoDepositoListView(MaestroListView):
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


class ProductoDepositoCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class ProductoDepositoUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class ProductoDepositoDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class ProductoDepositoDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

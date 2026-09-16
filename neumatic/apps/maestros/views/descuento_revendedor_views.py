# neumatic\apps\maestros\views\descuento_revendedor_views.py
from ..views.cruds_views_generics import *
from ..models.descuento_vendedor_models import DescuentoRevendedor
from ..forms.descuento_revendedor_forms import DescuentoRevendedorForm

	
class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = DescuentoRevendedor
	
	#-- Formulario asociado al modelo.
	form_class = DescuentoRevendedorForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = "descuento_revendedor"


class DataViewList():
	search_fields = ['id_marca__nombre_producto_marca', 'id_familia__nombre_producto_familia']
	
	ordering = ['id_marca__nombre_producto_marca', 'id_familia__nombre_producto_familia']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_descuento_revendedor': (1, 'Estatus'),
		'id_marca': (4, 'Marca'),
		'id_familia': (4, 'Familia'),
		'descuento': (2, 'Descuento(%)'),
		
		'acciones': (1, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_descuento_revendedor', 'date_format': None},
		{'field_name': 'id_marca', 'date_format': None},
		{'field_name': 'id_familia', 'date_format': None},
		{'field_name': 'descuento', 'date_format': None},
	]


class DescuentoRevendedorListView(MaestroListView):
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


class DescuentoRevendedorCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class DescuentoRevendedorUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class DescuentoRevendedorDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class DescuentoRevendedorDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

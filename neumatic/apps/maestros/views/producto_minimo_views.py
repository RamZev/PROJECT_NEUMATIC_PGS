# neumatic\apps\maestros\views\producto_minimo_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import ProductoMinimo
from ..forms.producto_minimo_forms import ProductoMinimoForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = ProductoMinimo
	
	#-- Formulario asociado al modelo.
	form_class = ProductoMinimoForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = "producto_minimo"


class DataViewList():
	search_fields = ['id_cai__cai', 'id_deposito__nombre_producto_deposito']
	
	ordering = ['id_cai']
	
	paginate_by = 8
	
	table_headers = {
		'id_cai': (2, 'CAI'),
		'id_deposito': (5, 'Depósito'),
		'minimo': (2, 'Mínimo'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'id_cai', 'date_format': None},
		{'field_name': 'id_deposito', 'date_format': None},
		{'field_name': 'minimo', 'date_format': None},
	]


class ProductoMinimoListView(MaestroListView):
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


class ProductoMinimoCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class ProductoMinimoUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class ProductoMinimoDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class ProductoMinimoDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

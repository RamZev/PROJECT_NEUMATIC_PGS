# neumatic\apps\maestros\views\cai_views.py
from .cruds_views_generics import *
from ..models.base_models import ProductoCai
from ..forms.producto_cai_forms import CaiForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = ProductoCai
	
	#-- Formulario asociado al modelo.
	form_class = CaiForm
	
	model_string = "producto_cai"


class DataViewList():
	search_fields = [
		'id_cai',
		'cai',
		'descripcion_cai'
	]
	
	ordering = ['cai']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_cai': (1, 'Estatus'),
		'id_cai': (1, 'ID'),
		'cai': (3, 'CAI'),
		'descripcion_cai': (5, 'Descripción CAI'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_cai', 'date_format': None},
		{'field_name': 'id_cai', 'date_format': None},
		{'field_name': 'cai', 'date_format': None},
		{'field_name': 'descripcion_cai', 'date_format': None},
	]


class ProductoCaiListView(MaestroListView):
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


class ProductoCaiCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class ProductoCaiUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class ProductoCaiDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view

class ProductoCaiDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

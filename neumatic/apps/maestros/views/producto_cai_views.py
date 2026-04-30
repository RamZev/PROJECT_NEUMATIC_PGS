# neumatic\apps\maestros\views\cai_views.py
from django.urls import reverse_lazy
from .cruds_views_generics import *
from ..models.base_models import ProductoCai
from ..forms.producto_cai_forms import CaiForm


class ConfigViews():
	#-- Modelo.
	model = ProductoCai
	
	#-- Formulario asociado al modelo.
	form_class = CaiForm
	
	#-- Aplicación asociada al modelo.
	app_label = model._meta.app_label
	
	#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	# model_string = model.__name__.lower()  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	
	#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
	model_string = "producto_cai"
	
	#-- Permisos.
	permission_add = f"{app_label}.add_{model.__name__.lower()}"
	permission_change = f"{app_label}.change_{model.__name__.lower()}"
	permission_delete = f"{app_label}.delete_{model.__name__.lower()}"
	
	#-- Vistas del CRUD del modelo.
	list_view_name = f"{model_string}_list"
	create_view_name = f"{model_string}_create"
	update_view_name = f"{model_string}_update"
	delete_view_name = f"{model_string}_delete"
	
	#-- Plantilla para crear o actualizar el modelo.
	template_form = f"{app_label}/{model_string}_form.html"
	
	#-- Plantilla para confirmar eliminación de un registro.
	template_delete = "base_confirm_delete.html"
	
	#-- Plantilla de la lista del CRUD.
	template_list = f'{app_label}/maestro_list.html'
	
	#-- Contexto de los datos de la lista.
	context_object_name	= 'objetos'
	
	#-- Vista del home del proyecto.
	home_view_name = "home"
	
	#-- Nombre de la url.
	success_url = reverse_lazy(list_view_name)


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


class ProductoCaiDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

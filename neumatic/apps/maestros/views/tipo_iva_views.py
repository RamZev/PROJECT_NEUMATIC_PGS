# neumatic\apps\maestros\views\tipo_iva_views.py
from django.urls import reverse_lazy
from ..views.cruds_views_generics import *
from ..models.base_models import TipoIva
from ..forms.tipo_iva_forms import TipoIvaForm


class ConfigViews():
	#-- Modelo.
	model = TipoIva
	
	#-- Formulario asociado al modelo.
	form_class = TipoIvaForm
	
	#-- Aplicación asociada al modelo.
	app_label = model._meta.app_label
	
	#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	# model_string = model.__name__.lower()  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	
	#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
	model_string = "tipo_iva"
	
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
		'codigo_iva',
		'nombre_iva',
		'codigo_afip_responsable'
	]
	
	ordering = ['nombre_iva']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_tipo_iva': (1, 'Estatus'),
		'nombre_iva': (3, 'Nombre'),
		'codigo_iva': (2, 'Código IVA'),
		'codigo_afip_responsable': (2, 'Código AFIP'),
		'discrimina_iva': (2, 'Discrimina IVA'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_tipo_iva', 'date_format': None},
		{'field_name': 'nombre_iva', 'date_format': None},
		{'field_name': 'codigo_iva', 'date_format': None},
		{'field_name': 'codigo_afip_responsable', 'date_format': None},
		{'field_name': 'discrimina_iva', 'date_format': None},
	]


class TipoIvaListView(MaestroListView):
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


class TipoIvaCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class TipoIvaUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class TipoIvaDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

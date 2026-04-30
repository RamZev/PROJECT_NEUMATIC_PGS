# neumatic\apps\maestros\views\tipo_documento_identidad_views.py
from django.urls import reverse_lazy
from ..views.cruds_views_generics import *
from ..models.base_models import TipoDocumentoIdentidad
from ..forms.tipo_documento_identidad_forms import TipoDocumentoIdentidadForm


class ConfigViews():
	#-- Modelo.
	model = TipoDocumentoIdentidad
	
	#-- Formulario asociado al modelo.
	form_class = TipoDocumentoIdentidadForm
	
	#-- Aplicación asociada al modelo.
	app_label = model._meta.app_label
	
	#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	# model_string = model.__name__.lower()  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	
	#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
	model_string = "tipo_documento_identidad"
	
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
		'nombre_documento_identidad',
		'tipo_documento_identidad',
		'codigo_afip',
		'ws_afip'
	]
	
	ordering = ['nombre_documento_identidad']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_tipo_documento_identidad': (1, 'Estatus'),
		'nombre_documento_identidad': (3, 'Nombre'),
		'tipo_documento_identidad': (2, 'Tipo'),
		'codigo_afip': (2, 'Código AFIP'),
		'ws_afip': (2, 'WS AFIP'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_tipo_documento_identidad', 'date_format': None},
		{'field_name': 'nombre_documento_identidad', 'date_format': None},
		{'field_name': 'tipo_documento_identidad', 'date_format': None},
		{'field_name': 'codigo_afip', 'date_format': None},
		{'field_name': 'ws_afip', 'date_format': None},
	]


class TipoDocumentoIdentidadListView(MaestroListView):
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


class TipoDocumentoIdentidadCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class TipoDocumentoIdentidadUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class TipoDocumentoIdentidadDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

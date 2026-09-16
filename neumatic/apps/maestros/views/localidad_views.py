# neumatic\apps\maestros\views\localidad_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import Localidad
from ..forms.localidad_forms import LocalidadForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = Localidad
	
	#-- Formulario asociado al modelo.
	form_class = LocalidadForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = model.__name__.lower()


class DataViewList():
	search_fields = [
		'codigo_postal',
		'nombre_localidad',
		'id_provincia__nombre_provincia'
	]
	
	ordering = ['nombre_localidad']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_localidad': (1, 'Estatus'),
		# 'id_localidad': (1, 'ID'),
		'nombre_localidad': (4, 'Nombre Localidad'),
		'codigo_postal': (2, 'Código Postal'),
		'id_provincia': (3, 'Provincia'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_localidad', 'date_format': None},
		# {'field_name': 'id_localidad', 'date_format': None},
		{'field_name': 'nombre_localidad', 'date_format': None},
		{'field_name': 'codigo_postal', 'date_format': None},
		{'field_name': 'id_provincia', 'date_format': None},
	]


class LocalidadListView(MaestroListView):
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


class LocalidadCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class LocalidadUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class LocalidadDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class LocalidadDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

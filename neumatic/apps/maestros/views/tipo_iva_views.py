# neumatic\apps\maestros\views\tipo_iva_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import TipoIva
from ..forms.tipo_iva_forms import TipoIvaForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = TipoIva
	
	#-- Formulario asociado al modelo.
	form_class = TipoIvaForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = "tipo_iva"


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
		"detail_view_name": ConfigViews.detail_view_name,
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


class TipoIvaDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class TipoIvaDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

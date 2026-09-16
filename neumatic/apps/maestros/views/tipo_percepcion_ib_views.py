# neumatic\apps\maestros\views\tipo_percepcion_ib_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import TipoPercepcionIb
from ..forms.tipo_percepcion_ib_forms import TipoPercepcionIbForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = TipoPercepcionIb
	
	#-- Formulario asociado al modelo.
	form_class = TipoPercepcionIbForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = "tipo_percepcion_ib"


class DataViewList():
	search_fields = ['descripcion_tipo_percepcion_ib']
	
	ordering = ['descripcion_tipo_percepcion_ib']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_tipo_percepcion_ib': (1, 'Estatus'),
		# 'id_tipo_percepcion_ib': (1, 'ID'),
		'descripcion_tipo_percepcion_ib': (4, 'Descripción'),
		'alicuota': (1, 'Alícuota'),
		'monto': (2, 'Monto'),
		'minimo': (2, 'Mínimo'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_tipo_percepcion_ib', 'date_format': None},
		# {'field_name': 'id_tipo_percepcion_ib', 'date_format': None},
		{'field_name': 'descripcion_tipo_percepcion_ib', 'date_format': None},
		{'field_name': 'alicuota', 'date_format': None},
		{'field_name': 'monto', 'date_format': None},
		{'field_name': 'minimo', 'date_format': None},
	]


class TipoPercepcionIbListView(MaestroListView):
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


class TipoPercepcionIbCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class TipoPercepcionIbUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class TipoPercepcionIbDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class TipoPercepcionIbDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

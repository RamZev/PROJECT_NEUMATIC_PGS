# neumatic\apps\maestros\views\moneda_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import Moneda
from ..forms.moneda_forms import MonedaForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = Moneda
	
	#-- Formulario asociado al modelo.
	form_class = MonedaForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	# model_string = "tipo_cambio"


class DataViewList():
	search_fields = ['nombre_moneda']
	
	ordering = ['nombre_moneda']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_moneda': (1, 'Estatus'),
		# 'id_moneda': (1, 'ID'),
		'nombre_moneda': (3, 'Moneda'),
		'simbolo_moneda': (1, 'Símbolo'),
		'ws_afip': (2, 'WS AFIP'),
		'cotizacion_moneda': (2, 'Cotización'),
		'predeterminada': (1, 'Predeterminada'),
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_moneda', 'date_format': None},
		{'field_name': 'nombre_moneda', 'date_format': None},
		{'field_name': 'simbolo_moneda', 'date_format': None},
		{'field_name': 'ws_afip', 'date_format': None},
		{'field_name': 'cotizacion_moneda', 'date_format': None},
		{'field_name': 'predeterminada', 'date_format': None},
	]


class MonedaListView(MaestroListView):
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


class MonedaCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class MonedaUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class MonedaDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class MonedaDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

# neumatic\apps\maestros\views\tarjeta_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import Tarjeta
from ..forms.tarjeta_forms import TarjetaForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = Tarjeta
	
	#-- Formulario asociado al modelo.
	form_class = TarjetaForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	# model_string = "tipo_cambio"


class DataViewList():
	search_fields = [
		'nombre_tarjeta', 
	]
	
	ordering = ['nombre_tarjeta']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_tarjeta': (1, 'Estatus'),
		'nombre_tarjeta': (4, 'Nombre Tarjeta'),
		'imputacion': (2, 'Imputación'),
		'banco_acreditacion': (2, 'Bco. Acreditación'),
		'propia': (1, 'Propia'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_tarjeta', 'date_format': None},
		{'field_name': 'nombre_tarjeta', 'date_format': None},
		{'field_name': 'imputacion', 'date_format': None},
		{'field_name': 'banco_acreditacion', 'date_format': None},
		{'field_name': 'propia', 'date_format': None},
	]


class TarjetaListView(MaestroListView):
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


class TarjetaCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class TarjetaUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class TarjetaDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class TarjetaDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

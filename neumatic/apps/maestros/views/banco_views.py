# neumatic\apps\maestros\views\banco_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import Banco
from ..forms.banco_forms import BancoForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = Banco
	
	#-- Formulario asociado al modelo.
	form_class = BancoForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	# model_string = "tipo_cambio"


class DataViewList():
	search_fields = [
		'codigo_banco', 
		'nombre_banco',
		'cuit_banco',
	]
	
	ordering = ['nombre_banco']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_banco': (1, 'Estatus'),
		'nombre_banco': (7, 'Nombre Banco'),
		'codigo_banco': (1, 'Código Banco'),
		'cuit_banco': (1, 'C.U.I.T.'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_banco', 'date_format': None},
		{'field_name': 'nombre_banco', 'date_format': None},
		{'field_name': 'codigo_banco', 'date_format': None},
		{'field_name': 'cuit_banco', 'date_format': None},
	]


class BancoListView(MaestroListView):
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


class BancoCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class BancoUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class BancoDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class BancoDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

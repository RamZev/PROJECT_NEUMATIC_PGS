# neumatic\apps\maestros\views\operario_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import Operario
from ..forms.operario_forms import OperarioForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = Operario
	
	#-- Formulario asociado al modelo.
	form_class = OperarioForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	# model_string = "tipo_cambio"


class DataViewList():
	search_fields = [
		'nombre_operario',
		'telefono_operario',
		'email_operario'
	]
	
	ordering = ['nombre_operario']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_operario': (1, 'Estatus'),
		# 'id_operario': (1, 'ID'),
		'nombre_operario': (4, 'Nombre'),
		'telefono_operario': (1, 'Teléfono'),
		'email_operario': (4, 'Correo'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_operario', 'date_format': None},
		# {'field_name': 'id_operario', 'date_format': None},
		{'field_name': 'nombre_operario', 'date_format': None},
		{'field_name': 'telefono_operario', 'date_format': None},
		{'field_name': 'email_operario', 'date_format': None},
	]


class OperarioListView(MaestroListView):
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


class OperarioCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class OperarioUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class OperarioDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view

class OperarioDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

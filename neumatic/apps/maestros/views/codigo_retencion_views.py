# neumatic\apps\maestros\views\codigo_retencion_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import CodigoRetencion
from ..forms.codigo_retencion_forms import CodigoRetencionForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = CodigoRetencion
	
	#-- Formulario asociado al modelo.
	form_class = CodigoRetencionForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = "codigo_retencion"
	


class DataViewList():
	search_fields = ['nombre_codigo_retencion']
	
	ordering = ['nombre_codigo_retencion']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_cod_retencion': (1, 'Estatus'),
		'nombre_codigo_retencion': (7, 'Nombre Código de Retención'),
		'imputacion': (2, 'Imputación'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_cod_retencion', 'date_format': None},
		{'field_name': 'nombre_codigo_retencion', 'date_format': None},
		{'field_name': 'imputacion', 'date_format': None},
	]


class CodigoRetencionListView(MaestroListView):
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


class CodigoRetencionCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class CodigoRetencionUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class CodigoRetencionDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class CodigoRetencionDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

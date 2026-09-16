# neumatic\apps\maestros\views\tipo_retencion_ib_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import TipoRetencionIb
from ..forms.tipo_retencion_ib_forms import TipoRetencionIbForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = TipoRetencionIb
	
	#-- Formulario asociado al modelo.
	form_class = TipoRetencionIbForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = "tipo_retencion_ib"


class DataViewList():
	search_fields = ['descripcion_tipo_retencion_ib']
	
	ordering = ['descripcion_tipo_retencion_ib']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_tipo_retencion_ib': (1, 'Estatus'),
		# 'id_tipo_retencion_ib': (1, 'ID'),
		'descripcion_tipo_retencion_ib': (5, 'Descripción'),
		'alicuota_inscripto': (1, 'Alícuota Inscripto'),
		'alicuota_no_inscripto': (1, 'Alícuota No Inscripto'),
		'monto': (1, 'Monto'),
		'minimo': (1, 'Mínimo'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_tipo_retencion_ib', 'date_format': None},
		# {'field_name': 'id_tipo_retencion_ib', 'date_format': None},
		{'field_name': 'descripcion_tipo_retencion_ib', 'date_format': None},
		{'field_name': 'alicuota_inscripto', 'date_format': None},
		{'field_name': 'alicuota_no_inscripto', 'date_format': None},
		{'field_name': 'monto', 'date_format': None},
		{'field_name': 'minimo', 'date_format': None},
	]


class TipoRetencionIbListView(MaestroListView):
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


class TipoRetencionIbCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class TipoRetencionIbUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class TipoRetencionIbDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class TipoRetencionIbDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

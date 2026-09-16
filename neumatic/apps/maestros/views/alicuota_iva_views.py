# apps\maestros\views\alicuota_iva_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import AlicuotaIva
from ..forms.alicuota_iva_forms import AlicuotaIvaForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = AlicuotaIva
	
	#-- Formulario asociado al modelo.
	form_class = AlicuotaIvaForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo).
	model_string = "alicuota_iva"


class DataViewList():
	search_fields = [
		'id_alicuota_iva',
		'codigo_alicuota',
		'alicuota_iva',
		'descripcion_alicuota_iva'
	]
	
	ordering = ['codigo_alicuota']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_alicuota_iva': (1, 'Estatus'),
		'id_alicuota_iva': (1, 'ID'),
		'codigo_alicuota': (2, 'Cód. Alíc. IVA'),
		'alicuota_iva': (2, 'Alíc. IVA(%)'),
		'descripcion_alicuota_iva': (4, 'Descripción Alíc. IVA'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_alicuota_iva', 'date_format': None},
		{'field_name': 'id_alicuota_iva', 'date_format': None},
		{'field_name': 'codigo_alicuota', 'date_format': None},
		{'field_name': 'alicuota_iva', 'date_format': None},
		{'field_name': 'descripcion_alicuota_iva', 'date_format': None},
	]


class AlicuotaIvaListView(MaestroListView):
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


class AlicuotaIvaCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class AlicuotaIvaUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class AlicuotaIvaDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class AlicuotaIvaDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

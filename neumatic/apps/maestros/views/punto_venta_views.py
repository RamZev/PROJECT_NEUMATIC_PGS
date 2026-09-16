# neumatic\apps\maestros\views\punto_venta_views.py
from ..views.cruds_views_generics import *
from ..models.base_models import PuntoVenta
from ..forms.punto_venta_forms import PuntoVentaForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = PuntoVenta
	
	#-- Formulario asociado al modelo.
	form_class = PuntoVentaForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = "punto_venta"


class DataViewList():
	search_fields = [
		'id_sucursal__nombre_sucursal',
		'punto_venta',
		'descripcion_punto_venta'
	]
	
	ordering = ['id_sucursal__nombre_sucursal', 'punto_venta']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_punto_venta': (1, 'Estatus'),
		'id_sucursal': (3, 'Sucursal'),
		'punto_venta': (2, 'Punto de Venta'),
		'descripcion_punto_venta': (4, 'Descripción Pto. Venta'),
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_punto_venta', 'date_format': None},
		{'field_name': 'id_sucursal', 'date_format': None},
		{'field_name': 'punto_venta', 'date_format': None},
		{'field_name': 'descripcion_punto_venta', 'date_format': None},
	]


class PuntoVentaListView(MaestroListView):
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


class PuntoVentaCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class PuntoVentaUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class PuntoVentaDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class PuntoVentaDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

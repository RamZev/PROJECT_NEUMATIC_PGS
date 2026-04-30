# neumatic\apps\maestros\views\comprobante_venta_views.py
from django.urls import reverse_lazy
from ..views.cruds_views_generics import *
from ..models.base_models import ComprobanteVenta
from ..forms.comprobante_venta_forms import ComprobanteVentaForm


class ConfigViews():
	#-- Modelo.
	model = ComprobanteVenta
	
	#-- Formulario asociado al modelo.
	form_class = ComprobanteVentaForm
	
	#-- Aplicación asociada al modelo.
	app_label = model._meta.app_label
	
	#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	# model_string = model.__name__.lower()  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	
	#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
	model_string = "comprobante_venta"
	
	#-- Permisos.
	permission_add = f"{app_label}.add_{model.__name__.lower()}"
	permission_change = f"{app_label}.change_{model.__name__.lower()}"
	permission_delete = f"{app_label}.delete_{model.__name__.lower()}"
	
	#-- Vistas del CRUD del modelo.
	list_view_name = f"{model_string}_list"
	create_view_name = f"{model_string}_create"
	update_view_name = f"{model_string}_update"
	delete_view_name = f"{model_string}_delete"
	
	#-- Plantilla para crear o actualizar el modelo.
	template_form = f"{app_label}/{model_string}_form.html"
	
	#-- Plantilla para confirmar eliminación de un registro.
	template_delete = "base_confirm_delete.html"
	
	#-- Plantilla de la lista del CRUD.
	template_list = f'{app_label}/maestro_list.html'
	
	#-- Contexto de los datos de la lista.
	context_object_name	= 'objetos'
	
	#-- Vista del home del proyecto.
	home_view_name = "home"
	
	#-- Nombre de la url.
	success_url = reverse_lazy(list_view_name)


class DataViewList():
	search_fields = [
		'codigo_comprobante_venta', 
		'nombre_comprobante_venta'
	]
	
	ordering = ['nombre_comprobante_venta']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_comprobante_venta': (1, 'Estatus'),
		'nombre_comprobante_venta': (3, 'Nombre Comprobante'),
		'codigo_comprobante_venta': (1, 'Código'),
		'libro_iva': (1, 'Lib. IVA'),
		'electronica': (1, 'Elec.'),
		'presupuesto': (1, 'Pres.'),
		'pendiente': (1, 'Pend.'),
		'remito': (1, 'Remito'),
		'recibo': (1, 'Recibo'),
		'acciones': (1, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_comprobante_venta', 'date_format': None},
		{'field_name': 'nombre_comprobante_venta', 'date_format': None},
		{'field_name': 'codigo_comprobante_venta', 'date_format': None},
		{'field_name': 'libro_iva', 'date_format': None},
		{'field_name': 'electronica', 'date_format': None},
		{'field_name': 'presupuesto', 'date_format': None},
		{'field_name': 'pendiente', 'date_format': None},
		{'field_name': 'remito', 'date_format': None},	
  		{'field_name': 'recibo', 'date_format': None},
	]


class ComprobanteVentaListView(MaestroListView):
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
		"delete_view_name": ConfigViews.delete_view_name,
		"table_headers": DataViewList.table_headers,
		"table_data": DataViewList.table_data,
	}


class ComprobanteVentaCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class ComprobanteVentaUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class ComprobanteVentaDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

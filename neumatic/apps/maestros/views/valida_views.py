# neumatic\apps\maestros\views\valida_views.py
from ..views.cruds_views_generics import *
from ..models.valida_models import Valida
from ..forms.valida_forms import ValidaForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = Valida
	
	#-- Formulario asociado al modelo.
	form_class = ValidaForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	# model_string = "tipo_cambio"


class DataViewList():
	search_fields = [
        'id_valida',
        'id_cliente__nombre_cliente',
        'id_cliente__cuit',          
    ]
	
	ordering = ['-id_valida']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_valida': (1, 'Estatus'),
		'id_valida': (1, 'ID'),
		'cliente_id': (1, 'ID Clie'),    
		'id_cliente': (2, 'Cliente'),
		'solicitado': (2, 'Solicitante'),
		'id_comprobante_venta': (2, 'Comprobante'),
		'fecha_valida': (1, 'Fecha'),
		'hora_valida': (1, 'Hora'),
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_valida', 'date_format': None},
		{'field_name': 'id_valida', 'date_format': None},
		{'field_name': 'cliente_id', 'date_format': None},
		{'field_name': 'id_cliente', 'date_format': None},
		{'field_name': 'solicitado', 'date_format': None},
		{'field_name': 'id_comprobante_venta', 'date_format': None},
		{'field_name': 'fecha_valida', 'date_format': 'd/m/Y'},
		{'field_name': 'hora_valida', 'date_format': None},
	]


class ValidaListView(MaestroListView):
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


class ValidaCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class ValidaUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class ValidaDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class ValidaDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete

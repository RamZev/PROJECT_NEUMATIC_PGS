# neumatic\apps\maestros\views\vendedor_views.py
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import F
import logging

from ..views.cruds_views_generics import *
from ..models.vendedor_models import Vendedor
from ..models.descuento_vendedor_models import DescuentoVendedor
from ..forms.vendedor_forms import VendedorForm
from apps.maestros.templatetags.custom_tags import formato_es_ar

logger = logging.getLogger(__name__)


class ConfigViews():
	#-- Modelo.
	model = Vendedor
	
	#-- Formulario asociado al modelo.
	form_class = VendedorForm
	
	#-- Aplicación asociada al modelo.
	app_label = model._meta.app_label
	
	#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	model_string = model.__name__.lower()  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	
	#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
	#model_string = "tipo_cambio"
	
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
		'id_vendedor',
		'nombre_vendedor'
	]
	
	ordering = ['nombre_vendedor']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_vendedor': (1, 'Estatus'),
		'id_vendedor': (1, 'ID'),
		'nombre_vendedor': (3, 'Nombre Vendedor'),
		'telefono_vendedor': (2, 'Teléfono'),
		'id_sucursal': (3, 'Sucursal'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_vendedor', 'date_format': None},
		{'field_name': 'id_vendedor', 'date_format': None},
		{'field_name': 'nombre_vendedor', 'date_format': None},
		{'field_name': 'telefono_vendedor', 'date_format': None},
		{'field_name': 'id_sucursal', 'date_format': None},
	]


class VendedorListView(MaestroListView):
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


class VendedorCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class VendedorUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class VendedorDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete


# --- NUEVA VISTA PARA EL MODAL (AJAX) ---
def get_descuentos_columna(request, columna):
	"""
	Vista que devuelve una lista de descuentos (Marca, Familia, Descuento)
	para una columna específica (ej. 'desc1', 'desc2', etc.) en formato JSON.
	"""
	#-- Validar que el nombre de la columna sea seguro para evitar inyección.
	#-- Solo permitimos 'desc' seguido de un número del 1 al 25.
	if not (columna.startswith('desc') and columna[4:].isdigit()):
		return JsonResponse({'error': f'Columna {columna[4:]} no válida. Asegúrese que sea un número entero entre 1 y 25.'}, status=400)
	
	numero_columna = columna[4:]
	if not (1 <= int(numero_columna) <= 25):
		return JsonResponse({'error': 'Número de columna fuera de rango (1-25)'}, status=400)
	
	try:
		# Filtramos los registros donde la columna específica NO sea nula.
		# Usamos __isnull=False para excluir los que están vacíos.
		filtro = {f"{columna}__isnull": False}
		# Excluimos también los que sean 0.00 si no queremos mostrarlos.
		# filtro = {f"{columna}__gt": 0} 
		
		# Construimos la consulta dinámicamente
		descuentos = DescuentoVendedor.objects.filter(**filtro).annotate(
			marca_nombre=F('id_marca__nombre_producto_marca'),
			familia_nombre=F('id_familia__nombre_producto_familia')
		).values(
			'marca_nombre', 
			'familia_nombre', 
			descuento_valor=F(columna)
		).order_by('marca_nombre', 'familia_nombre')
		
		# Convertir el QuerySet a una lista para que sea serializable a JSON y aplicar formato a los valores de descuento.
		data = list(descuentos)
		
		#-- Aplicar el filtro formato_es_ar a cada valor de descuento.
		for item in data:
			if 'descuento_valor' in item and item['descuento_valor'] is not None:
				item['descuento_valor'] = formato_es_ar(item['descuento_valor'])
		
		return JsonResponse(data, safe=False)
	
	except Exception as e:
		logger.error(f"Error al obtener descuentos para columna {columna}: {e}")
		return JsonResponse({'error': 'Error interno del servidor'}, status=500)

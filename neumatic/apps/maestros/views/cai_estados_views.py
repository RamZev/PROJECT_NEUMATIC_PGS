# neumatic\apps\maestros\views\cai_estados_views.py
from django.views import View
from django.http import JsonResponse

from ..views.cruds_views_generics import *
from ..models.base_models import MedidasEstados, ProductoCai
from ..forms.cai_estados_forms import CaiEstadosForm


class ConfigViews(BaseConfigViews):
	#-- Modelo.
	model = MedidasEstados
	
	#-- Formulario asociado al modelo.
	form_class = CaiEstadosForm
	
	#-- Si el nombre del modelo es una sola palabra: Ej. Color, se autodetermina en la clase BaseConfigViews.
	#-- Si el nombre del modelo es compuesto por más de una palabra: Ej. TipoCambio, se debe especificar manualmente (sobreescribir el atributo model_string).
	model_string = "cai_estados"


class DataViewList():
	search_fields = ['id_cai__cai', 'id_cai__producto__medida', 'id_cai__producto__nombre_producto']
	
	ordering = ['id_cai__cai']
	
	paginate_by = 8
	
	table_headers = {
		# 'estatus_medida_estado': (1, 'Estatus'),
		'id_cai': (2, 'CAI'),
		'medida': (2, 'Medida'),
		'nombre_producto': (4, 'Descripción Producto'),
		'stock_desde': (1, 'Stock Desde'),
		'stock_hasta': (1, 'Stock Hasta'),
		'id_estado': (1, 'Estado'),
		
		'acciones': (1, 'Acciones'),
	}
	
	table_data = [
		# {'field_name': 'estatus_medida_estado', 'date_format': None},
		{'field_name': 'id_cai', 'date_format': None},
		{'field_name': 'medida', 'date_format': None},
		{'field_name': 'nombre_producto', 'date_format': None},
		{'field_name': 'stock_desde', 'date_format': None},
		{'field_name': 'stock_hasta', 'date_format': None},
		{'field_name': 'id_estado', 'date_format': None},
	]


class CaiEstadosListView(MaestroListView):
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
	
	def get_queryset(self):
		queryset = super().get_queryset()
		
		#-- Optimizar consultas y eliminar duplicados.
		queryset = queryset.select_related(
			'id_cai', 
			'id_estado'
		).prefetch_related(
			'id_cai__producto_set'
		).distinct()
		
		return queryset


class CaiEstadosCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add


class CaiEstadosUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change


class CaiEstadosDetailView(MaestroDetailView):
	model = ConfigViews.model
	form_class = ConfigViews.form_class
	list_view_name = ConfigViews.list_view_name
	update_view_name = ConfigViews.update_view_name
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_view


class CaiEstadosDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete


class CAIDatosAPIView(View):
	def get(self, request, pk):
		try:
			cai = ProductoCai.objects.get(pk=pk)
			data = {
				'medida': cai.medida,
				'nombre_producto': cai.nombre_producto
			}
			return JsonResponse(data)
		except ProductoCai.DoesNotExist:
			return JsonResponse({'error': 'CAI no encontrado'}, status=404)

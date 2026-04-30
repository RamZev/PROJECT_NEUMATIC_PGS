# neumatic\apps\informes\views\list_views_generics.py
from django.views.generic import ListView

#-- Recursos necesarios para proteger las rutas.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.utils import timezone


# -- Vistas Genéricas Basada en Clases -----------------------------------------------
@method_decorator(login_required, name='dispatch')
class InformeListView(ListView):
	cadena_filtro = ""
	paginate_by = 8
	search_fields = []
	ordering = []
	report_title = ""
	table_info = {}
	pagination_options = [8, 20, 30, 40, 50]
	
	def get_queryset(self):
		#-- Acá ya determina el Modelo con el que se trabaja.
		#-- Obtiene todos los registros sin filtro.
		#-- Con lo cual no es necesario un filter.all().
		#-- luego cambiar a que por defecto no haya registros.
		queryset = super().get_queryset()
		
		#-- Obtener el valor de paginate_by de la URL, si está presente.
		paginate_by_param = self.request.GET.get('paginate_by')
		if paginate_by_param is not None:
			try:
				#-- Intentar convertir a entero, usar valor predeterminado si falla.
				paginate_by_value = int(paginate_by_param)
				self.paginate_by = paginate_by_value
			except ValueError:
				pass
		
		return queryset.order_by(*self.ordering)
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		#-- Agregar valores de paginación y valor seleccionado.
		context['pagination_options'] = self.pagination_options
		context['selected_pagination'] = int(self.paginate_by)
		
		#-- Agregar los filtros actuales al contexto.
		#-- Con esto se garantiza que la paginación funcione bien con
		#-- los datos filtrados.
		query_params = self.request.GET.copy()
		if 'page' in query_params:
			#-- Remover el parámetro de paginación actual.
			query_params.pop('page')
		
		context['query_params'] = query_params.urlencode()
		
		#-- Para pasar la fecha a la lista del maestro.
		context['fecha'] = timezone.now()
		
		return context
	
	def get(self, request, *args, **kwargs):
		#-- Obtener el valor de paginate_by de la URL, si está presente.
		paginate_by_param = self.request.GET.get('paginate_by')
		if paginate_by_param is not None:
			try:
				#-- Intentar convertir a entero, usar valor predeterminado si falla.
				paginate_by_value = int(paginate_by_param)
				self.paginate_by = paginate_by_value
			except ValueError:
				pass
		
		#-- Mantener el valor de paginate_by en el formulario de paginación.
		self.request.GET = self.request.GET.copy()
		self.request.GET['paginate_by'] = str(self.paginate_by)
		
		return super().get(request, *args, **kwargs)
	
	def get_paginate_by(self, queryset):
		#-- Utilizar el valor actualizado de paginate_by.
		return self.paginate_by

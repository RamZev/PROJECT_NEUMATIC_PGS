# neumatic\apps\maestros\views\producto_views.py
from django.urls import reverse_lazy
from ..views.cruds_views_generics import *
from ..models.producto_models import Producto
from ..forms.producto_forms import ProductoForm


class ConfigViews():
	# Modelo
	model = Producto
	
	# Formulario asociado al modelo
	form_class = ProductoForm
	
	# Aplicación asociada al modelo
	app_label = model._meta.app_label
	
	#-- Deshabilitado por redundancia:
	# # Título del listado del modelo
	# master_title = model._meta.verbose_name_plural
	
	#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	model_string = model.__name__.lower()  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	
	#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
	#model_string = "tipo_cambio"
	
	# Permisos
	permission_add = f"{app_label}.add_{model_string}"
	permission_change = f"{app_label}.change_{model_string}"
	permission_delete = f"{app_label}.delete_{model_string}"
	
	# Vistas del CRUD del modelo
	list_view_name = f"{model_string}_list"
	create_view_name = f"{model_string}_create"
	update_view_name = f"{model_string}_update"
	delete_view_name = f"{model_string}_delete"
	
	# Plantilla para crear o actualizar el modelo
	template_form = f"{app_label}/{model_string}_form.html"
	
	# Plantilla para confirmar eliminación de un registro
	template_delete = "base_confirm_delete.html"
	
	# Plantilla de la lista del CRUD
	template_list = f'{app_label}/maestro_list.html'
	
	# Contexto de los datos de la lista
	context_object_name	= 'objetos'
	
	# Vista del home del proyecto
	home_view_name = "home"
	
	# Nombre de la url 
	success_url = reverse_lazy(list_view_name)


class DataViewList():
	search_fields = ['nombre_producto']
	
	ordering = ['nombre_producto']
	
	paginate_by = 8
	  
	table_headers = {
		'codigo_producto': (2, 'Código'),
		'nombre_producto': (2, 'Nombre'),
        'tipo_producto': (2, 'Tip. Producto'),
        'precio': (2, 'Precio'),
        'costo': (1, 'Costo'),
        'stock': (1, 'Sctok'),
		'acciones': (2, 'Acciones'),
	}

	table_data = [
		{'field_name': 'codigo_producto', 'date_format': None},
        {'field_name': 'nombre_producto', 'date_format': None},
        {'field_name': 'tipo_producto', 'date_format': None},
        {'field_name': 'precio', 'date_format': None},
        {'field_name': 'costo', 'date_format': None},
        {'field_name': 'stock', 'date_format': None},
        
		
	]

# VendedorListView - Inicio
class ProductoListView(MaestroListView):
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


# ProductoCreateView - Inicio
class ProductoCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	# (revisar de donde lo copiaste que tienes asignado permission_change en vez de permission_add)
	permission_required = ConfigViews.permission_add
	
	extra_context = {
		"accion": f"Editar {ConfigViews.model._meta.verbose_name}",
		"list_view_name" : ConfigViews.list_view_name
	}


# ProductoUpdateView
class ProductoUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change
	
	extra_context = {
		 "accion": f"Editar {ConfigViews.model._meta.verbose_name}",
		"list_view_name" : ConfigViews.list_view_name
	}


# ProductoDeleteView
class ProductoDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete
	
	extra_context = {
		"accion": f"Eliminar {ConfigViews.model._meta.verbose_name}",
		"list_view_name" : ConfigViews.list_view_name,
		"mensaje": "Estás seguro de eliminar el Registro"
	}
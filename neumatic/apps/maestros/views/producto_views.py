# apps\maestros\views\producto_views.py
from django.urls import reverse_lazy

from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from ..views.cruds_views_generics import *
from ..models.producto_models import Producto
from ..forms.producto_forms import ProductoForm
from ..models.base_models import (
	ProductoDeposito,
	ProductoStock,
	ProductoMinimo
)


class ConfigViews():
	#-- Modelo.
	model = Producto
	
	#-- Formulario asociado al modelo.
	form_class = ProductoForm
	
	#-- Aplicación asociada al modelo.
	app_label = model._meta.app_label
	
	#-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	model_string = model.__name__.lower()  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
	
	#-- Usar esta forma cuando el modelo esté compuesto por más de una palabra: Ej. TipoCambio colocar "tipo_cambio".
	# model_string = "tipo_retencion_ib"
	
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
		'id_producto',
		'nombre_producto',
		'medida',
		'id_cai__cai', 
	]
	
	ordering = ['nombre_producto']
	
	paginate_by = 8
	
	table_headers = {
		'estatus_producto': (1, 'Estatus'),
		'id_producto': (1, 'ID'),
		'nombre_producto': (4, 'Nombre producto'),
		'medida': (2, 'Medida'),
		'id_cai': (2, 'CAI'),
		
		'acciones': (2, 'Acciones'),
	}
	
	table_data = [
		{'field_name': 'estatus_producto', 'date_format': None},
		{'field_name': 'id_producto', 'date_format': None},
		{'field_name': 'nombre_producto', 'date_format': None},
		{'field_name': 'medida', 'date_format': None},
		{'field_name': 'id_cai', 'date_format': None},
	]


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


class ProductoCreateView(MaestroCreateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_add
	
	def form_valid(self, form):
		return super().form_valid(form)


class ProductoUpdateView(MaestroUpdateView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	form_class = ConfigViews.form_class
	template_name = ConfigViews.template_form
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_change
	
	def form_valid(self, form):
		#-- Obtener el producto antes de guardar para comparar el CAI antiguo.
		producto_antes = Producto.objects.get(pk=self.object.pk)
		old_cai = producto_antes.id_cai
		
		#-- Guardar primero el formulario.
		response = super().form_valid(form)
		
		#-- Obtener el producto después de guardar.
		producto = self.object
		new_cai = producto.id_cai
		
		#-- Solo procesar si es producto (no servicio).
		if producto.tipo_producto == 'P':
			#-- Obtener todos os depósitos.
			depositos = ProductoDeposito.objects.all()
			
			#-- Manejar cambios en el CAI.
			if old_cai != new_cai:
				#-- 1. Si tenía CAI y ahora no tiene, o cambió de CAI.
				if old_cai:
					#-- Solo elimina el CAI anterior si no existen otros productos asociados.
					if not Producto.objects.filter(id_cai=old_cai).exclude(pk=producto.pk).exists():
						ProductoMinimo.objects.filter(id_cai=old_cai).delete()
				
				#-- 2. Si ahora tiene un CAI (nuevo o cambiado).
				if new_cai:
					#-- Crear registros para el nuevo CAI en cada depósito si no existen.
					for deposito in depositos:
						ProductoMinimo.objects.get_or_create(
							id_cai=new_cai,
							id_deposito=deposito,
							defaults={'minimo': producto.minimo or 0}
						)
			
			#-- 3. Si el CAI no cambió pero el mínimo podría haber cambiado.
			elif old_cai == new_cai and new_cai:
				#-- Actualizar el mínimo en todos los registros existentes de ProductoMinimo para este CAI.
				ProductoMinimo.objects.filter(id_cai=new_cai).update(minimo=producto.minimo or 0)
		
		return response
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		#-- Obtener el producto actual.
		producto = self.object
		
		#-- Consultar registros de ProductoStock y ProductoMinimo relacionados al producto.
		context['producto_stock_list'] = ProductoStock.objects.filter(id_producto=producto).order_by('id_deposito__nombre_producto_deposito')
		context['producto_minimo_list'] = ProductoMinimo.objects.filter(id_cai=producto.id_cai)\
			.values('id_deposito__id_producto_deposito', 'id_deposito__nombre_producto_deposito', 'id_cai__id_cai', 'id_cai__cai', 'minimo')\
			.order_by('id_deposito__nombre_producto_deposito')
		
		return context


class ProductoDeleteView (MaestroDeleteView):
	model = ConfigViews.model
	list_view_name = ConfigViews.list_view_name
	template_name = ConfigViews.template_delete
	success_url = ConfigViews.success_url
	
	#-- Indicar el permiso que requiere para ejecutar la acción.
	permission_required = ConfigViews.permission_delete
	
	def delete(self, request, *args, **kwargs):
		producto = self.get_object()
		
		#-- Almacena el CAI antes de eliminar el producto.
		cai = producto.id_cai
		
		#-- Eliminar el producto.
		response = super().delete(request, *args, **kwargs)
		
		#-- Eliminar registros en ProductoStock relacionados al producto eliminado.
		ProductoStock.objects.filter(id_producto=producto).delete()
		
		#-- Si el CAI existe, verifica que no haya otros productos con el mismo CAI.
		if cai and not Producto.objects.filter(id_cai=cai).exists():
			#-- Eliminar registros en ProductoMinimo asociados al CAI.
			ProductoMinimo.objects.filter(id_cai=cai).delete()
		
		return response	


@require_POST
def actualizar_minimo(request):
    id_cai = request.POST.get('id_cai')
    id_deposito = request.POST.get('id_deposito')
    minimo = request.POST.get('minimo')
    
    try:
        #-- Busca el registro correspondiente.
        producto_minimo = get_object_or_404(ProductoMinimo, id_cai=id_cai, id_deposito=id_deposito)
        
        #-- Actualiza el campo `minimo`.
        producto_minimo.minimo = minimo
        producto_minimo.save()
        
        return JsonResponse({'success': True, 'message': 'El mínimo se actualizó correctamente.'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

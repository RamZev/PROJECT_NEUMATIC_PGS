# neumatic\apps\maestros\views\actualizar_producto_estado_views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .cruds_views_generics import MaestroCustomView
from ..services import actualizar_estados_productos


class ActualizarEstadosProductosView(MaestroCustomView):
	"""
	Vista para actualizar estados de productos.
	"""
	permission_required = 'maestros.change_producto'
	template_name = 'maestros/confirmar_actualizar_producto_estado.html'
	home_view_name = 'home'
	
	#-- Contexto específico.
	accion = "Actualizar Estados de Productos"
	master_title = "Actualización Masiva de Estados de Productos"
	
	def get(self, request, *args, **kwargs):
		"""Muestra la página de confirmación"""
		context = self.get_context_data()
		context['mensaje'] = "¿Está seguro que desea actualizar los estados de todos los productos basado en el stock actual?"
		context['home_view_name'] = self.home_view_name
		
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		"""Ejecuta la actualización - con soporte para AJAX"""
		#-- Obtener el valor del checkbox (viene como 'on' si está marcado, o None si no)
		actualizar_todos = request.POST.get('actualizar_todos') == 'on'
		
		#-- Si es una petición AJAX, devolver JSON.
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			try:
				resultado = actualizar_estados_productos(actualizar_todos=actualizar_todos)
				return JsonResponse({
					'success': True,
					'message': f"{resultado['message']}.",
					'resultado': resultado
				})
			except Exception as e:
				return JsonResponse({
					'success': False,
					'message': f"Error al actualizar estados: {str(e)}"
				}, status=500)
		else:
			#-- Comportamiento normal para navegadores sin JavaScript.
			try:
				resultado = actualizar_estados_productos(actualizar_todos=actualizar_todos)
				messages.success(
					request, 
					f"{resultado['message']}."
				)
			except Exception as e:
				messages.error(request, f"Error al actualizar estados: {str(e)}")
			
			return redirect(self.home_view_name)
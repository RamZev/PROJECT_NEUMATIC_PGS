# neumatic\apps\maestros\views\actualizar_producto_views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal

from ..forms.actualizar_precios_producto_forms import ActualizarPreciosProductoForm
from .cruds_views_generics import MaestroCustomView
from ..models.producto_models import Producto
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


class ActualizarPreciosProductosView(MaestroCustomView):
	"""
	Vista para actualizar precios/costos de productos de forma masiva.
	"""
	permission_required = 'maestros.change_producto'
	template_name = 'maestros/actualizar_precios_producto.html'
	template_resultado_name = 'maestros/actualizar_precios_resultado.html'
	home_view_name = 'home'
	
	#-- Contexto específico.
	accion = "Cambio de Precios por porcentaje"
	master_title = "Actualización Masiva de Precios y Costos"
	
	#-- Configuración de paginación.
	paginate_by = 20
	
	def get(self, request, *args, **kwargs):
		"""
		Muestra el formulario o los resultados según corresponda.
		"""
		#-- Si se solicita limpiar (volver al formulario desde el botón).
		if request.GET.get('limpiar'):
			request.session.pop('filtros_actualizacion', None)
			request.session.pop('post_realizado', None)
			form = ActualizarPreciosProductoForm()
			context = self.get_context_data(form=form)
			return render(request, self.template_name, context)
		
		#-- Verificar si hay filtros guardados en sesión.
		if 'filtros_actualizacion' in request.session:
			#-- Si NO hay parámetros (excepto page) Y no venimos de un POST,
			#-- significa que el usuario entró desde el menú.
			otros_params = {k: v for k, v in request.GET.items() if k != 'page'}
			
			#-- Verificar si venimos de un POST (bandera en sesión).
			viene_de_post = request.session.get('post_realizado', False)
			
			#-- Si no hay otros parámetros, no hay page, y no venimos de POST.
			if not otros_params and not request.GET.get('page') and not viene_de_post:
				#-- El usuario entró desde el menú sin parámetros.
				#-- Limpiar sesión y mostrar formulario.
				request.session.pop('filtros_actualizacion', None)
				request.session.pop('post_realizado', None)
				form = ActualizarPreciosProductoForm()
				context = self.get_context_data(form=form)
				return render(request, self.template_name, context)
			
			#-- Si venimos de un POST, limpiar la bandera para la próxima vez.
			if viene_de_post:
				request.session.pop('post_realizado', None)
			
			#-- Mostrar resultados.
			filtros_data = request.session.get('filtros_actualizacion')
			
			#-- Reconstruir el queryset con los filtros guardados.
			productos, descripcion_filtros = self._obtener_productos_con_filtros(filtros_data)
			
			#-- Paginar los productos.
			paginator = Paginator(productos, self.paginate_by)
			page = request.GET.get('page')
			
			try:
				page_obj = paginator.page(page)
			except PageNotAnInteger:
				page_obj = paginator.page(1)
			except EmptyPage:
				page_obj = paginator.page(paginator.num_pages)
			
			#-- Preparar contexto para la página de resultados.
			resultado_context = {
				'total_productos': filtros_data.get('total_productos', 0),
				'actualizados': filtros_data.get('actualizados', 0),
				'errores': filtros_data.get('errores', []),
				'productos_actualizados': page_obj,
				'page_obj': page_obj,
				'paginator': paginator,
				'is_paginated': paginator.num_pages > 1,
				'porcentaje': filtros_data.get('porcentaje', 0),
				'actualizar_costo': filtros_data.get('actualizar_costo', False),
				'actualizar_precio': filtros_data.get('actualizar_precio', False),
				'filtros_aplicados': descripcion_filtros,
				'accion': self.accion,
				'master_title': f"Resultado - {self.master_title}",
			}
			
			return render(request, self.template_resultado_name, resultado_context)
		
		#-- Si no hay filtros, mostrar el formulario.
		form = ActualizarPreciosProductoForm()
		context = self.get_context_data(form=form)
		return render(request, self.template_name, context)
	
	def _obtener_productos_con_filtros(self, filtros_data):
		"""
		Reconstruye el queryset usando los filtros guardados.
		Retorna: (lista_productos_con_datos, lista_descripcion_filtros)
		"""
		productos = Producto.objects.filter(estatus_producto=True)
		descripcion_filtros = []
		
		#-- Aplicar filtros de familia.
		id_familia_desde = filtros_data.get('id_familia_desde')
		id_familia_hasta = filtros_data.get('id_familia_hasta')
		
		if id_familia_desde and id_familia_hasta:
			productos = productos.filter(
				id_familia_id__gte=id_familia_desde,
				id_familia_id__lte=id_familia_hasta
			)
			descripcion_filtros.append(f"Familia: {id_familia_desde} a {id_familia_hasta}")
		elif id_familia_desde:
			productos = productos.filter(id_familia_id__gte=id_familia_desde)
			descripcion_filtros.append(f"Familia: desde {id_familia_desde}")
		elif id_familia_hasta:
			productos = productos.filter(id_familia_id__lte=id_familia_hasta)
			descripcion_filtros.append(f"Familia: hasta {id_familia_hasta}")
		
		#-- Aplicar filtros de marca.
		id_marca_desde = filtros_data.get('id_marca_desde')
		id_marca_hasta = filtros_data.get('id_marca_hasta')
		
		if id_marca_desde and id_marca_hasta:
			productos = productos.filter(
				id_marca_id__gte=id_marca_desde,
				id_marca_id__lte=id_marca_hasta
			)
			descripcion_filtros.append(f"Marca: {id_marca_desde} a {id_marca_hasta}")
		elif id_marca_desde:
			productos = productos.filter(id_marca_id__gte=id_marca_desde)
			descripcion_filtros.append(f"Marca: desde {id_marca_desde}")
		elif id_marca_hasta:
			productos = productos.filter(id_marca_id__lte=id_marca_hasta)
			descripcion_filtros.append(f"Marca: hasta {id_marca_hasta}")
		
		#-- Aplicar filtros de modelo.
		id_modelo_desde = filtros_data.get('id_modelo_desde')
		id_modelo_hasta = filtros_data.get('id_modelo_hasta')
		
		if id_modelo_desde and id_modelo_hasta:
			productos = productos.filter(
				id_modelo_id__gte=id_modelo_desde,
				id_modelo_id__lte=id_modelo_hasta
			)
			descripcion_filtros.append(f"Modelo: {id_modelo_desde} a {id_modelo_hasta}")
		elif id_modelo_desde:
			productos = productos.filter(id_modelo_id__gte=id_modelo_desde)
			descripcion_filtros.append(f"Modelo: desde {id_modelo_desde}")
		elif id_modelo_hasta:
			productos = productos.filter(id_modelo_id__lte=id_modelo_hasta)
			descripcion_filtros.append(f"Modelo: hasta {id_modelo_hasta}")
		
		#-- Si no hay filtros aplicados.
		if not descripcion_filtros:
			descripcion_filtros.append("Todos los productos activos")
		
		#-- Ordenar por id_producto.
		productos = productos.order_by('id_producto')
		
		#-- Obtener el porcentaje y qué campos actualizar de los filtros.
		porcentaje = filtros_data.get('porcentaje', 0)
		actualizar_costo = filtros_data.get('actualizar_costo', False)
		actualizar_precio = filtros_data.get('actualizar_precio', False)
		
		#-- Calcular el factor de ajuste.
		factor = Decimal('1') + (Decimal(str(porcentaje)) / Decimal('100'))
		
		#-- Reconstruir los datos de antes/después para cada producto.
		productos_con_datos = []
		for producto in productos:
			datos_antes = {}
			datos_despues = {}
			
			if actualizar_costo:
				costo_actual = float(producto.costo) if producto.costo is not None else 0.0
				nuevo_costo = round(costo_actual * float(factor), 2)
				datos_antes['costo'] = costo_actual
				datos_despues['costo'] = nuevo_costo
			
			if actualizar_precio:
				precio_actual = float(producto.precio) if producto.precio is not None else 0.0
				nuevo_precio = round(precio_actual * float(factor), 2)
				datos_antes['precio'] = precio_actual
				datos_despues['precio'] = nuevo_precio
			
			productos_con_datos.append({
				'id': producto.id_producto,
				'nombre': producto.nombre_producto,
				'datos_antes': datos_antes,
				'datos_despues': datos_despues,
			})
		
		return productos_con_datos, descripcion_filtros
	
	def post(self, request, *args, **kwargs):
		"""Procesa la actualización masiva"""
		form = ActualizarPreciosProductoForm(request.POST)
		
		if not form.is_valid():
			context = self.get_context_data(form=form)
			return render(request, self.template_name, context)
		
		#-- Obtener datos del formulario.
		porcentaje = form.cleaned_data.get('porcentaje')
		actualizar_costo = form.cleaned_data.get('actualizar_costo')
		actualizar_precio = form.cleaned_data.get('actualizar_precio')
		
		#-- Filtros de rango.
		id_familia_desde = form.cleaned_data.get('id_familia_desde')
		id_familia_hasta = form.cleaned_data.get('id_familia_hasta')
		id_marca_desde = form.cleaned_data.get('id_marca_desde')
		id_marca_hasta = form.cleaned_data.get('id_marca_hasta')
		id_modelo_desde = form.cleaned_data.get('id_modelo_desde')
		id_modelo_hasta = form.cleaned_data.get('id_modelo_hasta')
		
		#-- Construir filtro de productos.
		filtros = models.Q()
		filtros_aplicados = False
		descripcion_filtros = []
		
		if id_familia_desde and id_familia_hasta:
			filtros &= models.Q(id_familia_id__gte=id_familia_desde, id_familia_id__lte=id_familia_hasta)
			filtros_aplicados = True
			descripcion_filtros.append(f"Familia: {id_familia_desde} a {id_familia_hasta}")
		elif id_familia_desde:
			filtros &= models.Q(id_familia_id__gte=id_familia_desde)
			filtros_aplicados = True
			descripcion_filtros.append(f"Familia: desde {id_familia_desde}")
		elif id_familia_hasta:
			filtros &= models.Q(id_familia_id__lte=id_familia_hasta)
			filtros_aplicados = True
			descripcion_filtros.append(f"Familia: hasta {id_familia_hasta}")
		
		if id_marca_desde and id_marca_hasta:
			filtros &= models.Q(id_marca_id__gte=id_marca_desde, id_marca_id__lte=id_marca_hasta)
			filtros_aplicados = True
			descripcion_filtros.append(f"Marca: {id_marca_desde} a {id_marca_hasta}")
		elif id_marca_desde:
			filtros &= models.Q(id_marca_id__gte=id_marca_desde)
			filtros_aplicados = True
			descripcion_filtros.append(f"Marca: desde {id_marca_desde}")
		elif id_marca_hasta:
			filtros &= models.Q(id_marca_id__lte=id_marca_hasta)
			filtros_aplicados = True
			descripcion_filtros.append(f"Marca: hasta {id_marca_hasta}")
		
		if id_modelo_desde and id_modelo_hasta:
			filtros &= models.Q(id_modelo_id__gte=id_modelo_desde, id_modelo_id__lte=id_modelo_hasta)
			filtros_aplicados = True
			descripcion_filtros.append(f"Modelo: {id_modelo_desde} a {id_modelo_hasta}")
		elif id_modelo_desde:
			filtros &= models.Q(id_modelo_id__gte=id_modelo_desde)
			filtros_aplicados = True
			descripcion_filtros.append(f"Modelo: desde {id_modelo_desde}")
		elif id_modelo_hasta:
			filtros &= models.Q(id_modelo_id__lte=id_modelo_hasta)
			filtros_aplicados = True
			descripcion_filtros.append(f"Modelo: hasta {id_modelo_hasta}")
		
		#-- Si no hay filtros, obtener todos los productos activos.
		if not filtros_aplicados:
			productos = Producto.objects.filter(estatus_producto=True)
			descripcion_filtros = ["Todos los productos activos"]
		else:
			productos = Producto.objects.filter(filtros, estatus_producto=True)
		
		#-- Ordenar por id_producto.
		productos = productos.order_by('id_producto')
		
		#-- Contar productos a actualizar.
		total_productos = productos.count()
		
		if total_productos == 0:
			messages.warning(request, "No se encontraron productos para actualizar con los filtros seleccionados.")
			context = self.get_context_data(form=form)
			return render(request, self.template_name, context)
		
		#-- Procesar actualización.
		try:
			with transaction.atomic():
				productos_actualizados = []
				errores = []
				
				#-- Convertir porcentaje a Decimal para cálculos precisos.
				porcentaje_decimal = Decimal(str(porcentaje))
				factor = Decimal('1') + (porcentaje_decimal / Decimal('100'))
				
				for producto in productos:
					try:
						cambios = {}
						datos_antes = {}
						datos_despues = {}
						
						if actualizar_costo:
							#-- Obtener costo actual como Decimal.
							costo_actual = producto.costo if producto.costo is not None else Decimal('0')
							
							#-- Calcular nuevo costo con Decimal.
							nuevo_costo = (costo_actual * factor).quantize(Decimal('0.01'))
							cambios['costo'] = nuevo_costo
							datos_antes['costo'] = float(costo_actual)
							datos_despues['costo'] = float(nuevo_costo)
													
						if actualizar_precio:
							#-- Obtener precio actual como Decimal.
							precio_actual = producto.precio if producto.precio is not None else Decimal('0')
							
							#-- Calcular nuevo precio con Decimal.
							nuevo_precio = (precio_actual * factor).quantize(Decimal('0.01'))
							cambios['precio'] = nuevo_precio
							datos_antes['precio'] = float(precio_actual)
							datos_despues['precio'] = float(nuevo_precio)
						
						if cambios:
							#-- Actualizar el producto.
							Producto.objects.filter(pk=producto.pk).update(**cambios)
							productos_actualizados.append({
								'id': producto.pk,
								'nombre': producto.nombre_producto,
								'datos_antes': datos_antes,
								'datos_despues': datos_despues,
							})
							
					except Exception as e:
						errores.append({
							'id': producto.pk,
							'nombre': producto.nombre_producto,
							'error': str(e)
						})
				
				#-- Guardar SOLO los filtros y metadatos en sesión (NO los productos).
				request.session['filtros_actualizacion'] = {
					'id_familia_desde': id_familia_desde,
					'id_familia_hasta': id_familia_hasta,
					'id_marca_desde': id_marca_desde,
					'id_marca_hasta': id_marca_hasta,
					'id_modelo_desde': id_modelo_desde,
					'id_modelo_hasta': id_modelo_hasta,
					'total_productos': total_productos,
					'actualizados': len(productos_actualizados),
					'errores': errores,
					'porcentaje': float(porcentaje),
					'actualizar_costo': actualizar_costo,
					'actualizar_precio': actualizar_precio,
					'filtros_aplicados': descripcion_filtros,
				}
				
				#-- Establecer bandera de que venimos de un POST.
				request.session['post_realizado'] = True
				
				#-- Redirigir a la misma vista para mostrar los resultados paginados.
				return redirect('actualizar_precios_productos')
				
		except Exception as e:
			messages.error(request, f"❌ Error al actualizar precios: {str(e)}")
			context = self.get_context_data(form=form)
			return render(request, self.template_name, context)
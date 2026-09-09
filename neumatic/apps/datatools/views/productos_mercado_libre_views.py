# neumatic\apps\datatools\views\productos_mercado_libre_views.py
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime
import logging
import csv
import json
import os

from apps.maestros.models.base_models import ProductoEstado
from apps.maestros.models.producto_models import Producto
from apps.datatools.forms.productos_mercado_libre_forms import (
	ExportarProductosForm,
	ExportarProductosArchivoForm
)


logger = logging.getLogger(__name__)


class ExportarProductosCarritoView(LoginRequiredMixin, TemplateView):
	template_name = 'datatools/productos_mercado_libre_form.html'
	paginate_by = 20
	
	def get_queryset(self, form):
		"""Obtiene el queryset aplicando todos los filtros"""
		productos = Producto.objects.filter(estatus_producto=True).select_related(
			'id_marca', 'id_familia', 'id_modelo', 'id_cai'
		)
		
		#-- Aplicar filtros.
		tipo_producto = form.cleaned_data.get('tipo_producto')
		if tipo_producto:
			productos = productos.filter(tipo_producto=tipo_producto)
		
		marca = form.cleaned_data.get('marca')
		if marca:
			productos = productos.filter(id_marca=marca)
		
		familia = form.cleaned_data.get('familia')
		if familia:
			productos = productos.filter(id_familia=familia)
		
		modelo = form.cleaned_data.get('modelo')
		if modelo:
			productos = productos.filter(id_modelo=modelo)
		
		medida = form.cleaned_data.get('medida')
		if medida:
			productos = productos.filter(medida__icontains=medida)
		
		cai = form.cleaned_data.get('cai')
		if cai:
			productos = productos.filter(id_cai__cai__icontains=cai)
		
		busqueda = form.cleaned_data.get('busqueda')
		if busqueda:
			productos = productos.filter(
				Q(nombre_producto__icontains=busqueda) |
				Q(descripcion_producto__icontains=busqueda)
			)
		
		solo_con_stock = form.cleaned_data.get('solo_con_stock')
		if solo_con_stock:
			productos = productos.annotate(
				stock_total=Sum('productostock__stock')
			).filter(stock_total__gt=0)
		
		carrito = form.cleaned_data.get('carrito')
		if carrito == 'si':
			productos = productos.filter(carrito=True)
		elif carrito == 'no':
			productos = productos.filter(carrito=False)
		
		return productos.order_by('nombre_producto')
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		form = ExportarProductosForm(request.GET)
		context['form'] = form
		context['titulo'] = 'Gestión de productos (E-Commerce)'
		
		tiene_filtros = any(key for key in request.GET.keys() if key not in ['page', 'accion'])
		productos = Producto.objects.none()
		total_registros = 0
		todos_ids = []
		
		if tiene_filtros and form.is_valid():
			productos = self.get_queryset(form)
			total_registros = productos.count()
			
			#-- Obtener TODOS los IDs filtrados (sin paginación).
			todos_ids = list(productos.values_list('id_producto', flat=True))
			
			#-- Paginación.
			paginator = Paginator(productos, self.paginate_by)
			page = request.GET.get('page', 1)
			
			try:
				page_obj = paginator.page(page)
			except PageNotAnInteger:
				page_obj = paginator.page(1)
			except EmptyPage:
				page_obj = paginator.page(paginator.num_pages)
			
			context.update({
				'page_obj': page_obj,
				'productos': page_obj.object_list,
				'total_registros': total_registros,
				'total_paginas': paginator.num_pages,
				'rango_paginas': self.get_page_range(page_obj, paginator),
				'todos_ids': todos_ids,
			})
		else:
			context.update({
				'page_obj': None,
				'productos': [],
				'total_registros': 0,
				'total_paginas': 0,
				'rango_paginas': [],
				'todos_ids': [],
			})
		
		#-- Procesar acción masiva si se envió.
		accion = request.GET.get('accion')
		if accion and hasattr(self, f'procesar_{accion}'):
			#-- Obtener los IDs de productos seleccionados de la URL.
			productos_ids_str = request.GET.get('productos_ids', '')
			productos_ids = []
			if productos_ids_str:
				try:
					productos_ids = [int(id) for id in productos_ids_str.split(',') if id.strip()]
				except ValueError:
					pass
			
			#-- Si no hay IDs seleccionados, mostrar mensaje de advertencia.
			if not productos_ids:
				messages.warning(request, 'No hay productos seleccionados para procesar.')
				url = reverse('exportar_productos_carrito')
				query_params = request.GET.copy()
				query_params.pop('accion', None)
				query_params.pop('productos_ids', None)
				return redirect(f'{url}?{query_params.urlencode()}')
			
			#-- Filtrar el queryset para solo los productos seleccionados.
			productos_seleccionados = Producto.objects.filter(
				id_producto__in=productos_ids,
				estatus_producto=True
			)
			
			#-- Si no hay productos válidos, mostrar mensaje.
			if not productos_seleccionados.exists():
				messages.warning(request, 'No se encontraron productos válidos para procesar.')
				url = reverse('exportar_productos_carrito')
				query_params = request.GET.copy()
				query_params.pop('accion', None)
				query_params.pop('productos_ids', None)
				return redirect(f'{url}?{query_params.urlencode()}')
			
			return getattr(self, f'procesar_{accion}')(request, form, productos_seleccionados)
		
		return self.render_to_response(context)
	
	def get_page_range(self, page_obj, paginator):
		"""Obtiene el rango de páginas para mostrar (máximo 5)"""
		current = page_obj.number
		total = paginator.num_pages
		
		if total <= 5:
			return range(1, total + 1)
		
		if current <= 3:
			return range(1, 6)
		elif current >= total - 2:
			return range(total - 4, total + 1)
		else:
			return range(current - 2, current + 3)
	
	def procesar_activar_carrito(self, request, form, productos):
		"""Activa el campo carrito para los productos seleccionados"""
		return self._procesar_accion_masiva(request, productos, True)
	
	def procesar_desactivar_carrito(self, request, form, productos):
		"""Desactiva el campo carrito para los productos seleccionados"""
		return self._procesar_accion_masiva(request, productos, False)
	
	def procesar_toggle_carrito(self, request, form, productos):
		"""Invierte el campo carrito para los productos seleccionados"""
		productos_ids = list(productos.values_list('id_producto', flat=True))
		
		if not productos_ids:
			messages.warning(request, 'No hay productos seleccionados para procesar.')
			url = reverse('exportar_productos_carrito')
			query_params = request.GET.copy()
			query_params.pop('accion', None)
			query_params.pop('productos_ids', None)
			return redirect(f'{url}?{query_params.urlencode()}')
		
		#-- Invertir estado SOLO para los productos seleccionados.
		for producto in productos:
			producto.carrito = not producto.carrito
		
		Producto.objects.bulk_update(productos, ['carrito'])
		
		cantidad_actualizados = productos.count()
		messages.success(
			request,
			f'Se invirtió el estado "Carrito" para {cantidad_actualizados} productos.'
		)
		
		url = reverse('exportar_productos_carrito')
		query_params = request.GET.copy()
		query_params.pop('accion', None)
		query_params.pop('productos_ids', None)
		return redirect(f'{url}?{query_params.urlencode()}')
	
	def _procesar_accion_masiva(self, request, productos, valor):
		"""Procesa la acción masiva para activar/desactivar carrito SOLO para seleccionados"""
		productos_ids = list(productos.values_list('id_producto', flat=True))
		
		if not productos_ids:
			messages.warning(request, 'No hay productos seleccionados para procesar.')
			url = reverse('exportar_productos_carrito')
			query_params = request.GET.copy()
			query_params.pop('accion', None)
			query_params.pop('productos_ids', None)
			return redirect(f'{url}?{query_params.urlencode()}')
		
		cantidad_actualizados = Producto.objects.filter(
			id_producto__in=productos_ids
		).update(carrito=valor)
		
		estado_texto = 'activado' if valor else 'desactivado'
		messages.success(
			request,
			f'Se {estado_texto} el campo "Carrito" para {cantidad_actualizados} productos.'
		)
		
		url = reverse('exportar_productos_carrito')
		query_params = request.GET.copy()
		query_params.pop('accion', None)
		query_params.pop('productos_ids', None)
		return redirect(f'{url}?{query_params.urlencode()}')
	
	def post(self, request, *args, **kwargs):
		"""Maneja peticiones POST para actualizar carrito individual"""
		try:
			producto_id = request.POST.get('producto_id')
			valor = request.POST.get('valor')
			
			if not producto_id or valor is None:
				return JsonResponse({
					'success': False,
					'error': 'Datos incompletos'
				}, status=400)
			
			producto = Producto.objects.get(id_producto=producto_id, estatus_producto=True)
			nuevo_valor = valor.lower() == 'true'
			producto.carrito = nuevo_valor
			producto.save(update_fields=['carrito'])
			
			return JsonResponse({
				'success': True,
				'message': 'Estado actualizado correctamente'
			})
			
		except Producto.DoesNotExist:
			return JsonResponse({
				'success': False,
				'error': 'Producto no encontrado'
			}, status=404)
		except Exception as e:
			logger.error(f'Error actualizando carrito: {str(e)}')
			return JsonResponse({
				'success': False,
				'error': 'Error al actualizar el estado'
			}, status=500)


class ExportarProductosArchivoView(LoginRequiredMixin, TemplateView):
	"""Vista para exportar productos a archivo"""
	
	template_name = 'datatools/exportar_productos_archivo.html'
	
	def get_queryset_export(self, estados_seleccionados):
		"""
		Obtiene el queryset con los datos para exportar
		Equivalente a la consulta SQL proporcionada
		"""
		#-- Filtrar productos activos y con carrito=True.
		productos = Producto.objects.filter(
			estatus_producto=True,
			carrito=True
		)
		
		#-- Filtrar por estados seleccionados.
		if estados_seleccionados:
			#-- Obtener los códigos de estado.
			codigos_estado = ProductoEstado.objects.filter(
				id_producto_estado__in=estados_seleccionados
			).values_list('estado_producto', flat=True)
			
			productos = productos.filter(
				id_producto_estado__estado_producto__in=codigos_estado
			)
		
		#-- Anotar el stock total (suma de stock de todos los depósitos).
		productos = productos.annotate(
			stock_total=Sum('productostock__stock')
		)
		
		#-- Seleccionar los campos necesarios (SIN calcular oferta aquí).
		productos = productos.values(
			'id_cai__cai',
			'nombre_producto',
			'medida',
			'stock_total',
			'descuento',
			'precio',
			'id_producto_estado__estado_producto'
		).order_by('id_cai__cai')
		
		return productos
	
	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		form = ExportarProductosArchivoForm()
		context['form'] = form
		context['titulo'] = 'Exportar productos (E-Commerce)'
		
		#-- Si hay parámetros GET, procesar.
		if request.GET.get('exportar'):
			form = ExportarProductosArchivoForm(request.GET)
			if form.is_valid():
				return self.procesar_exportacion(request, form)
			else:
				#-- Si hay errores, mostrar mensajes.
				for field, errors in form.errors.items():
					for error in errors:
						messages.error(request, f'{field}: {error}')
				context['form'] = form
		
		return self.render_to_response(context)
	
	def post(self, request, *args, **kwargs):
		"""Maneja la exportación desde un formulario POST"""
		form = ExportarProductosArchivoForm(request.POST)
		if form.is_valid():
			return self.procesar_exportacion(request, form)
		else:
			#-- Si hay errores, mostrar mensajes y volver al formulario.
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f'{field}: {error}')
			
			context = self.get_context_data()
			context['form'] = form
			return self.render_to_response(context)
	
	def procesar_exportacion(self, request, form):
		"""Procesa la exportación de datos"""
		
		#-- Obtener datos del formulario.
		estados_ids = form.cleaned_data.get('estados')
		formato = form.cleaned_data.get('formato')
		separador_decimal = form.cleaned_data.get('separador_decimal')
		ruta_archivo = form.cleaned_data.get('ruta_archivo')
		
		#-- Obtener los datos.
		datos = self.get_queryset_export(estados_ids)
		
		#-- Convertir a lista para poder contar.
		datos_lista = list(datos)
		
		if not datos_lista:
			messages.warning(request, 'No hay datos para exportar con los filtros seleccionados.')
			return redirect('exportar_productos_archivo')
		
		#-- Crear directorio si no existe.
		export_dir = os.path.join(settings.MEDIA_ROOT, 'exports')
		os.makedirs(export_dir, exist_ok=True)
		
		#-- Generar nombre de archivo con timestamp.
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
		nombre_base = f"{ruta_archivo}_{timestamp}"
		
		#-- Preparar datos para exportación (formatear decimales y calcular oferta).
		datos_export = []
		for item in datos_lista:
			#-- Crear copia del diccionario.
			row = dict(item)
			
			#-- Calcular oferta en Python (precio - (precio * descuento / 100))
			precio = row.get('precio', 0) or 0
			descuento = row.get('descuento', 0) or 0
			oferta = round(precio - (precio * descuento / 100), 2)
			
			#-- Formatear valores numéricos según el separador decimal.
			if separador_decimal == 'coma':
				stock = row.get('stock_total', 0) or 0
				precio_formateado = f"{precio:.2f}".replace('.', ',')
				descuento_formateado = f"{descuento:.2f}".replace('.', ',')
				oferta_formateada = f"{oferta:.2f}".replace('.', ',')
				stock_formateado = str(stock).replace('.', ',')
			else:
				precio_formateado = f"{precio:.2f}"
				descuento_formateado = f"{descuento:.2f}"
				oferta_formateada = f"{oferta:.2f}"
				stock_formateado = row.get('stock_total', 0) or 0
			
			#-- Renombrar campos para el archivo.
			row_export = {
				'CAI': row.get('id_cai__cai', ''),
				'Producto': row.get('nombre_producto', ''),
				'Medida': row.get('medida', ''),
				'Stock': stock_formateado,
				'Descuento (%)': descuento_formateado,
				'Oferta': oferta_formateada,
				'Precio': precio_formateado,
				'Estado': row.get('id_producto_estado__estado_producto', ''),
			}
			datos_export.append(row_export)
		
		#-- Exportar según formato.
		if formato == 'csv':
			return self.exportar_csv(request, datos_export, nombre_base)
		elif formato == 'json':
			return self.exportar_json(request, datos_export, nombre_base)
		elif formato == 'txt':
			return self.exportar_txt(request, datos_export, nombre_base)
		
		messages.error(request, 'Formato de exportación no válido.')
		return redirect('exportar_productos_archivo')
	
	def exportar_csv(self, request, datos, nombre_base):
		"""Exporta los datos a CSV"""
		export_dir = os.path.join(settings.MEDIA_ROOT, 'exports')
		nombre_archivo = f"{nombre_base}.csv"
		ruta_completa = os.path.join(export_dir, nombre_archivo)
		
		if not datos:
			messages.warning(request, 'No hay datos para exportar.')
			return redirect('exportar_productos_archivo')
		
		#-- Obtener los encabezados.
		headers = list(datos[0].keys())
		
		#-- Escribir archivo CSV.
		with open(ruta_completa, 'w', newline='', encoding='utf-8-sig') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=';')
			writer.writeheader()
			writer.writerows(datos)
		
		#-- Crear mensaje de éxito con enlace de descarga.
		url_descarga = f"{settings.MEDIA_URL}exports/{nombre_archivo}"
		messages.success(
			request, 
			f'Archivo CSV exportado correctamente: <a href="{url_descarga}" target="_blank">{nombre_archivo}</a>'
		)
		
		return redirect('exportar_productos_archivo')
	
	def exportar_json(self, request, datos, nombre_base):
		"""Exporta los datos a JSON"""
		export_dir = os.path.join(settings.MEDIA_ROOT, 'exports')
		nombre_archivo = f"{nombre_base}.json"
		ruta_completa = os.path.join(export_dir, nombre_archivo)
		
		if not datos:
			messages.warning(request, 'No hay datos para exportar.')
			return redirect('exportar_productos_archivo')
		
		#-- Escribir archivo JSON.
		with open(ruta_completa, 'w', encoding='utf-8') as jsonfile:
			json.dump(datos, jsonfile, ensure_ascii=False, indent=2)
		
		url_descarga = f"{settings.MEDIA_URL}exports/{nombre_archivo}"
		messages.success(
			request,
			f'Archivo JSON exportado correctamente: <a href="{url_descarga}" target="_blank">{nombre_archivo}</a>'
		)
		
		return redirect('exportar_productos_archivo')
	
	def exportar_txt(self, request, datos, nombre_base):
		"""Exporta los datos a TXT (formato tabla)"""
		export_dir = os.path.join(settings.MEDIA_ROOT, 'exports')
		nombre_archivo = f"{nombre_base}.txt"
		ruta_completa = os.path.join(export_dir, nombre_archivo)
		
		if not datos:
			messages.warning(request, 'No hay datos para exportar.')
			return redirect('exportar_productos_archivo')
		
		headers = list(datos[0].keys())
		
		#-- Detección automática de columnas numéricas.
		columnas_numericas = []
		for header in headers:
			#-- Verificar si la columna es numérica revisando varios registros.
			es_numerica = True
			muestras_revisadas = 0
			max_muestras = min(10, len(datos))  # Revisar hasta 10 registros
			
			for i, row in enumerate(datos):
				if i >= max_muestras:
					break
				valor = row.get(header, '')
				
				#-- Si el valor es None o cadena vacía, lo consideramos numérico (puede ser null).
				if valor is None or valor == '':
					continue
					
				#-- Convertir a string para analizar.
				valor_str = str(valor)
				
				#-- Limpiar caracteres de formato (comas de miles, etc.).
				valor_limpio = valor_str.replace('.', '').replace(',', '').strip()
				
				#-- Verificar si es numérico (entero o decimal).
				try:
					#-- Intentar convertir a float (acepta enteros y decimales).
					float(valor_limpio)
				except (ValueError, TypeError):
					es_numerica = False
					break
			
			if es_numerica:
				columnas_numericas.append(header)
		
		#-- Calcular anchos de columna.
		col_widths = {}
		for header in headers:
			max_len = len(header)
			for row in datos:
				value = str(row.get(header, ''))
				if len(value) > max_len:
					max_len = len(value)
			col_widths[header] = max_len + 2
		
		with open(ruta_completa, 'w', encoding='utf-8') as txtfile:
			#-- Línea superior.
			total_width = sum(col_widths.values()) + len(headers) + 12
			txtfile.write('=' * total_width + '\n')
			
			#-- Encabezados (todos alineados a la izquierda).
			header_line = ' | '.join([header.ljust(col_widths[header]) for header in headers])
			txtfile.write(header_line + '\n')
			txtfile.write('-' * total_width + '\n')
			
			#-- Datos.
			for row in datos:
				line_parts = []
				for header in headers:
					value = str(row.get(header, ''))
					#-- Si es columna numérica, alinear a la derecha.
					if header in columnas_numericas:
						line_parts.append(value.rjust(col_widths[header]))
					else:
						line_parts.append(value.ljust(col_widths[header]))
				line = ' | '.join(line_parts)
				txtfile.write(line + '\n')
			
			#-- Línea inferior.
			txtfile.write('=' * total_width + '\n')
			
			#-- Información adicional.
			txtfile.write(f'\nTotal de registros: {len(datos)}\n')
			txtfile.write(f'Fecha de exportación: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')
		
		url_descarga = f"{settings.MEDIA_URL}exports/{nombre_archivo}"
		messages.success(
			request,
			f'Archivo TXT exportado correctamente: <a href="{url_descarga}" target="_blank">{nombre_archivo}</a>'
		)
		
		return redirect('exportar_productos_archivo')
# neumatic\apps\datatools\views\actualizar_estados_views.py
import pandas as pd
from django.core.paginator import Paginator
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db import transaction

from ..forms.actualizar_estados_forms import ActualizarEstadosForm
from apps.maestros.models.base_models import MedidasEstados, ProductoCai, ProductoEstado


class ActualizarEstadosCargarView(FormView):
	template_name = 'datatools/actualizar_estados_cargar.html'
	form_class = ActualizarEstadosForm
	success_url = reverse_lazy('actualizar_estados_previsualizar')
	
	def get(self, request, *args, **kwargs):
		#-- Limpiar datos anteriores al mostrar el formulario
		keys_to_remove = ['actualizar_estados_excel_data', 'actualizar_estados_errores_procesamiento']
		for key in keys_to_remove:
			if key in self.request.session:
				del self.request.session[key]
		
		return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['fecha'] = timezone.now()
		return context
	
	def form_valid(self, form):
		from apps.informes.views.caiestados_list_views import ConfigViews
		
		#-- LIMPIAR datos anteriores antes de guardar nuevos.
		keys_to_remove = ['actualizar_estados_excel_data', 'actualizar_estados_errores_procesamiento']
		for key in keys_to_remove:
			if key in self.request.session:
				del self.request.session[key]
		
		archivo = form.cleaned_data['archivo_excel']
		
		try:
			if archivo.name.endswith('.xlsx') or archivo.name.endswith('.xls'):
				#-- PRIMERO: Leer los nombres de columnas para identificar tipos.
				df_headers = pd.read_excel(archivo, nrows=0)
				columnas_excel = df_headers.columns.tolist()
				
				#-- Identificar tipos de campos.
				columnas_texto = []
				columnas_booleanos = []
				columnas_enteros = []
				columnas_decimales = []
				
				for value in ConfigViews.table_info.values():
					if value.get('excel') and value['label'] in columnas_excel:
						if value.get('type') in ["char", "text", "string"]:
							columnas_texto.append(value['label'])
						elif value.get('type') in ["bool", "boolean"]:
							columnas_booleanos.append(value['label'])
						elif value.get('type') ==  "int":
							columnas_enteros.append(value['label'])
						elif value.get('type') in ["decimal", "float"]:
							columnas_decimales.append(value['label'])
						else:
							#-- Por defecto, tratar como string.
							columnas_texto.append(value['label'])
				
				#-- SEGUNDO: Leer Excel forzando las columnas string como texto.
				dtype_dict = {col: str for col in columnas_texto}
				
				#-- Para decimales, leer como float para preservar formato numérico.
				for columna in columnas_decimales:
					if columna in df_headers.columns:
						dtype_dict[columna] = float
				
				df = pd.read_excel(archivo, na_filter=False, dtype=dtype_dict, keep_default_na=False)
				
				#-- Verificar si el DataFrame está vacío.
				if df.empty:
					form.add_error('archivo_excel', 'El archivo Excel está vacío.')
					return self.form_invalid(form)
				
				#-- Verificar que las columnas coincidan con las esperadas.
				columnas_esperadas = [value['label'] for value in ConfigViews.table_info.values() if value['excel'] ]
				if set(columnas_esperadas) != set(columnas_excel):
					form.add_error('archivo_excel', f'Las columnas del archivo no coinciden con las esperadas. ')
					return self.form_invalid(form)
				
				#-- TERCERO: Asegurar que los campos string mantengan formato exacto.
				for columna in columnas_texto:
					if columna in df.columns:
						#-- Preservar strings exactos, incluyendo ceros iniciales.
						df[columna] = df[columna].apply(lambda x: self._preservar_formato_exacto(x))
				
				#-- CUARTO: Convertir campos booleanos a formato Si/No
				for columna in columnas_booleanos:
					if columna in df.columns:
						df[columna] = df[columna].apply(lambda x: self._convertir_booleano_a_si_no(x))
				
				#-- QUINTO: Procesar campos enteros para preservar formato
				for columna in columnas_enteros:
					if columna in df.columns:
						df[columna] = df[columna].apply(lambda x: self._preservar_formato_entero(x))
				
				#-- SEXTO: Procesar campos decimales para preservar formato
				for columna in columnas_decimales:
					if columna in df.columns:
						df[columna] = df[columna].apply(lambda x: self._preservar_formato_decimal(x))
				
				#-- Generar lista de campos protegidos y sus etiquetas.
				campos_portegidos = [campo for campo, info in ConfigViews.table_info.items() if info.get('protected', False)]
				etiquetas_portegidas = [info['label'] for info in ConfigViews.table_info.values() if info.get('protected', False)]
				
				#-- Mapear Columnas del Excel a nombres de campos {"label": producto.campo}.
				label_to_field_map = {value['label']: key for key, value in ConfigViews.table_info.items() if value['label'] in columnas_excel}
				#-- Limpiar datos (solo valores específicos, no formato).
				df = df.replace(['nan', 'NaN', 'NAN', 'NULL', 'null'], None)
				
				#-- Convertir a lista de diccionarios y guardar en sesión.
				todos_los_datos = df.to_dict('records')
				total_filas = len(todos_los_datos)
				
				#-- Guardar en sesión - optimizado para grandes volúmenes.
				self.request.session['actualizar_estados_excel_data'] = {
					'columnas': list(df.columns),
					'todos_los_datos': todos_los_datos,
					'total_filas': total_filas,
					'nombre_archivo': archivo.name,
					'campos_protegidos': campos_portegidos,
					'etiquetas_protegidas': etiquetas_portegidas,
					'etiquetas_a_campos_map': label_to_field_map,
				}
				
				return super().form_valid(form)
			else:
				form.add_error('archivo_excel', 'El archivo debe ser en formato Excel (.xlsx o .xls)')
				return self.form_invalid(form)
			
		except Exception as e:
			form.add_error('archivo_excel', f'Error al procesar el archivo: {str(e)}')
			return self.form_invalid(form)
		
	def _preservar_formato_exacto(self, valor):
		"""
		Preserva el formato exacto del valor tal como está en Excel.
		"""
		if valor is None or pd.isna(valor):
			return None
		
		#-- Si ya es string, devolver tal cual.
		if isinstance(valor, str):
			#-- Manejar casos especiales de pandas/Excel.
			if valor in ['nan', 'NaN', 'NAN', 'NULL', 'null']:
				return None
			return valor
		
		#-- Para números, convertirlos a string sin perder formato.
		if isinstance(valor, (int, float)):
			#-- Para evitar notación científica y preservar ceros.
			if isinstance(valor, int):
				return str(valor)
			else:
				#-- Para floats, usar formato que preserve decimales.
				if valor.is_integer():
					return str(int(valor))
				else:
					return str(valor)
		
		#-- Para cualquier otro tipo, convertir a string.
		return str(valor)
	
	def _convertir_booleano_a_si_no(self, valor):
		"""
		Convierte valores booleanos a formato Si/No específicamente para campos booleanos del modelo
		"""
		#-- Para valores vacíos o nulos, devolver "No"
		if valor is None or pd.isna(valor) or valor == '':
			return "No"
		
		#-- Si ya es string, verificar si representa un booleano
		if isinstance(valor, str):
			#-- Manejar casos especiales de pandas/Excel.
			if valor in ['nan', 'NaN', 'NAN', 'NULL', 'null']:
				return "No"
			
			#-- Convertir representaciones de booleanos a Si/No
			valor_lower = valor.lower().strip()
			true_values = ['true', 'yes', 'sí', 'si', 'verdadero', 'x', '✔', 'verdad', '1']
			false_values = ['false', 'no', 'not', 'falso', 'f', 'n', '0']
			
			if valor_lower in true_values:
				return "Si"
			elif valor_lower in false_values:
				return "No"
			
			#-- Si no coincide con ningún valor booleano conocido, devolver "No" por defecto
			return "No"
		
		#-- Para booleanos Python explícitos, convertir a Si/No.
		if isinstance(valor, bool):
			return "Si" if valor else "No"
		
		#-- Para números, considerar 1 como Si y otros como No
		if isinstance(valor, (int, float)):
			return "Si" if valor == 1 else "No"
		
		#-- Para cualquier otro tipo, devolver "No" por defecto
		return "No"
	
	def _preservar_formato_entero(self, valor):
		"""
		Preserva el formato de campos enteros, manejando valores vacíos y conversiones.
		"""
		if valor is None or pd.isna(valor) or valor == '':
			return 0
		
		#-- Si ya es entero, mantener como está.
		if isinstance(valor, int):
			return valor
		
		#-- Si es string, intentar convertir a numérico
		if isinstance(valor, str):
			#-- Manejar casos especiales
			if valor in ['nan', 'NaN', 'NAN', 'NULL', 'null']:
				return 0
			
			#-- Limpiar el string: reemplazar coma por punto y eliminar espacios.
			valor_limpio = valor.replace(',', '.').strip()
			
			#-- Intentar convertir a int.
			try:
				return int(valor_limpio)
			except (ValueError, TypeError):
				#-- Si no se puede convertir, devolver el valor original.
				return valor
		
		#-- Para cualquier otro tipo, intentar convertir a int.
		try:
			return int(valor)
		except (ValueError, TypeError):
			return valor
	
	def _preservar_formato_decimal(self, valor):
		"""
		Preserva el formato de campos decimales, manejando valores vacíos y conversiones.
		"""
		if valor is None or pd.isna(valor) or valor == '':
			return None
		
		#-- Si ya es numérico (float, int, Decimal), mantener como está.
		if isinstance(valor, (int, float, Decimal)):
			return valor
		
		#-- Si es string, intentar convertir a numérico
		if isinstance(valor, str):
			#-- Manejar casos especiales
			if valor in ['nan', 'NaN', 'NAN', 'NULL', 'null']:
				return None
			
			#-- Limpiar el string: reemplazar coma por punto y eliminar espacios.
			valor_limpio = valor.replace(',', '.').strip()
			
			#-- Intentar convertir a float
			try:
				return float(valor_limpio)
			except (ValueError, TypeError):
				#-- Si no se puede convertir, devolver el valor original.
				return valor
		
		#-- Para cualquier otro tipo, intentar convertir a float.
		try:
			return float(valor)
		except (ValueError, TypeError):
			return valor


class ActualizarEstadosPrevisualizarView(TemplateView):
	template_name = 'datatools/actualizar_estados_previsualizar.html'
	
	def get(self, request, *args, **kwargs):
		#-- Verificar que hay datos en la sesión antes de mostrar la previsualización.
		if 'actualizar_estados_excel_data' not in request.session:
			messages.error(request, 'No hay datos para previsualizar. Por favor, cargue un archivo Excel primero.')
			return redirect('actualizar_estados_cargar_excel')
		
		#-- Verificar que los datos no estén vacíos.
		actualizar_estados_excel_data = request.session.get('actualizar_estados_excel_data', {})
		if not actualizar_estados_excel_data.get('todos_los_datos'):
			messages.error(request, 'El archivo cargado está vacío. Por favor, cargue un archivo con datos.')
			return redirect('actualizar_estados_cargar_excel')
		
		return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		#-- Recuperar datos de la sesión.
		actualizar_estados_excel_data = self.request.session.get('actualizar_estados_excel_data', {})
		todos_los_datos = actualizar_estados_excel_data.get('todos_los_datos', [])
		
		#-- Obtener número de página del request.
		pagina_num = self.request.GET.get('pagina', 1)
		try:
			pagina_num = int(pagina_num)
		except (ValueError, TypeError):
			pagina_num = 1
		
		#-- Paginar los datos.
		paginator = Paginator(todos_los_datos, 100)
		
		try:
			pagina_datos = paginator.page(pagina_num)
		except:
			pagina_datos = paginator.page(1)
			pagina_num = 1
		
		context['nombre_archivo'] = actualizar_estados_excel_data.get('nombre_archivo', '')
		context['columnas'] = actualizar_estados_excel_data.get('columnas', [])
		context['datos'] = pagina_datos.object_list
		context['total_filas'] = actualizar_estados_excel_data.get('total_filas', 0)
		context['campos_protegidos'] = actualizar_estados_excel_data.get('campos_protegidos', [])
		context['etiquetas_protegidas'] = actualizar_estados_excel_data.get('etiquetas_protegidas', [])
		context['fecha'] = timezone.now()
		context['pagina_actual'] = pagina_num
		context['total_paginas'] = paginator.num_pages
		
		#-- Calcular rango de páginas.
		pagina_actual_num = context['pagina_actual']
		total_paginas = context['total_paginas']
		start_page = max(1, pagina_actual_num - 2)
		end_page = min(total_paginas, start_page + 4)
		
		if end_page - start_page < 4:
			start_page = max(1, end_page - 4)
		
		context['page_range'] = range(start_page, end_page + 1)
		context['page_start'] = (pagina_actual_num - 1) * 100 + 1
		context['page_end'] = min(pagina_actual_num * 100, context['total_filas'])
		
		return context


class ActualizarEstadosErroresView(TemplateView):
	template_name = 'datatools/actualizar_estados_errores.html'
	
	def get(self, request, *args, **kwargs):
		#-- Verificar que hay datos de errores en la sesión.
		if 'actualizar_estados_errores_procesamiento' not in request.session:
			messages.error(request, 'No hay datos de errores para mostrar.')
			return redirect('actualizar_estados_cargar_excel')
		
		#-- Obtener los datos.
		errores_data = request.session.get('actualizar_estados_errores_procesamiento', {})
		
		#-- Verificar si hay errores.
		if not errores_data.get('errores'):
			messages.error(request, 'No hay errores para mostrar.')
			return redirect('actualizar_estados_cargar_excel')
		
		return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		#-- Recuperar datos de errores de la sesión.
		errores_data = self.request.session.get('actualizar_estados_errores_procesamiento', {})
		
		context['errores'] = errores_data.get('errores', [])
		context['columnas'] = errores_data.get('columnas', [])
		context['total_registros'] = errores_data.get('total_registros', 0)
		context['campos_seleccionados'] = errores_data.get('campos_seleccionados', [])
		context['nombre_archivo'] = errores_data.get('nombre_archivo', '')
		context['fecha'] = timezone.now()
		
		#-- Obtener número de página del request.
		pagina_num = self.request.GET.get('pagina', 1)
		try:
			pagina_num = int(pagina_num)
		except (ValueError, TypeError):
			pagina_num = 1
		
		#-- Configurar paginación - SI filas_con_errores está vacío, usar datos alternativos.
		filas_con_errores = errores_data.get('filas_con_errores', [])
		if not filas_con_errores:
			#-- Si no hay filas con errores, crear una estructura básica para mostrar los errores.
			filas_con_errores = [{'row_index': i+1, 'error_message': error} for i, error in enumerate(context['errores'])]
		
		context['filas_con_errores'] = filas_con_errores
		
		#-- Paginar los datos.
		paginator = Paginator(filas_con_errores, 100)
		
		try:
			pagina_datos = paginator.page(pagina_num)
		except:
			pagina_datos = paginator.page(1)
			pagina_num = 1
		
		context['datos'] = pagina_datos.object_list
		context['pagina_actual'] = pagina_num
		context['total_paginas'] = paginator.num_pages
		context['page_start'] = (pagina_num - 1) * 100 + 1
		context['page_end'] = min(pagina_num * 100, len(filas_con_errores))
		
		#-- Calcular rango de páginas.
		start_page = max(1, pagina_num - 2)
		end_page = min(context['total_paginas'], start_page + 4)
		
		if end_page - start_page < 4:
			start_page = max(1, end_page - 4)
		
		context['page_range'] = range(start_page, end_page + 1)
		
		return context


class ActualizarEstadosView(TemplateView):
	template_name = 'datatools/actualizar_estados_resultado.html'
	
	def post(self, request, *args, **kwargs):
		#-- Obtener datos de la sesión.
		actualizar_estados_excel_data = request.session.get('actualizar_estados_excel_data', {})
		
		#-- Verificar que hay datos en la sesión.
		if not actualizar_estados_excel_data:
			messages.error(request, 'No hay datos para procesar. Por favor, cargue un archivo Excel primero.')
			return redirect('actualizar_estados_cargar_excel')
		
		#-- Obtener TODOS los datos de la sesión (ya procesados).
		todos_los_datos = actualizar_estados_excel_data.get('todos_los_datos', [])
		columnas_excel = actualizar_estados_excel_data.get('columnas', [])
		
		if not todos_los_datos:
			messages.error(request, 'No hay datos para procesar.')
			return redirect('actualizar_estados_cargar_excel')
		
		#-- Procesar los datos dentro de una transacción.
		try:
			with transaction.atomic():
				actualizados = 0
				creados = 0
				filas_con_errores = []
				errores = []
				estado_pocas = ProductoEstado.objects.get(nombre_producto_estado="POCAS")
				
				for index, fila in enumerate(todos_los_datos, 2):
					try:
						errores_en_fila = []
						
						# ========== VALIDACIÓN 1: CAI ==========
						cai = fila.get('CAI', '')
						#-- Asegurar que cai sea string y limpiarlo.
						if cai is None:
							cai = ''
						else:
							cai = str(cai).strip()
						
						if not cai:
							errores_en_fila.append("El campo CAI es obligatorio y no puede estar vacío")
						else:
							try:
								producto_cai = ProductoCai.objects.get(cai=cai)
							except ProductoCai.DoesNotExist:
								errores_en_fila.append(f"El CAI '{cai}' no existe en el sistema")
							except Exception as e:
								errores_en_fila.append(f"Error al buscar CAI '{cai}': {str(e)}")
						
						# ========== VALIDACIÓN 2: Stock Desde ==========
						stock_desde_valor = fila.get('Stock Desde', 0)
						
						#-- Convertir a string primero para manejar cualquier tipo de dato.
						if stock_desde_valor is None:
							stock_desde_str = ''
						else:
							stock_desde_str = str(stock_desde_valor).strip()
						
						#-- Validar que no esté vacío después de limpiar.
						if stock_desde_str == '':
							errores_en_fila.append("El campo Stock Desde no puede estar vacío")
						else:
							try:
								#-- Intentar convertir a entero.
								stock_desde = int(float(stock_desde_str)) if '.' in stock_desde_str else int(stock_desde_str)
								
								if stock_desde < 0:
									errores_en_fila.append("El Stock Desde no puede ser negativo")
							except (ValueError, TypeError):
								errores_en_fila.append(f"El Stock Desde '{stock_desde_valor}' debe ser un número entero válido")
							except Exception as e:
								errores_en_fila.append(f"Error al leer el Stock Desde: {str(e)}")
						
						# ========== VALIDACIÓN 3: Stock Hasta ==========
						stock_hasta_valor = fila.get('Stock Hasta', 0)
						
						#-- Convertir a string primero para manejar cualquier tipo de dato.
						if stock_hasta_valor is None:
							stock_hasta_str = ''
						else:
							stock_hasta_str = str(stock_hasta_valor).strip()
						
						#-- Validar que no esté vacío después de limpiar.
						if stock_hasta_str == '':
							errores_en_fila.append("El campo Stock Hasta no puede estar vacío")
						else:
							try:
								#-- Intentar convertir a entero.
								stock_hasta = int(float(stock_hasta_str)) if '.' in stock_hasta_str else int(stock_hasta_str)
								
								if stock_hasta < 0:
									errores_en_fila.append("El Stock Hasta no puede ser negativo")
							except (ValueError, TypeError):
								errores_en_fila.append(f"El Stock Hasta '{stock_hasta_valor}' debe ser un número entero válido")
							except Exception as e:
								errores_en_fila.append(f"Error al leer el Stock Hasta: {str(e)}")
						
						# ========== VALIDACIÓN 4: Stock Hasta <= Stock Desde ==========
						#-- Solo validar si no hay errores previos en estos campos.
						if not any("Stock Desde" in error or "Stock Hasta" in error for error in errores_en_fila):
							if stock_hasta < stock_desde:
								errores_en_fila.append("El Stock Hasta no puede ser menor que el Stock Desde")						
						
						# ========== Si hay errores, guardar fila con error ==========
						if errores_en_fila:
							fila_con_error = fila.copy()
							fila_con_error['error_message'] = "; ".join(errores_en_fila)
							fila_con_error['error_list'] = errores_en_fila
							fila_con_error['row_index'] = index
							filas_con_errores.append(fila_con_error)
							errores.extend(errores_en_fila)
							continue
						
						# ========== PROCESAR SI NO HAY ERRORES ==========
						try:
							#-- Buscar si ya existe el registro.
							medida_estado, creado = MedidasEstados.objects.get_or_create(
								id_cai=producto_cai,
								id_estado=estado_pocas,
								defaults={
									'stock_desde': stock_desde,
									'stock_hasta': stock_hasta
								}
							)
							
							if not creado:
								#-- Si ya existe, actualizar los valores si cambiaron.
								if medida_estado.stock_desde != stock_desde or medida_estado.stock_hasta != stock_hasta:
									medida_estado.stock_desde = stock_desde
									medida_estado.stock_hasta = stock_hasta
									medida_estado.save()
									actualizados += 1
									print(f"Registro actualizado para CAI {cai}: Stock Desde {stock_desde}, Stock Hasta {stock_hasta}")
								#-- Si no cambió, no contar como actualizado.
							else:
								#-- Si fue creado nuevo.
								creados += 1
						
						except Exception as e:
							error_clean = str(e).replace("['", "").replace("']", "").replace("'", "")
							error_msg = f"Error al procesar el registro - {error_clean}"
							errores.append(error_msg)
							
							fila_con_error = fila.copy()
							fila_con_error['error_message'] = error_msg
							fila_con_error['error_list'] = [error_msg]
							fila_con_error['row_index'] = index
							filas_con_errores.append(fila_con_error)
					
					except Exception as e:
						error_clean = str(e).replace("['", "").replace("']", "").replace("'", "")
						error_msg = f"Error inesperado al procesar fila - {error_clean}"
						errores.append(error_msg)
						
						fila_con_error = fila.copy()
						fila_con_error['error_message'] = error_msg
						fila_con_error['row_index'] = index
						filas_con_errores.append(fila_con_error)
						continue
				
				# ========== Si hay errores, revertir transacción ==========
				if errores:
					request.session['actualizar_estados_errores_procesamiento'] = {
						'errores': errores,
						'filas_con_errores': filas_con_errores,
						'columnas': columnas_excel,
						'total_registros': len(todos_los_datos),
						'nombre_archivo': actualizar_estados_excel_data.get('nombre_archivo', '')
					}
					request.session.modified = True
					raise ValidationError("Errores encontrados durante el procesamiento")
				
				# ========== Preparar contexto para mostrar resultados (éxito) ==========
				context = self.get_context_data()
				context['total_registros'] = len(todos_los_datos)
				context['actualizados'] = actualizados
				context['creados'] = creados
				context['errores'] = []
				context['mensaje_exito'] = f"Procesamiento completado: {creados} nuevos registros creados, {actualizados} registros actualizados"
				
				#-- Limpiar sesión.
				keys_to_remove = ['actualizar_estados_excel_data']
				for key in keys_to_remove:
					if key in request.session:
						del request.session[key]
				
				return self.render_to_response(context)
		
		except ValidationError as e:
			#-- Redirigir a la vista de errores.
			return redirect('actualizar_estados_errores')
		
		except Exception as e:
			#-- Error inesperado.
			error_clean = str(e).replace("['", "").replace("']", "").replace("'", "")
			messages.error(request, f'Error inesperado durante el procesamiento: {error_clean}')
			return redirect('actualizar_estados_cargar_excel')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['fecha'] = timezone.now()
		return context

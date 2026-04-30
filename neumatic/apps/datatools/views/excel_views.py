# apps\datatools\views\excel_views.py
import re
import pandas as pd
from django.core.paginator import Paginator
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ValidationError, FieldDoesNotExist
from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.db.models import (
	CharField, TextField, IntegerField, BigIntegerField, 
	DecimalField, FloatField, BooleanField, DateField, 
	DateTimeField, ForeignKey, AutoField, NOT_PROVIDED
)

from ..forms.excel_forms import ExcelUploadForm, CamposActualizacionForm
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.base_models import ProductoCai, AlicuotaIva


class ExcelUploadView(FormView):
	template_name = 'datatools/excel_upload.html'
	form_class = ExcelUploadForm
	success_url = reverse_lazy('excel_preview')
	
	def get(self, request, *args, **kwargs):
		#-- Limpiar datos anteriores al mostrar el formulario
		keys_to_remove = ['excel_data', 'errores_procesamiento']
		for key in keys_to_remove:
			if key in self.request.session:
				del self.request.session[key]
		
		return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['fecha'] = timezone.now()
		context['proceso'] = self.request.GET.get('proceso', 'actualizar')
		return context
	
	def form_valid(self, form):
		from apps.informes.views.vllista_list_views import ConfigViews
		
		#-- LIMPIAR datos anteriores antes de guardar nuevos.
		keys_to_remove = ['excel_data', 'errores_procesamiento']
		for key in keys_to_remove:
			if key in self.request.session:
				del self.request.session[key]
		
		archivo = form.cleaned_data['archivo_excel']
		
		try:
			if archivo.name.endswith('.xlsx') or archivo.name.endswith('.xls'):
				#-- PRIMERO: Leer solo los nombres de columnas para identificar tipos.
				df_headers = pd.read_excel(archivo, nrows=0)
				columnas_excel = df_headers.columns.tolist()
				
				#-- Identificar tipos de campos.
				columnas_id = []
				columnas_como_texto = []
				columnas_booleanas = []
				columnas_decimales = []
				columnas_enteras = []
				
				for key, value in ConfigViews.table_info.items():
					if value.get('excel') and value['label'] in columnas_excel:
						try:
							campo_obj = Producto._meta.get_field(key)
							
							if isinstance(campo_obj, (ForeignKey, AutoField)):
								columnas_id.append(value['label'])
							elif isinstance(campo_obj, (CharField, TextField)):
								columnas_como_texto.append(value['label'])
							elif isinstance(campo_obj, BooleanField):
								columnas_booleanas.append(value['label'])
							elif isinstance(campo_obj, (DecimalField, FloatField)):
								columnas_decimales.append(value['label'])
							elif isinstance(campo_obj, (IntegerField, BigIntegerField)):
								columnas_enteras.append(value['label'])
							
						except FieldDoesNotExist:
							continue
				
				#-- Leer el Excel con todas las columnas como string.
				df = pd.read_excel(archivo, na_filter=False, dtype=str, keep_default_na=False)
				
				#-- Verificar si el DataFrame está vacío.
				if df.empty:
					form.add_error('archivo_excel', 'El archivo Excel está vacío.')
					return self.form_invalid(form)
				
				#-- Verificar que las columnas coincidan con las esperadas.
				columnas_esperadas = [value['label'] for value in ConfigViews.table_info.values() if value['excel']]
				if set(columnas_esperadas) != set(columnas_excel):
					form.add_error('archivo_excel', f'Las columnas del archivo no coinciden con las esperadas.')
					return self.form_invalid(form)
				
				#-- AHORA: Convertir y limpiar los datos según el tipo.
				
				#-- 1. Procesar columnas decimales: convertir a float o 0.0 si está vacío.
				for columna in columnas_decimales:
					if columna in df.columns:
						df[columna] = df[columna].apply(self._convertir_decimal_seguro)
				
				#-- 2. Procesar columnas enteras (no ID): convertir a int o 0 si está vacío.
				for columna in columnas_enteras:
					if columna in df.columns:
						df[columna] = df[columna].apply(self._convertir_entero_seguro)
				
				#-- 3. Asegurar que los campos string mantengan formato exacto.
				for columna in columnas_como_texto:
					if columna in df.columns:
						df[columna] = df[columna].apply(lambda x: self._preservar_formato_exacto(x))
				
				#-- 4. Convertir campos booleanos a formato Si/No.
				for columna in columnas_booleanas:
					if columna in df.columns:
						df[columna] = df[columna].apply(lambda x: self._convertir_booleano_a_si_no(x))
				
				#-- 5. Convertir campos específicos a mayúsculas.
				campos_a_mayusculas = ['Tipo Producto']
				
				for columna in campos_a_mayusculas:
					if columna in df.columns:
						df[columna] = df[columna].apply(
							lambda x: str(x).strip().upper() if x and pd.notna(x) and str(x).strip() else x
						)
				
				#-- Generar lista de campos protegidos y sus etiquetas.
				campos_protegidos = [campo for campo, info in ConfigViews.table_info.items() if info.get('protected', False)]
				etiquetas_protegidas = [info['label'] for info in ConfigViews.table_info.values() if info.get('protected', False)]
				
				#-- Mapear Columnas del Excel a nombres de campos {"label": producto.campo}.
				label_to_field_map = {value['label']: key for key, value in ConfigViews.table_info.items() if value['label'] in columnas_excel}
				
				#-- Limpiar datos (solo valores específicos, no formato).
				df = df.replace(['nan', 'NaN', 'NAN', 'NULL', 'null', 'None'], None)
				
				#-- Convertir a lista de diccionarios y guardar en sesión.
				todos_los_datos = df.to_dict('records')
				total_filas = len(todos_los_datos)
				
				#-- Guardar en sesión - optimizado para grandes volúmenes.
				self.request.session['excel_data'] = {
					'columnas': list(df.columns),
					'todos_los_datos': todos_los_datos,
					'total_filas': total_filas,
					'nombre_archivo': archivo.name,
					'campos_protegidos': campos_protegidos,
					'etiquetas_protegidas': etiquetas_protegidas,
					'etiquetas_a_campos_map': label_to_field_map,
					'columnas_id': columnas_id,
					'columnas_booleanas': columnas_booleanas,
					'proceso': self.request.GET.get('proceso', 'actualizar')
				}
				
				return super().form_valid(form)
			else:
				form.add_error('archivo_excel', 'El archivo debe ser en formato Excel (.xlsx o .xls)')
				return self.form_invalid(form)
			
		except Exception as e:
			form.add_error('archivo_excel', f'Error al procesar el archivo: {str(e)}')
			return self.form_invalid(form)
	
	def _convertir_decimal_seguro(self, valor):
		"""
		Convierte valores a float, devolviendo 0.0 para valores vacíos.
		"""
		if valor is None or pd.isna(valor) or valor == '' or valor in ['nan', 'NaN', 'NAN', 'NULL', 'null', 'None']:
			return 0.0
		
		if isinstance(valor, (int, float)):
			return float(valor)
		
		if isinstance(valor, str):
			#-- Limpiar el string: reemplazar coma por punto y eliminar espacios.
			valor_limpio = valor.replace(',', '.').strip()
			try:
				return float(valor_limpio)
			except (ValueError, TypeError):
				return 0.0
		
		return 0.0
	
	def _convertir_entero_seguro(self, valor):
		"""
		Convierte valores a int, devolviendo 0 para valores vacíos.
		"""
		if valor is None or pd.isna(valor) or valor == '' or valor in ['nan', 'NaN', 'NAN', 'NULL', 'null', 'None']:
			return 0
		
		if isinstance(valor, (int, float)):
			return int(valor)
		
		if isinstance(valor, str):
			#-- Limpiar el string.
			valor_limpio = valor.strip()
			try:
				#-- Intentar convertir a float primero (por si tiene decimales).
				return int(float(valor_limpio))
			except (ValueError, TypeError):
				return 0
		
		return 0
	
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
		#-- Para valores vacíos o nulos, devolver "No".
		if valor is None or pd.isna(valor) or valor == '':
			return "No"
		
		#-- Si ya es string, verificar si representa un booleano.
		if isinstance(valor, str):
			#-- Manejar casos especiales de pandas/Excel.
			if valor in ['nan', 'NaN', 'NAN', 'NULL', 'null']:
				return "No"
			
			#-- Convertir representaciones de booleanos a Si/No.
			valor_lower = valor.lower().strip()
			true_values = ['true', 'yes', 'sí', 'si', 'verdadero', 'x', '✔', 'verdad', '1']
			false_values = ['false', 'no', 'not', 'falso', 'f', 'n', '0']
			
			if valor_lower in true_values:
				return "Si"
			elif valor_lower in false_values:
				return "No"
			
			#-- Si no coincide con ningún valor booleano conocido, devolver "No" por defecto.
			return "No"
		
		#-- Para booleanos Python explícitos, convertir a Si/No.
		if isinstance(valor, bool):
			return "Si" if valor else "No"
		
		#-- Para números, considerar 1 como Si y otros como No.
		if isinstance(valor, (int, float)):
			return "Si" if valor == 1 else "No"
		
		#-- Para cualquier otro tipo, devolver "No" por defecto.
		return "No"


class ExcelPreviewView(TemplateView):
	template_name = 'datatools/excel_preview.html'
	
	def get(self, request, *args, **kwargs):
		#-- Verificar que hay datos en la sesión antes de mostrar la previsualización.
		if 'excel_data' not in request.session:
			messages.error(request, 'No hay datos para previsualizar. Por favor, cargue un archivo Excel primero.')
			return redirect('cargar_excel')
		
		#-- Verificar que los datos no estén vacíos.
		excel_data = request.session.get('excel_data', {})
		if not excel_data.get('todos_los_datos'):
			messages.error(request, 'El archivo cargado está vacío. Por favor, cargue un archivo con datos.')
			return redirect('cargar_excel')
		
		return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		#-- Recuperar datos de la sesión.
		excel_data = self.request.session.get('excel_data', {})
		todos_los_datos = excel_data.get('todos_los_datos', [])
		
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
		
		context['nombre_archivo'] = excel_data.get('nombre_archivo', '')
		context['columnas'] = excel_data.get('columnas', [])
		context['datos'] = pagina_datos.object_list
		context['total_filas'] = excel_data.get('total_filas', 0)
		context['campos_protegidos'] = excel_data.get('campos_protegidos', [])
		context['etiquetas_protegidas'] = excel_data.get('etiquetas_protegidas', [])
		context['fecha'] = timezone.now()
		context['pagina_actual'] = pagina_num
		context['total_paginas'] = paginator.num_pages
		context['proceso'] = excel_data.get('proceso', 'actualizar')
		context['columnas_id'] = excel_data.get('columnas_id', [])
		context['columnas_booleanas'] = excel_data.get('columnas_booleanas', [])
		
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
		
		#-- Formulario para selección de campos.
		form_campos = CamposActualizacionForm(
			columnas=context['columnas'],
			etiquetas_protegidas=context['etiquetas_protegidas']
		)
		context['form_campos'] = form_campos
		
		return context


class MostrarErroresExcelView(TemplateView):
	template_name = 'datatools/errores_excel.html'
	
	def get(self, request, *args, **kwargs):
		#-- Verificar que hay datos de errores en la sesión.
		if 'errores_procesamiento' not in request.session:
			messages.error(request, 'No hay datos de errores para mostrar.')
			return redirect('cargar_excel')
		
		#-- Obtener los datos.
		errores_data = request.session.get('errores_procesamiento', {})
		
		#-- Verificar si hay errores.
		if not errores_data.get('errores'):
			messages.error(request, 'No hay errores para mostrar.')
			return redirect('cargar_excel')
			
		return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		#-- Recuperar datos de errores de la sesión.
		errores_data = self.request.session.get('errores_procesamiento', {})
		
		context['errores'] = errores_data.get('errores', [])
		context['columnas'] = errores_data.get('columnas', [])
		context['total_registros'] = errores_data.get('total_registros', 0)
		context['campos_seleccionados'] = errores_data.get('campos_seleccionados', [])
		context['nombre_archivo'] = errores_data.get('nombre_archivo', '')
		context['fecha'] = timezone.now()
		context['proceso'] = self.request.session.get('excel_data', {}).get('proceso', 'actualizar')
		
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


class ActualizarProductosView(TemplateView):
	template_name = 'datatools/resultado_productos.html'
	
	def post(self, request, *args, **kwargs):
		#-- Obtener datos de la sesión.
		excel_data = request.session.get('excel_data', {})
		
        #-- Verificar que hay datos en la sesión.
		if not excel_data:
			messages.error(request, 'No hay datos para procesar. Por favor, cargue un archivo Excel primero.')
			return redirect('cargar_excel')
		
		columnas_excel = excel_data.get('columnas', [])
		protected_fields = excel_data.get('campos_protegidos', [])
		protected_labels = excel_data.get('etiquetas_protegidas', [])
		label_to_field_map = excel_data.get('etiquetas_a_campos_map', {})
		
		campos_protegidos = protected_fields + protected_labels
		campos_protegidos = list(set(campos_protegidos))  # Eliminar duplicados.
		
		#-- Obtener campos seleccionados por el usuario
		campos_seleccionados = []
		for columna_label in columnas_excel:
			campo_post = f'actualizar_{columna_label}'
			if request.POST.get(campo_post) and columna_label in label_to_field_map:
				campo_modelo = label_to_field_map[columna_label]
				campos_seleccionados.append((columna_label, campo_modelo))
		
		if not campos_seleccionados:
			messages.error(request, 'Debe seleccionar al menos un campo para actualizar.')
			return redirect('excel_preview')
		
		#-- Obtener TODOS los datos de la sesión (ya procesados).
		todos_los_datos = excel_data.get('todos_los_datos', [])
		
		if not todos_los_datos:
			messages.error(request, 'No hay datos para procesar.')
			return redirect('cargar_excel')
		
		#-- Mapeo de tipos de datos para validación.
		tipo_validaciones = {
			'string': validar_string,
			'integer': validar_integer,
			'decimal': validar_decimal,
			'boolean': validar_boolean,
			'date': validar_date,
			'datetime': validar_datetime,
			'foreign_key': validar_foreign_key,
		}
		
		#-- Procesar los datos dentro de una transacción.
		try:
			with transaction.atomic():
				actualizados = 0
				errores = []
				filas_con_errores = []
				
				for index, fila in enumerate(todos_los_datos, 1):
					index +=1  #-- Ajustar índice para que coincida con fila Excel.
					
					try:
						codigo = fila.get('Código')
						if not codigo:
							error_msg = f"No se especificó código de producto"
							errores.append(error_msg)
							#-- Guardar información de la fila con error.
							fila_con_error = fila.copy()
							fila_con_error['error_message'] = error_msg
							fila_con_error['row_index'] = index
							filas_con_errores.append(fila_con_error)
							continue
						
						#-- Buscar el producto por código.
						try:
							producto = Producto.objects.get(id_producto=codigo)
						except Producto.DoesNotExist:
							error_msg = f"Producto con código '{codigo}' no existe"
							errores.append(error_msg)
							#-- Guardar información de la fila con error.
							fila_con_error = fila.copy()
							fila_con_error['error_message'] = error_msg
							fila_con_error['row_index'] = index
							filas_con_errores.append(fila_con_error)
							continue
						
						#-- Actualizar los campos seleccionados.
						cambios_realizados = False
						errores_en_fila = []
						
						for columna_label, campo_modelo in campos_seleccionados:
							#-- Saltar campos protegidos
							if campo_modelo in campos_protegidos or columna_label in campos_protegidos:
								continue
							
							#-- Comprobar si la columna existe en la fila.
							if columna_label in fila:
								#-- Obtener el valor de la celda.
								valor = fila[columna_label]
								
								#----------------------------------------------------
								
								#-- MANEJO ESPECIAL PARA EL CAMPO CAI.
								if columna_label == "CAI":
									#-- Buscar el ProductoCai por el valor del campo cai.
									try:
										if valor in ['', None, 'NULL', 'null', 'NaN', 'nan']:
											#-- Si el valor está vacío, establecer id_cai como None.
											valor_final = None
										else:
											#-- Buscar el ProductoCai por el valor cai.
											productocai = ProductoCai.objects.get(cai=valor)
											valor_final = productocai.id_cai
										
										#-- Verificar si el valor cambió.
										if producto.id_cai_id != valor_final:
											producto.id_cai_id = valor_final
											cambios_realizados = True
										
										#-- Saltar el procesamiento normal para el campo CAI.
										continue
										
									except ProductoCai.DoesNotExist:
										error_msg = f"CAI - '{valor}' no existe en la base de datos"
										errores.append(error_msg)
										errores_en_fila.append(error_msg)
										
										continue
									
									except Exception as e:
										error_msg = f"Error al procesar CAI '{valor}' - {str(e)}"
										errores.append(error_msg)
										errores_en_fila.append(error_msg)
										continue
								
								#-- MANEJO ESPECIAL PARA EL CAMPO ALICUOTA IVA
								if columna_label == "Alic. IVA":
									#-- Buscar la AlicuotaIva por el valor del campo alicuota_iva.
									try:
										if valor in ['', None, 'NULL', 'null', 'NaN', 'nan']:
											valor_final = None
										else:
											try:
												if isinstance(valor, str):
													valor = valor.replace(',', '.').strip()
												
												alicuota = AlicuotaIva.objects.get(alicuota_iva=Decimal(str(valor)))
												valor_final = alicuota.id_alicuota_iva
												
											except AlicuotaIva.DoesNotExist:
												error_msg = f"Alic. IVA - En la Base de Datos no está registrada una alícuota con valor '{valor}'"
												errores.append(error_msg)
												errores_en_fila.append(error_msg)
												continue
											except (ValueError, InvalidOperation) as e:
												error_msg = f"Alic. IVA - Valor inválido: '{valor}'"
												errores.append(error_msg)
												errores_en_fila.append(error_msg)
												continue
										
										#-- Verificar si el valor cambió
										if producto.id_alicuota_iva_id != valor_final:
											producto.id_alicuota_iva_id = valor_final
											cambios_realizados = True
										
										continue
										
									except Exception as e:
										error_msg = f"Alic. IVA - Error al procesar '{valor}' - {str(e)}"
										errores.append(error_msg)
										errores_en_fila.append(error_msg)
										continue
								
								#----------------------------------------------------
								#-- Obtener el tipo de campo del modelo.
								try:
									campo_obj = Producto._meta.get_field(campo_modelo)
									# tipo_dato = campo_obj.get_internal_type()
									
									#-- Determinar tipo de dato dinámicamente.
									tipo_dato = obtener_tipo_campo_desde_modelo(campo_obj)
									especificaciones = obtener_especificaciones_campo(campo_obj)
									
									#-- Validar campos obligatorios.
									if campo_obj.blank is False and campo_obj.null is False:
										#-- Campo es obligatorio en el modelo.
										if valor in ['', None, 'NULL', 'null', 'NaN', 'nan']:
											error_msg = f"{columna_label} - Es obligatorio y no puede estar vacío"
											errores.append(error_msg)
											errores_en_fila.append(error_msg)
											continue
									
									#-- Usar el valor por defecto del modelo para valores vacíos.
									if valor in ['', None, 'NULL', 'null', 'NaN', 'nan']:
										if campo_obj.default is not NOT_PROVIDED:
											#-- Usar el valor por defecto definido en el modelo.
											valor = campo_obj.default
										elif isinstance(campo_obj, (DecimalField, FloatField, IntegerField)):
											#-- Si no hay valor por defecto definido, usar 0 para numéricos.
											valor = 0
										else:
											valor = None
									else:
										#-- Validar y convertir el valor según el tipo de campo.
										try:
											if tipo_dato in tipo_validaciones:
												valor = tipo_validaciones[tipo_dato](valor, campo_obj, especificaciones)
											else:
												valor = validar_generico(valor, campo_obj, especificaciones)
										except ValidationError as e:
											#-- Extraer solo el mensaje sin los corchetes.
											error_clean = str(e).replace("['", "").replace("']", "").replace("'", "")
											error_msg = f"{columna_label} - {error_clean}"
											errores.append(error_msg)
											errores_en_fila.append(error_msg)
											continue
									
									#-- Verificar si el valor realmente cambió.
									valor_actual = getattr(producto, campo_modelo)
									
									#-- Comparación segura para tipos numéricos.
									if isinstance(valor, (int, float, Decimal)) and isinstance(valor_actual, (int, float, Decimal)):
										valor_cambio = abs(float(valor) - float(valor_actual)) > 0.001
									else:
										valor_cambio = valor != valor_actual
									
									#-- Asignar el nuevo valor si cambió.
									if valor_cambio:
										setattr(producto, campo_modelo, valor)
										cambios_realizados = True
								
								except FieldDoesNotExist:
									error_msg = f"El campo: '{campo_modelo}' no existe en el modelo."
									errores.append(error_msg)
									errores_en_fila.append(error_msg)
									
									continue
						
						#-- Si hubo errores en esta fila, guardarla completa.
						if errores_en_fila:
							fila_con_error = fila.copy()
							fila_con_error['error_message'] = "; ".join(errores_en_fila)
							fila_con_error['error_list'] = errores_en_fila
							fila_con_error['row_index'] = index
							filas_con_errores.append(fila_con_error)
						
						#-- Solo guardar si no hay errores y hay cambios.
						if cambios_realizados and not errores_en_fila:
							try:
								producto.save()
								actualizados += 1
								
							except Exception as e:
								#-- Guardar información de la fila con error.
								#-- Limpiar el mensaje de error si tiene corchetes.
								error_clean = str(e).replace("['", "").replace("']", "").replace("'", "")
								error_msg = f"Error al guardar cambios - {error_clean}"
								errores.append(error_msg)
								fila_con_error = fila.copy()
								fila_con_error['error_message'] = error_msg
								fila_con_error['row_index'] = index
								filas_con_errores.append(fila_con_error)
						
					except Exception as e:
						#-- Capturar cualquier error inesperado en la fila.
						#-- Limpiar el mensaje de error si tiene corchetes.
						error_clean = str(e).replace("['", "").replace("']", "").replace("'", "")
						error_msg = f"Error al procesar - {error_clean}"
						errores.append(error_msg)
						
						#-- Guardar información de la fila con error.
						fila_con_error = fila.copy()
						fila_con_error['error_message'] = error_msg
						fila_con_error['row_index'] = index
						filas_con_errores.append(fila_con_error)
						
						continue #-- Continuar con la siguiente fila.
				
				#-- Si hay errores, lanzar excepción para revertir la transacción.
				if errores:
					#-- Guardar información de errores en la sesión antes de lanzar la excepción.
					request.session['errores_procesamiento'] = {
						'errores': errores,
						'filas_con_errores': filas_con_errores,
						'columnas': columnas_excel,
						'total_registros': len(todos_los_datos),
						'campos_seleccionados': [columna for columna, _ in campos_seleccionados],
						'nombre_archivo': excel_data.get('nombre_archivo', '')
					}
					request.session.modified = True  #-- Asegurar que la sesión se guarde.
					raise ValidationError("Errores encontrados durante el procesamiento")
				
				#-- Preparar contexto para mostrar resultados (éxito).
				context = self.get_context_data()
				context['total_registros'] = len(todos_los_datos)
				context['actualizados'] = actualizados
				context['errores'] = []
				# context['campos_actualizados'] = [columna for columna, _ in campos_seleccionados]
				
				#-- Limpiar sesión.
				keys_to_remove = ['excel_data']
				for key in keys_to_remove:
					if key in request.session:
						del request.session[key]
				
				return self.render_to_response(context)
		
		except ValidationError as e:
			#-- Redirigir a la vista de errores.
			return redirect('mostrar_errores_excel')
		
		except Exception as e:
			#-- Error inesperado
			messages.error(request, f'Error inesperado durante el procesamiento: {str(e)}')
			return redirect('excel_preview')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['proceso'] = self.request.session.get('excel_data', {}).get('proceso', 'actualizar')
		context['fecha'] = timezone.now()
		return context


class AgregarProductosView(TemplateView):
	template_name = 'datatools/resultado_productos.html'
	
	def post(self, request, *args, **kwargs):
		#-- Obtener datos de la sesión.
		excel_data = request.session.get('excel_data', {})
		
		#-- Verificar que hay datos en la sesión.
		if not excel_data:
			messages.error(request, 'No hay datos para procesar. Por favor, cargue un archivo Excel primero.')
			return redirect('cargar_excel')
		
		columnas_excel = excel_data.get('columnas', [])
		label_to_field_map = excel_data.get('etiquetas_a_campos_map', {})
		
		#-- Obtener TODOS los datos de la sesión (ya procesados).
		todos_los_datos = excel_data.get('todos_los_datos', [])
		
		if not todos_los_datos:
			messages.error(request, 'No hay datos para procesar.')
			return redirect('cargar_excel')
		
		#-- Mapeo de tipos de datos para validación.
		tipo_validaciones = {
			'string': validar_string,
			'integer': validar_integer,
			'decimal': validar_decimal,
			'boolean': validar_boolean,
			'date': validar_date,
			'datetime': validar_datetime,
			'foreign_key': validar_foreign_key,
		}
		
		#-- Procesar los datos dentro de una transacción.
		try:
			with transaction.atomic():
				agregados = 0
				errores = []
				filas_con_errores = []
				
				for index, fila in enumerate(todos_los_datos, 1):
					index +=1  #-- Ajustar índice para que coincida con fila Excel.
					
					try:
						#-- Crear nuevo producto.
						producto = Producto()
						
						#-- Actualizar los campos seleccionados.
						errores_en_fila = []
						
						for columna_label, campo_modelo in label_to_field_map.items():
							#-- Saltar la columna Código porque el id se genera automáticamente.
							if columna_label == 'Código' or campo_modelo == 'id_producto':
								continue
							
							#-- Comprobar si la columna existe en la fila.
							if columna_label in fila:
								#-- Obtener el valor de la celda.
								valor = fila[columna_label]
								
								#-- MANEJO ESPECIAL PARA EL CAMPO CAI.
								if columna_label == "CAI":
									#-- Buscar el ProductoCai por el valor del campo cai.
									try:
										if valor not in ['', None, 'NULL', 'null', 'NaN', 'nan']:
											#-- Buscar el ProductoCai por el valor cai.
											productocai = ProductoCai.objects.get(cai=valor)
											producto.id_cai = productocai
										
										#-- Saltar el procesamiento normal para el campo CAI.
										continue
										
									except ProductoCai.DoesNotExist:
										error_msg = f"CAI - '{valor}' no existe en la base de datos"
										errores.append(error_msg)
										errores_en_fila.append(error_msg)
										continue
									
									except Exception as e:
										error_msg = f"Error al procesar CAI '{valor}' - {str(e)}"
										errores.append(error_msg)
										errores_en_fila.append(error_msg)
										continue
								
								#-- MANEJO ESPECIAL PARA EL CAMPO TIPO PRODUCTO.
								if columna_label == "Tipo Producto":
									#-- Validar que sea obligatorio
									if valor in ['', None, 'NULL', 'null', 'NaN', 'nan']:
										error_msg = f"Tipo Producto - Es obligatorio y no puede estar vacío"
										errores.append(error_msg)
										errores_en_fila.append(error_msg)
										continue
									
									#-- Asegurar que esté en mayúsculas (por si acaso)
									valor = str(valor).strip().upper()
									
									#-- Validación estricta: solo "P" o "S"
									if valor not in ['P', 'S']:
										error_msg = f"Tipo Producto - Debe ser 'P' (Producto) o 'S' (Servicio). Valor recibido: '{valor}'"
										errores.append(error_msg)
										errores_en_fila.append(error_msg)
										continue
									
									#-- Asignar el valor validado
									producto.tipo_producto = valor
									continue  #-- Saltar el procesamiento normal para este campo
								
								#-- MANEJO ESPECIAL PARA EL CAMPO ALICUOTA IVA
								if columna_label == "Alic. IVA":
									#-- Buscar la AlicuotaIva por el valor del campo alicuota_iva
									try:
										if valor in ['', None, 'NULL', 'null', 'NaN', 'nan']:
											#-- Si el valor está vacío, usar valor por defecto o None
											#-- Depende de si el campo es obligatorio en tu modelo
											valor_final = None
										else:
											#-- Convertir a decimal para la búsqueda
											try:
												#-- Limpiar y convertir el valor
												if isinstance(valor, str):
													valor = valor.replace(',', '.').strip()
												
												#-- Buscar la AlicuotaIva por el valor de alicuota_iva
												alicuota = AlicuotaIva.objects.get(alicuota_iva=Decimal(str(valor)))
												valor_final = alicuota.id_alicuota_iva
												
											except AlicuotaIva.DoesNotExist:
												error_msg = f"Alic. IVA - En la Base de Datos no está registrada una alícuota con valor '{valor}'"
												errores.append(error_msg)
												errores_en_fila.append(error_msg)
												continue
											except (ValueError, InvalidOperation) as e:
												error_msg = f"Alic. IVA - Valor inválido: '{valor}'"
												errores.append(error_msg)
												errores_en_fila.append(error_msg)
												continue
										
										#-- Asignar el ID de la alícuota encontrada
										producto.id_alicuota_iva_id = valor_final
										continue  #-- Saltar el procesamiento normal para este campo
										
									except Exception as e:
										error_msg = f"Alic. IVA - Error al procesar '{valor}' - {str(e)}"
										errores.append(error_msg)
										errores_en_fila.append(error_msg)
										continue
								
								#-- Obtener el tipo de campo del modelo.
								try:
									campo_obj = Producto._meta.get_field(campo_modelo)
									# tipo_dato = campo_obj.get_internal_type()
									
									#-- Determinar tipo de dato dinámicamente.
									tipo_dato = obtener_tipo_campo_desde_modelo(campo_obj)
									especificaciones = obtener_especificaciones_campo(campo_obj)
									
									#-- Validar campos obligatorios.
									if campo_obj.blank is False and campo_obj.null is False:
										#-- Campo es obligatorio en el modelo.
										if valor in ['', None, 'NULL', 'null', 'NaN', 'nan']:
											error_msg = f"{columna_label} - Es obligatorio y no puede estar vacío"
											errores.append(error_msg)
											errores_en_fila.append(error_msg)
											continue
									
									#-- Usar el valor por defecto del modelo para valores vacíos.
									if valor in ['', None, 'NULL', 'null', 'NaN', 'nan']:
										if campo_obj.default is not NOT_PROVIDED:
											#-- Usar el valor por defecto definido en el modelo.
											valor = campo_obj.default
										elif isinstance(campo_obj, (DecimalField, FloatField, IntegerField)):
											#-- Si no hay valor por defecto definido, usar 0 para numéricos.
											valor = 0
										else:
											valor = None
									else:
										#-- Validar y convertir el valor según el tipo de campo.
										try:
											if tipo_dato in tipo_validaciones:
												valor = tipo_validaciones[tipo_dato](valor, campo_obj, especificaciones)
											else:
												valor = validar_generico(valor, campo_obj, especificaciones)
										except ValidationError as e:
											#-- Extraer solo el mensaje sin los corchetes.
											error_clean = str(e).replace("['", "").replace("']", "").replace("'", "")
											error_msg = f"{columna_label} - {error_clean}"
											errores.append(error_msg)
											errores_en_fila.append(error_msg)
											continue
									
									#-- Asignar el valor de la celda al campo del nuevo objeto.
									setattr(producto, campo_modelo, valor)
									
								except FieldDoesNotExist:
									error_msg = f"El campo: '{campo_modelo}' no existe en el modelo."
									errores.append(error_msg)
									errores_en_fila.append(error_msg)
									continue
						
						#-- Si hubo errores en esta fila, guardarla completa.
						if errores_en_fila:
							fila_con_error = fila.copy()
							fila_con_error['error_message'] = "; ".join(errores_en_fila)
							fila_con_error['error_list'] = errores_en_fila
							fila_con_error['row_index'] = index
							filas_con_errores.append(fila_con_error)
						
						#-- VALIDACIÓN ESPECÍFICA: Obliga Operario solo para Servicios
						elif (hasattr(producto, 'tipo_producto') and hasattr(producto, 'obliga_operario') and producto.tipo_producto == 'P' and producto.obliga_operario is True):
							error_msg = "Obliga Operario - Solo puede estar marcado para servicios (Tipo Producto = 'S')"
							errores.append(error_msg)
							errores_en_fila.append(error_msg)
							
							fila_con_error = fila.copy()
							fila_con_error['error_message'] = "; ".join(errores_en_fila)
							fila_con_error['error_list'] = errores_en_fila
							fila_con_error['row_index'] = index
							filas_con_errores.append(fila_con_error)
						
						#-- Solo guardar si no hay errores.
						elif not errores_en_fila:
							try:
								producto.save()
								agregados += 1
								
							except Exception as e:
								#-- Guardar información de la fila con error.
								#-- Limpiar el mensaje de error si tiene corchetes.
								error_clean = str(e).replace("['", "").replace("']", "").replace("'", "")
								error_msg = f"Error al guardar cambios - {error_clean}"
								errores.append(error_msg)
								fila_con_error = fila.copy()
								fila_con_error['error_message'] = error_msg
								fila_con_error['row_index'] = index
								filas_con_errores.append(fila_con_error)
						
					except Exception as e:
						#-- Capturar cualquier error inesperado en la fila.
						#-- Limpiar el mensaje de error si tiene corchetes.
						error_clean = str(e).replace("['", "").replace("']", "").replace("'", "")
						error_msg = f"Error al procesar - {error_clean}"
						errores.append(error_msg)
						
						#-- Guardar información de la fila con error.
						fila_con_error = fila.copy()
						fila_con_error['error_message'] = error_msg
						fila_con_error['row_index'] = index
						filas_con_errores.append(fila_con_error)
						
						continue #-- Continuar con la siguiente fila.
				
				#-- Si hay errores, lanzar excepción para revertir la transacción.
				if errores:
					#-- Guardar información de errores en la sesión antes de lanzar la excepción.
					request.session['errores_procesamiento'] = {
						'errores': errores,
						'filas_con_errores': filas_con_errores,
						'columnas': columnas_excel,
						'total_registros': len(todos_los_datos),
						'campos_seleccionados': columnas_excel,
						'nombre_archivo': excel_data.get('nombre_archivo', '')
					}
					request.session.modified = True  #-- Asegurar que la sesión se guarde.
					raise ValidationError("Errores encontrados durante el procesamiento")
				
				#-- Preparar contexto para mostrar resultados (éxito).
				context = self.get_context_data()
				context['total_registros'] = len(todos_los_datos)
				context['actualizados'] = agregados
				context['errores'] = []
				
				#-- Limpiar sesión.
				keys_to_remove = ['excel_data']
				for key in keys_to_remove:
					if key in request.session:
						del request.session[key]
				
				return self.render_to_response(context)
		
		except ValidationError as e:
			#-- Redirigir a la vista de errores.
			return redirect('mostrar_errores_excel')
		
		except Exception as e:
			#-- Error inesperado
			messages.error(request, f'Error inesperado durante el procesamiento: {str(e)}')
			return redirect('excel_preview')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['proceso'] = self.request.session.get('excel_data', {}).get('proceso', 'actualizar')
		context['fecha'] = timezone.now()
		return context


#-- Funciones de validación según tipo de dato del campo.
def obtener_tipo_campo_desde_modelo(campo_obj):
	"""Obtener el tipo de campo basado en la instancia del campo del modelo"""
	if isinstance(campo_obj, (CharField, TextField)):
		return 'string'
	elif isinstance(campo_obj, (IntegerField, BigIntegerField, AutoField)):
		return 'integer'
	elif isinstance(campo_obj, (DecimalField, FloatField)):
		return 'decimal'
	elif isinstance(campo_obj, BooleanField):
		return 'boolean'
	elif isinstance(campo_obj, DateField):
		return 'date'
	elif isinstance(campo_obj, DateTimeField):
		return 'datetime'
	elif isinstance(campo_obj, ForeignKey):
		return 'foreign_key'
	else:
		return 'string'

def obtener_especificaciones_campo(campo_obj):
	"""Obtener especificaciones de validación del campo"""
	especificaciones = {}
	
	if hasattr(campo_obj, 'max_length') and campo_obj.max_length:
		especificaciones['max_length'] = campo_obj.max_length
	
	if hasattr(campo_obj, 'max_digits') and campo_obj.max_digits:
		especificaciones['max_digits'] = campo_obj.max_digits
	
	if hasattr(campo_obj, 'decimal_places') and campo_obj.decimal_places:
		especificaciones['decimal_places'] = campo_obj.decimal_places
	
	#-- Validaciones específicas basadas en el nombre del campo.
	if campo_obj.name == 'fecha_fabricacion':
		especificaciones.update({
			'pattern': r'^$|^20\d{2}(0[1-9]|1[0-2])$',
			'mensaje': 'Formato correcto AAAAMM (AAAA año, MM mes)'
		})
	elif campo_obj.name == 'unidad':
		especificaciones.update({
			'pattern': r'^[1-9]\d{0,2}$|^0$|^$',
			'mensaje': 'Número entero positivo de hasta 3 dígitos'
		})
	elif campo_obj.name in ['costo', 'descuento', 'precio']:
		especificaciones.update({
			'pattern': r'^(0|[1-9]\d{0,13})(\.\d{1,2})?$|^$',
			'mensaje': 'Número positivo con hasta 13 dígitos y 2 decimales'
		})
	
	return especificaciones

def validar_string(valor, campo_obj, especificaciones):
	"""Validar campo string preservando formato exacto"""
	#-- El valor ya viene preservado desde la carga del Excel.
	#-- Solo necesitamos validar, no convertir.
	
	#-- Validar campo obligatorio.
	if campo_obj.blank is False and campo_obj.null is False:
		if valor is None or valor == '':
			raise ValidationError("Este campo es obligatorio y no puede estar vacío")
	
	if valor is None:
		return None
	
	#-- Asegurar que es string (por si acaso).
	if not isinstance(valor, str):
		valor = str(valor)
	
	max_length = especificaciones.get('max_length')
	if max_length and len(valor) > max_length:
		raise ValidationError(f"Longitud máxima excedida ({max_length} caracteres)")
	
	#-- Validación específica por patrón si existe.
	pattern = especificaciones.get('pattern')
	if pattern and valor and not re.match(pattern, valor):
		raise ValidationError(especificaciones.get('mensaje', 'Formato inválido'))
	
	return valor

def validar_integer(valor, campo_obj, especificaciones):
	"""Validar campo integer"""
	try:
		int_val = int(valor)
		
		#-- Validación específica por patrón si existe.
		pattern = especificaciones.get('pattern')
		if pattern and not re.match(pattern, str(int_val)):
			raise ValidationError(especificaciones.get('mensaje', 'Formato inválido'))
		
		return int_val
	except (ValueError, TypeError):
		raise ValidationError("Valor entero inválido")

def validar_decimal(valor, campo_obj, especificaciones):
	"""Validar campo decimal"""
	try:
		#-- Si el valor está vacío, retornar 0.00
		if valor in ['', None, 'NULL', 'null', 'NaN', 'nan'] or pd.isna(valor):
			return Decimal('0.00')
		
		#-- Convertir a Decimal.
		if isinstance(valor, str):
			#-- Reemplazar coma por punto para formato argentino.
			valor = valor.replace(',', '.')
			#-- Eliminar caracteres no numéricos excepto punto y signo.
			valor = re.sub(r'[^\d\.\-]', '', valor)
		
		decimal_val = Decimal(str(valor))
		
		#-- Validar máximo de dígitos.
		max_digits = especificaciones.get('max_digits')
		decimal_places = especificaciones.get('decimal_places')
		
		if max_digits:
			#-- Verificar que no exceda los dígitos permitidos.
			digits = len(str(decimal_val).replace('.', '').replace('-', ''))
			if digits > max_digits:
				raise ValidationError(f"Máximo {max_digits} dígitos permitidos")
		
		if decimal_places:
			#-- Verificar decimales.
			if decimal_val.as_tuple().exponent and abs(decimal_val.as_tuple().exponent) > decimal_places:
				raise ValidationError(f"Máximo {decimal_places} decimales permitidos")
		
		#-- Validación específica por patrón si existe.
		pattern = especificaciones.get('pattern')
		if pattern and not re.match(pattern, str(decimal_val)):
			raise ValidationError(especificaciones.get('mensaje', 'Formato inválido'))
		
		return decimal_val
		
	except (ValueError, InvalidOperation):
		raise ValidationError("Valor decimal inválido")

def validar_boolean(valor, campo_obj, especificaciones):
	"""Validar campo boolean"""
	if isinstance(valor, bool):
		return valor
	
	elif isinstance(valor, str):
		valor_lower = valor.lower().strip()
		true_values = ['true', '1', 'yes', 'sí', 'si', 'verdadero', 'x', '✔', 'verdad', 't', 'v']
		false_values = ['false', '0', 'no', 'not', 'falso', '', 'null', 'none', 'f', 'n']
		
		if valor_lower in true_values:
			return True
		elif valor_lower in false_values:
			return False
		else:
			raise ValidationError("Valor booleano inválido")
	else:
		return bool(valor)

def validar_foreign_key(valor, campo_obj, especificaciones):
	"""Validar campo foreign key"""
	try:
		#-- Para foreign keys, validamos que sea un entero válido.
		if valor in ['', None, 'NULL', 'null']:
			return None
		
		int_val = int(valor)
		
		#-- Verificar que exista en la tabla relacionada.
		related_model = campo_obj.related_model
		
		if not related_model.objects.filter(pk=int_val).exists():
			raise ValidationError(f"ID {int_val} no existe en {related_model._meta.verbose_name}")
		
		return int_val
	except (ValueError, TypeError):
		raise ValidationError("ID inválido para relación")

def validar_date(valor, campo_obj, especificaciones):
	"""Validar campo date"""
	try:
		if isinstance(valor, datetime):
			return valor.date()
		elif isinstance(valor, str):
			#-- Intentar varios formatos de fecha.
			formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%Y%m%d']
			for fmt in formats:
				try:
					return datetime.strptime(valor, fmt).date()
				except ValueError:
					continue
			raise ValidationError("Formato de fecha inválido")
		else:
			raise ValidationError("Tipo de fecha inválido")
	except Exception:
		raise ValidationError("Fecha inválida")

def validar_datetime(valor, campo_obj, especificaciones):
	"""Validar campo datetime"""
	try:
		if isinstance(valor, datetime):
			return valor
		elif isinstance(valor, str):
			#-- Intentar varios formatos de fecha/hora.
			formats = ['%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y%m%d %H%M%S']
			for fmt in formats:
				try:
					return datetime.strptime(valor, fmt)
				except ValueError:
					continue
			raise ValidationError("Formato de fecha/hora inválido")
		else:
			raise ValidationError("Tipo de fecha/hora inválido")
	except Exception:
		raise ValidationError("Fecha/hora inválida")

def validar_generico(valor, campo_obj, especificaciones):
	"""Validación genérica para tipos no especificados"""
	try:
		#-- Intentar conversión básica a string.
		return str(valor)
	except Exception:
		raise ValidationError("Valor inválido para el campo")

# neumatic\utils\cleanup_foxpro\limpiar_caracteres_foxpro.py

#!/usr/bin/env python
"""
SCRIPT DE LIMPIEZA DE CARACTERES FOXPRO/DBF
============================================
Ubicación: neumatic/utils/cleanup_foxpro/
VERSIÓN MEJORADA: Usa una sola fuente de configuración
"""

import os
import sys
import django
import logging
import argparse
from datetime import datetime

#-- Obtener ruta actual del script.
script_dir = os.path.dirname(os.path.abspath(__file__))

#-- Subir 3 niveles para llegar a PROJECT_NEUMATIC/
#-- cleanup_foxpro/ → utils/ → neumatic/ → PROJECT_NEUMATIC/
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))

#-- DEBUG: Mostrar rutas
print(f"📍 Script: {script_dir}")
print(f"📍 Project root: {project_root}")
print(f"📍 ¿Existe neumatic/? {os.path.exists(os.path.join(project_root, 'neumatic'))}")

#-- AGREGAR AMBAS RUTAS AL PATH (esto es clave)
sys.path.insert(0, project_root)  # Para PROJECT_NEUMATIC
sys.path.insert(0, os.path.join(project_root, 'neumatic'))  # Para neumatic/

print(f"📍 Python path: {sys.path[:3]}")

#-- CONFIGURACIÓN CORRECTA PARA TU ESTRUCTURA:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')

#-- Configurar Django
import django

try:
	django.setup()
	print("✅ Django configurado correctamente")
	
	#-- Verificar que puede importar apps.
	from django.apps import apps
	print(f"✅ Apps cargadas: {len(apps.get_app_configs())}")
	
except Exception as e:
	print(f"❌ Error al configurar Django: {e}")
	print("\n🔍 Posible solución: Verifica el archivo settings.py")
	
	#-- Verificar contenido de settings.py.
	settings_path = os.path.join(project_root, 'neumatic', 'neumatic', 'settings.py')
	if os.path.exists(settings_path):
		with open(settings_path, 'r', encoding='utf-8') as f:
			content = f.read()
			if 'INSTALLED_APPS' in content:
				print("✅ INSTALLED_APPS encontrado en settings.py")
			else:
				print("❌ INSTALLED_APPS NO encontrado en settings.py")
	
	sys.exit(1)

#-- Importar después de django.setup()
from django.apps import apps
from django.db import transaction, models

#-- Importar configuración desde el mismo directorio.
from cleanup_config import (
	MODELOS_CAMPOS, 
	CARACTERES_REEMPLAZO, 
	CARACTERES_ELIMINAR,
	CARACTERES_DESCRIPCIONES,
	CARACTERES_REEMPLAZO_CON_DESCRIPCION,
)

# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================
def setup_logging(modo_check=True):
	"""Configura el sistema de logging según el modo"""
	log_filename = f"cleanup_foxpro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
	
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(levelname)s - %(message)s',
		handlers=[
			logging.FileHandler(log_filename, encoding='utf-8'),
			logging.StreamHandler(sys.stdout)
		]
	)
	
	logger = logging.getLogger(__name__)
	
	if modo_check:
		logger.info("=" * 70)
		logger.info("MODO ANÁLISIS - No se modificarán datos")
		logger.info("=" * 70)
	else:
		logger.info("=" * 70)
		logger.info("MODO LIMPIEZA - Se modificarán datos")
		logger.info("=" * 70)
	
	return logger, log_filename

# =============================================================================
# CLASE PRINCIPAL DE LIMPIEZA (MEJORADA - USANDO UNA SOLA FUENTE)
# =============================================================================
class LimpiadorCaracteresFoxPro:
	def __init__(self, modelos_campos=None):
		self.modelos_campos = modelos_campos or MODELOS_CAMPOS
		self.logger = logging.getLogger(__name__)
		
		#-- Estadísticas.
		self.estadisticas = {
			'modelos_procesados': 0,
			'registros_procesados': 0,
			'registros_modificados': 0,
			'campos_modificados': 0,
			'caracteres_reemplazados': 0,
			'caracteres_eliminados': 0,
			'errores': 0,
			'inicio': datetime.now(),
			'registros_problematicos': [],
		}
		
		#-- Parsear modelos.
		self.modelos_parseados = self._parsear_modelos()
	
	def _parsear_modelos(self):
		"""Convierte la configuración en tuplas (app_label, Modelo, campos)"""
		modelos = []
		
		for clave, campos in self.modelos_campos.items():
			try:
				if '.' not in clave:
					self.logger.error(f"Formato incorrecto: {clave}. Usa 'app.modelo'")
					continue
				
				app_label, model_name = clave.split('.', 1)
				Model = apps.get_model(app_label, model_name)
				modelos.append((app_label, Model, campos))
				
				self.logger.debug(f"Modelo configurado: {app_label}.{model_name}")
				
			except LookupError:
				self.logger.error(f"Modelo no encontrado: {clave}")
				self.estadisticas['errores'] += 1
			except Exception as e:
				self.logger.error(f"Error con {clave}: {e}")
				self.estadisticas['errores'] += 1
		
		return modelos
	
	def limpiar_texto(self, texto, registro_id=None, campo=None):
		"""Limpia un texto aplicando reemplazos y eliminaciones. Devuelve (texto_limpio, caracteres_eliminados_info)"""
		if not texto or not isinstance(texto, str):
			return texto, []
		
		original = texto
		texto_limpio = texto
		
		#-- Lista para almacenar información de caracteres eliminados.
		caracteres_eliminados_info = []
		
		#-- 1. Eliminar caracteres basura.
		for char in CARACTERES_ELIMINAR:
			if char in texto_limpio:
				count = texto_limpio.count(char)
				texto_limpio = texto_limpio.replace(char, '')
				self.estadisticas['caracteres_eliminados'] += count
				
				#-- Guardar información de caracteres eliminados para mostrarla después
				char_code = ord(char)
				caracteres_eliminados_info.append({
					'caracter': char,
					'codigo_hex': f'\\x{char_code:02x}',
					'codigo_unicode': f'U+{char_code:04X}',
					'contexto': self._obtener_contexto(original, char)
				})
		
		#-- 2. Reemplazar caracteres corruptos.
		for char_malo, char_bueno in CARACTERES_REEMPLAZO:
			if char_malo in texto_limpio:
				count = texto_limpio.count(char_malo)
				texto_limpio = texto_limpio.replace(char_malo, char_bueno)
				self.estadisticas['caracteres_reemplazados'] += count
		
		#-- 3. Limpiar espacios múltiples si hubo reemplazos.
		if texto_limpio != original:
			import re
			texto_limpio = re.sub(r'\s+', ' ', texto_limpio)
			texto_limpio = texto_limpio.strip()
		
		return texto_limpio, caracteres_eliminados_info
	
	def _obtener_contexto(self, texto, caracter, contexto_len=20):
		"""Obtiene contexto alrededor de un carácter"""
		idx = texto.find(caracter)
		if idx == -1:
			return ""
		
		inicio = max(0, idx - contexto_len)
		fin = min(len(texto), idx + contexto_len + 1)
		contexto = texto[inicio:fin]
		
		if inicio > 0:
			contexto = "..." + contexto
		if fin < len(texto):
			contexto = contexto + "..."
		
		return contexto
	
	def _detectar_cambio_especifico(self, original, corregido):
		"""Detecta qué caracteres específicos fueron cambiados usando la configuración centralizada"""
		cambios = []
		
		#-- Verificar patrones compuestos primero (como "N§", "C§").
		for char_malo, char_bueno in CARACTERES_REEMPLAZO:
			if len(char_malo) > 1:  # Patrones compuestos
				if char_malo in original and char_bueno in corregido and char_malo not in corregido:
					descripcion = CARACTERES_DESCRIPCIONES.get(char_malo, f'{char_malo} → {char_bueno}')
					cambios.append(descripcion)
		
		#-- Verificar caracteres individuales.
		for char_malo, char_bueno in CARACTERES_REEMPLAZO:
			if len(char_malo) == 1:  #-- Caracteres individuales.
				if char_malo in original and char_bueno in corregido and char_malo not in corregido:
					descripcion = CARACTERES_DESCRIPCIONES.get(char_malo, f'{char_malo} → {char_bueno}')
					if descripcion not in cambios:  #-- Evitar duplicados.
						cambios.append(descripcion)
		
		if cambios:
			#-- Limitar a 3 descripciones para no hacerlo muy largo.
			return ", ".join(cambios[:3])
		
		#-- Si no encontramos coincidencias específicas, buscar cambios generales.
		if original != corregido:
			#-- Contar cuántos caracteres no-ASCII fueron cambiados.
			chars_original = set(original)
			chars_corregido = set(corregido)
			caracteres_cambiados = chars_original - chars_corregido
			
			#-- Filtrar solo caracteres no-ASCII.
			caracteres_especiales = [c for c in caracteres_cambiados if ord(c) > 127]
			if caracteres_especiales:
				return f"{len(caracteres_especiales)} caracter(es) especial(es)"
		
		return "Varios caracteres"
	
	def analizar_modelo(self, app_label, Model, campos, modo_check=True):
		"""Analiza o limpia un modelo según el modo - VERSIÓN MEJORADA"""
		self.logger.info(f"{'[ANALIZANDO]' if modo_check else '[LIMPIANDO]'} " f"{app_label}.{Model.__name__}")
		
		try:
			#-- Verificar campos existentes.
			campos_validos = []
			for campo in campos:
				try:
					field = Model._meta.get_field(campo)
					if isinstance(field, (models.CharField, models.TextField)):
						campos_validos.append(campo)
					else:
						self.logger.warning(f"  Campo '{campo}' no es texto, omitiendo")
				except models.FieldDoesNotExist:
					self.logger.warning(f"  Campo '{campo}' no existe, omitiendo")
			
			if not campos_validos:
				self.logger.warning("  No hay campos válidos para procesar")
				return
			
			#-- Obtener registros.
			total_registros = Model.objects.count()
			
			if total_registros == 0:
				self.logger.info("  No hay registros")
				return
			
			self.logger.info(f"  Registros: {total_registros}")
			self.logger.info(f"  Campos: {', '.join(campos_validos)}")
			
			registros_modificados = 0
			campos_modificados = 0
			
			#-- Procesar en lotes.
			batch_size = 2000
			for i in range(0, total_registros, batch_size):
				batch = Model.objects.all()[i:i + batch_size]
				
				for registro in batch:
					cambios = {}
					cambios_por_campo = {}  #-- Para almacenar info de cada cambio.
					todos_caracteres_eliminados = []  #-- Para almacenar todos los caracteres eliminados en este registro.
					
					for campo in campos_validos:
						valor_actual = getattr(registro, campo)
						if valor_actual:
							valor_limpio, caracteres_eliminados = self.limpiar_texto(
								str(valor_actual), 
								registro.pk, 
								campo
							)
							
							#-- Guardar caracteres eliminados.
							if caracteres_eliminados:
								for info in caracteres_eliminados:
									todos_caracteres_eliminados.append({
										'campo': campo,
										'info': info
									})
							
							if valor_limpio != valor_actual:
								cambios[campo] = valor_limpio
								campos_modificados += 1
								
								#-- Guardar información detallada del cambio.
								cambios_por_campo[campo] = {
									'original': valor_actual,
									'corregido': valor_limpio,
									'tipo_cambio': self._detectar_cambio_especifico(valor_actual, valor_limpio)
								}
					
					if cambios:
						registros_modificados += 1
						registro_id = registro.pk
						
						#-- 📍 MOSTRAR DETALLES DEL REGISTRO CON PROBLEMAS.
						self.logger.info(f"  🔍 REGISTRO CON PROBLEMAS: -----------------------------------------")
						self.logger.info(f"    • Modelo: {Model.__name__}")
						self.logger.info(f"    • ID: {registro_id}")
						self.logger.info(f"    • Campos a modificar: {len(cambios)}")
						
						# Mostrar detalles de cada campo problemático
						for campo, info in cambios_por_campo.items():
							self.logger.info(f"    📋 Campo: {campo}")
							self.logger.info(f"      Cambio: {info['tipo_cambio']}")
							self.logger.info(f"      Original: {info['original'][:70]}")
							self.logger.info(f"      Corregido: {info['corregido'][:70]}")
						
						#-- Mostrar caracteres eliminados si los hay.
						if todos_caracteres_eliminados:
							self.logger.info(f"    ⚠️  CARACTERES A ELIMINAR ENCONTRADOS:")
							for elim_info in todos_caracteres_eliminados:
								info = elim_info['info']
								self.logger.info(f"      Campo: {elim_info['campo']}")
								self.logger.info(f"      Carácter: '{info['codigo_hex']}' ({info['codigo_unicode']})")
								self.logger.info(f"      Contexto: {info['contexto']}")
						
						#-- Guardar en estadísticas para resumen.
						self.estadisticas['registros_problematicos'].append({
							'modelo': Model.__name__,
							'id': registro_id,
							'campos': list(cambios.keys()),
							'total_campos': len(cambios),
							'caracteres_eliminados': len(todos_caracteres_eliminados)
						})
						
						#-- Si no es modo check, guardar cambios.
						if not modo_check:
							Model.objects.filter(pk=registro.pk).update(**cambios)
				
				#-- Mostrar progreso.
				progreso = min(i + batch_size, total_registros)
				if progreso % 5000 == 0:
					self.logger.info(f"    Procesados: {progreso}/{total_registros}")
					if modo_check:
						self.logger.info(f"    Registros problemáticos encontrados: {registros_modificados}")
			
			#-- Actualizar estadísticas.
			self.estadisticas['modelos_procesados'] += 1
			self.estadisticas['registros_procesados'] += total_registros
			self.estadisticas['registros_modificados'] += registros_modificados
			self.estadisticas['campos_modificados'] += campos_modificados
			
			#-- Resumen del modelo.
			if registros_modificados > 0:
				porcentaje = (registros_modificados / total_registros) * 100
				self.logger.info(f"  📊 RESUMEN {Model.__name__}:")
				self.logger.info(f"    ✓ {registros_modificados}/{total_registros} registros con problemas ({porcentaje:.1f}%)")
				self.logger.info(f"    ✓ {campos_modificados} campos a modificar")
			else:
				self.logger.info("  ✓ No se encontraron problemas")
			
		except Exception as e:
			self.logger.error(f"  ✗ Error: {e}")
			self.estadisticas['errores'] += 1
	
	def ejecutar_analisis(self):
		"""Ejecuta solo análisis (sin modificar) - VERSIÓN MEJORADA"""
		self.logger.info("=" * 70)
		self.logger.info("INICIANDO ANÁLISIS DE CARACTERES FOXPRO")
		self.logger.info("=" * 70)
		
		self.logger.info(f"Modelos a analizar: {len(self.modelos_parseados)}")
		
		for app_label, Model, campos in self.modelos_parseados:
			self.analizar_modelo(app_label, Model, campos, modo_check=True)
		
		self.mostrar_estadisticas(modo_check=True)
		
		#-- Mostrar resumen de registros problemáticos.
		self.mostrar_resumen_registros_problematicos()
		
		#-- Recomendación basada en análisis.
		if self.estadisticas['registros_modificados'] > 0:
			self.logger.info("=" * 70)
			self.logger.info("RECOMENDACIÓN:")
			self.logger.info(f"Se encontraron {self.estadisticas['registros_modificados']} registros con problemas.")
			self.logger.info(f"Para corregirlos ejecuta: python {sys.argv[0]} --fix")
			self.logger.info("=" * 70)
		else:
			self.logger.info("✓ No se encontraron caracteres problemáticos")
	
	def mostrar_resumen_registros_problematicos(self):
		"""Muestra un resumen de todos los registros con problemas"""
		if not self.estadisticas['registros_problematicos']:
			return
		
		self.logger.info("=" * 70)
		self.logger.info("📋 RESUMEN DE REGISTROS CON PROBLEMAS")
		self.logger.info("=" * 70)
		
		#-- Agrupar por modelo.
		modelos = {}
		for registro in self.estadisticas['registros_problematicos']:
			modelo = registro['modelo']
			if modelo not in modelos:
				modelos[modelo] = []
			modelos[modelo].append(registro)
		
		for modelo, registros in modelos.items():
			self.logger.info(f"📁 Modelo: {modelo}")
			self.logger.info(f"  Registros: {len(registros)}")
			
			#-- Contar campos problemáticos.
			campos_count = {}
			for r in registros:
				for campo in r['campos']:
					campos_count[campo] = campos_count.get(campo, 0) + 1
			
			if campos_count:
				self.logger.info(f"  Campos afectados:")
				for campo, count in sorted(campos_count.items(), key=lambda x: x[1], reverse=True):
					self.logger.info(f"    • {campo}: {count} registros")
			
			#-- Mostrar caracteres eliminados totales.
			total_eliminados = sum(r.get('caracteres_eliminados', 0) for r in registros)
			if total_eliminados > 0:
				self.logger.info(f"  Caracteres a eliminar: {total_eliminados}")
	
	@transaction.atomic
	def ejecutar_limpieza(self):
		"""Ejecuta limpieza real (modifica datos)"""
		self.logger.info("=" * 70)
		self.logger.info("INICIANDO LIMPIEZA DE CARACTERES FOXPRO")
		self.logger.info("ADVERTENCIA: Se modificarán datos en la base de datos")
		self.logger.info("=" * 70)
		
		self.logger.info(f"Modelos a limpiar: {len(self.modelos_parseados)}")
		
		for app_label, Model, campos in self.modelos_parseados:
			self.analizar_modelo(app_label, Model, campos, modo_check=False)
		
		self.mostrar_estadisticas(modo_check=False)
		
		#-- Mostrar resumen de lo que se modificó.
		if self.estadisticas['registros_modificados'] > 0:
			self.logger.info("=" * 70)
			self.logger.info("✅ RESUMEN DE MODIFICACIONES")
			self.logger.info("=" * 70)
			self.logger.info(f"• Registros modificados: {self.estadisticas['registros_modificados']}")
			self.logger.info(f"• Campos modificados: {self.estadisticas['campos_modificados']}")
			self.logger.info(f"• Caracteres reemplazados: {self.estadisticas['caracteres_reemplazados']}")
			self.logger.info(f"• Caracteres eliminados: {self.estadisticas['caracteres_eliminados']}")
			self.logger.info("=" * 70)
		
		self.logger.info("=" * 70)
		self.logger.info("LIMPIEZA COMPLETADA")
		self.logger.info("=" * 70)
	
	def mostrar_estadisticas(self, modo_check=True):
		"""Muestra estadísticas detalladas"""
		duracion = datetime.now() - self.estadisticas['inicio']
		
		self.logger.info("=" * 70)
		self.logger.info("ESTADÍSTICAS FINALES")
		self.logger.info("=" * 70)
		self.logger.info(f"Duración: {duracion}")
		self.logger.info(f"Modelos procesados: {self.estadisticas['modelos_procesados']}")
		self.logger.info(f"Registros procesados: {self.estadisticas['registros_procesados']}")
		
		if modo_check:
			self.logger.info(f"Registros CON PROBLEMAS: {self.estadisticas['registros_modificados']}")
		else:
			self.logger.info(f"Registros MODIFICADOS: {self.estadisticas['registros_modificados']}")
		
		if self.estadisticas['registros_procesados'] > 0:
			porcentaje = (self.estadisticas['registros_modificados'] / 
						self.estadisticas['registros_procesados']) * 100
			self.logger.info(f"Porcentaje: {porcentaje:.2f}%")
		
		self.logger.info(f"Campos a modificar: {self.estadisticas['campos_modificados']}")
		self.logger.info(f"Caracteres reemplazados: {self.estadisticas['caracteres_reemplazados']}")
		self.logger.info(f"Caracteres eliminados: {self.estadisticas['caracteres_eliminados']}")
		self.logger.info(f"Errores: {self.estadisticas['errores']}")

# =============================================================================
# FUNCIONES AUXILIARES (ACTUALIZADAS)
# =============================================================================
def buscar_caracteres_problematicos():
	"""Busca caracteres específicos en la base de datos usando la configuración centralizada"""
	logger = logging.getLogger(__name__)
	
	logger.info("=" * 70)
	logger.info("BÚSQUEDA DE CARACTERES PROBLEMÁTICOS")
	logger.info("=" * 70)
	
	#-- Usar la configuración centralizada - solo caracteres individuales (largo 1).
	caracteres_buscar = []
	for malo, bueno, desc in CARACTERES_REEMPLAZO_CON_DESCRIPCION:
		if len(malo) == 1:  # Solo caracteres individuales
			caracteres_buscar.append((malo, bueno, desc))
	
	#-- Limitar a los primeros 15 para no hacerlo muy largo.
	caracteres_buscar = caracteres_buscar[:15]
	
	if not caracteres_buscar:
		logger.warning("No se encontraron caracteres individuales para buscar")
		return
	
	for clave_modelo, campos in MODELOS_CAMPOS.items():
		try:
			app_label, model_name = clave_modelo.split('.', 1)
			Model = apps.get_model(app_label, model_name)
			
			logger.info(f"\nModelo: {app_label}.{model_name}")
			
			for campo in campos:
				try:
					Model._meta.get_field(campo)
					
					encontrados_en_campo = []
					for char_malo, char_bueno, descripcion in caracteres_buscar:
						try:
							filtro = {f"{campo}__contains": char_malo}
							count = Model.objects.filter(**filtro).count()
							
							if count > 0:
								encontrados_en_campo.append((descripcion, count))
						except:
							continue
					
					if encontrados_en_campo:
						logger.info(f"  Campo '{campo}':")
						for descripcion, count in encontrados_en_campo:
							logger.info(f"    • {descripcion}: {count} registros")
					
				except models.FieldDoesNotExist:
					continue
					
		except Exception as e:
			logger.warning(f"  Error con modelo {clave_modelo}: {e}")
			continue
	
	logger.info("=" * 70)
	logger.info("BÚSQUEDA COMPLETADA")
	logger.info("=" * 70)

def verificar_configuracion():
	"""Verifica que la configuración sea correcta"""
	logger = logging.getLogger(__name__)
	
	logger.info("=" * 70)
	logger.info("VERIFICACIÓN DE CONFIGURACIÓN")
	logger.info("=" * 70)
	
	# Verificar modelos
	logger.info("MODELOS CONFIGURADOS:")
	
	for clave, campos in MODELOS_CAMPOS.items():
		logger.info(f"  {clave}:")
		
		if '.' not in clave:
			logger.error("    ERROR: Formato incorrecto. Usa 'app.modelo'")
			continue
		
		app_label, model_name = clave.split('.', 1)
		
		try:
			Model = apps.get_model(app_label, model_name)
			logger.info(f"    ✓ Modelo encontrado")
			logger.info(f"    Campos: {len(campos)}")
			
			#-- Verificar campos.
			campos_validos = 0
			for campo in campos:
				try:
					field = Model._meta.get_field(campo)
					if isinstance(field, (models.CharField, models.TextField)):
						campos_validos += 1
						logger.info(f"      ✓ {campo} ({field.get_internal_type()})")
					else:
						logger.warning(f"      ✗ {campo} (no es CharField/TextField)")
				except models.FieldDoesNotExist:
					logger.error(f"      ✗ {campo} (no existe)")
			
			logger.info(f"    Campos válidos: {campos_validos}/{len(campos)}")
			
		except LookupError:
			logger.error(f"    ✗ Modelo no encontrado")
		except Exception as e:
			logger.error(f"    ✗ Error: {e}")
	
	#-- Verificar caracteres a reemplazar.
	logger.info("CARACTERES A REEMPLAZAR (con descripción):")
	
	#-- Primero mostrar caracteres individuales.
	caracteres_individuales = [c for c in CARACTERES_REEMPLAZO_CON_DESCRIPCION if len(c[0]) == 1]
	patrones_compuestos = [c for c in CARACTERES_REEMPLAZO_CON_DESCRIPCION if len(c[0]) > 1]
	
	logger.info(f"  Caracteres individuales ({len(caracteres_individuales)}):")
	for char_malo, char_bueno, descripcion in caracteres_individuales[:20]:  # Mostrar primeros 20
		try:
			#-- Mostrar en formato legible.
			if char_malo == ' ' or ord(char_malo) < 32:
				hex_code = f'\\x{ord(char_malo):02x}'
				logger.info(f"    {hex_code} → '{char_bueno}' - {descripcion}")
			else:
				logger.info(f"    '{char_malo}' → '{char_bueno}' - {descripcion}")
		except:
			logger.info(f"    ??? → '{char_bueno}' - {descripcion}")
	
	if len(caracteres_individuales) > 20:
		logger.info(f"    ... y {len(caracteres_individuales) - 20} más")
	
	if patrones_compuestos:
		logger.info(f"  Patrones compuestos ({len(patrones_compuestos)}):")
		for patron, reemplazo, descripcion in patrones_compuestos:
			logger.info(f"    '{patron}' → '{reemplazo}' - {descripcion}")
	
	logger.info(f"RESUMEN:")
	logger.info(f"  • Total caracteres a reemplazar: {len(CARACTERES_REEMPLAZO)}")
	logger.info(f"  • Caracteres individuales: {len(caracteres_individuales)}")
	logger.info(f"  • Patrones compuestos: {len(patrones_compuestos)}")
	logger.info(f"  • Caracteres a eliminar: {len(CARACTERES_ELIMINAR)}")
	
	logger.info("=" * 70)
	logger.info("VERIFICACIÓN COMPLETADA")
	logger.info("=" * 70)

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def main():
	"""Función principal del script"""
	parser = argparse.ArgumentParser(
		description='Limpia caracteres corruptos de FoxPro en base de datos Django',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Ejemplos:
%(prog)s                    # Solo analizar (modo check)
%(prog)s --fix              # Ejecutar limpieza real
%(prog)s --model productos.Producto  # Solo un modelo
%(prog)s --search           # Buscar caracteres específicos
%(prog)s --verify           # Verificar configuración
		"""
	)
	
	parser.add_argument('--fix', action='store_true',
					help='Ejecutar limpieza real (modifica datos)')
	parser.add_argument('--model', type=str,
					help='Procesar solo un modelo (formato: app.modelo)')
	parser.add_argument('--search', action='store_true',
					help='Buscar caracteres problemáticos específicos')
	parser.add_argument('--verify', action='store_true',
					help='Verificar configuración')
	parser.add_argument('--log', type=str, default=None,
					help='Archivo de log personalizado')
	
	args = parser.parse_args()
	
	#-- Configurar logging.
	logger, log_file = setup_logging(modo_check=not args.fix)
	logger.info(f"Log file: {log_file}")
	
	#-- Modos especiales.
	if args.verify:
		verificar_configuracion()
		return
	
	if args.search:
		buscar_caracteres_problematicos()
		return
	
	#-- Preparar configuración.
	if args.model:
		#-- Usar solo el modelo especificado.
		if args.model not in MODELOS_CAMPOS:
			logger.error(f"Modelo {args.model} no encontrado en configuración")
			logger.info("Modelos disponibles:")
			for modelo in MODELOS_CAMPOS.keys():
				logger.info(f"  - {modelo}")
			return
		
		modelos_campos = {args.model: MODELOS_CAMPOS[args.model]}
		logger.info(f"Procesando solo: {args.model}")
	else:
		#-- Usar todos los modelos configurados.
		modelos_campos = None
	
	#-- Crear limpiador.
	limpiador = LimpiadorCaracteresFoxPro(modelos_campos)
	
	#-- Verificar que hay modelos.
	if not limpiador.modelos_parseados:
		logger.error("No se encontraron modelos válidos para procesar")
		logger.info("Verifica la configuración en cleanup_config.py")
		return
	
	#-- Solicitar confirmación para modo fix.
	if args.fix:
		logger.warning("!" * 70)
		logger.warning("ADVERTENCIA: Se modificarán datos en la base de datos")
		logger.warning("!" * 70)
		
		respuesta = input("\n¿Continuar con la limpieza? (sí/no): ")
		if respuesta.lower() not in ['si', 'sí', 's', 'yes', 'y']:
			logger.info("Limpieza cancelada")
			return
	
	#-- Ejecutar.
	if args.fix:
		limpiador.ejecutar_limpieza()
	else:
		limpiador.ejecutar_analisis()
	
	#-- Información final.
	logger.info(f"Log completo guardado en: {log_file}")
	
	if args.fix:
		logger.info("¡Limpieza completada!")
		logger.info("Revisa el archivo de log para detalles.")
	else:
		logger.info("¡Análisis completado!")
		logger.info("Revisa el archivo de log para ver qué cambios se aplicarían.")

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print("\n\nOperación cancelada por el usuario")
		sys.exit(1)
	except Exception as e:
		logging.error(f"Error inesperado: {e}", exc_info=True)
		print(f"\nError: {e}")
		print("Revisa el archivo de log para detalles.")
		sys.exit(1)
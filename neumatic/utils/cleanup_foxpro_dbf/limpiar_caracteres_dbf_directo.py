#!/usr/bin/env python
"""
SCRIPT DE LIMPIEZA DE CARACTERES DIRECTO SOBRE ARCHIVOS DBF
============================================================
Operación directa sobre archivos .dbf de Visual FoxPro.
"""

import os
import sys
import re
import logging
import argparse
from datetime import datetime
import dbf

from cleanup_config import (
	RUTA_TABLAS_DBF,
	TABLAS_CAMPOS, 
	CARACTERES_REEMPLAZO, 
	CARACTERES_ELIMINAR,
	CARACTERES_DESCRIPCIONES,
)

def setup_logging(modo_check=True):
	log_filename = f"cleanup_dbf_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
	
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(levelname)s - %(message)s',
		handlers=[
			logging.FileHandler(log_filename, encoding='utf-8'),
			logging.StreamHandler(sys.stdout)
		]
	)
	
	logger = logging.getLogger(__name__)
	logger.info("=" * 70)
	logger.info(f"MODO {'ANÁLISIS' if modo_check else 'LIMPIEZA'} EN ARCHIVOS DBF")
	logger.info("=" * 70)
	
	return logger, log_filename


class LimpiadorDBFDirecto:
	def __init__(self, tablas_campos=None):
		self.tablas_campos = tablas_campos or TABLAS_CAMPOS
		self.logger = logging.getLogger(__name__)
		self.estadisticas = {
			'tablas_procesadas': 0,
			'registros_procesados': 0,
			'registros_modificados': 0,
			'campos_modificados': 0,
			'caracteres_reemplazados': 0,
			'caracteres_eliminados': 0,
			'errores': 0,
			'inicio': datetime.now(),
			'registros_problematicos': [],
		}

	def limpiar_texto(self, texto):
		if not texto or not isinstance(texto, str):
			return texto, []
		
		original = texto
		texto_limpio = texto
		caracteres_eliminados_info = []
		
		for char in CARACTERES_ELIMINAR:
			if char in texto_limpio:
				count = texto_limpio.count(char)
				texto_limpio = texto_limpio.replace(char, '')
				self.estadisticas['caracteres_eliminados'] += count
				char_code = ord(char)
				caracteres_eliminados_info.append({
					'caracter': char,
					'codigo_hex': f'\\x{char_code:02x}',
					'codigo_unicode': f'U+{char_code:04X}',
					'contexto': self._obtener_contexto(original, char)
				})
		
		for char_malo, char_bueno in CARACTERES_REEMPLAZO:
			if char_malo in texto_limpio:
				count = texto_limpio.count(char_malo)
				texto_limpio = texto_limpio.replace(char_malo, char_bueno)
				self.estadisticas['caracteres_reemplazados'] += count
		
		if texto_limpio != original:
			texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
		
		return texto_limpio, caracteres_eliminados_info

	def _obtener_contexto(self, texto, caracter, contexto_len=20):
		idx = texto.find(caracter)
		if idx == -1:
			return ""
		inicio = max(0, idx - contexto_len)
		fin = min(len(texto), idx + contexto_len + 1)
		contexto = texto[inicio:fin]
		if inicio > 0: contexto = "..." + contexto
		if fin < len(texto): contexto = contexto + "..."
		return contexto

	def _detectar_cambio_especifico(self, original, corregido):
		cambios = []
		for char_malo, char_bueno in CARACTERES_REEMPLAZO:
			if char_malo in original and char_malo not in corregido:
				desc = CARACTERES_DESCRIPCIONES.get(char_malo, f'{char_malo} → {char_bueno}')
				if desc not in cambios:
					cambios.append(desc)
		return ", ".join(cambios[:3]) if cambios else "Varios caracteres"

	def analizar_tabla_dbf(self, nombre_tabla, campos, modo_check=True):
		ruta_dbf = os.path.join(RUTA_TABLAS_DBF, nombre_tabla)
		self.logger.info(f"{'[ANALIZANDO]' if modo_check else '[LIMPIANDO]'} DBF: {nombre_tabla}")
		
		if not os.path.exists(ruta_dbf):
			self.logger.error(f"  Archivo no encontrado: {ruta_dbf}")
			self.estadisticas['errores'] += 1
			return

		try:
			# Abrir tabla DBF usando librería dbf
			tabla = dbf.Table(ruta_dbf)
			
			if modo_check:
				tabla.open(mode=dbf.READ_ONLY)
			else:
				tabla.open(mode=dbf.READ_WRITE)

			# Validar existencia de campos en la tabla DBF
			campos_dbf = [f.upper() for f in tabla.field_names]
			campos_validos = [c for c in campos if c.upper() in campos_dbf]

			if not campos_validos:
				self.logger.warning("  Ninguno de los campos especificados existe en la tabla DBF")
				tabla.close()
				return

			total_registros = len(tabla)
			registros_modificados = 0
			campos_modificados = 0

			for idx, registro in enumerate(tabla):
				if dbf.is_deleted(registro):
					continue  # Ignorar registros borrados en FoxPro

				cambios = {}
				cambios_por_campo = {}
				todos_caracteres_eliminados = []

				for campo in campos_validos:
					# Obtener el valor formateado sin espacios adicionales
					valor_actual = str(registro[campo]).strip() if registro[campo] else ""

					if valor_actual:
						valor_limpio, caracteres_eliminados = self.limpiar_texto(valor_actual)
						
						if caracteres_eliminados:
							for info in caracteres_eliminados:
								todos_caracteres_eliminados.append({'campo': campo, 'info': info})

						if valor_limpio != valor_actual:
							cambios[campo] = valor_limpio
							campos_modificados += 1
							cambios_por_campo[campo] = {
								'original': valor_actual,
								'corregido': valor_limpio,
								'tipo_cambio': self._detectar_cambio_especifico(valor_actual, valor_limpio)
							}

				if cambios:
					registros_modificados += 1
					rec_num = idx + 1
					
					self.logger.info(f"  🔍 REGISTRO #{rec_num} CON PROBLEMAS:")
					for c, info in cambios_por_campo.items():
						self.logger.info(f"    📋 Campo: {c} | {info['tipo_cambio']}")
						self.logger.info(f"      Original:  {info['original'][:60]}")
						self.logger.info(f"      Corregido: {info['corregido'][:60]}")

					if not modo_check:
						# Escribir cambios en el registro del archivo DBF
						with registro:
							for c, val in cambios.items():
								registro[c] = val

			tabla.close()

			self.estadisticas['tablas_procesadas'] += 1
			self.estadisticas['registros_procesados'] += total_registros
			self.estadisticas['registros_modificados'] += registros_modificados
			self.estadisticas['campos_modificados'] += campos_modificados

		except Exception as e:
			self.logger.error(f"  ✗ Error en {nombre_tabla}: {e}")
			self.estadisticas['errores'] += 1

	def ejecutar(self, modo_check=True):
		for tabla, campos in self.tablas_campos.items():
			self.analizar_tabla_dbf(tabla, campos, modo_check=modo_check)
		self.mostrar_estadisticas(modo_check=modo_check)

	def mostrar_estadisticas(self, modo_check=True):
		duracion = datetime.now() - self.estadisticas['inicio']
		self.logger.info("=" * 70)
		self.logger.info("ESTADÍSTICAS FINALES DBF")
		self.logger.info("=" * 70)
		self.logger.info(f"Tiempo: {duracion}")
		self.logger.info(f"Tablas procesadas: {self.estadisticas['tablas_procesadas']}")
		self.logger.info(f"Registros analizados: {self.estadisticas['registros_procesados']}")
		self.logger.info(f"Registros {'con problemas' if modo_check else 'modificados'}: {self.estadisticas['registros_modificados']}")
		self.logger.info(f"Campos procesados: {self.estadisticas['campos_modificados']}")
		self.logger.info(f"Errores: {self.estadisticas['errores']}")


def verificar_configuracion():
	logger = logging.getLogger(__name__)
	logger.info("VERIFICANDO CONFIGURACIÓN DBF...")
	for tabla, campos in TABLAS_CAMPOS.items():
		ruta = os.path.join(RUTA_TABLAS_DBF, tabla)
		existe = "✓ Encontrado" if os.path.exists(ruta) else "✗ NO existe"
		logger.info(f"  • Tabla: {tabla} -> {existe}")
		logger.info(f"    Campos: {', '.join(campos)}")


def main():
	parser = argparse.ArgumentParser(description='Limpia caracteres corruptos en tablas DBF')
	parser.add_argument('--fix', action='store_true', help='Aplica la limpieza sobre los archivos DBF')
	parser.add_argument('--tabla', type=str, help='Filtrar una sola tabla (ej: CLIENTES.DBF)')
	parser.add_argument('--verify', action='store_true', help='Verifica que existan los archivos DBF')

	args = parser.parse_args()
	logger, log_file = setup_logging(modo_check=not args.fix)

	if args.verify:
		verificar_configuracion()
		return

	tablas_config = TABLAS_CAMPOS
	if args.tabla:
		if args.tabla not in TABLAS_CAMPOS:
			logger.error(f"La tabla {args.tabla} no está en cleanup_config.py")
			return
		tablas_config = {args.tabla: TABLAS_CAMPOS[args.tabla]}

	limpiador = LimpiadorDBFDirecto(tablas_config)

	if args.fix:
		logger.warning("ADVERTENCIA: Se modificarán los archivos .DBF directamente.")
		if input("¿Deseas continuar? (s/n): ").lower() not in ['s', 'si', 'yes']:
			logger.info("Operación cancelada")
			return
		limpiador.ejecutar(modo_check=False)
	else:
		limpiador.ejecutar(modo_check=True)


if __name__ == '__main__':
	main()
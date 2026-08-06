"""
CONFIGURACIÓN PARA LIMPIEZA DE CARACTERES DIRECTO EN DBF
=========================================================
"""
import os

#-- Directorio donde se encuentran los archivos .dbf (dejar "" si están en la misma carpeta).
RUTA_TABLAS_DBF = r"G:\DISCO_P\Leoncio\ProyectosDjango\PROJECT_NEUMATIC_PGS\neumatic\data_load\datavfox"

#-- TABLAS Y CAMPOS A LIMPIAR
#-- Formato: 'NOMBRE_TABLA.DBF': ['CAMPO1', 'CAMPO2', ...]
TABLAS_CAMPOS = {
	'CLIENTES.DBF': ['NOMBRE', 'APEYNOM', 'DOMICILIO'],
	'PROVEEDOR.DBF': ['NOMBRE', 'DOMICILIO'],
	'VENDEDOR.DBF': ['NOMBRE', 'DOMICILIO'],
	'LISTA.DBF': ['NOMBRE', 'MEDIDA', 'DETALLE'],
	# 'ARTICULO.DBF': ['NOMBRE'],
	# 'MARCAS.DBF': ['NOMBRE'],
	# 'MODELOS.DBF': ['NOMBRE'],
	'FACTURAS.DBF': ['OBSERVA'],
}

#-- CARACTERES A REEMPLAZAR (caracter_malo → caracter_bueno).
CARACTERES_REEMPLAZO_CON_DESCRIPCION = [
	('\xb5', 'Á', 'µ → Á (acento agudo mayúscula)'),
	('\x90', 'É', '\\x90 → É (acento agudo mayúscula)'),
	('\xd2', 'Í', '\\xD2 → Í (acento agudo mayúscula)'),
	('\xe0', 'Ó', '\\xE0 → Ó (acento agudo mayúscula)'),
	('\xe9', 'Ú', '\\xE9 → Ú (acento agudo mayúscula)'),
	('\xa0', 'á', '\\xA0 → á (acento agudo minúscula)'),
	('\x82', 'é', '\\x82 → é (acento agudo minúscula)'),
	('\xa1', 'í', '\\xA1 → í (acento agudo minúscula)'),
	('\xa2', 'ó', '\\xA2 → ó (acento agudo minúscula)'),
	('\xa3', 'ú', '\\xA3 → ú (acento agudo minúscula)'),
	('\xa4', 'ñ', '\\xA4 → ñ (eñe minúscula)'),
	('\xa5', 'Ñ', '\\xA5 → Ñ (eñe mayúscula)'),
	('\x9a', 'Ü', '\\x9A → Ü (U con diéresis mayúscula)'),
	('\x81', 'ü', '\\x81 → ü (u con diéresis minúscula)'),
	('\x99', 'Ö', '\\x99 → Ö (O con diéresis mayúscula)'),
	('\x94', 'Ï', '\\x94 → Ï (I con diéresis mayúscula)'),
	('\x84', 'ä', '\\x84 → ä (a con diéresis minúscula)'),
	('\x8b', 'ï', '\\x8B → ï (i con diéresis minúscula)'),
	('\x87', 'à', '\\x87 → à (a con acento grave)'),
	('\x8a', 'è', '\\x8A → è (e con acento grave)'),
	('\x8d', 'ì', '\\x8D → ì (i con acento grave)'),
	('\x8e', 'ò', '\\x8E → ò (o con acento grave)'),
	('\x92', 'ù', '\\x92 → ù (u con acento grave)'),
	('\xff', ' ', '\\xFF → ESPACIO'),
	('\x00', ' ', 'NULL → espacio'),
	('\xa9', '©', '\\xA9 → © (Copyright)'),
	('\xae', '®', '\\xAE → ® (Registered)'),
	('\x9d', 'Ø', '\\x9D → Ø'),
	('\x9c', 'ø', '\\x9C → ø'),
	('\xa7', 'º', '\\xA7 → º'),
	('N§', 'Nº', 'N§ → Nº'),
	('N°', 'Nº', 'N° → Nº'),
	('C§', 'Cº', 'C§ → Cº'),
	('C°', 'Cº', 'C° → Cº'),
]

CARACTERES_REEMPLAZO = [(malo, bueno) for malo, bueno, _ in CARACTERES_REEMPLAZO_CON_DESCRIPCION]
CARACTERES_DESCRIPCIONES = {malo: desc for malo, _, desc in CARACTERES_REEMPLAZO_CON_DESCRIPCION}

CARACTERES_ELIMINAR = [
	'\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07',
	'\x08', '\x0b', '\x0c', '\x0e', '\x0f', '\x10', '\x11',
	'\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18',
	'\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x7f', '\xad',
]
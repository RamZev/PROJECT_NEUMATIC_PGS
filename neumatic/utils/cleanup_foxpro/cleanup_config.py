# neumatic\utils\cleanup_foxpro\cleanup_config.py

"""
CONFIGURACIÓN PARA LIMPIEZA DE CARACTERES FOXPRO/DBF
=====================================================
Configura qué modelos y campos limpiar, y qué caracteres reemplazar o eliminar.
"""

#-- MODELOS Y CAMPOS A LIMPIAR.
#--   Agregar los modelos a limpiar y sus campos correspondientes.
#--   Formato: 'nombre_app.Modelo': ['campo1', 'campo2', ...]
MODELOS_CAMPOS = {
	
	#-- App: maestros.
	'maestros.Cliente': ['nombre_cliente', 'domicilio_cliente'],
	'maestros.Proveedor': ['nombre_proveedor', 'domicilio_proveedor'],
	'maestros.Vendedor': ['nombre_vendedor', 'domicilio_vendedor'],
	'maestros.Producto': ['nombre_producto', 'medida', 'descripcion_producto'],
	'maestros.Provincia': ['nombre_provincia'],
	'maestros.Localidad': ['nombre_localidad'],
	'maestros.Operario': ['nombre_operario'],
	'maestros.ProductoFamilia': ['nombre_producto_familia'],
	'maestros.ProductoMarca': ['nombre_producto_marca'],
	'maestros.ProductoModelo': ['nombre_modelo'],
	
	#-- App: ventas.
	'ventas.Factura': ['observa_comprobante'],
	'ventas.DetalleFactura': ['producto_venta'],
	
}

#-- CARACTERES A REEMPLAZAR (caracter_malo → caracter_bueno).
CARACTERES_REEMPLAZO_CON_DESCRIPCION  = [
	#-- Acentos y letras especiales (CP850 -> UTF-8).
	
	# ============================================
	# ACENTOS AGUDOS (MAYÚSCULAS)
	# ============================================
	('\xb5', 'Á', 'µ → Á (acento agudo mayúscula)'),
	('\x90', 'É', '\\x90 → É (acento agudo mayúscula)'),
	('\xd2', 'Í', '\\xD2 → Í (acento agudo mayúscula)'),
	('\xe0', 'Ó', '\\xE0 → Ó (acento agudo mayúscula)'),
	('\xe9', 'Ú', '\\xE9 → Ú (acento agudo mayúscula)'),
	
	# ============================================
	# ACENTOS AGUDOS (MINÚSCULAS)
	# ============================================
	('\xa0', 'á', '\\xA0 → á (acento agudo minúscula)'),
	('\x82', 'é', '\\x82 → é (acento agudo minúscula)'),
	('\xa1', 'í', '\\xA1 → í (acento agudo minúscula)'),
	('\xa2', 'ó', '\\xA2 → ó (acento agudo minúscula)'),
	('\xa3', 'ú', '\\xA3 → ú (acento agudo minúscula)'),
	
	# ============================================
	# Ñ / ñ
	# ============================================
	('\xa4', 'ñ', '\\xA4 → ñ (eñe minúscula)'),
	('\xa5', 'Ñ', '\\xA5 → Ñ (eñe mayúscula)'),
	
	# ============================================
	# DIÉRESIS - Ü/ü (U con diéresis)
	# ============================================
	('\x9a', 'Ü', '\\x9A → Ü (U con diéresis mayúscula)'),
	('\x81', 'ü', '\\x81 → ü (u con diéresis minúscula)'),
	('\x99', 'Ö', '\\x99 → Ö (O con diéresis mayúscula)'),
	('\x94', 'Ï', '\\x94 → Ï (I con diéresis mayúscula)'),
	('\x84', 'ä', '\\x84 → ä (a con diéresis minúscula)'),
	('\x8b', 'ï', '\\x8B → ï (i con diéresis minúscula)'),
	
	# ============================================
	# ACENTOS GRAVES
	# ============================================
	('\x87', 'à', '\\x87 → à (a con acento grave)'),
	('\x8a', 'è', '\\x8A → è (e con acento grave)'),
	('\x8d', 'ì', '\\x8D → ì (i con acento grave)'),
	('\x8e', 'ò', '\\x8E → ò (o con acento grave)'),
	('\x92', 'ù', '\\x92 → ù (u con acento grave)'),
	
	# ============================================
	# SEPARADORES
	# ============================================
	('\xff', ' ', '\\xFF → ESPACIO (carácter de separación)'),
	('\x00', ' ', 'NULL → espacio'),
	
	# ============================================
	# SÍMBOLOS
	# ============================================
	('\xa9', '©', '\\xA9 → © (Copyright)'),
	('\xae', '®', '\\xAE → ® (Registered)'),
	('\x9d', 'Ø', '\\x9D → Ø (O con barra mayúscula)'),
	('\x9c', 'ø', '\\x9C → ø (o con barra minúscula)'),
	('\xa7', 'º', '\\xA7 → º (símbolo ordinal)'),  # § → º
	
	# ============================================
	# PATRONES COMPUESTOS (para detectar mejor)
	# ============================================
	('N§', 'Nº', 'N§ → Nº (número ordinal)'),
	('N°', 'Nº', 'N° → Nº (número ordinal)'),
	('C§', 'Cº', 'C§ → Cº (número ordinal)'),
	('C°', 'Cº', 'C° → Cº (número ordinal)'),
]

#-- Versión simple para el procesamiento (sin descripciones)
CARACTERES_REEMPLAZO = [(malo, bueno) for malo, bueno, _ in CARACTERES_REEMPLAZO_CON_DESCRIPCION]

#-- Diccionario para búsquedas rápidas
CARACTERES_DESCRIPCIONES = {malo: desc for malo, _, desc in CARACTERES_REEMPLAZO_CON_DESCRIPCION}

#-- CARACTERES A ELIMINAR COMPLETAMENTE.
CARACTERES_ELIMINAR = [
	#-- Caracteres de control.
	'\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07',
	'\x08', '\x0b', '\x0c', '\x0e', '\x0f', '\x10', '\x11',
	'\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18',
	'\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x7f',
	'\xad',  # guión suave
	# '\xa0',  # espacio no separable (NBSP)
]

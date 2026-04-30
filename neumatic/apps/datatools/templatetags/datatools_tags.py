# neumatic\apps\datatools\templatetags\datatools_tags.py
from django import template


register = template.Library()


@register.filter
def get_item(dictionary, key):
	"""Para uso general - devuelve lista vacía"""
	return dictionary.get(key, [])


@register.filter
def get_dict_value(dictionary, key):
	"""Específico para valores de diccionario - devuelve cadena vacía"""
	return dictionary.get(key, '')


@register.filter
def text_color_from_bg(hex_color):
	"""
	Determina el color del texto basado en el color de fondo considerando luminosidad y saturación.
	"""
	if not hex_color or hex_color == '':
		print("DEBUG: Color vacío, retornando negro")
		return 'black'
	
	hex_color = hex_color.strip('#')
	
	try:
		if len(hex_color) == 3:
			r = int(hex_color[0] * 2, 16)
			g = int(hex_color[1] * 2, 16)
			b = int(hex_color[2] * 2, 16)
		else:
			r = int(hex_color[0:2], 16)
			g = int(hex_color[2:4], 16)
			b = int(hex_color[4:6], 16)
	except ValueError:
		return 'black'
	
	#-- Método 1: Luminosidad simple (YIQ).
	yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000
	
	#-- Método 2: Verificar si es un color "fuerte" (alta saturación).
	#-- Para colores muy saturados, usar texto blanco es más legible.
	max_val = max(r, g, b)
	min_val = min(r, g, b)
	
	#-- Calcular saturación (0-1).
	if max_val == 0:
		saturation = 0
	else:
		saturation = 1 - (min_val / max_val)
	
	#-- Si el color es muy saturado (> 0.5) y no es muy claro, usar blanco.
	is_high_saturation = saturation > 0.5
	is_not_very_light = yiq < 180  #-- No es casi blanco.
	
	# Regla de decisión mejorada:
	# 1. Si es oscuro (YIQ < 128) → blanco
	# 2. Si es color saturado y no muy claro → blanco (para rojos, azules fuertes)
	# 3. En otros casos → negro
	resultado = 'white' if (yiq < 128 or (is_high_saturation and is_not_very_light)) else 'black'
	
	return resultado


@register.filter
def is_dark_background(hex_color):
	"""
	Retorna True si el fondo es oscuro.
	"""
	text_color = text_color_from_bg(hex_color)
	return text_color == 'white'
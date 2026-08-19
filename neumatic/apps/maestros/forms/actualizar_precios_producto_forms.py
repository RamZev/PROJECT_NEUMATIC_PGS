# neumatic/apps/maestros/forms/actualizar_precios_producto_forms.py
from django import forms
from django.core.exceptions import ValidationError


class ActualizarPreciosProductoForm(forms.Form):
	"""
	Formulario para actualización masiva de precios/costos de productos.
	"""
	#-- Porcentaje único (puede ser positivo o negativo).
	porcentaje = forms.DecimalField(
		required=True,
		label="Porcentaje de ajuste (%)",
		min_value=-100,
		max_value=1000,
		decimal_places=2,
		help_text="Ej: 10 para +10%, -5 para -5% (no puede ser 0)",
		widget=forms.NumberInput(attrs={
			'class': 'form-control',
			'placeholder': 'Ej: 10 ó -10',
			'step': '0.01'
		})
	)
	
	#-- Campos para filtros (rangos de ID).
	id_familia_desde = forms.IntegerField(
		required=False,
		label="Familia desde",
		min_value=1,
		widget=forms.NumberInput(attrs={
			'class': 'form-control',
			'placeholder': 'Desde'
		})
	)
	id_familia_hasta = forms.IntegerField(
		required=False,
		label="Familia hasta",
		min_value=1,
		widget=forms.NumberInput(attrs={
			'class': 'form-control',
			'placeholder': 'Hasta'
		})
	)
	id_marca_desde = forms.IntegerField(
		required=False,
		label="Marca desde",
		min_value=1,
		widget=forms.NumberInput(attrs={
			'class': 'form-control',
			'placeholder': 'Desde'
		})
	)
	id_marca_hasta = forms.IntegerField(
		required=False,
		label="Marca hasta",
		min_value=1,
		widget=forms.NumberInput(attrs={
			'class': 'form-control',
			'placeholder': 'Hasta'
		})
	)
	id_modelo_desde = forms.IntegerField(
		required=False,
		label="Modelo desde",
		min_value=1,
		widget=forms.NumberInput(attrs={
			'class': 'form-control',
			'placeholder': 'Desde'
		})
	)
	id_modelo_hasta = forms.IntegerField(
		required=False,
		label="Modelo hasta",
		min_value=1,
		widget=forms.NumberInput(attrs={
			'class': 'form-control',
			'placeholder': 'Hasta'
		})
	)
	
	#-- Checkboxes para seleccionar qué actualizar.
	actualizar_costo = forms.BooleanField(
		required=False,
		label="Actualizar Costo",
		help_text="Aplica el porcentaje al costo del producto",
		widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
	)
	actualizar_precio = forms.BooleanField(
		required=False,
		label="Actualizar Precio",
		help_text="Aplica el porcentaje al precio del producto",
		widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
	)
	
	def clean(self):
		cleaned_data = super().clean()
		
		errors = {}
		
		porcentaje = cleaned_data.get('porcentaje')
		actualizar_costo = cleaned_data.get('actualizar_costo')
		actualizar_precio = cleaned_data.get('actualizar_precio')
		
		#-- Validar que el porcentaje no sea 0.
		if porcentaje == 0:
			errors['porcentaje'] = "El porcentaje debe ser distinto de cero. Use valores positivos para incrementar o negativos para disminuir."
		
		#-- Validar que al menos un checkbox esté marcado.
		if not actualizar_costo and not actualizar_precio:
			errors['actualizar_costo'] = "Debe seleccionar al menos un campo a actualizar (Costo o Precio)."
		
		#-- Validar rangos.
		id_familia_desde = cleaned_data.get('id_familia_desde')
		id_familia_hasta = cleaned_data.get('id_familia_hasta')
		id_marca_desde = cleaned_data.get('id_marca_desde')
		id_marca_hasta = cleaned_data.get('id_marca_hasta')
		id_modelo_desde = cleaned_data.get('id_modelo_desde')
		id_modelo_hasta = cleaned_data.get('id_modelo_hasta')
		
		#-- Validar que desde <= hasta para cada rango.
		if id_familia_desde and id_familia_hasta and id_familia_desde > id_familia_hasta:
			errors['id_familia_desde'] = "El rango de Familia 'Desde' debe ser menor o igual que 'Hasta'."
		
		if id_marca_desde and id_marca_hasta and id_marca_desde > id_marca_hasta:
			errors['id_marca_desde'] = "El rango de Marca 'Desde' debe ser menor o igual que 'Hasta'."
		
		if id_modelo_desde and id_modelo_hasta and id_modelo_desde > id_modelo_hasta:
			errors['id_modelo_desde'] = "El rango de Modelo 'Desde' debe ser menor o igual que 'Hasta'."
		
		if errors:
			raise ValidationError(errors)
		
		return cleaned_data

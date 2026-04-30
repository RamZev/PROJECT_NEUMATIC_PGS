# neumatic\apps\informes\forms\buscador_producto_forms.py
from django import forms

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import (formclasstext, formclassselect)
from entorno.constantes_base import ESTATUS_CHOICES


class BuscadorProductoForm(InformesGenericForm):
	
	estatus = forms.ChoiceField(
		choices=ESTATUS_CHOICES, 
		label="Estatus", 
		required=False,
		widget=forms.Select(attrs={**formclassselect})
	)
	id_familia_desde = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Desde Familia",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_familia_hasta = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Hasta Familia",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_marca_desde = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Desde Marca",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_marca_hasta = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Hasta Marca",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_modelo_desde = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Desde Modelo",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_modelo_hasta = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Hasta Modelo",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	
	def clean(self):
		cleaned_data = super().clean()
		
		id_familia_desde = cleaned_data.get('id_familia_desde') or 0
		id_familia_hasta = cleaned_data.get('id_familia_hasta') or 0
		id_marca_desde = cleaned_data.get('id_marca_desde') or 0
		id_marca_hasta = cleaned_data.get('id_marca_hasta') or 0
		id_modelo_desde = cleaned_data.get('id_modelo_desde') or 0
		id_modelo_hasta = cleaned_data.get('id_modelo_hasta') or 0
		
		#-- Validaciones.
		if id_familia_desde and id_familia_desde < 1:
			self.add_error("id_familia_desde", "Debe indicar un Código de Familia")
		
		if id_familia_hasta and id_familia_hasta < 1:
			self.add_error("id_familia_hasta", "Debe indicar un Código de Familia")
		
		if id_familia_desde and id_familia_hasta and id_familia_desde > id_familia_hasta:
			self.add_error("id_familia_hasta", "El Código de Familia hasta no puede ser menor al Código de Familia desde.")
		
		if id_marca_desde and id_marca_desde < 1:
			self.add_error("id_marca_desde", "Debe indicar un Código de Marca")
		
		if id_marca_hasta and id_marca_hasta < 1:
			self.add_error("id_marca_hasta", "Debe indicar un Código de Marca")
		
		if id_marca_desde and id_marca_hasta and id_marca_desde > id_marca_hasta:
			self.add_error("id_marca_hasta", "El Código de Marca hasta no puede ser menor al Código de Marca desde.")
		
		if id_modelo_desde and id_modelo_desde < 1:
			self.add_error("id_modelo_desde", "Debe indicar un Código de Modelo")
		
		if id_modelo_hasta and id_modelo_hasta < 1:
			self.add_error("id_modelo_hasta", "Debe indicar un Código de Modelo")
		
		if id_modelo_desde and id_modelo_hasta and id_modelo_desde > id_modelo_hasta:
			self.add_error("id_modelo_hasta", "El Código de Modelo hasta no puede ser menor al Código de Modelo desde.")
		
		return cleaned_data
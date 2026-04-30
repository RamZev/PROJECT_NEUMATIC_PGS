# neumatic\apps\maestros\forms\tarjeta_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import Tarjeta
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect,
	formclasscheck
)


class TarjetaForm(CrudGenericForm):
	
	class Meta:
		model = Tarjeta
		fields = '__all__'
		
		widgets = {
			'estatus_tarjeta': 
				forms.Select(attrs={**formclassselect}), 
			'nombre_tarjeta': 
				forms.TextInput(attrs={**formclasstext}),
			'imputacion': 
				forms.NumberInput(attrs={**formclasstext, 'min': 0}),
			'banco_acreditacion': 
				forms.NumberInput(attrs={**formclasstext, 'min': 0}),
			'propia': 
				forms.CheckboxInput(attrs={**formclasscheck}),
		}

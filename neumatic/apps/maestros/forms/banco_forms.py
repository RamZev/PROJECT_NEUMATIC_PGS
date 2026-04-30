# neumatic\apps\maestros\forms\banco_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import Banco
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class BancoForm(CrudGenericForm):
	
	class Meta:
		model = Banco
		fields = '__all__'
		
		widgets = {
			'estatus_banco': 
				forms.Select(attrs={**formclassselect}), 
			'codigo_banco': 
				forms.NumberInput(attrs={**formclasstext, 'min': 0}),
			'nombre_banco': 
				forms.TextInput(attrs={**formclasstext}),
			'cuit_banco': 
				forms.TextInput(attrs={**formclasstext}),
		}

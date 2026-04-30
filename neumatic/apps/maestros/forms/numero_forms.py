# neumatic\apps\maestros\forms\numero_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.numero_models import Numero
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class NumeroForm(CrudGenericForm):
	
	class Meta:
		model = Numero
		fields = '__all__'
		
		widgets = {
			'estatus_numero': 
				forms.Select(attrs={**formclassselect}),
			'id_sucursal': 
				forms.Select(attrs={**formclassselect}),
			'id_punto_venta': 
				forms.Select(attrs={**formclassselect}),
			'comprobante': 
				forms.TextInput(attrs={**formclasstext}),
			'letra': 
				forms.TextInput(attrs={**formclasstext}),
			'numero': 
				forms.NumberInput(attrs={**formclasstext, 'min': 1, 'max': 9999999999999}),
			'lineas': 
				forms.NumberInput(attrs={**formclasstext, 'min': 1, 'max': 99}),
			'copias': 
				forms.NumberInput(attrs={**formclasstext, 'min': 1, 'max': 9}),
		}

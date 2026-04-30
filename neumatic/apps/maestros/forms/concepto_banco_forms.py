# neumatic\apps\maestros\forms\concepto_banco_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import ConceptoBanco
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class ConceptoBancoForm(CrudGenericForm):
	
	class Meta:
		model = ConceptoBanco
		fields = '__all__'
		
		widgets = {
			'estatus_concepto_banco': 
				forms.Select(attrs={**formclassselect}),
			'nombre_concepto_banco': 
				forms.TextInput(attrs={**formclasstext}),
			'factor': 
				forms.NumberInput(attrs={**formclasstext, 'min': -1, 'max': 1}),
		}

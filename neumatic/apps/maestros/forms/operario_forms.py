# neumatic\apps\maestros\forms\operario_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import Operario
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class OperarioForm(CrudGenericForm):
	
	class Meta:
		model = Operario
		fields = '__all__'
		
		widgets = {
			'estatus_operario': 
				forms.Select(attrs={**formclassselect}),
			'nombre_operario': 
				forms.TextInput(attrs={**formclasstext}),
			'telefono_operario': 
				forms.TextInput(attrs={**formclasstext}),
			'email_operario': 
				forms.TextInput(attrs={**formclasstext}),
		}

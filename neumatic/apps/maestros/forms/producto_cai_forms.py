# # neumatic\apps\maestros\forms\cai_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import ProductoCai
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class CaiForm(CrudGenericForm):
	
	class Meta:
		model = ProductoCai
		fields = '__all__'
		
		widgets = {
		'estatus_cai': 
				forms.Select(attrs={**formclassselect}), 
			'cai': 
				forms.TextInput(attrs={**formclasstext}),
			'descripcion_cai': 
				forms.TextInput(attrs={**formclasstext}),
		}
		
		error_messages = {
			'cai':{
				'unique': 'Este CAI ya existe.',
				# 'required': 'Debe completar este campo.',
				# 'invalid': 'Ingrese un valor válido.'
			},
		}

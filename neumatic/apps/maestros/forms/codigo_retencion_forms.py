# neumatic\apps\maestros\forms\codigo_retencion_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import CodigoRetencion
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class CodigoRetencionForm(CrudGenericForm):
	
	class Meta:
		model = CodigoRetencion
		fields = '__all__'
		
		widgets = {
			'estatus_cod_retencion': 
				forms.Select(attrs={**formclassselect}), 
			'nombre_codigo_retencion': 
				forms.TextInput(attrs={**formclasstext}),
			'imputacion': 
				forms.NumberInput(attrs={**formclasstext, 'min': 0}),
		}

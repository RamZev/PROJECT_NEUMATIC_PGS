# neumatic\apps\maestros\forms\tipo_iva_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import TipoIva
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect,
	formclasscheck
)


class TipoIvaForm(CrudGenericForm):
	
	class Meta:
		model = TipoIva
		fields = '__all__'
		
		widgets = {
			'estatus_tipo_iva': 
				forms.Select(attrs={**formclassselect}),
			'codigo_iva': 
				forms.TextInput(attrs={**formclasstext, 'oninput': 'this.value = this.value.toUpperCase()'}),
			'nombre_iva': 
				forms.TextInput(attrs={**formclasstext}),
			'discrimina_iva': 
				forms.CheckboxInput(attrs={**formclasscheck}),
			'codigo_afip_responsable': 
				forms.NumberInput(attrs={**formclasstext,}),
		}
		
		error_messages = {
			'codigo_iva': {
				'unique': 'Ya existe un tipo de IVA con el mismo código.',
				# 'required': 'Debe completar este campo.',
				# 'invalid': 'Ingrese un valor válido.'
			},
			'codigo_afip_responsable': {
				'unique': 'Ya existe un tipo de IVA con el mismo código AFIP.',
				# 'required': 'Debe completar este campo.',
				# 'invalid': 'Ingrese un valor válido.'
			},
		}

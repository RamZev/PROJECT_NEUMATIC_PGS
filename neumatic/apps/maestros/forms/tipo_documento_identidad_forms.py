# neumatic\apps\maestros\forms\tipo_documento_identidad_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import TipoDocumentoIdentidad
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class TipoDocumentoIdentidadForm(CrudGenericForm):
	
	class Meta:
		model = TipoDocumentoIdentidad
		fields = '__all__'
		
		widgets = {
			'estatus_tipo_documento_identidad': 
				forms.Select(attrs={**formclassselect}),
			'nombre_documento_identidad': 
				forms.TextInput(attrs={**formclasstext}),
			'tipo_documento_identidad': 
				forms.TextInput(attrs={**formclasstext}),
			'codigo_afip': 
				forms.TextInput(attrs={**formclasstext}),
			'ws_afip': 
				forms.TextInput(attrs={**formclasstext}),
		}
		
		error_messages = {
			'tipo_documento_identidad': {
				'unique': 'Ya existe un documento de identidad con el mismo tipo.',
				# 'required': 'Debe completar este campo.',
				# 'invalid': 'Ingrese un valor válido.'
			},
		}

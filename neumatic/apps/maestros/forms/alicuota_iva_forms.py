# neumatic\apps\maestros\forms\alicuota_iva_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import AlicuotaIva
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect,
	formclassnumb
)


class AlicuotaIvaForm(CrudGenericForm):
	
	class Meta:
		model = AlicuotaIva
		fields = '__all__'
		
		widgets = {
			'estatus_alicuota_iva': 
				forms.Select(attrs={**formclassselect}),
			'codigo_alicuota': 
				forms.TextInput(attrs={**formclasstext}),
			'alicuota_iva': 
				forms.TextInput(attrs={**formclassnumb}),
			'descripcion_alicuota_iva': 
				forms.TextInput(attrs={**formclasstext}),
		}
		
		error_messages = {
			'codigo_alicuota': {
				'unique': 'Ya existe una Alícuota de IVA con el mismo código.',
				# 'required': 'Debe completar este campo.',
				# 'invalid': 'Ingrese un valor válido.'
			},
			'alicuota_iva': {
				'unique': 'La Alícuota ya está registrada.',
				# 'required': 'Debe completar este campo.',
				# 'invalid': 'Ingrese un valor válido.'
			},
		}

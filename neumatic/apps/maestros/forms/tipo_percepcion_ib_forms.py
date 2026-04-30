# neumatic\apps\maestros\forms\tipo_iva_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import TipoPercepcionIb
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect,
	formclasscheck,
	formclassnumb
)


class TipoPercepcionIbForm(CrudGenericForm):
	
	class Meta:
		model = TipoPercepcionIb
		fields = '__all__'
		
		widgets = {
			'estatus_tipo_percepcion_ib': 
				forms.Select(attrs={**formclassselect}),
			'descripcion_tipo_percepcion_ib': 
				forms.TextInput(attrs={**formclasstext}),
			'alicuota': 
				forms.TextInput(attrs={**formclassnumb}),
			'monto': 
				forms.TextInput(attrs={**formclassnumb}),
			'minimo': 
				forms.TextInput(attrs={**formclassnumb}),
			'neto_total': 
				forms.CheckboxInput(attrs={**formclasscheck}),
		}

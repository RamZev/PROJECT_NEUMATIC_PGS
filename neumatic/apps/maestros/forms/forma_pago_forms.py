# neumatic\apps\maestros\forms\forma_pago_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import FormaPago
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class FormaPagoForm(CrudGenericForm):
	
	class Meta:
		model = FormaPago
		fields = '__all__'
		
		widgets = {
			'estatus_forma_pago': 
				forms.Select(attrs={**formclassselect}), 
			'descripcion_forma_pago': 
				forms.TextInput(attrs={**formclasstext}),
		}

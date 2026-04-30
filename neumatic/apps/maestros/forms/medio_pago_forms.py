# neumatic\apps\maestros\forms\medio_pago_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import MedioPago
from diseno_base.diseno_bootstrap import (
	formclasstext,
	formclassselect
)


class MedioPagoForm(CrudGenericForm):
	
	class Meta:
		model = MedioPago
		fields = '__all__'
		
		widgets = {
			'estatus_medio_pago': 
				forms.Select(attrs={**formclassselect}), 
			'nombre_medio_pago': 
				forms.TextInput(attrs={**formclasstext,
										'placeholder': 'Medio de Pago'}),
			'condicion_medio_pago': 
				forms.Select(attrs={**formclassselect}), 
			'plazo_medio_pago': 
				forms.TextInput(attrs={**formclasstext,
										'placeholder': 'Plazo'}),
		}


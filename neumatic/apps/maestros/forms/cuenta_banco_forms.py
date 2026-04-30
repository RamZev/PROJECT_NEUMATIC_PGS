# neumatic\apps\maestros\forms\cuenta_banco_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import CuentaBanco
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect,
	formclassnumb
)


class CuentaBancoForm(CrudGenericForm):
	
	class Meta:
		model = CuentaBanco
		fields = '__all__'
		
		widgets = {
			'estatus_cuenta_banco': 
				forms.Select(attrs={**formclassselect}), 
			'id_banco': 
				forms.Select(attrs={**formclassselect}),
			'numero_cuenta': 
				forms.TextInput(attrs={**formclasstext}),
			'tipo_cuenta': 
				forms.Select(attrs={**formclassselect}), 
			'cbu': 
				forms.TextInput(attrs={**formclasstext}),
			'sucursal': 
				forms.NumberInput(attrs={**formclasstext, 'min': 0}),
			'codigo_postal': 
				forms.NumberInput(attrs={**formclasstext, 'min': 0}),
			'codigo_imputacion': 
				forms.NumberInput(attrs={**formclasstext, 'min': 0}),
			'tope_negociacion': 
				forms.TextInput(attrs={**formclassnumb, 
							 	  'min': 0, 'max': 9999999999.99}),
			'reporte_reques': 
				forms.TextInput(attrs={**formclasstext}),
			'id_proveedor': 
				forms.Select(attrs={**formclassselect}),
			'id_moneda': 
				forms.Select(attrs={**formclassselect}),
		}

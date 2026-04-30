# neumatic\apps\maestros\forms\punto_venta_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import PuntoVenta
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class PuntoVentaForm(CrudGenericForm):
	
	class Meta:
		model = PuntoVenta
		fields = '__all__'
		
		widgets = {
			'estatus_punto_venta': 
				forms.Select(attrs={**formclassselect}),
			'id_sucursal': 
				forms.Select(attrs={**formclassselect}),
			'punto_venta': 
				forms.TextInput(attrs={**formclasstext}),
			'descripcion_punto_venta': 
				forms.TextInput(attrs={**formclasstext}),
		}
		
		error_messages = {
			'punto_venta': {
				'unique': 'Este Punto de Venta ya existe.',
				# 'required': 'Debe completar este campo.',
				# 'invalid': 'Ingrese un valor válido.'
			},
		}

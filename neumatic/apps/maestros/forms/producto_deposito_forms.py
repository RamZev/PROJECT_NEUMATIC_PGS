# neumatic\apps\maestros\forms\producto_deposito_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import ProductoDeposito
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class ProductoDepositoForm(CrudGenericForm):
	
	class Meta:
		model = ProductoDeposito
		fields = '__all__'
		
		widgets = {
			'estatus_producto_deposito': 
				forms.Select(attrs={**formclassselect}),
			'nombre_producto_deposito': 
				forms.TextInput(attrs={**formclasstext}),
			'id_sucursal': 
				forms.Select(attrs={**formclassselect}),
		}

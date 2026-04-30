# neumatic\apps\maestros\forms\producto_stock_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import ProductoStock
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect,
	formclassdate
)


class ProductoStockForm(CrudGenericForm):
	
	class Meta:
		model = ProductoStock
		fields = '__all__'
		
		widgets = {
			'id_producto': 
				forms.Select(attrs={**formclassselect}),
			'id_deposito': 
				forms.Select(attrs={**formclassselect}),
			'stock': 
				forms.TextInput(attrs={**formclasstext}),
			'minimo': 
				forms.TextInput(attrs={**formclasstext}),
			'fecha_producto_stock': 
				forms.TextInput(attrs={**formclassdate, 'type': 'date'}),
		}

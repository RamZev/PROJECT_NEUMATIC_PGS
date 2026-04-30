# neumatic\apps\maestros\forms\producto_marca_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import ProductoMarca
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect,
	formclasscheck
)


class ProductoMarcaForm(CrudGenericForm):
	
	class Meta:
		model = ProductoMarca
		fields = '__all__'
		
		widgets = {
			'estatus_producto_marca': 
				forms.Select(attrs={**formclassselect}),
			'nombre_producto_marca': 
				forms.TextInput(attrs={**formclasstext}),
			'principal': 
				forms.CheckboxInput(attrs={**formclasscheck}),
			'info_michelin_auto': 
				forms.CheckboxInput(attrs={**formclasscheck}),
			'info_michelin_camion': 
				forms.CheckboxInput(attrs={**formclasscheck}),
			'id_moneda': 
				forms.Select(attrs={**formclassselect}),
		}

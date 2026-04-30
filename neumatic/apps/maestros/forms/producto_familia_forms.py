# neumatic\apps\maestros\forms\producto_familia_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import ProductoFamilia
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect,
	formclasscheck
)


class ProductoFamiliaForm(CrudGenericForm):
	
	class Meta:
		model = ProductoFamilia
		fields = '__all__'
		
		widgets = {
			'estatus_producto_familia':
				forms.Select(attrs={**formclassselect}),
			'nombre_producto_familia':
				forms.TextInput(attrs={**formclasstext}),
			'comision_operario':
				forms.NumberInput(attrs={**formclasstext,
										 'min': 0, 'max': 99.99}),
			'info_michelin_auto':
				forms.CheckboxInput(attrs={**formclasscheck}),
			'info_michelin_camion':
				forms.CheckboxInput(attrs={**formclasscheck}),
		}

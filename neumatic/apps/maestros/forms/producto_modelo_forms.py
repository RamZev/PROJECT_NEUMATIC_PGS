# neumatic\apps\maestros\forms\producto_modelo_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import ProductoModelo
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class ProductoModeloForm(CrudGenericForm):
	
	class Meta:
		model = ProductoModelo
		fields = '__all__'
		
		widgets = {
			'estatus_modelo': 
				forms.Select(attrs={**formclassselect}),
			'nombre_modelo': 
				forms.TextInput(attrs={**formclasstext}),
		}

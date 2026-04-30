# neumatic\apps\maestros\forms\localidad_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import Localidad
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class LocalidadForm(CrudGenericForm):
	
	class Meta:
		model = Localidad
		fields = '__all__'
		
		widgets = {
			'estatus_localidad': 
				forms.Select(attrs={**formclassselect}),
			'id_provincia': 
				forms.Select(attrs={**formclassselect}),
			'codigo_postal': 
				forms.TextInput(attrs={**formclasstext}),
			'nombre_localidad': 
				forms.TextInput(attrs={**formclasstext}),
		}

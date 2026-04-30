# neumatic\apps\maestros\forms\actividad_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import Actividad
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class ActividadForm(CrudGenericForm):
	
	class Meta:
		model = Actividad
		fields = '__all__'
		
		widgets = {
			'estatus_actividad': 
				forms.Select(attrs={**formclassselect}), 
			'descripcion_actividad': 
				forms.TextInput(attrs={**formclasstext}),
		}

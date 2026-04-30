# neumatic\apps\maestros\forms\marketing_origen_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import MarketingOrigen
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class MarketingOrigenForm(CrudGenericForm):
	
	class Meta:
		model = MarketingOrigen
		fields = '__all__'
		
		widgets = {
			'estatus_marketing_origen':
				forms.Select(attrs={**formclassselect}), 
			'nombre_marketing_origen':
				forms.TextInput(attrs={**formclasstext}),
		}

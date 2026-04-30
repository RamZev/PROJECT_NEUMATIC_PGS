# neumatic\apps\informes\forms\buscador_moneda_forms.py
from django import forms

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassselect
from entorno.constantes_base import ESTATUS_CHOICES


class BuscadorMonedaForm(InformesGenericForm):
	
	estatus = forms.ChoiceField(
		choices=ESTATUS_CHOICES, 
		label="Estatus", 
		required=False,
		widget=forms.Select(attrs={**formclassselect})
	)
	
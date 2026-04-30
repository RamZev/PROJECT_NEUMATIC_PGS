# neumatic\apps\informes\forms\buscador_localidad_forms.py
from django import forms

from .informes_generics_forms import InformesGenericForm
from apps.maestros.models.base_models import Provincia
from diseno_base.diseno_bootstrap import formclassselect
from entorno.constantes_base import ESTATUS_CHOICES, ORDEN_CHOICES


class BuscadorLocalidadForm(InformesGenericForm):
	
	estatus = forms.ChoiceField(
		choices=ESTATUS_CHOICES, 
		label="Estatus", 
		required=False,
		widget=forms.Select(attrs={**formclassselect})
	)
	orden = forms.ChoiceField(
		choices=ORDEN_CHOICES, 
		label="Ordenar por", 
		required=False,
		widget=forms.Select(attrs={**formclassselect})
	)
	provincia = forms.ModelChoiceField(
		queryset=Provincia.objects.all(), 
		required=False,
		label="Provincia",
		widget=forms.Select(attrs={**formclassselect})
	)

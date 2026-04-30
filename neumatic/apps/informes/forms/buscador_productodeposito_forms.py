# neumatic\apps\informes\forms\buscador_productodeposito_forms.py
from django import forms

from .informes_generics_forms import InformesGenericForm
from apps.maestros.models.sucursal_models import Sucursal
from diseno_base.diseno_bootstrap import formclassselect
from entorno.constantes_base import ESTATUS_CHOICES


class BuscadorProductoDepositoForm(InformesGenericForm):
	
	estatus = forms.ChoiceField(
		choices=ESTATUS_CHOICES, 
		label="Estatus", 
		required=False,
		widget=forms.Select(attrs={**formclassselect})
	)
	sucursal = forms.ModelChoiceField(
		queryset=Sucursal.objects.filter(estatus_sucursal=True), 
		required=False,
		label="Sucursal",
		widget=forms.Select(attrs={**formclassselect})
	)

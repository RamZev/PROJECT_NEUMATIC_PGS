# neumatic\apps\informes\forms\buscador_banco_forms.py
from django import forms

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassselect
from entorno.constantes_base import ESTATUS_CHOICES


class BuscadorBancoForm(InformesGenericForm):
	
	estatus = forms.ChoiceField(
		choices=ESTATUS_CHOICES,
		label="Estatus",
		required=False,
		widget=forms.Select(attrs={**formclassselect})
	)

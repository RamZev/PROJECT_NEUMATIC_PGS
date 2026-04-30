# neumatic\apps\informes\forms\buscador_vlstockdeposito_forms.py
from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from apps.maestros.models.sucursal_models import Sucursal
from diseno_base.diseno_bootstrap import formclassselect


class BuscadorStockDepositoForm(InformesGenericForm):
	
	sucursal = forms.ModelChoiceField(
		queryset=Sucursal.objects.filter(estatus_sucursal=True), 
		required=False,
		label="Sucursal",
		widget=forms.Select(attrs={**formclassselect})
	)

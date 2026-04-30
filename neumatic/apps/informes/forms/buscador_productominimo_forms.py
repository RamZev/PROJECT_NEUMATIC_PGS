# neumatic\apps\informes\forms\buscador_productominimo_forms.py
from django import forms

from .informes_generics_forms import InformesGenericForm
from apps.maestros.models.base_models import ProductoCai, ProductoDeposito
from diseno_base.diseno_bootstrap import formclassselect


class BuscadorProductoMinimoForm(InformesGenericForm):
	
	cai = forms.ModelChoiceField(
		queryset=ProductoCai.objects.all(), 
		required=False,
		label="CAI",
		widget=forms.Select(attrs={**formclassselect})
	)
	deposito = forms.ModelChoiceField(
		queryset=ProductoDeposito.objects.filter(estatus_producto_deposito=True), 
		required=False,
		label="Depósito",
		widget=forms.Select(attrs={**formclassselect})
	)

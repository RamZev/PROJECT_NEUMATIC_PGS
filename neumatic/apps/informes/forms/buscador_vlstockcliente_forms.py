# neumatic\apps\informes\forms\buscador_vlstockcliente_forms.py
from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.vendedor_models import Vendedor
from diseno_base.diseno_bootstrap import formclassselect


class BuscadorStockClienteForm(InformesGenericForm):
	
	sucursal = forms.ModelChoiceField(
		queryset=Sucursal.objects.filter(estatus_sucursal=True), 
		required=False,
		label="Sucursal",
		widget=forms.Select(attrs={**formclassselect})
	)
	vendedor = forms.ModelChoiceField(
		queryset=Vendedor.objects.filter(estatus_vendedor=True), 
		required=False,
		label="Vendedor",
		widget=forms.Select(attrs={**formclassselect})
	)

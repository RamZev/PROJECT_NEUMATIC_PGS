# neumatic\apps\informes\forms\buscador_vlclienteultimaventa_forms.py

from django import forms

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassdate, formclassselect
from apps.maestros.models.vendedor_models import Vendedor
from entorno.constantes_base import ORDEN


class BuscadorClienteUltimaVentaForm(InformesGenericForm):
	
	vendedor = forms.ModelChoiceField(
		queryset=Vendedor.objects.filter(estatus_vendedor=True), 
		required=True,
		label="Vendedor",
		widget=forms.Select(attrs={**formclassselect})
	)
	fecha_consulta = forms.DateField(
		required=True, 
		label="Sin Mov. desde",
		widget=forms.TextInput(attrs={'type':'date', **formclassdate})
	)
	orden = forms.ChoiceField(
		choices=ORDEN, 
		label="Ordenar por", 
		required=True,
		widget=forms.Select(attrs={**formclassselect})
	)

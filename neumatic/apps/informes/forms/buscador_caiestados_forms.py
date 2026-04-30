# neumatic\apps\informes\forms\buscador_caiestados_forms.py
from django import forms

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassselect, formclasstext
from entorno.constantes_base import ESTATUS_CHOICES


class BuscadorCaiEstadosForm(InformesGenericForm):
	
	estatus = forms.ChoiceField(
		choices=ESTATUS_CHOICES, 
		label="Estatus", 
		required=False,
		widget=forms.Select(attrs={**formclassselect})
	)
	medida = forms.CharField(
		max_length=20,
		required=False, 
		label="Medida", 
		widget=forms.TextInput(attrs={**formclasstext})
	)
	nombre_producto = forms.CharField(
		max_length=50,
		required=False, 
		label="Descripción Producto", 
		widget=forms.TextInput(attrs={**formclasstext})
	)
	
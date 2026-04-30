# neumatic\apps\informes\forms\buscador_vlivaventasprovincias_forms.py

from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassselect, formclasstext
from apps.maestros.models.sucursal_models import Sucursal
from entorno.constantes_base import MESES


class BuscadorVLIVAVentasProvinciasForm(InformesGenericForm):
	
	sucursal = forms.ModelChoiceField(
		queryset=Sucursal.objects.filter(estatus_sucursal=True), 
		required=False,
		label="Sucursal",
		widget=forms.Select(attrs={**formclassselect})
	)
	mes = forms.ChoiceField(
		choices=MESES, 
		label="Mes", 
		required=True,
		widget=forms.Select(attrs={**formclassselect})
	)
	anno = forms.IntegerField(
		required=True, 
		label="Año", 
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		if "anno" not in self.initial:
			anno = date.today().year
			self.fields["anno"].initial = anno
			self.fields["anno"].widget.attrs["value"] = anno
		if "mes" not in self.initial:
			mes_actual = date.today().strftime('%m')
			self.fields["mes"].initial = mes_actual
		
	def clean(self):
		cleaned_data = super().clean()
		
		anno = cleaned_data.get("anno") or 0
		
		if anno <= 0:
			self.add_error("anno", "Debe indicar un año válido.")
		
		return cleaned_data

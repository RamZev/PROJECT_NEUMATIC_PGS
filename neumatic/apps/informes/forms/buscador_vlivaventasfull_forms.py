# neumatic\apps\informes\forms\buscador_vlivaventasfull_forms.py

from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassselect, formclasstext, formclasscheck
from apps.maestros.models.sucursal_models import Sucursal
from entorno.constantes_base import MESES


class BuscadorVLIVAVentasFULLForm(InformesGenericForm):
	
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
	folio = forms.IntegerField(
		min_value=0,
		initial=0,
		required=False,
		label="Último Folio",
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
		if "folio" not in self.initial:
			self.fields["folio"].initial = 0
			self.fields["folio"].widget.attrs["value"] = 0	
		
	def clean(self):
		cleaned_data = super().clean()
		
		anno = cleaned_data.get("anno") or 0
		folio = cleaned_data.get("folio") or 0
		
		if anno <= 0:
			self.add_error("anno", "Debe indicar un año válido.")
		
		if folio < 0:
			self.add_error("folio", "El Número de Folio no puede ser negativo.")
		
		return cleaned_data

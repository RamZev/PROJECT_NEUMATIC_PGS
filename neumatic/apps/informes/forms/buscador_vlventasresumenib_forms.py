# neumatic\apps\informes\forms\buscador_vlventasresumenib_forms.py

from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassselect, formclasstext
from apps.maestros.models.base_models import Provincia
from apps.maestros.models.sucursal_models import Sucursal
from entorno.constantes_base import MESES

class BuscadorVLVentasResumenIBForm(InformesGenericForm):
	
	sucursal = forms.ModelChoiceField(
		queryset=Sucursal.objects.filter(estatus_sucursal=True), 
		required=True,
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
	importe_max = forms.DecimalField(
		max_digits=14,
		decimal_places=2,
		min_value=0.0,
		required=False,
		label="Importe máx. por menor",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	provincias = forms.ModelMultipleChoiceField(
		# queryset=Provincia.objects.filter(estatus_provincia=True),
		queryset=Provincia.objects.filter(estatus_provincia=True).exclude(id_provincia=13),
		label="Elegir Provincias distintas a Santa Fe",
		required=True,
		widget=forms.SelectMultiple(attrs={'size': 10, **formclassselect}),
		# to_field_name='codigo_comprobante_venta'
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
		if "importe_max" not in self.initial:
			self.fields["importe_max"].initial = 1500.0
			self.fields["importe_max"].widget.attrs["value"] = 1500.0
		
	def clean(self):
		cleaned_data = super().clean()
		
		anno = cleaned_data.get("anno") or 0
		
		if anno <= 0:
			self.add_error("anno", "Debe indicar un año válido.")
		
		return cleaned_data

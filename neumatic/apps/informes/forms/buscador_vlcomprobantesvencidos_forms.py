# neumatic\apps\informes\forms\buscador_vlcomprobantesvencidos_forms.py

from django import forms

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassselect, formclasstext
from apps.maestros.models.vendedor_models import Vendedor
from apps.maestros.models.sucursal_models import Sucursal


class BuscadorComprobantesVencidosForm(InformesGenericForm):
	
	dias = forms.IntegerField(
		required=False, 
		label="Antigüedad mayor a",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	vendedor = forms.ModelChoiceField(
		queryset=Vendedor.objects.filter(estatus_vendedor=True), 
		required=False,
		initial=0,
		label="Vendedor",
		widget=forms.Select(attrs={**formclassselect})
	)
	sucursal = forms.ModelChoiceField(
		queryset=Sucursal.objects.filter(estatus_sucursal=True), 
		required=False,
		label="Sucursal",
		widget=forms.Select(attrs={**formclassselect})
	)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		if "dias" not in self.initial:
			self.fields["dias"].initial = 0
			self.fields["dias"].widget.attrs["value"] = 0

	def clean(self):
		cleaned_data = super().clean()
		
		dias = cleaned_data.get("dias") or 0
		
		if dias < 0:
			self.add_error('dias', "No puede indicar un número negativo.")
	
		return cleaned_data
	
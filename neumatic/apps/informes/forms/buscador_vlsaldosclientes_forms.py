# neumatic\apps\informes\forms\buscador_vlsaldosclientes_forms.py
from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassselect, formclassdate
from apps.maestros.models.vendedor_models import Vendedor


class BuscadorSaldosClientesForm(InformesGenericForm):
	
	CLIENTE_VENDEDOR = [
		('clientes', 'Todos los Clientes'),
		('vendedor', 'Seleccionar por Vendedor'),
	]
	
	cliente_vendedor = forms.ChoiceField(
		choices=CLIENTE_VENDEDOR, 
		label="Clientes a Listar", 
		required=False,
		widget=forms.Select(attrs={**formclassselect})
	)
	fecha_hasta = forms.DateField(
		required=False, 
		label="A Fecha",
		widget=forms.TextInput(attrs={'type':'date', **formclassdate})
	)
	vendedor = forms.ModelChoiceField(
		queryset=Vendedor.objects.all(), 
		required=False,
		label="Vendedor",
		widget=forms.Select(attrs={**formclassselect})
	)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if "fecha_hasta" not in self.initial:
			fecha_actual = date.today()
			self.fields["fecha_hasta"].initial = fecha_actual
			self.fields["fecha_hasta"].widget.attrs["value"] = fecha_actual

	def clean(self):
		cleaned_data = super().clean()
		
		fecha_hasta = cleaned_data.get("fecha_hasta")
		
		#-- Validar fecha.
		if not fecha_hasta:
			self.add_error('fecha_hasta', "Debe indicar una fecha válida.")
	
		return cleaned_data
	
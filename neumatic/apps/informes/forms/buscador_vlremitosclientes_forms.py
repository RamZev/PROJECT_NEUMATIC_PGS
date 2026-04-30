# neumatic\apps\informes\forms\buscador_vlremitosclientes_forms.py

from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from apps.maestros.models.cliente_models import Cliente
from diseno_base.diseno_bootstrap import formclasstext, formclassdate


class BuscadorRemitosClientesForm(InformesGenericForm):
	
	fecha_desde = forms.DateField(
		required=False, 
		label="Desde Fecha",
		widget=forms.TextInput(attrs={'type':'date', **formclassdate})
	)
	fecha_hasta = forms.DateField(
		required=False, 
		label="Hasta Fecha",
		widget=forms.TextInput(attrs={'type':'date', **formclassdate})
	)
	id_cliente = forms.IntegerField(
		label="Cód. Cliente",
		required=True,
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	nombre_cliente = forms.CharField(
		label="Cliente",
		required=False,
		widget=forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'})
	)
	
	def __init__(self, *args, **kwargs):
		"""
		Inicializa el formulario con valores predeterminados:
		- `fecha_desde` se establece en el 1 de enero del año actual.
		- `fecha_hasta` se establece en la fecha actual.
		"""
		
		super().__init__(*args, **kwargs)
		
		if "fecha_desde" not in self.initial:
			fecha_inicial = date(date.today().year, 1, 1)
			self.fields["fecha_desde"].initial = fecha_inicial
			self.fields["fecha_desde"].widget.attrs["value"] = fecha_inicial
		if "fecha_hasta" not in self.initial:
			fecha_actual = date.today()
			self.fields["fecha_hasta"].initial = fecha_actual
			self.fields["fecha_hasta"].widget.attrs["value"] = fecha_actual
	
	def clean(self):
		cleaned_data = super().clean()
		
		id_cliente = cleaned_data.get("id_cliente")
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		
		#-- Validaciones.
		if not id_cliente:
			self.add_error("id_cliente", "Debe indicar un Código de Cliente.")
		
		if id_cliente:
			try:
				cliente = Cliente.objects.get(id_cliente=id_cliente)
			except Cliente.DoesNotExist:
				self.add_error("id_cliente", "El cliente no existe. Por favor, verifique el código.")
		
		if not fecha_desde:
			self.add_error("fecha_desde", "Debe indicar una fecha válida.")
		
		if not fecha_hasta:
			self.add_error("fecha_hasta", "Debe indicar una fecha válida.")
		
		if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
			self.add_error("fecha_hasta", "La fecha hasta no puede ser anterior a la fecha desde.")
		
		return cleaned_data
	
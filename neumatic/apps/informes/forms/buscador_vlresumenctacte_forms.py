# neumatic\apps\informes\forms\buscador_vlresumenctacte_forms.py
from django import forms
from datetime import date
from .informes_generics_forms import InformesGenericForm
from apps.maestros.models.cliente_models import Cliente
from diseno_base.diseno_bootstrap import formclassselect, formclassdate, formclasscheck, formclasstext


class BuscadorResumenCtaCteForm(InformesGenericForm):
	
	CONDICION_VENTA = [
		(1, 'Contado'),
		(2, 'Cuenta Corriente'),
		(0, 'Ambos'),
	]
	
	resumen_pendiente = forms.BooleanField(
		label="Resumen de Cuenta Pendiente",
		required=False,
		widget=forms.CheckboxInput(attrs={**formclasscheck})
	)
	condicion_venta = forms.ChoiceField(
		choices=CONDICION_VENTA, 
		label="Condición de Venta", 
		required=False,
		widget=forms.Select(attrs={**formclassselect})
	)
	fecha_desde = forms.DateField(
		required=False, 
		label="Desde Fecha",
		widget=forms.TextInput(attrs={'type':'date', **formclassdate}),
	)
	fecha_hasta = forms.DateField(
		required=False, 
		label="Hasta Fecha",
		widget=forms.TextInput(attrs={'type':'date', **formclassdate}),
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
	observaciones = forms.CharField(
		label="Leyenda",
		required=False,
		widget=forms.Textarea(attrs={'rows':2, **formclasstext})
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
		
		resumen_pendiente = cleaned_data.get('resumen_pendiente')
		id_cliente = cleaned_data.get("id_cliente")
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		
		#-- Si resumen_pendiente no está marcado (False), se requieren las fechas y la condición de venta.
		if not resumen_pendiente:
			#-- Validar fechas.
			if not fecha_desde:
				self.add_error('fecha_desde', "Debe indicar una fecha válida.")
			
			if not fecha_hasta:
				self.add_error('fecha_hasta', "Debe indicar una fecha válida.")
			
			if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
				self.add_error("fecha_hasta", "La fecha hasta no puede ser anterior a la fecha desde.")
		
		#-- Validar que se haya indicado un cliente solo si hay datos enviados.
		if not id_cliente:
			self.add_error("id_cliente", "Debe indicar un Código de Cliente.")
		
		if id_cliente:
			try:
				cliente = Cliente.objects.get(id_cliente=id_cliente)
			except Cliente.DoesNotExist:
				self.add_error("id_cliente", "El cliente no existe. Por favor, verifique el código.")
		
		return cleaned_data
	
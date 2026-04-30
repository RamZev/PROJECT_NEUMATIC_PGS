# neumatic\apps\informes\forms\buscador_vlfichaseguimientostock_forms.py
from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from apps.maestros.models.sucursal_models import Sucursal
from diseno_base.diseno_bootstrap import formclassselect, formclassdate, formclasstext


class BuscadorFichaSeguimientoStockForm(InformesGenericForm):
	
	sucursal = forms.ModelChoiceField(
		queryset=Sucursal.objects.filter(estatus_sucursal=True), 
		required=False,
		label="Sucursal",
		widget=forms.Select(attrs={**formclassselect})
	)
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
	codigo = forms.IntegerField(
		label="Código",
		required=False,
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	cai = forms.CharField(
		max_length=20,
		label="CAI",
		required=False,
		widget=forms.TextInput(attrs={**formclasstext})
	)
	medida = forms.CharField(
		label="Medida",
		required=False,
		widget=forms.TextInput(attrs={**formclasstext, 'disabled': 'disabled'})
	)
	producto = forms.CharField(
		label="Producto",
		required=False,
		widget=forms.TextInput(attrs={**formclasstext, 'disabled': 'disabled'})
	)
	marca = forms.CharField(
		label="Marca",
		required=False,
		widget=forms.TextInput(attrs={**formclasstext, 'disabled': 'disabled'})
	)
	
	def __init__(self, *args, **kwargs):
		"""
		Inicializa el formulario con valores predeterminados:
		- `fecha_desde` se establece en el 1 del mes y año actual.
		- `fecha_hasta` se establece en la fecha actual.
		"""
		super().__init__(*args, **kwargs)
		
		if "fecha_desde" not in self.initial:
			fecha_inicial = date(date.today().year, date.today().month, 1)
			self.fields["fecha_desde"].initial = fecha_inicial
			self.fields["fecha_desde"].widget.attrs["value"] = fecha_inicial
		if "fecha_hasta" not in self.initial:
			fecha_actual = date.today()
			self.fields["fecha_hasta"].initial = fecha_actual
			self.fields["fecha_hasta"].widget.attrs["value"] = fecha_actual
	
	def clean(self):
		cleaned_data = super().clean()
		
		codigo = cleaned_data.get("codigo")
		cai = cleaned_data.get("cai")
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		
		#-- Validaciones.
		if not codigo and not cai:
			self.add_error(None, "Debe indicar un Código de Producto o un CAI.")
		
		if not fecha_desde:
			self.add_error("fecha_desde", "Debe indicar una fecha válida.")
		
		if not fecha_hasta:
			self.add_error("fecha_hasta", "Debe indicar una fecha válida.")
		
		if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
			self.add_error("fecha_hasta", "La fecha hasta no puede ser anterior a la fecha desde.")
		
		return cleaned_data
	
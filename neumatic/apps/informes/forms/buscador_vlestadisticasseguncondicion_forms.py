# neumatic\apps\informes\forms\buscador_vlestadisticasseguncondicion_forms.py

from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclasstext, formclassdate, formclassselect, formclasscheck
from apps.maestros.models.sucursal_models import Sucursal
from entorno.constantes_base import AGRUPAR


class BuscadorEstadisticasSegunCondicionForm(InformesGenericForm):
	
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
	id_marca_desde = forms.IntegerField(
		min_value=0,
		required=True, 
		label="Desde Marca",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_marca_hasta = forms.IntegerField(
		min_value=0,
		required=True, 
		label="Hasta Marca",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	agrupar = forms.ChoiceField(
		choices=AGRUPAR,
		label="Agrupar por",
		required=True,
		widget=forms.Select(attrs={**formclassselect})
	)
	imprimir_importes = forms.BooleanField(
		label="Imprimir Importes",
		initial=True,
		required=False,
		widget=forms.CheckboxInput(attrs={**formclasscheck})
	)
	
	def __init__(self, *args, **kwargs):
		
		user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
		
		#-- Si la jerarquía del usuario es diferente a 'A' asiganar su sucural.
		if user and user.jerarquia != "A":
			#-- Fijar el campo sucursal del usuario.
			self.fields['sucursal'].initial = user.id_sucursal
			
			#-- Deshabilitar el combo Sucursal.
			self.fields['sucursal'].disabled = True
		
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
		
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		id_marca_desde = cleaned_data.get("id_marca_desde") or 0
		id_marca_hasta = cleaned_data.get("id_marca_hasta") or 0
		
		#-- Validaciones.
		if not fecha_desde:
			self.add_error("fecha_desde", "Debe indicar una fecha válida.")
		
		if not fecha_hasta:
			self.add_error("fecha_hasta", "Debe indicar una fecha válida.")
		
		if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
			self.add_error("fecha_hasta", "La fecha hasta no puede ser anterior a la fecha desde.")
		
		if id_marca_desde < 1:
			self.add_error("id_marca_desde", "Debe indicar un Código de Marca")
		
		if id_marca_hasta < 1:
			self.add_error("id_marca_hasta", "Debe indicar un Código de Marca")
		
		if id_marca_desde > id_marca_hasta:
			self.add_error("id_marca_hasta", "El Código de Marca hasta no puede ser menor al Código de Marca desde.")
		
		return cleaned_data
	
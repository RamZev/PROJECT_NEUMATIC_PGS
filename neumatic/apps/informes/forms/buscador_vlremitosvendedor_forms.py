# neumatic\apps\informes\forms\buscador_vlremitosvendedor_forms.py

from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassselect, formclassdate
from apps.maestros.models.vendedor_models import Vendedor


class BuscadorRemitosVendedorForm(InformesGenericForm):
	
	vendedor = forms.ModelChoiceField(
		queryset=Vendedor.objects.filter(estatus_vendedor=True),
		required=False,
		initial=0,
		label="Vendedor",
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
	
	def __init__(self, *args, **kwargs):
		#-- Se espera que la vista pase el usuario autenticado con la clave 'user'.
		self.user = kwargs.pop('user', None)
		self.allowed_groups = set(kwargs.pop('allowed_groups', None))
		self.user_groups = set(self.user.groups.values_list('name', flat=True))
		super().__init__(*args, **kwargs)
		
		#-- Si el usuario es vendedor (tiene un id_vendedor asociado).
		if self.user and getattr(self.user, 'id_vendedor', None) and not self.user.is_superuser and not self.user_groups.intersection(self.allowed_groups):
			#-- Fijar el campo vendedor al id del vendedor asociado.
			self.fields['vendedor'].initial = self.user.id_vendedor
			
			#-- Deshabilitar el combo Vendedor.
			self.fields['vendedor'].disabled = True
		
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
		
		vendedor = cleaned_data.get("vendedor", None)
		fecha_desde = cleaned_data.get("fecha_desde")
		fecha_hasta = cleaned_data.get("fecha_hasta")
		
		#-- Validar fechas.
		if not fecha_desde:
			self.add_error("fecha_desde", "Debe indicar una fecha válida.")
		
		if not fecha_hasta:
			self.add_error("fecha_hasta", "Debe indicar una fecha válida.")
		
		if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
			self.add_error("fecha_hasta", "La fecha hasta no puede ser anterior a la fecha desde.")
		
		if not vendedor:
			self.add_error("vendedor", "Debe seleccionar un Vendedor.")
		
		return cleaned_data

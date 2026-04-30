# neumatic\apps\informes\forms\buscador_vlestadisticasventasmarcavendedor_forms.py

from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassdate, formclassselect, formclasstext
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.vendedor_models import Vendedor
from apps.maestros.models.base_models import ProductoMarca


class BuscadorEstadisticasVentasMarcaVendedorForm(InformesGenericForm):
	
	sucursal = forms.ModelChoiceField(
		queryset=Sucursal.objects.filter(estatus_sucursal=True), 
		required=False,
		label="Sucursal",
		widget=forms.Select(attrs={**formclassselect})
	)
	marca = forms.ModelChoiceField(
		queryset=ProductoMarca.objects.filter(estatus_producto_marca=True), 
		required=True,
		label="Marca",
		widget=forms.Select(attrs={**formclassselect})
	)
	vendedor = forms.ModelChoiceField(
		queryset=Vendedor.objects.filter(estatus_vendedor=True), 
		required=True,
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
	comision = forms.DecimalField(
		min_value=0.0,
		max_value=100.0,
		required=False, 
		label="Comisión (%)",
		widget=forms.NumberInput(attrs={**formclasstext})
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
		comision = cleaned_data.get("comision") or 0.0
		
		#-- Validaciones.
		if not fecha_desde:
			self.add_error("fecha_desde", "Debe indicar una fecha válida.")
		
		if not fecha_hasta:
			self.add_error("fecha_hasta", "Debe indicar una fecha válida.")
		
		if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
			self.add_error("fecha_hasta", "La fecha hasta no puede ser anterior a la fecha desde.")
		
		if comision and comision < 0:
			self.add_error("comision", "La comisión no puede ser negativa.")
		
		if comision and comision > 100:
			self.add_error("comision", "La comisión no puede ser mayor a 100%.")
		
		return cleaned_data
	
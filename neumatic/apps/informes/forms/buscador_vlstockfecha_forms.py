# apps\informes\forms\buscador_vlstockfecha_forms.py
from django import forms
from datetime import date

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclasstext, formclassdate


class BuscadorStockFechaForm(InformesGenericForm):
	
	id_producto_desde = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Desde Código",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_producto_hasta = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Hasta Código",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	fecha = forms.DateField(
		required=True, 
		label="A Fecha",
		widget=forms.TextInput(attrs={'type':'date', **formclassdate})
	)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		if "fecha" not in self.initial:
			fecha_actual = date.today()
			self.fields["fecha"].initial = fecha_actual
			self.fields["fecha"].widget.attrs["value"] = fecha_actual
	
	def clean(self):
		cleaned_data = super().clean()
		
		id_producto_desde = cleaned_data.get('id_producto_desde') or 0
		id_producto_hasta = cleaned_data.get('id_producto_hasta') or 0
		fecha = cleaned_data.get("fecha")
		
		#-- Validaciones.
		if id_producto_desde and id_producto_desde < 1:
			self.add_error("id_producto_desde", "El valor no puede ser negativo")
		
		if id_producto_hasta and id_producto_hasta < 1:
			self.add_error("id_producto_hasta", "El valor no puede ser negativo")
		
		if id_producto_desde and id_producto_hasta and id_producto_desde > id_producto_hasta:
			self.add_error("id_producto_hasta", "El Código de Producto hasta no puede ser menor al Código de Producto desde.")
		
		if not fecha:
			self.add_error("fecha", "Debe indicar una fecha válida.")
		
		return cleaned_data
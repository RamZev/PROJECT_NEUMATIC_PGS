# neumatic\apps\informes\forms\buscador_vlpreciodiferente_forms.py

from django import forms
from decimal import Decimal
from datetime import date

from .informes_generics_forms import InformesGenericForm
from diseno_base.diseno_bootstrap import formclassdate, formclasstext, formclassselect, formclassnumb
from apps.maestros.models.base_models import ComprobanteVenta
from entorno.constantes_base import ORDEN_CHOICES


class BuscadorPrecioDiferenteForm(InformesGenericForm):
	
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
	id_vendedor_desde = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Desde Vendedor",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_vendedor_hasta = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Hasta Vendedor",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	dif_mayor = forms.DecimalField(
		min_value=0.0,
		required=False, 
		label="Dif. superiro a",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	orden = forms.ChoiceField(
		choices=ORDEN_CHOICES, 
		label="Ordenar por", 
		required=False,
		widget=forms.Select(attrs={**formclassselect})
	)
	comprobantes = forms.ModelMultipleChoiceField(
		queryset=ComprobanteVenta.objects.filter(estatus_comprobante_venta=True),
		label="Comprobantes",
		required=True,
		widget=forms.SelectMultiple(attrs={'size': 10, **formclassselect}),
		to_field_name='codigo_comprobante_venta'
	)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# Personalización de cómo se muestran las opciones en el combo (display).
		# self.fields['comprobantes'].label_from_instance = lambda obj: f"{obj.codigo_comprobante_venta} {obj.nombre_comprobante_venta}"
		# self.fields['comprobantes'].label_from_instance = lambda obj: (f"{obj.codigo_comprobante_venta.ljust(3)} {obj.nombre_comprobante_venta}")
		# self.fields['comprobantes'].label_from_instance = lambda obj: (f"{obj.codigo_comprobante_venta.ljust(5)}│ {obj.nombre_comprobante_venta}")
		
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
		id_vendedor_desde = cleaned_data.get("id_vendedor_desde") or 0
		id_vendedor_hasta = cleaned_data.get("id_vendedor_hasta") or 0
		dif_mayor = cleaned_data.get("dif_mayor") or 0
		
		if not fecha_desde:
			self.add_error("fecha_desde", "Debe indicar una fecha válida.")
		
		if not fecha_hasta:
			self.add_error("fecha_hasta", "Debe indicar una fecha válida.")
		
		if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
			self.add_error("fecha_hasta", "La fecha hasta no puede ser anterior a la fecha desde.")
		
		if id_vendedor_desde < 1:
			self.add_error("id_vendedor_desde", "Debe indicar un Código de Vendedor")
		
		if id_vendedor_hasta < 1:
			self.add_error("id_vendedor_hasta", "Debe indicar un Código de Vendedor")
		
		if id_vendedor_desde > id_vendedor_hasta:
			self.add_error("id_vendedor_hasta", "El Código de Vendedor hasta no puede ser menor al desde.")
		
		if dif_mayor < 0:
			self.add_error("dif_mayor", "El valor no puede ser negativo")
		
		return cleaned_data

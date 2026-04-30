# neumatic\apps\informes\forms\buscador_vlstockgeneralsucursal_forms.py
from django import forms

from .informes_generics_forms import InformesGenericForm
from apps.maestros.models.sucursal_models import Sucursal
from diseno_base.diseno_bootstrap import formclasstext


class BuscadorStockGeneralSucursalForm(InformesGenericForm):
	
	id_familia_desde = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Desde Familia",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_familia_hasta = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Hasta Familia",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_marca_desde = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Desde Marca",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_marca_hasta = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Hasta Marca",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_modelo_desde = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Desde Modelo",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	id_modelo_hasta = forms.IntegerField(
		min_value=0,
		required=False, 
		label="Hasta Modelo",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	sucursales = forms.ModelMultipleChoiceField(
		queryset=Sucursal.objects.filter(estatus_sucursal=True),
		widget=forms.CheckboxSelectMultiple(attrs={'class': 'd-done'}),
		required=True,
		label="Seleccione Sucursales a detallar"
	)
	
	def clean(self):
		cleaned_data = super().clean()
		
		id_familia_desde = cleaned_data.get('id_familia_desde') or 0
		id_familia_hasta = cleaned_data.get('id_familia_hasta') or 0
		id_marca_desde = cleaned_data.get('id_marca_desde') or 0
		id_marca_hasta = cleaned_data.get('id_marca_hasta') or 0
		id_modelo_desde = cleaned_data.get('id_modelo_desde') or 0
		id_modelo_hasta = cleaned_data.get('id_modelo_hasta') or 0
		sucursales = cleaned_data.get('sucursales') or []
		
		#-- Validaciones.
		if id_familia_desde and id_familia_desde < 1:
			self.add_error("id_familia_desde", "El valor no puede ser negativo")
		
		if id_familia_hasta and id_familia_hasta < 1:
			self.add_error("id_familia_hasta", "El valor no puede ser negativo")
		
		if id_familia_desde and id_familia_hasta and id_familia_desde > id_familia_hasta:
			self.add_error("id_familia_hasta", "El Código de Familia hasta no puede ser menor al Código de Familia desde.")
		
		if id_marca_desde and id_marca_desde < 1:
			self.add_error("id_marca_desde", "El valor no puede ser negativo")
		
		if id_marca_hasta and id_marca_hasta < 1:
			self.add_error("id_marca_hasta", "El valor no puede ser negativo")
		
		if id_marca_desde and id_marca_hasta and id_marca_desde > id_marca_hasta:
			self.add_error("id_marca_hasta", "El Código de Marca hasta no puede ser menor al Código de Marca desde.")
		
		if id_modelo_desde and id_modelo_desde < 1:
			self.add_error("id_modelo_desde", "El valor no puede ser negativo")
		
		if id_modelo_hasta and id_modelo_hasta < 1:
			self.add_error("id_modelo_hasta", "El valor no puede ser negativo")
		
		if id_modelo_desde and id_modelo_hasta and id_modelo_desde > id_modelo_hasta:
			self.add_error("id_modelo_hasta", "El Código de Modelo hasta no puede ser menor al Código de Modelo desde.")
		
		if len(sucursales) > 8:
			self.add_error("sucursales", f"Debe seleccionar un máximo de 8 sucursales. Ha seleccionado {len(sucursales)} sucursales.")
		
		return cleaned_data
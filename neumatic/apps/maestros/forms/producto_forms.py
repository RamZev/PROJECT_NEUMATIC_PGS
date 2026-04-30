# apps\maestros\forms\producto_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.producto_models import Producto
from diseno_base.diseno_bootstrap import (
	formclasstext,
	formclassselect,
	formclasscheck
)


class ProductoForm(CrudGenericForm):
	
	class Meta:
		model = Producto
		fields = '__all__'
		
		widgets = {
			'estatus_producto': 
				forms.Select(attrs={**formclassselect}),
			'codigo_producto': 
				forms.NumberInput(attrs={**formclasstext, 'readonly': True}),
			'tipo_producto': 
				forms.Select(attrs={**formclassselect}),
			'id_producto_estado': 
				forms.Select(attrs={**formclassselect}),
			'id_familia': 
				forms.Select(attrs={**formclassselect}),
			'id_marca': 
				forms.Select(attrs={**formclassselect}),
			'id_modelo': 
				forms.Select(attrs={**formclassselect}),
			'id_cai': 
				forms.Select(attrs={**formclassselect}),
			'medida': 
				forms.TextInput(attrs={**formclasstext}),
			'segmento': 
				forms.TextInput(attrs={**formclasstext}),
			'nombre_producto': 
				forms.TextInput(attrs={**formclasstext}),
			'unidad': 
				forms.NumberInput(attrs={**formclasstext, 'min': 0, 'max': 999}),
			'fecha_fabricacion': 
				forms.TextInput(attrs={**formclasstext}),
			'costo': 
				forms.NumberInput(attrs={**formclasstext, 'min':0.01, 'max': 9999999999999.99}),
			'id_alicuota_iva': 
				forms.Select(attrs={**formclassselect}),
			'precio': 
				forms.NumberInput(attrs={**formclasstext, 'min':0.01, 'max': 9999999999999.99}),
			'stock': 
				forms.NumberInput(attrs={**formclasstext, 'readonly': True}),
			'minimo': 
				forms.NumberInput(attrs={**formclasstext, 'min': 0, 'max': 99999}),
			'descuento': 
				forms.NumberInput(attrs={**formclasstext, 'min': 0.01, 'max': 99.99}),
			'despacho_1': 
				forms.TextInput(attrs={**formclasstext}),
			'despacho_2': 
				forms.TextInput(attrs={**formclasstext}),
			'descripcion_producto': 
				forms.TextInput(attrs={**formclasstext}),
			'carrito': 
				forms.CheckboxInput(attrs={**formclasscheck}),
			'iva_exento': 
				forms.CheckboxInput(attrs={**formclasscheck}),
			'obliga_operario': 
				forms.CheckboxInput(attrs={**formclasscheck}),
		}
	
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#-- Si se está editando un producto existente, deshabilitar el campo tipo_producto.
		if self.instance and self.instance.pk:
			self.fields['tipo_producto'].widget = forms.HiddenInput()
			self.fields['tipo_producto'].required = False  #-- Desactiva la validación.
			self.initial['tipo_producto'] = self.instance.tipo_producto  #-- Asegurar valor inicial.
	
	def clean(self):
		cleaned_data = super().clean()
		#-- Asignar automáticamente tipo_producto si el formulario está en modo edición.
		if self.instance.pk:
			cleaned_data['tipo_producto'] = self.instance.tipo_producto
			#-- Remover tipo_producto de la validación en modo edición.
			self._errors.pop('tipo_producto', None)
		return cleaned_data

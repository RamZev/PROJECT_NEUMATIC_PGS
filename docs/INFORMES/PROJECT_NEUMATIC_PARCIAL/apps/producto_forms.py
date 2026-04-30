# D:\PROJECT_NEUMATIC\neumatic\apps\maestros\models\producto_models.py
from django import forms
from ..models.producto_models import Producto
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect, formclassdate,)


class ProductoForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		#-- Agregar clases CSS a los campos con errores.
		for field in self.fields:
			if self[field].errors:
				self.fields[field].widget.attrs['class'] += ' border-danger is-invalid'
	
	class Meta:
		model = Producto
		fields = '__all__'

		widgets = {
			'estatus_producto': 
				forms.Select(attrs={**formclassselect}), 
			'codigo_producto': 
				forms.TextInput(attrs={**formclasstext,
										'placeholder': 'Cód. Producto}'}),
			'tipo_producto': 
				forms.TextInput(attrs={**formclasstext,
										'placeholder': 'Tipo Producto'}),
			'id_familia': 
				forms.Select(attrs={**formclassselect}), 
            'id_marca': 
				forms.Select(attrs={**formclassselect}), 
             'id_modelo': 
				forms.Select(attrs={**formclassselect}), 
			'cai': 
				forms.TextInput(attrs={**formclasstext,
										'placeholder': 'Cai'}),
			'medida': 
				forms.TextInput(attrs={**formclasstext,
										'placeholder': 'Medida'}),
			'segmento': 
				forms.TextInput(attrs={**formclasstext,
					                    'placeholder':'Segmento'}),
			'nombre_producto': 
				forms.TextInput(attrs={**formclasstext,
						                'placeholder':'Nombre Producto'}),			
			'unidad': 
				forms.NumberInput(attrs={**formclasstext}),	
			'fecha_fabricacion': 
				forms.TextInput(attrs={**formclassdate, 'type': 'date'}),	
			'costo': 
				forms.NumberInput(attrs={**formclasstext,
										'placeholder': 'Costo'}),
			'alicuota_iva': 
				forms.TextInput(attrs={**formclasstext,
										'placeholder': 'Tipo Venta'}),
			'precio': 
				forms.NumberInput(attrs={**formclasstext}),
			'stock': 
				forms.NumberInput(attrs={**formclasstext}),
            'minimo': 
				forms.NumberInput(attrs={**formclasstext}),
            'descuento': 
				forms.NumberInput(attrs={**formclasstext}),
			'despacho_1': 
				forms.TextInput(attrs={**formclasstext,
										'placeholder': 'Despacho 1'}),
			'despacho_2': 
				forms.TextInput(attrs={**formclasstext,
										'placeholder': 'Despacho 2'}),
			'descripcion_producto': 
				forms.TextInput(attrs={**formclasstext,
										'placeholder': 'Descripción'}),
			'carrito': 
				forms.CheckboxInput(attrs={**formclassselect}),
		}

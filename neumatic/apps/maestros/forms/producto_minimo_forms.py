# neumatic\apps\maestros\forms\producto_minimo_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import ProductoMinimo
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect
)


class ProductoMinimoForm(CrudGenericForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#-- Si se está editando un producto existente, deshabilitar el campo tipo_producto.
		if self.instance and self.instance.pk:
			self.fields['id_cai'].widget = forms.HiddenInput()
			self.fields['id_cai'].required = False  #-- Desactiva la validación.
			self.initial['id_cai'] = self.instance.id_cai  #-- Asegurar valor inicial.
			
			self.fields['id_deposito'].widget = forms.HiddenInput()
			self.fields['id_deposito'].required = False  #-- Desactiva la validación.
			self.initial['id_deposito'] = self.instance.id_deposito  #-- Asegurar valor inicial.
	
	def clean(self):
		cleaned_data = super().clean()
		#-- Asignar automáticamente tipo_producto si el formulario está en modo edición.
		if self.instance.pk:
			cleaned_data['id_cai'] = self.instance.id_cai
			cleaned_data['id_deposito'] = self.instance.id_deposito
			#-- Remover tipo_producto de la validación en modo edición.
			self._errors.pop('id_cai', None)
			self._errors.pop('id_deposito', None)
		return cleaned_data
	
	
	class Meta:
		model = ProductoMinimo
		fields = '__all__'
		
		widgets = {
			# 'id_cai': 
			# 	forms.Select(attrs={**formclassselect, 'readonly': True}),
			'id_cai': 
				forms.TextInput(attrs={**formclassselect, 'readonly': True}),
			'minimo': 
				forms.NumberInput(attrs={**formclasstext, 
							 	  'min': 1, 'max': 99}),
			'id_deposito': 
				forms.Select(attrs={**formclassselect, 'readonly': True}),
		}

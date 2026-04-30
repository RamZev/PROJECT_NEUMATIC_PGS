# neumatic\apps\maestros\forms\descuento_revendedor_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.descuento_vendedor_models import DescuentoRevendedor
from diseno_base.diseno_bootstrap import formclassselect, formclassnumb


class DescuentoRevendedorForm(CrudGenericForm):
	
	class Meta:
		model = DescuentoRevendedor
		fields = '__all__'
		
		widgets = {
			'estatus_descuento_revendedor': 
				forms.Select(attrs={**formclassselect}),
			'id_marca': 
				forms.Select(attrs={**formclassselect}),
			'id_familia': 
				forms.Select(attrs={**formclassselect}),
			'descuento': 
				forms.TextInput(attrs={**formclassnumb}),
		}
		
		error_messages = {
			'descuento': {
				'max_digits': 'El descuento debe estar entre 0.01 y 99.99',
				'max_decimal_places': 'El descuento debe tener máximo 2 decimales',
				'min_value': 'El descuento debe ser mayor o igual a 0.01',
				'max_value': 'El descuento debe ser menor o igual a 99.99',
				'invalid': 'Ingrese un número válido',
			}
		}
		
	def clean(self):
		cleaned_data = super().clean()
		id_marca = cleaned_data.get('id_marca')
		id_familia = cleaned_data.get('id_familia')
		
		if id_marca and id_familia:
			#-- Verificar si ya existe un registro con esta combinación.
			instance_pk = self.instance.pk if self.instance else None
			
			existe = DescuentoRevendedor.objects.filter(
				id_marca=id_marca,
				id_familia=id_familia
			).exclude(pk=instance_pk).exists()
			
			if existe:
				#-- Agregar error al formulario.
				self.add_error(
					'id_marca', 
					'Esta combinación de Marca y Familia ya existe.'
				)
				self.add_error(
					'id_familia', 
					'Esta combinación de Marca y Familia ya existe.'
				)
				# #-- También se puede agregar un error no asociado a campo.
				# raise forms.ValidationError(
				# 	'Ya existe una configuración de descuento para esta combinación de Marca y Familia.'
				# )
		
		return cleaned_data
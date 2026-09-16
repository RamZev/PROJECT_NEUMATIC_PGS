# neumatic\apps\maestros\forms\crud_forms_generics.py
from django import forms


class CrudGenericForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		#-- Extraer el usuario autenticado.
		self.user = kwargs.pop('user', None)
		#-- Extraer la bandera de modo solo lectura.
		self.is_view_only = kwargs.pop('is_view_only', False)
		super().__init__(*args, **kwargs)
		
		#-- Si es modo solo lectura, deshabilitar todos los campos.
		if self.is_view_only:
			for field_name in self.fields:
				field = self.fields[field_name]
				
				#-- Deshabilitar el widget.
				field.widget.attrs['disabled'] = True
				
				#-- Agregar clase visual de solo lectura.
				existing_class = field.widget.attrs.get('class', '')
				field.widget.attrs['class'] = f'{existing_class} bg-light'.strip()
				
				#-- Quitar 'required' para que no valide en modo consulta.
				field.required = False
	
	def full_clean(self):
		super().full_clean()
		#-- Agregar clases CSS a los campos con errores después de la validación.
		for field_name in self.fields:
			if self[field_name].errors:
				if 'class' not in self.fields[field_name].widget.attrs:
					self.fields[field_name].widget.attrs['class'] = ''
				self.fields[field_name].widget.attrs['class'] += ' border-danger is-invalid'
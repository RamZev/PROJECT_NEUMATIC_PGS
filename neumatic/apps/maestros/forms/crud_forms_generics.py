# neumatic\apps\maestros\forms\crud_forms_generics.py
from django import forms


class CrudGenericForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		#-- Extraer el usuario autenticado.
		self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)

	def full_clean(self):
		super().full_clean()
		#-- Agregar clases CSS a los campos con errores después de la validación.
		for field_name in self.fields:
			if self[field_name].errors:
				if 'class' not in self.fields[field_name].widget.attrs:
					self.fields[field_name].widget.attrs['class'] = ''
				self.fields[field_name].widget.attrs['class'] += ' border-danger is-invalid'

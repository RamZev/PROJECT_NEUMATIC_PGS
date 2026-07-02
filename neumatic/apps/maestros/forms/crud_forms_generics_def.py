# neumatic\apps\maestros\forms\crud_forms_generics.py
from django import forms


class CrudGenericForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		#-- Agregar clases CSS a los campos con errores.
		for field in self.fields:
			if self[field].errors:
				#-- Asegurar que existe la clase.
				if 'class' not in self.fields[field].widget.attrs:
					self.fields[field].widget.attrs['class'] = ''
				self.fields[field].widget.attrs['class'] += ' border-danger is-invalid'

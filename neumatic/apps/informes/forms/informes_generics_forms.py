# neumatic\apps\informes\forms\informes_generics_forms.py
from django import forms


class InformesGenericForm(forms.Form):
	
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
	
	def add_error_classes(self):
		"""Agrega clases CSS a los campos con errores."""
		for field_name, field in self.fields.items():
			widget = field.widget
			if field_name in self.errors:
				existing_classes = widget.attrs.get('class', '')
				widget.attrs['class'] = f"{existing_classes} border-danger is-invalid".strip()
		
		# #-- Agregar clases CSS a los campos con errores.
		# for field in self.fields:
		# 	if self[field].errors:
		# 		self.fields[field].widget.attrs['class'] += ' border-danger is-invalid'

# apps\datatools\forms\forms_generics.py
from django import forms


class GenericForm(forms.Form):
	...
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	
	# 	#-- Agregar clases CSS a los campos con errores.
	# 	for field in self.fields:
	# 		if self[field].errors:
	# 			self.fields[field].widget.attrs['class'] += ' border-danger is-invalid'

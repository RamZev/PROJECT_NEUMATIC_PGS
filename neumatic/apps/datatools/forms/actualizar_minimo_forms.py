# neumatic\apps\datatools\forms\actualizar_minimo_forms.py
from django import forms
from .forms_generics import GenericForm


class ActualizarMinimoForm(GenericForm):
	archivo_excel = forms.FileField(
		label="Seleccione el archivo Excel",
		help_text="El archivo debe tener las mismas columnas que el exportado previamente",
		widget=forms.FileInput(attrs={'accept': '.xlsx, .xls'}),
		error_messages = {
			'required': 'Debe seleccionar un archivo Excel.',
			'invalid': 'El archivo seleccionado no es válido.',
		}
	)

# neumatic/apps/datatools/forms/padron_santafe_forms.py
from django import forms

class PadronSantaFeUploadForm(forms.Form):
    archivo_csv = forms.FileField(
        label="Seleccione el archivo CSV del Padrón (Santa Fe)",
        help_text="El archivo debe estar en formato CSV delimitado por punto y coma (;).",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )
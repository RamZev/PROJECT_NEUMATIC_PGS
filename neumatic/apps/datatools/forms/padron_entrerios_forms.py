# neumatic/apps/datatools/forms/padron_entrerios_forms.py
from django import forms

class PadronEntreRiosUploadForm(forms.Form):
    archivo_csv = forms.FileField(
        label="Seleccione el archivo CSV del Padrón (Entre Ríos)",
        help_text="El archivo debe estar en formato CSV delimitado por punto y coma (;).",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )
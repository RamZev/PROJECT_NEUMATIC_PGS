# neumatic/apps/maestros/forms/modelo_vehiculo_forms.py
from django import forms

from .crud_forms_generics import CrudGenericForm
from ..models.vehiculo_models import ModeloVehiculo, MarcaVehiculo
from diseno_base.diseno_bootstrap import (
    formclasstext,
    formclassselect,
)


class ModeloVehiculoForm(CrudGenericForm):
    class Meta:
        model = ModeloVehiculo
        fields = '__all__'
        widgets = {
            'estatus_modelo_vehiculo': forms.Select(attrs={**formclassselect}),
            'id_marca_vehiculo': forms.Select(attrs={
                **formclassselect,
                'id': 'id_marca_vehiculo',
            }),
            'modelo_vehiculo': forms.TextInput(attrs={
                **formclasstext,
                'id': 'id_modelo_vehiculo',
                'list': 'datalist_modelos',           # ← vínculo con el datalist
                'autocomplete': 'off',
                'placeholder': 'Escriba o seleccione un modelo',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ─── Filtrar solo marcas activas ───
        self.fields['id_marca_vehiculo'].queryset = MarcaVehiculo.objects.filter(
            estatus_marca_vehiculo=True
        ).order_by('marca_vehiculo')

        # ─── Etiqueta del select vacío ───
        self.fields['id_marca_vehiculo'].empty_label = 'Seleccione una marca'

    def clean(self):
        cleaned_data = super().clean()

        marca = cleaned_data.get('id_marca_vehiculo')
        modelo = cleaned_data.get('modelo_vehiculo')

        # ─── Validación: modelo único por marca ───
        if marca and modelo:
            qs = ModeloVehiculo.objects.filter(
                id_marca_vehiculo=marca,
                modelo_vehiculo__iexact=modelo.strip()
            )
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                self.add_error(
                    'modelo_vehiculo',
                    f'Ya existe el modelo "{modelo}" para la marca "{marca.marca_vehiculo}".'
                )

        return cleaned_data
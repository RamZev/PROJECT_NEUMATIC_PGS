# neumatic/apps/maestros/forms/vehiculo_forms.py
from django import forms

from .crud_forms_generics import CrudGenericForm
from ..models.vehiculo_models import Vehiculo, MarcaVehiculo, ModeloVehiculo
from diseno_base.diseno_bootstrap import (
    formclasstext,
    formclassselect,
    formclassdate,
    formclassnumb,
)


class VehiculoForm(CrudGenericForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'
        widgets = {
            'estatus_vehiculo': forms.Select(attrs={**formclassselect}),
            'tipo_vehiculo': forms.Select(attrs={**formclassselect}),
            'id_marca_vehiculo': forms.Select(attrs={
                **formclassselect,
                'id': 'id_marca_vehiculo',
            }),
            'id_modelo_vehiculo': forms.Select(attrs={
                **formclassselect,
                'id': 'id_modelo_vehiculo',
            }),
            'segmento': forms.Select(attrs={**formclassselect}),
            'anio': forms.NumberInput(attrs={
                **formclassnumb,
                'min': 1900,
                'max': 2100,
                'step': 1,
            }),
            'patente': forms.TextInput(attrs={
                **formclasstext,
                'maxlength': 7,
                'style': 'text-transform: uppercase;',
            }),
            'kmxmes': forms.NumberInput(attrs={
                **formclassnumb,
                'min': 0,
                'step': 1,
            }),
            'visita': forms.TextInput(attrs={
                **formclassdate,
                'type': 'date',
            }),
            'exportado': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ─── Filtrar solo marcas activas ───
        self.fields['id_marca_vehiculo'].queryset = MarcaVehiculo.objects.filter(
            estatus_marca_vehiculo=True
        ).order_by('marca_vehiculo')
        self.fields['id_marca_vehiculo'].empty_label = 'Seleccione una marca'

        # ─── Cascada: filtrar modelos según la marca ───
        # Prioridad:
        #   1. Si el form tiene POST (is_bound) → usar el valor del POST.
        #   2. Si estamos editando (instance.pk) → usar la marca guardada.
        #   3. Si no → queryset vacío.
        marca_id = None

        if self.is_bound:
            marca_id = self.data.get('id_marca_vehiculo') or None
        elif self.instance and self.instance.pk:
            marca_id = self.instance.id_marca_vehiculo_id

        if marca_id:
            self.fields['id_modelo_vehiculo'].queryset = ModeloVehiculo.objects.filter(
                id_marca_vehiculo=marca_id,
                estatus_modelo_vehiculo=True
            ).order_by('modelo_vehiculo')
        else:
            self.fields['id_modelo_vehiculo'].queryset = ModeloVehiculo.objects.none()

        self.fields['id_modelo_vehiculo'].empty_label = 'Seleccione un modelo'
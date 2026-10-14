# neumatic/apps/maestros/forms/marca_vehiculo_forms.py
from django import forms

from .crud_forms_generics import CrudGenericForm
from ..models.vehiculo_models import MarcaVehiculo
from diseno_base.diseno_bootstrap import (
    formclasstext,
    formclassselect,
)


class MarcaVehiculoForm(CrudGenericForm):
    class Meta:
        model = MarcaVehiculo
        fields = '__all__'
        widgets = {
            'estatus_marca_vehiculo': forms.Select(attrs={**formclassselect}),
            'marca_vehiculo': forms.TextInput(attrs={**formclasstext}),
        }
# neumatic/apps/ventas/forms/servicio_vehiculo_forms.py
from django import forms
from django.forms import inlineformset_factory

from ..models.servicio_vehiculo_models import (
    ServicioVehiculo, DetalleServicioVehiculo
)
from apps.maestros.models.cliente_models import Cliente
from apps.maestros.models.vehiculo_models import Vehiculo
from apps.maestros.models.vendedor_models import Vendedor
from diseno_base.diseno_bootstrap import (
    formclasstext, formclassnumb, formclassselect,
    formclassdate, formclasscheck
)


class ServicioVehiculoForm(forms.ModelForm):
    """Formulario de cabecera. Cliente y Vehículo se manejan con Select2."""

    # Campos display (solo lectura) para mostrar la selección actual
    cliente_display = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'})
    )
    vehiculo_display = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'})
    )

    class Meta:
        model = ServicioVehiculo
        fields = '__all__'
        widgets = {
            'estatus_servicio_vehiculo': forms.Select(attrs={**formclassselect}),
            'id_cliente': forms.HiddenInput(),
            'id_vehiculo': forms.HiddenInput(),
            'kmxmes': forms.NumberInput(attrs={**formclassnumb, 'min': 0}),
            'proxima_visita': forms.TextInput(attrs={**formclassdate, 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={**formclasstext, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        # Querysets base (Select2 los reemplaza via AJAX)
        self.fields['id_cliente'].queryset = Cliente.objects.filter(
            estatus_cliente=True
        ).order_by('nombre_cliente')
        self.fields['id_vehiculo'].queryset = Vehiculo.objects.filter(
            estatus_vehiculo=True
        ).order_by('patente')

        # Poblar displays en modo edición
        if self.instance and self.instance.pk:
            if self.instance.id_cliente_id:
                c = self.instance.id_cliente
                self.fields['cliente_display'].initial = (
                    f"{c.id_cliente} - {c.nombre_cliente}"
                )
            if self.instance.id_vehiculo_id:
                v = self.instance.id_vehiculo
                marca = v.id_marca_vehiculo.marca_vehiculo if v.id_marca_vehiculo else ''
                modelo = v.id_modelo_vehiculo.modelo_vehiculo if v.id_modelo_vehiculo else ''
                self.fields['vehiculo_display'].initial = (
                    f"{v.patente or 'S/P'} - {marca} {modelo}".strip(' -')
                )


class DetalleServicioVehiculoForm(forms.ModelForm):
    """Formulario del detalle, usado por el inline formset."""
    class Meta:
        model = DetalleServicioVehiculo
        fields = '__all__'
        widgets = {
            'id_detalle_servicio_vehiculo': forms.HiddenInput(),
            'id_servicio_vehiculo': forms.HiddenInput(),
            'id_producto': forms.HiddenInput(),
            'cantidad': forms.NumberInput(attrs={
                **formclassnumb, 'min': 0.01, 'step': 0.01,
                'class': 'form-control form-control-sm border border-primary text-end'
            }),
            'id_vendedor': forms.HiddenInput(),
            'exportado': forms.CheckboxInput(attrs={**formclasscheck}),
        }


DetalleServicioVehiculoFormSet = inlineformset_factory(
    ServicioVehiculo,
    DetalleServicioVehiculo,
    form=DetalleServicioVehiculoForm,
    extra=0,
    can_delete=True
)
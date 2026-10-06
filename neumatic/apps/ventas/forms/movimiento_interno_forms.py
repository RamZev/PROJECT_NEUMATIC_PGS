# neumatic/apps/ventas/forms/movimiento_interno_forms.py
from django import forms
from django.forms import inlineformset_factory
from datetime import date


from apps.ventas.models.movimiento_interno_models import (
    MovimientoInterno,
    DetalleMovimientoInterno,
)
from ...maestros.models.base_models import ComprobanteVenta


class MovimientoInternoForm(forms.ModelForm):
    """
    Formulario del encabezado del Movimiento Interno.
    Solo se exponen los campos que el usuario debe completar.
    Sucursal, Punto de Venta, Comprobante, Número, Letra y Compro
    se asignan automáticamente en la vista.
    """

    class Meta:
        model = MovimientoInterno
        fields = [
            'id_deposito',
            'fecha_comprobante',
            'observa_comprobante',
            # Campos que el usuario no edita pero necesitamos que existan en el form
            'estatus_comprobante',
        ]
        widgets = {
            'estatus_comprobante': forms.Select(attrs={
                'class': 'form-select form-select-sm border border-primary'
            }),
            'id_deposito': forms.Select(attrs={
                'class': 'form-select form-select-sm border border-primary'
            }),
            'fecha_comprobante': forms.TextInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'type': 'date',
                'readonly': 'readonly',
            }),
            'observa_comprobante': forms.Textarea(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'rows': 2,
                'placeholder': 'Descripción / Motivo del movimiento (ej: CORRECCION)',
            }),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        # Fecha automática si es creación (sin instancia guardada)
        if not self.instance.pk:
            hoy = date.today()
            # Forzar el valor en el widget (más fuerte que initial)
            self.fields['fecha_comprobante'].widget.attrs['value'] = hoy.strftime('%Y-%m-%d')

        # Forzar readonly SIEMPRE
        self.fields['fecha_comprobante'].widget.attrs['readonly'] = True

        # Filtrar depósitos según la sucursal del usuario
        if usuario and usuario.id_sucursal:
            from ...maestros.models.base_models import ProductoDeposito
            self.fields['id_deposito'].queryset = ProductoDeposito.objects.filter(
                id_sucursal=usuario.id_sucursal,
                estatus_producto_deposito=True
            ).order_by('nombre_producto_deposito')
        else:
            from ...maestros.models.base_models import ProductoDeposito
            self.fields['id_deposito'].queryset = ProductoDeposito.objects.none()


class DetalleMovimientoInternoForm(forms.ModelForm):
    """
    Formulario de cada línea del detalle.
    Solo expone producto_venta (nombre visible) y cantidad.
    medida, marca y descripcion_producto se muestran por relación
    al producto en la plantilla (no son campos del form).
    """

    class Meta:
        model = DetalleMovimientoInterno
        fields = [
            'id_detalle_movimiento_interno',
            'id_movimiento_interno',
            'id_producto',
            'codigo',
            'producto_venta',
            'cantidad',
        ]
        widgets = {
            'id_detalle_movimiento_interno': forms.HiddenInput(),
            'id_movimiento_interno': forms.HiddenInput(),
            'id_producto': forms.HiddenInput(),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'readonly': 'readonly',
            }),
            'producto_venta': forms.TextInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'readonly': 'readonly',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary text-end',
                'step': '0.01',
            }),
        }


# Formset que vincula MovimientoInterno (padre) con DetalleMovimientoInterno (hijo)
DetalleMovimientoInternoFormSet = inlineformset_factory(
    MovimientoInterno,
    DetalleMovimientoInterno,
    form=DetalleMovimientoInternoForm,
    extra=0,
    can_delete=True,
)
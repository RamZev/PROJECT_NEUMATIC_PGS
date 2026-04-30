# neumatic\apps\ventas\forms\caja_detalle_forms.py
from django import forms
from django.core.exceptions import ValidationError

from diseno_base.diseno_bootstrap import (
    formclasstext, formclassselect, formclassdatetime, formclassradio)

from apps.maestros.forms.crud_forms_generics import CrudGenericForm
from ..models.caja_models import Caja, CajaDetalle


# En apps/maestros/forms/caja_detalle_forms.py

class CajaDetalleForm(CrudGenericForm):
    # Campos informativos de solo lectura
    estado_caja_info = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            **formclasstext,
            'readonly': 'readonly',
            'class': 'form-control-plaintext fw-bold'
        }),
        label="Estado de Caja"
    )
    
    sucursal_info = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            **formclasstext,
            'readonly': 'readonly'
        }),
        label="Sucursal"
    )
    
    numero_caja_info = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            **formclasstext,
            'readonly': 'readonly'
        }),
        label="Número de Caja"
    )
    
    # Campo para mostrar el número de caja (no es del modelo, solo informativo)
    caja_info = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            **formclasstext,
            'readonly': 'readonly',
            'placeholder': 'Número de caja'
        }),
        label="Caja"
    )

    class Meta:
        model = CajaDetalle
        fields = '__all__'

        widgets = {
            'id_caja': forms.HiddenInput(),
            'idventas': forms.NumberInput(attrs={
                **formclasstext,
                'placeholder': 'ID Venta (opcional)',
            }),
            'idcompras': forms.NumberInput(attrs={
                **formclasstext,
                'placeholder': 'ID Compra (opcional)',
            }),
            'idbancos': forms.NumberInput(attrs={
                **formclasstext,
                'placeholder': 'ID Banco (opcional)',
            }),
            'tipo_movimiento': forms.RadioSelect(attrs={**formclassradio}),
            'id_forma_pago': forms.Select(attrs={**formclassselect}),
            'importe': forms.NumberInput(attrs={
                **formclasstext,
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'observacion': forms.TextInput(attrs={
                **formclasstext,
                'placeholder': 'Observaciones del movimiento'
            }),
            'fecha': forms.DateTimeInput(attrs={
                **formclassdatetime,
                'type': 'datetime-local',
                'readonly': 'readonly'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Si es una instancia existente (modificación), deshabilitar campos
        if self.instance and self.instance.pk:
            for field_name in self.fields:
                if field_name not in ['estado_caja_info', 'sucursal_info', 'numero_caja_info', 'caja_info']:
                    self.fields[field_name].disabled = True
            
            # Mostrar información de la caja asociada
            if self.instance.id_caja:
                self.fields['caja_info'].initial = self.instance.id_caja.id_caja
                self.fields['sucursal_info'].initial = self.instance.id_caja.nombre_sucursal
                self.fields['numero_caja_info'].initial = self.instance.id_caja.numero_caja
        
        # Para creación: verificar si hay caja abierta
        else:
            if self.request and self.request.user:
                usuario = self.request.user
                caja_abierta = self._obtener_caja_abierta(usuario)
                
                if caja_abierta:
                    self.fields['estado_caja_info'].initial = "✅ Caja ABIERTA"
                    self.fields['estado_caja_info'].widget.attrs['class'] += ' text-success'
                    self.fields['sucursal_info'].initial = caja_abierta.nombre_sucursal
                    self.fields['numero_caja_info'].initial = caja_abierta.numero_caja
                    self.fields['caja_info'].initial = caja_abierta.id_caja
                    # Asignar la caja abierta al campo oculto
                    self.fields['id_caja'].initial = caja_abierta
                else:
                    self.fields['estado_caja_info'].initial = "❌ Caja CERRADA"
                    self.fields['estado_caja_info'].widget.attrs['class'] += ' text-danger'
                    # Deshabilitar todos los campos excepto los informativos
                    for field_name in self.fields:
                        if field_name not in ['estado_caja_info', 'sucursal_info', 'numero_caja_info', 'caja_info']:
                            self.fields[field_name].disabled = True
    
    def _obtener_caja_abierta(self, usuario):
        """Obtiene la última caja abierta para la sucursal del usuario"""
        if not usuario or not usuario.id_sucursal:
            return None
        
        try:
            caja_abierta = Caja.objects.filter(
                id_sucursal=usuario.id_sucursal,
                caja_cerrada=False,
                estatus_caja=True
            ).latest('fecha_caja')
            return caja_abierta
        except Caja.DoesNotExist:
            return None
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Solo validar para creación (no para modificación)
        if not self.instance.pk:
            # Validar que haya caja abierta
            usuario = self.request.user if self.request else None
            if usuario:
                caja_abierta = self._obtener_caja_abierta(usuario)
                if not caja_abierta:
                    raise ValidationError(
                        "No hay cajas abiertas en esta sucursal. No se pueden agregar movimientos."
                    )
                # Asignar automáticamente la caja abierta
                cleaned_data['id_caja'] = caja_abierta
            
            # Validar que el importe sea mayor a 0
            importe = cleaned_data.get('importe')
            if importe and importe <= 0:
                raise ValidationError({
                    'importe': 'El importe debe ser mayor a 0'
                })
        
        return cleaned_data
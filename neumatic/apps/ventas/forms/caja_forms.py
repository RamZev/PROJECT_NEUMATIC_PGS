# neumatic\apps\ventas\forms\caja_forms.py
from django import forms
from django.utils import timezone
from ..models.caja_models import Caja, CajaDetalle
from diseno_base.diseno_bootstrap import (
    formclasstext, formclassselect, formclassdate, formclassdatetime)


# En neumatic\apps\ventas\forms\caja_forms.py
class CajaForm(forms.ModelForm):
    
    # Campo de solo lectura para mostrar el nombre de la sucursal
    nombre_sucursal = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border border-secondary bg-light',
            'readonly': 'readonly',
            'placeholder': 'Sucursal del usuario'
        }),
        label="Sucursal")
    
    class Meta:
        model = Caja
        fields = '__all__'

        widgets = {
            'estatus_caja': 
                forms.Select(attrs={**formclassselect}),
            'numero_caja': 
                forms.NumberInput(attrs={
                    'class': 'form-control form-control-sm border border-secondary bg-light',
                    'readonly': 'readonly',
                    'placeholder': 'Se generará automáticamente'
                }),
            'fecha_caja': 
                forms.TextInput(attrs={
                    'class': 'form-control form-control-sm border border-secondary',
                    'type': 'date',
                }),
            'saldoanterior': 
                forms.NumberInput(attrs={**formclasstext, 'step': '0.01',
                'readonly': 'readonly'}),
            'ingresos': 
                forms.NumberInput(attrs={**formclasstext, 'step': '0.01',
                'readonly': 'readonly'}),
            'egresos': 
                forms.NumberInput(attrs={**formclasstext, 'step': '0.01',
                'readonly': 'readonly'}),
            'saldo': 
                forms.NumberInput(attrs={**formclasstext, 'step': '0.01',
                'readonly': 'readonly'}),
            'caja_cerrada': 
                forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recuento': 
                forms.NumberInput(attrs={**formclasstext, 'step': '0.01',
                                         'readonly': 'readonly',}),
            'diferencia': 
                forms.NumberInput(attrs={**formclasstext, 'step': '0.01',
                'readonly': 'readonly'}),
            'id_sucursal': forms.HiddenInput(),
            # 'hora_cierre': 
            #     forms.DateTimeInput(attrs={
            #         'class': 'form-control form-control-sm border border-secondary',
            #         'type': 'datetime-local',
            #         'readonly': 'readonly'
            #     }),
            'hora_cierre': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', 
                attrs={
                    'class': 'form-control form-control-sm border border-secondary',
                    'type': 'datetime-local',
                    'readonly': 'readonly'
                }
            ),
                
            'observacion_caja': 
                forms.TextInput(attrs={**formclasstext}),
            'id_usercierre': 
                forms.Select(attrs={**formclassselect}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hacer numero_caja no requerido en el formulario
        self.fields['numero_caja'].required = False
        
        # Obtener instancia
        instance = kwargs.get('instance')
        
        if instance and instance.pk:
            # PARA EDICIÓN
            if instance.id_sucursal:
                self.fields['nombre_sucursal'].initial = instance.id_sucursal.nombre_sucursal
            
            # Formatear fechas
            if instance.fecha_caja:
                self.fields['fecha_caja'].initial = instance.fecha_caja.strftime('%Y-%m-%d')
            
            if instance.hora_cierre:
                self.fields['hora_cierre'].initial = instance.hora_cierre.strftime('%Y-%m-%dT%H:%M')
            
            # Si la caja está CERRADA, bloquear todos los campos
            if instance.caja_cerrada:
                # Hacer TODOS los campos readonly
                for field_name, field in self.fields.items():
                    field.widget.attrs['readonly'] = True
                    field.widget.attrs['disabled'] = True
                    field.required = False
                
                # Reemplazar id_usercierre por texto de solo lectura
                usuario_texto = "No registrado"
                if instance.id_usercierre:
                    usuario_texto = f"{instance.id_usercierre.get_full_name() or instance.id_usercierre.username}"
                
                self.fields['id_usercierre'] = forms.CharField(
                    required=False,
                    initial=usuario_texto,
                    widget=forms.TextInput(attrs={
                        'class': 'form-control form-control-sm border border-secondary bg-light',
                        'readonly': 'readonly',
                    }),
                    label="Usuario que cerró"
                )
                
                # Reemplazar hora_cierre por texto de solo lectura
                hora_texto = "No registrada"
                if instance.hora_cierre:
                    hora_texto = instance.hora_cierre.strftime('%Y-%m-%d %H:%M')
                
                self.fields['hora_cierre'] = forms.CharField(
                    required=False,
                    initial=hora_texto,
                    widget=forms.TextInput(attrs={
                        'class': 'form-control form-control-sm border border-secondary bg-light',
                        'readonly': 'readonly',
                    }),
                    label="Fecha y hora de cierre"
                )
        else:
            # PARA CREACIÓN/APERTURA
            # caja_cerrada deshabilitada
            self.fields['caja_cerrada'].initial = False
            self.fields['caja_cerrada'].widget.attrs['disabled'] = True
            
            # id_usercierre oculto (no aplica para apertura)
            self.fields['id_usercierre'].widget = forms.HiddenInput()
            self.fields['id_usercierre'].required = False
    
    def clean(self):
        """Validaciones del formulario - NO calcula ingresos/egresos aquí"""
        cleaned_data = super().clean()
        # Los cálculos se hacen en la vista, no aquí
        return cleaned_data
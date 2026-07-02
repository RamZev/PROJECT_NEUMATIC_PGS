from django import forms
from django.db.models import Q 
from datetime import time

from .crud_forms_generics_def import CrudGenericForm
from ..models.valida_models import Valida
from ..models.cliente_models import Cliente
from diseno_base.diseno_bootstrap import(
    formclasstext,
    formclassselect,
    formclassdate
)


class ValidaForm(CrudGenericForm):
    # Campo temporal para Select2 (búsqueda de cliente) - NO se guarda en DB
    # cliente_busqueda = forms.CharField(
    #     label='Cliente',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'id': 'id_cliente_busqueda',
    #         'style': 'width: 100%;',
    #         'autocomplete': 'off'
    #     }),
    #     required=True,
    #     error_messages={
    #         'required': 'Debe seleccionar un cliente'
    #     }
    # )
    cliente_busqueda = forms.CharField(
        label='Cliente',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border border-primary mb-2',  # ← Cambio aquí
            'id': 'id_cliente_busqueda',
            'style': 'width: 100%;',
            'autocomplete': 'off'
        }),
        required=True,
        error_messages={
            'required': 'Debe seleccionar un cliente'
        }
    )
    
    class Meta:
        model = Valida
        fields = '__all__'
    
        widgets = {
            'estatus_valida': forms.Select(attrs={**formclassselect}), 
            'id_sucursal': forms.Select(attrs={**formclassselect}),
            'fecha_valida': forms.TextInput(attrs={**formclassdate, 'type': 'date', 'readonly': 'readonly'}),
            'hora_valida': forms.TimeInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            'solicitado': forms.TextInput(attrs={**formclasstext}),                
            'comentario': forms.TextInput(attrs={**formclasstext}),
            'id_cliente': forms.HiddenInput(),  # Campo oculto que SÍ se guarda en DB
            'id_comprobante_venta': forms.Select(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'width: 100%;',
            }),
            'numero_comprobante': forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            'hs': forms.TimeInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            'motivo': forms.Select(attrs={**formclassselect}),            
        }
    
    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Configurar formatos de hora
        self.fields['hora_valida'].input_formats = ['%H:%M']
        self.fields['hs'].input_formats = ['%H:%M']
        
        # Si es edición (registro existente), mostrar el cliente actual
        if self.instance and self.instance.pk and self.instance.id_cliente:
            cliente = self.instance.id_cliente
            # Mostrar en el campo visual
            self.fields['cliente_busqueda'].initial = f"{cliente.id_cliente} - {cliente.nombre_cliente}"
            # Guardar el ID en el campo oculto
            self.fields['id_cliente'].initial = cliente.id_cliente
        
        # No cargar todos los clientes (150k es demasiado)
        # Select2 usará AJAX para buscar
        self.fields['id_cliente'].queryset = Cliente.objects.none()
    
    def clean(self):
        """Validar que se haya seleccionado un cliente válido"""
        cleaned_data = super().clean()
        cliente_id = cleaned_data.get('id_cliente')
        
        if not cliente_id:
            self.add_error('cliente_busqueda', 'Debe seleccionar un cliente de la lista')
        
        return cleaned_data
    
    def clean_hora_valida(self):
        hora_valida = self.cleaned_data.get('hora_valida')
        if hora_valida:
            return time(hora_valida.hour, hora_valida.minute)
        return hora_valida
    
    def clean_hs(self):
        hs = self.cleaned_data.get('hs')
        if hs:
            return time(hs.hour, hs.minute)
        return hs
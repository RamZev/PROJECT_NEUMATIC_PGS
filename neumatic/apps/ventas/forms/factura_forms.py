# neumatic\apps\ventas\forms\factura_forms.py
from django import forms
from django.forms import inlineformset_factory
from datetime import date
from django.db.models import Q

from ..models.factura_models import *
from ...maestros.models.base_models import ComprobanteVenta

from diseno_base.diseno_bootstrap import (formclasstext, 
                                          formclassnumb,
                                          formclassnumb2,
                                          formclassselect, 
                                          formclassdate, 
                                          formclasscheck)


class FacturaForm(forms.ModelForm):
    buscar_cliente = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            **formclasstext, 'id': 'buscar_cliente', 
            'readonly': 'readonly'
            }
                               )
        )
    
    nombre_sucursal = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'})
    )
    punto_venta = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'})
    )   
    
    vendedor_factura = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'})
    )
    
    cliente_vip = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'})
    )
    
    tipo_venta = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'})
    )
    
    discrimina_iva = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'disabled': 'disabled'})
    )
    
    es_remito = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'readonly': 'readonly'})
    )
    
    es_pendiente = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'disabled': 'disabled'})
    )
    
    es_presupuesto = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'disabled': 'disabled'})
    )
    
    
    
    class Meta:
        model = Factura
        
        fields = "__all__"
        
        widgets = {
            "id_factura": forms.HiddenInput(),
            "id_valida": forms.HiddenInput(),
            "estatus_comprobante": forms.Select(attrs={**formclassselect}),
            "id_marketing_origen": forms.Select(attrs={**formclassselect}),
            "id_sucursal": forms.HiddenInput(),
            "id_punto_venta": forms.HiddenInput(),
            "jerarquia": forms.HiddenInput(),
            "id_deposito": forms.Select(attrs={**formclassselect}),
            "id_comprobante_venta": forms.Select(attrs={**formclassselect}),
            "compro": forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            "letra_comprobante": forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            "numero_comprobante": forms.TextInput(attrs={
                **formclasstext, 
                'readonly': 'readonly', 
                'type': 'number',
                'autocomplete':"off" ,
                'required': 'required',
                'step': 'any'}),
            
            "comprobante_remito": forms.Select(attrs={**formclassselect}),            
            "remito": forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            "fecha_comprobante": forms.TextInput(
                attrs={
                    **formclassdate,
                    'type': 'date', 
                    'readonly': 'readonly'
                }
            ),
            "cuit": forms.TextInput(attrs={**formclasstext, 'type': 'number', 'step': '1'}),  # Sin decimales
            "condicion_comprobante": forms.Select(attrs={**formclassselect}),
            "no_estadist": forms.CheckboxInput(attrs={**formclasscheck}),
            # "id_vendedor": forms.Select(attrs={**formclassselect}),
            "id_vendedor": forms.HiddenInput(),
            
            "id_cliente": forms.TextInput(attrs={**formclasstext, 'type': 'number', 'readonly': 'readonly'}),
            "cuit": forms.TextInput(attrs={**formclasstext, 'type': 'number', 'readonly': 'readonly'}),
            "nombre_factura": forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            "domicilio_factura": forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            "movil_factura": forms.TextInput(attrs={**formclasstext}),
            "id_comprobante_asociado": forms.HiddenInput(),
            "comprobante_asociado": forms.Select(attrs={**formclassselect}),    
            "numero_asociado": forms.TextInput(attrs={**formclasstext}),
            "email_factura": forms.TextInput(attrs={**formclasstext}),
            "observa_comprobante": forms.Textarea(attrs={
                **formclasstext,
                'rows': 3,  # Altura inicial
                'cols': 40,  # Ancho inicial
                'class': 'form-control',  # Clases adicionales
                'style': 'resize: vertical;'  # Permite redimensionar verticalmente
            }),
            "stock_clie": forms.CheckboxInput(attrs={**formclasscheck}),
            
            "gravado": forms.TextInput(attrs={**formclassnumb, 'readonly': 'readonly'}),
            "exento": forms.TextInput(attrs={**formclassnumb, 'readonly': 'readonly'}),
            "iva": forms.TextInput(attrs={**formclassnumb, 'readonly': 'readonly'}),
            "percep_ib": forms.TextInput(attrs={**formclassnumb, 'readonly': 'readonly'}),
            "total": forms.TextInput(attrs={**formclassnumb, 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)  # Pasar el usuario desde la vista
        tipo_comprobante = kwargs.pop('tipo_comprobante', None)
        super().__init__(*args, **kwargs)
        
        # Asignar valores iniciales para los campos personalizados
        if usuario:
            self.fields['nombre_sucursal'].initial = usuario.id_sucursal
            self.fields['punto_venta'].initial = usuario.id_punto_venta
            
            
        # Filtrar id_deposito según la sucursal del usuario
        if usuario and usuario.id_sucursal:
            self.fields['id_deposito'].queryset = ProductoDeposito.objects.filter(
                id_sucursal=usuario.id_sucursal
            )
        else:
            self.fields['id_deposito'].queryset = ProductoDeposito.objects.none()  # Sin opciones
        
        # Establecer la fecha actual si no se proporciona un valor inicial
        if not self.initial.get("fecha_comprobante"):
            self.initial["fecha_comprobante"] = date.today().isoformat()
        
        # ← Agregar aquí la lógica para modo edición:
        if self.instance and self.instance.id_cliente and self.instance.id_cliente.id_vendedor:
            self.fields['vendedor_factura'].initial = self.instance.id_cliente.id_vendedor.nombre_vendedor

        if self.instance and self.instance.id_cliente and self.instance.id_cliente.id_vendedor:
            self.fields['vendedor_factura'].initial = self.instance.id_cliente.id_vendedor.nombre_vendedor
            self.fields['tipo_venta'].initial = self.instance.id_cliente.id_vendedor.tipo_venta
        
        # Filtrar los comprobantes electrónicos y de remito
        # self.fields['id_comprobante_venta'].queryset = ComprobanteVenta.objects.filter(
        #     Q(electronica=True) | Q(remito=True)
        # )
        
        # Filtro completo para comprobantes
        if tipo_comprobante == 'electronico': 
            self.fields['id_comprobante_venta'].queryset = ComprobanteVenta.objects.filter(
                Q(electronica=True) | Q(remito=True),
                recibo=False,
                presupuesto=False,
                manual=False,
                estatus_comprobante_venta=True  # Solo comprobantes activos
            ).order_by('nombre_comprobante_venta')
        elif tipo_comprobante == 'manual':
            self.fields['id_comprobante_venta'].queryset = ComprobanteVenta.objects.filter(
                manual=True,
                recibo=False,
                estatus_comprobante_venta=True  # Solo comprobantes activos
            ).order_by('nombre_comprobante_venta')

            print("Tipo de comprobante: Manual***")
        elif tipo_comprobante == 'presupuesto':
            self.fields['id_comprobante_venta'].queryset = ComprobanteVenta.objects.filter(
                presupuesto=True,
                estatus_comprobante_venta=True  # Solo comprobantes activos
            ).order_by('nombre_comprobante_venta')
        elif tipo_comprobante == 'interno':
            self.fields['id_comprobante_venta'].queryset = ComprobanteVenta.objects.filter(
                interno=True,
                estatus_comprobante_venta=True  # Solo comprobantes activos
            ).order_by('nombre_comprobante_venta')

    def clean_discrimina_iva(self):
        # Siempre retorna True o False, incluso si el checkbox está deshabilitado
        return bool(self.data.get('discrimina_iva', False))    
       
class DetalleFacturaForm(forms.ModelForm):
    gravado = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        widget=forms.HiddenInput(),
    )

    no_gravado = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        widget=forms.HiddenInput(),
    )
    
    alic_iva = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        widget=forms.HiddenInput()
    )
    
    iva = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.HiddenInput(),
        initial=0.00  # Opcional: valor inicial
    )
    
    medida = forms.CharField(
        label="Medida", 
        required=False, 
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem; margin-left: 0px; margin-right: 0px;'
            })
    )
    
    class Meta:
        model = DetalleFactura
        
        fields = "__all__"
        
        widgets = {
            'id_detalle_factura': forms.HiddenInput(),
            'id_factura': forms.HiddenInput(),
            'id_producto': forms.HiddenInput(),
            
            'codigo': forms.TextInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem; margin-left: 0px; margin-right: 0px;'
                }),
            
            'producto_venta': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem; margin-left: 0px; margin-right: 0px;'
                }),
            
            'cantidad': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control form-control-sm border border-primary text-end', 
                'step': '1',
                'style': 'font-size: 0.8rem; padding: 0.25rem; margin-left: 0px; margin-right: 0px;'
                }),
            'reventa': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem; margin-left: 0px; margin-right: 0px;'
                }),
            'precio_lista': forms.HiddenInput(),
            'precio': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control form-control-sm border border-primary text-end', 
                'step': '0.1',
                'style': 'font-size: 0.8rem; padding: 0.25rem; margin-left: 0px; margin-right: 0px;'
                }),
            'descuento': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control form-control-sm border border-primary  text-end', 'step': '0.1',
                'style': 'font-size: 0.8rem; padding: 0.25rem; margin-left: 0px; margin-right: 0px;'
                }),
            'id_operario': forms.Select(attrs={
                'class': 'form-control form-control-sm border border-primary small-font',
                'style': 'font-size: 0.8rem; padding: 0.25rem; margin-left: 0px; margin-right: 0px;'
                }),
            #'gravado': forms.HiddenInput(),
            #'alic_iva': forms.HiddenInput(),
            #'iva': forms.HiddenInput(),
            'total': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control form-control-sm border border-primary text-end', 'step': '0.1',
                'style': 'font-size: 0.8rem; padding: 0.25rem; margin-left: 0px; margin-right: 0px;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.id_producto:
            self.fields['medida'].initial = self.instance.id_producto.medida
    

class SerialFacturaForm(forms.ModelForm):
    
    class Meta:
        model = SerialFactura
        fields = ['id_serial_factura', 'id_factura', 'producto_serial']
        widgets = {
            'id_serial_factura': forms.HiddenInput(),
            'id_factura': forms.HiddenInput(),
            'producto_serial': forms.TextInput(attrs={'class': 'form-control form-control-sm border border-secondary'}),
        }


# Se crea una instancia donde vincula  Factura (Padre) DetalleFactura (hijo)
# Donde el set de formularios esta vinculado a DetalleFacturaForm
# DetalleFactura y form=DetalleFacturaForm deben estar vinculados
DetalleFacturaFormSet = inlineformset_factory(Factura, DetalleFactura, form=DetalleFacturaForm, extra=0)
formset_detalle = DetalleFacturaFormSet(queryset=DetalleFactura.objects.none())

SerialFacturaFormSet = inlineformset_factory(Factura, SerialFactura, form=SerialFacturaForm, extra=0)
formset_serial = SerialFacturaFormSet(queryset=SerialFactura.objects.none())


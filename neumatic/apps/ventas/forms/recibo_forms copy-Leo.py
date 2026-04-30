# neumatic\apps\ventas\forms\recibo_forms.py
from django import forms
from django.forms import inlineformset_factory
from datetime import date
from django.db.models import Q
from django.forms import DecimalField, NumberInput

from ..models.factura_models import *
from ..models.recibo_models import (
    DetalleRecibo,
    RetencionRecibo,
    DepositoRecibo,
    TarjetaRecibo,
    ChequeRecibo
)
from ..models.factura_models import Factura
from apps.maestros.models.base_models import (CodigoRetencion,
                                              Banco,
                                              CuentaBanco, 
                                              ConceptoBanco,
                                              Tarjeta)

from diseno_base.diseno_bootstrap import (
    formclasstext, 
    formclassnumb2,
    formclassselect, 
    formclassdate, 
    formclasscheck
)

# Clase para normalizar valores a dos decimales
class FixedDecimalField(DecimalField):
    def to_python(self, value):
        value = super().to_python(value)
        if value is None:
            return value
        # Normalizar a dos decimales
        return round(value, 2)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({'step': '0.01'})  # Añadir step para compatibilidad
        return attrs


# Encabezado de Recibo
class FacturaReciboForm(forms.ModelForm):
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
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'readonly': 'readonly'})
    )
    
    es_remito = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'disabled': 'disabled'})
    )
    
    es_pendiente = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'disabled': 'disabled'})
    )
    
    es_presupuesto = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'disabled': 'disabled'})
    )
        
    # Campos calculados (no ligados al modelo)
    total_cobrado = forms.DecimalField(
        max_digits=15, decimal_places=2, required=False, initial=0.00,
        widget=forms.NumberInput(attrs={
            **formclassnumb2,
            'readonly': 'readonly',
            'style': 'font-size: 0.8rem; padding: 0.25rem; background-color: #E6F6FF;',
            'step': '0.01',
            'value': '0.00'  
        })
    )
    total_retenciones = forms.DecimalField(
        max_digits=15, decimal_places=2, required=False, initial=0.00,
        widget=forms.NumberInput(attrs={
            **formclassnumb2,
            'readonly': 'readonly',
            'style': 'font-size: 0.8rem; padding: 0.25rem; background-color: #E6F6FF;'
        })
    )
    total_depositos = forms.DecimalField(
        max_digits=15, decimal_places=2, required=False, initial=0.00,
        widget=forms.NumberInput(attrs={
            **formclassnumb2,
            'readonly': 'readonly',
            'style': 'font-size: 0.8rem; padding: 0.25rem; background-color: #E6F6FF;'
        })
    )
    total_tarjetas = forms.DecimalField(
        max_digits=15, decimal_places=2, required=False, initial=0.00,
        widget=forms.NumberInput(attrs={
            **formclassnumb2,
            'readonly': 'readonly',
            'style': 'font-size: 0.8rem; padding: 0.25rem; background-color: #E6F6FF;'
        })
    )
    total_cheques = forms.DecimalField(
        max_digits=15, decimal_places=2, required=False, initial=0.00,
        widget=forms.NumberInput(attrs={
            **formclassnumb2,
            'readonly': 'readonly',
            'style': 'font-size: 0.8rem; padding: 0.25rem; background-color: #E6F6FF;'
        })
    )
    total_formas_pago = forms.DecimalField(
        max_digits=15, decimal_places=2, required=False, initial=0.00,
        widget=forms.NumberInput(attrs={
            **formclassnumb2,
            'readonly': 'readonly',
            'style': 'font-size: 0.8rem; padding: 0.25rem; background-color: #E6F6FF;'
        })
    )
    resto_cobrar = forms.DecimalField(
        max_digits=15, decimal_places=2, required=False, initial=0.00,
        widget=forms.NumberInput(attrs={
            **formclassnumb2,
            'readonly': 'readonly',
            'style': 'font-size: 0.8rem; padding: 0.25rem; background-color: #E6F6FF;'
        })
    )
    

    class Meta:
        model = Factura
        fields = ['id_factura',
                  'id_valida',
                  'estatus_comprobante',
                  
                  "id_sucursal",
                  "id_punto_venta",
                  "jerarquia",
                  "id_deposito",
                  'id_comprobante_venta',

                  'id_cliente', 
                  'nombre_factura', 
                  'domicilio_factura',
                  'cuit', 

                  'fecha_comprobante',
                  'compro',
                  'letra_comprobante',
                  'numero_comprobante',
                  'comprobante_remito',
                  'remito',

                  'condicion_comprobante',
                  'no_estadist',
                  'id_vendedor',
                  'movil_factura',
                  'email_factura',
                  'stock_clie',
                  'total',
                  'efectivo_recibo']
        
        widgets = {
            'id_factura': forms.HiddenInput(),
            "id_valida": forms.HiddenInput(),
            "estatus_comprobante": forms.Select(attrs={**formclassselect}),

            "id_sucursal": forms.HiddenInput(),
            "id_punto_venta": forms.HiddenInput(),
            "jerarquia": forms.HiddenInput(),
            "id_deposito": forms.Select(attrs={**formclassselect}),
            "id_comprobante_venta": forms.Select(attrs={**formclassselect}),

            "id_cliente": forms.TextInput(attrs={**formclasstext, 'type': 'number', 'readonly': 'readonly'}),
            "cuit": forms.TextInput(attrs={**formclasstext, 'type': 'number', 'readonly': 'readonly'}),
            'nombre_factura': forms.TextInput(attrs={
                **formclasstext, 
                'readonly': 'readonly'
            }),
            "domicilio_factura": forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),

            "fecha_comprobante": forms.TextInput(attrs={**formclassdate, 'type': 'date'}),
            "compro": forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            "letra_comprobante": forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            "numero_comprobante": forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly', 'type': 'number', 'step': 'any'}),
            "comprobante_remito": forms.Select(attrs={**formclassselect}),            
            "remito": forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
            
            "condicion_comprobante": forms.Select(attrs={**formclassselect}),
            "no_estadist": forms.CheckboxInput(attrs={**formclasscheck}),
            "id_vendedor": forms.HiddenInput(),
            "movil_factura": forms.TextInput(attrs={**formclasstext}),
            "stock_clie": forms.CheckboxInput(attrs={**formclasscheck}),
            "email_factura": forms.TextInput(attrs={**formclasstext}),

            'total': forms.NumberInput(attrs={
                **formclassnumb2, 
            }),
            'efectivo_recibo': forms.NumberInput(attrs={
                **formclassnumb2, 
            }),
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)  # Pasar el usuario desde la vista
        # Validar que el usuario exista
        if not usuario:
            raise ValueError("Se requiere un usuario para crear o actualizar el recibo")

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            print(f"DEBUG: Modo Actualización")
        else:
            print(f"DEBUG: Modo Creación")

        # Asignar valores iniciales para los campos personalizados
        if usuario:
             self.fields['nombre_sucursal'].initial = usuario.id_sucursal
             self.fields['punto_venta'].initial = usuario.id_punto_venta
             print("Entró al init de la sucursal")
        else:
             print("No asignó nombre sucursal y nombre de punto de venta")
    
        
        if usuario and usuario.id_sucursal:
            print("entro al filtro de deposito")
            deposito_queryset = ProductoDeposito.objects.filter(
                id_sucursal=usuario.id_sucursal
            ).order_by('id_producto_deposito')
            self.fields['id_deposito'].queryset = deposito_queryset
            # Establecer el primer depósito como valor inicial
            if deposito_queryset.exists() and not self.initial.get('id_deposito'):
                self.initial['id_deposito'] = deposito_queryset.first().id_producto_deposito
        else:
            print("NO entro al filtro de deposito")
            self.fields['id_deposito'].queryset = ProductoDeposito.objects.none()

        
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
        self.fields['id_comprobante_venta'].queryset = ComprobanteVenta.objects.filter(
            Q(recibo=True)
        )

        # Inicializar valores calculados
        self.fields['total_cobrado'].initial = 0.00
        self.fields['total_retenciones'].initial = 0.00
        self.fields['total_depositos'].initial = 0.00
        self.fields['total_tarjetas'].initial = 0.00
        self.fields['total_cheques'].initial = 0.00
        self.fields['total_formas_pago'].initial = 0.00
        self.fields['resto_cobrar'].initial = 0.00
    
    def clean_discrimina_iva(self):
        # Siempre retorna True o False, incluso si el checkbox está deshabilitado
        return bool(self.data.get('discrimina_iva', False))

# Detalle del Recibo
class DetalleReciboForm(forms.ModelForm):
    # Campos no guardados en el modelo
    comprobante = forms.CharField(max_length=100, required=False, disabled=True,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control form-control-sm border border-primary small-font readonly-select',
                                     'readonly': 'readonly'
                                 }))
    letra_comprobante = forms.CharField(max_length=1, required=False, disabled=True,
                                       widget=forms.TextInput(attrs={
                                           'class': 'form-control form-control-sm border border-primary small-font readonly-select',
                                           'readonly': 'readonly'
                                       }))
    numero_comprobante = forms.CharField(max_length=10, required=False, disabled=True,  # Nuevo campo
                                        widget=forms.TextInput(attrs={
                                            'class': 'form-control form-control-sm border border-primary small-font readonly-select',
                                            'readonly': 'readonly'
                                        }))
    fecha_comprobante = forms.DateField(required=False, disabled=True,
                                       widget=forms.DateInput(attrs={
                                           'class': 'form-control form-control-sm border border-primary small-font readonly-select',
                                           'readonly': 'readonly'
                                       }))
    total = forms.DecimalField(max_digits=12, decimal_places=2, required=False, disabled=True,
                              widget=forms.NumberInput(attrs={
                                  'class': 'form-control form-control-sm border border-primary text-end small-font readonly-select',
                                  'readonly': 'readonly'
                              }))
    entrega = forms.DecimalField(max_digits=12, decimal_places=2, required=False, disabled=True,
                                widget=forms.NumberInput(attrs={
                                    'class': 'form-control form-control-sm border border-primary text-end small-font readonly-select',
                                    'readonly': 'readonly'
                                }))
    saldo = forms.DecimalField(max_digits=12, decimal_places=2, required=False, disabled=True,
                              widget=forms.NumberInput(attrs={
                                  'class': 'form-control form-control-sm border border-primary text-end small-font readonly-select',
                                  'readonly': 'readonly'
                              }))

    class Meta:
        model = DetalleRecibo
        fields = ['id_detalle_recibo', 'id_factura', 'id_factura_cobrada', 'monto_cobrado']
        widgets = {
            'id_detalle_recibo': forms.HiddenInput(),
            'id_factura': forms.HiddenInput(),
            'id_factura_cobrada': forms.HiddenInput(),
            'monto_cobrado': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary text-end', 
                'step': '0.01',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar campos derivados desde id_factura_cobrada
        if self.instance and self.instance.id_factura_cobrada:
            factura_cobrada = self.instance.id_factura_cobrada
            self.initial['comprobante'] = factura_cobrada.id_comprobante_venta.nombre_comprobante_venta
            self.initial['letra_comprobante'] = factura_cobrada.letra_comprobante
            self.initial['numero_comprobante'] = factura_cobrada.numero_comprobante
            self.initial['fecha_comprobante'] = factura_cobrada.fecha_comprobante  # Fecha como objeto date
            self.initial['total'] = factura_cobrada.total
            self.initial['entrega'] = factura_cobrada.entrega
            self.initial['saldo'] = factura_cobrada.total - factura_cobrada.entrega

# Formularios de Retenciones
class RetencionReciboInputForm(forms.ModelForm):
    # Campos con sufijo _input para la fila de inserción
    id_codigo_retencion_input = forms.ModelChoiceField(
        queryset=CodigoRetencion.objects.filter(estatus_cod_retencion=True).order_by('nombre_codigo_retencion'),
        empty_label="Seleccione Código Retención",
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False,
        label="Código de Retención"
    )
    certificado_input = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False,
        label="Certificado"
    )
    importe_retencion_input = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary text-end',
            'step': '0.01',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False,
        label="Importe"
    )
    fecha_retencion_input = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'type': 'date',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False,
        label="Fecha"
    )

    class Meta:
        model = RetencionRecibo
        fields = ['id_codigo_retencion', 'certificado', 'importe_retencion', 'fecha_retencion']


class RetencionReciboForm(RetencionReciboInputForm):
#class RetencionReciboForm(forms.ModelForm):
    # Esta clase se usa para el formset, usando los nombres originales
    id_codigo_retencion = forms.ModelChoiceField(
        queryset=CodigoRetencion.objects.filter(estatus_cod_retencion=True).order_by('nombre_codigo_retencion'),
        empty_label="Seleccione Código Retención",
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False,
    )
    certificado = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    importe_retencion = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary text-end',
            'step': '0.01',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    fecha_retencion = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border border-primary datetimepicker mb-2',
            'type': 'date',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )

    class Meta:
        model = RetencionRecibo
        fields = ['id_retencion_recibo', 'id_factura', 'id_codigo_retencion', 'certificado', 'importe_retencion', 'fecha_retencion']
        widgets = {
            'id_retencion_recibo': forms.HiddenInput(),
            'id_factura': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print("Aquí es!")
        queryset = CodigoRetencion.objects.filter(estatus_cod_retencion=True).order_by('nombre_codigo_retencion')
        #for obj in queryset:
        #    print(f"Objeto CodigoRetencion: {obj}, tipo: {type(obj)}, attrs: {dir(obj)}")
        self.fields['id_codigo_retencion'].queryset = queryset
        self.fields['id_codigo_retencion'].empty_label = "Seleccione Código Retención"
        self.fields['id_codigo_retencion'].required = True
        self.fields['certificado'].required = True
        self.fields['importe_retencion'].required = True
        self.fields['fecha_retencion'].required = True
        
        # Asegurar que fecha_retencion se inicialice correctamente
        # if self.instance and self.instance.fecha_retencion:
        #     self.initial['fecha_retencion'] = self.instance.fecha_retencion
        # else:
        #     self.initial['fecha_retencion'] = None  # O date.today() si deseas un valor predeterminado


# Formularios de Depósitos
class DepositoReciboInputForm(forms.ModelForm):
    id_cuenta_banco_input = forms.ModelChoiceField(
        queryset=CuentaBanco.objects.all().order_by('numero_cuenta'),
        label="Cuenta Banco",
        empty_label="Seleccione Cuenta Banco",
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False,
    )    
    id_concepto_banco_input = forms.ModelChoiceField(
        queryset=ConceptoBanco.objects.all().order_by('nombre_concepto_banco'),
        label="Concepto",
        empty_label="Seleccione Concepto",
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    fecha_deposito_input = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'type': 'date',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    importe_deposito_input = forms.DecimalField(
        label="Importe",
        max_digits=12, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary text-end',
            'step': '0.01',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    detalle_deposito_input = forms.CharField(
        label="Detalle",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )

    class Meta:
        model = DepositoRecibo
        fields = ['id_cuenta_banco_input', 'id_concepto_banco', 'fecha_deposito', 'importe_deposito', 'detalle_deposito']


class DepositoReciboForm(forms.ModelForm):
    class Meta:
        model = DepositoRecibo
        fields = ['id_deposito_recibo', 'id_factura',
                  'id_cuenta_banco', 'id_concepto_banco',
                  'fecha_deposito', 'importe_deposito',
                  'detalle_deposito']
        
        widgets = {
            'id_deposito_recibo': forms.HiddenInput(),
            'id_factura': forms.HiddenInput(),
            'DELETE': forms.CheckboxInput(attrs={'style': 'display: none;'}),
            'id_cuenta_banco': forms.Select(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'id_concepto_banco': forms.Select(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'fecha_deposito': forms.TextInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'type': 'date',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'importe_deposito': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary text-end', 
                'step': '0.01',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'detalle_deposito': forms.TextInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_cuenta_banco'].queryset = CuentaBanco.objects.all().order_by('numero_cuenta')
        self.fields['id_cuenta_banco'].empty_label = "Seleccione Cuenta"
        self.fields['id_cuenta_banco'].required = True
        self.fields['id_concepto_banco'].queryset = ConceptoBanco.objects.all().order_by('nombre_concepto_banco')
        self.fields['id_concepto_banco'].empty_label = "Seleccione Concepto"
        self.fields['id_concepto_banco'].required = True
        self.fields['fecha_deposito'].required = True
        self.fields['importe_deposito'].required = True
        self.fields['detalle_deposito'].required = False


# Formularios de Tarjetas
class TarjetaReciboInputForm(forms.ModelForm):
    id_tarjeta_input = forms.ModelChoiceField(
        queryset=Tarjeta.objects.filter(estatus_tarjeta=True).order_by('nombre_tarjeta'),
        label="Tarjeta",
        empty_label="Seleccione Tarjeta",
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    cupon_input = forms.IntegerField(
        label="Cupón",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    lote_input = forms.IntegerField(
        label="Lote",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    cuotas_input = forms.IntegerField(
        label="Cuotas",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    importe_tarjeta_input = forms.DecimalField(
        label="Importe",
        max_digits=12, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary text-end',
            'step': '0.01',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )

    class Meta:
        model = TarjetaRecibo
        fields = ['id_tarjeta', 'cupon', 'lote', 'cuotas', 'importe_tarjeta']


class TarjetaReciboForm(forms.ModelForm):
    class Meta:
        model = TarjetaRecibo
        fields = ['id_tarjeta_recibo', 'id_factura', 'id_tarjeta', 'cupon',
                 'lote', 'cuotas', 'importe_tarjeta']
        
        widgets = {
            'id_tarjeta_recibo': forms.HiddenInput(),
            'id_factura': forms.HiddenInput(),
            'DELETE': forms.CheckboxInput(attrs={'style': 'display: none;'}),
            'id_tarjeta': forms.Select(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'cupon': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'lote': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'cuotas': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'importe_tarjeta': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary text-end', 
                'step': '0.01',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_tarjeta'].queryset = Tarjeta.objects.filter(estatus_tarjeta=True).order_by('nombre_tarjeta')
        self.fields['id_tarjeta'].empty_label = "Seleccione Tarjeta"
        self.fields['id_tarjeta'].required = True
        self.fields['cupon'].required = True
        self.fields['lote'].required = True
        self.fields['cuotas'].required = True
        self.fields['importe_tarjeta'].required = True
        

# Formularios de Cheques
class ChequeReciboInputForm(forms.ModelForm):
    codigo_banco_input = forms.CharField(
        max_length=3,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;',
            'pattern': '[0-9]{1,3}',
            'title': 'Ingrese un código de banco de hasta 3 dígitos'
        }),
        required=False,
        label="Código Banco"
    )
    id_banco_input2 = forms.ModelChoiceField(
        queryset=Banco.objects.all().order_by('nombre_banco'),
        label="Banco",
        empty_label="Seleccione Banco",
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False,
    )
    sucursal_input = forms.IntegerField(
        label="Sucursal",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    codigo_postal_input = forms.IntegerField(
        label="Código Postal",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    numero_cheque_recibo_input = forms.IntegerField(
        label="Número",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    cuenta_cheque_recibo_input = forms.IntegerField(
        label="Cuenta",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    cuit_cheque_recibo_input = forms.IntegerField(
        label="CUIT",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )
    fecha_cheque1_input = forms.DateField(
        label="Fecha Ingreso",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;',
            'type': 'date'
        }),
        required=False
    )
    fecha_cheque2_input = forms.DateField(
        label="Fecha Cheque",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border border-primary',
            'style': 'font-size: 0.8rem; padding: 0.25rem;',
            'type': 'date'
        }),
        required=False
    )
    importe_cheque_input = forms.DecimalField(
        label="Importe",
        max_digits=12, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm border border-primary text-end',
            'step': '0.01',
            'style': 'font-size: 0.8rem; padding: 0.25rem;'
        }),
        required=False
    )

    class Meta:
        model = ChequeRecibo
        fields = ['id_banco', 'sucursal', 'codigo_postal', 'numero_cheque_recibo', 
                  'cuenta_cheque_recibo', 'cuit_cheque_recibo', 'fecha_cheque1', 
                  'fecha_cheque2', 'importe_cheque']

class ChequeReciboForm(forms.ModelForm):
    class Meta:
        model = ChequeRecibo
        fields = [
            'id_cheque_recibo', 'id_factura', 'codigo_banco', 'id_banco', 'sucursal',
            'codigo_postal', 'numero_cheque_recibo', 'cuenta_cheque_recibo',
            'cuit_cheque_recibo', 'fecha_cheque1', 'fecha_cheque2', 'importe_cheque'
        ]
        widgets = {
            'id_cheque_recibo': forms.HiddenInput(),
            'id_factura': forms.HiddenInput(),
            'DELETE': forms.CheckboxInput(attrs={'style': 'display: none;'}),
            'codigo_banco': forms.TextInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'id_banco': forms.Select(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'sucursal': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'codigo_postal': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'numero_cheque_recibo': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'cuenta_cheque_recibo': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'cuit_cheque_recibo': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
            'fecha_cheque1': forms.TextInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;',
                'type': 'date'
            }),
            'fecha_cheque2': forms.TextInput(attrs={
                'class': 'form-control form-control-sm border border-primary',
                'style': 'font-size: 0.8rem; padding: 0.25rem;',
                'type': 'date'
            }),
            'importe_cheque': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm border border-primary text-end',
                'step': '0.01',
                'style': 'font-size: 0.8rem; padding: 0.25rem;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_banco'].queryset = Banco.objects.all().order_by('nombre_banco')
        self.fields['id_banco'].empty_label = "Seleccione Banco"
        self.fields['id_banco'].required = True
        self.fields['sucursal'].required = True
        self.fields['codigo_postal'].required = True
        self.fields['numero_cheque_recibo'].required = True
        self.fields['cuenta_cheque_recibo'].required = True
        self.fields['cuit_cheque_recibo'].required = True
        self.fields['fecha_cheque1'].required = True
        self.fields['fecha_cheque2'].required = True
        self.fields['importe_cheque'].required = True



# Creamos los formsets para cada tipo de detalle
DetalleReciboFormSet = inlineformset_factory(
    Factura, 
    DetalleRecibo, 
    form=DetalleReciboForm, 
    extra=0,
    fk_name='id_factura',
)
formset_recibo = DetalleReciboFormSet(queryset=DetalleRecibo.objects.none())

RetencionReciboFormSet = inlineformset_factory(
    Factura, 
    RetencionRecibo, 
    form=RetencionReciboForm, 
    extra=0,
)
formset_retencion = RetencionReciboFormSet(queryset=RetencionRecibo.objects.none())

DepositoReciboFormSet = inlineformset_factory(
    Factura, 
    DepositoRecibo, 
    form=DepositoReciboForm, 
    extra=0,
)
formset_deposito = DepositoReciboFormSet(queryset=DepositoRecibo.objects.none())

TarjetaReciboFormSet = inlineformset_factory(
    Factura, 
    TarjetaRecibo, 
    form=TarjetaReciboForm, 
    extra=0,
)
formset_tarjeta = TarjetaReciboFormSet(queryset=TarjetaRecibo.objects.none())

ChequeReciboFormSet = inlineformset_factory(
    Factura, 
    ChequeRecibo, 
    form=ChequeReciboForm, 
    extra=0,
)
formset_cheque = ChequeReciboFormSet(queryset=ChequeRecibo.objects.none())
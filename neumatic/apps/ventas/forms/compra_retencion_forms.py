# neumatic\apps\ventas\forms\compra_retencion_forms.py
from django import forms
from datetime import date

from .forms_generics import GenericForm
from ..models.compra_models import Compra
from apps.maestros.models.base_models import ComprobanteCompra
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect, formclassdate)


class CompraRetencionForm(GenericForm):
	#-- Este campo es solo para visualización.
	numero_comprobante_formateado = forms.CharField(
		required=False,
		label="Número",
		widget=forms.TextInput(attrs={
			**formclasstext, 
			'readonly': 'readonly',
		})
	)
	
	class Meta:
		model = Compra
		fields = '__all__'
		
		widgets = {
			'estatus_comprabante': 
				forms.Select(attrs={**formclassselect}),
			'id_sucursal': 
				forms.Select(attrs={**formclassselect}),
			'id_punto_venta': 
				forms.Select(attrs={**formclassselect}),
			'id_deposito': 
				forms.Select(attrs={**formclassselect}),
			'id_comprobante_compra': 
				forms.Select(attrs={**formclassselect}),
			'compro': 
				forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
			'letra_comprobante': 
				forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'}),
			'numero_comprobante': forms.HiddenInput(),
			'fecha_comprobante': 
				forms.TextInput(attrs={**formclassdate, 'type':'date'}),
			'id_proveedor': 
				forms.Select(attrs={**formclassselect}),
			'id_provincia': 
				forms.Select(attrs={**formclassselect}),
			'condicion_comprobante': 
				forms.Select(attrs={**formclassselect}),
			'id_comprobante_venta': 
				forms.Select(attrs={**formclassselect}),
			'numero_comprobante_venta': 
				forms.NumberInput(attrs={**formclasstext, 'min': 1, 'max': 99999999}),
			'total_comprobante_venta': 
				forms.NumberInput(attrs={**formclasstext}),
			'fecha_registro': 
				forms.TextInput(attrs={**formclassdate, 'type':'date'}),
			'fecha_vencimiento': 
				forms.TextInput(attrs={**formclassdate, 'type':'date'}),
			'gravado': 
				forms.NumberInput(attrs={**formclasstext}),
			'no_gravado': 
				forms.NumberInput(attrs={**formclasstext}),
			'no_inscripto': 
				forms.NumberInput(attrs={**formclasstext}),
			'exento': 
				forms.NumberInput(attrs={**formclasstext}),
			'retencion_iva': 
				forms.NumberInput(attrs={**formclasstext}),
			'retencion_ganancia': 
				forms.NumberInput(attrs={**formclasstext}),
			'retencion_ingreso_bruto': 
				forms.NumberInput(attrs={**formclasstext, 'readonly': 'readonly'}),
			'sellado': 
				forms.NumberInput(attrs={**formclasstext}),
			'percepcion_iva': 
				forms.NumberInput(attrs={**formclasstext}),
			'percepcion_ingreso_bruto': 
				forms.NumberInput(attrs={**formclasstext}),
			'iva': 
				forms.NumberInput(attrs={**formclasstext}),
			'total': 
				forms.NumberInput(attrs={**formclasstext, 'readonly': 'readonly'}),
			'entrega': 
				forms.NumberInput(attrs={**formclasstext}),
			'alicuota_iva': 
				forms.NumberInput(attrs={**formclasstext, 'readonly': 'readonly'}),
			'documento_asociado': 
				forms.TextInput(attrs={**formclasstext}),
			'observa_comprobante': 
				forms.TextInput(attrs={**formclasstext}),
		}
		
		error_messages = {
			'codigo_comprobante_compra': {
				'unique': 'Este Código de Comprobante de Compra ya existe.',
				# 'required': 'Debe completar este campo.',
				# 'invalid': 'Ingrese un valor válido.'
			},
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		allowed_codes = ["IB", "RG", "RI"]
		base_queryset = ComprobanteCompra.objects.filter(codigo_comprobante_compra__in=allowed_codes)

		#-- Si es una instancia existente y su comprobante no está en la lista, incluirlo.
		if self.instance and self.instance.pk and self.instance.id_comprobante_compra:
			current_comprobante = self.instance.id_comprobante_compra
			if current_comprobante.codigo_comprobante_compra not in allowed_codes:
				base_queryset = ComprobanteCompra.objects.filter(
					pk=current_comprobante.pk
				) | base_queryset

		self.fields['id_comprobante_compra'].queryset = base_queryset

		#-- Asignar fecha de hoy a fecha_comprobante solo en creación.
		if not self.instance.pk:  #-- Es un registro nuevo.
			self.initial['fecha_comprobante'] = date.today()
			self.initial['fecha_registro'] = date.today()
			self.initial['fecha_vencimiento'] = date.today()
		
		#-- Si es una instancia existente, mostrar el valor formateado.
		if self.instance and self.instance.pk:
			self.initial['numero_comprobante_formateado'] = self.instance.numero_comprobante_formateado
		else:
			#-- Para nuevos registros, inicializar con valor vacío.
			self.initial['numero_comprobante_formateado'] = ''
			self.fields['numero_comprobante_formateado'].widget.attrs['placeholder'] = 'Se generará automáticamente'
	
	def clean(self):
		cleaned_data = super().clean()
		
		errors = {}
		
		if not cleaned_data.get('id_comprobante_compra'):
			errors['id_comprobante_compra'] = "El campo 'Comprobante' es obligatorio."
		
		if not cleaned_data.get('compro'):
			errors['compro'] = "El campo 'Compro' es obligatorio."
		
		if not cleaned_data.get('letra_comprobante'):
			errors['letra_comprobante'] = "El campo 'Letra' es obligatorio."
		
		if not cleaned_data.get('numero_comprobante'):
			errors['numero_comprobante'] = "El campo 'Número' es obligatorio."
			#-- Resaltar el campo formateado que es el visible.
			self.fields['numero_comprobante_formateado'].widget.attrs['class'] += ' border-danger is-invalid'
		
		numero_comprobante_venta = cleaned_data.get('numero_comprobante_venta') or 0
		if numero_comprobante_venta and numero_comprobante_venta < 1 or numero_comprobante_venta > 99999999:
			errors['numero_comprobante_venta'] = "El Número del Comprobante debe estar entre 1 y 99999999."
		
		if not cleaned_data.get('fecha_registro'):
			errors['fecha_registro'] = "El campo 'Fecha Registro' es obligatorio."
		
		
		if not cleaned_data.get('id_proveedor'):
			errors['id_proveedor'] = "El campo 'Proveedor' es obligatorio."
		
		
		if not cleaned_data.get('id_comprobante_venta'):
			errors['id_comprobante_venta'] = "El campo 'Comp. Compra' es obligatorio."
		
		if not cleaned_data.get('numero_comprobante_venta'):
			errors['numero_comprobante_venta'] = "El campo 'Número C/Compra' es obligatorio."
		
		if not cleaned_data.get('fecha_comprobante'):
			errors['fecha_comprobante'] = "El campo 'Fecha Emisión' es obligatorio."
		
		if cleaned_data.get('fecha_vencimiento') and cleaned_data.get('fecha_vencimiento') < cleaned_data.get('fecha_comprobante'):
			errors['fecha_vencimiento'] = "La fecha de vencimiento no puede ser anterior a la fecha de emisión."
		
		if errors:
			from django.core.exceptions import ValidationError
			raise ValidationError(errors)
		
		return cleaned_data
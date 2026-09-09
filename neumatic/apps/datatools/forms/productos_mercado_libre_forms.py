# neumatic\apps\datatools\forms\productos_mercado_libre_forms.py
from django import forms

from entorno.constantes_base import (
	TIPO_PRODUCTO_SERVICIO,
	FORMATOS_CHOICES,
	SEPARADOR_DECIMAL_CHOICES
)
from apps.maestros.models.base_models import (
	ProductoMarca,
	ProductoFamilia,
	ProductoModelo,
	ProductoEstado
)


class ExportarProductosForm(forms.Form):
	tipo_producto = forms.ChoiceField(
		choices=[('', 'Todos')] + TIPO_PRODUCTO_SERVICIO,
		required=False,
		widget=forms.Select(attrs={'class': 'form-select'})
	)
	marca = forms.ModelChoiceField(
		queryset=ProductoMarca.objects.filter(estatus_producto_marca=True).order_by('nombre_producto_marca'),
		required=False,
		empty_label="Todas las marcas",
		widget=forms.Select(attrs={'class': 'form-select'})
	)
	familia = forms.ModelChoiceField(
		queryset=ProductoFamilia.objects.filter(estatus_producto_familia=True).order_by('nombre_producto_familia'),
		required=False,
		empty_label="Todas las familias",
		widget=forms.Select(attrs={'class': 'form-select'})
	)
	modelo = forms.ModelChoiceField(
		queryset=ProductoModelo.objects.filter(estatus_modelo=True).order_by('nombre_modelo'),
		required=False,
		empty_label="Todos los modelos",
		widget=forms.Select(attrs={'class': 'form-select'})
	)
	medida = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medida'})
	)
	cai = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CAI'})
	)
	busqueda = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por nombre'})
	)
	solo_con_stock = forms.BooleanField(
		required=False,
		initial=False,
		widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
	)
	carrito = forms.ChoiceField(  # <--- NUEVO CAMPO (reemplaza solo_carrito)
		choices=[
			('', 'Todos'),
			('si', 'Sí'),
			('no', 'No'),
		],
		required=False,
		label='Carrito',
		widget=forms.Select(attrs={'class': 'form-select'})
	)
	accion = forms.ChoiceField(
		choices=[
			('', 'Seleccionar acción...'),
			('activar_carrito', 'Activar "Carrito"'),
			('desactivar_carrito', 'Desactivar "Carrito"'),
			('toggle_carrito', 'Invertir estado "Carrito"'),
		],
		required=False,
		widget=forms.Select(attrs={'class': 'form-select'})
	)


class ExportarProductosArchivoForm(forms.Form):
	"""Formulario para exportar productos a archivo"""
	
	estados = forms.ModelMultipleChoiceField(
		queryset=ProductoEstado.objects.filter(
			estatus_producto_estado=True
		).order_by('nombre_producto_estado'),
		widget=forms.CheckboxSelectMultiple(
			attrs={'class': 'form-check-input'}
		),
		required=True,
		label='Estados de producto'
	)
	
	formato = forms.ChoiceField(
		choices=FORMATOS_CHOICES,
		widget=forms.Select(attrs={'class': 'form-select'}),
		required=True,
		label='Exportar como'
	)
	
	separador_decimal = forms.ChoiceField(
		choices=SEPARADOR_DECIMAL_CHOICES,
		widget=forms.Select(attrs={'class': 'form-select'}),
		required=True,
		initial='punto',
		label='Separador decimal'
	)
	
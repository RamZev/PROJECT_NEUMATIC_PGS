# neumatic\apps\usuarios\forms\user_form.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

from apps.usuarios.models import User
from apps.maestros.models.base_models import PuntoVenta
from diseno_base.diseno_bootstrap import (
	formclasstext, formclassselect, formclasscheck)


class RegistroUsuarioForm(UserCreationForm):
	
	password1 = forms.CharField(
		label="Contraseña",
		widget=forms.PasswordInput(attrs={**formclasstext})
	)
	password2 = forms.CharField(
		label="Confirmar Contraseña",
		widget=forms.PasswordInput(attrs={**formclasstext})
	)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#-- Al crear, no mostrar ningún punto de venta hasta elegir sucursal.
		self.fields['id_punto_venta'].queryset = PuntoVenta.objects.none()
	
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'email_alt',
			'telefono',
			'is_active',
			'is_staff',
			'iniciales',
			'jerarquia',
			'id_vendedor',
			'id_sucursal',
			'id_punto_venta',
			'password1',
			'password2',
			'cambia_precio_descripcion',
		]
		
		widgets = {
			'username': 
				forms.TextInput(attrs={**formclasstext}),
			'first_name': 
				forms.TextInput(attrs={**formclasstext}),
			'last_name': 
				forms.TextInput(attrs={**formclasstext}),
			'email': 
				forms.EmailInput(attrs={**formclasstext}),
			'email_alt': 
				forms.TextInput(attrs={**formclasstext}),
			'telefono': 
				forms.TextInput(attrs={**formclasstext}),
			'is_active': 
				forms.CheckboxInput(attrs={**formclasscheck}),
			'is_staff': 
				forms.CheckboxInput(attrs={**formclasscheck}),
			'iniciales': 
				forms.TextInput(attrs={**formclasstext}),
			'jerarquia': 
				forms.Select(attrs={**formclassselect}),
			'id_punto_venta': 
				forms.Select(attrs={**formclassselect}),
			'id_vendedor': 
				forms.Select(attrs={**formclassselect}),
			'id_sucursal': 
				forms.Select(attrs={**formclassselect}),
			'cambia_precio_descripcion':
				forms.Select(attrs={**formclassselect}),
		}
	
	def clean(self):
		cleaned_data = super().clean()
		sucursal = cleaned_data.get('id_sucursal')
		punto_venta = cleaned_data.get('id_punto_venta')
		
		if sucursal and punto_venta:
			if punto_venta.id_sucursal_id != sucursal.id_sucursal:
				self.add_error(
					'id_punto_venta',
					'El punto de venta seleccionado no pertenece a la sucursal indicada.'
				)
		
		return cleaned_data


class EditarUsuarioForm(UserChangeForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		#-- Filtrar puntos de venta según la sucursal del usuario.
		if self.instance and self.instance.pk and self.instance.id_sucursal_id:
			self.fields['id_punto_venta'].queryset = PuntoVenta.objects.filter(
				id_sucursal_id=self.instance.id_sucursal_id,
				estatus_punto_venta=True
			).order_by('punto_venta')
		else:
			self.fields['id_punto_venta'].queryset = PuntoVenta.objects.none()
	
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'email_alt',
			'telefono',
			'is_active',
			'is_staff',
			'iniciales',
			'jerarquia',
			'id_vendedor',
			'id_sucursal',
			'id_punto_venta',
			'cambia_precio_descripcion',
		]
		
		widgets = {
			'username': 
				forms.TextInput(attrs={**formclasstext}),
			'first_name': 
				forms.TextInput(attrs={**formclasstext}),
			'last_name': 
				forms.TextInput(attrs={**formclasstext}),
			'email': 
				forms.TextInput(attrs={**formclasstext}),
			'email_alt': 
				forms.TextInput(attrs={**formclasstext}),
			'telefono': 
				forms.TextInput(attrs={**formclasstext}),
			'is_active': 
				forms.CheckboxInput(attrs={**formclasscheck}),
			'is_staff': 
				forms.CheckboxInput(attrs={**formclasscheck}),
			'iniciales': 
				forms.TextInput(attrs={**formclasstext}),
			'jerarquia': 
				forms.Select(attrs={**formclassselect}),
			'id_punto_venta': 
				forms.Select(attrs={**formclassselect}),
			'id_vendedor': 
				forms.Select(attrs={**formclassselect}),
			'id_sucursal': 
				forms.Select(attrs={**formclassselect}),
			'cambia_precio_descripcion':
				forms.Select(attrs={**formclassselect}),
		}
	
	def clean(self):
		cleaned_data = super().clean()
		sucursal = cleaned_data.get('id_sucursal')
		punto_venta = cleaned_data.get('id_punto_venta')
		
		if sucursal and punto_venta:
			if punto_venta.id_sucursal_id != sucursal.id_sucursal:
				self.add_error(
					'id_punto_venta',
					'El punto de venta seleccionado no pertenece a la sucursal indicada.'
				)
		
		return cleaned_data


class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = ["name"]

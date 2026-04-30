# neumatic\apps\usuarios\forms\user_form.py
from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

#from apps.usuarios.models.user_models import User
from apps.usuarios.models import User

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


class EditarUsuarioForm(UserChangeForm):
	
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
			'cambia_precio_descripcion':
				forms.Select(attrs={**formclassselect}),
		}


class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = ["name"]

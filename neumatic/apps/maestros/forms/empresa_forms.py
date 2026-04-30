# neumatic\apps\maestros\forms\empresa_forms.py
from django import forms
from PIL import Image
import os

from .crud_forms_generics import CrudGenericForm
from ..models.base_models import *
from ..models.empresa_models import Empresa
from diseno_base.diseno_bootstrap import (
	formclasstext,
	formclassselect,
	formclassdate,
)


class EmpresaForm(CrudGenericForm):
	#-- Campo para manejar la carga del logo.
	logo_file = forms.ImageField(
		required=False,
		label="Logo",
		help_text="Formatos permitidos: JPG, PNG, GIF. Tamaño máximo: 2MB",
		widget=forms.FileInput(attrs={
			# 'class': 'form-control',
			**formclasstext,
			'accept': 'image/*'
		})
	)
	
	#-- Campo oculto para indicar eliminación de logo
	eliminar_logo_flag = forms.BooleanField(
		required=False,
		widget=forms.HiddenInput(),
		initial=False
	)
	
	class Meta:
		model = Empresa
		fields ='__all__'
		
		widgets = {
			'estatus_empresa':
				forms.Select(attrs={**formclassselect}),
			'nombre_fiscal':
				forms.TextInput(attrs={**formclasstext}),
			'nombre_comercial':
				forms.TextInput(attrs={**formclasstext}),
			'domicilio_empresa':
				forms.TextInput(attrs={**formclasstext}),
			'codigo_postal':
				forms.TextInput(attrs={
					**formclasstext,
					'readonly': True
				}),
			'id_localidad':
				forms.Select(attrs={**formclassselect}),
			'id_provincia':
				forms.Select(attrs={**formclassselect}),
			'id_iva':
				forms.Select(attrs={**formclassselect}),
			'cuit':
				forms.TextInput(attrs={**formclasstext}),
			'ingresos_bruto':
				forms.TextInput(attrs={**formclasstext}),
			'inicio_actividad': 
				forms.TextInput(attrs={
					**formclassdate,
					'type':
					'date'
				}),
			'cbu':
				forms.TextInput(attrs={**formclasstext}),
			'cbu_alias':
				forms.TextInput(attrs={**formclasstext}),
			'cbu_vence': 
				forms.TextInput(attrs={
					**formclassdate,
					'type':
					'date'
				}),
			'telefono':
				forms.TextInput(attrs={**formclasstext}),
			'email_empresa':
				forms.EmailInput(attrs={**formclasstext}),
			'web_empresa':
				forms.TextInput(attrs={**formclasstext}),
			
			'logo_empresa':
				forms.HiddenInput(),
							
			'ws_archivo_crt2':
				forms.Textarea(attrs={
					**formclasstext,
					'rows': 5,
					'readonly': True
				}),
			'ws_archivo_key2':
				forms.Textarea(attrs={
					**formclasstext,
					'rows': 5,
					'readonly': True
				}),
			'ws_vence_h':
				forms.TextInput(attrs={
					**formclasstext, 
					'readonly': True,
					'style': 'background-color: #d4eaff;'
				}),
			
			'ws_archivo_crt_p':
				forms.Textarea(attrs={
					**formclasstext,
					'rows': 5,
					'readonly': True
				}),
			'ws_archivo_key_p':
				forms.Textarea(attrs={
					**formclasstext,
					'rows': 5,
					'readonly': True
				}),
			'ws_vence_p':
				forms.TextInput(attrs={
					**formclasstext, 
					'readonly': True,
					'style': 'background-color: #d4eaff;'
				}),
			
			'ws_token_h':
				forms.Textarea(attrs={
					**formclasstext,
					'rows': 3,
					'readonly': True
				}),
			'ws_sign_h':
				forms.Textarea(attrs={
					**formclasstext,
					'rows': 3,
					'readonly': True
				}),
			'ws_expiracion_h':
				forms.TextInput(attrs={
					**formclasstext, 
					'readonly': True,
					'style': 'background-color: #d4eaff;'
				}),
			
			'ws_token_p':
				forms.Textarea(attrs={
					**formclasstext,
					'rows': 3,
					'readonly': True
				}),
			'ws_sign_p':
				forms.Textarea(attrs={
					**formclasstext,
					'rows': 3,
					'readonly': True
				}),
			'ws_expiracion_p':
				forms.TextInput(attrs={
					**formclasstext, 
					'readonly': True,
					'style': 'background-color: #d4eaff;'
				}),
			
			'ws_modo':
				forms.Select(attrs={**formclassselect}),
			'interes':
				forms.NumberInput(attrs={
					**formclasstext,
					'min': -99.99,
					'max': 99.99
				}),
			'interes_dolar':
				forms.NumberInput(attrs={
					**formclasstext,
					'min': -99.99,
					'max': 99.99
				}),
			'cotizacion_dolar':
				forms.NumberInput(attrs={
					**formclasstext,
					'min': 0,
					'max': 9999999999999.99
				}),
			'dias_vencimiento':
				forms.NumberInput(attrs={
					**formclasstext,
					'min': 0,
					'max': 999
				}),
			'descuento_maximo':
				forms.NumberInput(attrs={
					**formclasstext,
					'min': -99.99,
					'max': 99.99
				}),
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		#-- Formatear fechas para datetime-local si existen.
		if self.instance and self.instance.pk:
			if self.instance.ws_vence_h:
				self.initial['ws_vence_h'] = self.instance.ws_vence_h.strftime('%d/%m/%Y %H:%M:%S')
			if self.instance.ws_vence_p:
				self.initial['ws_vence_p'] = self.instance.ws_vence_p.strftime('%d/%m/%Y %H:%M:%S')
			if self.instance.ws_expiracion_h:
				self.initial['ws_expiracion_h'] = self.instance.ws_expiracion_h.strftime('%d/%m/%Y %H:%M:%S')
			if self.instance.ws_expiracion_p:
				self.initial['ws_expiracion_p'] = self.instance.ws_expiracion_p.strftime('%d/%m/%Y %H:%M:%S')
		
		self.fields['id_localidad'].choices = []
		
		#-- Verificar si el formulario se llama con datos (POST).
		if self.is_bound:
			#-- Obtener el valor enviado de id_provincia_tarjeta.
			provincia_id = self.data.get('id_provincia')
			localidad_id = self.data.get('id_localidad', '')
			
			if provincia_id:
				#-- Filtrar localidades según la provincia enviada.
				localidades = Localidad.objects.filter(id_provincia=provincia_id).order_by('nombre_localidad')
				self.fields['id_localidad'].choices = [("", "Seleccione una localidad")] + [
					(loc.id_localidad, f"{loc.nombre_localidad} - {loc.codigo_postal}") for loc in localidades
				]
				self.initial['id_localidad'] = localidad_id
			else:
				self.fields['id_localidad'].choices = [("", "Seleccione una localidad")]
			
		#-- Si se está editando un registro existente.
		elif self.instance and self.instance.pk and self.instance.id_provincia:
			localidades = Localidad.objects.filter(id_provincia=self.instance.id_provincia).order_by('nombre_localidad')
			self.fields['id_localidad'].choices = [
				(loc.id_localidad, f"{loc.nombre_localidad} - {loc.codigo_postal}")
				for loc in localidades
			]
			
			#-- Establecer localidad seleccionada inicialmente.
			if self.instance.id_localidad:
				self.initial['id_localidad'] = self.instance.id_localidad.id_localidad
		
		#-- Asegurar que exista una opción inicial en cualquier caso.
		self.fields['id_localidad'].choices.insert(0, ("", "Seleccione una localidad"))
		
		#-- Si hay un logo guardado, mostrar información.
		if self.instance and self.instance.pk and self.instance.logo_empresa:
			self.fields['logo_file'].help_text = "Logo actual cargado. Seleccione uno nuevo para reemplazarlo."
			
			#-- También podemos agregar un atributo data para el nombre del archivo actual.
			self.fields['logo_file'].widget.attrs['data-current-file'] = os.path.basename(self.instance.logo_empresa.name)
	
	def clean_logo_file(self):
		"""Validar y procesar el archivo de logo"""
		logo = self.cleaned_data.get('logo_file')
		
		if logo:
			#-- Validar tipo de archivo.
			if not logo.content_type.startswith('image/'):
				raise forms.ValidationError('El archivo debe ser una imagen.')
			
			#-- Validar tamaño máximo (por ejemplo, 2MB).
			if logo.size > 2 * 1024 * 1024:
				raise forms.ValidationError('La imagen no debe exceder los 2MB.')
			
			#-- Validar formato (opcional, usando PIL)
			try:
				img = Image.open(logo)
				img.verify()  #-- Verificar que es una imagen válida.
			except Exception:
				raise forms.ValidationError('El archivo no es una imagen válida.')
		
		return logo
	
	def clean(self):
		"""Validación general del formulario"""
		cleaned_data = super().clean()
		
		#-- Si se marcó eliminar_logo, establecer logo_empresa como None.
		if cleaned_data.get('eliminar_logo_flag'):
			cleaned_data['logo_empresa'] = None
		
		return cleaned_data
	
	def save(self, commit=True):
		"""Sobrescribir save para manejar el logo"""
		instance = super().save(commit=False)
		
		#-- Procesar el logo si se subió uno nuevo.
		logo_data = self.cleaned_data.get('logo_file')
		if logo_data is not None:
			#-- Si hay un logo existente, eliminarlo antes de guardar el nuevo.
			if instance.pk and instance.logo_empresa:
				old_logo_path = instance.logo_empresa.path
				if os.path.isfile(old_logo_path):
					os.remove(old_logo_path)
			instance.logo_empresa = logo_data
		
		elif self.cleaned_data.get('eliminar_logo_flag'):
			#-- Si se solicitó eliminar el logo.
			if instance.logo_empresa:
				#-- Eliminar el archivo físico.
				logo_path = instance.logo_empresa.path
				if os.path.isfile(logo_path):
					os.remove(logo_path)
			instance.logo_empresa = None
		
		if commit:
			instance.save()
			self.save_m2m()
		
		return instance

# neumatic\apps\maestros\forms\sucursal_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import *
from ..models.sucursal_models import Sucursal
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect,
	formclassdate
)


class SucursalForm(CrudGenericForm):
	
	class Meta:
		model = Sucursal
		fields = '__all__'
		
		widgets = {
			'estatus_sucursal':
				forms.Select(attrs={**formclassselect}),
			'nombre_sucursal':
				forms.TextInput(attrs={**formclasstext}),
			'codigo_michelin':
				forms.NumberInput(attrs={**formclasstext,
							 'min':1, 'max': 99999}),
			'domicilio_sucursal':
				forms.TextInput(attrs={**formclasstext}),
			'codigo_postal': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'id_provincia':
				forms.Select(attrs={**formclassselect}),
   			'id_localidad':
				forms.Select(attrs={**formclassselect}),
			'telefono_sucursal':
				forms.TextInput(attrs={**formclasstext}),
			'email_sucursal':
				forms.EmailInput(attrs={**formclasstext}),
			'inicio_actividad':
				forms.TextInput(attrs={**formclassdate,
										 'type': 'date'}),
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.fields['id_localidad'].choices = []
		
		#-- Verificar si el formulario se llama con datos (POST).
		if self.is_bound:
			#-- Obtener el valor enviado de id_provincia y id_localidad.
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

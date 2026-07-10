# neumatic\apps\maestros\forms\cliente_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import *
from ..models.cliente_models import Cliente
from diseno_base.diseno_bootstrap import(
	formclasstext,
	formclassselect,
	formclassdate,
	formclassnumb
)


class ClienteForm(CrudGenericForm):
		
	class Meta:
		model = Cliente
		fields ='__all__'
		
		widgets = {
			'estatus_cliente': 
				forms.Select(attrs={**formclassselect}),
			'nombre_cliente': 
				forms.TextInput(attrs={**formclasstext}),
			'domicilio_cliente': 
				forms.TextInput(attrs={**formclasstext}),
			'codigo_postal': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'id_provincia': 
				forms.Select(attrs={**formclassselect}),
			'id_localidad': 
				forms.Select(attrs={**formclassselect}),
			'tipo_persona': 
				forms.Select(attrs={**formclassselect}),
			'id_tipo_iva': 
				forms.Select(attrs={**formclassselect}),
			'id_tipo_documento_identidad': 
				forms.Select(attrs={**formclassselect}),
			'cuit': 
				forms.TextInput(attrs={**formclasstext}),
			'condicion_venta': 
				forms.Select(attrs={**formclassselect}),
			'telefono_cliente': 
				forms.TextInput(attrs={**formclasstext}),
			'fax_cliente': 
				forms.TextInput(attrs={**formclasstext}),
			'movil_cliente': 
				forms.TextInput(attrs={**formclasstext}),
			'email_cliente': 
				forms.TextInput(attrs={**formclasstext}),
			'email2_cliente': 
				forms.TextInput(attrs={**formclasstext}),
			'transporte_cliente': 
				forms.TextInput(attrs={**formclasstext}),
			'id_vendedor': 
				forms.Select(attrs={**formclassselect}),
			'fecha_nacimiento': 
				forms.TextInput(attrs={'type':'date', **formclassdate}),
			'fecha_alta': 
				forms.TextInput(attrs={'type':'date', **formclassdate, 'readonly': True}),
   			'sexo': 
				forms.Select(attrs={**formclassselect}),
			'id_actividad': 
				forms.Select(attrs={**formclassselect}),
			'id_sucursal': 
				forms.Select(attrs={**formclassselect}),
			'id_percepcion_ib':
				forms.Select(attrs={**formclassselect}),
			'numero_ib': 
				forms.TextInput(attrs={**formclasstext}),
			'transporte_cliente': 
				forms.TextInput(attrs={**formclasstext}),
			'vip': 
				forms.Select(attrs={**formclassselect}),
			'mayorista': 
				forms.Select(attrs={**formclassselect}),
			'sub_cuenta': 
				forms.TextInput(attrs={**formclasstext}),
   			'observaciones_cliente': 
				forms.TextInput(attrs={**formclasstext}),
			'black_list': 
				forms.Select(attrs={**formclassselect}),
			'black_list_motivo': 
				forms.TextInput(attrs={**formclasstext}),
			'black_list_usuario': 
				forms.TextInput(attrs={**formclasstext, 'readonly': True}),
			'fecha_baja': 
				forms.TextInput(attrs={'type':'date', **formclassdate, 'readonly': True}),
			'cliente_empresa': 
				forms.Select(attrs={**formclassselect}),
			'limite_credito':
				forms.TextInput(attrs={**formclassnumb}),
		}
	
	def __init__(self, *args, **kwargs):
		
		self.restricted_fields = kwargs.pop('restricted_fields', [])
		super().__init__(*args, **kwargs)
		
		self.fields['id_localidad'].choices = []
		
		#-- Verificar si el formulario se llama con datos (POST).
		if self.is_bound:
			#-- Obtener el valor enviado de id_provincia.
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
		
		###################################################################################
		#-- Si es un nuevo registro.
		if not self.instance.pk:
			self.fields['id_sucursal'].initial = self.initial.get('id_sucursal')
			#-- Deshabilita el campo y evita la validación del requerido.
			self.fields['id_sucursal'].required = False
			self.fields['id_sucursal'].widget.attrs['disabled'] = True
		else:
			#-- Configuración en modo edición.
			self.fields['id_sucursal'].widget = forms.HiddenInput()
			self.fields['id_sucursal'].required = False
			self.initial['id_sucursal'] = self.instance.id_sucursal
		
		##########################################################################
		#-- Restricciones por jerarquía (sólo en modo edición).
		if self.instance.pk and self.restricted_fields:
			for campo in self.restricted_fields:
				if campo in self.fields:
					#-- Marcar como no requerido para evitar validación de requerido en campos vacíos.
					self.fields[campo].required = False
					#-- Usar Field.disabled para que Django no valide.
					self.fields[campo].disabled = True
					self.fields[campo].widget.attrs['readonly'] = True
					self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class', '') + ' bg-body-secondary'
		
		#-- Configurar el campo limite_credito según la condición de venta.
		if self.instance and self.instance.pk:
			if self.instance.condicion_venta == 1:  #-- Contado.
				self.fields['limite_credito'].required = False
				self.fields['limite_credito'].disabled = True
				self.fields['limite_credito'].widget.attrs['readonly'] = True
	
	def clean(self):
		cleaned_data = super().clean()
		
		#-- Asignar automáticamente id_sucursal si el formulario está en modo edición.
		if self.instance.pk:
			cleaned_data['id_sucursal'] = self.instance.id_sucursal
			#-- Remover id_sucursal de la validación en modo edición.
			if self._errors is not None:
				self._errors.pop('id_sucursal', None)
		
		#-- Restaurar valores de campos disabled y limpiar errores asociados.
		for campo in self.restricted_fields:
			if campo in self.fields and self.fields[campo].disabled:
				#-- Restaurar el valor original del instance.
				if self.instance and hasattr(self.instance, campo):
					cleaned_data[campo] = getattr(self.instance, campo)
				#-- Limpiar cualquier error de validación para este campo.
				if self._errors is not None and campo in self._errors:
					del self._errors[campo]
		
		return cleaned_data

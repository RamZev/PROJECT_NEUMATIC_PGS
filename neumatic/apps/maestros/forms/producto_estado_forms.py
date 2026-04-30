# neumatic\apps\maestros\forms\producto_estado_forms.py
from django import forms
from .crud_forms_generics import CrudGenericForm
from ..models.base_models import ProductoEstado
from diseno_base.diseno_bootstrap import formclasstext, formclassselect


class ProductoEstadoForm(CrudGenericForm):
	
	class Meta:
		model = ProductoEstado
		fields = '__all__'
		
		widgets = {
			'estatus_producto_estado':
				forms.Select(attrs={**formclassselect}),
			'estado_producto': 
				forms.TextInput(attrs={**formclasstext, 'oninput': 'this.value = this.value.toUpperCase()'}),
			'nombre_producto_estado': 
				forms.TextInput(attrs={**formclasstext, 'oninput': 'this.value = this.value.toUpperCase()'}),
			'color':
				forms.TextInput(attrs={**formclasstext, 'type': 'color'}),
		}
		
		error_messages = {
			'estado_producto': {
				'unique': 'Ya existe un Estado de Producto con ese Estado.',
				# 'required': 'Debe completar este campo.',
				# 'invalid': 'Ingrese un valor válido.'
			},
		}
	
	def __init__(self, *args, **kwargs):
		#-- Extraer registros_protegidos si se pasa como argumento.
		self.registros_protegidos = kwargs.pop('registros_protegidos', [])
		super().__init__(*args, **kwargs)
		
		#-- Si es un registro protegido, hacer los campos de solo lectura.
		if self.instance and self.instance.pk in self.registros_protegidos:
			for field_name in ['estado_producto', 'nombre_producto_estado']:
				self.fields[field_name].widget.attrs['readonly'] = True
				self.fields[field_name].widget.attrs['style'] = 'background-color: #d4eaff;'
				self.fields[field_name].widget.attrs['title'] = 'Campo protegido, no se puede modificar.'
	
	def clean(self):
		cleaned_data = super().clean()
		
		#-- Validar que no se modifiquen registros protegidos.
		if self.instance and self.instance.pk in self.registros_protegidos:
			#-- Verificar si se intentó modificar algún campo protegido.
			campos_protegidos = ['estado_producto', 'nombre_producto_estado']
			for campo in campos_protegidos:
				if campo in self.changed_data:
					raise forms.ValidationError(
						f"No se puede modificar el campo '{self.fields[campo].label}' "
						f"en el estado '{self.instance.nombre_producto_estado}' porque está protegido."
					)
		
		return cleaned_data
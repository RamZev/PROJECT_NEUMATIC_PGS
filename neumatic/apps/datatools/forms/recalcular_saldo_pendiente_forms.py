# neumatic\apps\datatools\forms\recalcular_saldo_pendiente_forms.py
from django import forms

from apps.maestros.models.cliente_models import Cliente
from diseno_base.diseno_bootstrap import formclasstext

class RecalcularSaldoPendienteForm(forms.Form):
	id_cliente = forms.IntegerField(
		label="Cód. Cliente",
		required=True,
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	nombre_cliente = forms.CharField(
		label="Cliente",
		required=False,
		widget=forms.TextInput(attrs={**formclasstext, 'readonly': 'readonly'})
	)
	
	def clean(self):
		cleaned_data = super().clean()
		
		id_cliente = cleaned_data.get("id_cliente")
		
		#-- Validar que se haya indicado un cliente solo si hay datos enviados.
		if not id_cliente:
			self.add_error("id_cliente", "Debe indicar un Código de Cliente.")
		
		if id_cliente:
			try:
				cliente = Cliente.objects.get(id_cliente=id_cliente)
				
				# #-- Validar que el usuario autenticado sea el vendedor del cliente, a menos que sea superusuario o pertenezca a los grupos permitidos.
				# if not self.user.is_superuser and not self.user_groups.intersection(self.allowed_groups) and cliente.id_vendedor != self.user.id_vendedor and self.user.jerarquia != 'A':
				# 	self.add_error("id_cliente", "No tiene permisos para consultar este cliente. Solo puede consultar clientes de su vendedor.")
				
			except Cliente.DoesNotExist:
				self.add_error("id_cliente", "El cliente no existe. Por favor, verifique el código.")
		
		return cleaned_data
	
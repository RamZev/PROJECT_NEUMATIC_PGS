# neumatic\apps\informes\forms\buscador_detallecupones_forms.py
from django import forms

from .informes_generics_forms import InformesGenericForm
from apps.ventas.models.caja_models import Caja
from diseno_base.diseno_bootstrap import (formclasstext)
from utils.helpers.export_helpers import JerarquiaSucursal


class BuscadorDetalleCuponesForm(InformesGenericForm):
	
	caja = forms.IntegerField(
		required=False,
		label="Número de Caja",
		widget=forms.NumberInput(attrs={**formclasstext})
	)
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
	
	def clean(self):
		cleaned_data = super().clean()
		
		caja = cleaned_data.get('caja')
		
		#-- Validaciones.
		if caja is None or caja < 1:
			self.add_error("caja", "Debe indicar un Número de Caja válido.")
		else:
			try:
				caja_obj = Caja.objects.get(numero_caja=caja)
			except Caja.DoesNotExist:
				self.add_error("caja", "El Número de Caja indicado no existe")
				return cleaned_data
			
			#-- Usar el helper para verificar permisos.
			if not JerarquiaSucursal.puede_consultar_caja(self.user, caja_obj):
				self.add_error(
					"caja", 
					"No tiene permisos para consultar esta caja. "
					"Solo puede consultar cajas de su sucursal."
				)
		
		return cleaned_data

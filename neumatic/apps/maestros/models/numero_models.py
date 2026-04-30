# neumatic\apps\maestros\models\numero_models.py
from django.db import models
from django.core.exceptions import ValidationError
import re

from .base_gen_models import ModeloBaseGenerico
from .base_models import PuntoVenta
from .sucursal_models import Sucursal
from entorno.constantes_base import ESTATUS_GEN


class Numero(ModeloBaseGenerico):
	id_numero = models.AutoField(
		primary_key=True
	)
	estatus_numero = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	id_sucursal = models.ForeignKey(
		Sucursal,
		on_delete=models.CASCADE,
		verbose_name="Sucursal"
	)
	id_punto_venta = models.ForeignKey(
		PuntoVenta,
		on_delete=models.PROTECT,
		verbose_name="Punto de Venta"
	)
	comprobante = models.CharField(
		verbose_name="Comprobante",
		max_length=3
	)
	letra = models.CharField(
		verbose_name="Letra",
		max_length=1
	)
	numero = models.BigIntegerField(
		verbose_name="Número"
	)
	lineas = models.IntegerField(
		verbose_name="Líneas"
	)
	copias = models.IntegerField(
		verbose_name="Copias"
	)
	
	class Meta:
		db_table = 'numero'
		verbose_name = 'Número de Comprobante'
		verbose_name_plural = 'Números de Comprobante'
		ordering = ['id_punto_venta__punto_venta', 'comprobante']
	
	def __str__(self):
		return self.comprobante
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not re.match(r'^\d{1,13}$', str(self.numero)):
			errors.update({'numero': 'Debe indicar sólo dígitos numéricos positivos, mínimo 1 y máximo 13.'})
		
		if not re.match(r'^^[1-9]\d{0,1}$', str(self.lineas)):
			errors.update({'lineas': 'Debe indicar sólo dígitos numéricos positivos, mínimo 1 y máximo 2.'})
		
		if not re.match(r'^[1-9]$', str(self.copias)):
			errors.update({'copias': 'Debe indicar sólo dígitos numéricos positivos, mínimo y máximo 1.'})
		
		if errors:
			raise ValidationError(errors)

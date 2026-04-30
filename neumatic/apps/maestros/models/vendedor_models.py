# neumatic\apps\maestros\models\vendedor_models.py
from django.db import models
from django.core.exceptions import ValidationError
import re
from .base_gen_models import ModeloBaseGenerico
from .sucursal_models import Sucursal
from entorno.constantes_base import ESTATUS_GEN, TIPO_VENTA


class Vendedor(ModeloBaseGenerico):
	id_vendedor = models.AutoField(
		primary_key=True
	)
	estatus_vendedor = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_vendedor = models.CharField(
		verbose_name="Nombre vendedor",
		max_length=30
	)
	domicilio_vendedor = models.CharField(
		verbose_name="Domicilio",
		max_length=30
	)
	email_vendedor = models.EmailField(
		verbose_name="Correo",
		max_length=50
	)
	telefono_vendedor = models.CharField(
		verbose_name="Teléfono",
		max_length=15
	)
	pje_auto = models.DecimalField(
		verbose_name="% auto",
		max_digits=4,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	pje_camion = models.DecimalField(
		verbose_name="% camión",
		max_digits=4,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	vence_factura = models.IntegerField(
		verbose_name="Días vcto. Fact.",
		default=0,
		blank=True
	)
	vence_remito = models.IntegerField(
		verbose_name="Días vcto. Remito",
		default=0,
		blank=True
	)
	id_sucursal = models.ForeignKey(
		Sucursal,
		on_delete=models.CASCADE,
		verbose_name="Sucursal"
	)
	tipo_venta = models.CharField(
		verbose_name="Tipo",
		max_length=1,
		choices=TIPO_VENTA
	)
	col_descuento = models.IntegerField(
		verbose_name="Columna Dcto.",
		default=0,
		blank=True
	)
	email_venta = models.BooleanField(
		verbose_name="Enviar correos con Comprobantes",
		default=False
	)
	info_saldo = models.BooleanField(
		verbose_name="Mostrar Saldo en Correos Electrónicos",
		default=False
	)
	info_estadistica = models.BooleanField(
		verbose_name="Mostrar Saldos en Comp. Sin Estadísticas",
		default=False
	)
	
	class Meta:
		db_table = 'vendedor'
		verbose_name = 'Vendedor'
		verbose_name_plural = 'Vendedores'
		ordering = ['nombre_vendedor']
	
	def __str__(self):
		return self.nombre_vendedor
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		pje_auto_str = str(self.pje_auto) if self.pje_auto is not None else ""
		pje_camion_str = str(self.pje_camion) if self.pje_camion is not None else ""
		vence_factura_str = str(self.vence_factura) if self.vence_factura is not None else ""
		vence_remito_str = str(self.vence_remito) if self.vence_remito is not None else ""
		col_descuento_str = str(self.col_descuento) if self.col_descuento is not None else ""
		
		if not re.match(r'^\+?\d[\d ]{0,14}$', str(self.telefono_vendedor)):
			errors.update({'telefono_vendedor': 'Debe indicar sólo dígitos numéricos positivos, mínimo 1 y máximo 15, el signo + y espacios.'})
		
		if not re.match(r'^(0|[1-9]\d{0,1})(\.\d{1,2})?$', pje_auto_str):
			errors.update({'pje_auto': 'El valor debe ser positivo, con hasta 2 dígitos enteros y hasta 2 decimales o cero.'})
		
		if not re.match(r'^(0|[1-9]\d{0,1})(\.\d{1,2})?$', pje_camion_str):
			errors.update({'pje_camion': 'El valor debe ser positivo, con hasta 2 dígitos enteros y hasta 2 decimales o cero.'})
		
		if not re.match(r'^[1-9]\d{0,2}$|^0$', vence_factura_str):
			errors.update({'vence_factura': 'El valor debe ser un número entero positivo, con hasta 3 dígitos o cero.'})
		
		if not re.match(r'^[1-9]\d{0,2}$|^0$', vence_remito_str):
			errors.update({'vence_remito': 'El valor debe ser un número entero positivo, con hasta 3 dígitos o cero.'})
		
		if not re.match(r'^[1-9]\d{0,2}$|^0$', col_descuento_str):
			errors.update({'col_descuento': 'El valor debe ser un número entero positivo, con hasta 3 dígitos o cero.'})
		
		if errors:
			raise ValidationError(errors)

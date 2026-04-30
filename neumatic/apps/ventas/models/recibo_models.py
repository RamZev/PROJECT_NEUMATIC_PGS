# neumatic\apps\ventas\models\recibo_models.py
from django.db import models

from apps.maestros.models.base_gen_models import ModeloBaseGenerico
from apps.maestros.models.base_models import (
	Banco,
	CuentaBanco,
	ConceptoBanco,
	Tarjeta,
	CodigoRetencion
)
from .factura_models import Factura


#-- Detalle del Recibo (I).
class DetalleRecibo(ModeloBaseGenerico):
	id_detalle_recibo = models.AutoField(
		primary_key=True
	)
	id_factura = models.ForeignKey(
		Factura,
		on_delete=models.CASCADE,
		verbose_name="Factura",
		related_name='detalles_recibo',
		null=True,
		blank=True
	)
	id_factura_cobrada = models.ForeignKey(
		Factura,
		on_delete=models.PROTECT,
		verbose_name="Factura Cobrada",
		related_name='cobranza',
		null=True,
		blank=True
	)
	monto_cobrado = models.DecimalField(
		verbose_name="Costo",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	observaciones_recibo = models.CharField(
		verbose_name="Observaciones", 
		max_length=50,
		null=True,
		blank=True
 	)
	
	class Meta:
		db_table = "detalle_recibo"
		verbose_name = 'Recibo'
		verbose_name_plural = 'Recibo'
		# ordering = ['id_detalle_recibo']
	
	def __str__(self):
		return f"{self.id_factura} {self.id_detalle_recibo}"

   
#-- Detalle de las Retenciones (II).
class RetencionRecibo(ModeloBaseGenerico):
	id_retencion_recibo = models.AutoField(
		primary_key=True
	)
	id_factura = models.ForeignKey(
		Factura,
		on_delete=models.CASCADE,
		verbose_name="Factura",
		null=True,
		blank=True
	)
	id_codigo_retencion = models.ForeignKey(
        CodigoRetencion,
        on_delete=models.CASCADE,
        verbose_name="Código Retención",
        null=True,
        blank=True
    )
	certificado = models.CharField(
		verbose_name="Certificado", 
		max_length=20,
		null=True,
		blank=True
 	)
	importe_retencion = models.DecimalField(
		verbose_name="Importe Retención",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	fecha_retencion = models.DateField(
		verbose_name="Fecha Retención",
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = "retencion_recibo"
		verbose_name = 'Retención Recibo'
		verbose_name_plural = 'Retenciones Recibo'
		# ordering = ['id_retencion_recibo']
	
	def __str__(self):
		return f"{self.id_factura} {self.id_retencion_recibo}"


#-- Detalle del depósito o transferencia  (III).
class DepositoRecibo(ModeloBaseGenerico):
	id_deposito_recibo = models.AutoField(
		primary_key=True
	)
	id_factura = models.ForeignKey(
		Factura,
		on_delete=models.CASCADE,
		verbose_name="Factura",
		null=True,
		blank=True
	)
	id_cuenta_banco = models.ForeignKey(
		CuentaBanco,
		on_delete=models.CASCADE,
		verbose_name="Banco",
		null=True,
		blank=True
	)
	id_concepto_banco = models.ForeignKey(
		ConceptoBanco,
		on_delete=models.CASCADE,
		verbose_name="Concepto",
		null=True,
		blank=True
	)
	fecha_deposito = models.DateField(
		verbose_name="Fecha Depósito",
		null=True,
		blank=True
	)
	importe_deposito = models.DecimalField(
		verbose_name="Importe Depósito",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	detalle_deposito = models.CharField(
		verbose_name="Detalle", 
		max_length=20,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = "deposito_recibo"
		verbose_name = 'Depósito Recibo'
		verbose_name_plural = 'Dépositos Recibo'
		# ordering = ['id_deposito_recibo']
	
	def __str__(self):
		return f"{self.id_factura} {self.id_deposito_recibo}"


#-- Detalle del Pago con Tarjeta  (IV).
class TarjetaRecibo(ModeloBaseGenerico):
	id_tarjeta_recibo = models.AutoField(
		primary_key=True
	)
	id_factura = models.ForeignKey(
		Factura,
		on_delete=models.CASCADE,
		verbose_name="Factura",
		null=True,
		blank=True
	)
	id_tarjeta = models.ForeignKey(
		Tarjeta,
		on_delete=models.CASCADE,
		verbose_name="Tarjeta",
		null=True,
		blank=True
	)
	cupon = models.BigIntegerField(
		verbose_name="Cupón",
		null=True,
		blank=True
	)
	lote = models.BigIntegerField(
		verbose_name="Lote",
		null=True,
		blank=True
	)
	cuotas = models.BigIntegerField(
		verbose_name="Cuotas",
		null=True,
		blank=True
	)
	importe_tarjeta = models.DecimalField(
		verbose_name="Importe Tarjeta",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	
	class Meta:
		db_table = "tarjeta_recibo"
		verbose_name = 'Tarjeta Recibo'
		verbose_name_plural = 'Tarjetas Recibo'
		# ordering = ['id_tarjeta_recibo']
	
	def __str__(self):
		return f"{self.id_factura} {self.id_tarjeta_recibo}"


#-- Detalle del cheque  (V).
class ChequeRecibo(ModeloBaseGenerico):
	id_cheque_recibo = models.AutoField(
		primary_key=True
	)
	id_factura = models.ForeignKey(
		Factura,
		on_delete=models.CASCADE,
		verbose_name="Factura",
		null=True,
		blank=True
	)
	id_banco = models.ForeignKey(
		Banco,
		on_delete=models.CASCADE,
		verbose_name="Banco",
		null=True,
		blank=True
	)
	codigo_banco = models.BigIntegerField(
		verbose_name="Código Banco", 
		null=True,
		blank=True
	)
	sucursal = models.BigIntegerField(
		verbose_name="Sucursal", 
		null=True,
		blank=True
	)
	codigo_postal = models.BigIntegerField(
		verbose_name="Código Postal",
		null=True,
		blank=True
	)
	numero_cheque_recibo = models.BigIntegerField(
		verbose_name="Número",
		null=True,
		blank=True
	)
	cuenta_cheque_recibo = models.BigIntegerField(
		verbose_name="Cuenta",
		null=True,
		blank=True
	)
	cuit_cheque_recibo = models.BigIntegerField(
		verbose_name="CUIT",
		null=True,
		blank=True
	)
	fecha_cheque1 = models.DateField(
		verbose_name="Fecha 1",
		null=True,
		blank=True
	)
	fecha_cheque2 = models.DateField(
		verbose_name="Fecha 2",
		null=True,
		blank=True
	)
	importe_cheque = models.DecimalField(
		verbose_name="Importe Cheque",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	electronico = models.BooleanField(
		verbose_name="Estatus",
		null=True,
		blank=True,
		default=False
	)
	
	class Meta:
		db_table = "cheque_recibo"
		verbose_name = 'Cheque Recibo'
		verbose_name_plural = 'Cheques Recibo'
		# ordering = ['id_cheque_recibo']
	
	def __str__(self):
		return f"{self.id_factura} {self.id_cheque_recibo}"


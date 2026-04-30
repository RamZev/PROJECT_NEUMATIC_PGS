# neumatic\apps\ventas\models\compra_models.py
from django.db import models

from apps.maestros.models.base_gen_models import ModeloBaseGenerico
from entorno.constantes_base import ESTATUS_GEN, CONDICION_VENTA
from apps.maestros.models.base_models import (ComprobanteCompra,
											  ComprobanteVenta, 
											  ProductoDeposito, 
											  Provincia, 
											  PuntoVenta,)
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.proveedor_models import Proveedor
from apps.maestros.models.producto_models import Producto


class Compra(ModeloBaseGenerico):
	id_compra = models.AutoField(
		primary_key=True
	)
	estatus_comprabante = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	id_sucursal = models.ForeignKey(
		Sucursal,
		on_delete=models.PROTECT,
		verbose_name="Sucursal",
		null=True,
		blank=True
	)
	id_punto_venta = models.ForeignKey(
		PuntoVenta,
		on_delete=models.PROTECT,
		verbose_name="Punto de Venta",
		null=True,
		blank=True
	)
	id_deposito = models.ForeignKey(
		ProductoDeposito,
		on_delete=models.PROTECT,
		verbose_name="Depósito",
		null=True,
		blank=True
	)
	id_comprobante_compra = models.ForeignKey(
		ComprobanteCompra,
		on_delete=models.PROTECT,
		verbose_name="Comprobante",
		null=True,
		blank=True
	)
	compro = models.CharField(
		verbose_name="Compro",
		max_length=3,
		null=True,
		blank=True
	)
	letra_comprobante = models.CharField(
		verbose_name="Letra",
		max_length=1,
		null=True,
		blank=True
	)
	numero_comprobante = models.BigIntegerField(
		verbose_name="Número",
		null=True,
		blank=True
	)
	fecha_registro = models.DateField(
		verbose_name="Fecha Registro",
		null=True,
		blank=True
	)
	id_proveedor = models.ForeignKey(
		Proveedor,
		on_delete=models.PROTECT,
		verbose_name="Proveedor",
		null=True,
		blank=True
	)
	id_provincia = models.ForeignKey(
		Provincia,
		on_delete=models.PROTECT,
		verbose_name="Provincia",
		null=True,
		blank=True
	)
	condicion_comprobante = models.IntegerField(
		verbose_name="Condición de Compra",
		default=1,
		choices=CONDICION_VENTA
	)
	id_comprobante_venta = models.ForeignKey(
		ComprobanteVenta,
		on_delete=models.PROTECT,
		verbose_name="Comp. Compra",
		null=True,
		blank=True
	)
	numero_comprobante_venta = models.BigIntegerField(
		verbose_name="Número C/Compra",
		null=True,
		blank=True
	)
	total_comprobante_venta = models.DecimalField(
		verbose_name="Total C/Compra",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	fecha_comprobante = models.DateField(
		verbose_name="Fecha Emisión",
		null=True,
		blank=True
	)
	fecha_vencimiento = models.DateField(
		verbose_name="Fecha Vencimiento",
		null=True,
		blank=True
	)
	gravado = models.DecimalField(
		verbose_name="Gravado",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	no_gravado = models.DecimalField(
		verbose_name="No Gravado",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	no_inscripto = models.DecimalField(
		verbose_name="No Inscripto",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	exento = models.DecimalField(
		verbose_name="Exento",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	retencion_iva = models.DecimalField(
		verbose_name="Retención IVA",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	retencion_ganancia = models.DecimalField(
		verbose_name="Retención Ganancia",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	retencion_ingreso_bruto = models.DecimalField(
		verbose_name="Retención Ingreso Bruto",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	sellado = models.DecimalField(
		verbose_name="Sellado",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	percepcion_iva = models.DecimalField(
		verbose_name="Percepción IVA",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	percepcion_ingreso_bruto = models.DecimalField(
		verbose_name="Percepción Ingreso Bruto",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	iva = models.DecimalField(
		verbose_name="Iva",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	total = models.DecimalField(
		verbose_name="Total",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	entrega = models.DecimalField(
		verbose_name="Entrega",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	documento_asociado = models.CharField(
		verbose_name="Documento Asociado",
		max_length=12,
		default="",
		null=True,
		blank=True
	)
	alicuota_iva = models.DecimalField(
		verbose_name="Alicuota",
		max_digits=4,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	observa_comprobante = models.TextField(
		verbose_name="Observaciones",
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = "compra"
		verbose_name = 'Compra'
		verbose_name_plural = 'Compras'
	
	def __str__(self):
		numero = str(self.numero_comprobante).strip().zfill(12)
		return f"{self.id_comprobante_compra.codigo_comprobante_compra} {self.letra_comprobante} {numero[:4]}-{numero[4:]}"
	
	@property
	def numero_comprobante_formateado(self):
		numero = str(self.numero_comprobante).strip().zfill(12)
		return f"{numero[:4]}-{numero[4:]}"
	
	@property
	def numero_comprobante_venta_formateado(self):
		numero = str(self.numero_comprobante_venta).strip().zfill(12)
		return f"{numero[:4]}-{numero[4:]}"


class DetalleCompra(ModeloBaseGenerico):
	id_detalle_compra = models.AutoField(
		primary_key=True
	)
	id_compra = models.ForeignKey(
		Compra,
		on_delete=models.CASCADE,
		verbose_name="Factura",
		null=True,
		blank=True
	)
	id_producto = models.ForeignKey(
		Producto,
		on_delete=models.PROTECT,
		verbose_name="Producto",
		null=True,
		blank=True
	)
	cantidad = models.DecimalField(
		verbose_name="Cantidad",
		max_digits=7,
		decimal_places=2,
		null=True,
		blank=True
	)
	precio = models.DecimalField(
		verbose_name="Precio",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True
	)
	total = models.DecimalField(
		verbose_name="Total",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True
	)
	stock = models.DecimalField(
		verbose_name="Stock",
		max_digits=10,
		decimal_places=2,
		null=True,
		blank=True
	)
	despacho = models.CharField(
		verbose_name="Despacho",
		max_length=16,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = "detalle_compra"
		verbose_name = 'Detalle Compra'
		verbose_name_plural = 'Detalles Compra'
	
	def __str__(self):
		return self.id_detalle_compra

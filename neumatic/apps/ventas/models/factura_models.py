# neumatic\apps\ventas\models\factura_models.py
from django.db import models

from apps.maestros.models.base_gen_models import ModeloBaseGenerico
from entorno.constantes_base import ESTATUS_GEN, CONDICION_VENTA
from apps.maestros.models.base_models import (
	ComprobanteVenta,
	ProductoDeposito,
	Operario,
	PuntoVenta,
	MarketingOrigen,
)
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.cliente_models import Cliente
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.vendedor_models import Vendedor
from apps.maestros.models.valida_models import Valida
from apps.ventas.models.caja_models import Caja


class Factura(ModeloBaseGenerico):
	id_factura = models.AutoField(
		primary_key=True
	)
	id_orig = models.IntegerField(
		verbose_name="ID_ORIG",
		null=True,
		blank=True
	)
	estatus_comprobante = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	id_marketing_origen = models.ForeignKey(
		MarketingOrigen,
		on_delete=models.PROTECT,
		verbose_name="Marketing",
		default=1
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
	id_caja = models.ForeignKey(
        Caja,
        on_delete=models.PROTECT,
        verbose_name="Caja",
        null=True,
        blank=True
    )
	jerarquia = models.CharField(
		verbose_name="Jerarquía", 
		max_length=1,
		null=True, 
		blank=True
	)
	id_comprobante_venta = models.ForeignKey(
		ComprobanteVenta,
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
	comprobante_remito = models.CharField(
		verbose_name="Comprobante Remito",
		max_length=2,
		default="",
		null=True,
		blank=True
	)
	remito = models.CharField(
		verbose_name="Remito",
		max_length=15,
		null=True,
		blank=True
	)
	id_comprobante_asociado = models.IntegerField(
		verbose_name="Comprobate Asociado",
		null=True,
		blank=True
	)
	comprobante_asociado = models.CharField(
		verbose_name="Comprobante Asociado",
		max_length=2,
		default="",
		null=True,
		blank=True
	)
	numero_asociado = models.CharField(
		verbose_name="Número Asoc.",
		max_length=15,
		null=True,
		blank=True
	)
	fecha_comprobante = models.DateField(
		verbose_name="Fecha Emisión",
		null=True,
		blank=True
	)
	id_cliente = models.ForeignKey(
		Cliente,
		on_delete=models.PROTECT,
		verbose_name="Cliente",
		null=True,
		blank=True
	)
	cuit = models.BigIntegerField(
		verbose_name="CUIT",
		null=True,
		blank=True
	)
	nombre_factura = models.CharField(
		verbose_name="Nombre",
		max_length=50,
		null=True,
		blank=True
	)
	domicilio_factura = models.CharField(
		verbose_name="Domicilio",
		max_length=50,
		null=True,
		blank=True
	)
	movil_factura = models.CharField(
		verbose_name="Móvil", 
		max_length=15, 
		null=True, 
		blank=True
	)
	email_factura = models.EmailField(
		verbose_name="Email*", 
		max_length=50, 
		null=True, 
		blank=True
	)
	condicion_comprobante = models.IntegerField(
		verbose_name="Condición de Venta",
		default=1,
		choices=CONDICION_VENTA
	)
	id_vendedor = models.ForeignKey(
		Vendedor, 
		on_delete=models.PROTECT,
		null=True, blank=True,
		verbose_name="Vendedor"
	)
	gravado = models.DecimalField(
		verbose_name="Gravado",
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
	iva = models.DecimalField(
		verbose_name="IVA",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	percep_ib = models.DecimalField(
		verbose_name="Percepción IB",
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
	estado = models.CharField(
		verbose_name="Estado",
		max_length=1,
		null=True,
		blank=True,
		default=""
	)
	marca = models.CharField(
		verbose_name="Marca",
		max_length=1,
		null=True,
		blank=True
	)
	comision = models.CharField(
		verbose_name="Comisión",
		max_length=1,
		null=True,
		blank=True
	)
	fecha_pago = models.DateField(
		verbose_name="Fecha Pago",
		null=True,
		blank=True
	)
	no_estadist = models.BooleanField(
		verbose_name="No estadist.",
		null=True,
		blank=True
	)
	suc_imp = models.SmallIntegerField(
		verbose_name="sucimp",
		null=True,
		blank=True
	)
	cae = models.BigIntegerField(
		verbose_name="CAE",
		null=True,
		blank=True,
		default=0
	)
	cae_vto = models.DateField(
		verbose_name="Vcto. CAE",
		null=True,
		blank=True
	)
	observa_comprobante = models.TextField(
		verbose_name="Observaciones",
		# max_length=50,
		null=True,
		blank=True
	)
	stock_clie = models.BooleanField(
		verbose_name="stockclie",
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
	promo = models.BooleanField(
		verbose_name="Promo",
		null=True,
		blank=True
	)
	id_valida = models.ForeignKey(
		Valida,
		on_delete=models.PROTECT,
		verbose_name="Validar",
		null=True,
		blank=True
	)
	recibo_manual_auto = models.SmallIntegerField(
		verbose_name="Talonario",
		null=True,
		blank=True
	)
	suma_comision_vendedor = models.BooleanField(
		verbose_name="Suma Comisión a Vendedor",
		null=True,
		blank=True
	)
	productos_camiones = models.BooleanField(
		verbose_name="Productos de Camiones",
		null=True,
		blank=True
	)
	efectivo_recibo = models.DecimalField(
		verbose_name="Efectivo",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	compensa_factura = models.DecimalField(
		verbose_name="Compensa",
		max_digits=14,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	
	class Meta:
		db_table = "factura"
		verbose_name = 'Factura'
		verbose_name_plural = 'Facturas'
		# ordering = ['id_factura']
	
	def __str__(self):
		numero = str(self.numero_comprobante).strip().zfill(12)
		return f"{self.id_comprobante_venta.codigo_comprobante_venta} {self.letra_comprobante} {numero[:4]}-{numero[4:]}"
	
	@property
	def condicion_venta(self):
		return dict(CONDICION_VENTA).get(self.condicion_comprobante, "No definido")
	
	@property
	def numero_comprobante_formateado(self):
		numero = str(self.numero_comprobante).strip().zfill(12)
		return f"{numero[:4]}-{numero[4:]}"
	
	@property
	def letra_numero_comprobante_formateado(self):
		return f"{self.letra_comprobante} {self.numero_comprobante_formateado}"
	
	@property
	def compro_letra_numero_comprobante_formateado(self):
		return f"{self.compro} {self.letra_comprobante} {self.numero_comprobante_formateado}"
	
	@property
	def compro_letra_numero_comprobante(self):
		return f"{self.compro} {self.letra_comprobante} {self.numero_comprobante}"
	
	@property
	def numero_asociado_formateado(self):
		numero = ""
		if self.numero_asociado:
			numero = str(self.numero_asociado).strip().zfill(12)
			numero = f"{numero[:4]}-{numero[4:]}"
		return numero
	
	@property
	def letra_numero_asociado_formateado(self):
		return f"{self.letra_asociado}-{self.numero_asociado_formateado}" if self.numero_asociado_formateado else ""


class DetalleFactura(ModeloBaseGenerico):
	id_detalle_factura = models.AutoField(
		primary_key=True
	)
	id_factura = models.ForeignKey(
		Factura,
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
	codigo = models.IntegerField(
		verbose_name="Cód. Producto",
		null=True,
		blank=True
	)
	producto_venta = models.CharField(
	 	verbose_name="Nombre producto", 
	  	max_length=50,
		null=True,
		blank=True
	)
	cantidad = models.DecimalField(
		verbose_name="Cantidad",
		max_digits=7,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	costo = models.DecimalField(
		verbose_name="Costo",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	precio_lista = models.DecimalField(
		verbose_name="Precio",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	precio = models.DecimalField(
		verbose_name="Precio",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	descuento = models.DecimalField(
		verbose_name="Descuento(%)",
		max_digits=6,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	desc_vendedor = models.DecimalField(
		verbose_name="Desc. Vend(%)",
		max_digits=6,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	desc_revendedor = models.DecimalField(
		verbose_name="Desc. Rev(%)",
		max_digits=6,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
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
	alic_iva = models.DecimalField(
		verbose_name="Alíc. IVA(%)",
		max_digits=6,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	iva = models.DecimalField(
		verbose_name="IVA",
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
	reventa = models.CharField(
		verbose_name="Reventa",
		max_length=1,
		null=True,
		blank=True
	)
	stock = models.DecimalField(
		verbose_name="Stock",
		max_digits=10,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	act_stock = models.BooleanField(
		verbose_name="Act. Stock",
		null=True,
		blank=True,
		default=False
	)
	id_operario = models.ForeignKey(
		Operario,
		on_delete=models.PROTECT,
		verbose_name="Operario",
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = "detalle_factura"
		verbose_name = 'Detalle Factura'
		verbose_name_plural = 'Detalles Factura'
		# ordering = ['id_detalle_factura']
	
	def __str__(self):
		return self.id_detalle_factura


class SerialFactura(ModeloBaseGenerico):
	id_serial_factura = models.AutoField(
		primary_key=True
	)
	id_factura = models.ForeignKey(
		Factura,
		on_delete=models.CASCADE,
		verbose_name="Factura",
		null=True,
		blank=True
	)
	producto_serial = models.CharField(
		verbose_name="Serial producto", 
		max_length=50,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = "serial_factura"
		verbose_name = 'Detalle Serial'
		verbose_name_plural = 'Detalles Serial'

	def __str__(self):
		return self.producto_serial

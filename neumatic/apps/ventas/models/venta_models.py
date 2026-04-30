# neumatic\apps\ventas\models\venta_models.py
from django.db import models
from apps.maestros.models.base_models import ModeloBaseGenerico


class StockCliente(ModeloBaseGenerico):
	id_stock_cliente = models.AutoField(
		primary_key=True
	)
	id_factura = models.ForeignKey(
		'Factura',
		on_delete=models.PROTECT,
		verbose_name="Factura",
		null=True,
		blank=True
	)
	id_producto = models.ForeignKey(
		'maestros.Producto',
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
		blank=True,
		default=0.0
	)
	retirado = models.DecimalField(
		verbose_name="Retiro",
		max_digits=7,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.0
	)
	fecha_retiro = models.DateField(
		verbose_name="Fecha Retiro",
		null=True,
		blank=True
	)
	numero = models.IntegerField(
		verbose_name="Número",
		null=True,
		blank=True
	)
	comentario = models.CharField(
		verbose_name="Comentario",
		max_length=60,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = 'stock_cliente'
		verbose_name = 'Stock Cliente'
		verbose_name_plural = 'Stocks Clientes'
		ordering = ['id_stock_cliente', 'fecha_retiro']

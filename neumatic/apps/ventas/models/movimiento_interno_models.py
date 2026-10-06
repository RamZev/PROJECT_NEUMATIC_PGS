# neumatic/apps/ventas/models/movimiento_interno_models.py
from django.db import models

from apps.maestros.models.base_gen_models import ModeloBaseGenerico
from entorno.constantes_base import ESTATUS_GEN
from apps.maestros.models.base_models import (
    ComprobanteVenta,
    ProductoDeposito,
)
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.producto_models import Producto


class MovimientoInterno(ModeloBaseGenerico):
    id_movimiento_interno = models.AutoField(
        primary_key=True
    )
    estatus_comprobante = models.BooleanField(
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
    id_deposito = models.ForeignKey(
        ProductoDeposito,
        on_delete=models.PROTECT,
        verbose_name="Depósito",
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
    fecha_comprobante = models.DateField(
        verbose_name="Fecha Emisión",
        null=True,
        blank=True
    )
    observa_comprobante = models.TextField(
        verbose_name="Observaciones",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "movimiento_interno"
        verbose_name = 'Movimiento Interno'
        verbose_name_plural = 'Movimientos Internos'
        ordering = ['id_movimiento_interno']

    def __str__(self):
        compro = self.id_comprobante_venta.codigo_comprobante_venta if self.id_comprobante_venta else "MI"
        letra = self.letra_comprobante or ""
        numero = str(self.numero_comprobante).zfill(8) if self.numero_comprobante else "00000000"
        return f"{compro} {letra} {numero}".strip()


class DetalleMovimientoInterno(ModeloBaseGenerico):
    id_detalle_movimiento_interno = models.AutoField(
        primary_key=True
    )
    id_movimiento_interno = models.ForeignKey(
        MovimientoInterno,
        on_delete=models.CASCADE,
        verbose_name="Movimiento Interno",
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

    class Meta:
        db_table = "detalle_movimiento_interno"
        verbose_name = 'Detalle Movimiento Interno'
        verbose_name_plural = 'Detalles Movimiento Interno'
        ordering = ['id_detalle_movimiento_interno']

    def __str__(self):
        return f"{self.id_detalle_movimiento_interno} - {self.producto_venta}"
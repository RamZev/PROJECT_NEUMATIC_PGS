# neumatic\apps\ventas\models\servicio_vehiculo_models.py
from django.db import models
from django.core.exceptions import ValidationError

from apps.maestros.models.base_gen_models import ModeloBaseGenerico
from apps.maestros.models.cliente_models import Cliente
from apps.maestros.models.vehiculo_models import Vehiculo
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.vendedor_models import Vendedor
from entorno.constantes_base import ESTATUS_GEN


class ServicioVehiculo(ModeloBaseGenerico):
    """
    Cabecera de un servicio realizado a un vehículo.
    La fecha de registro se hereda de ModeloBaseGenerico (campo `fcontrol`,
    auto_now_add=True), por lo que NO se declara explícitamente.
    """
    id_servicio_vehiculo = models.AutoField(primary_key=True)

    estatus_servicio_vehiculo = models.BooleanField(
        verbose_name="Estatus",
        default=True,
        choices=ESTATUS_GEN,
        db_index=True
    )

    id_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        verbose_name="Cliente",
        related_name="servicios_vehiculo",
        db_index=True
    )

    id_vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT,
        verbose_name="Vehículo",
        related_name="servicios",
        db_index=True
    )

    kmxmes = models.PositiveIntegerField(
        verbose_name="Kilometraje actual",
        null=True, blank=True
    )
    
    proxima_visita = models.DateField(
        verbose_name="Próxima visita",
        null=True,
        blank=True
    )

    observaciones = models.TextField(
        verbose_name="Observaciones",
        null=True, blank=True
    )

    class Meta:
        db_table = "servicio_vehiculo"
        verbose_name = "Servicio de Vehículo"
        verbose_name_plural = "Servicios de Vehículos"
        ordering = ["-id_servicio_vehiculo"]
        indexes = [
            models.Index(fields=["id_cliente", "id_vehiculo"]),
        ]

    def __str__(self):
        return f"Servicio #{self.id_servicio_vehiculo} - {self.id_vehiculo}"

    def clean(self):
        super().clean()
        errors = {}
        if not self.id_cliente:
            errors['id_cliente'] = 'Debe seleccionar un cliente.'
        if not self.id_vehiculo:
            errors['id_vehiculo'] = 'Debe seleccionar un vehículo.'
        if errors:
            raise ValidationError(errors)


class DetalleServicioVehiculo(ModeloBaseGenerico):
    """
    Detalle de un servicio. Corresponde a la tabla origen `trabvehi.DBF`.
    La patente, fecha, km y próxima visita viven en la cabecera
    (ServicioVehiculo); aquí solo van los datos propios de la línea.
    """
    id_detalle_servicio_vehiculo = models.AutoField(primary_key=True)

    id_servicio_vehiculo = models.ForeignKey(
        ServicioVehiculo,
        on_delete=models.CASCADE,
        verbose_name="Servicio",
        related_name="detalles"
    )

    id_producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        verbose_name="Producto"
    )

    cantidad = models.DecimalField(
        verbose_name="Cantidad",
        max_digits=10,
        decimal_places=2,
        default=1.00
    )

    id_vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.PROTECT,
        verbose_name="Vendedor",
        null=True, blank=True
    )

    exportado = models.BooleanField(
        verbose_name="Exportado",
        default=False
    )

    class Meta:
        db_table = "detalle_servicio_vehiculo"
        verbose_name = "Detalle de Servicio de Vehículo"
        verbose_name_plural = "Detalles de Servicios de Vehículos"
        ordering = ["id_detalle_servicio_vehiculo"]

    def __str__(self):
        return f"{self.id_producto} x {self.cantidad}"

    def clean(self):
        super().clean()
        errors = {}
        if self.cantidad is not None and self.cantidad <= 0:
            errors['cantidad'] = 'La cantidad debe ser mayor a cero.'
        if errors:
            raise ValidationError(errors)
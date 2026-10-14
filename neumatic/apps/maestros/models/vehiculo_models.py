# neumatic\apps\maestros\models\vehiculo_models.py
from django.db import models
from django.core.exceptions import ValidationError
import re

from .base_gen_models import ModeloBaseGenerico
from entorno.constantes_base import ESTATUS_GEN, TIPO_PRODUCTO_SERVICIO

TIPO_CHOICES = [
        (0, "0 - Otro"),
        (1, "1 - Automóvil"),
        (2, "2 - Pickup / SUV"),
        (3, "3 - Utilitario / Comercial"),
        (4, "4 - Camión"),
    ]

SEGMENTO_CHOICES = [
        (" ", " "),
        ("H", "H"),
        ("LT", "LT"),
        ("MM", "MM"),
        ("SUV", "SUV"),
        ("VZ", "VZ"),
    ]

class MarcaVehiculo(ModeloBaseGenerico):
    id_marca_vehiculo = models.AutoField(
            primary_key=True
        )
    estatus_marca_vehiculo = models.BooleanField(
        verbose_name="Estatus",
        default=True,
        choices=ESTATUS_GEN
    )
    marca_vehiculo = models.CharField(
        max_length=20, 
        unique=True
    )

    class Meta:
        db_table = "marca_vehiculo"
        verbose_name = "Marca Vehículo"
        verbose_name_plural = "Marcas Vehículos"
        ordering = ["marca_vehiculo"]

    def __str__(self):
        return self.marca_vehiculo


class ModeloVehiculo(ModeloBaseGenerico):
    id_modelo_vehiculo = models.AutoField(
                primary_key=True
            )
    estatus_modelo_vehiculo = models.BooleanField(
        verbose_name="Estatus",
        default=True,
        choices=ESTATUS_GEN
    )
    id_marca_vehiculo = models.ForeignKey(
        MarcaVehiculo,
        on_delete=models.CASCADE,
        related_name="modelos",
        verbose_name="Marca", 
    )
    modelo_vehiculo = models.CharField(
        verbose_name="Modelo", 
        max_length=20
    )

    class Meta:
        db_table = "modelo_vehiculo"
        verbose_name = "Modelo Vehículo"
        verbose_name_plural = "Modelos Vehículos"
        ordering = ["id_marca_vehiculo", "modelo_vehiculo"]
        constraints = [
            models.UniqueConstraint(
                fields=["id_marca_vehiculo", "modelo_vehiculo"], name="unique_modelo_por_marca"
            )
        ]

    def __str__(self):
        return f"{self.id_marca_vehiculo.marca_vehiculo} {self.modelo_vehiculo}"


class Vehiculo(ModeloBaseGenerico):
    id_vehiculo = models.AutoField(
        primary_key=True
    )
    estatus_vehiculo = models.BooleanField(
        verbose_name="Estatus", 
        default=True,
        choices=ESTATUS_GEN
    )
    tipo_vehiculo = models.PositiveSmallIntegerField(
        verbose_name="Tipo de vehículo", 
        choices=TIPO_CHOICES, 
        default=1, 
        db_index=True
    )
    id_marca_vehiculo = models.ForeignKey(
        MarcaVehiculo,
        on_delete=models.PROTECT,
        related_name="vehiculos",     # ← marca.vehiculos.all()
        null=True, blank=True,
    )
    id_modelo_vehiculo = models.ForeignKey(
        ModeloVehiculo,
        on_delete=models.PROTECT,
        related_name="vehiculos",     # ← modelo.vehiculos.all()  (no choca, son modelos distintos)
        null=True, blank=True,
    )    
    segmento = models.CharField(
        verbose_name="Segmento",
        max_length=3,
        choices=SEGMENTO_CHOICES, 
        default=" ", 
        db_index=True,
        blank=True,     # ← agregar
    )
    anio = models.PositiveSmallIntegerField(
        verbose_name="Año",
        null=True, 
        blank=True, 
        db_index=True
    )
    patente = models.CharField(
        verbose_name="Patente",
        max_length=7, 
        blank=True, 
        db_index=True
    )
    kmxmes = models.PositiveIntegerField(
        verbose_name="Kilometraje",
        null=True, 
        blank=True
    )
    visita = models.DateField(
        verbose_name="Visita",
        null=True, 
        blank=True, 
        db_index=True)
    exportado = models.BooleanField(
        verbose_name="Exportado", 
        default=False,
    )
    # Nuevo campo tipo Memo
    observacion = models.TextField(
        verbose_name="Observación",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "vehiculo"
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = [
            "id_marca_vehiculo__marca_vehiculo",
            "id_modelo_vehiculo__modelo_vehiculo",
            "anio",
        ]
        indexes = [
            models.Index(fields=["id_marca_vehiculo", "id_modelo_vehiculo"]),
            models.Index(fields=["exportado", "visita"]),
        ]

    def __str__(self):
        marca = self.id_marca_vehiculo.marca_vehiculo if self.id_marca_vehiculo else "?"
        modelo = self.id_modelo_vehiculo.modelo_vehiculo if self.id_modelo_vehiculo else "?"
        return f"{marca} {modelo} ({self.anio}) - {self.patente}"
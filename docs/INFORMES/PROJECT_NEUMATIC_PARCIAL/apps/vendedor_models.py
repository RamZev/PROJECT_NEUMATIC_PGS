# D:\PROJECT_NEUMATIC\neumatic\apps\maestros\models\empresa_models.py
from django.db import models
from .base_gen_models import ModeloBaseGenerico
from .base_models import *


# -- Datos estándares aplicables a los modelos base
ESTATUS_GEN = [
    (True, 'Activo'),
    (False, 'Inactivo'),
]

class Vendedor(ModeloBaseGenerico):
    id_vendedor = models.AutoField(primary_key=True)
    estatus_vendedor = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)
    nombre_vendedor = models.CharField(max_length=30)
    domicilio_vendedor = models.CharField(max_length=30)
    email_vendedor = models.CharField(max_length=50)
    telefono_vendedor = models.CharField(max_length=15)
    pje_auto = models.DecimalField(max_digits=6, decimal_places=2)
    pje_camion = models.DecimalField(max_digits=6, decimal_places=2)
    vence_factura = models.IntegerField()
    vence_remito = models.IntegerField()
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)  # Relación con sucursal
    tipo_venta = models.CharField(max_length=1)
    col_descuento = models.IntegerField()
    email_venta = models.BooleanField(default=False)
    info_saldo = models.BooleanField(default=False)
    info_estadistica = models.BooleanField(default=False)

    class Meta:
        db_table = 'vendedor'
        verbose_name = ('Vendedor')
        verbose_name_plural = ('Vendedores')
        ordering = ['nombre_vendedor']
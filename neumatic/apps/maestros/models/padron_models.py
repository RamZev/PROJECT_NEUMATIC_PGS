# apps/maestros/models/padron_models.py
from django.db import models
from .base_gen_models import ModeloBaseGenerico
from .base_models import Provincia

class PadronEntreRiosIIBB(ModeloBaseGenerico):
    id_padron = models.AutoField(primary_key=True)
    
    fecha_publicacion = models.DateField(verbose_name="Fecha publicación")
    fecha_vigencia_desde = models.DateField(verbose_name="Vigencia desde")
    fecha_vigencia_hasta = models.DateField(verbose_name="Vigencia hasta")
    
    cuit = models.BigIntegerField(verbose_name="CUIT", db_index=True)
    tipo_contr_insc = models.CharField(
        max_length=1,
        verbose_name="Tipo contribuyente",
        choices=[('D', 'D'), ('C', 'C'), ('-', 'Sin dato')],
        blank=True,
        null=True
    )
    marca_alta_sujeto = models.BooleanField(verbose_name="Alta sujeto", default=False)
    marca_alicuota = models.BooleanField(verbose_name="Aplica alícuota", default=False)
    
    alicuota_percepcion = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name="Alícuota percepción (%)",
        default=0.00
    )
    alicuota_retencion = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name="Alícuota retención (%)",
        default=0.00
    )
    
    nro_grupo_percepcion = models.CharField(
        max_length=5,
        verbose_name="Nro grupo percepción",
        blank=True,
        default='0'
    )
    nro_grupo_retencion = models.CharField(
        max_length=5,
        verbose_name="Nro grupo retención",
        blank=True,
        default='0'
    )
    
    razon_social = models.CharField(
        max_length=100,
        verbose_name="Razón social"
    )
    
    id_provincia = models.ForeignKey(
        Provincia,
        on_delete=models.PROTECT,
        verbose_name="Provincia",
        default=6  # Asumiendo que Entre Ríos tiene id=1, pero puedes ajustar
    )
    
    class Meta:
        db_table = 'padron_entre_rios'
        verbose_name = 'Padrón IIBB - Entre Ríos'
        verbose_name_plural = 'Padrones IIBB - Entre Ríos'
        ordering = ['-fecha_vigencia_desde', 'razon_social']
        unique_together = [['cuit', 'fecha_vigencia_desde']]
    
    def __str__(self):
        return f"{self.cuit} - {self.razon_social}"


class PadronSantaFeIIBB(ModeloBaseGenerico):
    id_padron = models.AutoField(primary_key=True)
    
    fecha_publicacion = models.DateField(verbose_name="Fecha publicación")
    fecha_vigencia_desde = models.DateField(verbose_name="Vigencia desde")
    fecha_vigencia_hasta = models.DateField(verbose_name="Vigencia hasta")
    
    cuit = models.BigIntegerField(verbose_name="CUIT", db_index=True)
    tipo_contr_insc = models.CharField(
        max_length=1,
        verbose_name="Tipo contribuyente",
        choices=[('D', 'D'), ('C', 'C'), ('-', 'Sin dato')],
        blank=True,
        null=True
    )
    marca_alta_sujeto = models.BooleanField(verbose_name="Alta sujeto", default=False)
    marca_alicuota = models.BooleanField(verbose_name="Aplica alícuota", default=False)
    
    alicuota_percepcion = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name="Alícuota percepción (%)",
        default=0.00
    )
    alicuota_retencion = models.DecimalField(
        max_digits=6, decimal_places=2,
        verbose_name="Alícuota retención (%)",
        default=0.00
    )
    
    nro_grupo_percepcion = models.CharField(
        max_length=5,
        verbose_name="Nro grupo percepción",
        blank=True,
        default='0'
    )
    nro_grupo_retencion = models.CharField(
        max_length=5,
        verbose_name="Nro grupo retención",
        blank=True,
        default='0'
    )
    
    razon_social = models.CharField(
        max_length=100,
        verbose_name="Razón social"
    )
    
    id_provincia = models.ForeignKey(
        Provincia,
        on_delete=models.PROTECT,
        verbose_name="Provincia",
        default=13  # Asumiendo Santa Fe id=2
    )
    
    class Meta:
        db_table = 'padron_santa_fe'
        verbose_name = 'Padrón IIBB - Santa Fe'
        verbose_name_plural = 'Padrones IIBB - Santa Fe'
        ordering = ['-fecha_vigencia_desde', 'razon_social']
        unique_together = [['cuit', 'fecha_vigencia_desde']]
    
    def __str__(self):
        return f"{self.cuit} - {self.razon_social}"
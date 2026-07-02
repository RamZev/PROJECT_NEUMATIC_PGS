# neumatic\apps\maestros\models\valida_models.py
from django.db import models
from django.utils import timezone

from .base_gen_models import ModeloBaseGenerico
from .base_models import ComprobanteVenta
from .sucursal_models import Sucursal
from .cliente_models import Cliente
from entorno.constantes_base import ESTATUS_GEN, MOTIVO_AUTORIZACION


class Valida(ModeloBaseGenerico):
	id_valida = models.AutoField(
		primary_key=True
	)
	estatus_valida = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	id_sucursal = models.ForeignKey(
		Sucursal,
		on_delete=models.CASCADE,
		verbose_name="Sucursal*",
		null=True, 
		blank=True,
	)
	fecha_valida = models.DateField(
		verbose_name='Fecha',
		blank=True,
		null=True
	)
	hora_valida = models.TimeField(
		verbose_name='Hora',
		blank=True,
		null=True
	)
	solicitado = models.CharField(
		verbose_name='Solicitado por',
		max_length=20
	)
	comentario = models.CharField(
		verbose_name='Comentario',
		max_length=50,
		blank=True,
		null=True
	)
	id_cliente = models.ForeignKey(
		Cliente,
		on_delete=models.PROTECT,
		verbose_name="Cliente",
		null=True,
		blank=True
	)
	id_comprobante_venta = models.ForeignKey(
        ComprobanteVenta,
        on_delete=models.PROTECT,
        verbose_name="Comprobante*",
        null=True,
        blank=True,
        limit_choices_to={
            'estatus_comprobante_venta': True,
			'tipo_comprobante__in': ["REMITO", "FACTURA", "NOTA DE CRÉDITO"]
        }
    )
	numero_comprobante = models.IntegerField(
		verbose_name="Número",
		null=True,
		blank=True
	)
	hs = models.TimeField(
		verbose_name='Hora Aplicación',
		null=True,
		blank=True
	)
	validacion = models.CharField(
		verbose_name='Validación',
		max_length=4,
		blank=True,
		null=True
	)
	motivo = models.CharField(
		verbose_name="Motivo de autorización",
		max_length=20,
		choices=MOTIVO_AUTORIZACION,
		blank=True,
		null=True,
		help_text="Razón por la que se emitió la autorización (Vencimiento o Límite de crédito)"
	)	
	
	class Meta:
		verbose_name = 'Validación'
		verbose_name_plural = 'Validaciones'
		db_table = 'valida'
	
	def __str__(self):
		return f"{self.id_comprobante_venta}-{self.numero_comprobante} ({self.fecha_valida})"  # Corregido
	
	@property
	def cliente_id(self):
		"""Devuelve el ID del cliente para mostrar en la lista"""
		return self.id_cliente.id_cliente if self.id_cliente else ''
	
	def save(self, *args, **kwargs):
		#-- Asigna fecha y hora actual solo si no tienen valor (o siempre, según tu necesidad).
		if not self.fecha_valida:
			self.fecha_valida = timezone.now().date()
		if not self.hora_valida:
			self.hora_valida = timezone.now().time()
		
		#-- Llama al método save() de la clase padre para guardar el objeto.
		super().save(*args, **kwargs)

# neumatic\apps\maestros\models\descuento_vendedor_models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

from .base_gen_models import ModeloBaseGenerico
from .base_models import ProductoMarca, ProductoFamilia
from entorno.constantes_base import ESTATUS_GEN


class DescuentoVendedor(ModeloBaseGenerico):
	id_descuento_vendedor = models.AutoField(
		primary_key=True
	)
	estatus_descuento_vendedor = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	id_marca = models.ForeignKey(
		ProductoMarca,
		on_delete=models.PROTECT,
		verbose_name="Marca"
	)
	id_familia = models.ForeignKey(
		ProductoFamilia,
		on_delete=models.PROTECT,
		verbose_name="Familia"
	)
	desc1 = models.DecimalField(
		verbose_name="Desc. Col1",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc2 = models.DecimalField(
		verbose_name="Desc. Col2",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc3 = models.DecimalField(
		verbose_name="Desc. Col3",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc4 = models.DecimalField(
		verbose_name="Desc. Col4",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc5 = models.DecimalField(
		verbose_name="Desc. Col5",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc6 = models.DecimalField(
		verbose_name="Desc. Col6",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc7 = models.DecimalField(
		verbose_name="Desc. Col7",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc8 = models.DecimalField(
		verbose_name="Desc. Col8",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc9 = models.DecimalField(
		verbose_name="Desc. Col9",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc10 = models.DecimalField(
		verbose_name="Desc. Col10",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc11 = models.DecimalField(
		verbose_name="Desc. Col11",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc12 = models.DecimalField(
		verbose_name="Desc. Col12",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc13 = models.DecimalField(
		verbose_name="Desc. Col13",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc14 = models.DecimalField(
		verbose_name="Desc. Col14",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc15 = models.DecimalField(
		verbose_name="Desc. Col15",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc16 = models.DecimalField(
		verbose_name="Desc. Col16",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc17 = models.DecimalField(
		verbose_name="Desc. Col17",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc18 = models.DecimalField(
		verbose_name="Desc. Col18",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc19 = models.DecimalField(
		verbose_name="Desc. Col19",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc20 = models.DecimalField(
		verbose_name="Desc. Col20",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc21 = models.DecimalField(
		verbose_name="Desc. Col21",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc22 = models.DecimalField(
		verbose_name="Desc. Col22",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc23 = models.DecimalField(
		verbose_name="Desc. Col23",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc24 = models.DecimalField(
		verbose_name="Desc. Col24",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	desc25 = models.DecimalField(
		verbose_name="Desc. Col25",
		max_digits=4,
		decimal_places=2,
		null=True, blank=True,
		validators=[MinValueValidator(0.00),
					MaxValueValidator(99.99)])
	
	class Meta:
		db_table = 'descuento_vendedor'
		verbose_name = 'Descuento Vendedor'
		verbose_name_plural = 'Descuentos Vendedor'
		ordering = ['id_marca', 'id_familia']
		unique_together = ['id_marca', 'id_familia']
		constraints = [
			models.UniqueConstraint(
				fields=['id_marca', 'id_familia'],
				name='unique_marca_familia_vendedor',
				violation_error_message="Ya existe una configuración de descuento para esta combinación de Marca y Familia."
			)
		]
	
	def __str__(self):
		return f'{self.id_marca} - {self.id_familia}'


class DescuentoRevendedor(ModeloBaseGenerico):
	id_descuento_revendedor = models.AutoField(
		primary_key=True
	)
	estatus_descuento_revendedor = models.BooleanField(
		verbose_name="Estatus", default=True,
		choices=ESTATUS_GEN
	)
	id_marca = models.ForeignKey(
		ProductoMarca,
		on_delete=models.PROTECT,
		verbose_name="Marca"
	)
	id_familia = models.ForeignKey(
		ProductoFamilia,
		on_delete=models.PROTECT,
		verbose_name="Familia"
	)
	descuento = models.DecimalField(
		verbose_name="Descuento",
		max_digits=4,
		decimal_places=2,
		null=True,
		blank=True,
		validators=[MinValueValidator(Decimal('0.01')),
					MaxValueValidator(Decimal('99.99'))]
	)
	
	class Meta:
		db_table = 'descuento_revendedor'
		verbose_name = 'Descuento Revendedor'
		verbose_name_plural = 'Descuentos Revendedores'
		ordering = ['id_marca', 'id_familia']
		unique_together = ['id_marca', 'id_familia']
		constraints = [
			models.UniqueConstraint(
				fields=['id_marca', 'id_familia'],
				name='unique_marca_familia_revendedor',
				violation_error_message="Ya existe una configuración de descuento para esta combinación de Marca y Familia."
			)
		]
	
	def __str__(self):
		return f'{self.id_marca} - {self.id_familia}'


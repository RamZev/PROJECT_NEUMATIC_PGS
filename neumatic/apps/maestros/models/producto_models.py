# neumatic\apps\maestros\models\producto_models.py
from django.db import models
from django.core.exceptions import ValidationError
import re
from django.utils import timezone

from .base_gen_models import ModeloBaseGenerico
from .base_models import (ProductoFamilia, ProductoMarca, ProductoModelo, ProductoCai, 
						  AlicuotaIva, ProductoDeposito, ProductoStock, ProductoMinimo)
from entorno.constantes_base import ESTATUS_GEN, TIPO_PRODUCTO_SERVICIO


class Producto(ModeloBaseGenerico):
	id_producto = models.AutoField(
		primary_key=True
	)
	estatus_producto = models.BooleanField(
		verbose_name="Estatus", default=True,
		choices=ESTATUS_GEN
	)
	codigo_producto = models.CharField(
		verbose_name="Código producto",
		max_length=7,
		null=True,
		blank=True
	)
	tipo_producto = models.CharField(
		verbose_name="Tipo producto",
		max_length=1,
		choices=TIPO_PRODUCTO_SERVICIO
	)
	id_familia = models.ForeignKey(
		ProductoFamilia,
		on_delete=models.PROTECT,
		verbose_name="Familia"
	)
	id_marca = models.ForeignKey(
		ProductoMarca,
		on_delete=models.PROTECT,
		verbose_name="Marca"
	)
	id_modelo = models.ForeignKey(
		ProductoModelo,
		on_delete=models.PROTECT,
		verbose_name="Modelo"
	)
	id_cai = models.ForeignKey(
		ProductoCai,
		on_delete=models.PROTECT,
		verbose_name="CAI",
		null=True,
		blank=True,
	)
	cai = models.CharField(
		verbose_name="CAI.",
		max_length=21,
		null=True,
		blank=True
	)
	medida = models.CharField(
		verbose_name="Medida",
		max_length=15
	)
	segmento = models.CharField(
		verbose_name="Segmento",
		max_length=3
	)
	nombre_producto = models.CharField(
		verbose_name="Nombre producto",
		max_length=50
	)
	unidad = models.IntegerField(
		verbose_name="Unidad",
		null=True,
		blank=True,
		default=0
	)
	fecha_fabricacion = models.CharField(
		verbose_name="Fecha fabricación",
		max_length=6,
		null=True,
		blank=True
	)
	costo = models.DecimalField(
		verbose_name="Costo",
		max_digits=15,
		decimal_places=2,
		default=0.00,
		null=True,
		blank=True
	)
	alicuota_iva = models.DecimalField(
		verbose_name="Alícuota IVA",
		max_digits=4,
		decimal_places=2,
		default=0.00,
		null=True,
		blank=True
	)
	id_alicuota_iva = models.ForeignKey(
		AlicuotaIva,
		on_delete=models.PROTECT,
		verbose_name="Alíc. IVA",
		default=1
	)
	precio = models.DecimalField(
		verbose_name="Precio",
		max_digits=15,
		decimal_places=2,
		default=0.00,
		null=True,
		blank=True
	)
	stock = models.IntegerField(
		verbose_name="Stock",
		null=True,
		blank=True,
		default=0
	)
	minimo = models.IntegerField(
		verbose_name="Stock mínimo",
		null=True,
		default=0
	)
	descuento = models.DecimalField(
		verbose_name="Descuento",
		max_digits=4,
		decimal_places=2,
		default=0.00,
		null=True,
		blank=True
	)
	despacho_1 = models.CharField(
		verbose_name="Despacho 1",
		max_length=16,
		null=True,
		blank=True
	)
	despacho_2 = models.CharField(
		verbose_name="Despacho 2",
		max_length=16,
		null=True,
		blank=True
	)
	descripcion_producto = models.CharField(
		verbose_name="Descripción",
		max_length=50
	)
	carrito = models.BooleanField(
		verbose_name="Carrito",
		default=False
	)
	iva_exento = models.BooleanField(
		verbose_name="IVA Exento",
		default=False
	)
	obliga_operario = models.BooleanField(
		verbose_name="Obliga Operario",
		default=False
	)
	id_producto_estado = models.ForeignKey(
		'ProductoEstado',
		on_delete=models.PROTECT,
		verbose_name="Estado",
		default=1,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = 'producto'
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
		ordering = ['nombre_producto']
	
	def __str__(self):
		return self.nombre_producto
	
	def save(self, *args, **kwargs):
		#-- Identificar si el registro es nuevo antes de llamar a super().
		es_nuevo = self.pk is None
		
		#-- Llamar al método save original para que se guarde el registro y se asigne el ID.
		super().save(*args, **kwargs)
		
		#-- Si no tiene código, asigna el ID con ceros a la izquierda.
		if not self.codigo_producto:
			self.codigo_producto = f'{self.id_producto:07d}'  # 7 dígitos con ceros a la izquierda
		
		#-- Solo procesar stock y mínimo si es nuevo y es producto.
		if es_nuevo and self.tipo_producto.upper() == 'P':
			self._crear_registros_stock_y_minimo()		
		
	def _crear_registros_stock_y_minimo(self):
		"""Método auxiliar para crear registros de stock y mínimo"""
		
		#-- Obtén todos los depósitos.
		depositos = ProductoDeposito.objects.all()
		
		#-- Crear registros de stock para cada depósito.
		for deposito in depositos:
			ProductoStock.objects.get_or_create(
				id_producto=self,            # Producto actual
				id_deposito=deposito,        # Depósito en la iteración
				defaults={
					'stock': self.stock or 0,               # Valor de stock de Producto o 0
					'minimo': self.minimo or 0,             # Valor de mínimo de Producto o 0
					'fecha_producto_stock': timezone.now()  # Fecha actual
				}
			)
		
			#-- Crear registros de mínimo si tiene CAI.
			if self.id_cai:
				ProductoMinimo.objects.get_or_create(
					id_cai=self.id_cai,
					id_deposito=deposito,
					defaults={
						'minimo': self.minimo or 0
					}
				)
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		fecha_fabricacion_str = str(self.fecha_fabricacion) if self.fecha_fabricacion else ""
		unidad_str = str(self.unidad) if self.unidad else ""
		costo_str = str(self.costo) if self.costo else ""
		descuento_str = str(self.descuento) if self.descuento else ""
		tipo = self.tipo_producto
		obliga = self.obliga_operario

		if tipo != 'S' and obliga:
			errors.update({'obliga_operario': 'El campo obliga operario solo puede estar marcado para servicios.'})
		
		if not re.match(r'^$|^20\d{2}(0[1-9]|1[0-2])$', fecha_fabricacion_str):
			errors.update({'fecha_fabricacion': 'Debe indicar el dato en el formato AAAAMM (AAAA para el año, MM para el mes). Indicar año y mes válidos. El año debe iniciar en 20 o puede dejar el dato vacío.'})
		
		if not re.match(r'^[1-9]\d{0,2}$|^0$|^$', unidad_str):
			errors.update({'unidad': 'El valor debe ser un número entero positivo, con hasta 3 dígitos, o estar en blanco o cero.'})
		
		if not re.match(r'^(0|[1-9]\d{0,13})(\.\d{1,2})?$|^$', costo_str):
			errors.update({'costo': 'El valor debe ser positivo, con hasta 13 dígitos enteros y hasta 2 decimales, o estar en blanco o cero.'})
		
		if not re.match(r'^(0|[1-9]\d{0,13})(\.\d{1,2})?$|^$', descuento_str):
			errors.update({'descuento': 'El valor debe ser positivo, con hasta 13 dígitos enteros y hasta 2 decimales, o estar en blanco o cero.'})
		
		if errors:
			raise ValidationError(errors)

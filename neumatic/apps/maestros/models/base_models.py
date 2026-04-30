# neumatic\apps\maestros\models\base_models.py
from django.db import models
from django.utils.html import format_html
from django.utils.functional import cached_property
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import re

from utils.validator.validaciones import validar_cuit
from .base_gen_models import ModeloBaseGenerico
from entorno.constantes_base import (
	ESTATUS_GEN,
	CONDICION_PAGO,
	TIPO_CUENTA,
	TIPO_COMPROBANTE,
	TIPO_COMPROBANTE_COMPRA,
	TIPO_NUMERACION
)


class Actividad(ModeloBaseGenerico):
	id_actividad = models.AutoField(
		primary_key=True
	)
	estatus_actividad = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	descripcion_actividad = models.CharField(
		verbose_name="Descripción actividad",
		max_length=30
	)

	class Meta:
		db_table = 'actividad'
		verbose_name = 'Actividad'
		verbose_name_plural = 'Actividades'
		ordering = ['descripcion_actividad']
	
	def __str__(self):
		return self.descripcion_actividad


class ProductoDeposito(ModeloBaseGenerico):
	id_producto_deposito = models.AutoField(
		primary_key=True
	)
	estatus_producto_deposito = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	id_sucursal = models.ForeignKey(
		'Sucursal',
		on_delete=models.CASCADE,
		verbose_name="Sucursal"
	)
	nombre_producto_deposito = models.CharField(
		verbose_name="Nombre",
		max_length=50
	)
	
	class Meta:
		db_table = 'producto_deposito'
		verbose_name = 'Producto Depósito'
		verbose_name_plural = 'Producto Depósitos'
		ordering = ['nombre_producto_deposito']
	
	def __str__(self):
		return self.nombre_producto_deposito


class ProductoFamilia(ModeloBaseGenerico):
	id_producto_familia = models.AutoField(
		primary_key=True
	)
	estatus_producto_familia = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_producto_familia = models.CharField(
		verbose_name="Nombre",
		max_length=50
	)
	comision_operario = models.DecimalField(
		verbose_name="Comisión Operario(%)",
		max_digits=4,
		decimal_places=2,
		default=0.00,
		null=True,
		blank=True
	)
	info_michelin_auto = models.BooleanField(
		verbose_name="Info. Michelin auto",
		default=False
	)
	info_michelin_camion = models.BooleanField(
		verbose_name="Info. Michelin camión",
		default=False
	)
	
	class Meta:
		db_table = 'producto_familia'
		verbose_name = 'Familia de Producto'
		verbose_name_plural = 'Familias de Producto'
		ordering = ['nombre_producto_familia']
	
	def __str__(self):
		return self.nombre_producto_familia
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		comision_operario_str = str(self.comision_operario) if self.comision_operario else ""
		
		if not re.match(r'^(0|[1-9]\d{0,1})(\.\d{1,2})?$|^$', comision_operario_str):
			errors.update({'comision_operario': 'El valor debe ser positivo, con hasta 2 dígitos enteros y hasta 2 decimales, o estar en blanco o cero.'})
		
		if errors:
			raise ValidationError(errors)


class Moneda(ModeloBaseGenerico):
	id_moneda = models.AutoField(
		primary_key=True
	)
	estatus_moneda = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_moneda = models.CharField(
		verbose_name="Nombre",
		max_length=20
	)
	cotizacion_moneda = models.DecimalField(
		verbose_name="Cotización",
		max_digits=15,
		decimal_places=4,
		validators=[
			MinValueValidator(1),
			MaxValueValidator(99999999999.9999)
		]
	)
	simbolo_moneda = models.CharField(
		verbose_name="Símbolo",
		max_length=3
	)
	ws_afip = models.CharField(
		verbose_name="WS AFIP",
		max_length=3
	)
	predeterminada = models.BooleanField(
		verbose_name="Predeterminada",
		null=True,
		blank=True,
		default=False
	)
	
	class Meta:
		db_table = 'moneda'
		verbose_name = 'Moneda'
		verbose_name_plural = 'Monedas'
		ordering = ['nombre_moneda']
	
	def __str__(self):
		return self.nombre_moneda
	
	def clean(self):
		super().clean()
		
		#-- Diccionario contenedor de errores.
		errors = {}
		
		#-- Validación para predeterminada.
		if self.predeterminada:
			#-- Buscar si ya existe otra moneda con predeterminada = True.
			moneda_existente = Moneda.objects.filter(
				predeterminada=True
			).exclude(pk=self.pk).first()
			
			if moneda_existente:
				errors['predeterminada'] = f'Ya existe una moneda marcada como predeterminada: {moneda_existente.nombre_moneda}. Solo puede haber una moneda predeterminada a la vez.'
		
		if errors:
			raise ValidationError(errors)


class ProductoMarca(ModeloBaseGenerico):
	id_producto_marca = models.AutoField(
		primary_key=True
	)
	estatus_producto_marca = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_producto_marca = models.CharField(
		verbose_name="Nombre",
		max_length=50
	)
	principal = models.BooleanField(
		verbose_name="Principal",
		default=False
	)
	info_michelin_auto = models.BooleanField(
		verbose_name="Info. Michelin auto",
		default=False
	)
	info_michelin_camion = models.BooleanField(
		verbose_name="Info. Michelin camión",
		default=False
	)
	id_moneda = models.ForeignKey(
		Moneda,
		on_delete=models.PROTECT,
		verbose_name="Moneda"
	)
	
	class Meta:
		db_table = 'producto_marca'
		verbose_name = 'Marca de Producto'
		verbose_name_plural = 'Marcas de Producto'
		ordering = ['nombre_producto_marca']
	
	def __str__(self):
		return self.nombre_producto_marca


class ProductoModelo(ModeloBaseGenerico):
	id_modelo = models.AutoField(
		primary_key=True
	)
	estatus_modelo = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_modelo = models.CharField(
		verbose_name="Nombre",
		max_length=50
	)
	
	class Meta:
		db_table = 'producto_modelo'
		verbose_name = 'Modelo de Producto'
		verbose_name_plural = 'Modelos de Producto'
		ordering = ['nombre_modelo']
	
	def __str__(self):
		return self.nombre_modelo


class ProductoCai(ModeloBaseGenerico):
	id_cai = models.AutoField(
		primary_key=True
	)
	estatus_cai = models.BooleanField(
		verbose_name="Estatus*",
		default=True,
		choices=ESTATUS_GEN
	)
	cai = models.CharField(
		verbose_name="CAI*",
		max_length=20,
		unique=True
	)
	descripcion_cai = models.CharField(
		verbose_name="Descripción CAI",
		max_length=50,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = 'producto_cai'
		verbose_name = 'CAI'
		verbose_name_plural = 'CAIs de Productos'
		ordering = ['cai']
	
	def __str__(self):
		return self.cai
	
	@cached_property
	def nombre_producto(self):
		"""
		Retorna el nombre_producto de la primera coincidencia en el modelo Producto
		asociado al ProductoCai.
		"""
		producto = self.producto_set.first() if hasattr(self, 'producto_set') else None
		return producto.nombre_producto if producto else ''
	
	@cached_property
	def medida(self):
		"""
		Retorna la medida de la primera coincidencia en el modelo Producto
		asociado al ProductoCai.
		"""
		producto = self.producto_set.first() if hasattr(self, 'producto_set') else None
		return producto.medida if producto else ''


class ProductoMinimo(ModeloBaseGenerico):
	id_producto_minimo = models.AutoField(
		primary_key=True
	)
	id_cai = models.ForeignKey(
		ProductoCai,
		on_delete=models.PROTECT,
		verbose_name="CAI"
	)
	minimo = models.IntegerField(
		verbose_name="Mínimo",
		default=0
	)
	id_deposito = models.ForeignKey(
		'ProductoDeposito',
		on_delete=models.CASCADE,
		verbose_name="Depósito"
	)
	
	class Meta:
		db_table = 'producto_minimo'
		verbose_name = 'Producto Mínimo'
		verbose_name_plural = 'Productos Mínimos'
		ordering = ['id_producto_minimo']
		# unique_together = ['id_cai', 'id_deposito']
	
	def __str__(self):
		return f'{self.id_cai} - Min: {self.minimo}'


class ProductoStock(ModeloBaseGenerico):
	id_producto_stock = models.AutoField(
		primary_key=True
	)
	id_producto = models.ForeignKey(
		'Producto',
		on_delete=models.CASCADE,
		verbose_name="Producto"
	)
	id_deposito = models.ForeignKey(
		'ProductoDeposito',
		on_delete=models.CASCADE,
		verbose_name="Depósito"
	)
	stock = models.IntegerField(
		verbose_name="Stock",
		default=0
	)
	minimo = models.IntegerField(
		verbose_name="Mínimo",
		default=0
	)
	fecha_producto_stock = models.DateField(
		verbose_name="Fecha Stock"
	)
	
	class Meta:
		db_table = 'producto_stock'
		verbose_name = 'Producto Stock'
		verbose_name_plural = 'Productos Stock'
		ordering = ['id_producto_stock']
	
	def __str__(self):
		return f'Producto {self.id_producto} - Stock: {self.stock} - \
			Depósito: {self.id_deposito}'


class ProductoEstado(ModeloBaseGenerico):
	id_producto_estado = models.AutoField(
		primary_key=True
	)
	estatus_producto_estado = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	estado_producto = models.CharField(
		verbose_name="Estado Producto",
		max_length=1,
		unique=True
	)
	nombre_producto_estado = models.CharField(
		verbose_name="Nombre",
		max_length=15
	)
	color = models.CharField(
		max_length=7,
		default='#FFFFFF',
		blank=True,
		help_text='Código de color en formato hexadecimal (ej: #FFFFFF)'
	)
	
	class Meta:
		db_table = 'producto_estado'
		verbose_name = 'Estado de Producto'
		verbose_name_plural = 'Estados de Productos'
		ordering = ['nombre_producto_estado']
	
	def __str__(self):
		return self.nombre_producto_estado
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.estado_producto.isupper():
			errors.update({'estado_producto': 'Debe ingresar solo mayúsculas.'})
		
		if errors:
			raise ValidationError(errors)
	
	@property
	def color_bar(self):
		return format_html(
			f'<div style="width:200px; height:20px; background-color:{self.color}; border: 1px solid #000;"></div>'
		)
	

class ComprobanteVenta(ModeloBaseGenerico):
	id_comprobante_venta = models.AutoField(
		primary_key=True
	)
	estatus_comprobante_venta = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	codigo_comprobante_venta = models.CharField(
		verbose_name="Cód. Comprobante",
		max_length=3,
		unique=True
	)
	nombre_comprobante_venta = models.CharField(
		verbose_name="Nombre Comprobante",
		max_length=30
	)
	tipo_comprobante = models.CharField(
		verbose_name="Tipo Comprobante",
		max_length=20,
		null=True,
		blank=True,
		choices=TIPO_COMPROBANTE
	)
	tipo_numeracion = models.IntegerField(
		verbose_name="Tipo Numeración",
		null=True,
		blank=True,
		choices=TIPO_NUMERACION
	)
	compro_asociado = models.CharField(
		verbose_name="Comprobante Asociado",
		max_length=20,
		null=True,
		blank=True
	)
	mult_venta = models.IntegerField(
		verbose_name="Mult. Venta"
	)
	mult_saldo = models.IntegerField(
		verbose_name="Mult. Saldo"
	)
	mult_stock = models.IntegerField(
		verbose_name="Mult. Stock"
	)
	mult_comision = models.IntegerField(
		verbose_name="Mult. Comisión"
	)
	mult_caja = models.IntegerField(
		verbose_name="Mult. Caja"
	)
	mult_estadistica = models.IntegerField(
		verbose_name="Mult. Estadísticas"
	)
	libro_iva = models.BooleanField(
		verbose_name="Libro IVA",
		default=False
	)
	estadistica = models.BooleanField(
		verbose_name="Estadísticas",
		default=False
	)
	electronica = models.BooleanField(
		verbose_name="Electrónica",
		default=False
	)
	presupuesto = models.BooleanField(
		verbose_name="Presupuesto",
		default=False
	)
	pendiente = models.BooleanField(
		verbose_name="Pendiente",
		default=False
	)
	info_michelin_auto = models.BooleanField(
		verbose_name="Info. Michelin auto",
		default=False
	)
	info_michelin_camion = models.BooleanField(
		verbose_name="Info. Michelin camión",
		default=False
	)
	codigo_afip_a = models.CharField(
		verbose_name="Código AFIP A",
		max_length=3
	)
	codigo_afip_b = models.CharField(
		verbose_name="Código AFIP B",
		max_length=3
	)
	remito = models.BooleanField(
		verbose_name="Remito",
		default=False,
		blank=True,
		null=True
	)
	recibo = models.BooleanField(
		verbose_name="Recibo",
		default=False,
		blank=True,
		null=True
	)
	ncr_ndb = models.BooleanField(
		verbose_name="NCR/NDB",
		default=False,
		blank=True,
		null=True
	)
	manual = models.BooleanField(
		verbose_name="Manual",
		default=False,
		blank=True,
		null=True
	)
	mipyme = models.BooleanField(
		verbose_name="MiPyME",
		default=False,
		blank=True,
		null=True
	)
	interno = models.BooleanField(
		verbose_name="Interno",
		default=False,
		blank=True,
		null=True
	)
	
	class Meta:
		db_table = 'comprobante_venta'
		verbose_name = 'Comprobante de Venta'
		verbose_name_plural = 'Comprobantes de Venta'
		ordering = ['nombre_comprobante_venta']
	
	def __str__(self):
		return self.nombre_comprobante_venta
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.codigo_comprobante_venta.isupper():
			errors.update({'codigo_comprobante_venta': 'Debe ingresar solo mayúsculas.'})
		
		if not self.tipo_comprobante:
			errors.update({'tipo_comprobante': 'Debe indicar un Tipo de Comprobante.'})
		
		if self.mult_venta != -1 and self.mult_venta != 0 and self.mult_venta != 1:
			errors.update({'mult_venta': "Los valores permitidos son: -1, 0 y 1"})
		
		if self.mult_saldo != -1 and self.mult_saldo != 0 and self.mult_saldo != 1:
			errors.update({'mult_saldo': "Los valores permitidos son: -1, 0 y 1"})
		
		if self.mult_stock != -1 and self.mult_stock != 0 and self.mult_stock != 1:
			errors.update({'mult_stock': "Los valores permitidos son: -1, 0 y 1"})
		
		if self.mult_comision != -1 and self.mult_comision != 0 and self.mult_comision != 1:
			errors.update({'mult_comision': "Los valores permitidos son: -1, 0 y 1"})
		
		if self.mult_caja != -1 and self.mult_caja != 0 and self.mult_caja != 1:
			errors.update({'mult_caja': "Los valores permitidos son: -1, 0 y 1"})
		
		if self.mult_estadistica != -1 and self.mult_estadistica != 0 and self.mult_estadistica != 1:
			errors.update({'mult_estadistica': "Los valores permitidos son: -1, 0 y 1"})
		
		#-- VALIDACIÓN PARA CÓDIGOS AFIP.
		if self.libro_iva:
			#-- Si libro_iva está activado, validar que los códigos sean diferentes.
			if self.codigo_afip_a == self.codigo_afip_b:
				errors.update({'codigo_afip_b': 'Los códigos AFIP A y B deben ser diferentes cuando Libro IVA está activado.'})
		else:
			#-- Si libro_iva NO está activado, forzar que codigo_afip_b sea igual a codigo_afip_a.
			self.codigo_afip_b = self.codigo_afip_a
		
		#-- VALIDACIÓN PARA COMPROBANTES ASOCIADOS.
		if self.compro_asociado:
			#-- Separar los códigos por coma y eliminar espacios.
			codigos = [codigo.strip() for codigo in self.compro_asociado.split(',')]
			
			#-- Verificar que cada código exista en la base de datos.
			for codigo in codigos:
				if codigo:
					if not ComprobanteVenta.objects.filter(
						codigo_comprobante_venta=codigo
					).exists():
						errors.update({
							'compro_asociado': f'El código "{codigo}" no existe en los comprobantes de venta. Debe indicar valores separados por una coma (,).'
						})
						break
		
		if errors:
			raise ValidationError(errors)


class ComprobanteCompra(ModeloBaseGenerico):
	id_comprobante_compra = models.AutoField(
		primary_key=True
	)
	estatus_comprobante_compra = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	codigo_comprobante_compra = models.CharField(
		verbose_name="Código comprobante",
		max_length=3,
		unique=True
	)
	nombre_comprobante_compra = models.CharField(
		verbose_name="Nombre",
		max_length=30
	)
	nombre_impresion = models.CharField(
		verbose_name="Nombre Impresión",
		max_length=20,
		null=True,
		blank=True,
		choices=TIPO_COMPROBANTE_COMPRA
	)
	mult_compra = models.IntegerField(
		verbose_name="Mult. Compra"
	)
	mult_saldo = models.IntegerField(
		verbose_name="Mult. Saldo"
	)
	mult_stock = models.IntegerField(
		verbose_name="Mult. Stock"
	)
	mult_caja = models.IntegerField(
		verbose_name="Mult. IVA"
	)
	libro_iva = models.BooleanField(
		verbose_name="Libro IVA",
		default=False
	)
	codigo_afip_a = models.CharField(
		verbose_name="Código AFIP A",
		max_length=3
	)
	codigo_afip_b = models.CharField(
		verbose_name="Código AFIP B",
		max_length=3
	)
	codigo_afip_c = models.CharField(
		verbose_name="Código AFIP C",
		max_length=3
	)
	codigo_afip_m = models.CharField(
		verbose_name="Código AFIP M",
		max_length=3
	)
	remito = models.BooleanField(
		verbose_name="Remito",
		default=False,
		blank=True,
		null=True
	)
	retencion = models.BooleanField(
		verbose_name="Retención",
		default=False,
		blank=True,
		null=True
	)
	
	class Meta:
		db_table = 'comprobante_compra'
		verbose_name = 'Comprobante de Compra'
		verbose_name_plural = 'Comprobantes de Compra'
		ordering = ['nombre_comprobante_compra']
	
	def __str__(self):
		return self.nombre_comprobante_compra
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.codigo_comprobante_compra.isupper():
			errors.update({'codigo_comprobante_compra': 'Debe ingresar solo mayúsculas.'})
		
		if not self.nombre_impresion:
			errors.update({'nombre_impresion': 'Debe indicar un Nombre de Impresión.'})
		
		if self.mult_compra != -1 and self.mult_compra != 0 and self.mult_compra != 1:
			errors.update({"mult_compra": "Los valores permitidos son: -1, 0 y 1"})
		
		if self.mult_saldo != -1 and self.mult_saldo != 0 and self.mult_saldo != 1:
			errors.update({"mult_saldo": "Los valores permitidos son: -1, 0 y 1"})
		
		if self.mult_stock != -1 and self.mult_stock != 0 and self.mult_stock != 1:
			errors.update({"mult_stock": "Los valores permitidos son: -1, 0 y 1"})
		
		if self.mult_caja != -1 and self.mult_caja != 0 and self.mult_caja != 1:
			errors.update({"mult_caja": "Los valores permitidos son: -1, 0 y 1"})
		
		if errors:
			raise ValidationError(errors)


class Provincia(ModeloBaseGenerico):
	id_provincia = models.AutoField(
		primary_key=True
	)
	estatus_provincia = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	codigo_provincia = models.CharField(
		verbose_name="Código",
		max_length=2,
		unique=True
	)
	nombre_provincia = models.CharField(
		verbose_name="Nombre",
		max_length=30
	)
	
	class Meta:
		db_table = 'provincia'
		verbose_name = 'Provincia'
		verbose_name_plural = 'Provincias'
		ordering = ['nombre_provincia']
	
	def __str__(self):
		return self.nombre_provincia


class Localidad(ModeloBaseGenerico):
	id_localidad = models.AutoField(
		primary_key=True
	)
	estatus_localidad = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_localidad = models.CharField(
		verbose_name="Nombre Localidad",
		max_length=50
	)
	codigo_postal = models.CharField(
		verbose_name="Código Postal",
		max_length=5
	)
	id_provincia = models.ForeignKey(
		'Provincia',
		on_delete=models.CASCADE,
		verbose_name="Provincia"
	)
	
	class Meta:
		db_table = 'localidad'
		verbose_name = 'Localidad'
		verbose_name_plural = 'Localidades'
		ordering = ['codigo_postal']
	
	def __str__(self):
		return self.nombre_localidad


class TipoDocumentoIdentidad(ModeloBaseGenerico):
	id_tipo_documento_identidad = models.AutoField(
		primary_key=True
	)
	estatus_tipo_documento_identidad = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_documento_identidad = models.CharField(
		verbose_name="Nombre",
		max_length=20
	)
	tipo_documento_identidad = models.CharField(
		verbose_name="Tipo",
		max_length=4,
		unique=True
	)
	codigo_afip = models.CharField(
		verbose_name="Código AFIP",
		max_length=2
	)
	ws_afip = models.CharField(
		verbose_name="WS AFIP",
		max_length=2
	)
	
	class Meta:
		db_table = 'tipo_documento_identidad'
		verbose_name = 'Tipo de Documento de Identidad'
		verbose_name_plural = 'Tipos de Documentos de Identidad'
		ordering = ['tipo_documento_identidad']
	
	def __str__(self):
		return self.nombre_documento_identidad


class TipoIva(ModeloBaseGenerico):
	id_tipo_iva = models.AutoField(
		primary_key=True
	)
	estatus_tipo_iva = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	codigo_iva = models.CharField(
		verbose_name="Código IVA",
		max_length=4,
		unique=True
	)
	nombre_iva = models.CharField(
		verbose_name="Nombre",
		max_length=25
	)
	discrimina_iva = models.BooleanField(
		verbose_name="Discrimina IVA",
		null=True,
		blank=True
	)
	codigo_afip_responsable = models.IntegerField(
		verbose_name="Cód. AFIP",
		unique=True,
		null=True,
		blank=True,
		default=0
	)
	
	class Meta:
		db_table = 'tipo_iva'
		verbose_name = 'Tipo de IVA'
		verbose_name_plural = 'Tipos de IVA'
		ordering = ['nombre_iva']
	
	def __str__(self):
		return self.nombre_iva
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.codigo_iva.isupper():
			errors.update({'codigo_iva': 'Debe ingresar solo mayúsculas.'})
		
		if errors:
			raise ValidationError(errors)


class TipoPercepcionIb(ModeloBaseGenerico):
	id_tipo_percepcion_ib = models.AutoField(
		primary_key=True
	)
	estatus_tipo_percepcion_ib = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	descripcion_tipo_percepcion_ib = models.CharField(
		verbose_name="Descripción",
		max_length=50
	)
	alicuota = models.DecimalField(
		verbose_name="Alícuota(%)",
		max_digits=4,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	monto = models.DecimalField(
		verbose_name="Monto",
		max_digits=15,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	minimo = models.DecimalField(
		verbose_name="Mínimo",
		max_digits=15,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	neto_total = models.BooleanField(
		verbose_name="Neto total",
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = 'tipo_percepcion_ib'
		verbose_name = 'Tipo de Percepción IB'
		verbose_name_plural = 'Tipos de Percepción IB'
		ordering = ['descripcion_tipo_percepcion_ib']
	
	def __str__(self):
		return self.descripcion_tipo_percepcion_ib
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		alicuota_str = str(self.alicuota) if self.alicuota is not None else ""
		monto_str = str(self.monto) if self.monto is not None else ""
		minimo_str = str(self.minimo) if self.minimo is not None else ""
		
		if not re.match(r'^(0|[1-9]\d{0,1})(\.\d{1,2})?$', alicuota_str):
			errors.update({'alicuota': 'El valor debe ser positivo, con hasta 2 dígitos enteros y hasta 2 decimales o cero.'})
		
		if not re.match(r'^(0|[1-9]\d{0,13})(\.\d{1,2})?$', monto_str):
			errors.update({'monto': 'El valor debe ser positivo, con hasta 13 dígitos enteros y hasta 2 decimales o cero.'})
		
		if not re.match(r'^(0|[1-9]\d{0,13})(\.\d{1,2})?$', minimo_str):
			errors.update({'minimo': 'El valor debe ser positivo, con hasta 13 dígitos enteros y hasta 2 decimales o cero.'})
		
		if errors:
			raise ValidationError(errors)


class TipoRetencionIb(ModeloBaseGenerico):
	id_tipo_retencion_ib = models.AutoField(
		primary_key=True
	)
	estatus_tipo_retencion_ib = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	descripcion_tipo_retencion_ib = models.CharField(
		verbose_name="Descripción",
		max_length=50
	)
	alicuota_inscripto = models.DecimalField(
		verbose_name="Alícuota Inscripto(%)",
		max_digits=4,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	alicuota_no_inscripto = models.DecimalField(
		verbose_name="Alícuota No Inscripto(%)",
		max_digits=4,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	monto = models.DecimalField(
		verbose_name="Monto",
		max_digits=15,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	minimo = models.DecimalField(
		verbose_name="Mínimo",
		max_digits=15,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	
	class Meta:
		db_table = 'tipo_retencion_ib'
		verbose_name = 'Tipo de Retención IB'
		verbose_name_plural = 'Tipos de Retención IB'
		ordering = ['descripcion_tipo_retencion_ib']
	
	def __str__(self):
		return self.descripcion_tipo_retencion_ib
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		alicuota_inscripto_str = str(self.alicuota_inscripto) if self.alicuota_inscripto is not None else ""
		alicuota_no_inscripto_str = str(self.alicuota_no_inscripto) if self.alicuota_no_inscripto is not None else ""
		monto_str = str(self.monto) if self.monto is not None else ""
		minimo_str = str(self.minimo) if self.minimo is not None else ""
		
		if not re.match(r'^(0|[1-9]\d{0,1})(\.\d{1,2})?$', alicuota_inscripto_str):
			errors.update({'alicuota_inscripto': 'El valor debe ser positivo, con hasta 2 dígitos enteros y hasta 2 decimales o cero.'})
		
		if not re.match(r'^(0|[1-9]\d{0,1})(\.\d{1,2})?$', alicuota_no_inscripto_str):
			errors.update({'alicuota_no_inscripto': 'El valor debe ser positivo, con hasta 2 dígitos enteros y hasta 2 decimales o cero.'})
		
		if not re.match(r'^(0|[1-9]\d{0,13})(\.\d{1,2})?$', monto_str):
			errors.update({'monto': 'El valor debe ser positivo, con hasta 13 dígitos enteros y hasta 2 decimales o cero.'})
		
		if not re.match(r'^(0|[1-9]\d{0,13})(\.\d{1,2})?$', minimo_str):
			errors.update({'minimo': 'El valor debe ser positivo, con hasta 13 dígitos enteros y hasta 2 decimales o cero.'})
		
		if errors:
			raise ValidationError(errors)


class Operario(ModeloBaseGenerico):
	id_operario = models.AutoField(
		primary_key=True
	)
	estatus_operario = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_operario = models.CharField(
		verbose_name="Nombre",
		max_length=50
	)
	telefono_operario = models.CharField(
		verbose_name="Teléfono",
		max_length=15
	)
	email_operario = models.CharField(
		verbose_name="Correo",
		max_length=50
	)
	
	class Meta:
		db_table = 'operario'
		verbose_name = 'Operario'
		verbose_name_plural = 'Operarios'
		ordering = ['nombre_operario']
	
	def __str__(self):
		return self.nombre_operario
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.nombre_operario:
			errors.update({'nombre_operario': "Debe indicar un Nombre de Operario."})
		
		if errors:
			raise ValidationError(errors)


class MedioPago(ModeloBaseGenerico):
	id_medio_pago = models.AutoField(
		primary_key=True
	)
	estatus_medio_pago = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_medio_pago = models.CharField(
		verbose_name="Nombre",
		max_length=30
	)
	condicion_medio_pago = models.IntegerField(
		verbose_name="Condición Pago",
		default=True,
		choices=CONDICION_PAGO
	)
	plazo_medio_pago = models.IntegerField(
		verbose_name="Plazo medio de Pago",
		default=0
	)
	
	class Meta:
		db_table = 'medio_pago'
		verbose_name = 'Medio de Pago'
		verbose_name_plural = 'Medios de Pago'
		ordering = ['nombre_medio_pago']
	
	def __str__(self):
		return self.nombre_medio_pago
	
	@property
	def condicion_medio_pago_display(self):
		return self.get_condicion_medio_pago_display()


class PuntoVenta(ModeloBaseGenerico):
	id_punto_venta = models.AutoField(
		primary_key=True
	)
	estatus_punto_venta = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	id_sucursal = models.ForeignKey(
		'Sucursal',
		on_delete=models.PROTECT,
		verbose_name="Sucursal",
		null=True, blank=True
	)
	punto_venta = models.CharField(
		verbose_name="Punto de Venta",
		max_length=5
	)
	descripcion_punto_venta = models.CharField(
		verbose_name="Descripción Pto. Venta",
		max_length=50,
		null=True, blank=True
	)
	
	class Meta:
		db_table = 'punto_venta'
		verbose_name = 'Punto de Venta'
		verbose_name_plural = 'Puntos de Venta'
		ordering = ['punto_venta']
	
	def __str__(self):
		return f'{self.id_sucursal} {self.punto_venta}'
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		#-- Limpiar y formatear el valor de `punto_venta` con ceros a la izquierda.
		if self.punto_venta:
			try:
				#-- Convertir a entero y luego a string para evitar ceros iniciales no deseados.
				self.punto_venta = str(int(self.punto_venta)).zfill(5)
			except ValueError:
				errors.update({'punto_venta': 'Debe ser un número entero positivo.'})
		
		#-- Validar el formato después de formatear el valor.
		if not re.match(r'^\d{5}$', self.punto_venta):
			errors.update({'punto_venta': 'Debe indicar un número de hasta 5 dígitos.'})
		
		if errors:
			raise ValidationError(errors)


class AlicuotaIva(ModeloBaseGenerico):
	id_alicuota_iva = models.AutoField(
		primary_key=True
	)
	estatus_alicuota_iva = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	codigo_alicuota = models.CharField(
		verbose_name="Cód. Alíc. IVA",
		max_length=4,
		unique=True
	)
	alicuota_iva = models.DecimalField(
		verbose_name="Alícuota IVA(%)",
		unique=True,
		max_digits=5,
		decimal_places=2,
		default=0.0
	)
	descripcion_alicuota_iva = models.CharField(
		verbose_name="Descripción Alíc. IVA",
		max_length=50,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = 'codigo_alicuota'
		verbose_name = 'Alícuota IVA'
		verbose_name_plural = 'Alícuotas IVA'
		ordering = ['alicuota_iva']
	
	def __str__(self):
		return f"{self.alicuota_iva:3.2f}%"
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		#-- Limpiar y formatear el valor de `codigo_alicuota` con ceros a la izquierda.
		if self.codigo_alicuota:
			try:
				#-- Convertir a entero y luego a string para evitar ceros iniciales no deseados.
				self.codigo_alicuota = str(int(self.codigo_alicuota)).zfill(4)
			except ValueError:
				errors.update({'codigo_alicuota': 'Debe ser un número entero positivo.'})
		
		#-- Validar el formato después de formatear el valor.
		if not re.match(r'^\d{4}$', self.codigo_alicuota):
			errors.update({'codigo_alicuota': 'Debe indicar un número de hasta 4 dígitos.'})
		
		if errors:
			raise ValidationError(errors)


class Banco(ModeloBaseGenerico):
	id_banco = models.AutoField(
		primary_key=True
	)
	estatus_banco = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_banco = models.CharField(
		verbose_name="Nombre Banco",
		max_length=50,
		null=True,
		blank=True
	)
	codigo_banco = models.SmallIntegerField(
		verbose_name="Código Banco",
		null=True,
		blank=True,
		default=0
	)
	cuit_banco = models.IntegerField(
		verbose_name="CUIT",
		null=True,
		blank=True,
		default=0
	)
	
	class Meta:
		db_table = 'banco'
		verbose_name = 'Banco'
		verbose_name_plural = 'Bancos'
		ordering = ['nombre_banco']
	
	def __str__(self):
		return self.nombre_banco
	
	def clean(self):
		super().clean()
		
		#-- Diccionario contenedor de errores.
		errors = {}
		
		try:
			validar_cuit(self.cuit_banco)
		except ValidationError as e:
			#-- Agrego el error al dicciobario errors.
			errors['cuit_banco'] = e.messages
		
		if not self.nombre_banco:
			errors.update({'nombre_banco': "Debe indicar un Nombre de Banco."})
		
		if errors:
			#-- Lanza el conjunto de excepciones.
			raise ValidationError(errors)


class CuentaBanco(ModeloBaseGenerico):
	id_cuenta_banco = models.AutoField(
		primary_key=True
	)
	estatus_cuenta_banco = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	id_banco = models.ForeignKey(
		Banco,
		on_delete=models.PROTECT,
		verbose_name="Banco",
		null=True,
		blank=True
	)
	numero_cuenta = models.CharField(
		verbose_name="Número Cuenta",
		max_length=15,
		null=True,
		blank=True
	)
	tipo_cuenta = models.SmallIntegerField(
		verbose_name="Tipo de Cta.",
		choices=TIPO_CUENTA,
		null=True,
		blank=True,
		default=0
	)
	cbu = models.CharField(
		verbose_name="CBU",
		max_length=22,
		null=True,
		blank=True
	)
	sucursal = models.IntegerField(
		verbose_name="Sucursal",
		null=True,
		blank=True,
		default=0
	)
	codigo_postal = models.IntegerField(
		verbose_name="Código Postal",
		null=True,
		blank=True,
		default=0
	)
	codigo_imputacion = models.IntegerField(
		verbose_name="Cód. Imputación",
		null=True,
		blank=True,
		default=0
	)
	tope_negociacion = models.DecimalField(
		verbose_name="Tope Negociación",
		max_digits=12,
		decimal_places=2,
		null=True,
		blank=True,
		default=0.00
	)
	reporte_reques = models.CharField(
		verbose_name="Reporte Cheques",
		max_length=20,
		null=True,
		blank=True
	)
	id_proveedor = models.ForeignKey(
		"Proveedor",
		on_delete=models.PROTECT,
		verbose_name="Proveedor",
		null=True,
		blank=True
	)
	id_moneda = models.ForeignKey(
		Moneda,
		on_delete=models.PROTECT,
		verbose_name="Moneda",
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = 'cuenta_banco'
		verbose_name = 'Cuentas Banco'
		verbose_name_plural = 'Cuentas de Bancos'
		ordering = ['numero_cuenta']
	
	def __str__(self):
		return f"{self.tipo_cuenta} - {self.id_banco.nombre_banco}"
	
	def clean(self):
		super().clean()
		
		# Diccionario contenedor de errores
		errors = {}
		
		if not self.numero_cuenta:
			errors.update({'numero_cuenta': "Debe indicar un Número de Cuenta."})
		
		if not self.id_banco:
			errors.update({'id_banco': "Debe indicar un Banco."})
		
		if not self.id_moneda:
			errors.update({'id_moneda': "Debe indicar una Moneda."})
		
		if not self.tipo_cuenta:
			errors.update({'tipo_cuenta': "Debe indicar un Tipo de Cuenta."})
		
		if errors:
			#-- Lanza el conjunto de excepciones.
			raise ValidationError(errors)
	
	@property
	def tipo_cuenta_display(self):
		return self.get_tipo_cuenta_display()


class Tarjeta(ModeloBaseGenerico):
	id_tarjeta = models.AutoField(
		primary_key=True
	)
	estatus_tarjeta = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_tarjeta = models.CharField(
		verbose_name="Nombre Tarjeta",
		max_length=30,
		null=True,
		blank=True
	)
	imputacion = models.IntegerField(
		verbose_name="Cód. Imputación",
		null=True,
		blank=True,
		default=0
	)
	banco_acreditacion = models.IntegerField(
		verbose_name="Banco",
		null=True,
		blank=True
	)
	propia = models.BooleanField(
		verbose_name="Propia",
		default=False
	)
	
	class Meta:
		db_table = 'tarjeta'
		verbose_name = 'Tarjeta'
		verbose_name_plural = 'Tarjetas'
		ordering = ['nombre_tarjeta']    
	
	def __str__(self):
		return self.nombre_tarjeta
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.nombre_tarjeta:
			errors.update({'nombre_tarjeta': "Debe indicar un nombre."})
		
		if errors:
			raise ValidationError(errors)


class CodigoRetencion(ModeloBaseGenerico):
	id_codigo_retencion = models.AutoField(
		primary_key=True
	)
	estatus_cod_retencion = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_codigo_retencion = models.CharField(
		verbose_name="Nombre Cód. Ret.",
		max_length=30,
		null=True,
		blank=True
	)
	imputacion = models.IntegerField(
		verbose_name="Cód. Imputación",
		default=0,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = 'codigo_retencion'
		verbose_name = 'Codigo Retención'
		verbose_name_plural = 'Codigos Retención'
		ordering = ['nombre_codigo_retencion']
	
	def __str__(self):
		return self.nombre_codigo_retencion
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.nombre_codigo_retencion:
			errors.update({'nombre_codigo_retencion': "Debe indicar un nombre."})
		
		if errors:
			raise ValidationError(errors)


class ConceptoBanco(ModeloBaseGenerico):
	id_concepto_banco = models.AutoField(
		primary_key=True
	)
	estatus_concepto_banco = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_concepto_banco = models.CharField(
		verbose_name="Descripción",
		max_length=30,
		null=True,
		blank=True
	)
	factor = models.IntegerField(
		verbose_name="Factor"
	)
	
	class Meta:
		db_table = 'concepto_banco'
		verbose_name = 'Concepto Bancario'
		verbose_name_plural = 'Conceptos Bancarios'
		ordering = ['nombre_concepto_banco']
	
	def __str__(self):
		return self.nombre_concepto_banco
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.nombre_concepto_banco:
			errors.update({'nombre_concepto_banco': "Debe indicar un nombre."})
		
		if self.factor != -1 and self.factor != 0 and self.factor != 1:
			errors.update({'factor': "Los valores permitidos son: -1, 0 y 1"})
		
		if errors:
			raise ValidationError(errors)


class MarketingOrigen(ModeloBaseGenerico):
	id_marketing_origen = models.AutoField(
		primary_key=True
	)
	estatus_marketing_origen = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_marketing_origen = models.CharField(
		verbose_name="Descripción",
		max_length=30,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = 'marketing_origen'
		verbose_name = 'Marketing Origen'
		verbose_name_plural = 'Marketing Origen'
		ordering = ['id_marketing_origen']
	
	def __str__(self):
		return self.nombre_marketing_origen
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.nombre_marketing_origen:
			errors.update({'nombre_marketing_origen': "Debe indicar una Descripción."})
		
		if errors:
			raise ValidationError(errors)


class Leyenda(ModeloBaseGenerico):
	id_leyenda = models.AutoField(
		primary_key=True
	)
	estatus_leyenda = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	nombre_leyenda = models.CharField(
		verbose_name="Nombre",
		max_length=30,
		null=True,
		blank=True
	)
	leyenda = models.CharField(
		verbose_name="Leyenda",
		max_length=250,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = 'leyenda'
		verbose_name = 'Leyenda'
		verbose_name_plural = 'Leyendas'
		ordering = ['nombre_leyenda']
	
	def __str__(self):
		return self.nombre_leyenda


class MedidasEstados(ModeloBaseGenerico):
	id_medida_estado = models.AutoField(
		primary_key=True
	)
	estatus_medida_estado = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	id_cai = models.ForeignKey(
		ProductoCai,
		on_delete=models.PROTECT,
		verbose_name="CAI",
		null=True,
		blank=True
	)
	id_estado = models.ForeignKey(
		ProductoEstado,
		on_delete=models.PROTECT,
		verbose_name="Estado",
		null=True,
		blank=True
	)
	stock_desde = models.IntegerField(
		verbose_name="Desde Stock",
		default=0,
		null=True,
		blank=True
	)
	stock_hasta = models.IntegerField(
		verbose_name="Hasta Stock",
		default=0,
		null=True,
		blank=True
	)
	
	class Meta:
		db_table = 'medidas_estados'
		# verbose_name = 'Estado por Medida'
		# verbose_name_plural = 'Estados por Medidas'
		verbose_name = 'Estado por CAI'
		verbose_name_plural = 'Estados por CAI'
	
	def __str__(self):
		return f"{self.id_cai} - {self.medida} - {self.nombre_producto}"
	
	def clean(self):
		super().clean()
		
		errors = {}
		
		if not self.id_cai:
			errors.update({'id_cai': "Debe indicar un CAI."})
		
		if self.stock_desde and self.stock_desde < 0:
			errors.update({'stock_desde': "El valor no puede ser negativo."})
		
		if self.stock_hasta and self.stock_hasta < 0:
			errors.update({'stock_hasta': "El valor no puede ser negativo."})
		
		if self.stock_desde and self.stock_hasta and self.stock_hasta < self.stock_desde:
			errors.update({'stock_hasta': "La cantidad del Hasta Stock no puede ser menor que la del Desde Stock."})
		
		if errors:
			raise ValidationError(errors)
	
	@property
	def nombre_producto(self):
		"""
		Retorna el nombre_producto del ProductoCai asociado
		"""
		return self.id_cai.nombre_producto if self.id_cai else ''
	
	@property
	def medida(self):
		"""
		Retorna la medida del ProductoCai asociado
		"""
		return self.id_cai.medida if self.id_cai else ''


class FormaPago(ModeloBaseGenerico):
	id_forma_pago = models.AutoField(
		primary_key=True
	)
	estatus_forma_pago = models.BooleanField(
		verbose_name="Estatus",
		default=True,
		choices=ESTATUS_GEN
	)
	descripcion_forma_pago = models.CharField(
		verbose_name="Forma Pago",
		max_length=20
	)
	
	class Meta:
		db_table = 'forma_pago'
		verbose_name = 'Forma de Pago'
		verbose_name_plural = 'Formas de Pago'
		ordering = ['descripcion_forma_pago']
	
	def __str__(self):
		return self.descripcion_forma_pago
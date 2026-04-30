# neumatic\apps\maestros\models\base_models.py
from django.db import models
from .base_gen_models import ModeloBaseGenerico
from .sucursal_models import Sucursal

# -- Datos estándares aplicables a los modelos base
ESTATUS_GEN = [
    (True, 'Activo'),
    (False, 'Inactivo'),
]


class Actividad(ModeloBaseGenerico):
    id_actividad = models.AutoField(primary_key=True)
    estatus_actividad = models.BooleanField("Estatus", default=True,
                                         choices=ESTATUS_GEN)    
    descripcion_actividad = models.CharField("Descripción actividad", 
                                             max_length=30)
    fecha_registro_actividad = models.DateField("Fecha de registro")
    
    class Meta:
        db_table = 'actividad'
        verbose_name = ('Actividad')
        verbose_name_plural = ('Actividades')
        ordering = ['descripcion_actividad']


class ComprobanteCompra(ModeloBaseGenerico):
    id_comprobante_compra = models.AutoField(primary_key=True)
    estatus_comprobante_compra = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)
    codigo_comprobante_compra = models.CharField(max_length=3)
    nombre_comprobante_compra = models.CharField(max_length=30)
    mult_compra = models.IntegerField()
    mult_saldo = models.IntegerField()
    mult_stock = models.IntegerField()
    mult_caja = models.IntegerField()
    libro_iva = models.BooleanField()
    codigo_afip_a = models.CharField(max_length=3)
    codigo_afip_b = models.CharField(max_length=3)
    codigo_afip_c = models.CharField(max_length=3)
    codigo_afip_m = models.CharField(max_length=3)
    
    class Meta:
        db_table = 'comprobante_compra'
        verbose_name = 'Comprobante de Compra'
        verbose_name_plural = 'Comprobantes de Compra'
        ordering = ['nombre_comprobante_compra']


class ComprobanteVenta(ModeloBaseGenerico):
    id_comprobante_venta = models.AutoField(primary_key=True)
    estatus_comprobante_venta = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)  # Estatus del comprobante
    codigo_comprobante_venta = models.CharField(max_length=3)
    nombre_comprobante_venta = models.CharField(max_length=50)  # Nombre del comprobante
    impresion = models.CharField(max_length=50)  # Detalle de impresión
    mult_venta = models.IntegerField()  # Multiplicador de venta
    mult_saldo = models.IntegerField()  # Multiplicador de saldo
    mult_stock = models.IntegerField()  # Multiplicador de stock
    mult_comision = models.IntegerField()  # Multiplicador de comisión
    mult_caja = models.IntegerField()  # Multiplicador de caja
    mult_estadistica = models.IntegerField()  # Multiplicador de estadísticas
    libro_iva = models.BooleanField()  # Libro IVA asociado
    estadistica = models.BooleanField()  # Indicador de estadísticas
    electronica = models.BooleanField()  # Comprobante electrónico
    presupuesto = models.BooleanField()  # Presupuesto
    pendiente = models.BooleanField()  # Indicador de pendiente
    info_michelin_auto = models.BooleanField()  # Información Michelin auto
    info_michelin_camion = models.BooleanField()  # Información Michelin camión
    codigo_afip_a = models.CharField(max_length=3)  # Código AFIP A
    codigo_afip_b = models.CharField(max_length=3)  # Código AFIP B
    compro_asociado = models.CharField(max_length=20)  # Comprobante asociado

    class Meta:
        db_table = 'comprobante_venta'
        verbose_name = 'Comprobante de Venta'
        verbose_name_plural = 'Comprobantes de Venta'
        ordering = ['nombre_comprobante_venta']


class Provincia(ModeloBaseGenerico):
    id_provincia = models.AutoField(primary_key=True)
    estatus_provincia = models.BooleanField("Estatus", default=True,
                                            choices=ESTATUS_GEN)
    codigo_provincia = models.CharField(max_length=1)
    nombre_provincia = models.CharField(max_length=30)

    class Meta:
        db_table = 'provincia'
        verbose_name = ('Provincia')
        verbose_name_plural = ('Provincias')
        ordering = ['nombre_provincia']


class Localidad(ModeloBaseGenerico):
    id_localidad = models.AutoField(primary_key=True)
    estatus_localidad = models.BooleanField("Estatus", default=True,
                                            choices=ESTATUS_GEN)
    id_provincia = models.ForeignKey('Provincia', on_delete=models.CASCADE)
    codigo_postal = models.CharField(max_length=5)
    nombre_localidad = models.CharField(max_length=30)

    class Meta:
        db_table = 'localidad'
        verbose_name = ('Localidad')
        verbose_name_plural = ('Localidades')
        ordering = ['codigo_postal']
        
        
class TipoDocumentoIdentidad(ModeloBaseGenerico):
    id_tipo_documento_identidad = models.AutoField(primary_key=True)
    estatus_tipo_documento_identidad = models.BooleanField("Estatus", default=True,
                                                           choices=ESTATUS_GEN)
    nombre_documento_identidad = models.CharField(max_length=4)
    tipo_documento_identidad = models.CharField(max_length=4)
    codigo_afip = models.CharField(max_length=2)
    ws_afip = models.CharField(max_length=2)

    class Meta:
        db_table = 'tipo_documento_identidad'
        verbose_name = ('Tipo de Documento de Identidad')
        verbose_name_plural = ('Tipos de Documentos de Identidad')
        ordering = ['tipo_documento_identidad']
        
        
class TipoIva(ModeloBaseGenerico):
    id_tipo_iva = models.AutoField(primary_key=True)
    estatus_tipo_iva = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)
    codigo_iva = models.CharField(max_length=4)
    nombre_iva = models.CharField(max_length=25)
    discrimina_iva = models.BooleanField()

    class Meta:
        db_table = 'tipo_iva'
        verbose_name = ('Tipo de IVA')
        verbose_name_plural = ('Tipos de IVA')
        ordering = ['nombre_iva']
        
        
class TipoPercepcionIb(ModeloBaseGenerico):
    id_tipo_percepcion_ib = models.AutoField(primary_key=True)
    estatus_tipo_percepcion_ib = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)
    descripcion_tipo_percepcion_ib = models.CharField(max_length=50)
    alicuota = models.DecimalField(max_digits=6, decimal_places=2)
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    minimo = models.DecimalField(max_digits=18, decimal_places=2)
    neto_total = models.BooleanField()

    class Meta:
        db_table = 'tipo_percepcion_ib'
        verbose_name = ('Tipo de Percepción IB')
        verbose_name_plural = ('Tipos de Percepción IB')
        ordering = ['descripcion_tipo_percepcion_ib']
        

class TipoRetencionIb(ModeloBaseGenerico):
    id_tipo_retencion_ib = models.AutoField(primary_key=True)
    estatus_tipo_retencion_ib = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)
    descripcion_tipo_retencion_ib = models.CharField(max_length=50)
    alicuota_inscripto = models.DecimalField(max_digits=6, decimal_places=2)
    alicuota_no_inscripto = models.DecimalField(max_digits=6, decimal_places=2)
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    minimo = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'tipo_retencion_ib'
        verbose_name = ('Tipo de Retención IB')
        verbose_name_plural = ('Tipos de Retención IB')
        ordering = ['descripcion_tipo_retencion_ib']


class Moneda(ModeloBaseGenerico):
    id_moneda = models.AutoField(primary_key=True)
    estatus_moneda = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)
    nombre_moneda = models.CharField(max_length=20)
    cotizacion_moneda = models.DecimalField(max_digits=18, decimal_places=4)
    simbolo_moneda = models.CharField(max_length=3)
    ws_afip = models.CharField(max_length=3)
    predeterminada = models.BooleanField("Predeterminada", default=False)

    class Meta:
        db_table = 'moneda'
        verbose_name = ('Moneda')
        verbose_name_plural = ('Monedas')
        ordering = ['nombre_moneda']


class ProductoDeposito(ModeloBaseGenerico):
    id_producto_deposito = models.AutoField(primary_key=True)
    estatus_producto_deposito = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)
    id_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    nombre_producto_deposito = models.CharField(max_length=50)

    class Meta:
        db_table = 'producto_deposito'
        verbose_name = 'Producto Depósito'
        verbose_name_plural = 'Producto Depósitos'
        ordering = ['nombre_producto_deposito']

    def __str__(self):
        return self.nombre_producto_deposito
    
    
class ProductoEstado(ModeloBaseGenerico):
    id_producto_estado = models.AutoField(primary_key=True)
    estado_producto = models.CharField(max_length=1)
    nombre_producto_estado = models.CharField(max_length=15)
    
    class Meta:
        db_table = 'producto_estado'
        verbose_name = 'Estado de Producto'
        verbose_name_plural = 'Estados de Productos'
        ordering = ['nombre_producto_estado']

    def __str__(self):
        return self.nombre_producto_estado


class ProductoFamilia(ModeloBaseGenerico):
    id_producto_familia = models.AutoField(primary_key=True)
    estatus_producto_familia = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)
    nombre_producto_familia = models.CharField(max_length=50,null=True, 
                                    blank=True)
    comision_operario = models.DecimalField(max_digits=6, decimal_places=2,null=True, 
                                    blank=True)

    class Meta:
        db_table = 'producto_familia'
        verbose_name = ('Familia de Producto')
        verbose_name_plural = ('Familias de Producto')
        ordering = ['nombre_producto_familia']


class ProductoMarca(ModeloBaseGenerico):
    id_producto_marca = models.AutoField(primary_key=True)
    estatus_producto_marca = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)
    nombre_producto_marca = models.CharField(max_length=50,null=True, blank=True)
    principal = models.BooleanField("Principal", default=False,null=True,blank=True)
    id_moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)

    class Meta:
        db_table = 'producto_marca'
        verbose_name = ('Marca de Producto')
        verbose_name_plural = ('Marcas de Producto')
        ordering = ['nombre_producto_marca']


class ProductoMinimo(ModeloBaseGenerico):
    id_producto_minimo = models.AutoField(primary_key=True)
    cai = models.CharField(max_length=20)
    minimo = models.IntegerField()
    id_deposito = models.ForeignKey('ProductoDeposito', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'producto_minimo'
        verbose_name = 'Producto Mínimo'
        verbose_name_plural = 'Productos Mínimos'
        ordering = ['id_producto_minimo']

    def __str__(self):
        return f'{self.cai} - Min: {self.minimo}'        

        
class ProductoModelo(ModeloBaseGenerico):
    id_modelo = models.AutoField(primary_key=True)  # Clave primaria
    estatus_modelo = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)  # Estatus del modelo
    nombre_modelo = models.CharField(max_length=50, null=True,blank=True)

    class Meta:
        db_table = 'producto_modelo'
        verbose_name = 'Modelo de Producto'
        verbose_name_plural = 'Modelos de Producto'
        ordering = ['nombre_modelo']

        
class ProductoStock(ModeloBaseGenerico):
    id_producto_stock = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    id_deposito = models.ForeignKey('ProductoDeposito', on_delete=models.CASCADE)
    stock = models.IntegerField()
    minimo = models.IntegerField()
    fecha_producto_stock = models.DateField()

    class Meta:
        db_table = 'producto_stock'
        verbose_name = 'Producto Stock'
        verbose_name_plural = 'Productos Stock'
        ordering = ['id_producto_stock']

    def __str__(self):
        return f'Producto {self.id_producto} - Stock: {self.stock} - Depósito: {self.id_deposito}'


class Operario(ModeloBaseGenerico):
    id_operario = models.AutoField(primary_key=True)
    estatus_operario = models.BooleanField("Estatus", default=True,
                                           choices=ESTATUS_GEN)
    nombre_operario = models.CharField(max_length=50)
    telefono_operario = models.CharField(max_length=50)
    email_operario = models.CharField(max_length=50)

    class Meta:
        db_table = 'operario'
        verbose_name = ('Operario')
        verbose_name_plural = ('Operarios')
        ordering = ['nombre_operario']


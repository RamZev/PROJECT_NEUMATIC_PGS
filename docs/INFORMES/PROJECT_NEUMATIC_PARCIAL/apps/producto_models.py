# D:\PROJECT_NEUMATIC\neumatic\apps\maestros\models\producto_models.py
from django.db import models
from .base_gen_models import ModeloBaseGenerico
from .base_models import (ProductoFamilia, ProductoMarca,
                          ProductoModelo)

# -- Datos estándares aplicables a los modelos base
ESTATUS_GEN = [
    (True, 'Activo'),
    (False, 'Inactivo'),
]

class Producto(ModeloBaseGenerico):
    id_producto = models.AutoField(primary_key=True)
    estatus_producto = models.BooleanField("Estatus", default=True, choices=ESTATUS_GEN)  
    codigo_producto = models.CharField(max_length=10,null=True,blank=True,)
    tipo_producto = models.CharField(max_length=50,null=True, 
                                    blank=True)
    id_familia = models.ForeignKey(ProductoFamilia, on_delete=models.CASCADE, null=True, blank=True)
    id_marca = models.ForeignKey(ProductoMarca, on_delete=models.CASCADE, null=True, blank=True)
    id_modelo = models.ForeignKey(ProductoModelo, on_delete=models.CASCADE, null=True, blank=True)
    cai = models.CharField(max_length=20,null=True, 
                                    blank=True)  # CAI del producto
    medida = models.CharField(max_length=15,null=True,blank=True)  # Medida del producto
    segmento = models.CharField(max_length=3,null=True, 
                                    blank=True)  # Segmento del producto
    nombre_producto = models.CharField(max_length=50, null=True, 
                                    blank=True )  # Nombre del producto
    unidad = models.IntegerField(null=True, 
                                    blank=True)
    fecha_fabricacion = models.CharField(max_length=6,null=True, 
                                    blank=True)  # Fecha de fabricación
    costo = models.DecimalField(max_digits=18, decimal_places=2,null=True, 
                                    blank=True)  # Costo del producto
    alicuota_iva = models.DecimalField(max_digits=6, decimal_places=2,null=True, 
                                    blank=True)  # Alicuota IVA
    precio = models.DecimalField(max_digits=18, decimal_places=2,null=True, 
                                    blank=True)  # Precio del producto
    stock = models.IntegerField(null=True,blank=True,)  # Stock disponible
    minimo = models.IntegerField(null=True,blank=True,)  # Stock mínimo
    descuento = models.DecimalField(max_digits=6, decimal_places=2,null=True, 
                                    blank=True)  # Descuento aplicable
    despacho_1 = models.CharField(max_length=16,null=True, 
                                    blank=True)  # Dirección de despacho 1
    despacho_2 = models.CharField(max_length=16,null=True, 
                                    blank=True)  # Dirección de despacho 2
    descripcion_producto = models.CharField(max_length=50,null=True, 
                                    blank=True)  # Descripción del producto
    carrito = models.BooleanField(null=True,blank=True,)  # Indica si el producto está en el carrito

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre_producto']

# neumatic\apps\usuarios\models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from entorno.constantes_base import JERARQUIA, SI_NO


class User(AbstractUser):
	email = models.EmailField(
		verbose_name="Correo electrónico"
	)
	email_alt = models.EmailField(
		verbose_name="Correo alternativo",
		max_length=50,
		null=True,
		blank=True
	)
	telefono = models.CharField(
		verbose_name="Teléfono",
		max_length=15,
		null=True,
		blank=True
	)
	iniciales = models.CharField(
		verbose_name="Iniciales",
		max_length=3,
		null=True,
		blank=True
	)
	jerarquia = models.CharField(
		verbose_name="Jerarquía",
		max_length=1,
		choices=JERARQUIA,
		default="Z",
		null=True,
		blank=True
	)
	id_vendedor = models.ForeignKey(
		'maestros.Vendedor',
		on_delete=models.PROTECT,
		verbose_name="Vendedor",
		null=True,
		blank=True,
	)
	id_sucursal = models.ForeignKey(
		'maestros.Sucursal',
		on_delete=models.PROTECT,
		verbose_name="Sucursal",
		null=True,
		blank=True,
	)
	id_punto_venta = models.ForeignKey(
		'maestros.PuntoVenta',
		on_delete=models.PROTECT,
		verbose_name="Punto de Venta",
		null=True,
		blank=True,
	)
	cambia_precio_descripcion = models.BooleanField(
		verbose_name="Cambia Precio y Descripción",
		default=False,
		null=True,
		blank=True,
		choices=SI_NO
	)


#-- Al crear un nuevo usuario este quede activo por defecto.
@receiver(post_save, sender=User)
def set_user_active(sender, instance, created, **kwargs):
	if created and not instance.is_active:
		instance.is_active = True
		instance.save()

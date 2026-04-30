# neumatic\apps\maestros\signals\signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import socket
from django.db import transaction
from django.db.models import Sum

from ..models.producto_models import Producto
from ..models.base_models import (
	ProductoDeposito,
	ProductoStock,
	ProductoMinimo,
	ProductoCai,
	ProductoEstado,
	MedidasEstados
)

BATCH_SIZE = 1000  #-- Tamaño del lote para inserción masiva.


@receiver(post_save, sender=ProductoDeposito)
def trasladar_productos_a_stock_y_minimo(sender, instance, created, **kwargs):
	if created:
		
		try:
			#-- Inicia una transacción para las operaciones en el signal.
			with transaction.atomic():
				#-- Obtener el usuario autenticado.
				usuario_autenticado = instance.id_user
				nombre_usuario = usuario_autenticado.username if usuario_autenticado else 'Sistema'
				
				#-- Obtener el nombre de la estación y la fecha.
				estacion = socket.gethostname()
				fecha_actual = timezone.now().strftime("%Y-%m-%d %H:%M:%S")		
				
				
				#-- Paso 1: Obtener productos tipo "P" para ProductoStock.
				productos_stock = Producto.objects.filter(tipo_producto="P")
				
				#-- Crear registros para ProductoStock.
				producto_stock_instances = [
					ProductoStock(
						id_producto=producto,
						id_deposito=instance,
						stock=0,
						minimo=0,
						fecha_producto_stock=timezone.now(),
						id_user=usuario_autenticado,
						usuario=nombre_usuario,
						estacion=estacion,
						fcontrol=fecha_actual
					)
					for producto in productos_stock
				]
				
				#-- Guardar en ProductoStock en lotes.
				ProductoStock.objects.bulk_create(producto_stock_instances, batch_size=BATCH_SIZE)
				
				#-- Paso 2: Obtener productos con id_cai único para ProductoMinimo.
				productos_minimo = Producto.objects.exclude(id_cai=None).values("id_cai").distinct()
				
				#-- Crear registros para ProductoMinimo.
				producto_minimo_instances = [
					ProductoMinimo(
						id_deposito=instance,
						id_cai=ProductoCai.objects.get(pk=producto["id_cai"]),
						minimo=0,
						id_user=usuario_autenticado,
						usuario=nombre_usuario,
						estacion=estacion,
						fcontrol=fecha_actual
					)
					for producto in productos_minimo
				]
				
				#-- Guardar en ProductoMinimo en lotes.
				ProductoMinimo.objects.bulk_create(producto_minimo_instances, batch_size=BATCH_SIZE)
				
		except Exception as e:
			import logging
			logger = logging.getLogger(__name__)
			logger.error(f"Error en el signal trasladar_productos_a_stock_y_minimo: {str(e)}")


@receiver(post_save, sender=ProductoStock)
def actualizar_estado_producto_por_stock(sender, instance, **kwargs):
	"""
	Signal que programa la actualización del Estado del Producto para después del commit.
	Esto evita bloqueos extendidos y posibles deadlocks.
	Solo actualiza si el producto tiene estado automático (FALTANTES, DISPONIBLES, POCAS).
	"""
	#-- Programar para ejecutar después que se libere el bloqueo de la transacción actual.
	transaction.on_commit(lambda: _procesar_estado_producto(instance))


def _procesar_estado_producto(instance):
	"""
	Función que se ejecuta después del commit para actualizar el estado del producto.
	Solo actualiza si el producto tiene estado automático (FALTANTES, DISPONIBLES, POCAS).
	"""
	try:
		with transaction.atomic():
			#-- Obtener el producto relacionado.
			producto = instance.id_producto
			
			#-- Solo procesar si es un producto (no servicio) y tiene CAI.
			if producto.tipo_producto.upper() != 'P' or not producto.id_cai:
				return
			
			#-- Obtener los estados una vez para eficiencia.
			estados = ProductoEstado.objects.filter(
				nombre_producto_estado__in=['FALTANTES', 'DISPONIBLES', 'POCAS']
			)
			
			estado_faltantes = estados.filter(nombre_producto_estado='FALTANTES').first()
			estado_disponibles = estados.filter(nombre_producto_estado='DISPONIBLES').first()
			estado_pocas = estados.filter(nombre_producto_estado='POCAS').first()
			
			#-- Verificar que existan los 3 estados requeridos.
			if not all([estado_faltantes, estado_disponibles, estado_pocas]):
				estados_faltantes = []
				if not estado_faltantes: estados_faltantes.append('FALTANTES')
				if not estado_disponibles: estados_faltantes.append('DISPONIBLES')
				if not estado_pocas: estados_faltantes.append('POCAS')
				raise ValueError(f"No se encontraron los estados: {', '.join(estados_faltantes)}")
			
			#-- Solo proceder si el producto tiene un estado automático.
			estados_auto_ids = [e.id_producto_estado for e in [estado_faltantes, estado_disponibles, estado_pocas] if e]
			
			if producto.id_producto_estado_id not in estados_auto_ids:
				#-- El producto tiene un estado manual (OFERTAS, etc.), no actualizar.
				return
			
			#-- Calcular stock total sumando todos los depósitos.
			stock_total = ProductoStock.objects.filter(
				id_producto=producto
			).aggregate(total_stock=Sum('stock'))['total_stock'] or 0
			
			#-- Buscar la configuración en MedidasEstados para este CAI.
			medidas_estados = MedidasEstados.objects.filter(id_cai=producto.id_cai).first()
			
			if medidas_estados:
				stock_desde = medidas_estados.stock_desde or 0
				stock_hasta = medidas_estados.stock_hasta or 999999
				
				#-- Determinar el estado basado en el stock.
				if stock_total < stock_desde:
					nuevo_estado = estado_faltantes
				elif stock_total > stock_hasta:
					nuevo_estado = estado_disponibles
				else:
					nuevo_estado = estado_pocas
			else:
				#-- Si no hay medidas_estados, usar estado por defecto.
				if stock_total > 0:
					nuevo_estado = estado_disponibles
				else:
					nuevo_estado = estado_faltantes
			
			#-- Actualizar el estado del producto si cambió.
			if producto.id_producto_estado != nuevo_estado:
				Producto.objects.filter(pk=producto.pk).update(
					id_producto_estado=nuevo_estado
				)
				
	except Exception as e:
		import logging
		logger = logging.getLogger(__name__)
		logger.error(f"Error en el signal actualizar_estado_producto_por_stock: {str(e)}")

# neumatic\apps\maestros\services.py
from django.db import transaction
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.base_models import ProductoEstado, MedidasEstados


def actualizar_estados_productos(actualizar_todos=False):
	"""
	Actualiza el estado de los productos basado en stock y rangos de MedidasEstados.
	
	Args:
		actualizar_todos (bool): Si es True, actualiza todos los productos.
								 Si es False, solo actualiza los que tienen estado
								 FALTANTES, DISPONIBLES o POCAS.
	"""
	#-- Obtener los estados una vez para eficiencia.
	estados = ProductoEstado.objects.filter(
		nombre_producto_estado__in=['FALTANTES', 'DISPONIBLES', 'POCAS']
	)
	
	estado_faltantes = estados.filter(nombre_producto_estado='FALTANTES').first()
	estado_disponibles = estados.filter(nombre_producto_estado='DISPONIBLES').first()
	estado_pocas = estados.filter(nombre_producto_estado='POCAS').first()
	
	if not all([estado_faltantes, estado_disponibles, estado_pocas]):
		estados_faltantes = []
		if not estado_faltantes: estados_faltantes.append('FALTANTES')
		if not estado_disponibles: estados_faltantes.append('DISPONIBLES')
		if not estado_pocas: estados_faltantes.append('POCAS')
		raise ValueError(f"No se encontraron los estados: {', '.join(estados_faltantes)}")
	
	#-- Obtener rangos de MedidasEstados para eficiencia.
	rangos_por_cai = {
		rango.id_cai_id: rango 
		for rango in MedidasEstados.objects.select_related('id_cai').all()
	}
	
	#-- Construir queryset base.
	queryset_base = Producto.objects.filter(tipo_producto='P')
	
	#-- Aplicar filtro según la opción elegida.
	if not actualizar_todos:
		#-- Solo actualizar productos que tengan estados automáticos.
		estados_auto = [estado_faltantes, estado_disponibles, estado_pocas]
		queryset_base = queryset_base.filter(
			id_producto_estado__in=estados_auto
		)
	
	#-- Optimizar consultas.
	productos = (queryset_base
		.select_related('id_cai')
		.prefetch_related('productostock_set')
	)
	
	productos_actualizados = 0
	actualizaciones = []
	
	with transaction.atomic():
		for producto in productos:
			#-- Calcular stock total.
			stock_total = sum(stock.stock for stock in producto.productostock_set.all())
			
			#-- Obtener rango para este CAI si existe.
			rango = rangos_por_cai.get(producto.id_cai_id)
			
			if rango:
				stock_desde = rango.stock_desde or 0
				stock_hasta = rango.stock_hasta or 999999
				
				#-- Determinar el estado basado en el stock.
				if stock_total < stock_desde:
					nuevo_estado = estado_faltantes
				elif stock_total > stock_hasta:
					nuevo_estado = estado_disponibles
				else:
					nuevo_estado = estado_pocas
			else:
				#-- Si no hay rango, usar estado por defecto.
				nuevo_estado = estado_disponibles if stock_total > 0 else estado_faltantes
			
			#-- Actualizar solo si cambió el estado.
			if producto.id_producto_estado != nuevo_estado:
				producto.id_producto_estado = nuevo_estado
				actualizaciones.append(producto)
				productos_actualizados += 1
		
		#-- Bulk update para mejor performance.
		if actualizaciones:
			Producto.objects.bulk_update(actualizaciones, ['id_producto_estado'])
	
	#-- Mensaje informativo sobre el alcance.
	tipo_actualizacion = "TODOS los productos" if actualizar_todos else "solo productos con estados automáticos"
	
	return {
		'total_productos': productos.count(),
		'productos_actualizados': productos_actualizados,
		'tipo_actualizacion': tipo_actualizacion,
		'message': f"Se actualizaron {productos_actualizados} de {productos.count()} productos ({tipo_actualizacion})"
	}
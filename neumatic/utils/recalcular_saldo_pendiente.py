# neumatic\utils\recalcular_saldo_pendiente.py
from decimal import Decimal
from django.db import transaction

from apps.ventas.models.factura_models import Factura


@transaction.atomic
def recalcular_saldo_pendiente_cliente(id_cliente, condicion_cta_cte=2):
	"""
	Recalcula los saldos pendientes de un cliente en cuenta corriente.

	Imputa los comprobantes que RESTAN saldo (mult_saldo = -1: recibos, NC)
	contra los que SUMAN saldo (mult_saldo = 1: facturas, ND), de más
	antiguo a más nuevo, según la fecha del comprobante.

	Modifica en Factura:
	- entrega: monto imputado (0 si no tiene imputación).
	- estado:  "C" si el comprobante queda totalmente cancelado.

	Devuelve un dict con el resumen del proceso.
	"""
	comprobantes = list(
		Factura.objects
		.filter(
			id_cliente_id=id_cliente,
			condicion_comprobante=condicion_cta_cte,
			id_comprobante_venta__mult_saldo__in=(1, -1),
		)
		.select_related('id_comprobante_venta')
		.order_by('fecha_comprobante', 'id_factura')
	)
	
	if not comprobantes:
		return {
			'procesados': 0,
			'cancelados': 0,
			'a_favor': Decimal('0.00'),
			'pendiente': Decimal('0.00'),
		}
	
	#-- Resetear en memoria.
	for c in comprobantes:
		c.entrega = Decimal('0.00')
		c.estado = ""
	
	#-- Algoritmo de imputación.
	for comp_resta in comprobantes:
		mult = comp_resta.id_comprobante_venta.mult_saldo
		if not (mult < 0 or (comp_resta.total is not None and comp_resta.total < 0)):
			continue
			
		monto_disponible = abs(comp_resta.total - comp_resta.entrega)
		if monto_disponible == 0:
			continue
			
		for comp_suma in comprobantes:
			if comp_suma is comp_resta:
				continue
			if comp_suma.id_comprobante_venta.mult_saldo != 1:
				continue
			if comp_suma.estado == "C":
				continue
			if comp_suma.total is None or comp_suma.total <= 0:
				continue
				
			saldo_suma = (comp_suma.total - comp_suma.entrega) * comp_suma.id_comprobante_venta.mult_saldo
			
			if saldo_suma <= monto_disponible:
				monto_disponible -= saldo_suma
				comp_suma.entrega = comp_suma.total
				comp_suma.estado = "C"
			else:
				comp_suma.entrega = comp_suma.entrega + monto_disponible
				monto_disponible = Decimal('0.00')
			
			if monto_disponible == 0:
				break
				
		comp_resta.entrega = comp_resta.total - monto_disponible
		if comp_resta.entrega == comp_resta.total:
			comp_resta.estado = "C"
	
	Factura.objects.bulk_update(comprobantes, ['entrega', 'estado'], batch_size=500)
	
	cancelados = sum(1 for c in comprobantes if c.estado == "C")
	a_favor = sum(
		(c.total - c.entrega)
		for c in comprobantes
		if c.id_comprobante_venta.mult_saldo == -1 and c.estado != "C"
	)
	pendiente = sum(
		(c.total - c.entrega)
		for c in comprobantes
		if c.id_comprobante_venta.mult_saldo == 1 and c.estado != "C"
	)
	
	return {
		'procesados': len(comprobantes),
		'cancelados': cancelados,
		'a_favor': a_favor,
		'pendiente': pendiente,
	}
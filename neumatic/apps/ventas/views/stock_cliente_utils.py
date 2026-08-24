from django.db import transaction
from apps.ventas.models.factura_models import DetalleFactura
from apps.ventas.models.venta_models import StockCliente


def crear_stock_cliente_desde_factura(factura):
    """
    Crea registros de StockCliente para una factura dada, a partir de sus detalles
    que sean productos físicos (tipo_producto='P') y con cantidad > 0.
    Si ya existe stock, no hace nada.
    """
    if factura.stock_clie:
        # Ya tiene stock, no duplicar
        return

    detalles = factura.detallefactura_set.filter(
        cantidad__gt=0,
        id_producto__tipo_producto='P'
    )

    if not detalles.exists():
        # No hay productos para crear stock
        return

    with transaction.atomic():
        for detalle in detalles:
            StockCliente.objects.create(
                id_factura=factura,
                id_producto=detalle.id_producto,
                cantidad=detalle.cantidad,
                retirado=0,
                numero=0,
                comentario="Generado desde factura"
            )
        factura.stock_clie = True
        factura.save(update_fields=['stock_clie'])
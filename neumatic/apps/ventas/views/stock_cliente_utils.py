from django.db import transaction
from apps.ventas.models.factura_models import DetalleFactura
from apps.ventas.models.venta_models import StockCliente


def crear_stock_cliente_desde_factura(factura):
    """
    Crea registros de StockCliente para una factura dada, a partir de sus detalles
    que sean productos físicos (tipo_producto='P') y con cantidad > 0.
    Verifica la existencia real en la tabla, no confía en factura.stock_clie.
    """
    print("🔍 [DEBUG] Entrando a crear_stock_cliente_desde_factura")
    print(f"🔍 [DEBUG] factura.id_factura: {factura.id_factura}")
    print(f"🔍 [DEBUG] factura.stock_clie actual: {factura.stock_clie}")

    # Verificación REAL: ¿existen registros en stock_cliente para esta factura?
    existentes = StockCliente.objects.filter(id_factura=factura).exists()
    print(f"🔍 [DEBUG] ¿Existen registros en stock_cliente? {existentes}")

    if existentes:
        print("⚠️ [DEBUG] Ya existen registros, saliendo.")
        # Sincronizar por si acaso
        if not factura.stock_clie:
            factura.stock_clie = True
            factura.save(update_fields=['stock_clie'])
        return

    # Si no hay registros, proceder a crearlos (independientemente de stock_clie)
    print("🔍 [DEBUG] No hay registros, procediendo a crear...")

    detalles = factura.detallefactura_set.filter(
        cantidad__gt=0,
        id_producto__tipo_producto='P'
    )

    print(f"🔍 [DEBUG] Detalles con cantidad>0 y tipo_producto='P': {detalles.count()}")

    if not detalles.exists():
        print("⚠️ [DEBUG] No hay productos físicos. Se dejará stock_clie=False.")
        if factura.stock_clie:
            factura.stock_clie = False
            factura.save(update_fields=['stock_clie'])
        return

    with transaction.atomic():
        creados = 0
        for detalle in detalles:
            try:
                StockCliente.objects.create(
                    id_factura=factura,
                    id_producto=detalle.id_producto,
                    cantidad=detalle.cantidad,
                    retirado=0,
                    numero=0,
                    comentario="Generado desde factura"
                )
                creados += 1
                print(f"✅ Creado StockCliente para producto {detalle.id_producto_id} x {detalle.cantidad}")
            except Exception as e:
                print(f"❌ Error al crear StockCliente: {e}")

        if creados > 0:
            factura.stock_clie = True
            factura.save(update_fields=['stock_clie'])
            print(f"✅ factura.stock_clie actualizado a True. Creados: {creados}")
        else:
            factura.stock_clie = False
            factura.save(update_fields=['stock_clie'])
            print("⚠️ No se crearon registros, stock_clie = False")
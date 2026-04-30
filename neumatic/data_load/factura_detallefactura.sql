UPDATE detalle_factura
SET producto_venta = (
    SELECT nombre_producto
    FROM producto
    WHERE producto.id_producto = detalle_factura.id_producto_id
)
WHERE id_producto_id IS NOT NULL;


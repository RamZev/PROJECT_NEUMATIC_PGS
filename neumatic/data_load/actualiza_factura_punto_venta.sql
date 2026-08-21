UPDATE factura
SET id_punto_venta_id = (
    SELECT id_punto_venta
    FROM punto_venta
    WHERE punto_venta.id_sucursal_id = factura.id_sucursal_id
    LIMIT 1
)
WHERE id_punto_venta_id IS NULL
AND id_sucursal_id IS NOT NULL;
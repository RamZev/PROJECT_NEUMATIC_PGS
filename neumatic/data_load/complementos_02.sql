-- medidas_estados_sin_cai.sql
-- Script para eliminar los registros con id_cai_id NULL en medidas_estados:
DELETE FROM medidas_estados where id_cai_id is NULL;

-- actualiza_factura_punto_venta.sql
UPDATE factura
SET id_punto_venta_id = (
    SELECT id_punto_venta
    FROM punto_venta
    WHERE punto_venta.id_sucursal_id = factura.id_sucursal_id
    LIMIT 1
)
WHERE id_punto_venta_id IS NULL
AND id_sucursal_id IS NOT NULL;

-- descuento_revendedor.sql
TRUNCATE TABLE descuento_revendedor RESTART IDENTITY;
INSERT INTO descuento_revendedor (
	usuario, estacion, fcontrol, fcontrol2,
	estatus_descuento_revendedor, descuento,
	id_user_id, id_user_update_id,
	id_familia_id, id_marca_id
) VALUES
	(NULL, NULL, NULL, NULL, true, 4.00, NULL, NULL, 1, 1),
	(NULL, NULL, NULL, NULL, true, 4.00, NULL, NULL, 2, 1),
	(NULL, NULL, NULL, NULL, true, 4.00, NULL, NULL, 1, 2),
	(NULL, NULL, NULL, NULL, true, 4.00, NULL, NULL, 2, 2);

-- Actualizar letra eb comprobante de recibos RB
UPDATE numero
SET letra = 'R'
WHERE comprobante = 'RB';
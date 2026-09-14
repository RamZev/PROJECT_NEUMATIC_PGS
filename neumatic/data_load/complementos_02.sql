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

-- marcar los comprobantes internos
UPDATE comprobante_venta 
SET interno='true' 
WHERE remito='true' AND nombre_comprobante_venta ILIKE '%int%';

-- marcar los comprobantes manuales
UPDATE 
comprobante_venta 
SET manual='true' 
WHERE nombre_comprobante_venta ILIKE '%manual%';

-- marcar los comprobantes que se puede dejar mercaderia en stock de clientes
UPDATE comprobante_venta 
SET stock_clie='true' 
WHERE mult_stock < 0 AND interno = 'false' AND ncr_ndb = 'false' AND codigo_comprobante_venta <> 'MM';
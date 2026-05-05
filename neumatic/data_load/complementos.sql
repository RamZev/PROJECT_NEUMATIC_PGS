-- actualiza_color_producto_estado.sql
UPDATE producto_estado SET
	color = '#ffffff' WHERE id_producto_estado = 1;

UPDATE producto_estado SET
	color = '#ffff00' WHERE id_producto_estado = 2;

UPDATE producto_estado SET
	color = '#ff3232' WHERE id_producto_estado = 3;

UPDATE producto_estado SET
	color = '#64ff64' WHERE id_producto_estado = 4;

UPDATE producto_estado SET
	color = '#ffb432' WHERE id_producto_estado = 5;

-- actualiza_tipo_comprobante.sql
-- Factura
UPDATE 
	comprobante_venta 
	SET tipo_comprobante = 'FACTURA' WHERE id_comprobante_venta IN (1, 8, 13, 20, 27, 30);

-- Nota de Crédito
UPDATE 
	comprobante_venta 
	SET tipo_comprobante = 'NOTA DE CRÉDITO' WHERE id_comprobante_venta IN (2, 9, 28);

-- Nota de Débito
UPDATE 
	comprobante_venta 
	SET tipo_comprobante = 'NOTA DE DÉBITO' WHERE id_comprobante_venta IN (3, 10, 29);

-- Recibo
UPDATE 
	comprobante_venta 
	SET tipo_comprobante = 'RECIBO' WHERE id_comprobante_venta IN (4, 15, 21, 24, 26, 32);

-- Ajuste
UPDATE 
	comprobante_venta 
	SET tipo_comprobante = 'AJUSTE' WHERE id_comprobante_venta IN (5);

-- Movimiento Interno
UPDATE 
	comprobante_venta 
	SET tipo_comprobante = 'MOVIMIENTO INTERNO' WHERE id_comprobante_venta IN (6);

-- Presupuesto
UPDATE 
	comprobante_venta 
	SET tipo_comprobante = 'PRESUPUESTO' WHERE id_comprobante_venta IN (7);

-- Remito
UPDATE 
	comprobante_venta 
	SET tipo_comprobante = 'REMITO' WHERE id_comprobante_venta IN (11, 12, 14, 16, 17, 18, 19, 22, 31);

-- Egreso de Caja
UPDATE 
	comprobante_venta 
	SET tipo_comprobante = 'EGRESOS DE CAJA' WHERE id_comprobante_venta IN (23);

-- Ingreso de Caja
UPDATE 
	comprobante_venta 
	SET tipo_comprobante = 'INGRESO DE CAJA' WHERE id_comprobante_venta IN (25);

-- actualiza_producto_operario.sql
UPDATE producto
SET obliga_operario = TRUE
WHERE tipo_producto = 'S' AND (obliga_operario IS NULL OR obliga_operario = FALSE);

-- detalle_factura_nogravado.sql
-- Hay que incorporarlo en detalle_factura_migra.py
-- Contemplar al momente de crear los comprobantes
-- Sentencia para mover el valor de la columna gravado a la columna no_gravado cuyo iva sea cero.
UPDATE
	detalle_factura
SET
	no_gravado = gravado,
	gravado = 0
WHERE
	iva = 0;

-- factura_detallefactura.sql
UPDATE detalle_factura
SET producto_venta = (
    SELECT nombre_producto
    FROM producto
    WHERE producto.id_producto = detalle_factura.id_producto_id
)
WHERE id_producto_id IS NOT NULL;

-- producto_migra_tipo_servicio.sql
-- Primera actualización
UPDATE producto 
SET tipo_producto = UPPER(tipo_producto)
WHERE tipo_producto IN ('s', 'p');

-- Segunda actualización
UPDATE producto
SET tipo_producto = 'S'
WHERE (tipo_producto IS NULL OR tipo_producto = '')
AND (
    UPPER(nombre_producto) LIKE '%REPARACION%' 
    OR UPPER(nombre_producto) LIKE '%REPARACON%'
    OR UPPER(nombre_producto) LIKE '%REP %'
    OR UPPER(nombre_producto) LIKE '% REP%'
    OR UPPER(nombre_producto) LIKE 'REP%'
);

-- Tercera Actualización
UPDATE producto
SET tipo_producto = 'P'
WHERE (tipo_producto IS NULL OR tipo_producto = '');

-- Cuarta Actualización
UPDATE producto
SET tipo_producto = 'P'
WHERE tipo_producto = 'O';

-- cambios_medidas_estados.sql
UPDATE producto_estado SET nombre_producto_estado = 'FALTANTES' WHERE id_producto_estado = 3;
UPDATE medidas_estados SET id_estado_id = 5;

-- forma_pago_sql
INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:00:26', 1, TRUE, 'EFECTIVO');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:00:36', 2, TRUE, 'CUENTA CORRIENTE');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:00:44', 3, TRUE, 'TARJETA CREDITO');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:00:53', 4, TRUE, 'TARJETA DEBITO');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:01:03', 5, TRUE, 'DEPOSITO');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:01:26', 6, TRUE, 'DOLARES');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:01:35', 7, TRUE, 'CHEQUES');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:01:44', 8, TRUE, 'RETENCIONES');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:01:55', 9, TRUE, 'COMPENSA. FACTURAS');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:02:05', 10, TRUE, 'MERCADO PAGO');

-- actualizar_camion_factura.sql
UPDATE factura set comision = 'C' 
WHERE id_factura in (1505686, 1519621, 1549989, 1580175, 
1589641, 1602573, 1620291, 1621025, 1627924, 1629556, 1659081, 1677861);

-- actualiza_cliente.sql
UPDATE cliente SET cliente_empresa = true WHERE id_cliente = 30007;
DELETE FROM cliente WHERE id_cliente = 0;

-- actualiza_ventas_null.sql
-- Scripts para actualizar con cero (0) los campos de valores numéricos en NULL.
UPDATE detalle_factura SET costo=0.0 WHERE costo is NULL;
UPDATE detalle_factura SET precio_lista=0.0 WHERE precio_lista is NULL;
UPDATE detalle_factura SET precio=0.0 WHERE precio is NULL;
UPDATE detalle_factura SET descuento=0.0 WHERE descuento is NULL;
UPDATE detalle_factura SET desc_vendedor=0.0 WHERE desc_vendedor is NULL;
UPDATE detalle_factura SET gravado=0.0 WHERE gravado is NULL;
UPDATE detalle_factura SET alic_iva=0.0 WHERE alic_iva is NULL;
UPDATE detalle_factura SET iva=0.0 WHERE iva is NULL;
UPDATE detalle_factura SET stock=0.0 WHERE stock is NULL;
UPDATE detalle_factura SET "total"=0.0 WHERE "total" is NULL;

UPDATE detalle_factura SET act_stock=False WHERE act_stock is NULL;

-- Script para actualizar el id_vendedor_id en cliente si es nulo.
UPDATE cliente SET id_vendedor_id=1 WHERE id_vendedor_id is NULL;




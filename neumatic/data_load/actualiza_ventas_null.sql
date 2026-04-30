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
UPDATE cliente SET id_vendedor_id=1 WHERE id_vendedor_id is NULL
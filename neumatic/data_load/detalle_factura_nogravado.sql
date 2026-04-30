-- Hay que incorporarlo en detalle_factura_migra.py
-- Contemplar al momente de crear los comprobantes
-- Sentencia para mover el valor de la columna gravado a la columna no_gravado cuyo iva sea cero.
UPDATE
	detalle_factura
SET
	no_gravado = gravado,
	gravado = 0
WHERE
	iva = 0
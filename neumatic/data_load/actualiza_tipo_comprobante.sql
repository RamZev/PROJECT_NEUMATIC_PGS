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
-- FICHA DE SEGUIMIENTO DE STOCK.
-- POR CÓDIGO DE PRODUCTO

-- NUEVAS TABLAS EN DB_BROWSER (movimientos en Ventas y Movimientos Internos)

--CREATE VIEW vlFichaStockVentas AS 
SELECT detalle_factura.id_producto_id, factura.compro, factura.letra_comprobante, factura.numero_comprobante, factura.fecha_comprobante,
	detalle_factura.cantidad*comprobante_venta.mult_stock as cantidad,
	detalle_factura.precio, detalle_factura.total,
	factura.id_cliente_id, cliente.nombre_cliente,
	factura.no_estadist, factura.id_sucursal_id, factura.id_deposito_id,
	'V' as marca
FROM detalle_factura 
	INNER JOIN factura on detalle_factura.id_factura_id = factura.id_factura
	INNER JOIN comprobante_venta on factura.id_comprobante_venta_id = comprobante_venta.id_comprobante_venta
	INNER JOIN cliente on factura.id_cliente_id = cliente.id_cliente
WHERE comprobante_venta.mult_stock <> 0
ORDER BY factura.fecha_comprobante


--(movimientos en Compras)
--CREATE VIEW vlFichaStockCompra AS
SELECT detalle_compra.id_producto_id, compra.compro, compra.letra_comprobante, compra.numero_comprobante, compra.fecha_comprobante,
	detalle_compra.cantidad*comprobante_compra.mult_stock as cantidad,
	detalle_compra.precio, detalle_compra.total,
	compra.id_proveedor_id, proveedor.nombre_proveedor,
	False as no_estadist, compra.id_sucursal_id, compra.id_deposito_id,
	'C' as marca
FROM detalle_compra
	INNER JOIN compra on detalle_compra.id_compra_id = compra.id_compra
	INNER JOIN comprobante_compra on compra.id_comprobante_compra_id = comprobante_compra.id_comprobante_compra
	INNER JOIN proveedor on compra.id_proveedor_id = proveedor.id_proveedor
WHERE comprobante_compra.mult_stock <> 0
ORDER BY compra.fecha_comprobante


-- ============================================================ --
-- PRUEBAS
-- ============================================================ --
-- VENTAS.

--CREATE VIEW vlFichaStockVentas AS 
SELECT
	ROW_NUMBER() OVER() AS id,
	df.id_producto_id,
	pc.cai,
	--f.compro,
	--f.letra_comprobante,
	--f.numero_comprobante,
	f.fecha_comprobante,
	(f.compro || ' ' || f.letra_comprobante || ' ' || SUBSTR(printf('%012d', f.numero_comprobante), 1, 4) || '-' || SUBSTR(printf('%012d', f.numero_comprobante), 5)) AS comprobante,
	(df.cantidad * cv.mult_stock) AS cantidad,
	df.precio,
	df.total,
	f.id_cliente_id,
	c.nombre_cliente,
	f.no_estadist,
	f.id_sucursal_id,
	f.id_deposito_id,
	'Vta.' AS marca
FROM
	detalle_factura df
	INNER JOIN factura f ON df.id_factura_id = f.id_factura
	INNER JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
	INNER JOIN cliente c ON f.id_cliente_id = c.id_cliente
	INNER JOIN producto p ON df.id_producto_id = p.id_producto
	LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
WHERE
	--df.id_producto_id = 1450
	cv.mult_stock <> 0
	AND df.id_producto_id = 1450
	AND f.fecha_comprobante BETWEEN '2025-01-01' AND '2025-10-16'
ORDER BY
	f.fecha_comprobante



-- COMPRAS.

--CREATE VIEW vlFichaStockCompra AS
SELECT
	dc.id_producto_id,
	pc.cai,
	--c.compro,
	--c.letra_comprobante,
	--c.numero_comprobante,
	c.fecha_comprobante,
	(c.compro || ' ' || c.letra_comprobante || ' ' || SUBSTR(printf('%012d', c.numero_comprobante), 1, 4) || '-' || SUBSTR(printf('%012d', c.numero_comprobante), 5)) AS comprobante,
	(dc.cantidad * cc.mult_stock) AS cantidad,
	dc.precio,
	dc.total,
	c.id_proveedor_id,
	pr.nombre_proveedor,
	False AS no_estadist,
	c.id_sucursal_id,
	c.id_deposito_id,
	'Cpr.' AS marca
FROM detalle_compra dc
	INNER JOIN compra c ON dc.id_compra_id = c.id_compra
	INNER JOIN comprobante_compra cc ON c.id_comprobante_compra_id = cc.id_comprobante_compra
	INNER JOIN proveedor pr ON c.id_proveedor_id = pr.id_proveedor
	INNER JOIN producto p ON dc.id_producto_id = p.id_producto
	LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
WHERE
	--dc.id_producto_id = 1450
	cc.mult_stock <> 0
	AND dc.id_producto_id = 335725
	AND c.fecha_comprobante BETWEEN '2025-01-01' AND '2025-10-16'
ORDER BY
	c.fecha_comprobante



--select * from detalle_compra where id_producto_id = 440;
--select * from compra;
------------------------------------------------------------
SELECT
	c.id_compra, c.compro, c.letra_comprobante, c.numero_comprobante, c.fecha_comprobante,
	dc.id_detalle_compra, dc.cantidad, dc.id_producto_id
FROM
	compra c
	JOIN detalle_compra dc ON c.id_compra = dc.id_compra_id
WHERE
	dc.id_producto_id = 335795
ORDER by
	c.fecha_comprobante desc
--



-----------------------------------------------------------------------------------
-- Solución
-----------------------------------------------------------------------------------
SELECT
	ROW_NUMBER() OVER(ORDER BY fecha_orden) AS id,
	id_producto_id,
	id_cai_id,
	cai,
	medida,
	nombre_producto,
	id_marca_id,
	nombre_producto_marca,
	fecha_comprobante,
	comprobante,
	cantidad,
	precio,
	total,
	
	id_cliente_proveedor,
	nombre_cliente_proveedor,
	no_estadist,
	id_sucursal_id,
	id_deposito_id,
	marca
FROM (
	-- Consulta VENTAS.
	SELECT
		df.id_producto_id,
		p.id_cai_id,
		pc.cai,
		p.medida,
		p.nombre_producto,
		p.id_marca_id,
		pm.nombre_producto_marca,
		f.fecha_comprobante AS fecha_orden,
		strftime('%d/%m/%Y', f.fecha_comprobante) AS fecha_comprobante,
		(f.compro || ' ' || f.letra_comprobante || ' ' || SUBSTR(printf('%012d', f.numero_comprobante), 1, 4) || '-' || SUBSTR(printf('%012d', f.numero_comprobante), 5)) AS comprobante,
		(df.cantidad * cv.mult_stock) AS cantidad,
		df.precio,
		df.total,
		f.id_cliente_id AS id_cliente_proveedor,
		c.nombre_cliente AS nombre_cliente_proveedor,
		f.no_estadist,
		f.id_sucursal_id,
		f.id_deposito_id,
		'Vta.' AS marca
	FROM
		detalle_factura df
		INNER JOIN factura f ON df.id_factura_id = f.id_factura
		INNER JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		INNER JOIN cliente c ON f.id_cliente_id = c.id_cliente
		INNER JOIN producto p ON df.id_producto_id = p.id_producto
		LEFT JOIN producto_marca pm ON p.id_marca_id = pm.id_producto_marca
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
	WHERE
		cv.mult_stock <> 0
		AND df.id_producto_id = 36900
		AND f.fecha_comprobante BETWEEN '2025-01-01' AND '2025-01-31'

	UNION ALL

	SELECT
		-- Consulta COMPRAS.
		dc.id_producto_id,
		p.id_cai_id,
		pc.cai,
		p.medida,
		p.nombre_producto,
		p.id_marca_id,
		pm.nombre_producto_marca,
		c.fecha_comprobante AS fecha_orden,
		strftime('%d/%m/%Y', c.fecha_comprobante) AS fecha_comprobante,
		(c.compro || ' ' || c.letra_comprobante || ' ' || SUBSTR(printf('%012d', c.numero_comprobante), 1, 4) || '-' || SUBSTR(printf('%012d', c.numero_comprobante), 5)) AS comprobante,
		(dc.cantidad * cc.mult_stock) AS cantidad,
		dc.precio,
		dc.total,
		c.id_proveedor_id AS id_cliente_proveedor,
		pr.nombre_proveedor AS nombre_cliente_proveedor,
		False AS no_estadist,
		c.id_sucursal_id,
		c.id_deposito_id,
		'Cpr.' AS marca
	FROM detalle_compra dc
		INNER JOIN compra c ON dc.id_compra_id = c.id_compra
		INNER JOIN comprobante_compra cc ON c.id_comprobante_compra_id = cc.id_comprobante_compra
		INNER JOIN proveedor pr ON c.id_proveedor_id = pr.id_proveedor
		INNER JOIN producto p ON dc.id_producto_id = p.id_producto
		LEFT JOIN producto_marca pm ON p.id_marca_id = pm.id_producto_marca
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
	WHERE
		cc.mult_stock <> 0
		AND dc.id_producto_id = 36900
		AND c.fecha_comprobante BETWEEN '2025-01-01' AND '2025-01-31'
) AS combined_data
ORDER BY
	fecha_orden, comprobante, marca;
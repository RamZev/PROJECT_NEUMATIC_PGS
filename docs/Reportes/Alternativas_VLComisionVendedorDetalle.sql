-- Consulta original:
SELECT 
	factura.compro,
	factura.letra_comprobante,
	factura.numero_comprobante,
	factura.fecha_comprobante,
	--factura.id_cliente_id,
	cliente.nombre_cliente,
	detalle_factura.reventa,
	detalle_factura.id_producto_id,
	producto.medida,
	--producto.id_marca_id,
	producto_marca.nombre_producto_marca,
	--producto.id_familia_id,
	producto_familia.nombre_producto_familia,
	--detalle_factura.cantidad,
	--detalle_factura.precio,
	--detalle_factura.costo,
	--detalle_factura.descuento,
	detalle_factura.gravado*comprobante_venta.mult_comision AS gravado,
	--detalle_factura.total*comprobante_venta.mult_comision AS total,
	--factura.no_estadist,
	detalle_factura.alic_iva*0 AS pje_auto,
	detalle_factura.alic_iva*0 AS comision,
	cliente.id_vendedor_id,
	vendedor.nombre_vendedor
FROM 
	detalle_factura 
	INNER JOIN factura ON detalle_factura.id_factura_id = factura.id_factura
	INNER JOIN comprobante_venta ON factura.id_comprobante_venta_id = comprobante_venta.id_comprobante_venta
	INNER JOIN cliente ON factura.id_cliente_id = cliente.id_cliente
	INNER JOIN vendedor ON cliente.id_vendedor_id = vendedor.id_vendedor
	INNER JOIN producto ON detalle_factura.id_producto_id = producto.id_producto
	INNER JOIN producto_familia ON producto.id_familia_id = producto_familia.id_producto_familia
	INNER JOIN producto_marca ON producto.id_marca_id = producto_marca.id_producto_marca
WHERE 
	comprobante_venta.mult_comision<>0 AND 
	factura.no_estadist <> True;


-- Primera propuesta: Obtención de porcentaje de comisión.
SELECT 
	f.id_factura,
	f.compro,
	f.letra_comprobante,
	f.numero_comprobante,
	(f.compro || '  ' || f.letra_comprobante || '  ' || SUBSTR(printf('%012d', f.numero_comprobante), 1, 4) || '-' || SUBSTR(printf('%012d', f.numero_comprobante), 5)) AS comprobante,
	f.fecha_comprobante,
	--factura.id_cliente_id,
	c.nombre_cliente,
	df.reventa,
	df.id_producto_id,
	p.medida,
	--producto.id_marca_id,
	pm.nombre_producto_marca,
	--producto.id_familia_id,
	pf.nombre_producto_familia,
	--detalle_factura.cantidad,
	--detalle_factura.precio,
	--detalle_factura.costo,
	--detalle_factura.descuento,
	df.gravado*cv.mult_comision AS gravado,
	--detalle_factura.total*comprobante_venta.mult_comision AS total,
	--factura.no_estadist,
	--detalle_factura.alic_iva*0 AS pje_auto,
	COALESCE(ROUND((SELECT 
			dvc.comision_porcentaje
		FROM vendedor_comision vc
			JOIN detalle_vendedor_comision dvc ON dvc.id_vendedor_comision_id = vc.id_vendedor_comision
			--JOIN vendedor v ON vc.id_vendedor_id = v.id_vendedor
			--JOIN producto_familia f ON dvc.id_familia_id = f.id_producto_familia
			--JOIN producto_marca m ON dvc.id_marca_id = m.id_producto_marca
		WHERE vc.id_vendedor_id = c.id_vendedor_id
			AND dvc.id_familia_id = p.id_familia_id
			AND dvc.id_marca_id = p.id_marca_id
		LIMIT 1), 2), 0) AS pje_comision,
	--detalle_factura.alic_iva*0 AS comision,
	c.id_vendedor_id,
	v.nombre_vendedor,
	"D" AS consulta
FROM 
	detalle_factura df
	INNER JOIN factura f ON df.id_factura_id = f.id_factura
	INNER JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
	INNER JOIN cliente c ON f.id_cliente_id = c.id_cliente
	INNER JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
	INNER JOIN producto p ON df.id_producto_id = p.id_producto
	INNER JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
	INNER JOIN producto_marca pm ON p.id_marca_id = pm.id_producto_marca
WHERE 
	cv.mult_comision<>0 AND 
	f.no_estadist <> True;
	

-- Segunda propuesta: Obtención de porcentaje de comisión y Cálculo de la comisión.
SELECT *,
       ROUND((pje_comision/100.0 * gravado), 2) AS monto_comision
FROM (
    SELECT 
        factura.compro,
        factura.letra_comprobante,
        factura.numero_comprobante,
        factura.fecha_comprobante,
        cliente.nombre_cliente,
        detalle_factura.reventa,
        detalle_factura.id_producto_id,
        producto.medida,
        producto_marca.nombre_producto_marca,
        producto_familia.nombre_producto_familia,
        detalle_factura.gravado * comprobante_venta.mult_comision AS gravado,
        detalle_factura.alic_iva * 0 AS pje_auto,
        COALESCE(ROUND((SELECT 
                ROUND(dvc.comision_porcentaje, 2)
            FROM vendedor_comision vc
                JOIN detalle_vendedor_comision dvc ON dvc.id_vendedor_comision_id = vc.id_vendedor_comision
                JOIN vendedor v ON vc.id_vendedor_id = v.id_vendedor
                JOIN producto_familia f ON dvc.id_familia_id = f.id_producto_familia
                JOIN producto_marca m ON dvc.id_marca_id = m.id_producto_marca
            WHERE vc.id_vendedor_id = cliente.id_vendedor_id
                AND dvc.id_familia_id = producto.id_familia_id
                AND dvc.id_marca_id = producto.id_marca_id
            LIMIT 1), 2), 0) AS pje_comision,
        cliente.id_vendedor_id,
        vendedor.nombre_vendedor
    FROM 
        detalle_factura 
        INNER JOIN factura ON detalle_factura.id_factura_id = factura.id_factura
        INNER JOIN comprobante_venta ON factura.id_comprobante_venta_id = comprobante_venta.id_comprobante_venta
        INNER JOIN cliente ON factura.id_cliente_id = cliente.id_cliente
        INNER JOIN vendedor ON cliente.id_vendedor_id = vendedor.id_vendedor
        INNER JOIN producto ON detalle_factura.id_producto_id = producto.id_producto
        INNER JOIN producto_familia ON producto.id_familia_id = producto_familia.id_producto_familia
        INNER JOIN producto_marca ON producto.id_marca_id = producto_marca.id_producto_marca
    WHERE 
        comprobante_venta.mult_comision <> 0 AND 
        factura.no_estadist <> True
) AS datos


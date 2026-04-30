-- ============================================
-- MIGRACIÓN DE VISTAS DE SQLITE3 A POSTGRESQL 18
-- CONVERSIÓN COMPLETA Y DEFINITIVA
-- ============================================

-- Eliminar vistas si existen
DROP VIEW IF EXISTS VLSaldosClientes CASCADE;
DROP VIEW IF EXISTS VLResumenCtaCte CASCADE;
DROP VIEW IF EXISTS VLMercaderiaPorCliente CASCADE;
DROP VIEW IF EXISTS VLRemitosClientes CASCADE;
DROP VIEW IF EXISTS VLTotalRemitosClientes CASCADE;
DROP VIEW IF EXISTS VLVentaComproLocalidad CASCADE;
DROP VIEW IF EXISTS VLVentaMostrador CASCADE;
DROP VIEW IF EXISTS VLVentaCompro CASCADE;
DROP VIEW IF EXISTS VLComprobantesVencidos CASCADE;
DROP VIEW IF EXISTS VLRemitosPendientes CASCADE;
DROP VIEW IF EXISTS VLRemitosVendedor CASCADE;
DROP VIEW IF EXISTS VLIVAVentasFULL CASCADE;
DROP VIEW IF EXISTS VLIVAVentasProvincias CASCADE;
DROP VIEW IF EXISTS VLIVAVentasSitrib CASCADE;
DROP VIEW IF EXISTS VLPercepIBVendedorTotales CASCADE;
DROP VIEW IF EXISTS VLPercepIBVendedorDetallado CASCADE;
DROP VIEW IF EXISTS VLPercepIBSubcuentaTotales CASCADE;
DROP VIEW IF EXISTS VLPercepIBSubcuentaDetallado CASCADE;
DROP VIEW IF EXISTS VLComisionVendedor CASCADE;
DROP VIEW IF EXISTS VLComisionVendedorDetalle CASCADE;
DROP VIEW IF EXISTS VLComisionOperario CASCADE;
DROP VIEW IF EXISTS VLPrecioDiferente CASCADE;
DROP VIEW IF EXISTS VLVentasResumenIB CASCADE;
DROP VIEW IF EXISTS VLEstadisticasVentas CASCADE;
DROP VIEW IF EXISTS VLEstadisticasVentasVendedor CASCADE;
DROP VIEW IF EXISTS VLEstadisticasVentasVendedorCliente CASCADE;
DROP VIEW IF EXISTS VLEstadisticasSegunCondicion CASCADE;
DROP VIEW IF EXISTS VLEstadisticasVentasMarca CASCADE;
DROP VIEW IF EXISTS VLEstadisticasVentasMarcaVendedor CASCADE;
DROP VIEW IF EXISTS VLClienteUltimaVenta CASCADE;
DROP VIEW IF EXISTS VLEstadisticasVentasProvincia CASCADE;
DROP VIEW IF EXISTS VLVentaSinEstadistica CASCADE;
DROP VIEW IF EXISTS VLTablaDinamicaVentas CASCADE;
DROP VIEW IF EXISTS VLTablaDinamicaDetalleVentas CASCADE;
DROP VIEW IF EXISTS VLTablaDinamicaEstadistica CASCADE;
DROP VIEW IF EXISTS VLLista CASCADE;
DROP VIEW IF EXISTS VLListaRevendedor CASCADE;
DROP VIEW IF EXISTS VLStockSucursal CASCADE;
DROP VIEW IF EXISTS VLStockGeneralSucursal CASCADE;
DROP VIEW IF EXISTS VLStockFecha CASCADE;
DROP VIEW IF EXISTS VLStockUnico CASCADE;
DROP VIEW IF EXISTS VLReposicionStock CASCADE;
DROP VIEW IF EXISTS VLMovimientoInternoStock CASCADE;
DROP VIEW IF EXISTS VLStockCliente CASCADE;
DROP VIEW IF EXISTS VLStockDeposito CASCADE;
DROP VIEW IF EXISTS VLFichaSeguimientoStock CASCADE;
DROP VIEW IF EXISTS VLDetalleCompraProveedor CASCADE;
DROP VIEW IF EXISTS VLCompraIngresada CASCADE;
DROP VIEW IF EXISTS VLProductoMinimo CASCADE;

-- ============================================
-- FUNCIÓN AUXILIAR PARA FORMATEAR NÚMEROS DE COMPROBANTE
-- ============================================
CREATE OR REPLACE FUNCTION format_comprobante(letra VARCHAR, numero INTEGER, formato VARCHAR DEFAULT 'completo')
RETURNS VARCHAR AS $$
DECLARE
    numero_padded VARCHAR;
    parte1 VARCHAR;
    parte2 VARCHAR;
BEGIN
    numero_padded := LPAD(numero::TEXT, 12, '0');
    
    IF formato = 'completo' THEN
        parte1 := SUBSTRING(numero_padded FROM 1 FOR 4);
        parte2 := SUBSTRING(numero_padded FROM 5);
        RETURN letra || ' ' || parte1 || '-' || parte2;
    ELSIF formato = 'solo_numero' THEN
        RETURN SUBSTRING(numero_padded FROM 1 FOR 4) || '-' || SUBSTRING(numero_padded FROM 5);
    ELSE
        RETURN numero_padded;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- FUNCIÓN AUXILIAR PARA JULIANDAY
-- ============================================
CREATE OR REPLACE FUNCTION julianday(fecha DATE)
RETURNS DECIMAL AS $$
BEGIN
    RETURN EXTRACT(EPOCH FROM fecha) / 86400.0 + 2440587.5;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- ============================================
-- Saldos Clientes.
-- Modelo: VLSaldosClientes
-- ============================================
CREATE VIEW VLSaldosClientes AS 
	SELECT 
		f.id_cliente_id, 
		f.fecha_comprobante, 
		f.fecha_pago, 
		c.nombre_cliente, 
		c.domicilio_cliente, 
		l.nombre_localidad,
		c.codigo_postal, 
		c.telefono_cliente, 
		c.sub_cuenta, 
		c.id_vendedor_id, 
		v.nombre_vendedor,
		f.total,
		f.entrega, 
		f.condicion_comprobante,
		cv.mult_saldo
	FROM
		factura f 
		JOIN cliente c ON f.id_cliente_id = c.id_cliente 
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta 
		JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
		LEFT JOIN localidad l ON c.id_localidad_id = l.id_localidad
	WHERE 
		f.condicion_comprobante = 2
		AND cv.mult_saldo <> 0;

-- ============================================
-- Resumen Cuenta Corriente.
-- Modelo: VLResumenCtaCte
-- ============================================
CREATE VIEW VLResumenCtaCte AS 
	SELECT 
		f.id_cliente_id, 
		c.nombre_cliente AS razon_social, 
		cv.nombre_comprobante_venta, 
		f.letra_comprobante, 
		f.numero_comprobante, 
		format_comprobante(f.letra_comprobante, f.numero_comprobante, 'completo') AS numero, 
		f.fecha_comprobante, 
		f.remito,
		f.condicion_comprobante, 
		CASE 
			WHEN f.condicion_comprobante = 1 THEN 'Contado'
			WHEN f.condicion_comprobante = 2 THEN 'Cta. Cte.'
			ELSE 'Desconocido'
		END AS condicion,
		f.total * cv.mult_saldo AS total, 
		f.entrega * cv.mult_saldo AS entrega,
		CASE
			WHEN (f.total * cv.mult_saldo) >= 0 THEN (f.total * cv.mult_saldo) * 1.0
			ELSE 0.0
		END AS debe,
		CASE
			WHEN (f.total * cv.mult_saldo) < 0 THEN (f.total * cv.mult_saldo) * 1.0
			ELSE 0.0
		END AS haber,
		0 AS intereses,
		0 AS saldo_acumulado,
		f.marca,
		CASE
			WHEN f.no_estadist THEN 'S'
			ELSE ''
		END AS no_estadist
	FROM
		factura f 
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
	WHERE
		cv.mult_saldo <> 0
	ORDER BY
		f.id_cliente_id, f.fecha_comprobante;

-- ============================================
-- Mercadería por Cliente.
-- Modelo: VLMercaderiaPorCliente
-- ============================================
CREATE VIEW VLMercaderiaPorCliente AS 
	SELECT 
	   f.id_cliente_id, 
	   cv.nombre_comprobante_venta, 
	   f.letra_comprobante, 
	   f.numero_comprobante,
	   format_comprobante(f.letra_comprobante, f.numero_comprobante, 'completo') AS numero, 
	   f.fecha_comprobante, 
	   COALESCE(m.nombre_producto_marca, '') AS nombre_producto_marca, 
	   COALESCE(p.medida, '') AS medida, 
	   df.id_producto_id, 
	   COALESCE(p.nombre_producto, '') AS nombre_producto, 
	   COALESCE(df.cantidad, 0.0)::DECIMAL AS cantidad, 
	   COALESCE(df.precio, 0.0)::DECIMAL AS precio, 
	   COALESCE(df.descuento, 0.0)::DECIMAL AS descuento, 
	   COALESCE(df.total, 0.0)::DECIMAL AS total
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura 
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN producto p ON df.id_producto_id = p.id_producto 
		LEFT JOIN producto_marca m ON p.id_marca_id = m.id_producto_marca;

-- ============================================
-- Remitos por Clientes.
-- Modelo: VLRemitosClientes
-- ============================================
CREATE VIEW VLRemitosClientes AS
	SELECT
		f.id_cliente_id, 
		cv.codigo_comprobante_venta, 
		cv.nombre_comprobante_venta, 
		f.fecha_comprobante, 
		f.letra_comprobante, 
		f.numero_comprobante, 
		format_comprobante(f.letra_comprobante, f.numero_comprobante, 'completo') AS numero, 
		p.nombre_producto, 
		p.medida, 
		COALESCE(df.cantidad, 0.0)::DECIMAL AS cantidad, 
		COALESCE(df.precio, 0.0)::DECIMAL AS precio, 
		COALESCE(df.descuento, 0.0)::DECIMAL AS descuento, 
		COALESCE(df.total, 0.0)::DECIMAL * COALESCE(cv.mult_stock, 0.0)::DECIMAL * -1 AS total
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN producto p ON df.id_producto_id = p.id_producto
	WHERE
		cv.mult_venta = 0;

-- ============================================
-- Total Remitos por Clientes.
-- Modelo: VLTotalRemitosClientes
-- ============================================
CREATE VIEW VLTotalRemitosClientes AS 
	SELECT 
		f.id_cliente_id, 
		f.fecha_comprobante, 
		c.nombre_cliente, 
		c.domicilio_cliente, 
		c.codigo_postal, 
		ti.nombre_iva, 
		c.cuit, 
		c.telefono_cliente, 
		(f.total * cv.mult_stock * -1) AS total
	FROM
		factura f
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN tipo_iva ti ON c.id_tipo_iva_id = ti.id_tipo_iva
	WHERE
		cv.mult_saldo = 0;

-- ============================================
-- Ventas por Localidad.
-- Modelo: VLVentaComproLocalidad
-- ============================================
CREATE VIEW VLVentaComproLocalidad AS 
	SELECT 
		f.id_cliente_id,
		f.id_sucursal_id,
		f.fecha_comprobante,
		c.nombre_cliente,
		c.cuit,
		c.codigo_postal,
		cv.nombre_comprobante_venta,
		cv.codigo_comprobante_venta,
		f.letra_comprobante,
		f.numero_comprobante,
		(cv.codigo_comprobante_venta || ' ' || f.letra_comprobante || ' ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante, 
		COALESCE(f.gravado, 0.0)::DECIMAL AS gravado,
		COALESCE(f.exento, 0.0)::DECIMAL AS exento,
		COALESCE(f.iva, 0.0)::DECIMAL AS iva,
		COALESCE(f.percep_ib, 0.0)::DECIMAL AS percep_ib,
		COALESCE(f.total, 0.0)::DECIMAL AS total,
		u.iniciales
	FROM
		factura f
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN usuarios_user u ON f.id_user_id = u.id
	WHERE
		cv.mult_venta <> 0;

-- ============================================
-- Ventas por Mostrador.
-- Modelo: VLVentaMostrador
-- ============================================
CREATE VIEW VLVentaMostrador AS 
	SELECT 
		df.id_detalle_factura,
		cv.nombre_comprobante_venta,
		cv.codigo_comprobante_venta,
		f.letra_comprobante,
		f.numero_comprobante,
		(cv.codigo_comprobante_venta || ' ' || f.letra_comprobante || ' ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.fecha_comprobante,
		f.id_cliente_id,
		c.nombre_cliente,
		c.mayorista,
		df.reventa,
		df.id_producto_id,
		p.nombre_producto,
		p.tipo_producto,
		(df.reventa || ' ' || p.tipo_producto) AS rv_tp,
		df.cantidad,
		df.precio,
		df.total * cv.mult_venta AS Total,
		f.id_sucursal_id
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN producto p ON df.id_producto_id = p.id_producto
	WHERE
		cv.mult_venta <> 0 AND f.no_estadist <> True;

-- ============================================
-- Ventas por Comprobantes.
-- Modelo: VLVentaCompro
-- ============================================
CREATE VIEW VLVentaCompro AS 
	SELECT 
		f.id_factura,
		cv.nombre_comprobante_venta,
		f.letra_comprobante,
		f.numero_comprobante,
		(cv.codigo_comprobante_venta || ' ' || f.letra_comprobante || ' ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.fecha_comprobante,
		f.condicion_comprobante,
		CASE 
			WHEN f.condicion_comprobante = 1 THEN 'Contado'
			WHEN f.condicion_comprobante = 2 THEN 'Cta. Cte.'
		END AS condicion,
		f.id_cliente_id,
		c.nombre_cliente,
		f.gravado * cv.mult_venta as gravado,
		f.iva * cv.mult_venta AS IVA,
		f.percep_ib * cv.mult_venta AS percep_ib,
		f.total * cv.mult_venta AS total,
		f.id_sucursal_id
	FROM
		factura f
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente;

-- ============================================
-- Comprobantes Vencidos.
-- Modelo: VLComprobantesVencidos
-- ============================================
CREATE VIEW VLComprobantesVencidos AS 
	SELECT 
		f.id_factura,
		f.fecha_comprobante,
		(julianday(CURRENT_DATE) - julianday(f.fecha_comprobante))::INTEGER AS dias_vencidos,
		cv.codigo_comprobante_venta,
		f.letra_comprobante,
		f.numero_comprobante,
		(cv.codigo_comprobante_venta || ' ' || f.letra_comprobante || ' ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.id_cliente_id,
		c.nombre_cliente,
		f.total::NUMERIC * 1.0 AS total,
		f.entrega::NUMERIC * 1.0 AS entrega,
		ROUND((f.total - f.entrega)::NUMERIC, 2) * 1.0 AS saldo,
		f.id_vendedor_id,
		f.id_sucursal_id
	FROM
		factura f
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
	WHERE
		f.estado = '';

-- ============================================
-- Remitos Pendientes.
-- Modelo: VLRemitosPendientes
-- ============================================
CREATE VIEW VLRemitosPendientes AS 
	SELECT 
		f.id_factura,
		f.id_cliente_id,
		c.nombre_cliente,
		cv.nombre_comprobante_venta,
		f.fecha_comprobante,
		f.letra_comprobante,
		f.numero_comprobante,
		format_comprobante(f.letra_comprobante, f.numero_comprobante, 'completo') AS comprobante,
		df.id_producto_id,
		p.nombre_producto,
		p.medida,
		df.cantidad,
		df.precio,
		df.descuento,
		df.total * cv.mult_stock * -1 AS total,
		f.id_vendedor_id,
		f.id_sucursal_id AS id_sucursal_fac,
		c.id_sucursal_id AS id_sucursal_cli
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
	WHERE
		cv.mult_venta = 0 AND cv.remito = 1
		AND f.estado = '';

-- ============================================
-- Remitos Vendedor.
-- Modelo: VLRemitosVendedor
-- ============================================
CREATE VIEW VLRemitosVendedor AS 
	SELECT 
		f.id_factura,
		f.id_cliente_id,
		c.nombre_cliente,
		cv.nombre_comprobante_venta,
		f.fecha_comprobante,
		f.letra_comprobante,
		f.numero_comprobante,
		format_comprobante(f.letra_comprobante, f.numero_comprobante, 'completo') AS comprobante,
		df.id_producto_id,
		p.nombre_producto,
		p.medida,
		df.cantidad,
		df.precio,
		df.descuento,
		df.total * cv.mult_stock * -1 AS total,
		f.id_vendedor_id
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
	WHERE
		cv.mult_venta = 0;

-- ============================================
-- Libro I.V.A. Ventas - Detalle.
-- Modelo: VLIVAVentasFULL
-- ============================================
CREATE VIEW VLIVAVentasFULL AS 
	SELECT 
		f.id_factura,
		cv.nombre_comprobante_venta,
		cv.codigo_comprobante_venta,
		f.letra_comprobante,
		f.numero_comprobante,
		(cv.codigo_comprobante_venta || ' ' || f.letra_comprobante || ' ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.fecha_comprobante,
		c.nombre_cliente,
		c.cuit,
		ti.codigo_iva,
		ROUND(f.gravado * cv.mult_venta, 2) * 1.0 AS gravado,
		ROUND(f.exento * cv.mult_venta, 2) * 1.0 AS exento,
		ROUND(f.iva * cv.mult_venta, 2) * 1.0 AS iva,
		ROUND(f.percep_ib * cv.mult_venta, 2) * 1.0 AS percep_ib,
		ROUND(f.total * cv.mult_venta, 2) * 1.0 AS total,
		f.id_sucursal_id
	FROM
		factura f
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN tipo_iva ti ON c.id_tipo_iva_id = ti.id_tipo_iva
	WHERE
		cv.libro_iva;

-- ============================================
-- Libro I.V.A. Ventas - Totales por Provincias.
-- Modelo: VLIVAVentasProvincias
-- ============================================
CREATE VIEW VLIVAVentasProvincias AS 
	SELECT 
		f.id_factura,
		p.id_provincia,
		p.nombre_provincia,
		f.fecha_comprobante,
		ROUND(f.gravado * cv.mult_venta * 1.0, 2) AS gravado,
		ROUND(f.exento * cv.mult_venta * 1.0, 2) AS exento,
		ROUND(f.iva * cv.mult_venta * 1.0, 2) AS iva,
		ROUND(f.percep_ib * cv.mult_venta * 1.0, 2) AS percep_ib,
		ROUND(f.total * cv.mult_venta * 1.0, 2) AS total,
		f.id_sucursal_id
	FROM
		factura f
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		LEFT JOIN localidad l ON c.id_localidad_id = l.id_localidad
		LEFT JOIN provincia p ON l.id_provincia_id = p.id_provincia
	WHERE
		cv.libro_iva;

-- ============================================
-- Libro I.V.A. Ventas - Totales para SITRIB.
-- Modelo: VLIVAVentasSitrib
-- ============================================
CREATE VIEW VLIVAVentasSitrib AS 
	SELECT 
		f.id_factura,
		f.fecha_comprobante,
		ti.codigo_iva,
		ti.nombre_iva,
		ROUND(f.gravado * cv.mult_venta * 1.0, 2) AS gravado, 
		ROUND(f.exento * cv.mult_venta * 1.0, 2) AS exento, 
		ROUND(f.iva * cv.mult_venta * 1.0, 2) AS iva, 
		ROUND(f.percep_ib * cv.mult_venta * 1.0, 2) AS percep_ib, 
		ROUND(f.total * cv.mult_venta * 1.0, 2) AS total,
		f.id_sucursal_id
	FROM
		factura f
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN tipo_iva ti ON c.id_tipo_iva_id = ti.id_tipo_iva
		LEFT JOIN localidad l ON c.id_localidad_id = l.id_localidad
		LEFT JOIN provincia p ON l.id_provincia_id = p.id_provincia
	WHERE
		cv.libro_iva;

-- ============================================
-- Percepciones por Vendedor - Totales.
-- Modelo: VLPercepIBVendedorTotales
-- ============================================
CREATE VIEW VLPercepIBVendedorTotales AS 
	SELECT 
		f.id_factura,
		c.id_vendedor_id,
		v.nombre_vendedor,
		f.fecha_comprobante,
		ROUND(f.gravado * cv.mult_venta * 1.0, 2) AS neto,
		ROUND(f.percep_ib * cv.mult_venta * 1.0, 2) AS percep_ib
	FROM
		factura f
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente 
		JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
	WHERE
		f.percep_ib <> 0
		AND cv.mult_venta <> 0;

-- ============================================
-- Percepciones por Vendedor - Detallado.
-- Modelo: VLPercepIBVendedorDetallado
-- ============================================
CREATE VIEW VLPercepIBVendedorDetallado AS
	SELECT 
		f.id_factura,
		c.id_vendedor_id,
		v.nombre_vendedor,
		cv.nombre_comprobante_venta,
		f.letra_comprobante,
		f.numero_comprobante,
		f.fecha_comprobante,
		(cv.codigo_comprobante_venta || '  ' || f.letra_comprobante || '  ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.id_cliente_id,
		c.nombre_cliente,
		c.cuit,
		f.gravado * cv.mult_venta AS neto,
		f.percep_ib * cv.mult_venta AS percep_ib,
		f.no_estadist
	FROM
		factura f
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente 
		JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
	WHERE
		f.percep_ib <> 0
		AND cv.mult_venta <> 0;

-- ============================================
-- Percepciones por Sub Cuenta - Totales.
-- Modelo: VLPercepIBSubcuentaTotales
-- ============================================
CREATE VIEW VLPercepIBSubcuentaTotales AS 
	SELECT 
		f.id_factura,
		f.fecha_comprobante,
		c.sub_cuenta,
		p.nombre_cliente AS nombre_cliente_padre,
		f.id_cliente_id,
		c.nombre_cliente,
		ROUND(f.gravado * cv.mult_venta * 1.0, 2) AS neto,
		ROUND(f.percep_ib * cv.mult_venta * 1.0, 2) AS percep_ib
	FROM
		factura f
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente 
		LEFT JOIN cliente p ON c.sub_cuenta = p.id_cliente 
	WHERE
		f.percep_ib <> 0
		AND cv.mult_venta <> 0;

-- ============================================
-- Percepciones por Sub Cuenta - Detallado.
-- Modelo: VLPercepIBSubcuentaDetallado
-- ============================================
CREATE VIEW VLPercepIBSubcuentaDetallado AS 
	SELECT 
		f.id_factura,
		c.sub_cuenta,
		p.nombre_cliente AS nombre_cliente_padre,
		cv.codigo_comprobante_venta,
		f.letra_comprobante,
		f.numero_comprobante,
		f.fecha_comprobante,
		(cv.codigo_comprobante_venta || '  ' || f.letra_comprobante || '  ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.id_cliente_id,
		c.nombre_cliente,
		c.cuit,
		f.gravado * cv.mult_venta AS neto,
		f.percep_ib * cv.mult_venta AS percep_ib,
		f.no_estadist
	FROM
		factura f
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		LEFT JOIN cliente p ON c.sub_cuenta = p.id_cliente
	WHERE
		f.percep_ib <> 0
		AND cv.mult_venta <> 0
	GROUP BY
		c.sub_cuenta, f.numero_comprobante;

-- ============================================
-- Comisiones a Vendedores según Facturas.
-- Modelo: VLComisionVendedor
-- ============================================
CREATE VIEW VLComisionVendedor AS 
	SELECT 
		f.id_factura,
		(cv.codigo_comprobante_venta || '  ' || f.letra_comprobante || '  ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.fecha_comprobante,
		f.id_cliente_id,
		c.nombre_cliente,
		'' AS reventa,
		0 AS id_producto_id,
		'' AS medida,
		0 AS id_marca_id,
		'' AS nombre_producto_marca,
		0 AS id_familia_id,
		'' AS nombre_producto_familia,
		0 AS cantidad,
		0 AS precio,
		0 AS costo,
		0 AS descuento,
		ROUND(f.total / (((SELECT alicuota_iva FROM codigo_alicuota WHERE codigo_alicuota = '0005')/100.0)+1), 2) AS gravado,
		f.total,
		0 AS no_estadist,
		CASE
			WHEN f.comision = 'C' THEN v.pje_camion
			ELSE v.pje_auto
		END AS pje_comision,
		c.id_vendedor_id,
		v.nombre_vendedor,
		'R' AS consulta
	FROM
		factura f
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
	WHERE
		(f.compro = 'RC' OR f.compro = 'RB' OR f.compro = 'RE');

-- ============================================
-- Comisiones a Vendedores según Facturas (Detalle).
-- Modelo: VLComisionVendedorDetalle
-- ============================================
CREATE VIEW VLComisionVendedorDetalle AS 
	SELECT 
		f.id_factura,
		(cv.codigo_comprobante_venta || '  ' || f.letra_comprobante || '  ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.fecha_comprobante,
		f.id_cliente_id,
		c.nombre_cliente,
		df.reventa,
		df.id_producto_id,
		p.medida,
		p.id_marca_id,
		pm.nombre_producto_marca,
		p.id_familia_id,
		pf.nombre_producto_familia,
		df.cantidad,
		df.precio,
		df.costo,
		df.descuento,
		df.gravado * cv.mult_comision AS gravado,
		df.total * cv.mult_comision AS total,
		f.no_estadist,
		COALESCE(ROUND((SELECT 
				dvc.comision_porcentaje
			FROM vendedor_comision vc
				JOIN detalle_vendedor_comision dvc ON dvc.id_vendedor_comision_id = vc.id_vendedor_comision
			WHERE vc.id_vendedor_id = c.id_vendedor_id
				AND dvc.id_familia_id = p.id_familia_id
				AND dvc.id_marca_id = p.id_marca_id
			LIMIT 1), 2), 0) AS pje_comision,
		c.id_vendedor_id,
		v.nombre_vendedor,
		'C' AS consulta
	FROM 
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		JOIN producto_marca pm ON p.id_marca_id = pm.id_producto_marca
	WHERE 
		cv.mult_comision <> 0
		AND f.no_estadist <> True;

-- ============================================
-- Comisiones a Operarios.
-- Modelo: VLComisionOperario
-- ============================================
CREATE VIEW VLComisionOperario AS 
	SELECT 
		f.id_factura,
		df.id_operario_id,
		o.nombre_operario,
		f.compro,
		f.letra_comprobante,
		f.numero_comprobante,
		(f.compro || '  ' || f.letra_comprobante || '  ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.fecha_comprobante,
		df.id_producto_id,
		pf.nombre_producto_familia,
		p.nombre_producto,
		(df.total * cv.mult_estadistica) * 1.0 AS total,
		(pf.comision_operario) * 1.0 AS comision_operario,
		ROUND(((df.total * cv.mult_estadistica) * pf.comision_operario) / 100.0, 2) AS monto_comision
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN operario o ON df.id_operario_id = o.id_operario
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
	WHERE 
		pf.comision_operario <> 0
		AND cv.mult_estadistica <> 0;

-- ============================================
-- Diferencias de Precios en Facturación.
-- Modelo: VLPrecioDiferente
-- ============================================
CREATE VIEW VLPrecioDiferente AS 
	SELECT 
		f.id_factura,
		f.compro,
		f.letra_comprobante,
		f.numero_comprobante,
		(f.compro || '  ' || f.letra_comprobante || '  ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.fecha_comprobante,
		f.id_cliente_id,
		c.nombre_cliente,
		df.id_producto_id,
		p.nombre_producto,
		df.cantidad,
		df.precio,
		df.precio_lista,
		(df.precio - df.precio_lista) * 1.0 AS diferencia,
		df.descuento,
		ROUND(p.precio * p.descuento / 100, 2) AS adicional,
		c.id_vendedor_id,
		v.nombre_vendedor
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
	WHERE 
		f.no_estadist = False
		AND df.precio <> df.precio_lista;

-- ============================================
-- Resumen de Ventas Ing. Brutos Mercadolibre.
-- Modelo: VLVentasResumenIB
-- ============================================
CREATE VIEW VLVentasResumenIB AS 
	SELECT 
		f.id_factura,
		f.fecha_comprobante,
		f.gravado * cv.mult_venta AS gravado,
		f.iva * cv.mult_venta AS iva,
		f.total * cv.mult_venta AS total,
		c.id_provincia_id,
		p.nombre_provincia,
		f.suc_imp
	FROM
		factura f
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		LEFT JOIN provincia p ON c.id_provincia_id = p.id_provincia
	WHERE
		cv.libro_iva = True;

-- ============================================
-- Estadísticas de Ventas.
-- Modelo: VLEstadisticasVentas
-- ============================================
CREATE VIEW VLEstadisticasVentas AS 
	SELECT 
		f.id_factura, 
		df.id_producto_id, 
		pc.cai,
		p.nombre_producto,
		p.unidad,
		p.id_familia_id,
		pf.nombre_producto_familia, 
		p.id_modelo_id,
		pm.nombre_modelo,
		p.id_marca_id,
		m.nombre_producto_marca,
		df.cantidad * cv.mult_estadistica AS cantidad,
		ROUND(((df.cantidad * df.precio) + (df.cantidad * df.precio * df.descuento / 100.0)) * cv.mult_estadistica, 2) AS total,
		f.fecha_comprobante,
		f.id_cliente_id,
		f.id_sucursal_id
	FROM 
		detalle_factura df
		LEFT JOIN factura f ON df.id_factura_id = f.id_factura
		LEFT JOIN producto p ON df.id_producto_id = p.id_producto
		LEFT JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
		LEFT JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		LEFT JOIN producto_marca m ON p.id_marca_id = m.id_producto_marca
		LEFT JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
	WHERE 
		df.id_producto_id <> 0
		AND cv.mult_estadistica <> 0
		AND f.no_estadist = False;

-- ============================================
-- Estadísticas de Ventas Vendedor.
-- Modelo: VLEstadisticasVentasVendedor
-- ============================================
CREATE VIEW VLEstadisticasVentasVendedor AS 
	SELECT 
		f.id_factura, 
		df.id_producto_id, 
		p.nombre_producto,
		p.id_familia_id,
		pf.nombre_producto_familia, 
		p.id_modelo_id,
		pm.nombre_modelo,
		p.id_marca_id,
		m.nombre_producto_marca,
		df.cantidad * cv.mult_estadistica AS cantidad,
		ROUND(((df.cantidad * df.precio) + (df.cantidad * df.precio * df.descuento / 100.0)) * cv.mult_estadistica, 2) AS total,
		f.fecha_comprobante,
		p.id_marca_id,
		f.id_sucursal_id,
		f.id_vendedor_id
	FROM 
		detalle_factura df 
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
		JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		JOIN producto_marca m ON p.id_marca_id = m.id_producto_marca
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
	WHERE 
		df.id_producto_id <> 0
		AND cv.mult_estadistica <> 0
		AND f.no_estadist = False;

-- ============================================
-- Estadísticas de Ventas Vendedores Clientes.
-- Modelo: VLEstadisticasVentasVendedorCliente
-- ============================================
CREATE VIEW VLEstadisticasVentasVendedorCliente AS 
	SELECT 
		df.id_producto_id,
		p.nombre_producto,
		p.id_familia_id,
		pf.nombre_producto_familia, 
		p.id_modelo_id,
		pm.nombre_modelo,
		p.id_marca_id,
		m.nombre_producto_marca,
		df.cantidad * cv.mult_estadistica AS cantidad,
		ROUND(((df.cantidad * df.precio) + (df.cantidad * df.precio * df.descuento / 100.0)) * cv.mult_estadistica, 2) AS total,
		f.fecha_comprobante,
		f.id_sucursal_id,
		f.id_cliente_id,
		c.nombre_cliente,
		f.id_vendedor_id,
		v.nombre_vendedor,
		f.no_estadist
	FROM 
		detalle_factura df 
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
		JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		JOIN producto_marca m ON p.id_marca_id = m.id_producto_marca
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN vendedor v ON f.id_vendedor_id = v.id_vendedor
	WHERE 
		df.id_producto_id <> 0
		AND cv.mult_estadistica <> 0;

-- ============================================
-- Ventas de Productos según Condición.
-- Modelo: VLEstadisticasSegunCondicion
-- ============================================
CREATE VIEW VLEstadisticasSegunCondicion AS 
	SELECT
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_marca_id,
		pk.nombre_producto_marca,
		p.id_modelo_id,
		pm.nombre_modelo,
		df.id_producto_id, 
		p.nombre_producto,
		df.reventa,
		df.cantidad * cv.mult_estadistica AS cantidad,
		ROUND(((df.precio + (df.precio * df.descuento / 100.0)) * df.cantidad) * cv.mult_estadistica, 2) AS importe,
		df.costo * df.cantidad * cv.mult_estadistica AS costo,
		f.fecha_comprobante,
		f.id_sucursal_id
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura 
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		JOIN producto_marca pk ON p.id_marca_id = pk.id_producto_marca
		JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
	WHERE
		f.no_estadist = False
		AND cv.mult_estadistica <> 0;

-- ============================================
-- Estadísticas de Ventas por Marcas.
-- Modelo: VLEstadisticasVentasMarca
-- ============================================
CREATE VIEW VLEstadisticasVentasMarca AS 
	SELECT
		(f.compro || '  ' || f.letra_comprobante || '  ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.fecha_comprobante,
		f.id_cliente_id,
		df.id_producto_id,
		p.nombre_producto,
		p.medida,
		df.cantidad,
		df.precio,
		df.descuento,
		df.total,
		df.precio * df.cantidad * cv.mult_estadistica AS compra,
		f.id_sucursal_id,
		p.id_marca_id,
		pk.nombre_producto_marca,
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_modelo_id,
		pm.nombre_modelo
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN producto_marca pk ON p.id_marca_id = pk.id_producto_marca
		JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
	WHERE
		cv.mult_estadistica <> 0
		AND f.no_estadist <> True;

-- ============================================
-- Estadísticas de Ventas por Marcas Vendedor.
-- Modelo: VLEstadisticasVentasMarcaVendedor
-- ============================================
CREATE VIEW VLEstadisticasVentasMarcaVendedor AS 
	SELECT
		(f.compro || '  ' || f.letra_comprobante || '  ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.fecha_comprobante,
		f.id_cliente_id,
		df.id_producto_id,
		p.nombre_producto,
		p.medida,
		df.cantidad,
		df.costo * cv.mult_stock * -1 AS precio,
		df.descuento,
		(df.costo * df.cantidad) * (1 + (df.descuento / 100.0)) * cv.mult_estadistica AS total,
		f.id_sucursal_id,
		c.id_vendedor_id,
		p.id_marca_id,
		pk.nombre_producto_marca,
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_modelo_id,
		pm.nombre_modelo
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN producto_marca pk ON p.id_marca_id = pk.id_producto_marca
		JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
	WHERE
		cv.mult_estadistica <> 0
		AND f.no_estadist <> True;

-- ============================================
-- Estadísticas de clientes sin Ventas.
-- Modelo: VLClienteUltimaVenta
-- ============================================
CREATE VIEW VLClienteUltimaVenta AS 
	SELECT 
		f.id_cliente_id,
		c.nombre_cliente,
		MAX(f.fecha_comprobante) AS fecha_ultimo_comprobante,
		f.id_vendedor_id
	FROM
		factura f
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
	GROUP BY
		f.id_cliente_id
	ORDER BY
		f.id_cliente_id;

-- ============================================
-- Estadísticas de Ventas por Provincia.
-- Modelo: VLEstadisticasVentasProvincia
-- ============================================
CREATE VIEW VLEstadisticasVentasProvincia AS 
	SELECT 
		f.id_factura,
		df.id_producto_id,
		p.nombre_producto,
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_modelo_id,
		pm.nombre_modelo,
		p.id_marca_id,
		m.nombre_producto_marca,
		df.cantidad * cv.mult_estadistica AS cantidad,
		ROUND(((df.cantidad * df.precio) + (df.cantidad * df.precio * df.descuento / 100.0)) * cv.mult_estadistica, 2) AS total,
		f.fecha_comprobante,
		p.id_marca_id,
		f.id_sucursal_id,
		f.id_vendedor_id,
		pr.id_provincia,
		pr.nombre_provincia
	FROM 
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
		JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		JOIN producto_marca m ON p.id_marca_id = m.id_producto_marca
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		LEFT JOIN provincia pr ON c.id_provincia_id = pr.id_provincia
	WHERE 
		df.id_producto_id <> 0
		AND cv.mult_estadistica <> 0
		AND f.no_estadist = False;

-- ============================================
-- Comprobantes sin Estadísticas.
-- Modelo: VLVentaSinEstadistica
-- ============================================
CREATE VIEW VLVentaSinEstadistica AS 
	SELECT
		f.fecha_comprobante, 
		(f.compro || ' ' || f.letra_comprobante || ' ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante, 
		f.id_cliente_id,
		c.nombre_cliente,
		f.total,
		c.id_vendedor_id,
		v.nombre_vendedor,
		c.sub_cuenta,
		f.id_sucursal_id,
		s.nombre_sucursal
	FROM
		factura f
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN sucursal s ON f.id_sucursal_id = s.id_sucursal
		JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
	WHERE
		f.no_estadist = True;

-- ============================================
-- Tablas Dinámicas de Ventas - Ventas por Comprobantes.
-- Modelo: VLTablaDinamicaVentas
-- ============================================
CREATE VIEW VLTablaDinamicaVentas AS 
	SELECT
		s.nombre_sucursal,
		cv.nombre_comprobante_venta,
		f.fecha_comprobante,
		f.letra_comprobante,
		f.numero_comprobante,
		CASE
			WHEN f.remito IS NOT NULL AND f.remito != '' AND f.remito != '0000-00000000' THEN f.remito
			ELSE ''
		END AS remito,
		(f.compro || ' ' || f.letra_comprobante || ' ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante, 
		CASE f.condicion_comprobante
			WHEN 1 THEN 'Contado'
			WHEN 2 THEN 'Cta. Cte.'
			ELSE 'Desconocido'
		END AS condicion_comprobante,
		f.id_cliente_id,
		c.nombre_cliente,
		ti.codigo_iva AS sitiva,
		c.cuit,
		c.mayorista,
		f.gravado * cv.mult_venta AS gravado,
		f.exento * cv.mult_venta AS exento,
		f.iva * cv.mult_venta AS iva,
		f.percep_ib * cv.mult_venta AS percepcion,
		f.total * cv.mult_venta AS total,
		f.no_estadist,
		f.id_user_id,
		c.codigo_postal,
		l.nombre_localidad,
		p.nombre_provincia,
		v.nombre_vendedor,
		f.promo,
		cv.libro_iva,
		mo.nombre_marketing_origen
	FROM
		factura f
		LEFT JOIN cliente c ON f.id_cliente_id = c.id_cliente
		LEFT JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		LEFT JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
		LEFT JOIN sucursal s ON f.id_sucursal_id = s.id_sucursal
		LEFT JOIN localidad l ON c.id_localidad_id = l.id_localidad
		LEFT JOIN provincia p ON l.id_provincia_id = p.id_provincia
		LEFT JOIN tipo_iva ti ON c.id_tipo_iva_id = ti.id_tipo_iva
		LEFT JOIN marketing_origen mo ON f.id_marketing_origen_id = mo.id_marketing_origen;

-- ============================================
-- Tablas Dinámicas de Ventas - Detalle de Ventas por Productos.
-- Modelo: VLTablaDinamicaDetalleVentas
-- ============================================
CREATE VIEW VLTablaDinamicaDetalleVentas AS 
	SELECT
		df.id_factura_id,
		s.nombre_sucursal,
		cv.nombre_comprobante_venta,
		f.fecha_comprobante,
		f.letra_comprobante,
		f.numero_comprobante,
		CASE
			WHEN f.remito IS NOT NULL AND f.remito != '' AND f.remito != '0000-00000000' THEN f.remito
			ELSE ''
		END AS remito,
		(f.compro || ' ' || f.letra_comprobante || ' ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante, 
		CASE f.condicion_comprobante
			WHEN 1 THEN 'Contado'
			WHEN 2 THEN 'Cta. Cte.'
			ELSE 'Desconocido'
		END AS condicion_comprobante,
		f.id_cliente_id,
		c.nombre_cliente,
		ti.codigo_iva AS sitiva,
		c.cuit,
		c.mayorista,
		df.reventa,
		df.id_producto_id,
		pc.cai,
		p.nombre_producto,
		pm.nombre_producto_marca,
		pf.nombre_producto_familia,
		p.segmento,
		df.cantidad * cv.mult_venta AS cantidad,
		df.costo,
		df.precio,
		df.descuento,
		df.gravado * cv.mult_venta AS gravado,
		df.no_gravado * cv.mult_venta AS no_gravado,
		df.alic_iva,
		df.iva * cv.mult_venta AS iva,
		df.total * cv.mult_venta AS total,
		f.no_estadist,
		f.id_user_id,
		c.codigo_postal,
		l.nombre_localidad,
		pr.nombre_provincia,
		v.nombre_vendedor,
		df.id_operario_id,
		o.nombre_operario,
		f.promo,
		cv.libro_iva,
		mo.nombre_marketing_origen
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		JOIN producto_marca pm ON p.id_marca_id = pm.id_producto_marca
		JOIN operario o ON df.id_operario_id = o.id_operario
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
		JOIN sucursal s ON f.id_sucursal_id = s.id_sucursal
		LEFT JOIN localidad l ON c.id_localidad_id = l.id_localidad
		LEFT JOIN provincia pr ON l.id_provincia_id = pr.id_provincia
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
		JOIN tipo_iva ti ON c.id_tipo_iva_id = ti.id_tipo_iva
		JOIN marketing_origen mo ON f.id_marketing_origen_id = mo.id_marketing_origen;

-- ============================================
-- Tablas Dinámicas de Ventas - Tablas para Estadísticas.
-- Modelo: VLTablaDinamicaEstadistica
-- ============================================
CREATE VIEW VLTablaDinamicaEstadistica AS 
	SELECT
		df.id_factura_id,
		s.nombre_sucursal,
		cv.nombre_comprobante_venta,
		f.fecha_comprobante,
		f.letra_comprobante,
		f.numero_comprobante,
		CASE
			WHEN f.remito IS NOT NULL AND f.remito != '' AND f.remito != '0000-00000000' THEN f.remito
			ELSE ''
		END AS remito,
		(f.compro || ' ' || f.letra_comprobante || ' ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante, 
		CASE f.condicion_comprobante
			WHEN 1 THEN 'Contado'
			WHEN 2 THEN 'Cta. Cte.'
			ELSE 'Desconocido'
		END AS condicion_comprobante,
		f.id_cliente_id,
		c.nombre_cliente,
		ti.codigo_iva AS sitiva,
		c.cuit,
		c.mayorista,
		df.reventa,
		df.id_producto_id,
		pc.cai,
		p.nombre_producto,
		pm.nombre_producto_marca,
		pf.nombre_producto_familia,
		p.segmento,
		df.cantidad * cv.mult_estadistica AS cantidad,
		df.costo,
		df.precio,
		df.descuento,
		df.gravado * cv.mult_estadistica AS gravado,
		df.no_gravado * cv.mult_estadistica AS no_gravado,
		df.alic_iva,
		df.iva * cv.mult_estadistica AS iva,
		df.total * cv.mult_estadistica AS total,
		f.no_estadist,
		f.id_user_id,
		c.codigo_postal,
		l.nombre_localidad,
		pr.nombre_provincia,
		v.nombre_vendedor,
		df.id_operario_id,
		o.nombre_operario,
		f.promo,
		cv.libro_iva,
		mo.nombre_marketing_origen
	FROM
		detalle_factura df
		JOIN factura f ON df.id_factura_id = f.id_factura
		JOIN producto p ON df.id_producto_id = p.id_producto
		JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		JOIN producto_marca pm ON p.id_marca_id = pm.id_producto_marca
		JOIN operario o ON df.id_operario_id = o.id_operario
		JOIN cliente c ON f.id_cliente_id = c.id_cliente
		JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
		JOIN vendedor v ON c.id_vendedor_id = v.id_vendedor
		JOIN sucursal s ON f.id_sucursal_id = s.id_sucursal
		LEFT JOIN localidad l ON c.id_localidad_id = l.id_localidad
		LEFT JOIN provincia pr ON l.id_provincia_id = pr.id_provincia
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
		JOIN tipo_iva ti ON c.id_tipo_iva_id = ti.id_tipo_iva
		JOIN marketing_origen mo ON f.id_marketing_origen_id = mo.id_marketing_origen
	WHERE
		cv.mult_estadistica <> 0
		AND f.no_estadist = False;

-- ============================================
-- Lista de Precios.
-- Modelo: VLLista
-- ============================================
CREATE VIEW VLLista AS 
	SELECT
		p.id_producto,
		p.id_cai_id,
		pc.cai,
		p.tipo_producto,
		p.medida,
		p.segmento,
		p.unidad,
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_modelo_id,
		pm.nombre_modelo,
		p.nombre_producto,
		p.id_marca_id,
		px.nombre_producto_marca,
		p.precio,
		p.costo,
		p.descuento,
		p.id_alicuota_iva_id,
		ca.alicuota_iva,
		p.minimo,
		p.despacho_1,
		p.despacho_2,
		p.fecha_fabricacion,
		p.id_producto_estado_id,
		pe.nombre_producto_estado,
		p.descripcion_producto,
		p.carrito,
		p.obliga_operario,
		p.iva_exento
	FROM 
		producto p
		LEFT JOIN producto_marca px ON p.id_marca_id = px.id_producto_marca
		LEFT JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		LEFT JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
		LEFT JOIN producto_estado pe ON p.id_producto_estado_id = pe.id_producto_estado
		LEFT JOIN codigo_alicuota ca ON p.id_alicuota_iva_id = ca.id_alicuota_iva;

-- ============================================
-- Lista de Precios a Revendedor.
-- Modelo: VLListaRevendedor
-- ============================================
CREATE VIEW VLListaRevendedor AS 
	SELECT
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_marca_id,
		px.nombre_producto_marca,
		p.id_modelo_id,
		pm.nombre_modelo,
		p.id_producto,
		p.id_cai_id,
		pc.cai,
		p.medida,
		p.nombre_producto,
		p.precio AS contado,
		p.precio AS precio30,
		p.precio AS precio90,
		p.precio AS precio120
	FROM 
		producto p
		LEFT JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		LEFT JOIN producto_marca px ON p.id_marca_id = px.id_producto_marca
		LEFT JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai;

-- ============================================
-- Listado de Stock por Sucursal.
-- Modelo: VLStockSucursal
-- ============================================
CREATE VIEW VLStockSucursal AS 
	SELECT
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_modelo_id,
		pm.nombre_modelo,
		p.id_marca_id,
		px.nombre_producto_marca,
		ps.id_producto_id,
		p.id_cai_id,
		pc.cai,
		p.medida,
		p.nombre_producto,
		ps.stock,
		p.costo * ps.stock AS costo_inventario,
		ps.id_deposito_id
	FROM
		producto_stock ps
		LEFT JOIN producto p ON ps.id_producto_id = p.id_producto
		LEFT JOIN producto_marca px ON p.id_marca_id = px.id_producto_marca
		LEFT JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		LEFT JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
	WHERE
		ps.stock <> 0;

-- ============================================
-- Stock General por Sucursal.
-- Modelo: VLStockGeneralSucursal
-- ============================================
CREATE VIEW VLStockGeneralSucursal AS 
	SELECT 1 AS dummy;

-- ============================================
-- Listado de Stock a Fecha.
-- Modelo: VLStockFecha
-- ============================================
CREATE VIEW VLStockFecha AS 
	SELECT
		ROW_NUMBER() OVER() AS id,
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_modelo_id,
		pm.nombre_modelo,
		p.id_marca_id,
		px.nombre_producto_marca,
		ps.id_producto_id,
		p.id_cai_id,
		pc.cai,
		p.medida,
		p.nombre_producto,
		SUM(ps.stock) AS stock
	FROM
		producto_stock ps
		LEFT JOIN producto p ON ps.id_producto_id = p.id_producto
		LEFT JOIN producto_marca px ON p.id_marca_id = px.id_producto_marca
		LEFT JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		LEFT JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
	WHERE
		p.tipo_producto = 'P' AND
		ps.stock <> 0
	GROUP BY
		ps.id_producto_id
	HAVING
		SUM(ps.stock) <> 0
	ORDER BY
		p.id_familia_id, p.id_modelo_id, p.id_marca_id, ps.id_producto_id;

-- ============================================
-- Listado de Stock Único.
-- Modelo: VLStockUnico
-- ============================================
CREATE VIEW VLStockUnico AS 
	SELECT
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_modelo_id,
		pm.nombre_modelo,
		p.id_marca_id,
		px.nombre_producto_marca,
		ps.id_producto_id,
		p.id_cai_id,
		pc.cai,
		p.medida,
		p.nombre_producto,
		SUM(ps.stock) AS stock
	FROM
		producto_stock ps
		LEFT JOIN producto p ON ps.id_producto_id = p.id_producto
		LEFT JOIN producto_marca px ON p.id_marca_id = px.id_producto_marca
		LEFT JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		LEFT JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
	WHERE
		ps.stock <> 0
	GROUP BY
		ps.id_producto_id
	HAVING
		SUM(ps.stock) <> 0;

-- ============================================
-- Reposición de Stock.
-- Modelo: VLReposicionStock
-- ============================================
CREATE VIEW VLReposicionStock AS 
	SELECT 1 AS dummy;

-- ============================================
-- Movimiento Interno de Stock.
-- Modelo: VLMovimientoInternoStock
-- ============================================
CREATE VIEW VLMovimientoInternoStock AS
	SELECT
		f.fecha_comprobante,
		f.numero_comprobante,
		(f.compro || '  ' || f.letra_comprobante || '  ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		f.observa_comprobante,
		df.id_producto_id,
		p.medida,
		p.id_marca_id,
		pm.nombre_producto_marca,
		p.nombre_producto,
		df.cantidad,
		f.id_deposito_id
	FROM
		detalle_factura df
		INNER JOIN factura f ON df.id_factura_id = f.id_factura
		INNER JOIN producto p ON df.id_producto_id = p.id_producto
		INNER JOIN producto_marca pm ON p.id_marca_id = pm.id_producto_marca
		INNER JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
	WHERE
		cv.interno = 1;

-- ============================================
-- Stock por Cliente en Depósito.
-- Modelo: VLStockCliente
-- ============================================
CREATE VIEW VLStockCliente AS 
	SELECT
		f.id_cliente_id,
		sc.id_stock_cliente,
		c.nombre_cliente,
		sc.id_producto_id,
		p.medida,
		pc.cai,
		sc.cantidad,
		sc.retirado,
		(sc.cantidad - sc.retirado) AS stock,
		(f.compro || '  ' || f.letra_comprobante || '  ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5) || '  ' || TO_CHAR(f.fecha_comprobante, 'DD/MM/YYYY')) AS comprobante,
		f.id_sucursal_id,
		f.id_vendedor_id
	FROM
		stock_cliente sc
		INNER JOIN factura f ON sc.id_factura_id = f.id_factura
		INNER JOIN producto p ON sc.id_producto_id = p.id_producto
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
		INNER JOIN cliente c ON f.id_cliente_id = c.id_cliente
	WHERE
		sc.cantidad <> sc.retirado;

-- ============================================
-- Stock en Depósitos de Clientes.
-- Modelo: VLStockDeposito
-- ============================================
CREATE VIEW VLStockDeposito AS
	SELECT
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_modelo_id,
		pm.nombre_modelo,
		p.id_marca_id,
		px.nombre_producto_marca,
		sc.id_producto_id,
		p.medida,
		pc.cai,
		p.nombre_producto,
		SUM(sc.cantidad - sc.retirado) AS stock,
		f.id_sucursal_id
	FROM
		stock_cliente sc
		INNER JOIN producto p ON sc.id_producto_id = p.id_producto
		INNER JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		INNER JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
		INNER JOIN producto_marca px ON p.id_marca_id = px.id_producto_marca
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
		INNER JOIN factura f ON sc.id_factura_id = f.id_factura
	WHERE
		sc.cantidad <> sc.retirado
	GROUP BY
		sc.id_producto_id
	HAVING
		SUM(sc.cantidad - sc.retirado) <> 0;

-- ============================================
-- Ficha de Seguimiento de Stock por Código o CAI.
-- Modelo: VLFichaSeguimientoStock
-- ============================================
CREATE VIEW VLFichaSeguimientoStock AS 
	SELECT
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
		-- Consulta VENTAS
		SELECT
			df.id_producto_id,
			p.id_cai_id,
			pc.cai,
			p.medida,
			p.nombre_producto,
			p.id_marca_id,
			pm.nombre_producto_marca,
			f.fecha_comprobante,
			(f.compro || ' ' || f.letra_comprobante || ' ' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(f.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
			(df.cantidad * cv.mult_stock) AS cantidad,
			COALESCE(df.precio, 0.0)::DECIMAL AS precio,
			COALESCE(df.total, 0.0)::DECIMAL AS total,
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
		
		UNION ALL
		
		-- Consulta COMPRAS
		SELECT
			dc.id_producto_id,
			p.id_cai_id,
			pc.cai,
			p.medida,
			p.nombre_producto,
			p.id_marca_id,
			pm.nombre_producto_marca,
			c.fecha_comprobante,
			(c.compro || ' ' || c.letra_comprobante || ' ' || SUBSTRING(LPAD(c.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(c.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
			(dc.cantidad * cc.mult_stock) AS cantidad,
			COALESCE(dc.precio, 0.0)::DECIMAL AS precio,
			COALESCE(dc.total, 0.0)::DECIMAL AS total, 
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
	) AS consulta_unida;

-- ============================================
-- Detalle de Compras por Proveedor.
-- Modelo: VLDetalleCompraProveedor
-- ============================================
CREATE VIEW VLDetalleCompraProveedor AS
	SELECT
		c.id_proveedor_id,
		pv.nombre_proveedor,
		(cc.codigo_comprobante_compra || '  ' || c.letra_comprobante || '  ' || SUBSTRING(LPAD(c.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(c.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		c.fecha_comprobante,
		p.id_cai_id,
		pc.cai,
		dc.id_producto_id,
		p.nombre_producto,
		p.id_familia_id,
		pf.nombre_producto_familia,
		p.id_marca_id,
		pm.nombre_producto_marca,
		dc.cantidad,
		p.unidad,
		dc.precio,
		dc.total,
		c.id_sucursal_id,
		s.nombre_sucursal,
		c.id_deposito_id,
		pd.nombre_producto_deposito
	FROM
		detalle_compra dc
		INNER JOIN compra c ON dc.id_compra_id = c.id_compra
		INNER JOIN comprobante_compra cc ON c.id_comprobante_compra_id = cc.id_comprobante_compra
		INNER JOIN producto p ON dc.id_producto_id = p.id_producto
		INNER JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
		INNER JOIN producto_marca pm ON p.id_marca_id = pm.id_producto_marca
		INNER JOIN proveedor pv ON c.id_proveedor_id = pv.id_proveedor
		INNER JOIN sucursal s ON c.id_sucursal_id = s.id_sucursal
		INNER JOIN producto_deposito pd ON c.id_deposito_id = pd.id_producto_deposito
		LEFT JOIN producto_cai pc ON p.id_cai_id = pc.id_cai;

-- ============================================
-- Comprobantes Ingresados.
-- Modelo: VLCompraIngresada
-- ============================================
CREATE VIEW VLCompraIngresada AS
	SELECT
		c.fecha_comprobante,
		cc.codigo_comprobante_compra,
		cc.nombre_comprobante_compra,
		(cc.codigo_comprobante_compra || '  ' || c.letra_comprobante || '  ' || SUBSTRING(LPAD(c.numero_comprobante::TEXT, 12, '0'), 1, 4) || '-' || SUBSTRING(LPAD(c.numero_comprobante::TEXT, 12, '0'), 5)) AS comprobante,
		c.id_proveedor_id,
		p.nombre_proveedor,
		c.total,
		c.observa_comprobante
	FROM
		compra c
		INNER JOIN comprobante_compra cc ON c.id_comprobante_compra_id = cc.id_comprobante_compra
		INNER JOIN proveedor p ON c.id_proveedor_id = p.id_proveedor;

-- ============================================
-- Stock Mínimo por CAI.
-- Modelo: VLProductoMinimo
-- ============================================
CREATE VIEW VLProductoMinimo AS 
	SELECT
		pm.id_cai_id,
		pc.cai, 
		pm.id_deposito_id, 
		d.nombre_producto_deposito, 
		pm.minimo
	FROM
		producto_minimo pm
		JOIN producto_cai pc ON pm.id_cai_id = pc.id_cai
		JOIN producto_deposito d ON pm.id_deposito_id = d.id_producto_deposito;

-- ============================================
-- VERIFICACIÓN FINAL
-- ============================================
DO $$
DECLARE
    vista RECORD;
    total_vistas INTEGER := 0;
BEGIN
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'VERIFICACIÓN DE VISTAS CREADAS';
    RAISE NOTICE '==========================================';
    
    FOR vista IN 
        SELECT schemaname, viewname 
        FROM pg_views 
        WHERE schemaname = 'public' 
        AND viewname LIKE 'VL%'
        ORDER BY viewname
    LOOP
        total_vistas := total_vistas + 1;
        RAISE NOTICE '✅ %', vista.viewname;
    END LOOP;
    
    RAISE NOTICE '==========================================';
    RAISE NOTICE 'Total de vistas creadas: %', total_vistas;
    RAISE NOTICE '==========================================';
END $$;
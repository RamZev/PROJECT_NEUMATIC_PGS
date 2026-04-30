-- FICHA DE SEGUIMIENTO DE STOCK.
-- POR CÓDIGO DE PRODUCTO

-- Consultas SQL en VFP

-- Select de ventas:
SELECT Detven.codigo, Detven.compro, Detven.letra, Detven.numero,;
	Facturas.fecha, Detven.cantidad*Codven.mult_sto AS cantidad,;
	Detven.precio, Detven.total, Facturas.cliente, "V" AS marca,;
	Facturas.noestadist, Facturas.sucursal, Facturas.deposito;
FROM detven
	INNER JOIN codven ON  Detven.compro = Codven.compro;
	INNER JOIN facturas ON  Detven.id = Facturas.id ;
WHERE Codven.mult_sto <> 0;
	AND Detven.codigo = ?nCodigo;
	AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta;
ORDER BY Facturas.fecha

 
-- Select de Compras
SELECT Detcom.codigo, Detcom.compro, Detcom.letra, Detcom.numero,;
	Compras.fecha, Detcom.cantidad*Codcom.mult_sto AS cantidad,;
	Detcom.precio, Detcom.total, Compras.proveedor, "C" AS marca,;
	Compras.sucursal, Compras.deposito;
FROM compras!compras,;
	detcom INNER JOIN compras!codcom ;
	ON  Detcom.compro = Codcom.codigo;
WHERE Detcom.id = Compras.id;
	AND (Codcom.mult_sto <> 0;
	AND Detcom.codigo = ?nCodigo;
	AND Compras.fecha BETWEEN ?dDesde AND ?dHasta);
ORDER BY Compras.fecha


-- Select de Movimientos Internos
SELECT Detven.codigo, Detven.compro, Detven.letra, Detven.numero,;
	Movstock.fecha, Detven.cantidad, Detven.precio, Detven.total, 0 AS cliente,;
	"V" AS marca, Movstock.sucursal, Movstock.deposito;
FROM detven
	INNER JOIN movstock ON Detven.id = Movstock.id;
WHERE Detven.codigo = ?nCodigo;
	AND Movstock.fecha BETWEEN ?dDesde AND ?dHasta;
ORDER BY Movstock.fecha


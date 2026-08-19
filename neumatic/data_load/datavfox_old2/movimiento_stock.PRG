CLOSE TABLES ALL 
nCodigo = 84513
dDesde = {01/06/25}
dHasta = DATE()

SELECT detven.id, detven.compro, detven.letra, detven.numero, facturas.fecha, facturas.cliente, facturas.nombre, facturas.sucursal, facturas.deposito, detven.cantidad*codven.mult_sto as cantidad, detven.stock ;
	from detven LEFT JOIN facturas ON detven.id = facturas.id ;
				LEFT JOIN codven ON detven.compro = codven.codigo ;
	WHERE detven.compro # 'MI' AND codven.mult_sto#0 AND detven.codigo = nCodigo AND facturas.fecha BETWEEN dDesde AND dHasta ;
	INTO CURSOR ltVentas
COPY TO Mov_Ventas.xls TYPE FOX2X 

SELECT detcom.id, compras.compro, compras.letra, compras.numero, compras.fecha, compras.proveedor as cliente, 'COMPRAS' as nombre, compras.sucursal, compras.deposito, detcom.cantidad*codcom.mult_sto as cantidad, detcom.stock ;
	from detcom LEFT JOIN compras ON detcom.id = compras.id ;
				LEFT JOIN codcom ON compras.compro = codcom.compro ;
	WHERE codcom.mult_sto#0 AND detcom.codigo = nCodigo  AND compras.fecha BETWEEN dDesde AND dHasta ;
	INTO CURSOR ltcompras
COPY TO Mov_Compras.xls TYPE FOX2X 

SELECT detven.id, detven.compro, detven.letra, detven.numero, movstock.fecha, 0 as cliente, 'MOV.STOCK' AS nombre, movstock.sucursal, movstock.deposito, detven.cantidad, detven.stock ;
	from detven LEFT JOIN movstock ON detven.id = movstock.id ;
	WHERE detven.compro = 'MI' AND detven.codigo = nCodigo AND movStock.fecha BETWEEN dDesde AND dHasta;
	INTO CURSOR ltMovStock
COPY TO Mov_Stock.xls TYPE FOX2X 

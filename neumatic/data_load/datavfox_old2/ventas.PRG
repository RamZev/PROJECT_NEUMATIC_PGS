CLOSE TABLES ALL 
CLOSE DATABASES ALL 
CLEAR  

USE facturas ORDER id IN 0
USE detven ORDER id IN 0
USE codven ORDER codigo IN  0
USE lista ORDER codigo IN 0
USE marcas ORDER codigo IN 0
USE modelos ORDER codigo IN 0
USE clientes ORDER codigo IN 0 
USE vendedor ORDER codigo IN 0 
USE articulo ORDER codigo IN 0 
USE sucursal ORDER id IN 0 

dDesde={01/07/24}
dHasta={31/07/24}


*----------- Totales sin intervenir otras tablas para saber el importe total real
SELECT facturas.*,facturas.gravado*codven.mult_ven FROM facturas,codven ;
	WHERE facturas.compro=codven.compro AND fecha between dDesde AND dHasta AND codven.libroiva ;
	INTO CURSOR ltVentas0 ORDER BY  facturas.id
SELECT ltVentas0 
?"Totales sin intervenir otras tablas para saber el importe total real"
SUM gravado TO g 
GO BOTTOM 
?g
?RECCOUNT()

*----------- Totales Full por comprobantes Impositovos
SELECT sucursal.nombre AS Sucursal, codven.nombre AS Comprobante, facturas.fecha, facturas.letra, facturas.numero, facturas.condicion, facturas.cliente, clientes.nombre AS Nombre_Cliente, clientes.mayorista, ;
	facturas.gravado*codven.mult_ven AS Gravado, facturas.iva*codven.mult_ven AS IVA, facturas.percepib*codven.mult_ven AS Percepcion, facturas.total*codven.mult_ven AS Total, facturas.noEstadist, facturas.operador, clientes.codpostal, localida.localidad, localida.provincia, vendedor.nombre AS Vendedor, facturas.codcomis;
	FROM facturas,clientes,codven, vendedor, sucursal, localida ;
	WHERE facturas.sucursal=sucursal.id AND facturas.compro=codven.compro AND facturas.cliente=clientes.codigo AND clientes.vendedor=vendedor.codigo AND clientes.codpostal=localida.codigo AND fecha between dDesde AND dHasta AND codven.libroiva ;
	INTO CURSOR ltVentas ORDER BY  facturas.id
?"Totales Full por comprobantes Impositovos"
SELECT ltVentas 
SUM gravado TO g 
GO BOTTOM 
?g
?RECCOUNT()

*----------- Totales Full todos tipo de comprobantes 
SELECT sucursal.nombre AS Sucursal, codven.nombre AS Comprobante, facturas.fecha, facturas.letra, facturas.numero, facturas.condicion, facturas.cliente, clientes.nombre AS Nombre_Cliente, clientes.mayorista, ;
	facturas.gravado*codven.mult_ven AS Gravado, facturas.iva*codven.mult_ven AS IVA, facturas.percepib*codven.mult_ven AS Percepcion, facturas.total*codven.mult_ven AS Total, facturas.noEstadist, facturas.operador, clientes.codpostal, localida.localidad, localida.provincia, vendedor.nombre AS Vendedor, facturas.codcomis ;
	FROM facturas,clientes,codven, vendedor, sucursal, localida ;
	WHERE facturas.sucursal=sucursal.id AND facturas.compro=codven.compro AND facturas.cliente=clientes.codigo AND clientes.vendedor=vendedor.codigo AND clientes.codpostal=localida.codigo AND fecha between dDesde AND dHasta  ;
	INTO CURSOR tablaVentas ORDER BY  facturas.id
		
?"Totales Full todos tipo de comprobantes "
SELECT tablaVentas 
SUM gravado TO g 
GO BOTTOM 
?g
?RECCOUNT()


*----------- Totales Full con detelle de ventas y todos tipo de comprobantes 
SELECT detven.id, codven.nombre AS Comprobante, detven.letra, detven.numero, facturas.fecha, facturas.condicion, facturas.cliente, clientes.nombre AS Nombre_Cliente, clientes.mayorista, clientes.codpostal, localida.localidad, localida.provincia, vendedor.nombre AS Vendedor, ;
		detven.codigo, lista.nombre as producto, marcas.nombre AS Marcas, articulo.nombre AS Familia, lista.segmento, detven.cantidad*codven.mult_ven AS Cantidad, detven.precio, detven.gravado*codven.mult_ven as GRAVADO, detven.total*codven.mult_ven as Total, ;
		facturas.noEstadist, facturas.codcomis, facturas.operador, sucursal.nombre AS Sucursal ;
	FROM detven, facturas, codven, lista, clientes, marcas, modelos, vendedor, articulo, sucursal, localida ;
	WHERE detven.id = facturas.id AND detven.compro = codven.compro AND detven.codigo = lista.codigo AND facturas.cliente = clientes.codigo AND lista.modelo = modelos.codigo AND lista.marca = marcas.codigo AND clientes.vendedor = vendedor.codigo AND lista.articulo = articulo.codigo ;
		AND  facturas.sucursal=sucursal.id AND clientes.codpostal=localida.codigo AND facturas.fecha betwee dDesde AND dHasta AND codven.libroiva ;
	INTO CURSOR ltVentasDetalle
?"Totales Full con detelle de ventas y todos tipo de comprobantes "
SELECT ltVentasDetalle 
SUM gravado TO g1
GO BOTTOM 
?g1
?RECCOUNT()

?g-g1

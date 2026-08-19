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

dDesde={01/07/24}
dHasta={31/07/24}
nDesdeMarca = 1 
nHastaMarca = 2
nDesdeArt = 1
nHastaArt = 2

SELECT detven.id, detven.compro, detven.letra, detven.numero, facturas.fecha, facturas.cliente, clientes.nombre, detven.codigo, lista.nombre as producto, marcas.nombre AS Marcas, articulo.nombre AS Familia, lista.segmento, detven.cantidad*codven.mult_ven AS Cantidad, detven.precio, detven.total*codven.mult_ven as Total, facturas.sucursal, facturas.operador, vendedor.nombre as vendedor ;
	from detven,facturas,codven, lista, clientes, marcas, modelos, vendedor, articulo ;
	WHERE detven.id = facturas.id AND detven.compro = codven.compro AND detven.codigo = lista.codigo AND facturas.cliente = clientes.codigo AND lista.modelo = modelos.codigo AND lista.marca = marcas.codigo AND clientes.vendedor = vendedor.codigo AND lista.articulo = articulo.codigo ;
	AND  facturas.fecha betwee dDesde AND dHasta AND detven.reventa="R" AND codven.libroiva AND lista.marca between nDesdeMarca AND nHastaMarca AND articulo Between nDesdeArt AND nHastaArt ;
	INTO CURSOR T1 ORDER BY cliente 
	
SELECT t1
BROWSE 
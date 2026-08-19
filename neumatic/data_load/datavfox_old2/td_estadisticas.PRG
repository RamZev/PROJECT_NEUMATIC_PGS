CLOSE TABLES ALL 

dDesde={01/07/24}
dHasta={31/07/24}

*---- Tabla Dinamica

SELECT detven.id, codven.nombre AS Comprobante, detven.letra, detven.numero, facturas.fecha, facturas.condicion, facturas.cliente, clientes.nombre AS Nombre_Cliente, clientes.mayorista, clientes.codpostal, localida.localidad, localida.provincia, vendedor.nombre AS Vendedor, ;
		detven.reventa, detven.codigo, lista.nombre as producto, marcas.nombre AS Marcas, articulo.nombre AS Familia, lista.segmento, detven.cantidad*codven.mult_stad AS Cantidad, detven.costo, detven.precio, detven.gravado*codven.mult_stad as GRAVADO, detven.total*codven.mult_stad as Total, ;
		facturas.noEstadist, facturas.codcomis, facturas.operador, sucursal.nombre AS Sucursal ;
	FROM detven, facturas, codven, lista, clientes, marcas, modelos, vendedor, articulo, sucursal, localida ;
	WHERE detven.id = facturas.id AND detven.compro = codven.compro AND detven.codigo = lista.codigo AND facturas.cliente = clientes.codigo AND lista.modelo = modelos.codigo AND lista.marca = marcas.codigo AND clientes.vendedor = vendedor.codigo AND lista.articulo = articulo.codigo ;
		AND  facturas.sucursal=sucursal.id AND clientes.codpostal=localida.codigo AND facturas.fecha betwee dDesde AND dHasta AND codven.mult_stad#0 AND !facturas.noestadist;
	INTO CURSOR ltVentas 
			
			
*---- Estasdisticas

*!*	SELECT detven.compro,detven.letra,detven.numero,facturas.fecha,detven.codigo,lista.articulo,lista.modelo,lista.marca,lista.nombre,lista.unidad,detven.cantidad,detven.precio,detven.descuento,facturas.cliente,lista.codfabrica FROM detven,facturas,lista,codven ;
*!*		WHERE detven.id=facturas.id.AND.detven.codigo=lista.codigo.AND.detven.compro=codven.compro ;
*!*		.AND.detven.codigo#0.AND.codven.mult_stad#0.AND.facturas.fecha BETWEEN dDesde.AND.dHasta.AND.!facturas.noestadist ;
*!*		INTO CURSOR T1 READWRITE ORDER BY 6,7,8,5
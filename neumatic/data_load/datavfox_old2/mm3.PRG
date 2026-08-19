*.*
*.* Selecciono todos los clientes que en algun momento hicieron ventas como Reventa
*.* luego controlo si esta bien el cursor creado
*.*
*.*
*.*
CLEAR 
CLOSE TABLES ALL 
USE facturas ORDER id IN 0 
USE detven   ORDER id IN 0 
USE clientes ORDER codigo IN 0 
USE lista    ORDER codigo IN 0 

SET DEFAULT TO D:\MAAS\DEBONA-SH\DATA
SELECT detven.id, facturas.cliente, clientes.* ;
	from detven INNER JOIN facturas  ON detven.id=facturas.id ;
		INNER JOIN clientes ON facturas.cliente = clientes.codigo ;
		INNER JOIN detven ON detven.codigo = lista.codigo ;
	GROUP BY 2 ORDER BY 2 ;
		WHERE detven.reventa='R' AND lista.articulo>=1 AND lista.articulo<=2 ;
	INTO CURSOR t1
*!*	SELECT detven.id, facturas.cliente ;
*!*		from detven INNER JOIN facturas  ON detven.id=facturas.id ;
*!*		WHERE detven.reventa='R' ;
*!*		GROUP BY 2 ORDER BY 2 ;
*!*		INTO CURSOR t1 READWRITE 

SELECT detven 
SET RELATION TO id INTO facturas

*------------------------------------------------- Controlo si todos los datos del Cursor creado tienen al menos una venta como reventa
SELECT t1
SCAN 
	SELECT detven 
	GO TOP 
	LOCATE FOR facturas.cliente = t1.cliente AND detven.reventa = 'R'
	IF EOF()
		?t1.cliente
	ENDIF 
	SELECT t1
ENDSCAN 


*------------------------------------------------- Controlo si todos las ventas con reventas existen en el Cursor creado
SELECT t1 
INDEX ON cliente TAG cliente
SELECT detven 
SCAN FOR detven.reventa = 'R'
	nCliente=facturas.cliente
	SELECT t1
	SEEK nCliente
	IF EOF()
		?'cliente', facturas.cliente
	ENDIF 
	SELECT detven 
	IF MOD(RECNO(),10000) = 0 
		?RECNO()
	ENDIF 
ENDSCAN 

*.*
*.*   Control de integridad detalle encabezado de Facturacion
*.*
SET DATE DMY 
SET STRICTDATE TO 0 
CLEAR 
CLOSE TABLES ALL 

dDesde = {01/12/24}
dHasta = {31/12/24}
STORE 0 TO nID, nTotFactura, nTotal, nGravado

USE codven   ORDER codigo IN 0 
USE facturas ORDER id IN 0 
USE detven   ORDER id IN 0 

SELECT detven
SET RELATION TO compro INTO codven, id INTO facturas
* ----- Total Gravado Detalle
SCAN FOR facturas.fecha>=dDesde AND Facturas.fecha<=dHasta AND codven.libroIVA
	IF detven.id # nID
		IF nTotal # nTotFactura
			?nID, nTotal, nTotFactura, nTotal-nTotFactura
		ENDIF 
		nTotFactura = Facturas.total - Facturas.percepIB
		nID = detven.id
		nTotal = 0
	ENDIF 
	nTotal = nTotal + detven.total
	nGravado = nGravado + (detven.Gravado*codven.mult_ven)
	SELECT detven
ENDSCAN 
?'Gravado Total Detalle', nGravado

SELECT detven
SET RELATION TO 
* ----- Total Gravado Facturas
SELECT facturas
SET RELATION TO compro INTO codven
STORE 0 TO nGravado
SCAN FOR facturas.fecha>=dDesde AND Facturas.fecha<=dHasta AND codven.libroIVA
	nGravado = nGravado + ((facturas.Gravado+facturas.exento)*codven.mult_ven)
	SELECT facturas
ENDSCAN 
?'Gravado Total', nGravado

*------------------ Diferencia entre FActuas y Detalle
STORE 0 TO nID, nGravado
SELECT facturas
SET RELATION TO compro INTO codven

SCAN FOR facturas.fecha>=dDesde AND Facturas.fecha<=dHasta AND codven.libroIVA
	nId=facturas.id
	nGravado=0
	SELECT detven
	SCAN FOR id=nID
		nGravado=nGravado+detven.gravado
	ENDSCAN  
	IF facturas.gravado # nGravado
		?nID, nGravado
	ENDIF 
	SELECT facturas
ENDSCAN 

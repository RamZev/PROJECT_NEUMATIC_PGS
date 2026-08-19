*.*
*.*   Control de integridad detalle encabezado de Facturacion
*.*
*!*	SET DATE DMY 
*!*	SET STRICTDATE TO 0 
CLEAR 
*!*	CLOSE TABLES ALL 

*!*	dDesde = {01/11/24}
*!*	dHasta = {30/11/24}
STORE 0 TO nID, nTotFactura, nTotal

*!*	USE codven   ORDER codigo IN 0 
*!*	USE facturas ORDER id IN 0 
*!*	USE detven   ORDER id IN 0 

SELECT ltVentasDet
SET RELATION TO id INTO ltVentas

SCAN 
	IF ltVentasDet.id # nID
		IF nTotal # nTotFactura
			?nID, nTotal, nTotFactura, nTotal-nTotFactura
		ENDIF 
		nTotFactura = ltVentas.total - ltVentas.percepcion
		nID = ltVentasDet.id
		nTotal = 0
	ENDIF 
	nTotal = nTotal + ltVentasDet.total
	SELECT ltVentasDet
ENDSCAN 

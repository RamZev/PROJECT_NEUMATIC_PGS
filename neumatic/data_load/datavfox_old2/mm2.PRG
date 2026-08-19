*
*   Control correlatividad de ID en Facturas
*

CLEAR 
CLOSE TABLES ALL 
SET DELETED ON

USE facturas ORDER id IN 0 

cDMY=INPUTBOX("Desde Fecha ","Controlar",DTOC(DATE()-30))
dDesde=CTOD(cDMY)
cDMY=INPUTBOX("Hasta Fecha ","Controlar",DTOC(DATE()))
dHasta=CTOD(cDMY)

nID=0
SELECT facturas
SCAN FOR fecha>=dDesde .AND. fecha<=dHasta
	IF facturas.id # nID
		?nID
		nID=facturas.id
	ENDIF 
	nID = nID + 1
	SELECT facturas
ENDSCAN 
CLOSE TABLES ALL 

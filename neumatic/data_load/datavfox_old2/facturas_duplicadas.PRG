*
*   Control de Facturas duplicadas por ID
*
CLEAR 
CLOSE TABLES ALL 
SET DELETED ON

USE facturas ORDER id IN 0 

AFIELDS(alCursor,"facturas")
CREATE CURSOR tlFacturas FROM ARRAY alCursor
RELEASE alCursor

cDMY=INPUTBOX("Desde Fecha ","Controlar",DTOC(DATE()-30))
dDesde=CTOD(cDMY)
cDMY=INPUTBOX("Hasta Fecha ","Controlar",DTOC(DATE()))
dHasta=CTOD(cDMY)

nID=0
SELECT facturas
SCAN FOR fecha>=dDesde .AND. fecha<=dHasta
	IF facturas.id=nID
		SCATTER MEMVAR 
		INSERT INTO tlFacturas FROM MEMVAR 
		?facturas.id, facturas.fecha
	ENDIF 
	SELECT facturas
	nID=facturas.id
ENDSCAN 
SELECT tlFacturas 
LIST off 
BROWSE 
CLOSE TABLES ALL 

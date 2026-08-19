CLOSE ALL
CLEAR ALL 
CLEAR 

nID=0
USE facturas ORDER id
SCAN FOR MONTH(fecha)=7 AND YEAR(fecha)=2025
	IF nID=facturas.id
		?nId
	ENDIF 
	nId=Facturas.id
	SELECT facturas
ENDSCAN 
CLOSE ALL 

CLOSE TABLES ALL 
SET EXCLUSIVE OFF 
SET TALK OFF 
SET DELETED ON 

CREATE CURSOR borrar (cai C(15))
USE lista ORDER codfabrica IN 0 
USE stock ORDER codigo IN 0 

cArchivo = GETFILE('csv')
APPEND FROM (cArchivo) DELIMITED WITH  CHARACTER ';'

SELECT borrar
SCAN 
	cCAI=borrar.cai
	SELECT lista
	SEEK cCAI
	IF FOUND()
		nCodigo = lista.codigo
		SELECT stock 
		DELETE FOR codigo=nCodigo
		SELECT lista
		DELETE 
	ENDIF 
	SELECT borrar
ENDSCAN 

SELECT lista
COUNT TO s FOR marca=30
?s


CLOSE ALL 

USE sinprecio IN 0 
USE lista ORDER codigo IN 0 
USE stock ORDER codigo IN 0 

SELECT sinprecio
SCAN 
	nCodigo = sinprecio.codigo
	IF SEEK(nCodigo ,"lista","codigo")
		SELECT lista
		?codigo,nombre
		DELETE 
	ENDIF 
	IF SEEK(sinprecio.codigo,"stock","codigo")
		SELECT stock 
		DELETE for codigo = nCodigo 
	ENDIF 
	SELECT sinprecio
ENDSCAN 

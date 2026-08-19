*.*
*.* Agrego nuevos producto en stock sin cantidades
*.*
CLOSE ALL 
SET EXCLUSIVE OFF 

USE lista ORDER codigo IN 0 
USE stock ORDER deposito IN 0 
USE listamin ORDER deposito IN 0 

SELECT lista
SCAN 
	*--------------------------------------- Agrego Stock 0 en depositos
	FOR i=1 TO 17
		cClave=STR(i,2)+STR(lista.codigo,6)
		IF !SEEK(cCLave,"stock","deposito")
			INSERT INTO stock (deposito,codigo,fecha) VALUES (i,lista.codigo,DATE())
		ENDIF 
	ENDFOR 
	
	*--------------------------------------- Agrego minimos en 0 por Despositos
	IF !EMPTY(lista.codfabrica)
		FOR i=1 TO 17
			cClave=STR(i,2)+lista.codfabrica
			IF !SEEK(cCLave,"listamin","deposito")
				INSERT INTO listamin (cai,deposito,minimo) VALUES (lista.codfabrica,i,0)
			ENDIF 
		ENDFOR 
		SELECT lista
	ENDIF 	

	SELECT lista
ENDSCAN 
CLOSE TABLES ALL 

CLOSE ALL 
CLEAR ALL 
CLEAR 
CLOSE TABLES ALL 

SET EXCLUSIVE ON 
SET DELETED ON
SET DATE DMY 
SET STRICTDATE TO 0

USE facturas ORDER id IN 0
USE detven   ORDER id IN 0 
USE codven   ORDER codigo IN 0 

dFecha = {31/12/2023}

SELECT cliente,sum(total*codven.mult_cli) as saldo ;
	FROM facturas, codven ;
	WHERE facturas.compro=codven.codigo AND fecha<=dFecha and codven.mult_cli#0 AND condicion=2;
	GROUP BY cliente ;
	INTO CURSOR T1

SELECT facturas
GO BOTTOM 
nID=id
nNro=0

SELECT T1
BROWSE FOR SALDO#0 NODELETE NOAPPEND NOMODIFY 

IF MESSAGEBOX("QUIERE PROCEDER AL AJUSTE DE CUENTAS",4+32+256,"VERIFICAR")=6
	SCAN FOR saldo#0
		nID=nID+1
		nNro=nNro+1
		INSERT INTO facturas (compro,letra,numero,fecha,cliente,condicion,total,sucursal,id,observa) ;
			VALUES ("ND","X",nNro,dFecha+1,t1.cliente,2,t1.saldo,1,nID,"AJUSTE DE CUENTA A LA FECHA")
	ENDSCAN 
	SELECT FACTURAS
	DELETE FOR fecha<=dFecha
	PACK
	SELECT detven
	SET RELATION TO id INTO facturas
	DELETE FOR EMPTY(facturas.id) 
	PACK 
ENDIF 

CLOSE TABLES ALL 
USE FACTURAS 
SORT TO FACT_ORD ON fecha

CLOSE TABLES ALL 
USE facturas EXCLUSIVE 
ZAP 
APPEND FROM fact_ord 

BROWSE




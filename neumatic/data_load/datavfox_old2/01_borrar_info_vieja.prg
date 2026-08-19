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
		INSERT INTO facturas (compro,letra,numero,fecha,cliente,condicion,total,entrega,estado,sucursal,id,observa) ;
			VALUES ("ND","X",nNro,dFecha+1,t1.cliente,2,t1.saldo,t1.saldo,'C',1,nID,"AJUSTE DE CUENTA A LA FECHA")
	ENDSCAN 
	SELECT FACTURAS
	DELETE FOR fecha<=dFecha
	PACK
	SELECT detven
	SET RELATION TO id INTO facturas
	DELETE FOR EMPTY(facturas.id) AND compro#'MI' 
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

*---------------------------------------------------- Borro Compras Viejas
CLOSE TABLES ALL 
*dFecha = {31/12/2023}

USE compras ORDER id IN 0 EXCLUSIVE 
USE detcom  ORDER id IN 0 EXCLUSIVE 

SELECT detcom 
SET RELATION TO id INTO compras
DELETE FOR compras.fecha<=dFecha
PACK 

SELECT compras 
DELETE FOR compras.fecha<=dFecha
PACK 
CLOSE TABLES ALL 

*---------------------------------------------------- Borro Mov Stock Viejos
CLOSE TABLES ALL 
*dFecha = {31/12/2023}

USE movStock ORDER id IN 0 EXCLUSIVE 
USE detven   ORDER id IN 0 EXCLUSIVE 

SELECT detven   
SET RELATION TO id INTO movStock 
DELETE FOR detven.compro='MI' AND movStock.fecha<=dFecha
PACK 

SELECT movStock
DELETE FOR movStock.fecha<=dFecha
PACK 
CLOSE TABLES ALL 


*---------------------------------------------------- Borro Mov Cajas Viejas
CLOSE TABLES ALL 

USE caja ORDER numero IN 0 EXCLUSIVE 
USE cajaDetalle ORDER caja IN 0 EXCLUSIVE 
USE cajaArqueo ORDER caja IN 0 EXCLUSIVE 

SELECT cajaDetalle 
SET RELATION TO caja INTO caja 
DELETE FOR caja.fecha<=dFecha
PACK 

SELECT cajaArqueo 
SET RELATION TO caja INTO caja 
DELETE FOR caja.fecha<=dFecha
PACK

SELECT caja
DELETE FOR fecha<=dFecha
PACK 
CLOSE TABLES ALL 

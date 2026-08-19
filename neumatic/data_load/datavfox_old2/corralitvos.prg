*.* 
*.* Control de correlatividad de Comprobantes Electronicos
*.*
CLOSE TABLES ALL 
SET EXCLUSIVE OFF
SET DELETED ON 
SET DATE DMY 
SET STRICTDATE TO 0 
CLEAR 
STORE '05' TO cMes
STORE '2025' TO cAnio
cMes = INPUTBOX('Ingreso el mes a controlar','Mes',cMes)
nMes = INT(VAL(cMes))
cAnio = INPUTBOX('Ingreso el año a controlar','Año',cAnio)
nAnio = INT(VAL(cAnio))

USE facturas ORDER numero
SELECT facturas.id, facturas.letra, facturas.numero, codven.codcitiA, codven.codcitiB, facturas.compro ;
	FROM facturas INNER JOIN codven ON facturas.compro = codven.compro AND codven.libroiva ;
	WHERE MONTH(fecha)=nMes AND YEAR(fecha)=nAnio ;
	ORDER BY facturas.letra,facturas.numero ;
	INTO CURSOR ltVentas

nPtoVta=0
nNumero=0
cCodCITIA=''
SELECT ltVentas
SCAN 
	IF nNumero#ltVentas.numero
		IF cCodCITIA=ltVentas.codcitiA
			IF nPtoVta=INT(ltVentas.numero/100000000)
				?nNumero, ltVentas.numero
			ENDIF 
		ENDIF 
		nPtoVta=INT(ltVentas.numero/100000000)
		nNumero=ltVentas.numero
		cCodCITIA=ltVentas.codcitiA
	ENDIF 
	nNumero=nNumero+1
	SELECT ltVentas
ENDSCAN 

*-------------------------------- Otro modo de controlar solo comprobantes A y B

*---------------------------- Control de Comprobantes A
STORE DTOC(DATE()) TO cDesde, cHasta
cDesde= INPUTBOX('Ingreso desde Fecha a controlar','Primer dia',cDesde)
dDesde = CTOD(cDesde)
cHasta = INPUTBOX('Ingreso hasta Fecha a controlar','Ultimo dia',cHasta)
dHasta = CTOD(cHasta)


SELECT id,codven.codcitiA,letra,numero ;
	FROM facturas INNER JOIN codven ON facturas.compro = codven.compro ;
	WHERE fecha between dDesde and dHasta AND letra='A' ;
	ORDER BY 2,3,4 INTO CURSOR A1
nNumero=numero
SELECT a1
SCAN 
	IF nNumero#numero
		IF nNumero/100000000 = numero/100000000
			?'Falta Numero', letra, nNumero
		ENDIF 
		nNumero=numero
	ENDIF 
	nNumero = nNumero + 1
ENDSCAN 

*---------------------------- Control de Comprobantes B
SELECT id,codven.codcitiB,letra,numero ;
	FROM facturas INNER JOIN codven ON facturas.compro = codven.compro ;
	WHERE fecha between dDesde and dHasta AND letra='B' ;
	ORDER BY 2,3,4 INTO CURSOR B1
nNumero=numero
SELECT b1
SCAN 
	IF nNumero#numero
		IF nNumero/100000000 = numero/100000000
			?'Falta Numero', letra, nNumero
		ENDIF 
		nNumero=numero
	ENDIF 
	nNumero = nNumero + 1
ENDSCAN 

CLOSE ALL 
CLEAR All 


USE terminal ORDER login IN 0 
USE sucursal ORDER id IN 0 
USE codven   ORDER compro IN 0 
SELECT SUCURSAL, SUCURSAL.nombre, PUNTOVTA FROM TERMINAL INNER JOIN SUCURSAL ON terminal.sucursal=sucursal.id GROUP BY 1 INTO CURSOR vlSucursal
SELECT codcitia, codcitib, nombre FROM codven GROUP BY 1,2 INTO CURSOR  vlCodVen

CREATE CURSOR numeracion  (sucursal n(2), comprobante c(3), puntoventa n(5), numero n(13), letra c(1), renglones n(2), copias n(2))
SELECT numeracion
INDEX ON STR(SUCURSAL,2)+STR(PUNTOVENTA,5)+COMPROBANTE TAG NUMERO

CLEAR 
SELECT vlSucursal
SCAN 
	SELECT vlCodVen
	SCAN FOR !EMPTY(codcitiA)
		cLetra=IIF(codcitiA='091','R',IIF(codcitiA$'001*002*003*201*202*203', 'A', 'X'))
		cClave = STR(vlSucursal.sucursal,2)+STR(vlSucursal.puntovta,5)+vlCodVen.codcitiA
		IF !SEEK(cClave,"numeracion","numero")
			INSERT INTO numeracion  (sucursal, comprobante, puntoventa, numero, letra, renglones, copias) ;
				VALUES (vlSucursal.sucursal, vlCodVen.codcitiA, vlSucursal.puntovta, vlSucursal.puntovta*100000000, cLetra, 11, 2)
		ENDIF 
		IF !EMPTY(codcitiB) AND (codcitiA#codcitiB)
			cLetra=IIF(codcitiB='091','R',IIF(codcitiB$'006*007*008*206*207*208','B','X'))
			cClave = STR(vlSucursal.sucursal,2)+STR(vlSucursal.puntovta,5)+vlCodVen.codcitiB
			IF !SEEK(cClave,"numeracion","numero")
				INSERT INTO numeracion  (sucursal, comprobante, puntoventa, numero, letra, renglones, copias) ;
					VALUES (vlSucursal.sucursal, vlCodVen.codcitiB, vlSucursal.puntovta, vlSucursal.puntovta*100000000, cLetra, 11, 2)
			ENDIF 
		ENDIF 
		SELE vlCodVen
	ENDSCAN 
	SELECT vlSucursal
ENDSCAN 

*------------------------------------- Actualizo Numeracion
USE numeros ORDER sucursal IN 0 
SELECT numeracion
SCAN 
	IF SEEK(numeracion.sucursal,'numeros','sucursal')
		DO CASE 
			CASE comprobante='091'
				REPLACE numero WITH numeros.remitos
			CASE comprobante='RB'
				REPLACE numero WITH numeros.recibo
			CASE comprobante='RE'
				REPLACE numero WITH numeros.recibo2
			CASE comprobante='MI'
				REPLACE numero WITH numeros.forint
			CASE comprobante='AJ'
				REPLACE numero WITH numeros.ajuste
			CASE comprobante='PR'
				REPLACE numero WITH numeros.presup
		ENDCASE 
	ENDIF 
	SELECT numeracion
ENDSCAN 
SELECT numeracion
BROWSE

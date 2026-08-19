*-- Script que obtiene solo los que están faltando.
SELECT ;
	r.*, ;
	f.id, ;
	f.compro AS "Compro_Rcbo", ;
	f.letra AS "Letra_Rcbo", ;
	f.numero AS "Numero_Rcbo", ;
	f.fecha AS "Fecha_Rcbo", ;
	fa.compro AS "Compro_FA", ;
	fa.letra AS "Letra_FA", ;
	fa.numero AS "Numero_FA", ;
	fa.fecha AS "Fecha_FA" ;
FROM ;
	recibos r ;
	JOIN facturas f ON r.recibo = f.numero ;
	LEFT JOIN facturas fa ON (r.compro=fa.compro AND r.letra=fa.letra AND r.numero=fa.numero) ;
WHERE ;
	fa.numero is null

*	f.numero = 1400001059   ==> Recibo.
*	fa.numero is null       ==> Todos los que faltarían.



*-- Script que obtiene los datos crudos
*!*	SELECT ;
*!*		r.*, ;
*!*		f.id, ;
*!*		f.compro AS "Compro_Rcbo", ;
*!*		f.letra AS "Letra_Rcbo", ;
*!*		f.numero AS "Numero_Rcbo", ;
*!*		f.fecha AS "Fecha_Rcbo", ;
*!*		fa.compro AS "Compro_FA", ;
*!*		fa.letra AS "Letra_FA", ;
*!*		fa.numero AS "Numero_FA", ;
*!*		fa.fecha AS "Fecha_FA" ;
*!*	FROM ;
*!*		recibos r ;
*!*		JOIN facturas f ON r.recibo = f.numero ;
*!*		LEFT JOIN facturas fa ON (r.compro=fa.compro AND r.letra=fa.letra AND r.numero=fa.numero)
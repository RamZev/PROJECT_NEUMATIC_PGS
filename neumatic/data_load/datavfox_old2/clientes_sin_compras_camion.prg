* Busca todos los clientes sin operatoria conm mas de 6 meses y sean clientes de camiones
* Fecha corte = hoy menos 6 meses
*

CLOSE TABLE all 
USE clientes ORDER codigo IN 0 
USE vendedor ORDER codigo IN 0
USE facturas ORDER id IN 0
USE detven ORDER id IN 0 
USE lista ORDER codigo IN 0


*!*	ldCorte = GOMONTH(DATE(), -6)

*!*	SELECT c.codigo, c.nombre, c.domicilio, ld.localidad, c.telefono, c.mail, c.sucursal, MAX(f.fecha) AS ultima_oper, v.nombre as vendedor ;
*!*	FROM clientes c LEFT JOIN facturas f ON f.cliente = c.codigo ;
*!*		INNER JOIN vendedor v ON c.vendedor = v.codigo ;
*!*		INNER JOIN localidad ld ON c.codpostal = ld.codigo ;
*!*	WHERE c.codigo NOT IN ( ;
*!*	    SELECT f2.cliente ;
*!*	    FROM facturas f2 ;
*!*	    INNER JOIN detven d  ON d.id = f2.id ;
*!*	    INNER JOIN lista  l  ON l.codigo = d.codigo ;
*!*	    GROUP BY f2.cliente ;
*!*	    HAVING MIN(l.articulo) = 4 AND MAX(l.articulo) = 4 ;
*!*	) ;
*!*	GROUP BY c.codigo, c.nombre ;
*!*	HAVING MAX(f.fecha) < ldCorte ;
*!*	INTO CURSOR ltInactivos READWRITE

ldCorte = GOMONTH(DATE(), -6)

SELECT ;
    c.codigo, ;
    c.nombre, ;
    c.domicilio, ;
    ld.localidad, ;
    c.telefono, ;
    c.mail, ;
    c.sucursal, ;
    v.nombre AS vendedor, ;
    MAX(f.fecha) AS ultima_oper ;
FROM clientes c ;
LEFT JOIN facturas  f  ON f.cliente   = c.codigo ;
INNER JOIN vendedor v  ON v.codigo    = c.vendedor ;
INNER JOIN localidad ld ON ld.codigo  = c.codpostal ;
WHERE ;
    c.codigo IN ( ;
        SELECT fA.cliente ;
        FROM facturas fA ;
        INNER JOIN detven dA ON dA.id = fA.id ;
        INNER JOIN lista  lA ON lA.codigo = dA.codigo ;
        WHERE lA.articulo = 4 ) ;
    AND ;
    c.codigo NOT IN ( ;
        SELECT fB.cliente ;
        FROM facturas fB ;
        INNER JOIN detven dB ON dB.id = fB.id ;
        INNER JOIN lista  lB ON lB.codigo = dB.codigo ;
        GROUP BY fB.cliente ;
        HAVING MIN(lB.articulo) = 4 AND MAX(lB.articulo) = 4 ;
    ) ;
GROUP BY ;
    c.codigo, c.nombre, c.domicilio, ld.localidad, c.telefono, c.mail, c.sucursal, v.nombre ;
HAVING MAX(f.fecha) < ldCorte ;
INTO CURSOR ltInactivos READWRITE

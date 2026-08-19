* Busca todos los clientes sin operatoria conm mas de 6 meses
* Fecha corte = hoy menos 6 meses
*

CLOSE TABLE all 
USE clientes ORDER codigo IN 0 
USE facturas ORDER id IN 0


ldCorte = GOMONTH(DATE(), -6)

SELECT c.codigo, c.nombre, MAX(f.fecha) AS ultima_oper  ;
FROM clientes c ;
LEFT JOIN facturas f ON f.cliente = c.codigo ;
GROUP BY c.codigo, c.nombre ;
HAVING MAX(f.fecha) < ldCorte OR MAX(f.fecha) IS NULL ;
INTO CURSOR ltInactivos READWRITE

BROWSE NORMAL

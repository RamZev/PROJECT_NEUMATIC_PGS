CLOSE DATABASES
CLEAR ALL
SET exclusiv on
SET DELETED OFF 
CLEAR 


* Antes de ejecutar el algoritmo, en la tabla DBF, se eliminaron los dos últimos registros uno blank otro sin nombre y se hizo un pack
?"Operarios"
USE operario EXCLUSIVE
REPLACE codigo WITH 99 FOR codigo=0
DELETE FOR EMPTY(nombre)
PACK

USE detven IN 0
USE lista ORDER codigo IN 0
SELECT detven
SET RELATION TO Detven.codigo INTO Lista ADDITIVE
REPLACE operario WITH 99 FOR lista.tipo= 'S' AND operario=0
CLOSE TABLES ALL 


* Eliminar los registro con el campo **lista.codigo** duplicados
* Modificar valores del campo lista **lista.iva** mayores a 100
?"Lista de precios, duplicados"
USE lista EXCLUSIVE
SELECT codigo, COUNT(*) AS cantidad FROM lista GROUP BY codigo HAVING COUNT(*) > 1
LIST
SELECT lista
PACK
USE 

* Se asignó código 1 a SANTA FE MOSTRADOR. Hacer un pack. 
USE vendedor EXCLUSIVE
REPLACE codigo WITH 1 FOR codigo=0
PACK
USE clientes 
REPLACE vendedor WITH 1 FOR vendedor=0
CLOSE TABLES ALL 


* Antes de ejecutar el algoritmo, en la tabla DBF, se hizo un pack, había un archivo marcado para borrar
USE depositos EXCLUSIVE
PACK
USE


* Antes de migrar, eliminar ID que se repiten en factura.dbf: 1550326, 1551103, 1591230
* corregir los id manualmente y en detven igual
?"Facturas duplicadas"
USE facturas EXCLUSIVE
SELECT id, COUNT(*) as repeticiones FROM facturas WHERE fecha > {01/01/2024} GROUP BY id HAVING COUNT(*) > 1
LIST 
SELECT facturas
SET ORDER TO id
?'primer id', id
PACK 


* En la tabla origen detven.dbf hay que corregir en los 1566500 y 1569043 la inversón de PRECIO y CANTIDAD, se colocó el precio en la cantidad. También filtrar por el campo ALICIVA > 21 y reemplazar esos valores por 21
USE detven EXCLUSIVE
REPLACE precio   WITH cantidad FOR cantidad>10000 AND precio<2
REPLACE cantidad WITH 1 FOR cantidad>10000 AND precio=cantidad
PACK 
USE 



* en tabla Stock reemplazar por 0 lo valores en blanco 
USE stock EXCLUSIVE
REPLACE stock WITH 0 FOR EMPTY(stock)
REPLACE minimo WITH 0 FOR EMPTY(minimo)
PACK 
USE 


* en tabla VenDescArt borrar registro que no encuentra familia
USE stock EXCLUSIVE
USE articulo ORDER codigo  EXCLUSIVE 
USE vendescart IN 0 
SELECT vendescart
SET RELATION TO articulo INTO articulo
DELETE FOR EMPTY(articulo.codigo)
PACK 
CLOSE TABLES ALL 


* en tabla VenDescArt borrar registro que no encuentra familia
USE stock EXCLUSIVE
USE articulo ORDER codigo  EXCLUSIVE 
USE vendescart IN 0 
SELECT vendescart
SET RELATION TO articulo INTO articulo
DELETE FOR EMPTY(articulo.codigo)
PACK 
CLOSE TABLES ALL 


* en tabla VendedorComision borrar registro que no encuentra familia
USE vendedorcomision EXCLUSIVE 
USE marcas ORDER codigo IN 0 SHARED
USE articulo ORDER codigo IN 0 SHARED
SELECT vendedorcomision 
SET RELATION TO Vendedorcomision.marca INTO Marcas ADDITIVE
SET RELATION TO Vendedorcomision.articulo INTO Articulo ADDITIVE
DELETE FOR EMPTY(marcas.codigo)
DELETE FOR EMPTY(articulo.codigo)
PACK 
CLOSE TABLES ALL 


* en tabla VendedorComision borrar registro que no encuentra familia
USE venDesc EXCLUSIVE 
USE modelos order codigo IN 0
USE marcas ORDER codigo IN 0 SHARED
SELECT venDesc 
SET RELATION TO Vendesc.modelo INTO Modelos ADDITIVE
SET RELATION TO Vendesc.marca INTO Marcas ADDITIVE
DELETE FOR EMPTY(modelos.codigo)
DELETE FOR EMPTY(marcas.codigo)
PACK 
CLOSE TABLES ALL 

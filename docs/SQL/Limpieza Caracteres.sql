-------------------------------------------------------------------------------------
-- Modelo Producto:

-- Caracter: 
--SELECT id_producto, nombre_producto FROM producto WHERE nombre_producto like '%%'
UPDATE producto SET nombre_producto = replace(nombre_producto, '', '');

-- Caracter: 
--SELECT id_producto, nombre_producto FROM producto WHERE nombre_producto like '%%'
UPDATE producto SET nombre_producto = replace(nombre_producto, '', '');

-- Caracter: 
--SELECT id_producto, nombre_producto FROM producto WHERE nombre_producto like '%%'
UPDATE producto SET nombre_producto = replace(nombre_producto, '', '');

-- Caracter: ÿ
--SELECT id_producto, nombre_producto FROM producto WHERE nombre_producto like '%ÿ%'
UPDATE producto SET nombre_producto = replace(nombre_producto, 'ÿ', ' ');

-- Caracter: ¥
--SELECT id_producto, nombre_producto FROM producto WHERE nombre_producto like '%¥%'
UPDATE producto SET nombre_producto = replace(nombre_producto, '¥', 'Ñ');

-- Caracter: à
--SELECT id_producto, nombre_producto FROM producto WHERE nombre_producto like '%à%'
UPDATE producto SET nombre_producto = replace(nombre_producto, 'à', 'Ó');

-- Caracter:  (É)
--SELECT id_producto, nombre_producto FROM producto WHERE nombre_producto like '%%'
UPDATE producto SET nombre_producto = replace(nombre_producto, '', 'É');

-------------------------------------------------------------------------------------
-- Modelo Cliente:

-- Caracter: 
--SELECT id_cliente, nombre_cliente FROM cliente WHERE nombre_cliente like '%%'
UPDATE cliente SET nombre_cliente = replace(nombre_cliente, '', 'É');

-- Caracter: ¥
--SELECT id_cliente, nombre_cliente FROM cliente WHERE nombre_cliente like '%¥%'
UPDATE cliente SET nombre_cliente = replace(nombre_cliente, '¥', 'Ñ');

-- Caracter: µ
--SELECT id_cliente, nombre_cliente FROM cliente WHERE nombre_cliente like '%µ%'
UPDATE cliente SET nombre_cliente = replace(nombre_cliente, 'µ', 'Á');

-- Caracter: é
--SELECT id_cliente, nombre_cliente FROM cliente WHERE nombre_cliente like '%é%'
UPDATE cliente SET nombre_cliente = replace(nombre_cliente, 'é', 'Ú');

-- Caracter: Ö
--SELECT id_cliente, nombre_cliente FROM cliente WHERE nombre_cliente like '%Ö%'
UPDATE cliente SET nombre_cliente = replace(nombre_cliente, 'Ö', 'Í');
-------------------------------------------------------------------------------------

-- Primera actualización
UPDATE producto 
SET tipo_producto = UPPER(tipo_producto)
WHERE tipo_producto IN ('s', 'p');

-- Segunda actualización
UPDATE producto
SET tipo_producto = 'S'
WHERE (tipo_producto IS NULL OR tipo_producto = '')
AND (
    UPPER(nombre_producto) LIKE '%REPARACION%' 
    OR UPPER(nombre_producto) LIKE '%REPARACON%'
    OR UPPER(nombre_producto) LIKE '%REP %'
    OR UPPER(nombre_producto) LIKE '% REP%'
    OR UPPER(nombre_producto) LIKE 'REP%'
);

-- Tercera Actualización
UPDATE producto
SET tipo_producto = 'P'
WHERE (tipo_producto IS NULL OR tipo_producto = '');

-- Cuarta Actualización
UPDATE producto
SET tipo_producto = 'P'
WHERE tipo_producto = 'O';
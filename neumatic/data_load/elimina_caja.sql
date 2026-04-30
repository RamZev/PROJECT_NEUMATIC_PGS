-- Eliminar registros de la tabla detalle primero
DELETE FROM caja_detalle;
-- Eliminar registros de la tabla principal
DELETE FROM caja;
-- Resetear el contador para caja_detalle
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'caja_detalle';
-- Resetear el contador para caja
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'caja';
-- caja_detalle: Script para asignar 2 (Egreso) a tipo_movimiento si idventas = -2.
UPDATE caja_detalle SET tipo_movimiento=2 WHERE idventas=-2 AND tipo_movimiento<>2;

-- caja_detalle: Script para asignar 1 (Ingreso) a tipo_movimiento si idventas <> -2.
UPDATE caja_detalle SET tipo_movimiento=1 WHERE idventas<>-2;

UPDATE producto
SET obliga_operario = TRUE
WHERE tipo_producto = 'S' AND (obliga_operario IS NULL OR obliga_operario = FALSE);
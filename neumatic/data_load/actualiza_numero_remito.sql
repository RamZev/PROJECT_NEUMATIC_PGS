UPDATE numero n
SET numero = (
    SELECT COALESCE(MAX(f.numero_comprobante), 0)
    FROM factura f
    JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
    WHERE f.id_sucursal_id = n.id_sucursal_id
      AND f.id_punto_venta_id = n.id_punto_venta_id
      AND f.letra_comprobante = n.letra
      AND cv.remito = TRUE
      AND cv.tipo_numeracion = 2
)
WHERE n.comprobante = '091'
  AND n.letra = 'R';


-- Verificaciones
SELECT id_sucursal_id, id_punto_venta_id, comprobante, letra, numero
FROM numero
WHERE comprobante = '091' AND letra = 'R'
ORDER BY id_sucursal_id, id_punto_venta_id;

-- Comparar con los máximos reales de Factura
SELECT 
    f.id_sucursal_id,
    f.id_punto_venta_id,
    f.letra_comprobante,
    MAX(f.numero_comprobante) AS max_real
FROM factura f
JOIN comprobante_venta cv ON f.id_comprobante_venta_id = cv.id_comprobante_venta
WHERE cv.remito = TRUE
  AND cv.tipo_numeracion = 2
GROUP BY f.id_sucursal_id, f.id_punto_venta_id, f.letra_comprobante
ORDER BY f.id_sucursal_id, f.id_punto_venta_id;
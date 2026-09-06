-- ============================================================
-- Script para exportar las tablas como JSON en formato array
-- ============================================================

-- Asegúrate de que la carpeta D:\NEUMATIC_BAK\json_01 exista

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM comprobante_venta) t
) TO 'D:/NEUMATIC_BAK/json_01/comprobante_venta.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM comprobante_compra) t
) TO 'D:/NEUMATIC_BAK/json_01/comprobante_compra.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM moneda) t
) TO 'D:/NEUMATIC_BAK/json_01/moneda.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM tipo_iva) t
) TO 'D:/NEUMATIC_BAK/json_01/tipo_iva.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM codigo_alicuota) t
) TO 'D:/NEUMATIC_BAK/json_01/alicuota_iva.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM empresa) t
) TO 'D:/NEUMATIC_BAK/json_01/empresa.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM medio_pago) t
) TO 'D:/NEUMATIC_BAK/json_01/medio_pago.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM tipo_documento_identidad) t
) TO 'D:/NEUMATIC_BAK/json_01/tipo_documento_identidad.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM sucursal) t
) TO 'D:/NEUMATIC_BAK/json_01/sucursal.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM punto_venta) t
) TO 'D:/NEUMATIC_BAK/json_01/punto_venta.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM leyenda) t
) TO 'D:/NEUMATIC_BAK/json_01/leyenda.json';

COPY (
    SELECT json_agg(row_to_json(t)) 
    FROM (SELECT * FROM marketing_origen) t
) TO 'D:/NEUMATIC_BAK/json_01/marketing_origen.json';
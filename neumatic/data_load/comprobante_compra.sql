-- ============================================
-- LIMPIEZA Y RESETEO DE SECUENCIA
-- ============================================

-- Eliminar todos los registros
DELETE FROM comprobante_compra;

-- Resetear la secuencia en PostgreSQL
SELECT setval(pg_get_serial_sequence('comprobante_compra', 'id_comprobante_compra'), 1, false);

-- ============================================
-- INSERCIÓN DE DATOS (manteniendo IDs manuales)
-- ============================================

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES (NULL, NULL, NULL, 1, TRUE, 'FA', 'FACTURA', 1, 1, 1, 0, TRUE, '001', '006', '011', '', FALSE, FALSE, NULL, 'FACTURA');

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES (NULL, NULL, NULL, 2, TRUE, 'NC', 'NOTA DE CRÉDITO', -1, -1, -1, 0, TRUE, '003', '008', '013', '', FALSE, FALSE, NULL, 'NOTA DE CRÉDITO');

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES (NULL, NULL, NULL, 3, TRUE, 'ND', 'NOTA DE DÉBITO', 1, 1, 1, 0, TRUE, '002', '007', '012', '', FALSE, FALSE, NULL, 'NOTA DE DÉBITO');

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES (NULL, NULL, NULL, 4, TRUE, 'OP', 'ORDEN DE PAGO', 0, -1, 0, 0, FALSE, '000', '000', '000', '', FALSE, FALSE, NULL, 'ORDEN DE PAGO');

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES (NULL, NULL, NULL, 5, TRUE, 'AJ', 'AJUSTE', 0, 1, 0, 0, FALSE, '000', '000', '000', '', FALSE, FALSE, NULL, 'AJUSTE');

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES (NULL, NULL, NULL, 6, TRUE, 'RG', 'RETENCIÓN GANACIAS', 0, -1, 0, 0, TRUE, '000', '000', '000', '', FALSE, TRUE, NULL, 'RETENCIÓN');

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES (NULL, NULL, NULL, 7, TRUE, 'RI', 'RETENCIÓN IVA', 0, -1, 0, 0, TRUE, '000', '000', '000', '', FALSE, TRUE, NULL, 'RETENCIÓN');

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES (NULL, NULL, NULL, 8, TRUE, 'IB', 'RETENCIÓN IIBB', 0, -1, 0, 0, TRUE, '000', '000', '000', '', FALSE, TRUE, NULL, 'RETENCIÓN');

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES ('admin', 'Leoncio', '2026-04-08 13:10:39', 9, TRUE, 'RT', 'REMITOS', 0, 0, 1, 0, FALSE, '091', '000', '000', '0', TRUE, FALSE, 1, 'REMITOS');

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES (NULL, NULL, NULL, 10, TRUE, 'DV', 'DEVOLUCIÓN', 0, 0, -1, 0, FALSE, '000', '000', '000', '', FALSE, FALSE, NULL, 'DEVOLUCIÓN');

INSERT INTO comprobante_compra (usuario, estacion, fcontrol, id_comprobante_compra, estatus_comprobante_compra, codigo_comprobante_compra, nombre_comprobante_compra, mult_compra, mult_saldo, mult_stock, mult_caja, libro_iva, codigo_afip_a, codigo_afip_b, codigo_afip_c, codigo_afip_m, remito, retencion, id_user_id, nombre_impresion) VALUES ('admin', 'Leoncio', '2026-04-08 13:06:09', 11, TRUE, 'RM', 'REMITOS INTERNOS', 0, 0, 1, 0, FALSE, '091', '000', '000', '0', TRUE, FALSE, 1, 'REMITOS');

-- ============================================
-- VERIFICACIÓN
-- ============================================
SELECT COUNT(*) AS total_registros FROM comprobante_compra;
SELECT * FROM comprobante_compra ORDER BY id_comprobante_compra;
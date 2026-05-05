-- Sincronizacion de secuencias para VENTAS
-- Tablas con datos: se setea al MAX(id)
-- Tablas vacias: se setea a 1 con is_called=false (proximo ID sera 1)

DO $$
DECLARE
    max_id INTEGER;
BEGIN
    -- caja
    SELECT COALESCE(MAX(id_caja), 0) INTO max_id FROM caja;
    IF max_id > 0 THEN
        PERFORM setval('caja_id_caja_seq', max_id);
        RAISE NOTICE 'OK caja: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('caja_id_caja_seq', 1, false);
        RAISE NOTICE 'VACIA caja: Tabla vacia, proximo ID sera 1';
    END IF;

    -- caja_detalle
    SELECT COALESCE(MAX(id_caja_detalle), 0) INTO max_id FROM caja_detalle;
    IF max_id > 0 THEN
        PERFORM setval('caja_detalle_id_caja_detalle_seq', max_id);
        RAISE NOTICE 'OK caja_detalle: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('caja_detalle_id_caja_detalle_seq', 1, false);
        RAISE NOTICE 'VACIA caja_detalle: Tabla vacia, proximo ID sera 1';
    END IF;

    -- caja_arqueo
    SELECT COALESCE(MAX(id_caja_arqueo), 0) INTO max_id FROM caja_arqueo;
    IF max_id > 0 THEN
        PERFORM setval('caja_arqueo_id_caja_arqueo_seq', max_id);
        RAISE NOTICE 'OK caja_arqueo: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('caja_arqueo_id_caja_arqueo_seq', 1, false);
        RAISE NOTICE 'VACIA caja_arqueo: Tabla vacia, proximo ID sera 1';
    END IF;

    -- caja_medio_pago
    SELECT COALESCE(MAX(id_caja_medio_pago), 0) INTO max_id FROM caja_medio_pago;
    IF max_id > 0 THEN
        PERFORM setval('caja_medio_pago_id_caja_medio_pago_seq', max_id);
        RAISE NOTICE 'OK caja_medio_pago: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('caja_medio_pago_id_caja_medio_pago_seq', 1, false);
        RAISE NOTICE 'VACIA caja_medio_pago: Tabla vacia, proximo ID sera 1';
    END IF;

    -- compra
    SELECT COALESCE(MAX(id_compra), 0) INTO max_id FROM compra;
    IF max_id > 0 THEN
        PERFORM setval('compra_id_compra_seq', max_id);
        RAISE NOTICE 'OK compra: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('compra_id_compra_seq', 1, false);
        RAISE NOTICE 'VACIA compra: Tabla vacia, proximo ID sera 1';
    END IF;

    -- detalle_compra
    SELECT COALESCE(MAX(id_detalle_compra), 0) INTO max_id FROM detalle_compra;
    IF max_id > 0 THEN
        PERFORM setval('detalle_compra_id_detalle_compra_seq', max_id);
        RAISE NOTICE 'OK detalle_compra: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('detalle_compra_id_detalle_compra_seq', 1, false);
        RAISE NOTICE 'VACIA detalle_compra: Tabla vacia, proximo ID sera 1';
    END IF;

    -- factura
    SELECT COALESCE(MAX(id_factura), 0) INTO max_id FROM factura;
    IF max_id > 0 THEN
        PERFORM setval('factura_id_factura_seq', max_id);
        RAISE NOTICE 'OK factura: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('factura_id_factura_seq', 1, false);
        RAISE NOTICE 'VACIA factura: Tabla vacia, proximo ID sera 1';
    END IF;

    -- detalle_factura
    SELECT COALESCE(MAX(id_detalle_factura), 0) INTO max_id FROM detalle_factura;
    IF max_id > 0 THEN
        PERFORM setval('detalle_factura_id_detalle_factura_seq', max_id);
        RAISE NOTICE 'OK detalle_factura: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('detalle_factura_id_detalle_factura_seq', 1, false);
        RAISE NOTICE 'VACIA detalle_factura: Tabla vacia, proximo ID sera 1';
    END IF;

    -- serial_factura
    SELECT COALESCE(MAX(id_serial_factura), 0) INTO max_id FROM serial_factura;
    IF max_id > 0 THEN
        PERFORM setval('serial_factura_id_serial_factura_seq', max_id);
        RAISE NOTICE 'OK serial_factura: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('serial_factura_id_serial_factura_seq', 1, false);
        RAISE NOTICE 'VACIA serial_factura: Tabla vacia, proximo ID sera 1';
    END IF;

    -- detalle_recibo
    SELECT COALESCE(MAX(id_detalle_recibo), 0) INTO max_id FROM detalle_recibo;
    IF max_id > 0 THEN
        PERFORM setval('detalle_recibo_id_detalle_recibo_seq', max_id);
        RAISE NOTICE 'OK detalle_recibo: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('detalle_recibo_id_detalle_recibo_seq', 1, false);
        RAISE NOTICE 'VACIA detalle_recibo: Tabla vacia, proximo ID sera 1';
    END IF;

    -- retencion_recibo
    SELECT COALESCE(MAX(id_retencion_recibo), 0) INTO max_id FROM retencion_recibo;
    IF max_id > 0 THEN
        PERFORM setval('retencion_recibo_id_retencion_recibo_seq', max_id);
        RAISE NOTICE 'OK retencion_recibo: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('retencion_recibo_id_retencion_recibo_seq', 1, false);
        RAISE NOTICE 'VACIA retencion_recibo: Tabla vacia, proximo ID sera 1';
    END IF;

    -- deposito_recibo
    SELECT COALESCE(MAX(id_deposito_recibo), 0) INTO max_id FROM deposito_recibo;
    IF max_id > 0 THEN
        PERFORM setval('deposito_recibo_id_deposito_recibo_seq', max_id);
        RAISE NOTICE 'OK deposito_recibo: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('deposito_recibo_id_deposito_recibo_seq', 1, false);
        RAISE NOTICE 'VACIA deposito_recibo: Tabla vacia, proximo ID sera 1';
    END IF;

    -- tarjeta_recibo
    SELECT COALESCE(MAX(id_tarjeta_recibo), 0) INTO max_id FROM tarjeta_recibo;
    IF max_id > 0 THEN
        PERFORM setval('tarjeta_recibo_id_tarjeta_recibo_seq', max_id);
        RAISE NOTICE 'OK tarjeta_recibo: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('tarjeta_recibo_id_tarjeta_recibo_seq', 1, false);
        RAISE NOTICE 'VACIA tarjeta_recibo: Tabla vacia, proximo ID sera 1';
    END IF;

    -- cheque_recibo
    SELECT COALESCE(MAX(id_cheque_recibo), 0) INTO max_id FROM cheque_recibo;
    IF max_id > 0 THEN
        PERFORM setval('cheque_recibo_id_cheque_recibo_seq', max_id);
        RAISE NOTICE 'OK cheque_recibo: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('cheque_recibo_id_cheque_recibo_seq', 1, false);
        RAISE NOTICE 'VACIA cheque_recibo: Tabla vacia, proximo ID sera 1';
    END IF;

    -- stock_cliente
    SELECT COALESCE(MAX(id_stock_cliente), 0) INTO max_id FROM stock_cliente;
    IF max_id > 0 THEN
        PERFORM setval('stock_cliente_id_stock_cliente_seq', max_id);
        RAISE NOTICE 'OK stock_cliente: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('stock_cliente_id_stock_cliente_seq', 1, false);
        RAISE NOTICE 'VACIA stock_cliente: Tabla vacia, proximo ID sera 1';
    END IF;

END $$;
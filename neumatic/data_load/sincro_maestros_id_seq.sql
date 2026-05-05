-- Sincronizacion de secuencias para base_models
-- Tablas con datos: se setea al MAX(id)
-- Tablas vacias: se setea a 1 con is_called=false (proximo ID sera 1)

DO $$
DECLARE
    max_id INTEGER;
BEGIN
    -- actividad
    SELECT COALESCE(MAX(id_actividad), 0) INTO max_id FROM actividad;
    IF max_id > 0 THEN
        PERFORM setval('actividad_id_actividad_seq', max_id);
        RAISE NOTICE 'OK actividad: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('actividad_id_actividad_seq', 1, false);
        RAISE NOTICE 'VACIA actividad: Tabla vacia, proximo ID sera 1';
    END IF;

    -- producto_deposito
    SELECT COALESCE(MAX(id_producto_deposito), 0) INTO max_id FROM producto_deposito;
    IF max_id > 0 THEN
        PERFORM setval('producto_deposito_id_producto_deposito_seq', max_id);
        RAISE NOTICE 'OK producto_deposito: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('producto_deposito_id_producto_deposito_seq', 1, false);
        RAISE NOTICE 'VACIA producto_deposito: Tabla vacia, proximo ID sera 1';
    END IF;

    -- producto_familia
    SELECT COALESCE(MAX(id_producto_familia), 0) INTO max_id FROM producto_familia;
    IF max_id > 0 THEN
        PERFORM setval('producto_familia_id_producto_familia_seq', max_id);
        RAISE NOTICE 'OK producto_familia: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('producto_familia_id_producto_familia_seq', 1, false);
        RAISE NOTICE 'VACIA producto_familia: Tabla vacia, proximo ID sera 1';
    END IF;

    -- moneda
    SELECT COALESCE(MAX(id_moneda), 0) INTO max_id FROM moneda;
    IF max_id > 0 THEN
        PERFORM setval('moneda_id_moneda_seq', max_id);
        RAISE NOTICE 'OK moneda: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('moneda_id_moneda_seq', 1, false);
        RAISE NOTICE 'VACIA moneda: Tabla vacia, proximo ID sera 1';
    END IF;

    -- producto_marca
    SELECT COALESCE(MAX(id_producto_marca), 0) INTO max_id FROM producto_marca;
    IF max_id > 0 THEN
        PERFORM setval('producto_marca_id_producto_marca_seq', max_id);
        RAISE NOTICE 'OK producto_marca: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('producto_marca_id_producto_marca_seq', 1, false);
        RAISE NOTICE 'VACIA producto_marca: Tabla vacia, proximo ID sera 1';
    END IF;

    -- producto_modelo
    SELECT COALESCE(MAX(id_modelo), 0) INTO max_id FROM producto_modelo;
    IF max_id > 0 THEN
        PERFORM setval('producto_modelo_id_modelo_seq', max_id);
        RAISE NOTICE 'OK producto_modelo: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('producto_modelo_id_modelo_seq', 1, false);
        RAISE NOTICE 'VACIA producto_modelo: Tabla vacia, proximo ID sera 1';
    END IF;

    -- producto_cai
    SELECT COALESCE(MAX(id_cai), 0) INTO max_id FROM producto_cai;
    IF max_id > 0 THEN
        PERFORM setval('producto_cai_id_cai_seq', max_id);
        RAISE NOTICE 'OK producto_cai: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('producto_cai_id_cai_seq', 1, false);
        RAISE NOTICE 'VACIA producto_cai: Tabla vacia, proximo ID sera 1';
    END IF;

    -- producto_minimo
    SELECT COALESCE(MAX(id_producto_minimo), 0) INTO max_id FROM producto_minimo;
    IF max_id > 0 THEN
        PERFORM setval('producto_minimo_id_producto_minimo_seq', max_id);
        RAISE NOTICE 'OK producto_minimo: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('producto_minimo_id_producto_minimo_seq', 1, false);
        RAISE NOTICE 'VACIA producto_minimo: Tabla vacia, proximo ID sera 1';
    END IF;

    -- producto_stock
    SELECT COALESCE(MAX(id_producto_stock), 0) INTO max_id FROM producto_stock;
    IF max_id > 0 THEN
        PERFORM setval('producto_stock_id_producto_stock_seq', max_id);
        RAISE NOTICE 'OK producto_stock: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('producto_stock_id_producto_stock_seq', 1, false);
        RAISE NOTICE 'VACIA producto_stock: Tabla vacia, proximo ID sera 1';
    END IF;

    -- producto_estado
    SELECT COALESCE(MAX(id_producto_estado), 0) INTO max_id FROM producto_estado;
    IF max_id > 0 THEN
        PERFORM setval('producto_estado_id_producto_estado_seq', max_id);
        RAISE NOTICE 'OK producto_estado: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('producto_estado_id_producto_estado_seq', 1, false);
        RAISE NOTICE 'VACIA producto_estado: Tabla vacia, proximo ID sera 1';
    END IF;

    -- comprobante_venta
    SELECT COALESCE(MAX(id_comprobante_venta), 0) INTO max_id FROM comprobante_venta;
    IF max_id > 0 THEN
        PERFORM setval('comprobante_venta_id_comprobante_venta_seq', max_id);
        RAISE NOTICE 'OK comprobante_venta: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('comprobante_venta_id_comprobante_venta_seq', 1, false);
        RAISE NOTICE 'VACIA comprobante_venta: Tabla vacia, proximo ID sera 1';
    END IF;

    -- comprobante_compra
    SELECT COALESCE(MAX(id_comprobante_compra), 0) INTO max_id FROM comprobante_compra;
    IF max_id > 0 THEN
        PERFORM setval('comprobante_compra_id_comprobante_compra_seq', max_id);
        RAISE NOTICE 'OK comprobante_compra: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('comprobante_compra_id_comprobante_compra_seq', 1, false);
        RAISE NOTICE 'VACIA comprobante_compra: Tabla vacia, proximo ID sera 1';
    END IF;

    -- provincia
    SELECT COALESCE(MAX(id_provincia), 0) INTO max_id FROM provincia;
    IF max_id > 0 THEN
        PERFORM setval('provincia_id_provincia_seq', max_id);
        RAISE NOTICE 'OK provincia: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('provincia_id_provincia_seq', 1, false);
        RAISE NOTICE 'VACIA provincia: Tabla vacia, proximo ID sera 1';
    END IF;

    -- localidad
    SELECT COALESCE(MAX(id_localidad), 0) INTO max_id FROM localidad;
    IF max_id > 0 THEN
        PERFORM setval('localidad_id_localidad_seq', max_id);
        RAISE NOTICE 'OK localidad: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('localidad_id_localidad_seq', 1, false);
        RAISE NOTICE 'VACIA localidad: Tabla vacia, proximo ID sera 1';
    END IF;

    -- tipo_documento_identidad
    SELECT COALESCE(MAX(id_tipo_documento_identidad), 0) INTO max_id FROM tipo_documento_identidad;
    IF max_id > 0 THEN
        PERFORM setval('tipo_documento_identidad_id_tipo_documento_identidad_seq', max_id);
        RAISE NOTICE 'OK tipo_documento_identidad: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('tipo_documento_identidad_id_tipo_documento_identidad_seq', 1, false);
        RAISE NOTICE 'VACIA tipo_documento_identidad: Tabla vacia, proximo ID sera 1';
    END IF;

    -- tipo_iva
    SELECT COALESCE(MAX(id_tipo_iva), 0) INTO max_id FROM tipo_iva;
    IF max_id > 0 THEN
        PERFORM setval('tipo_iva_id_tipo_iva_seq', max_id);
        RAISE NOTICE 'OK tipo_iva: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('tipo_iva_id_tipo_iva_seq', 1, false);
        RAISE NOTICE 'VACIA tipo_iva: Tabla vacia, proximo ID sera 1';
    END IF;

    -- tipo_percepcion_ib
    SELECT COALESCE(MAX(id_tipo_percepcion_ib), 0) INTO max_id FROM tipo_percepcion_ib;
    IF max_id > 0 THEN
        PERFORM setval('tipo_percepcion_ib_id_tipo_percepcion_ib_seq', max_id);
        RAISE NOTICE 'OK tipo_percepcion_ib: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('tipo_percepcion_ib_id_tipo_percepcion_ib_seq', 1, false);
        RAISE NOTICE 'VACIA tipo_percepcion_ib: Tabla vacia, proximo ID sera 1';
    END IF;

    -- tipo_retencion_ib
    SELECT COALESCE(MAX(id_tipo_retencion_ib), 0) INTO max_id FROM tipo_retencion_ib;
    IF max_id > 0 THEN
        PERFORM setval('tipo_retencion_ib_id_tipo_retencion_ib_seq', max_id);
        RAISE NOTICE 'OK tipo_retencion_ib: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('tipo_retencion_ib_id_tipo_retencion_ib_seq', 1, false);
        RAISE NOTICE 'VACIA tipo_retencion_ib: Tabla vacia, proximo ID sera 1';
    END IF;

    -- operario
    SELECT COALESCE(MAX(id_operario), 0) INTO max_id FROM operario;
    IF max_id > 0 THEN
        PERFORM setval('operario_id_operario_seq', max_id);
        RAISE NOTICE 'OK operario: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('operario_id_operario_seq', 1, false);
        RAISE NOTICE 'VACIA operario: Tabla vacia, proximo ID sera 1';
    END IF;

    -- medio_pago
    SELECT COALESCE(MAX(id_medio_pago), 0) INTO max_id FROM medio_pago;
    IF max_id > 0 THEN
        PERFORM setval('medio_pago_id_medio_pago_seq', max_id);
        RAISE NOTICE 'OK medio_pago: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('medio_pago_id_medio_pago_seq', 1, false);
        RAISE NOTICE 'VACIA medio_pago: Tabla vacia, proximo ID sera 1';
    END IF;

    -- punto_venta
    SELECT COALESCE(MAX(id_punto_venta), 0) INTO max_id FROM punto_venta;
    IF max_id > 0 THEN
        PERFORM setval('punto_venta_id_punto_venta_seq', max_id);
        RAISE NOTICE 'OK punto_venta: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('punto_venta_id_punto_venta_seq', 1, false);
        RAISE NOTICE 'VACIA punto_venta: Tabla vacia, proximo ID sera 1';
    END IF;

    -- codigo_alicuota
    SELECT COALESCE(MAX(id_alicuota_iva), 0) INTO max_id FROM codigo_alicuota;
    IF max_id > 0 THEN
        PERFORM setval('codigo_alicuota_id_alicuota_iva_seq', max_id);
        RAISE NOTICE 'OK codigo_alicuota: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('codigo_alicuota_id_alicuota_iva_seq', 1, false);
        RAISE NOTICE 'VACIA codigo_alicuota: Tabla vacia, proximo ID sera 1';
    END IF;

    -- banco
    SELECT COALESCE(MAX(id_banco), 0) INTO max_id FROM banco;
    IF max_id > 0 THEN
        PERFORM setval('banco_id_banco_seq', max_id);
        RAISE NOTICE 'OK banco: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('banco_id_banco_seq', 1, false);
        RAISE NOTICE 'VACIA banco: Tabla vacia, proximo ID sera 1';
    END IF;

    -- cuenta_banco
    SELECT COALESCE(MAX(id_cuenta_banco), 0) INTO max_id FROM cuenta_banco;
    IF max_id > 0 THEN
        PERFORM setval('cuenta_banco_id_cuenta_banco_seq', max_id);
        RAISE NOTICE 'OK cuenta_banco: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('cuenta_banco_id_cuenta_banco_seq', 1, false);
        RAISE NOTICE 'VACIA cuenta_banco: Tabla vacia, proximo ID sera 1';
    END IF;

    -- tarjeta
    SELECT COALESCE(MAX(id_tarjeta), 0) INTO max_id FROM tarjeta;
    IF max_id > 0 THEN
        PERFORM setval('tarjeta_id_tarjeta_seq', max_id);
        RAISE NOTICE 'OK tarjeta: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('tarjeta_id_tarjeta_seq', 1, false);
        RAISE NOTICE 'VACIA tarjeta: Tabla vacia, proximo ID sera 1';
    END IF;

    -- codigo_retencion
    SELECT COALESCE(MAX(id_codigo_retencion), 0) INTO max_id FROM codigo_retencion;
    IF max_id > 0 THEN
        PERFORM setval('codigo_retencion_id_codigo_retencion_seq', max_id);
        RAISE NOTICE 'OK codigo_retencion: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('codigo_retencion_id_codigo_retencion_seq', 1, false);
        RAISE NOTICE 'VACIA codigo_retencion: Tabla vacia, proximo ID sera 1';
    END IF;

    -- concepto_banco
    SELECT COALESCE(MAX(id_concepto_banco), 0) INTO max_id FROM concepto_banco;
    IF max_id > 0 THEN
        PERFORM setval('concepto_banco_id_concepto_banco_seq', max_id);
        RAISE NOTICE 'OK concepto_banco: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('concepto_banco_id_concepto_banco_seq', 1, false);
        RAISE NOTICE 'VACIA concepto_banco: Tabla vacia, proximo ID sera 1';
    END IF;

    -- marketing_origen
    SELECT COALESCE(MAX(id_marketing_origen), 0) INTO max_id FROM marketing_origen;
    IF max_id > 0 THEN
        PERFORM setval('marketing_origen_id_marketing_origen_seq', max_id);
        RAISE NOTICE 'OK marketing_origen: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('marketing_origen_id_marketing_origen_seq', 1, false);
        RAISE NOTICE 'VACIA marketing_origen: Tabla vacia, proximo ID sera 1';
    END IF;

    -- leyenda
    SELECT COALESCE(MAX(id_leyenda), 0) INTO max_id FROM leyenda;
    IF max_id > 0 THEN
        PERFORM setval('leyenda_id_leyenda_seq', max_id);
        RAISE NOTICE 'OK leyenda: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('leyenda_id_leyenda_seq', 1, false);
        RAISE NOTICE 'VACIA leyenda: Tabla vacia, proximo ID sera 1';
    END IF;

    -- medidas_estados
    SELECT COALESCE(MAX(id_medida_estado), 0) INTO max_id FROM medidas_estados;
    IF max_id > 0 THEN
        PERFORM setval('medidas_estados_id_medida_estado_seq', max_id);
        RAISE NOTICE 'OK medidas_estados: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('medidas_estados_id_medida_estado_seq', 1, false);
        RAISE NOTICE 'VACIA medidas_estados: Tabla vacia, proximo ID sera 1';
    END IF;

    -- forma_pago
    SELECT COALESCE(MAX(id_forma_pago), 0) INTO max_id FROM forma_pago;
    IF max_id > 0 THEN
        PERFORM setval('forma_pago_id_forma_pago_seq', max_id);
        RAISE NOTICE 'OK forma_pago: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('forma_pago_id_forma_pago_seq', 1, false);
        RAISE NOTICE 'VACIA forma_pago: Tabla vacia, proximo ID sera 1';
    END IF;

    -- Sincronizacion de secuencias para MAESTROS PRINCIPALES
    -- Tablas con datos: se setea al MAX(id)
    -- Tablas vacias: se setea a 1 con is_called=false (proximo ID sera 1)

    -- cliente
    SELECT COALESCE(MAX(id_cliente), 0) INTO max_id FROM cliente;
    IF max_id > 0 THEN
        PERFORM setval('cliente_id_cliente_seq', max_id);
        RAISE NOTICE 'OK cliente: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('cliente_id_cliente_seq', 1, false);
        RAISE NOTICE 'VACIA cliente: Tabla vacia, proximo ID sera 1';
    END IF;

    -- descuento_vendedor
    SELECT COALESCE(MAX(id_descuento_vendedor), 0) INTO max_id FROM descuento_vendedor;
    IF max_id > 0 THEN
        PERFORM setval('descuento_vendedor_id_descuento_vendedor_seq', max_id);
        RAISE NOTICE 'OK descuento_vendedor: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('descuento_vendedor_id_descuento_vendedor_seq', 1, false);
        RAISE NOTICE 'VACIA descuento_vendedor: Tabla vacia, proximo ID sera 1';
    END IF;

    -- empresa
    SELECT COALESCE(MAX(id_empresa), 0) INTO max_id FROM empresa;
    IF max_id > 0 THEN
        PERFORM setval('empresa_id_empresa_seq', max_id);
        RAISE NOTICE 'OK empresa: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('empresa_id_empresa_seq', 1, false);
        RAISE NOTICE 'VACIA empresa: Tabla vacia, proximo ID sera 1';
    END IF;

    -- numero
    SELECT COALESCE(MAX(id_numero), 0) INTO max_id FROM numero;
    IF max_id > 0 THEN
        PERFORM setval('numero_id_numero_seq', max_id);
        RAISE NOTICE 'OK numero: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('numero_id_numero_seq', 1, false);
        RAISE NOTICE 'VACIA numero: Tabla vacia, proximo ID sera 1';
    END IF;

    -- parametro
    SELECT COALESCE(MAX(id_parametro), 0) INTO max_id FROM parametro;
    IF max_id > 0 THEN
        PERFORM setval('parametro_id_parametro_seq', max_id);
        RAISE NOTICE 'OK parametro: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('parametro_id_parametro_seq', 1, false);
        RAISE NOTICE 'VACIA parametro: Tabla vacia, proximo ID sera 1';
    END IF;

    -- producto
    SELECT COALESCE(MAX(id_producto), 0) INTO max_id FROM producto;
    IF max_id > 0 THEN
        PERFORM setval('producto_id_producto_seq', max_id);
        RAISE NOTICE 'OK producto: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('producto_id_producto_seq', 1, false);
        RAISE NOTICE 'VACIA producto: Tabla vacia, proximo ID sera 1';
    END IF;

    -- proveedor
    SELECT COALESCE(MAX(id_proveedor), 0) INTO max_id FROM proveedor;
    IF max_id > 0 THEN
        PERFORM setval('proveedor_id_proveedor_seq', max_id);
        RAISE NOTICE 'OK proveedor: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('proveedor_id_proveedor_seq', 1, false);
        RAISE NOTICE 'VACIA proveedor: Tabla vacia, proximo ID sera 1';
    END IF;

    -- sucursal
    SELECT COALESCE(MAX(id_sucursal), 0) INTO max_id FROM sucursal;
    IF max_id > 0 THEN
        PERFORM setval('sucursal_id_sucursal_seq', max_id);
        RAISE NOTICE 'OK sucursal: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('sucursal_id_sucursal_seq', 1, false);
        RAISE NOTICE 'VACIA sucursal: Tabla vacia, proximo ID sera 1';
    END IF;

    -- valida
    SELECT COALESCE(MAX(id_valida), 0) INTO max_id FROM valida;
    IF max_id > 0 THEN
        PERFORM setval('valida_id_valida_seq', max_id);
        RAISE NOTICE 'OK valida: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('valida_id_valida_seq', 1, false);
        RAISE NOTICE 'VACIA valida: Tabla vacia, proximo ID sera 1';
    END IF;

    -- vendedor_comision
    SELECT COALESCE(MAX(id_vendedor_comision), 0) INTO max_id FROM vendedor_comision;
    IF max_id > 0 THEN
        PERFORM setval('vendedor_comision_id_vendedor_comision_seq', max_id);
        RAISE NOTICE 'OK vendedor_comision: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('vendedor_comision_id_vendedor_comision_seq', 1, false);
        RAISE NOTICE 'VACIA vendedor_comision: Tabla vacia, proximo ID sera 1';
    END IF;

    -- vendedor
    SELECT COALESCE(MAX(id_vendedor), 0) INTO max_id FROM vendedor;
    IF max_id > 0 THEN
        PERFORM setval('vendedor_id_vendedor_seq', max_id);
        RAISE NOTICE 'OK vendedor: max_id=%, proximo ID=%', max_id, max_id + 1;
    ELSE
        PERFORM setval('vendedor_id_vendedor_seq', 1, false);
        RAISE NOTICE 'VACIA vendedor: Tabla vacia, proximo ID sera 1';
    END IF;

END $$;
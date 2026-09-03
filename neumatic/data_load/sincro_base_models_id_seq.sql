-- sincro_base_models_id_seq.sql
-- Actualiza las secuencias de todas las tablas maestras (modelos en base_models.py)
-- para que el próximo ID sea el máximo actual + 1.
-- Si la tabla está vacía, reinicia la secuencia a 1.

DO $$
DECLARE
    tablas_cols TEXT[][] := ARRAY[
        ['actividad', 'id_actividad'],
        ['producto_deposito', 'id_producto_deposito'],
        ['producto_familia', 'id_producto_familia'],
        ['moneda', 'id_moneda'],
        ['producto_marca', 'id_producto_marca'],
        ['producto_modelo', 'id_modelo'],
        ['producto_cai', 'id_cai'],
        ['producto_minimo', 'id_producto_minimo'],
        ['producto_stock', 'id_producto_stock'],
        ['producto_estado', 'id_producto_estado'],
        ['comprobante_venta', 'id_comprobante_venta'],
        ['comprobante_compra', 'id_comprobante_compra'],
        ['provincia', 'id_provincia'],
        ['localidad', 'id_localidad'],
        ['tipo_documento_identidad', 'id_tipo_documento_identidad'],
        ['tipo_iva', 'id_tipo_iva'],
        ['tipo_percepcion_ib', 'id_tipo_percepcion_ib'],
        ['tipo_retencion_ib', 'id_tipo_retencion_ib'],
        ['operario', 'id_operario'],
        ['medio_pago', 'id_medio_pago'],
        ['punto_venta', 'id_punto_venta'],
        ['codigo_alicuota', 'id_alicuota_iva'],
        ['banco', 'id_banco'],
        ['cuenta_banco', 'id_cuenta_banco'],
        ['tarjeta', 'id_tarjeta'],
        ['codigo_retencion', 'id_codigo_retencion'],
        ['concepto_banco', 'id_concepto_banco'],
        ['marketing_origen', 'id_marketing_origen'],
        ['leyenda', 'id_leyenda'],
        ['medidas_estados', 'id_medida_estado'],
        ['forma_pago', 'id_forma_pago']
    ];
    i INTEGER;
    seq_name TEXT;
    max_id INTEGER;
    tabla TEXT;
    columna TEXT;
BEGIN
    FOR i IN 1..array_length(tablas_cols, 1) LOOP
        tabla := tablas_cols[i][1];
        columna := tablas_cols[i][2];

        -- Obtener el nombre de la secuencia automáticamente
        seq_name := pg_get_serial_sequence(tabla, columna);

        IF seq_name IS NULL THEN
            RAISE NOTICE 'No se encontró secuencia para %.%', tabla, columna;
            CONTINUE;
        END IF;

        -- Obtener el máximo valor actual
        EXECUTE format('SELECT COALESCE(MAX(%I), 0) FROM %I', columna, tabla) INTO max_id;

        IF max_id > 0 THEN
            PERFORM setval(seq_name, max_id);
            RAISE NOTICE 'Tabla %: secuencia ajustada a %, próximo ID %', tabla, max_id, max_id + 1;
        ELSE
            PERFORM setval(seq_name, 1, false);
            RAISE NOTICE 'Tabla % vacía, secuencia reiniciada a 1', tabla;
        END IF;
    END LOOP;
END $$;
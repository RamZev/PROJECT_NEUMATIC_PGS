-- sincro_maestros_id_seq.sql
-- Actualiza las secuencias de las tablas maestras (modelos de cliente, descuento, empresa, numero, parametro, producto, proveedor, sucursal, valida, vendedor, etc.)
-- para que el próximo ID sea el máximo actual + 1.
-- Si la tabla está vacía, reinicia la secuencia a 1.

DO $$
DECLARE
    tablas_cols TEXT[][] := ARRAY[
        ['cliente', 'id_cliente'],
        ['descuento_vendedor', 'id_descuento_vendedor'],
        ['descuento_revendedor', 'id_descuento_revendedor'],
        ['empresa', 'id_empresa'],
        ['numero', 'id_numero'],
        ['parametro', 'id_parametro'],
        ['producto', 'id_producto'],
        ['proveedor', 'id_proveedor'],
        ['sucursal', 'id_sucursal'],
        ['valida', 'id_valida'],
        ['vendedor_comision', 'id_vendedor_comision'],
        ['detalle_vendedor_comision', 'id_detalle_vendedor_comision'],
        ['vendedor', 'id_vendedor']
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
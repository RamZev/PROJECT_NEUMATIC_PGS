DO $$
DECLARE
    tablas_cols TEXT[][] := ARRAY[
        ['auth_group', 'id'],
        ['auth_group_permissions', 'id'],
        ['usuarios_user', 'id'],
        ['usuarios_user_groups', 'id'],
        ['menu_menuheading', 'id_menu_heading'],
        ['menu_menuitem', 'id_menu_item'],
        ['menu_menuitem_groups', 'id']
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

        -- Obtener el nombre de la secuencia automaticamente
        seq_name := pg_get_serial_sequence(tabla, columna);

        IF seq_name IS NULL THEN
            RAISE NOTICE 'No se encontro secuencia para %.%', tabla, columna;
            CONTINUE;
        END IF;

        -- Obtener el maximo valor actual
        EXECUTE format('SELECT COALESCE(MAX(%I), 0) FROM %I', columna, tabla) INTO max_id;

        IF max_id > 0 THEN
            PERFORM setval(seq_name, max_id);
            RAISE NOTICE 'Tabla %: secuencia ajustada a %, proximo ID %', tabla, max_id, max_id + 1;
        ELSE
            PERFORM setval(seq_name, 1, false);
            RAISE NOTICE 'Tabla % vacia, secuencia reiniciada a 1', tabla;
        END IF;
    END LOOP;
END $$;
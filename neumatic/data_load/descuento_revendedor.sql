DO $$
BEGIN
    TRUNCATE TABLE descuento_revendedor RESTART IDENTITY;

    INSERT INTO descuento_revendedor (
        usuario, estacion, fcontrol, fcontrol2,
        estatus_descuento_revendedor, descuento,
        id_user_id, id_user_update_id,
        id_familia_id, id_marca_id
    ) VALUES
        (NULL, NULL, NULL, NULL, true, 4.00, NULL, NULL, 1, 1),
        (NULL, NULL, NULL, NULL, true, 4.00, NULL, NULL, 2, 1),
        (NULL, NULL, NULL, NULL, true, 4.00, NULL, NULL, 1, 2),
        (NULL, NULL, NULL, NULL, true, 4.00, NULL, NULL, 2, 2);

    RAISE NOTICE 'Proceso completado con éxito. 4 registros insertados.';
END $$;
-- ============================================
-- CONVERSIÓN DE SQL SERVER A POSTGRESQL 18
-- Tabla: usuarios_user_groups
-- ============================================

-- Eliminar datos existentes
DELETE FROM usuarios_user_groups;

-- Resetear la secuencia (el próximo ID será 1)
SELECT setval(pg_get_serial_sequence('usuarios_user_groups', 'id'), 1, false);

-- Insertar registros (PostgreSQL permite inserción explícita de IDs)
INSERT INTO usuarios_user_groups (id, user_id, group_id) VALUES (1, 3, 2);
INSERT INTO usuarios_user_groups (id, user_id, group_id) VALUES (2, 4, 1);
INSERT INTO usuarios_user_groups (id, user_id, group_id) VALUES (3, 5, 3);
INSERT INTO usuarios_user_groups (id, user_id, group_id) VALUES (4, 6, 4);
INSERT INTO usuarios_user_groups (id, user_id, group_id) VALUES (5, 7, 2);

-- ACTUALIZAR LA SECUENCIA AL MÁXIMO ID INSERTADO
SELECT setval(pg_get_serial_sequence('usuarios_user_groups', 'id'), (SELECT MAX(id) FROM usuarios_user_groups));

-- Verificar
SELECT * FROM usuarios_user_groups;

-- Verificar el valor actual de la secuencia
SELECT currval(pg_get_serial_sequence('usuarios_user_groups', 'id'));
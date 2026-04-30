-- ============================================
-- CONVERSIÓN DE SQL SERVER A POSTGRESQL 18
-- Tabla: auth_group
-- ============================================

-- Eliminar datos existentes
DELETE FROM auth_group;

-- Resetear la secuencia (el próximo ID será 1)
SELECT setval(pg_get_serial_sequence('auth_group', 'id'), 1, false);

-- Insertar registros
INSERT INTO auth_group (id, name) VALUES (1, 'Administracion');
INSERT INTO auth_group (id, name) VALUES (2, 'Puntos de Ventas');
INSERT INTO auth_group (id, name) VALUES (3, 'Vendedores');
INSERT INTO auth_group (id, name) VALUES (4, 'Encargado Sucursal');
INSERT INTO auth_group (id, name) VALUES (5, 'Deposito');

-- ACTUALIZAR LA SECUENCIA AL MÁXIMO ID INSERTADO
SELECT setval(pg_get_serial_sequence('auth_group', 'id'), (SELECT MAX(id) FROM auth_group));

-- Verificar
SELECT * FROM auth_group;

-- Verificar el valor actual de la secuencia
SELECT currval(pg_get_serial_sequence('auth_group', 'id'));
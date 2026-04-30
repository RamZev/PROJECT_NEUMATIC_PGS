-- ============================================
-- CONVERSIÓN DE SQL SERVER A POSTGRESQL 18
-- Tabla: usuarios_user
-- Omitiendo el registro con ID 1 (admin)
-- ============================================

-- Eliminar datos existentes (opcional)
-- DELETE FROM usuarios_user;

-- Resetear la secuencia (el próximo ID será 2)
SELECT setval(pg_get_serial_sequence('usuarios_user', 'id'), 2, false);

-- Insertar registros (PostgreSQL permite inserción explícita de IDs)

-- Insertar registro ID 3 (juan)
INSERT INTO usuarios_user (
    id, password, last_login, is_superuser, username, first_name, last_name, 
    is_staff, is_active, date_joined, email
) VALUES (
    3, 'pbkdf2_sha256$870000$VxZxUdecBPWNbdOC2NT0O8$v+2pfRIJfBuYNid3z/yeQoHutMVLMS3kIVEOCaNDC94=', 
    '2025-10-31 21:31:20.829689', FALSE, 'juan', 'Juan', '', FALSE, TRUE, '2025-10-30 01:20:56', 
    '123@gmail.com'
);

-- Insertar registro ID 4 (alberto)
INSERT INTO usuarios_user (
    id, password, last_login, is_superuser, username, first_name, last_name, 
    is_staff, is_active, date_joined, email
) VALUES (
    4, 'pbkdf2_sha256$870000$2FjwXmFRoOyPNKXGLMzfB7$ceZt+VBs4p2mZn3Y6il7yrc0KBKgTWy0e99vOYnBRNk=', 
    '2025-10-31 22:47:15.940314', FALSE, 'alberto', 'Alberto', 'García', FALSE, TRUE, '2025-10-30 01:25:10', 
    'albertogarcia@gmail.com'
);

-- Insertar registro ID 5 (maria)
INSERT INTO usuarios_user (
    id, password, last_login, is_superuser, username, first_name, last_name, 
    is_staff, is_active, date_joined, email
) VALUES (
    5, 'pbkdf2_sha256$870000$l40YysYnE3ID1ZZIOPsfAj$Aaxjq1481WTHcFDe7lwbOFcCqFVgDv/WmURd/x7EAy0=', 
    '2025-10-31 22:31:58.343834', FALSE, 'maria', 'Maria', 'Diaz', FALSE, TRUE, '2025-10-31 21:51:50.381092', 
    'ramosric1410@gmail.com'
);

-- Insertar registro ID 6 (Federico)
INSERT INTO usuarios_user (
    id, password, last_login, is_superuser, username, first_name, last_name, 
    is_staff, is_active, date_joined, email
) VALUES (
    6, 'pbkdf2_sha256$870000$fFAOOQLUxTFUAHVmgZwaS4$t8OAdExznmrFxKq/bH8gChcYoqxkzMrtOJDsdZZqIzM=', 
    '2025-11-02 14:21:57.721893', FALSE, 'Federico', 'Federico', 'Camiletti', FALSE, TRUE, '2025-11-01 21:53:35.673835', 
    'fede@ndebona.com'
);

-- Insertar registro ID 7 (Francisco)
INSERT INTO usuarios_user (
    id, password, last_login, is_superuser, username, first_name, last_name, 
    is_staff, is_active, date_joined, email
) VALUES (
    7, 'pbkdf2_sha256$870000$o7GYQGdqOXdFTLlh8Xxfh1$/pfISSbe28pBVBAqGH4e5wF7dnLOXBH6KTddMwiirRU=', 
    '2025-12-12 22:55:50.858369', FALSE, 'Francisco', 'Francisco', '', FALSE, TRUE, '2025-11-02 13:58:45.399568', 
    'fran@ndebona.com'
);

-- ACTUALIZAR LA SECUENCIA AL MÁXIMO ID INSERTADO
SELECT setval(pg_get_serial_sequence('usuarios_user', 'id'), (SELECT MAX(id) FROM usuarios_user));

-- Verificar los registros insertados
SELECT id, username, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined FROM usuarios_user;

-- Verificar el valor actual de la secuencia
SELECT currval(pg_get_serial_sequence('usuarios_user', 'id'));
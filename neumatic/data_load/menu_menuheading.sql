-- ============================================
-- CONVERSIÓN DE SQL SERVER A POSTGRESQL 18
-- Tabla: menu_menuheading
-- ============================================

-- Eliminar datos existentes
DELETE FROM menu_menuheading;

-- Resetear la secuencia (el próximo ID será 1)
SELECT setval(pg_get_serial_sequence('menu_menuheading', 'id_menu_heading'), 1, false);

-- Insertar registros (PostgreSQL permite inserción explícita de IDs)
INSERT INTO menu_menuheading (id_menu_heading, name, "order") VALUES (1, 'Archivos', 0);
INSERT INTO menu_menuheading (id_menu_heading, name, "order") VALUES (2, 'Ventas', 1);
INSERT INTO menu_menuheading (id_menu_heading, name, "order") VALUES (3, 'Compras', 3);
INSERT INTO menu_menuheading (id_menu_heading, name, "order") VALUES (4, 'Informes', 2);
INSERT INTO menu_menuheading (id_menu_heading, name, "order") VALUES (6, 'Estadísticas Ventas', 6);
INSERT INTO menu_menuheading (id_menu_heading, name, "order") VALUES (7, 'Configurar menú', 8);
INSERT INTO menu_menuheading (id_menu_heading, name, "order") VALUES (8, 'Tablas Dinamicas', 7);
INSERT INTO menu_menuheading (id_menu_heading, name, "order") VALUES (9, 'Caja', 5);

-- ACTUALIZAR LA SECUENCIA AL MÁXIMO ID INSERTADO
SELECT setval(pg_get_serial_sequence('menu_menuheading', 'id_menu_heading'), (SELECT MAX(id_menu_heading) FROM menu_menuheading));

-- Verificar
SELECT * FROM menu_menuheading;

-- Verificar el valor actual de la secuencia
SELECT currval(pg_get_serial_sequence('menu_menuheading', 'id_menu_heading'));
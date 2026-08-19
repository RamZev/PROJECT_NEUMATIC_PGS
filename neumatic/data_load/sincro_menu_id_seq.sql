-- Seteo de id de items de menú:
SELECT setval('menu_menuitem_id_menu_item_seq', (SELECT MAX(id_menu_item) FROM menu_menuitem));
-- Seteo del id de los encabezados
SELECT setval('menu_menuheading_id_menu_heading_seq', (SELECT MAX(id_menu_heading) FROM menu_menuheading));--
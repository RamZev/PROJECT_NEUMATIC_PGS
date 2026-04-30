-- Reordenar los números para que sean consecutivos de las opciones de: Archivos -> Ventas
UPDATE "main"."menu_menuitem" SET "order" =  1 WHERE parent_id = 135 AND "name" = 'Vendedores';

UPDATE "main"."menu_menuitem" SET "order" =  4 WHERE parent_id = 135 AND "name" = 'Números';
UPDATE "main"."menu_menuitem" SET "order" =  5 WHERE parent_id = 135 AND "name" = 'Comprobantes de Ventas';
UPDATE "main"."menu_menuitem" SET "order" =  6 WHERE parent_id = 135 AND "name" = 'Operarios';
UPDATE "main"."menu_menuitem" SET "order" =  7 WHERE parent_id = 135 AND "name" = 'Formas de Pago';
UPDATE "main"."menu_menuitem" SET "order" =  8 WHERE parent_id = 135 AND "name" = 'Medios de Pagos';
UPDATE "main"."menu_menuitem" SET "order" =  9 WHERE parent_id = 135 AND "name" = 'Puntos de Venta';
UPDATE "main"."menu_menuitem" SET "order" = 10 WHERE parent_id = 135 AND "name" = 'Marketins Origen';
-- Corregir la ortografía de la siguiente opción:
UPDATE "main"."menu_menuitem" SET "name" = 'Marketing Origen' WHERE parent_id = 135 AND "name" = 'Marketins Origen';

-- Script para agregar nuevas opciones en: Archivos -> Ventas
INSERT INTO "main"."menu_menuitem" ("name", "url_name", "query_params", "icon", "is_collapse", "order", "heading_id", "parent_id")
	VALUES ('Descuento Vendedor', 'descuento_vendedor_list', '', '', '0', 2, NULL, 135);
INSERT INTO "main"."menu_menuitem" ("name", "url_name", "query_params", "icon", "is_collapse", "order", "heading_id", "parent_id")
	VALUES ('Descuento Revendedor', 'descuento_revendedor_list', '', '', '0', 3, NULL, 135);


-- Reordenar los números para que sean consecutivos de las opciones de: Informes -> Ventas
UPDATE "main"."menu_menuitem" SET "order" =  7 WHERE parent_id = 80 AND "name" = 'Remitos por Cliente';
UPDATE "main"."menu_menuitem" SET "order" =  8 WHERE parent_id = 80 AND "name" = 'Totales de Remitos por Cliente';
UPDATE "main"."menu_menuitem" SET "order" =  9 WHERE parent_id = 80 AND "name" = 'Comprobantes de Ventas por Localidad';
UPDATE "main"."menu_menuitem" SET "order" = 10 WHERE parent_id = 80 AND "name" = 'Ventas por Mostrador';
UPDATE "main"."menu_menuitem" SET "order" = 11 WHERE parent_id = 80 AND "name" = 'Total de Ventas por Comprobantes';
UPDATE "main"."menu_menuitem" SET "order" = 12 WHERE parent_id = 80 AND "name" = 'Comprobantes Vencidos';
UPDATE "main"."menu_menuitem" SET "order" = 13 WHERE parent_id = 80 AND "name" = 'Remitos Pendientes';
UPDATE "main"."menu_menuitem" SET "order" = 14 WHERE parent_id = 80 AND "name" = 'Remitos por Vendedor';
UPDATE "main"."menu_menuitem" SET "order" = 15 WHERE parent_id = 80 AND "name" = 'Resumen de Ventas I. Brutos Mercadolibre';
UPDATE "main"."menu_menuitem" SET "order" = 16 WHERE parent_id = 80 AND "name" = 'Libro I.V.A. Ventas';
UPDATE "main"."menu_menuitem" SET "order" = 17 WHERE parent_id = 80 AND "name" = 'Percepciones por Vendedor';
UPDATE "main"."menu_menuitem" SET "order" = 18 WHERE parent_id = 80 AND "name" = 'Comisiones a Vendedores según Facturas';
UPDATE "main"."menu_menuitem" SET "order" = 19 WHERE parent_id = 80 AND "name" = 'Comisiones a Operarios';
UPDATE "main"."menu_menuitem" SET "order" = 20 WHERE parent_id = 80 AND "name" = 'Comprobantes Ventas';
UPDATE "main"."menu_menuitem" SET "order" = 21 WHERE parent_id = 80 AND "name" = 'Diferencias de Precios en Facturación';
UPDATE "main"."menu_menuitem" SET "order" = 22 WHERE parent_id = 80 AND "name" = 'Números';
UPDATE "main"."menu_menuitem" SET "order" = 23 WHERE parent_id = 80 AND "name" = 'Operarios';
UPDATE "main"."menu_menuitem" SET "order" = 24 WHERE parent_id = 80 AND "name" = 'Medios de Pago';
UPDATE "main"."menu_menuitem" SET "order" = 25 WHERE parent_id = 80 AND "name" = 'Puntos de Venta';
UPDATE "main"."menu_menuitem" SET "order" = 26 WHERE parent_id = 80 AND "name" = 'Marketing Origen';

-- Script para agregar nuevas opciones en: Informes -> Ventas
INSERT INTO "main"."menu_menuitem" ("name", "url_name", "query_params", "icon", "is_collapse", "order", "heading_id", "parent_id")
	VALUES ('Descuento Vendedor', 'descuentovendedor_informe_list', '', '', '0', 5, NULL, 80);
INSERT INTO "main"."menu_menuitem" ("name", "url_name", "query_params", "icon", "is_collapse", "order", "heading_id", "parent_id")
	VALUES ('Descuento Revendedor', 'descuentorevendedor_informe_list', '', '', '0', 6, NULL, 80);


-----------------------------------------------------------------------------------------------------------------------------------------------


-- Script para crear nueva opción en: Archivos -> Productos -> Actualizaciones.
INSERT INTO "main"."menu_menuitem" ("name", "url_name", "query_params", "icon", "is_collapse", "order", "heading_id", "parent_id")
VALUES ('Actualizar Estados de Productos por CAI', 'actualizar_estados_cargar', '', '', '0', 3, NULL, 138);


-- Script para modificar el nombre de la opción: Archivos -> Productos.
UPDATE "main"."menu_menuitem" SET "name" = 'Estados de Productos por CAI' WHERE parent_id = 136 AND "name" = 'Estados de Productos por Medidas';


-- Script para reordenar las opciones en: Informes -> Productos:
UPDATE "main"."menu_menuitem" SET "order" =  9 WHERE parent_id = 53 AND "name" = 'Depósitos';
UPDATE "main"."menu_menuitem" SET "order" = 10 WHERE parent_id = 53 AND "name" = 'Mínimos por CAI';
UPDATE "main"."menu_menuitem" SET "order" = 11 WHERE parent_id = 53 AND "name" = 'Stock';


-- Script para agregar nueva opción en: Informes -> Productos.
INSERT INTO "main"."menu_menuitem" ("name", "url_name", "query_params", "icon", "is_collapse", "order", "heading_id", "parent_id")
VALUES ('Estados de Productos por CAI', 'medidasestados_informe_list', '', '', '0', 8, NULL, 53);


-----------------------------------------------------------------------------------------------------------------------------------------------


-- Script para actualizar la url de la opción: Archivos -> Productos.
UPDATE "main"."menu_menuitem" SET "url_name" = 'cai_estados_list' WHERE parent_id = 136 AND "name" = 'Estados de Productos por CAI';


-- Script para actualizar la url de la opción: Informes -> Productos.
UPDATE "main"."menu_menuitem" SET "url_name" = 'caiestados_informe_list' WHERE parent_id = 53 AND "name" = 'Estados de Productos por CAI';

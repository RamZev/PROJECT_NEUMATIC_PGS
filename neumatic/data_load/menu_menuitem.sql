-- ============================================
-- CONVERSIÓN DE SQL SERVER A POSTGRESQL 18
-- Tabla: menu_menuitem
-- ============================================

-- Eliminar todos los registros de la tabla
DELETE FROM menu_menuitem;

-- Resetear la secuencia (el próximo ID será 1)
SELECT setval(pg_get_serial_sequence('menu_menuitem', 'id_menu_item'), 1, false);

-- Insertar registros (PostgreSQL permite inserción explícita de IDs)

INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (1, 'Comunes', '', '', '', TRUE, 3, 1, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (2, 'Clientes', 'cliente_list', '', '', FALSE, 0, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (3, 'Proveedores', 'proveedor_list', '', '', FALSE, 1, NULL, 137);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (4, 'Productos', 'producto_list', '', '', FALSE, 1, NULL, 136);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (5, 'Vendedores', 'vendedor_list', '', '', FALSE, 1, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (6, 'Empresa', 'empresa_list', '', '', FALSE, 4, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (7, 'Sucursales', 'sucursal_list', '', '', FALSE, 5, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (8, 'Números', 'numero_list', '', '', FALSE, 4, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (9, 'Bancos', '', '', '', TRUE, 4, 1, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (10, 'Actividad', 'actividad_list', '', '', FALSE, 0, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (11, 'Depósitos', 'producto_deposito_list', '', '', FALSE, 9, NULL, 136);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (12, 'Familias', 'producto_familia_list', '', '', FALSE, 2, NULL, 136);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (13, 'Marca', 'producto_marca_list', '', '', FALSE, 3, NULL, 136);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (14, 'Modelos', 'producto_modelo_list', '', '', FALSE, 4, NULL, 136);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (15, 'CAI', 'producto_cai_list', '', '', FALSE, 5, NULL, 136);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (16, 'Estados Productos', 'producto_estado_list', '', '', FALSE, 6, NULL, 136);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (17, 'Estados de Productos por CAI', 'cai_estados_list', '', '', FALSE, 7, NULL, 136);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (18, 'Comprobantes de Ventas', 'comprobante_venta_list', '', '', FALSE, 5, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (19, 'Comprobantes de Compras', 'comprobante_compra_list', '', '', FALSE, 9, NULL, 137);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (20, 'Monedas', 'moneda_list', '', '', FALSE, 10, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (21, 'Provincias', 'provincia_list', '', '', FALSE, 11, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (22, 'Localidades', 'localidad_list', '', '', FALSE, 12, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (23, 'Tipo Documento', 'tipo_documento_identidad_list', '', '', FALSE, 13, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (24, 'Tipo IVA', 'tipo_iva_list', '', '', FALSE, 14, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (25, 'Alícuotas IVA', 'alicuota_iva_list', '', '', FALSE, 15, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (26, 'Tipo Percepción', 'tipo_percepcion_ib_list', '', '', FALSE, 16, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (27, 'Tipo Retención', 'tipo_retencion_ib_list', '', '', FALSE, 17, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (28, 'Operarios', 'operario_list', '', '', FALSE, 6, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (29, 'Medios de Pagos', 'medio_pago_list', '', '', FALSE, 8, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (30, 'Puntos de Venta', 'punto_venta_list', '', '', FALSE, 9, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (31, 'Bancos Nacionales', 'banco_list', '', '', FALSE, 21, NULL, 9);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (32, 'Cuentas de Bancos', 'cuenta_banco_list', '', '', FALSE, 22, NULL, 9);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (33, 'Tarjetas', 'tarjeta_list', '', '', FALSE, 23, NULL, 9);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (34, 'Códigos de Retención', 'codigo_retencion_list', '', '', FALSE, 24, NULL, 1);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (35, 'Conceptos de Bancos', 'concepto_banco_list', '', '', FALSE, 25, NULL, 9);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (36, 'Marketing Origen', 'marketing_origen_list', '', '', FALSE, 10, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (37, 'Comprobante Electrónico', 'factura_list', '', '', FALSE, 0, 2, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (38, 'Comprobante Manual', 'factura_manual_list', '', '', FALSE, 1, 2, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (39, 'Recibo', 'recibo_list', '', '', FALSE, 2, 2, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (40, 'Presupuesto', 'presupuesto_list', '', '', FALSE, 3, 2, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (41, 'Movimiento Interno', 'movimiento_interno_list', '', '', FALSE, 4, 2, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (42, 'Remitos', 'compra_list', '', '', FALSE, 0, 3, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (43, 'Retenciones', 'compra_retencion_list', '', '', FALSE, 1, 3, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (44, 'Comunes', '', '', '', TRUE, 4, 4, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (45, 'Clientes', 'cliente_informe_list', '', '', FALSE, 0, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (47, 'Productos', 'producto_informe_list', '', '', FALSE, 0, NULL, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (48, 'Vendedores', 'vendedor_informe_list', '', '', FALSE, 4, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (49, 'Empresa', '', '', '', FALSE, 4, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (50, 'Sucursales', 'sucursal_informe_list', '', '', FALSE, 5, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (51, 'Parámetros', '', '', '', FALSE, 6, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (52, 'Números', '', '', '', FALSE, 22, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (53, 'Productos', '', '', '', TRUE, 2, 4, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (54, 'Actividades', 'actividad_informe_list', '', '', FALSE, 0, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (55, 'Depósitos', 'productodeposito_informe_list', '', '', FALSE, 9, NULL, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (56, 'Familias', 'productofamilia_informe_list', '', '', FALSE, 3, NULL, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (57, 'Marcas', 'productomarca_informe_list', '', '', FALSE, 4, NULL, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (58, 'Modelos', 'productomodelo_informe_list', '', '', FALSE, 5, NULL, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (59, 'CAIs', 'productocai_informe_list', '', '', FALSE, 6, NULL, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (60, 'Estados', 'productoestado_informe_list', '', '', FALSE, 7, NULL, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (61, 'Comprobantes Ventas', 'comprobanteventa_informe_list', '', '', FALSE, 20, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (63, 'Monedas', 'moneda_informe_list', '', '', FALSE, 9, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (64, 'Provincias', 'provincia_informe_list', '', '', FALSE, 10, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (65, 'Localidades', 'localidad_informe_list', '', '', FALSE, 11, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (66, 'Tipos Documento', 'tipodocumentoidentidad_informe_list', '', '', FALSE, 12, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (67, 'Tipos Iva', 'tipoiva_informe_list', '', '', FALSE, 13, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (68, 'Alícuotas IVA', 'alicuotaiva_informe_list', '', '', FALSE, 14, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (69, 'Tipos Percepción', 'tipopercepcionib_informe_list', '', '', FALSE, 15, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (70, 'Tipos Retención', 'tiporetencionib_informe_list', '', '', FALSE, 16, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (71, 'Operarios', 'operario_informe_list', '', '', FALSE, 23, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (72, 'Medios de Pago', 'mediopago_informe_list', '', '', FALSE, 24, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (73, 'Puntos de Venta', 'puntoventa_informe_list', '', '', FALSE, 25, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (74, 'Bancos', 'banco_informe_list', '', '', FALSE, 20, NULL, 140);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (75, 'Cuentas de Bancos', 'cuentabanco_informe_list', '', '', FALSE, 21, NULL, 140);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (76, 'Tarjetas', 'tarjeta_informe_list', '', '', FALSE, 22, NULL, 140);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (77, 'Códigos de Retención', 'codigoretencion_informe_list', '', '', FALSE, 23, NULL, 44);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (78, 'Conceptos de Banco', 'conceptobanco_informe_list', '', '', FALSE, 24, NULL, 140);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (79, 'Marketing Origen', 'marketingorigen_informe_list', '', '', FALSE, 26, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (80, 'Ventas', '', '', '', TRUE, 1, 4, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (81, 'Saldos de Clientes', 'vlsaldosclientes_informe_list', '', '', FALSE, 1, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (82, 'Resumen de Cuenta Corriente', 'vlresumenctacte_informe_list', '', '', FALSE, 2, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (83, 'Mercadería por Cliente', 'vlmercaderiaporcliente_informe_list', '', '', FALSE, 3, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (84, 'Remitos por Cliente', 'vlremitosclientes_informe_list', '', '', FALSE, 7, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (85, 'Totales de Remitos por Cliente', 'vltotalremitosclientes_informe_list', '', '', FALSE, 8, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (86, 'Comprobantes de Ventas por Localidad', 'vlventacomprolocalidad_informe_list', '', '', FALSE, 9, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (87, 'Ventas por Mostrador', 'vlventamostrador_informe_list', '', '', FALSE, 10, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (88, 'Total de Ventas por Comprobantes', 'vlventacompro_informe_list', '', '', FALSE, 11, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (89, 'Comprobantes Vencidos', 'vlcomprobantesvencidos_informe_list', '', '', FALSE, 12, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (90, 'Remitos Pendientes', 'vlremitospendientes_informe_list', '', '', FALSE, 13, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (91, 'Remitos por Vendedor', 'vlremitosvendedor_informe_list', '', '', FALSE, 14, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (92, 'Libro I.V.A. Ventas', '', '', '', TRUE, 16, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (93, 'Detallado', 'vlivaventasfull_informe_list', '', '', FALSE, 0, NULL, 92);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (94, 'Totales por Provincia', 'vlivaventasprovincias_informe_list', '', '', FALSE, 1, NULL, 92);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (95, 'Totales para SITRIB', 'vlivaventassitrib_informe_list', '', '', FALSE, 2, NULL, 92);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (96, 'Percepciones por Vendedor', '', '', '', TRUE, 17, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (97, 'Vendedores - Solo Totales', 'vlpercepibvendedortotales_informe_list', '', '', FALSE, 0, NULL, 96);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (98, 'Vendedores - Detallado por Comprobantes', 'vlpercepibvendedordetallado_informe_list', '', '', FALSE, 1, NULL, 96);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (99, 'Sub Cuentas - Solo Totales', 'vlpercepibsubcuentatotales_informe_list', '', '', FALSE, 2, NULL, 96);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (100, 'Sub Cuentas - Detallado por Comprobantes', 'vlpercepibsubcuentadetallado_informe_list', '', '', FALSE, 3, NULL, 96);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (101, 'Comisiones a Vendedores según Facturas', 'vlcomisionvendedor_informe_list', '', '', FALSE, 18, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (102, 'Comisiones a Operarios', 'vlcomisionoperario_informe_list', '', '', FALSE, 19, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (103, 'Diferencias de Precios en Facturación', 'vlpreciodiferente_informe_list', '', '', FALSE, 21, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (104, 'Resumen de Ventas I. Brutos Mercadolibre', 'vlventasresumenib_informe_list', '', '', FALSE, 15, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (106, 'Lista de Precios', 'vllista_informe_list', '', '', FALSE, 1, NULL, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (107, 'Lista de Precios a Revendedores', 'vllistarevendedor_informe_list', '', '', FALSE, 2, NULL, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (108, 'Listado de Stock por Sucursal', 'vlstocksucursal_informe_list', '', '', FALSE, 0, NULL, 141);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (109, 'Stock General por Sucursal', 'vlstockgeneralsucursal_informe_list', '', '', FALSE, 1, NULL, 141);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (110, 'Listado de Stock Único', 'vlstockunico_informe_list', '', '', FALSE, 2, NULL, 141);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (111, 'Reposición de Stock', 'vlreposicionstock_informe_list', '', '', FALSE, 3, NULL, 141);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (112, 'Actualizar Productos (Excel)', 'cargar_excel', 'proceso=actualizar', '', FALSE, 0, 1, 138);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (113, 'Agregar nuevos Productos (Excel)', 'cargar_excel', 'proceso=agregar', '', FALSE, 1, 1, 138);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (114, 'Estadísticas de Ventas', 'vlestadisticasventas_informe_list', '', '', FALSE, 0, 6, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (115, 'Estadísticas de Ventas Vendedores', 'vlestadisticasventasvendedor_informe_list', '', '', FALSE, 1, 6, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (116, 'Estadísticas de Ventas Vendedores Clientes', 'vlestadisticasventasvendedorcliente_informe_list', '', '', FALSE, 2, 6, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (117, 'Ventas de Productos Según Condición', 'vlestadisticasseguncondicion_informe_list', '', '', FALSE, 3, 6, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (118, 'Estadísticas de Ventas por Marca', 'vlestadisticasventasmarca_informe_list', '', '', FALSE, 4, 6, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (119, 'Estadísticas de Ventas por Marca-Vendedor', 'vlestadisticasventasmarcavendedor_informe_list', '', '', FALSE, 5, 6, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (120, 'Estadísticas de Clientes sin Movimiento', 'vlclienteultimaventa_informe_list', '', '', FALSE, 6, 6, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (121, 'Estadísticas de Ventas por Provincia', 'vlestadisticasventasprovincia_informe_list', '', '', FALSE, 7, 6, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (122, 'Comprobantes sin Estadísticas', 'vlventasinestadistica_informe_list', '', '', FALSE, 8, 6, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (124, 'Ventas por Comprobantes', 'vltabladinamicaventas_informe_list', '', '', FALSE, 0, 8, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (125, 'Detalle de Ventas por Productos', 'vltabladinamicadetalleventas_informe_list', '', '', FALSE, 1, 8, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (126, 'Tablas para Estadísticas', 'vltabladinamicaestadistica_informe_list', '', '', FALSE, 2, 8, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (131, 'Movimiento Interno de Stock', 'vlmovimientointernostock_informe_list', '', 'fas fa-book-open', FALSE, 5, NULL, 141);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (135, 'Ventas', '', '', '', TRUE, 0, 1, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (136, 'Productos', '', '', '', TRUE, 1, 1, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (137, 'Compras', '', '', '', TRUE, 2, 1, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (138, 'Actualizaciones', '', '', '', TRUE, 10, 1, 136);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (140, 'Bancos', '', '', '', TRUE, 5, 4, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (141, 'Stock', '', '', '', TRUE, 11, 4, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (142, 'Compras', '', '', '', TRUE, 0, 4, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (143, 'Detalle de Compras por Proveedor', 'vldetallecompraproveedor_informe_list', '', '', FALSE, 2, NULL, 142);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (144, 'Comprobantes Ingresados', 'vlcompraingresada_informe_list', '', '', FALSE, 3, NULL, 142);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (145, 'Stock por Clientes en Depósitos', 'vlstockcliente_informe_list', '', '', FALSE, 6, NULL, 141);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (146, 'Stock en Depósitos de Clientes', 'vlstockdeposito_informe_list', '', '', FALSE, 7, NULL, 141);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (147, 'Ficha de Seguimiento de Stock', 'vlfichaseguimientostock_informe_list', '', '', FALSE, 4, NULL, 141);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (148, 'Comprobantes de Compra', 'comprobantecompra_informe_list', '', '', FALSE, 0, NULL, 142);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (149, 'Proveedores', 'proveedor_informe_list', '', '', FALSE, 1, NULL, 142);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (150, 'Caja', 'caja_list', '', '', FALSE, 0, 9, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (151, 'Actualizar Estados de Productos', 'actualizar_estados_productos', '', '', FALSE, 8, NULL, 136);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (152, 'Actualizar Mínimos por CAI', 'actualizar_minimo_cargar', '', '', FALSE, 2, NULL, 138);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (153, 'Mínimos por CAI', 'vlproductominimo_informe_list', '', '', FALSE, 10, NULL, 53);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (154, 'Movimientos de Caja', 'caja_detalle_list', '', '', FALSE, 1, 9, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (155, 'Caja', '', '', '', TRUE, 6, 4, NULL);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (156, 'Planilla de Caja', 'planillacaja_informe_list', '', '', FALSE, 0, NULL, 155);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (157, 'Egresos de Caja', 'egresoscaja_informe_list', '', '', FALSE, 2, NULL, 155);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (158, 'Detalle de Tarjetas Recibidas', 'tarjetarecibo_informe_list', '', '', FALSE, 3, NULL, 155);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (159, 'Detalle de Cupones por Fechas', 'cuponesfecha_informe_list', '', '', FALSE, 4, NULL, 155);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (160, 'Detalle de Cheques Recibidos', 'chequerecibo_informe_list', '', '', FALSE, 5, NULL, 155);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (161, 'Arqueo de Caja', 'cajaarqueo_informe_list', '', '', FALSE, 1, NULL, 155);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (162, 'Detalle de Comprobantes', 'detallecomprobantes_informe_list', '', '', FALSE, 7, NULL, 155);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (163, 'Detalle de Cheques por Fecha', 'chequesfecha_informe_list', '', '', FALSE, 6, NULL, 155);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (166, 'Formas de Pago', 'forma_pago_list', '', '', FALSE, 7, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (167, 'Descuento Vendedor', 'descuento_vendedor_list', '', '', FALSE, 2, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (168, 'Descuento Revendedor', 'descuento_revendedor_list', '', '', FALSE, 3, NULL, 135);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (169, 'Descuento Vendedor', 'descuentovendedor_informe_list', '', '', FALSE, 5, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (170, 'Descuento Revendedor', 'descuentorevendedor_informe_list', '', '', FALSE, 6, NULL, 80);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (171, 'Actualizar Estados de Productos por CAI', 'actualizar_estados_cargar', '', '', FALSE, 3, NULL, 138);
INSERT INTO menu_menuitem (id_menu_item, name, url_name, query_params, icon, is_collapse, "order", heading_id, parent_id) VALUES (175, 'Estados de Productos por CAI', 'caiestados_informe_list', '', '', FALSE, 8, NULL, 53);

-- ACTUALIZAR LA SECUENCIA AL MÁXIMO ID INSERTADO
SELECT setval(pg_get_serial_sequence('menu_menuitem', 'id_menu_item'), (SELECT MAX(id_menu_item) FROM menu_menuitem));

-- Verificar cantidad de registros insertados
SELECT COUNT(*) as TotalRegistros FROM menu_menuitem;

-- Verificar el valor actual de la secuencia
SELECT currval(pg_get_serial_sequence('menu_menuitem', 'id_menu_item'));

-- Mostrar los primeros 10 registros como muestra
SELECT id_menu_item, name, parent_id, heading_id, "order" FROM menu_menuitem ORDER BY id_menu_item LIMIT 10;
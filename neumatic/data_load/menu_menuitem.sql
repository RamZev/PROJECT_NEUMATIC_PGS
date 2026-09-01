--
-- PostgreSQL database dump
--

\restrict WaCQvFmzv6wJ21PlyuxVXl8Ow0YuJr25K8TkZeeh0OGuhgq0DawDOLA1tv9g8UU

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-09-01 00:39:03

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5388 (class 0 OID 59401)
-- Dependencies: 294
-- Data for Name: menu_menuitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.menu_menuitem VALUES (1, 'Comunes', '', '', '', true, 3, 0, 1, NULL);
INSERT INTO public.menu_menuitem VALUES (3, 'Proveedores', 'proveedor_list', '', '', false, 1, 0, NULL, 137);
INSERT INTO public.menu_menuitem VALUES (5, 'Vendedores', 'vendedor_list', '', '', false, 1, 0, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (6, 'Empresa', 'empresa_list', '', '', false, 4, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (7, 'Sucursales', 'sucursal_list', '', '', false, 5, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (8, 'Números', 'numero_list', '', '', false, 4, 0, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (9, 'Bancos', '', '', '', true, 4, 0, 1, NULL);
INSERT INTO public.menu_menuitem VALUES (10, 'Actividad', 'actividad_list', '', '', false, 0, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (11, 'Depósitos', 'producto_deposito_list', '', '', false, 9, 0, NULL, 136);
INSERT INTO public.menu_menuitem VALUES (12, 'Familias', 'producto_familia_list', '', '', false, 2, 0, NULL, 136);
INSERT INTO public.menu_menuitem VALUES (13, 'Marca', 'producto_marca_list', '', '', false, 3, 0, NULL, 136);
INSERT INTO public.menu_menuitem VALUES (14, 'Modelos', 'producto_modelo_list', '', '', false, 4, 0, NULL, 136);
INSERT INTO public.menu_menuitem VALUES (15, 'CAI', 'producto_cai_list', '', '', false, 5, 0, NULL, 136);
INSERT INTO public.menu_menuitem VALUES (16, 'Estados Productos', 'producto_estado_list', '', '', false, 6, 0, NULL, 136);
INSERT INTO public.menu_menuitem VALUES (17, 'Estados de Productos por CAI', 'cai_estados_list', '', '', false, 7, 0, NULL, 136);
INSERT INTO public.menu_menuitem VALUES (18, 'Comprobantes de Ventas', 'comprobante_venta_list', '', '', false, 5, 0, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (19, 'Comprobantes de Compras', 'comprobante_compra_list', '', '', false, 9, 0, NULL, 137);
INSERT INTO public.menu_menuitem VALUES (20, 'Monedas', 'moneda_list', '', '', false, 10, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (21, 'Provincias', 'provincia_list', '', '', false, 11, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (22, 'Localidades', 'localidad_list', '', '', false, 12, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (23, 'Tipo Documento', 'tipo_documento_identidad_list', '', '', false, 13, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (24, 'Tipo IVA', 'tipo_iva_list', '', '', false, 14, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (25, 'Alícuotas IVA', 'alicuota_iva_list', '', '', false, 15, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (26, 'Tipo Percepción', 'tipo_percepcion_ib_list', '', '', false, 16, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (27, 'Tipo Retención', 'tipo_retencion_ib_list', '', '', false, 17, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (28, 'Operarios', 'operario_list', '', '', false, 6, 0, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (29, 'Medios de Pagos', 'medio_pago_list', '', '', false, 8, 0, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (30, 'Puntos de Venta', 'punto_venta_list', '', '', false, 9, 0, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (31, 'Bancos Nacionales', 'banco_list', '', '', false, 21, 0, NULL, 9);
INSERT INTO public.menu_menuitem VALUES (32, 'Cuentas de Bancos', 'cuenta_banco_list', '', '', false, 22, 0, NULL, 9);
INSERT INTO public.menu_menuitem VALUES (33, 'Tarjetas', 'tarjeta_list', '', '', false, 23, 0, NULL, 9);
INSERT INTO public.menu_menuitem VALUES (34, 'Códigos de Retención', 'codigo_retencion_list', '', '', false, 24, 0, NULL, 1);
INSERT INTO public.menu_menuitem VALUES (35, 'Conceptos de Bancos', 'concepto_banco_list', '', '', false, 25, 0, NULL, 9);
INSERT INTO public.menu_menuitem VALUES (36, 'Marketing Origen', 'marketing_origen_list', '', '', false, 10, 0, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (41, 'Movimiento Interno', 'movimiento_interno_list', '', '', false, 4, 0, 2, NULL);
INSERT INTO public.menu_menuitem VALUES (42, 'Remitos', 'compra_list', '', '', false, 0, 0, 3, NULL);
INSERT INTO public.menu_menuitem VALUES (43, 'Retenciones', 'compra_retencion_list', '', '', false, 1, 0, 3, NULL);
INSERT INTO public.menu_menuitem VALUES (44, 'Comunes', '', '', '', true, 4, 0, 4, NULL);
INSERT INTO public.menu_menuitem VALUES (49, 'Empresa', '', '', '', false, 4, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (50, 'Sucursales', 'sucursal_informe_list', '', '', false, 5, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (51, 'Parámetros', '', '', '', false, 6, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (53, 'Productos', '', '', '', true, 2, 0, 4, NULL);
INSERT INTO public.menu_menuitem VALUES (54, 'Actividades', 'actividad_informe_list', '', '', false, 0, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (63, 'Monedas', 'moneda_informe_list', '', '', false, 9, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (64, 'Provincias', 'provincia_informe_list', '', '', false, 10, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (65, 'Localidades', 'localidad_informe_list', '', '', false, 11, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (66, 'Tipos Documento', 'tipodocumentoidentidad_informe_list', '', '', false, 12, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (67, 'Tipos Iva', 'tipoiva_informe_list', '', '', false, 13, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (68, 'Alícuotas IVA', 'alicuotaiva_informe_list', '', '', false, 14, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (69, 'Tipos Percepción', 'tipopercepcionib_informe_list', '', '', false, 15, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (70, 'Tipos Retención', 'tiporetencionib_informe_list', '', '', false, 16, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (74, 'Bancos', 'banco_informe_list', '', '', false, 20, 0, NULL, 140);
INSERT INTO public.menu_menuitem VALUES (75, 'Cuentas de Bancos', 'cuentabanco_informe_list', '', '', false, 21, 0, NULL, 140);
INSERT INTO public.menu_menuitem VALUES (76, 'Tarjetas', 'tarjeta_informe_list', '', '', false, 22, 0, NULL, 140);
INSERT INTO public.menu_menuitem VALUES (77, 'Códigos de Retención', 'codigoretencion_informe_list', '', '', false, 23, 0, NULL, 44);
INSERT INTO public.menu_menuitem VALUES (78, 'Conceptos de Banco', 'conceptobanco_informe_list', '', '', false, 24, 0, NULL, 140);
INSERT INTO public.menu_menuitem VALUES (80, 'Ventas', '', '', '', true, 1, 0, 4, NULL);
INSERT INTO public.menu_menuitem VALUES (93, 'Detallado', 'vlivaventasfull_informe_list', '', '', false, 0, 0, NULL, 92);
INSERT INTO public.menu_menuitem VALUES (2, 'Clientes', 'cliente_list', '', 'fas fa-users', false, 0, 5, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (82, 'Resumen de Cuenta Corriente', 'vlresumenctacte_informe_list', '', '', false, 3, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (37, 'Comprobante Electrónico', 'factura_list', '', 'fas fa-file-invoice-dollar', false, 0, 1, 2, NULL);
INSERT INTO public.menu_menuitem VALUES (38, 'Comprobante Manual', 'factura_manual_list', '', 'fas fa-file-signature', false, 1, 2, 2, NULL);
INSERT INTO public.menu_menuitem VALUES (39, 'Recibo', 'recibo_list', '', 'fas fa-hand-holding-usd', false, 2, 3, 2, NULL);
INSERT INTO public.menu_menuitem VALUES (40, 'Presupuesto', 'presupuesto_list', '', 'fas fa-file-invoice', false, 3, 4, 2, NULL);
INSERT INTO public.menu_menuitem VALUES (4, 'Productos', 'producto_list', '', 'fas fa-boxes', false, 1, 6, NULL, 136);
INSERT INTO public.menu_menuitem VALUES (47, 'Productos', 'producto_informe_list', '', '', false, 1, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (55, 'Depósitos', 'productodeposito_informe_list', '', '', false, 10, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (56, 'Familias', 'productofamilia_informe_list', '', '', false, 4, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (57, 'Marcas', 'productomarca_informe_list', '', '', false, 5, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (58, 'Modelos', 'productomodelo_informe_list', '', '', false, 6, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (59, 'CAIs', 'productocai_informe_list', '', '', false, 7, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (60, 'Estados', 'productoestado_informe_list', '', '', false, 8, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (45, 'Clientes', 'cliente_informe_list', '', '', false, 1, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (81, 'Saldos de Clientes', 'vlsaldosclientes_informe_list', '', '', false, 2, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (52, 'Números', '', '', '', false, 24, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (94, 'Totales por Provincia', 'vlivaventasprovincias_informe_list', '', '', false, 1, 0, NULL, 92);
INSERT INTO public.menu_menuitem VALUES (95, 'Totales para SITRIB', 'vlivaventassitrib_informe_list', '', '', false, 2, 0, NULL, 92);
INSERT INTO public.menu_menuitem VALUES (97, 'Vendedores - Solo Totales', 'vlpercepibvendedortotales_informe_list', '', '', false, 0, 0, NULL, 96);
INSERT INTO public.menu_menuitem VALUES (98, 'Vendedores - Detallado por Comprobantes', 'vlpercepibvendedordetallado_informe_list', '', '', false, 1, 0, NULL, 96);
INSERT INTO public.menu_menuitem VALUES (99, 'Sub Cuentas - Solo Totales', 'vlpercepibsubcuentatotales_informe_list', '', '', false, 2, 0, NULL, 96);
INSERT INTO public.menu_menuitem VALUES (100, 'Sub Cuentas - Detallado por Comprobantes', 'vlpercepibsubcuentadetallado_informe_list', '', '', false, 3, 0, NULL, 96);
INSERT INTO public.menu_menuitem VALUES (108, 'Listado de Stock por Sucursal', 'vlstocksucursal_informe_list', '', '', false, 0, 0, NULL, 141);
INSERT INTO public.menu_menuitem VALUES (109, 'Stock General por Sucursal', 'vlstockgeneralsucursal_informe_list', '', '', false, 1, 0, NULL, 141);
INSERT INTO public.menu_menuitem VALUES (110, 'Listado de Stock Único', 'vlstockunico_informe_list', '', '', false, 2, 0, NULL, 141);
INSERT INTO public.menu_menuitem VALUES (111, 'Reposición de Stock', 'vlreposicionstock_informe_list', '', '', false, 3, 0, NULL, 141);
INSERT INTO public.menu_menuitem VALUES (112, 'Actualizar Productos (Excel)', 'cargar_excel', 'proceso=actualizar', '', false, 0, 0, 1, 138);
INSERT INTO public.menu_menuitem VALUES (113, 'Agregar nuevos Productos (Excel)', 'cargar_excel', 'proceso=agregar', '', false, 1, 0, 1, 138);
INSERT INTO public.menu_menuitem VALUES (114, 'Estadísticas de Ventas', 'vlestadisticasventas_informe_list', '', '', false, 0, 0, 6, NULL);
INSERT INTO public.menu_menuitem VALUES (115, 'Estadísticas de Ventas Vendedores', 'vlestadisticasventasvendedor_informe_list', '', '', false, 1, 0, 6, NULL);
INSERT INTO public.menu_menuitem VALUES (116, 'Estadísticas de Ventas Vendedores Clientes', 'vlestadisticasventasvendedorcliente_informe_list', '', '', false, 2, 0, 6, NULL);
INSERT INTO public.menu_menuitem VALUES (117, 'Ventas de Productos Según Condición', 'vlestadisticasseguncondicion_informe_list', '', '', false, 3, 0, 6, NULL);
INSERT INTO public.menu_menuitem VALUES (118, 'Estadísticas de Ventas por Marca', 'vlestadisticasventasmarca_informe_list', '', '', false, 4, 0, 6, NULL);
INSERT INTO public.menu_menuitem VALUES (119, 'Estadísticas de Ventas por Marca-Vendedor', 'vlestadisticasventasmarcavendedor_informe_list', '', '', false, 5, 0, 6, NULL);
INSERT INTO public.menu_menuitem VALUES (120, 'Estadísticas de Clientes sin Movimiento', 'vlclienteultimaventa_informe_list', '', '', false, 6, 0, 6, NULL);
INSERT INTO public.menu_menuitem VALUES (121, 'Estadísticas de Ventas por Provincia', 'vlestadisticasventasprovincia_informe_list', '', '', false, 7, 0, 6, NULL);
INSERT INTO public.menu_menuitem VALUES (122, 'Comprobantes sin Estadísticas', 'vlventasinestadistica_informe_list', '', '', false, 8, 0, 6, NULL);
INSERT INTO public.menu_menuitem VALUES (124, 'Ventas por Comprobantes', 'vltabladinamicaventas_informe_list', '', '', false, 0, 0, 8, NULL);
INSERT INTO public.menu_menuitem VALUES (125, 'Detalle de Ventas por Productos', 'vltabladinamicadetalleventas_informe_list', '', '', false, 1, 0, 8, NULL);
INSERT INTO public.menu_menuitem VALUES (131, 'Movimiento Interno de Stock', 'vlmovimientointernostock_informe_list', '', 'fas fa-book-open', false, 5, 0, NULL, 141);
INSERT INTO public.menu_menuitem VALUES (135, 'Ventas', '', '', '', true, 0, 0, 1, NULL);
INSERT INTO public.menu_menuitem VALUES (136, 'Productos', '', '', '', true, 1, 0, 1, NULL);
INSERT INTO public.menu_menuitem VALUES (137, 'Compras', '', '', '', true, 2, 0, 1, NULL);
INSERT INTO public.menu_menuitem VALUES (138, 'Actualizaciones', '', '', '', true, 10, 0, 1, 136);
INSERT INTO public.menu_menuitem VALUES (140, 'Bancos', '', '', '', true, 5, 0, 4, NULL);
INSERT INTO public.menu_menuitem VALUES (141, 'Stock', '', '', '', true, 11, 0, 4, 53);
INSERT INTO public.menu_menuitem VALUES (142, 'Compras', '', '', '', true, 0, 0, 4, NULL);
INSERT INTO public.menu_menuitem VALUES (143, 'Detalle de Compras por Proveedor', 'vldetallecompraproveedor_informe_list', '', '', false, 2, 0, NULL, 142);
INSERT INTO public.menu_menuitem VALUES (144, 'Comprobantes Ingresados', 'vlcompraingresada_informe_list', '', '', false, 3, 0, NULL, 142);
INSERT INTO public.menu_menuitem VALUES (148, 'Comprobantes de Compra', 'comprobantecompra_informe_list', '', '', false, 0, 0, NULL, 142);
INSERT INTO public.menu_menuitem VALUES (149, 'Proveedores', 'proveedor_informe_list', '', '', false, 1, 0, NULL, 142);
INSERT INTO public.menu_menuitem VALUES (150, 'Caja', 'caja_list', '', '', false, 0, 0, 9, NULL);
INSERT INTO public.menu_menuitem VALUES (151, 'Actualizar Estados de Productos', 'actualizar_estados_productos', '', '', false, 8, 0, NULL, 136);
INSERT INTO public.menu_menuitem VALUES (152, 'Actualizar Mínimos por CAI', 'actualizar_minimo_cargar', '', '', false, 2, 0, NULL, 138);
INSERT INTO public.menu_menuitem VALUES (154, 'Movimientos de Caja', 'caja_detalle_list', '', '', false, 1, 0, 9, NULL);
INSERT INTO public.menu_menuitem VALUES (155, 'Caja', '', '', '', true, 6, 0, 4, NULL);
INSERT INTO public.menu_menuitem VALUES (166, 'Formas de Pago', 'forma_pago_list', '', '', false, 7, 0, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (167, 'Descuento Vendedor', 'descuento_vendedor_list', '', '', false, 2, 0, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (168, 'Descuento Revendedor', 'descuento_revendedor_list', '', '', false, 3, 0, NULL, 135);
INSERT INTO public.menu_menuitem VALUES (171, 'Actualizar Estados de Productos por CAI', 'actualizar_estados_cargar', '', '', false, 3, 0, NULL, 138);
INSERT INTO public.menu_menuitem VALUES (156, 'Planilla de Caja', 'planillacaja_informe_list', '', '', false, 1, 0, NULL, 155);
INSERT INTO public.menu_menuitem VALUES (145, 'Stock por Clientes en Depósitos', 'vlstockcliente_informe_list', '', '', false, 6, 0, NULL, 141);
INSERT INTO public.menu_menuitem VALUES (146, 'Stock en Depósitos de Clientes', 'vlstockdeposito_informe_list', '', '', false, 7, 0, NULL, 141);
INSERT INTO public.menu_menuitem VALUES (106, 'Lista de Precios', 'vllista_informe_list', '', '', false, 2, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (107, 'Lista de Precios a Revendedores', 'vllistarevendedor_informe_list', '', '', false, 3, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (153, 'Mínimos por CAI', 'vlproductominimo_informe_list', '', '', false, 11, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (175, 'Estados de Productos por CAI', 'caiestados_informe_list', '', '', false, 9, 0, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (169, 'Descuento Vendedor', 'descuentovendedor_informe_list', '', '', false, 7, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (170, 'Descuento Revendedor', 'descuentorevendedor_informe_list', '', '', false, 8, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (161, 'Arqueo de Caja', 'cajaarqueo_informe_list', '', '', false, 2, 0, NULL, 155);
INSERT INTO public.menu_menuitem VALUES (157, 'Egresos de Caja', 'egresoscaja_informe_list', '', '', false, 3, 0, NULL, 155);
INSERT INTO public.menu_menuitem VALUES (158, 'Detalle de Tarjetas Recibidas', 'tarjetarecibo_informe_list', '', '', false, 4, 0, NULL, 155);
INSERT INTO public.menu_menuitem VALUES (159, 'Detalle de Cupones por Fechas', 'cuponesfecha_informe_list', '', '', false, 5, 0, NULL, 155);
INSERT INTO public.menu_menuitem VALUES (160, 'Detalle de Cheques Recibidos', 'chequerecibo_informe_list', '', '', false, 6, 0, NULL, 155);
INSERT INTO public.menu_menuitem VALUES (163, 'Detalle de Cheques por Fecha', 'chequesfecha_informe_list', '', '', false, 7, 0, NULL, 155);
INSERT INTO public.menu_menuitem VALUES (162, 'Detalle de Comprobantes', 'detallecomprobantes_informe_list', '', '', false, 8, 0, NULL, 155);
INSERT INTO public.menu_menuitem VALUES (104, 'Resumen de Ventas I. Brutos Mercadolibre', 'vlventasresumenib_informe_list', '', '', false, 17, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (96, 'Percepciones por Vendedor', '', '', '', true, 19, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (101, 'Comisiones a Vendedores según Facturas', 'vlcomisionvendedor_informe_list', '', '', false, 20, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (102, 'Comisiones a Operarios', 'vlcomisionoperario_informe_list', '', '', false, 21, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (103, 'Diferencias de Precios en Facturación', 'vlpreciodiferente_informe_list', '', '', false, 23, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (180, 'Detalle de Depositos por Fecha', 'caja_deposito_fecha_informe_list', '', '', false, 9, 0, NULL, 155);
INSERT INTO public.menu_menuitem VALUES (176, 'Detalle de Depositos por Caja', 'caja_deposito_informe_list', '', '', false, 9, 0, NULL, 155);
INSERT INTO public.menu_menuitem VALUES (182, 'Validaciones', 'valida_list', '', '', false, 0, 0, 10, NULL);
INSERT INTO public.menu_menuitem VALUES (183, 'Connsultas de Precios', 'consulta_productos_stock', '', 'fas fa-boxes', false, 0, 9, NULL, 53);
INSERT INTO public.menu_menuitem VALUES (48, 'Vendedores', 'vendedor_informe_list', '', '', false, 6, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (84, 'Remitos por Cliente', 'vlremitosclientes_informe_list', '', '', false, 9, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (85, 'Totales de Remitos por Cliente', 'vltotalremitosclientes_informe_list', '', '', false, 10, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (86, 'Comprobantes de Ventas por Localidad', 'vlventacomprolocalidad_informe_list', '', '', false, 11, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (87, 'Ventas por Mostrador', 'vlventamostrador_informe_list', '', '', false, 12, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (88, 'Total de Ventas por Comprobantes', 'vlventacompro_informe_list', '', '', false, 13, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (89, 'Comprobantes Vencidos', 'vlcomprobantesvencidos_informe_list', '', '', false, 14, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (92, 'Libro I.V.A. Ventas', '', '', '', true, 18, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (90, 'Remitos Pendientes', 'vlremitospendientes_informe_list', '', '', false, 15, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (91, 'Remitos por Vendedor', 'vlremitosvendedor_informe_list', '', '', false, 16, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (61, 'Comprobantes Ventas', 'comprobanteventa_informe_list', '', '', false, 22, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (71, 'Operarios', 'operario_informe_list', '', '', false, 25, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (72, 'Medios de Pago', 'mediopago_informe_list', '', '', false, 26, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (73, 'Puntos de Venta', 'puntoventa_informe_list', '', '', false, 27, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (79, 'Marketing Origen', 'marketingorigen_informe_list', '', '', false, 28, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (181, 'Resumen Cuenta Corriente Vendedor', 'vlresumenctactevendedor_informe_list', '', '', false, 4, 0, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (83, 'Mercadería por Cliente', 'vlmercaderiaporcliente_informe_list', '', 'fas fa-info', false, 5, 8, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (184, 'Comprobantes por Clientes', 'consulta_facturas_cliente', '', 'fas fa-address-book', false, 0, 7, NULL, 80);
INSERT INTO public.menu_menuitem VALUES (185, 'Comprobantes por Clientes', 'consulta_facturas_cliente', '', '', false, 1, 0, 11, NULL);
INSERT INTO public.menu_menuitem VALUES (126, 'Tablas para Estadísticas', 'vltabladinamicaestadistica_informe_list', '', '', false, 3, 0, 8, NULL);
INSERT INTO public.menu_menuitem VALUES (187, 'Comprobantes Segun Remitos', 'buscar_remito', '', '', false, 3, 0, 11, NULL);
INSERT INTO public.menu_menuitem VALUES (186, 'Consultas de Precios', 'consulta_productos_stock', '', '', false, 2, 0, 11, NULL);
INSERT INTO public.menu_menuitem VALUES (188, 'Cambio de Precios por Porcentaje', 'actualizar_precios_productos', '', '', false, 5, 0, NULL, 138);
INSERT INTO public.menu_menuitem VALUES (147, 'Ficha de Seguimiento de Stock', 'vlfichaseguimientostock_informe_list', '', '', false, 4, 0, NULL, 141);


--
-- TOC entry 5395 (class 0 OID 0)
-- Dependencies: 297
-- Name: menu_menuitem_id_menu_item_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menu_menuitem_id_menu_item_seq', 188, true);


-- Completed on 2026-09-01 00:39:03

--
-- PostgreSQL database dump complete
--

\unrestrict WaCQvFmzv6wJ21PlyuxVXl8Ow0YuJr25K8TkZeeh0OGuhgq0DawDOLA1tv9g8UU


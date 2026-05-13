-- Script que agrega la factura para asignarla a los registros cuyo id_factura_cobrada_id sea null en detalle_recibo.
INSERT INTO factura (
    usuario, estacion, fcontrol, id_factura, id_orig, estatus_comprobante,
    jerarquia, compro, letra_comprobante, numero_comprobante, comprobante_remito,
    remito, id_comprobante_asociado, comprobante_asociado, numero_asociado,
    fecha_comprobante, cuit, nombre_factura, domicilio_factura, movil_factura,
    email_factura, condicion_comprobante, gravado, exento, iva, percep_ib,
    total, entrega, estado, marca, comision, fecha_pago, no_estadist, suc_imp,
    cae, cae_vto, observa_comprobante, stock_clie, promo, recibo_manual_auto,
    suma_comision_vendedor, productos_camiones, efectivo_recibo, compensa_factura,
    id_caja_id, id_cliente_id, id_comprobante_venta_id, id_deposito_id,
    id_marketing_origen_id, id_punto_venta_id, id_sucursal_id, id_user_id,
    id_valida_id, id_vendedor_id
) VALUES (
    NULL,      -- usuario
    NULL,      -- estacion
    NULL,      -- fcontrol
    1737462,   -- id_factura
    NULL,      -- id_orig
    TRUE,      -- estatus_comprobante ('t')
    NULL,      -- jerarquia
    'FF',      -- compro
    'A',       -- letra_comprobante
    111111111111,  -- numero_comprobante
    NULL,      -- comprobante_remito
    NULL,      -- remito
    NULL,      -- id_comprobante_asociado
    NULL,      -- comprobante_asociado
    NULL,      -- numero_asociado
    '2023-01-01',  -- fecha_comprobante
    NULL,      -- cuit
    NULL,      -- nombre_factura
    NULL,      -- domicilio_factura
    NULL,      -- movil_factura
    NULL,      -- email_factura
    1,         -- condicion_comprobante
    0.00,      -- gravado
    0.00,      -- exento
    0.00,      -- iva
    0.00,      -- percep_ib
    0.00,      -- total
    0.00,      -- entrega
    'C',       -- estado
    NULL,      -- marca
    NULL,      -- comision
    NULL,      -- fecha_pago
    FALSE,     -- no_estadist ('f')
    0,         -- suc_imp
    0,         -- cae
    NULL,      -- cae_vto
    NULL,      -- observa_comprobante
    FALSE,     -- stock_clie ('f')
    FALSE,     -- promo ('f')
    NULL,      -- recibo_manual_auto
    NULL,      -- suma_comision_vendedor
    NULL,      -- productos_camiones
    0.00,      -- efectivo_recibo
    0.00,      -- compensa_factura
    NULL,      -- id_caja_id ✅
    NULL,      -- id_cliente_id ✅ (CORRECTO: NULL)
    8,         -- id_comprobante_venta_id ✅ (CORRECTO: 8)
    1,         -- id_deposito_id
    1,         -- id_marketing_origen_id
    1,         -- id_punto_venta_id
    1,         -- id_sucursal_id
    1,         -- id_user_id
    NULL,      -- id_valida_id
    NULL       -- id_vendedor_id
);

-- Script para asignar la factura creada (id_factura=1) a los detalles de recibo sin id_factura_cobrada_id:
UPDATE detalle_recibo SET id_factura_cobrada_id = 1 WHERE id_factura_cobrada_id is null;
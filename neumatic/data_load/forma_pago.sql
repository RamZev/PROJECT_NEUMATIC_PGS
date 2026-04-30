BEGIN TRANSACTION;

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:00:26', 1, TRUE, 'EFECTIVO');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:00:36', 2, TRUE, 'CUENTA CORRIENTE');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:00:44', 3, TRUE, 'TARJETA CREDITO');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:00:53', 4, TRUE, 'TARJETA DEBITO');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:01:03', 5, TRUE, 'DEPOSITO');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:01:26', 6, TRUE, 'DOLARES');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:01:35', 7, TRUE, 'CHEQUES');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:01:44', 8, TRUE, 'RETENCIONES');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:01:55', 9, TRUE, 'COMPENSA. FACTURAS');

INSERT INTO forma_pago (usuario, estacion, fcontrol, id_forma_pago, estatus_forma_pago, descripcion_forma_pago) 
VALUES ('admin', 'ESTACION03', '2025-11-25 22:02:05', 10, TRUE, 'MERCADO PAGO');

COMMIT;
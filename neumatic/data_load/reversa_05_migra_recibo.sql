-- Eliminar registros y reiniciar el contador de IDs para cada tabla

DELETE FROM tarjeta_recibo;
DELETE FROM sqlite_sequence WHERE name = 'tarjeta_recibo';

DELETE FROM cheque_recibo;
DELETE FROM sqlite_sequence WHERE name = 'cheque_recibo';

DELETE FROM concepto_banco;
DELETE FROM sqlite_sequence WHERE name = 'concepto_banco';

DELETE FROM codigo_retencion;
DELETE FROM sqlite_sequence WHERE name = 'codigo_retencion';

DELETE FROM tarjeta;
DELETE FROM sqlite_sequence WHERE name = 'tarjeta';

DELETE FROM cuenta_banco;
DELETE FROM sqlite_sequence WHERE name = 'cuenta_banco';

DELETE FROM banco;
DELETE FROM sqlite_sequence WHERE name = 'banco';
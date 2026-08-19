* *********************************************************
* *
* * 06/02/24             LISTADOS.DBC             08:37:18
* *
* *********************************************************
* *
* * Descripción:
* * Este programa lo ha generado automáticamente GENDBC
* * Versión 2.26.67
* *
* *********************************************************


DisplayStatus([Creando base de datos...])
CLOSE DATA ALL
CREATE DATABASE 'LISTADOS.DBC'
DisplayStatus([Creando vista VLFACTPENDIENTE...])
MakeView_VLFACTPENDIENTE()
DisplayStatus([Creando vista VLRESUMENCLIENTE...])
MakeView_VLRESUMENCLIENTE()
DisplayStatus([Creando vista VLSALDOCLIENTES...])
MakeView_VLSALDOCLIENTES()
DisplayStatus([Creando vista VLDETALLEMERCA...])
MakeView_VLDETALLEMERCA()
DisplayStatus([Creando vista VLVENTACOMPRO...])
MakeView_VLVENTACOMPRO()
DisplayStatus([Creando vista VLREMITOSCLIENTES...])
MakeView_VLREMITOSCLIENTES()
DisplayStatus([Creando vista VLCOMISIONVENDEDOR...])
MakeView_VLCOMISIONVENDEDOR()
DisplayStatus([Creando vista VLRESUMENPROV...])
MakeView_VLRESUMENPROV()
DisplayStatus([Creando vista VLIVACOMPRAS...])
MakeView_VLIVACOMPRAS()
DisplayStatus([Creando vista VLCOMISIONVENDEDORREMITOS...])
MakeView_VLCOMISIONVENDEDORREMITOS()
DisplayStatus([Creando vista VLIVAVENTAS...])
MakeView_VLIVAVENTAS()
DisplayStatus([Creando vista VLVENTAIMPUTACION...])
MakeView_VLVENTAIMPUTACION()
DisplayStatus([Creando vista VLMOVSTOCK...])
MakeView_VLMOVSTOCK()
DisplayStatus([Creando vista VLSTOCK...])
MakeView_VLSTOCK()
DisplayStatus([Creando vista VLSTOCKVTA...])
MakeView_VLSTOCKVTA()
DisplayStatus([Creando vista VLSTOCKMOVSTOCK...])
MakeView_VLSTOCKMOVSTOCK()
DisplayStatus([Creando vista VLSTOCKCOM...])
MakeView_VLSTOCKCOM()
DisplayStatus([Creando vista VLVENTASMARCA...])
MakeView_VLVENTASMARCA()
DisplayStatus([Creando vista VLVENTASMARCAVENDEDOR...])
MakeView_VLVENTASMARCAVENDEDOR()
DisplayStatus([Creando vista VLFICHASTOVEN...])
MakeView_VLFICHASTOVEN()
DisplayStatus([Creando vista VLFICHASTOCOM...])
MakeView_VLFICHASTOCOM()
DisplayStatus([Creando vista VLFICHASTOMOV...])
MakeView_VLFICHASTOMOV()
DisplayStatus([Creando vista VLTOTALRTOSCLIENTES...])
MakeView_VLTOTALRTOSCLIENTES()
DisplayStatus([Creando vista VLDETALLECOMPRASPROV...])
MakeView_VLDETALLECOMPRASPROV()
DisplayStatus([Creando vista VLCOMISIONRECIBOS...])
MakeView_VLCOMISIONRECIBOS()
DisplayStatus([Creando vista VLVENTASPROV...])
MakeView_VLVENTASPROV()
DisplayStatus([Creando vista VLVENTASSITRIB...])
MakeView_VLVENTASSITRIB()
DisplayStatus([Creando vista VLVENTASRESUMENIB...])
MakeView_VLVENTASRESUMENIB()
DisplayStatus([Creando vista VLMARKSERVICIOS...])
MakeView_VLMARKSERVICIOS()
DisplayStatus([Creando vista VLVENTASSINESTADISTICAS...])
MakeView_VLVENTASSINESTADISTICAS()
DisplayStatus([Creando vista VLCOBRANZAVENDEDORDETALLADA...])
MakeView_VLCOBRANZAVENDEDORDETALLADA()
DisplayStatus([Creando vista VLCOMPRASIMPUTACION...])
MakeView_VLCOMPRASIMPUTACION()
DisplayStatus([Creando vista VLPRECIODIFERENTE...])
MakeView_VLPRECIODIFERENTE()
DisplayStatus([Creando vista VLVENTAMOSTRADOR...])
MakeView_VLVENTAMOSTRADOR()
DisplayStatus([Creando vista VLHORARIOS...])
MakeView_VLHORARIOS()
DisplayStatus([Creando vista VLMERCACABECERA...])
MakeView_VLMERCACABECERA()
DisplayStatus([Creando vista VLMERCADETALLE...])
MakeView_VLMERCADETALLE()
DisplayStatus([Creando vista VLCLIENTES...])
MakeView_VLCLIENTES()
DisplayStatus([Creando vista VLFACTPENDIENTESUC...])
MakeView_VLFACTPENDIENTESUC()
DisplayStatus([Creando vista VLSTOCKUNICO...])
MakeView_VLSTOCKUNICO()
DisplayStatus([Creando vista VLVENTACOMISIONVENDEDORDET...])
MakeView_VLVENTACOMISIONVENDEDORDET()
DisplayStatus([Creando vista VLIVAVENTASFULL...])
MakeView_VLIVAVENTASFULL()
DisplayStatus([Creando vista VLCOMISIONPLANILLA...])
MakeView_VLCOMISIONPLANILLA()
DisplayStatus([Creando vista VLCLIECUBCAMION...])
MakeView_VLCLIECUBCAMION()
DisplayStatus([Creando vista VLCOMISIONSERV...])
MakeView_VLCOMISIONSERV()
DisplayStatus([Creando vista VLPERCEPIBVENDEDOR...])
MakeView_VLPERCEPIBVENDEDOR()
DisplayStatus([Creando vista VLPERCEPIBVENDEDORDETALLADO...])
MakeView_VLPERCEPIBVENDEDORDETALLADO()
DisplayStatus([Creando vista VLPERCEPIBSUBCUENTA...])
MakeView_VLPERCEPIBSUBCUENTA()
DisplayStatus([Creando vista VLPERCEPIBSUBCUENTADETALLADO...])
MakeView_VLPERCEPIBSUBCUENTADETALLADO()
DisplayStatus([Creando vista VLVENTACOMPROREALIZADO...])
MakeView_VLVENTACOMPROREALIZADO()
DisplayStatus([Creando vista VLMOVSTOCKTOTAL...])
MakeView_VLMOVSTOCKTOTAL()
DisplayStatus([Creando vista VLPRECIOS...])
MakeView_VLPRECIOS()
DisplayStatus([Creando vista VLSTOCKVENTAS...])
MakeView_VLSTOCKVENTAS()
DisplayStatus([Creando vista VLSTOCKCLIENTES...])
MakeView_VLSTOCKCLIENTES()
DisplayStatus([Creando vista VLSTOCKDEPOSITO...])
MakeView_VLSTOCKDEPOSITO()
DisplayStatus([Creando vista VLSTOCKDEPOSITOSUC...])
MakeView_VLSTOCKDEPOSITOSUC()
DisplayStatus([Creando vista VLREMITOSPENDIENTES...])
MakeView_VLREMITOSPENDIENTES()
DisplayStatus([Creando vista VLCOMISIONVENDEDORCOBRO...])
MakeView_VLCOMISIONVENDEDORCOBRO()
DisplayStatus([Creando vista VLREMITOSVENDEDOR...])
MakeView_VLREMITOSVENDEDOR()
DisplayStatus([Creando vista VLSALDOSCLIENTES...])
MakeView_VLSALDOSCLIENTES()
DisplayStatus([Creando vista VLVENTACOMPROLOCALIDAD...])
MakeView_VLVENTACOMPROLOCALIDAD()
DisplayStatus([Creando vista VLWHATSAPPRECIBOS...])
MakeView_VLWHATSAPPRECIBOS()
DisplayStatus([Creando vista VLWHATSAPPFACTURAS...])
MakeView_VLWHATSAPPFACTURAS()
DisplayStatus([Creando vista VLSTOCKREPOSICION...])
MakeView_VLSTOCKREPOSICION()
DisplayStatus([Terminado.])

FUNCTION MakeView_VLFACTPENDIENTE
***************** Ver la configuración para VLFACTPENDIENTE ***************

CREATE SQL VIEW "VLFACTPENDIENTE" ; 
   AS SELECT Facturas.compro, Codven.nombre, Facturas.letra, Facturas.numero,  Facturas.fecha, Facturas.cliente, Clientes.nombre AS razonsocial,  Facturas.remito, Facturas.total*Codven.mult_cli AS total,  Facturas.entrega*Codven.mult_cli AS entrega,  (Facturas.total-Facturas.entrega)*Codven.mult_cli AS saldo,  Facturas.total*0 AS pagos, Facturas.marca, Facturas.noestadist FROM clientes,   facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.cliente BETWEEN ?nDesCli AND ?nHasCli   AND Facturas.cliente = Clientes.codigo   AND (Facturas.total <> Facturas.entrega   AND Codven.mult_cli <> 0) ORDER BY Facturas.cliente, Facturas.fecha

DBSetProp('VLFACTPENDIENTE', 'View', 'UpdateType', 1)
DBSetProp('VLFACTPENDIENTE', 'View', 'WhereType', 3)
DBSetProp('VLFACTPENDIENTE', 'View', 'FetchMemo', .T.)
DBSetProp('VLFACTPENDIENTE', 'View', 'SendUpdates', .F.)
DBSetProp('VLFACTPENDIENTE', 'View', 'UseMemoSize', 255)
DBSetProp('VLFACTPENDIENTE', 'View', 'FetchSize', 100)
DBSetProp('VLFACTPENDIENTE', 'View', 'MaxRecords', -1)
DBSetProp('VLFACTPENDIENTE', 'View', 'Tables', 'clientes,facturas')
DBSetProp('VLFACTPENDIENTE', 'View', 'Prepared', .F.)
DBSetProp('VLFACTPENDIENTE', 'View', 'CompareMemo', .T.)
DBSetProp('VLFACTPENDIENTE', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLFACTPENDIENTE', 'View', 'FetchSize', 100)
DBSetProp('VLFACTPENDIENTE', 'View', 'Comment', "")
DBSetProp('VLFACTPENDIENTE', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLFACTPENDIENTE', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLFACTPENDIENTE
* Props for the VLFACTPENDIENTE.compro field.
DBSetProp('VLFACTPENDIENTE.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTE.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLFACTPENDIENTE.compro', 'Field', 'DataType', "C(2)")
* Props for the VLFACTPENDIENTE.nombre field.
DBSetProp('VLFACTPENDIENTE.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTE.nombre', 'Field', 'UpdateName', 'codven.nombre')
DBSetProp('VLFACTPENDIENTE.nombre', 'Field', 'DataType', "C(20)")
* Props for the VLFACTPENDIENTE.letra field.
DBSetProp('VLFACTPENDIENTE.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTE.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLFACTPENDIENTE.letra', 'Field', 'DataType', "C(1)")
* Props for the VLFACTPENDIENTE.numero field.
DBSetProp('VLFACTPENDIENTE.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTE.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLFACTPENDIENTE.numero', 'Field', 'DataType', "N(12)")
* Props for the VLFACTPENDIENTE.fecha field.
DBSetProp('VLFACTPENDIENTE.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTE.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLFACTPENDIENTE.fecha', 'Field', 'DataType', "D")
* Props for the VLFACTPENDIENTE.cliente field.
DBSetProp('VLFACTPENDIENTE.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTE.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLFACTPENDIENTE.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLFACTPENDIENTE.razonsocial field.
DBSetProp('VLFACTPENDIENTE.razonsocial', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.razonsocial', 'Field', 'Updatable', .T.)
DBSetProp('VLFACTPENDIENTE.razonsocial', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLFACTPENDIENTE.razonsocial', 'Field', 'DataType', "C(30)")
* Props for the VLFACTPENDIENTE.remito field.
DBSetProp('VLFACTPENDIENTE.remito', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.remito', 'Field', 'Updatable', .T.)
DBSetProp('VLFACTPENDIENTE.remito', 'Field', 'UpdateName', 'facturas.remito')
DBSetProp('VLFACTPENDIENTE.remito', 'Field', 'DataType', "C(15)")
* Props for the VLFACTPENDIENTE.total field.
DBSetProp('VLFACTPENDIENTE.total', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.total', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTE.total', 'Field', 'UpdateName', 'Facturas.cliente*')
DBSetProp('VLFACTPENDIENTE.total', 'Field', 'DataType', "N(15,2)")
* Props for the VLFACTPENDIENTE.entrega field.
DBSetProp('VLFACTPENDIENTE.entrega', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.entrega', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTE.entrega', 'Field', 'UpdateName', 'Facturas.cliente**')
DBSetProp('VLFACTPENDIENTE.entrega', 'Field', 'DataType', "N(15,2)")
* Props for the VLFACTPENDIENTE.saldo field.
DBSetProp('VLFACTPENDIENTE.saldo', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.saldo', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTE.saldo', 'Field', 'UpdateName', 'Facturas.cliente***')
DBSetProp('VLFACTPENDIENTE.saldo', 'Field', 'DataType', "N(16,2)")
* Props for the VLFACTPENDIENTE.pagos field.
DBSetProp('VLFACTPENDIENTE.pagos', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.pagos', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTE.pagos', 'Field', 'UpdateName', 'Facturas.remito****')
DBSetProp('VLFACTPENDIENTE.pagos', 'Field', 'DataType', "N(14,2)")
* Props for the VLFACTPENDIENTE.marca field.
DBSetProp('VLFACTPENDIENTE.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.marca', 'Field', 'Updatable', .T.)
DBSetProp('VLFACTPENDIENTE.marca', 'Field', 'UpdateName', 'facturas.marca')
DBSetProp('VLFACTPENDIENTE.marca', 'Field', 'DataType', "C(1)")
* Props for the VLFACTPENDIENTE.noestadist field.
DBSetProp('VLFACTPENDIENTE.noestadist', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTE.noestadist', 'Field', 'Updatable', .T.)
DBSetProp('VLFACTPENDIENTE.noestadist', 'Field', 'UpdateName', 'facturas.noestadist')
DBSetProp('VLFACTPENDIENTE.noestadist', 'Field', 'DataType', "L")
ENDFUNC
 
FUNCTION MakeView_VLRESUMENCLIENTE
***************** Ver la configuración para VLRESUMENCLIENTE ***************

CREATE SQL VIEW "VLRESUMENCLIENTE" ; 
   AS SELECT Facturas.compro, Codven.nombre, Facturas.letra, Facturas.numero,  Facturas.fecha, Facturas.remito, Facturas.cliente, Facturas.condicion,  Facturas.total*Codven.mult_cli AS total,  (Facturas.total-Facturas.entrega)*Codven.mult_cli AS saldo,  Facturas.marca, Facturas.noestadist FROM  facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.cliente BETWEEN ?nDesCli AND ?nHasCli   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Facturas.condicion BETWEEN ?nDesCon AND ?nHasCon   AND Codven.mult_cli <> 0 ORDER BY Facturas.cliente, Facturas.fecha

DBSetProp('VLRESUMENCLIENTE', 'View', 'UpdateType', 1)
DBSetProp('VLRESUMENCLIENTE', 'View', 'WhereType', 3)
DBSetProp('VLRESUMENCLIENTE', 'View', 'FetchMemo', .T.)
DBSetProp('VLRESUMENCLIENTE', 'View', 'SendUpdates', .F.)
DBSetProp('VLRESUMENCLIENTE', 'View', 'UseMemoSize', 255)
DBSetProp('VLRESUMENCLIENTE', 'View', 'FetchSize', 100)
DBSetProp('VLRESUMENCLIENTE', 'View', 'MaxRecords', -1)
DBSetProp('VLRESUMENCLIENTE', 'View', 'Tables', 'facturas')
DBSetProp('VLRESUMENCLIENTE', 'View', 'Prepared', .F.)
DBSetProp('VLRESUMENCLIENTE', 'View', 'CompareMemo', .T.)
DBSetProp('VLRESUMENCLIENTE', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLRESUMENCLIENTE', 'View', 'FetchSize', 100)
DBSetProp('VLRESUMENCLIENTE', 'View', 'Comment', "")
DBSetProp('VLRESUMENCLIENTE', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLRESUMENCLIENTE', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLRESUMENCLIENTE
* Props for the VLRESUMENCLIENTE.compro field.
DBSetProp('VLRESUMENCLIENTE.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENCLIENTE.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLRESUMENCLIENTE.compro', 'Field', 'DataType', "C(2)")
* Props for the VLRESUMENCLIENTE.nombre field.
DBSetProp('VLRESUMENCLIENTE.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENCLIENTE.nombre', 'Field', 'UpdateName', 'codven.nombre')
DBSetProp('VLRESUMENCLIENTE.nombre', 'Field', 'DataType', "C(20)")
* Props for the VLRESUMENCLIENTE.letra field.
DBSetProp('VLRESUMENCLIENTE.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENCLIENTE.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLRESUMENCLIENTE.letra', 'Field', 'DataType', "C(1)")
* Props for the VLRESUMENCLIENTE.numero field.
DBSetProp('VLRESUMENCLIENTE.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENCLIENTE.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLRESUMENCLIENTE.numero', 'Field', 'DataType', "N(12)")
* Props for the VLRESUMENCLIENTE.fecha field.
DBSetProp('VLRESUMENCLIENTE.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENCLIENTE.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLRESUMENCLIENTE.fecha', 'Field', 'DataType', "D")
* Props for the VLRESUMENCLIENTE.remito field.
DBSetProp('VLRESUMENCLIENTE.remito', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.remito', 'Field', 'Updatable', .T.)
DBSetProp('VLRESUMENCLIENTE.remito', 'Field', 'UpdateName', 'facturas.remito')
DBSetProp('VLRESUMENCLIENTE.remito', 'Field', 'DataType', "C(15)")
* Props for the VLRESUMENCLIENTE.cliente field.
DBSetProp('VLRESUMENCLIENTE.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENCLIENTE.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLRESUMENCLIENTE.cliente', 'Field', 'DataType', "N(5)")
* Props for the VLRESUMENCLIENTE.condicion field.
DBSetProp('VLRESUMENCLIENTE.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.condicion', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENCLIENTE.condicion', 'Field', 'UpdateName', 'facturas.condicion')
DBSetProp('VLRESUMENCLIENTE.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLRESUMENCLIENTE.total field.
DBSetProp('VLRESUMENCLIENTE.total', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.total', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENCLIENTE.total', 'Field', 'UpdateName', 'Facturas.condicion*')
DBSetProp('VLRESUMENCLIENTE.total', 'Field', 'DataType', "N(15,2)")
* Props for the VLRESUMENCLIENTE.saldo field.
DBSetProp('VLRESUMENCLIENTE.saldo', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.saldo', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENCLIENTE.saldo', 'Field', 'UpdateName', 'Facturas.condicion**')
DBSetProp('VLRESUMENCLIENTE.saldo', 'Field', 'DataType', "N(16,2)")
* Props for the VLRESUMENCLIENTE.marca field.
DBSetProp('VLRESUMENCLIENTE.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.marca', 'Field', 'Updatable', .T.)
DBSetProp('VLRESUMENCLIENTE.marca', 'Field', 'UpdateName', 'facturas.marca')
DBSetProp('VLRESUMENCLIENTE.marca', 'Field', 'DataType', "C(1)")
* Props for the VLRESUMENCLIENTE.noestadist field.
DBSetProp('VLRESUMENCLIENTE.noestadist', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENCLIENTE.noestadist', 'Field', 'Updatable', .T.)
DBSetProp('VLRESUMENCLIENTE.noestadist', 'Field', 'UpdateName', 'facturas.noestadist')
DBSetProp('VLRESUMENCLIENTE.noestadist', 'Field', 'DataType', "L")
ENDFUNC
 
FUNCTION MakeView_VLSALDOCLIENTES
***************** Ver la configuración para VLSALDOCLIENTES ***************

CREATE SQL VIEW "VLSALDOCLIENTES" ; 
   AS SELECT Facturas.cliente,  SUM(Facturas.total* Codven.mult_cli) AS saldo FROM  facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.condicion = 2   AND Facturas.fecha < ?dFecha GROUP BY Facturas.cliente ORDER BY Facturas.cliente

DBSetProp('VLSALDOCLIENTES', 'View', 'UpdateType', 1)
DBSetProp('VLSALDOCLIENTES', 'View', 'WhereType', 3)
DBSetProp('VLSALDOCLIENTES', 'View', 'FetchMemo', .T.)
DBSetProp('VLSALDOCLIENTES', 'View', 'SendUpdates', .F.)
DBSetProp('VLSALDOCLIENTES', 'View', 'UseMemoSize', 255)
DBSetProp('VLSALDOCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLSALDOCLIENTES', 'View', 'MaxRecords', -1)
DBSetProp('VLSALDOCLIENTES', 'View', 'Tables', '')
DBSetProp('VLSALDOCLIENTES', 'View', 'Prepared', .F.)
DBSetProp('VLSALDOCLIENTES', 'View', 'CompareMemo', .T.)
DBSetProp('VLSALDOCLIENTES', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSALDOCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLSALDOCLIENTES', 'View', 'Comment', "")
DBSetProp('VLSALDOCLIENTES', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSALDOCLIENTES', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSALDOCLIENTES
* Props for the VLSALDOCLIENTES.cliente field.
DBSetProp('VLSALDOCLIENTES.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOCLIENTES.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLSALDOCLIENTES.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLSALDOCLIENTES.cliente', 'Field', 'DataType', "N(4)")
* Props for the VLSALDOCLIENTES.saldo field.
DBSetProp('VLSALDOCLIENTES.saldo', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOCLIENTES.saldo', 'Field', 'Updatable', .F.)
DBSetProp('VLSALDOCLIENTES.saldo', 'Field', 'UpdateName', '')
DBSetProp('VLSALDOCLIENTES.saldo', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLDETALLEMERCA
***************** Ver la configuración para VLDETALLEMERCA ***************

CREATE SQL VIEW "VLDETALLEMERCA" ; 
   AS SELECT Detven.compro, Detven.letra, Detven.numero, Facturas.fecha,  Facturas.cliente, Detven.codigo, Lista.medida, Lista.nombre,  Marcas.nombre AS marca, Detven.cantidad, Detven.precio, Detven.descuento,  Detven.total, Facturas.noestadist FROM marcas, facturas,   detven INNER JOIN lista    ON  Detven.codigo = Lista.codigo WHERE Lista.marca = Marcas.codigo   AND Detven.compro = Facturas.compro   AND Detven.letra = Facturas.letra   AND Detven.numero = Facturas.numero   AND (Facturas.cliente = ?nCliente   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta) ORDER BY Facturas.fecha, Detven.numero

DBSetProp('VLDETALLEMERCA', 'View', 'UpdateType', 1)
DBSetProp('VLDETALLEMERCA', 'View', 'WhereType', 3)
DBSetProp('VLDETALLEMERCA', 'View', 'FetchMemo', .T.)
DBSetProp('VLDETALLEMERCA', 'View', 'SendUpdates', .F.)
DBSetProp('VLDETALLEMERCA', 'View', 'UseMemoSize', 255)
DBSetProp('VLDETALLEMERCA', 'View', 'FetchSize', 100)
DBSetProp('VLDETALLEMERCA', 'View', 'MaxRecords', -1)
DBSetProp('VLDETALLEMERCA', 'View', 'Tables', 'facturas')
DBSetProp('VLDETALLEMERCA', 'View', 'Prepared', .F.)
DBSetProp('VLDETALLEMERCA', 'View', 'CompareMemo', .T.)
DBSetProp('VLDETALLEMERCA', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLDETALLEMERCA', 'View', 'FetchSize', 100)
DBSetProp('VLDETALLEMERCA', 'View', 'Comment', "")
DBSetProp('VLDETALLEMERCA', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLDETALLEMERCA', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLDETALLEMERCA
* Props for the VLDETALLEMERCA.compro field.
DBSetProp('VLDETALLEMERCA.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLDETALLEMERCA.compro', 'Field', 'DataType', "C(2)")
* Props for the VLDETALLEMERCA.letra field.
DBSetProp('VLDETALLEMERCA.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLDETALLEMERCA.letra', 'Field', 'DataType', "C(1)")
* Props for the VLDETALLEMERCA.numero field.
DBSetProp('VLDETALLEMERCA.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLDETALLEMERCA.numero', 'Field', 'DataType', "N(12)")
* Props for the VLDETALLEMERCA.fecha field.
DBSetProp('VLDETALLEMERCA.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLDETALLEMERCA.fecha', 'Field', 'DataType', "D")
* Props for the VLDETALLEMERCA.cliente field.
DBSetProp('VLDETALLEMERCA.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLDETALLEMERCA.cliente', 'Field', 'DataType', "N(5)")
* Props for the VLDETALLEMERCA.codigo field.
DBSetProp('VLDETALLEMERCA.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLDETALLEMERCA.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLDETALLEMERCA.medida field.
DBSetProp('VLDETALLEMERCA.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.medida', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLDETALLEMERCA.medida', 'Field', 'DataType', "C(10)")
* Props for the VLDETALLEMERCA.nombre field.
DBSetProp('VLDETALLEMERCA.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLDETALLEMERCA.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLDETALLEMERCA.marca field.
DBSetProp('VLDETALLEMERCA.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.marca', 'Field', 'UpdateName', 'marcas.nombre')
DBSetProp('VLDETALLEMERCA.marca', 'Field', 'DataType', "C(20)")
* Props for the VLDETALLEMERCA.cantidad field.
DBSetProp('VLDETALLEMERCA.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.cantidad', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLDETALLEMERCA.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLDETALLEMERCA.precio field.
DBSetProp('VLDETALLEMERCA.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.precio', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLDETALLEMERCA.precio', 'Field', 'DataType', "N(10,2)")
* Props for the VLDETALLEMERCA.descuento field.
DBSetProp('VLDETALLEMERCA.descuento', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.descuento', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.descuento', 'Field', 'UpdateName', 'detven.descuento')
DBSetProp('VLDETALLEMERCA.descuento', 'Field', 'DataType', "N(6,2)")
* Props for the VLDETALLEMERCA.total field.
DBSetProp('VLDETALLEMERCA.total', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.total', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLEMERCA.total', 'Field', 'UpdateName', 'detven.total')
DBSetProp('VLDETALLEMERCA.total', 'Field', 'DataType', "N(10,2)")
* Props for the VLDETALLEMERCA.noestadist field.
DBSetProp('VLDETALLEMERCA.noestadist', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLEMERCA.noestadist', 'Field', 'Updatable', .T.)
DBSetProp('VLDETALLEMERCA.noestadist', 'Field', 'UpdateName', 'facturas.noestadist')
DBSetProp('VLDETALLEMERCA.noestadist', 'Field', 'DataType', "L")
ENDFUNC
 
FUNCTION MakeView_VLVENTACOMPRO
***************** Ver la configuración para VLVENTACOMPRO ***************

CREATE SQL VIEW "VLVENTACOMPRO" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.fecha,  Facturas.condicion, Facturas.cliente, Clientes.nombre,  Facturas.total*Codven.mult_ven AS total,  Facturas.gravado* Codven.mult_ven AS Gravado,  Facturas.iva* Codven.mult_ven AS IVA,  Facturas.percepib* Codven.mult_ven AS PercepIB, Facturas.sucursal FROM clientes,   facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.cliente = Clientes.codigo   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta ORDER BY Facturas.compro, Facturas.letra, Facturas.numero

DBSetProp('VLVENTACOMPRO', 'View', 'UpdateType', 1)
DBSetProp('VLVENTACOMPRO', 'View', 'WhereType', 3)
DBSetProp('VLVENTACOMPRO', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTACOMPRO', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTACOMPRO', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTACOMPRO', 'View', 'FetchSize', 100)
DBSetProp('VLVENTACOMPRO', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTACOMPRO', 'View', 'Tables', 'facturas')
DBSetProp('VLVENTACOMPRO', 'View', 'Prepared', .F.)
DBSetProp('VLVENTACOMPRO', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTACOMPRO', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTACOMPRO', 'View', 'FetchSize', 100)
DBSetProp('VLVENTACOMPRO', 'View', 'Comment', "")
DBSetProp('VLVENTACOMPRO', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTACOMPRO', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTACOMPRO
* Props for the VLVENTACOMPRO.compro field.
DBSetProp('VLVENTACOMPRO.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLVENTACOMPRO.compro', 'Field', 'DataType', "C(2)")
* Props for the VLVENTACOMPRO.letra field.
DBSetProp('VLVENTACOMPRO.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLVENTACOMPRO.letra', 'Field', 'DataType', "C(1)")
* Props for the VLVENTACOMPRO.numero field.
DBSetProp('VLVENTACOMPRO.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLVENTACOMPRO.numero', 'Field', 'DataType', "N(12)")
* Props for the VLVENTACOMPRO.fecha field.
DBSetProp('VLVENTACOMPRO.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTACOMPRO.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTACOMPRO.condicion field.
DBSetProp('VLVENTACOMPRO.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.condicion', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.condicion', 'Field', 'UpdateName', 'facturas.condicion')
DBSetProp('VLVENTACOMPRO.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLVENTACOMPRO.cliente field.
DBSetProp('VLVENTACOMPRO.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLVENTACOMPRO.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLVENTACOMPRO.nombre field.
DBSetProp('VLVENTACOMPRO.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLVENTACOMPRO.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLVENTACOMPRO.total field.
DBSetProp('VLVENTACOMPRO.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.total', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.total', 'Field', 'UpdateName', '')
DBSetProp('VLVENTACOMPRO.total', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTACOMPRO.gravado field.
DBSetProp('VLVENTACOMPRO.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.gravado', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.gravado', 'Field', 'UpdateName', '')
DBSetProp('VLVENTACOMPRO.gravado', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTACOMPRO.iva field.
DBSetProp('VLVENTACOMPRO.iva', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.iva', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.iva', 'Field', 'UpdateName', '')
DBSetProp('VLVENTACOMPRO.iva', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTACOMPRO.percepib field.
DBSetProp('VLVENTACOMPRO.percepib', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.percepib', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPRO.percepib', 'Field', 'UpdateName', '')
DBSetProp('VLVENTACOMPRO.percepib', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTACOMPRO.sucursal field.
DBSetProp('VLVENTACOMPRO.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPRO.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPRO.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLVENTACOMPRO.sucursal', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLREMITOSCLIENTES
***************** Ver la configuración para VLREMITOSCLIENTES ***************

CREATE SQL VIEW "VLREMITOSCLIENTES" ; 
   AS SELECT Detven.compro, Detven.letra, Detven.numero, Facturas.fecha,  Facturas.cliente, Lista.nombre, Lista.medida, Detven.cantidad,  Detven.precio, Detven.descuento,  Detven.total* Codven.mult_sto*-1 AS total FROM facturas, codven,   detven INNER JOIN lista    ON  Detven.codigo = Lista.codigo WHERE Detven.compro = Facturas.compro   AND Detven.letra = Facturas.letra   AND Detven.numero = Facturas.numero   AND Detven.compro = Codven.compro   AND (Detven.compro BETWEEN "RD" AND "RT"   AND Facturas.cliente = ?nCliente   AND Codven.mult_ven = 0) ORDER BY Facturas.fecha, Detven.numero

DBSetProp('VLREMITOSCLIENTES', 'View', 'UpdateType', 1)
DBSetProp('VLREMITOSCLIENTES', 'View', 'WhereType', 3)
DBSetProp('VLREMITOSCLIENTES', 'View', 'FetchMemo', .T.)
DBSetProp('VLREMITOSCLIENTES', 'View', 'SendUpdates', .F.)
DBSetProp('VLREMITOSCLIENTES', 'View', 'UseMemoSize', 255)
DBSetProp('VLREMITOSCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLREMITOSCLIENTES', 'View', 'MaxRecords', -1)
DBSetProp('VLREMITOSCLIENTES', 'View', 'Tables', '')
DBSetProp('VLREMITOSCLIENTES', 'View', 'Prepared', .F.)
DBSetProp('VLREMITOSCLIENTES', 'View', 'CompareMemo', .T.)
DBSetProp('VLREMITOSCLIENTES', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLREMITOSCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLREMITOSCLIENTES', 'View', 'Comment', "")
DBSetProp('VLREMITOSCLIENTES', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLREMITOSCLIENTES', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLREMITOSCLIENTES
* Props for the VLREMITOSCLIENTES.compro field.
DBSetProp('VLREMITOSCLIENTES.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLREMITOSCLIENTES.compro', 'Field', 'DataType', "C(2)")
* Props for the VLREMITOSCLIENTES.letra field.
DBSetProp('VLREMITOSCLIENTES.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLREMITOSCLIENTES.letra', 'Field', 'DataType', "C(1)")
* Props for the VLREMITOSCLIENTES.numero field.
DBSetProp('VLREMITOSCLIENTES.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLREMITOSCLIENTES.numero', 'Field', 'DataType', "N(12)")
* Props for the VLREMITOSCLIENTES.fecha field.
DBSetProp('VLREMITOSCLIENTES.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLREMITOSCLIENTES.fecha', 'Field', 'DataType', "D")
* Props for the VLREMITOSCLIENTES.cliente field.
DBSetProp('VLREMITOSCLIENTES.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLREMITOSCLIENTES.cliente', 'Field', 'DataType', "N(4)")
* Props for the VLREMITOSCLIENTES.nombre field.
DBSetProp('VLREMITOSCLIENTES.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLREMITOSCLIENTES.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLREMITOSCLIENTES.medida field.
DBSetProp('VLREMITOSCLIENTES.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.medida', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLREMITOSCLIENTES.medida', 'Field', 'DataType', "C(10)")
* Props for the VLREMITOSCLIENTES.cantidad field.
DBSetProp('VLREMITOSCLIENTES.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.cantidad', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLREMITOSCLIENTES.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLREMITOSCLIENTES.precio field.
DBSetProp('VLREMITOSCLIENTES.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.precio', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLREMITOSCLIENTES.precio', 'Field', 'DataType', "N(10,2)")
* Props for the VLREMITOSCLIENTES.descuento field.
DBSetProp('VLREMITOSCLIENTES.descuento', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.descuento', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.descuento', 'Field', 'UpdateName', 'detven.descuento')
DBSetProp('VLREMITOSCLIENTES.descuento', 'Field', 'DataType', "N(6,2)")
* Props for the VLREMITOSCLIENTES.total field.
DBSetProp('VLREMITOSCLIENTES.total', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSCLIENTES.total', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSCLIENTES.total', 'Field', 'UpdateName', '')
DBSetProp('VLREMITOSCLIENTES.total', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLCOMISIONVENDEDOR
***************** Ver la configuración para VLCOMISIONVENDEDOR ***************

CREATE SQL VIEW "VLCOMISIONVENDEDOR" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.fecha,  Facturas.condicion, Facturas.cliente, Clientes.nombre,  (gravado+exento)*Codven.mult_com AS gravado, Facturas.total,  Facturas.comision, Facturas.total*0 AS impComision FROM clientes,   facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.cliente = Clientes.codigo   AND (Clientes.vendedor = ?nVendedor   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Codven.mult_com <> 0) ORDER BY Facturas.fecha

DBSetProp('VLCOMISIONVENDEDOR', 'View', 'UpdateType', 1)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'WhereType', 3)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'FetchMemo', .T.)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'SendUpdates', .F.)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'UseMemoSize', 255)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'MaxRecords', -1)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'Tables', 'facturas,clientes')
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'Prepared', .F.)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'CompareMemo', .T.)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'Comment', "")
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLCOMISIONVENDEDOR', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLCOMISIONVENDEDOR
* Props for the VLCOMISIONVENDEDOR.compro field.
DBSetProp('VLCOMISIONVENDEDOR.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDOR.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLCOMISIONVENDEDOR.compro', 'Field', 'DataType', "C(2)")
* Props for the VLCOMISIONVENDEDOR.letra field.
DBSetProp('VLCOMISIONVENDEDOR.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDOR.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLCOMISIONVENDEDOR.letra', 'Field', 'DataType', "C(1)")
* Props for the VLCOMISIONVENDEDOR.numero field.
DBSetProp('VLCOMISIONVENDEDOR.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDOR.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLCOMISIONVENDEDOR.numero', 'Field', 'DataType', "N(12)")
* Props for the VLCOMISIONVENDEDOR.fecha field.
DBSetProp('VLCOMISIONVENDEDOR.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDOR.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLCOMISIONVENDEDOR.fecha', 'Field', 'DataType', "D")
* Props for the VLCOMISIONVENDEDOR.condicion field.
DBSetProp('VLCOMISIONVENDEDOR.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.condicion', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDOR.condicion', 'Field', 'UpdateName', 'facturas.condicion')
DBSetProp('VLCOMISIONVENDEDOR.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLCOMISIONVENDEDOR.cliente field.
DBSetProp('VLCOMISIONVENDEDOR.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDOR.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLCOMISIONVENDEDOR.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLCOMISIONVENDEDOR.nombre field.
DBSetProp('VLCOMISIONVENDEDOR.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDOR.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLCOMISIONVENDEDOR.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLCOMISIONVENDEDOR.gravado field.
DBSetProp('VLCOMISIONVENDEDOR.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.gravado', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDOR.gravado', 'Field', 'UpdateName', 'Clientes.nombre*')
DBSetProp('VLCOMISIONVENDEDOR.gravado', 'Field', 'DataType', "N(16,2)")
* Props for the VLCOMISIONVENDEDOR.total field.
DBSetProp('VLCOMISIONVENDEDOR.total', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.total', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDOR.total', 'Field', 'UpdateName', 'facturas.total')
DBSetProp('VLCOMISIONVENDEDOR.total', 'Field', 'DataType', "N(12,2)")
* Props for the VLCOMISIONVENDEDOR.comision field.
DBSetProp('VLCOMISIONVENDEDOR.comision', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.comision', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDOR.comision', 'Field', 'UpdateName', 'facturas.comision')
DBSetProp('VLCOMISIONVENDEDOR.comision', 'Field', 'DataType', "C(1)")
* Props for the VLCOMISIONVENDEDOR.impcomision field.
DBSetProp('VLCOMISIONVENDEDOR.impcomision', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDOR.impcomision', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDOR.impcomision', 'Field', 'UpdateName', '')
DBSetProp('VLCOMISIONVENDEDOR.impcomision', 'Field', 'DataType', "N(14,2)")
ENDFUNC
 
FUNCTION MakeView_VLRESUMENPROV
***************** Ver la configuración para VLRESUMENPROV ***************

CREATE SQL VIEW "VLRESUMENPROV" ; 
   AS SELECT Compras.compro, Codcom.nombre, Compras.letra, Compras.numero,  Compras.fecha, Compras.vencimient, Compras.proveedor, Compras.condicion,  Compras.total*Codcom.mult_pro AS total, Compras.entrega,  Compras.estado FROM  compras INNER JOIN codcom    ON  Compras.compro = Codcom.codigo WHERE Compras.proveedor = ?nProveedor   AND Compras.fecha BETWEEN ?dDesde AND ?dHasta   AND Compras.condicion = 2 ORDER BY Compras.fecha, Compras.compro, Compras.numero

DBSetProp('VLRESUMENPROV', 'View', 'UpdateType', 1)
DBSetProp('VLRESUMENPROV', 'View', 'WhereType', 3)
DBSetProp('VLRESUMENPROV', 'View', 'FetchMemo', .T.)
DBSetProp('VLRESUMENPROV', 'View', 'SendUpdates', .F.)
DBSetProp('VLRESUMENPROV', 'View', 'UseMemoSize', 255)
DBSetProp('VLRESUMENPROV', 'View', 'FetchSize', 100)
DBSetProp('VLRESUMENPROV', 'View', 'MaxRecords', -1)
DBSetProp('VLRESUMENPROV', 'View', 'Tables', '')
DBSetProp('VLRESUMENPROV', 'View', 'Prepared', .F.)
DBSetProp('VLRESUMENPROV', 'View', 'CompareMemo', .T.)
DBSetProp('VLRESUMENPROV', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLRESUMENPROV', 'View', 'FetchSize', 100)
DBSetProp('VLRESUMENPROV', 'View', 'Comment', "")
DBSetProp('VLRESUMENPROV', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLRESUMENPROV', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLRESUMENPROV
* Props for the VLRESUMENPROV.compro field.
DBSetProp('VLRESUMENPROV.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.compro', 'Field', 'UpdateName', 'compras.compro')
DBSetProp('VLRESUMENPROV.compro', 'Field', 'DataType', "C(2)")
* Props for the VLRESUMENPROV.nombre field.
DBSetProp('VLRESUMENPROV.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.nombre', 'Field', 'UpdateName', 'codcom.nombre')
DBSetProp('VLRESUMENPROV.nombre', 'Field', 'DataType', "C(20)")
* Props for the VLRESUMENPROV.letra field.
DBSetProp('VLRESUMENPROV.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.letra', 'Field', 'UpdateName', 'compras.letra')
DBSetProp('VLRESUMENPROV.letra', 'Field', 'DataType', "C(1)")
* Props for the VLRESUMENPROV.numero field.
DBSetProp('VLRESUMENPROV.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.numero', 'Field', 'UpdateName', 'compras.numero')
DBSetProp('VLRESUMENPROV.numero', 'Field', 'DataType', "N(12)")
* Props for the VLRESUMENPROV.fecha field.
DBSetProp('VLRESUMENPROV.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.fecha', 'Field', 'UpdateName', 'compras.fecha')
DBSetProp('VLRESUMENPROV.fecha', 'Field', 'DataType', "D")
* Props for the VLRESUMENPROV.vencimient field.
DBSetProp('VLRESUMENPROV.vencimient', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.vencimient', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.vencimient', 'Field', 'UpdateName', 'compras.vencimient')
DBSetProp('VLRESUMENPROV.vencimient', 'Field', 'DataType', "D")
* Props for the VLRESUMENPROV.proveedor field.
DBSetProp('VLRESUMENPROV.proveedor', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.proveedor', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.proveedor', 'Field', 'UpdateName', 'compras.proveedor')
DBSetProp('VLRESUMENPROV.proveedor', 'Field', 'DataType', "N(4)")
* Props for the VLRESUMENPROV.condicion field.
DBSetProp('VLRESUMENPROV.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.condicion', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.condicion', 'Field', 'UpdateName', 'compras.condicion')
DBSetProp('VLRESUMENPROV.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLRESUMENPROV.total field.
DBSetProp('VLRESUMENPROV.total', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.total', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.total', 'Field', 'UpdateName', 'Compras.condicion*')
DBSetProp('VLRESUMENPROV.total', 'Field', 'DataType', "N(13,2)")
* Props for the VLRESUMENPROV.entrega field.
DBSetProp('VLRESUMENPROV.entrega', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.entrega', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.entrega', 'Field', 'UpdateName', 'compras.entrega')
DBSetProp('VLRESUMENPROV.entrega', 'Field', 'DataType', "N(10,2)")
* Props for the VLRESUMENPROV.estado field.
DBSetProp('VLRESUMENPROV.estado', 'Field', 'KeyField', .F.)
DBSetProp('VLRESUMENPROV.estado', 'Field', 'Updatable', .F.)
DBSetProp('VLRESUMENPROV.estado', 'Field', 'UpdateName', 'compras.estado')
DBSetProp('VLRESUMENPROV.estado', 'Field', 'DataType', "C(1)")
ENDFUNC
 
FUNCTION MakeView_VLIVACOMPRAS
***************** Ver la configuración para VLIVACOMPRAS ***************

CREATE SQL VIEW "VLIVACOMPRAS" ; 
   AS SELECT Compras.compro, Compras.letra, Compras.numero, Compras.fecha,  Provedor.nombre, Provedor.sitiva, Provedor.cuit,  Compras.gravado*Codcom.mult_com AS gravado,  Compras.nogravado*Codcom.mult_com AS nogravado,  Compras.monotrib*Codcom.mult_com AS monotrib,  Compras.iva*Codcom.mult_com AS iva,  Compras.percepcion* Codcom.mult_com AS percepcion,  Compras.total*Codcom.mult_com AS total FROM provedor,   compras INNER JOIN codcom    ON  Compras.compro = Codcom.codigo WHERE Compras.proveedor = Provedor.codigo   AND (MONTH(Compras.fecha) = ?nMes   AND YEAR(Compras.fecha) = ?nAnio   AND Codcom.libroiva = .T.) ORDER BY Compras.fecha

DBSetProp('VLIVACOMPRAS', 'View', 'UpdateType', 1)
DBSetProp('VLIVACOMPRAS', 'View', 'WhereType', 3)
DBSetProp('VLIVACOMPRAS', 'View', 'FetchMemo', .T.)
DBSetProp('VLIVACOMPRAS', 'View', 'SendUpdates', .F.)
DBSetProp('VLIVACOMPRAS', 'View', 'UseMemoSize', 255)
DBSetProp('VLIVACOMPRAS', 'View', 'FetchSize', 100)
DBSetProp('VLIVACOMPRAS', 'View', 'MaxRecords', -1)
DBSetProp('VLIVACOMPRAS', 'View', 'Tables', '')
DBSetProp('VLIVACOMPRAS', 'View', 'Prepared', .F.)
DBSetProp('VLIVACOMPRAS', 'View', 'CompareMemo', .T.)
DBSetProp('VLIVACOMPRAS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLIVACOMPRAS', 'View', 'FetchSize', 100)
DBSetProp('VLIVACOMPRAS', 'View', 'Comment', "")
DBSetProp('VLIVACOMPRAS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLIVACOMPRAS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLIVACOMPRAS
* Props for the VLIVACOMPRAS.compro field.
DBSetProp('VLIVACOMPRAS.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.compro', 'Field', 'UpdateName', 'compras.compro')
DBSetProp('VLIVACOMPRAS.compro', 'Field', 'DataType', "C(2)")
* Props for the VLIVACOMPRAS.letra field.
DBSetProp('VLIVACOMPRAS.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.letra', 'Field', 'UpdateName', 'compras.letra')
DBSetProp('VLIVACOMPRAS.letra', 'Field', 'DataType', "C(1)")
* Props for the VLIVACOMPRAS.numero field.
DBSetProp('VLIVACOMPRAS.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.numero', 'Field', 'UpdateName', 'compras.numero')
DBSetProp('VLIVACOMPRAS.numero', 'Field', 'DataType', "N(12)")
* Props for the VLIVACOMPRAS.fecha field.
DBSetProp('VLIVACOMPRAS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.fecha', 'Field', 'UpdateName', 'compras.fecha')
DBSetProp('VLIVACOMPRAS.fecha', 'Field', 'DataType', "D")
* Props for the VLIVACOMPRAS.nombre field.
DBSetProp('VLIVACOMPRAS.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.nombre', 'Field', 'UpdateName', 'provedor.nombre')
DBSetProp('VLIVACOMPRAS.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLIVACOMPRAS.sitiva field.
DBSetProp('VLIVACOMPRAS.sitiva', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.sitiva', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.sitiva', 'Field', 'UpdateName', 'provedor.sitiva')
DBSetProp('VLIVACOMPRAS.sitiva', 'Field', 'DataType', "C(3)")
* Props for the VLIVACOMPRAS.cuit field.
DBSetProp('VLIVACOMPRAS.cuit', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.cuit', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.cuit', 'Field', 'UpdateName', 'provedor.cuit')
DBSetProp('VLIVACOMPRAS.cuit', 'Field', 'DataType', "C(13)")
* Props for the VLIVACOMPRAS.gravado field.
DBSetProp('VLIVACOMPRAS.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.gravado', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.gravado', 'Field', 'UpdateName', 'Provedor.cuit*')
DBSetProp('VLIVACOMPRAS.gravado', 'Field', 'DataType', "N(13,2)")
* Props for the VLIVACOMPRAS.nogravado field.
DBSetProp('VLIVACOMPRAS.nogravado', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.nogravado', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.nogravado', 'Field', 'UpdateName', 'Provedor.cuit**')
DBSetProp('VLIVACOMPRAS.nogravado', 'Field', 'DataType', "N(13,2)")
* Props for the VLIVACOMPRAS.monotrib field.
DBSetProp('VLIVACOMPRAS.monotrib', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.monotrib', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.monotrib', 'Field', 'UpdateName', 'Provedor.cuit***')
DBSetProp('VLIVACOMPRAS.monotrib', 'Field', 'DataType', "N(13,2)")
* Props for the VLIVACOMPRAS.iva field.
DBSetProp('VLIVACOMPRAS.iva', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.iva', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.iva', 'Field', 'UpdateName', 'Provedor.cuit**')
DBSetProp('VLIVACOMPRAS.iva', 'Field', 'DataType', "N(13,2)")
* Props for the VLIVACOMPRAS.percepcion field.
DBSetProp('VLIVACOMPRAS.percepcion', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.percepcion', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.percepcion', 'Field', 'UpdateName', '')
DBSetProp('VLIVACOMPRAS.percepcion', 'Field', 'DataType', "N(13,2)")
* Props for the VLIVACOMPRAS.total field.
DBSetProp('VLIVACOMPRAS.total', 'Field', 'KeyField', .F.)
DBSetProp('VLIVACOMPRAS.total', 'Field', 'Updatable', .F.)
DBSetProp('VLIVACOMPRAS.total', 'Field', 'UpdateName', 'Provedor.cuit***')
DBSetProp('VLIVACOMPRAS.total', 'Field', 'DataType', "N(13,2)")
ENDFUNC
 
FUNCTION MakeView_VLCOMISIONVENDEDORREMITOS
***************** Ver la configuración para VLCOMISIONVENDEDORREMITOS ***************

CREATE SQL VIEW "VLCOMISIONVENDEDORREMITOS" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.fecha,  Facturas.condicion, Facturas.cliente, Clientes.nombre,  Facturas.gravado*Codven.mult_com AS gravado, Facturas.total,  Facturas.comision, Facturas.marca, Facturas.total*0 AS impComision FROM clientes,   facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.cliente = Clientes.codigo   AND (Codven.compro BETWEEN "RD" AND "RT"   AND Facturas.marca = "C"   AND Clientes.vendedor = ?nVendedor   AND Facturas.fechapago BETWEEN ?dDesde AND ?dHasta) ORDER BY Facturas.fecha

DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'UpdateType', 1)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'WhereType', 3)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'FetchMemo', .T.)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'SendUpdates', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'UseMemoSize', 255)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'MaxRecords', -1)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'Tables', 'facturas')
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'Prepared', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'CompareMemo', .T.)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'Comment', "")
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLCOMISIONVENDEDORREMITOS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLCOMISIONVENDEDORREMITOS
* Props for the VLCOMISIONVENDEDORREMITOS.compro field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLCOMISIONVENDEDORREMITOS.compro', 'Field', 'DataType', "C(2)")
* Props for the VLCOMISIONVENDEDORREMITOS.letra field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLCOMISIONVENDEDORREMITOS.letra', 'Field', 'DataType', "C(1)")
* Props for the VLCOMISIONVENDEDORREMITOS.numero field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLCOMISIONVENDEDORREMITOS.numero', 'Field', 'DataType', "N(12)")
* Props for the VLCOMISIONVENDEDORREMITOS.fecha field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLCOMISIONVENDEDORREMITOS.fecha', 'Field', 'DataType', "D")
* Props for the VLCOMISIONVENDEDORREMITOS.condicion field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.condicion', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.condicion', 'Field', 'UpdateName', 'facturas.condicion')
DBSetProp('VLCOMISIONVENDEDORREMITOS.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLCOMISIONVENDEDORREMITOS.cliente field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLCOMISIONVENDEDORREMITOS.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLCOMISIONVENDEDORREMITOS.nombre field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLCOMISIONVENDEDORREMITOS.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLCOMISIONVENDEDORREMITOS.gravado field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.gravado', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.gravado', 'Field', 'UpdateName', 'Clientes.nombre*')
DBSetProp('VLCOMISIONVENDEDORREMITOS.gravado', 'Field', 'DataType', "N(15,2)")
* Props for the VLCOMISIONVENDEDORREMITOS.total field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.total', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.total', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.total', 'Field', 'UpdateName', 'facturas.total')
DBSetProp('VLCOMISIONVENDEDORREMITOS.total', 'Field', 'DataType', "N(12,2)")
* Props for the VLCOMISIONVENDEDORREMITOS.comision field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.comision', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.comision', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.comision', 'Field', 'UpdateName', 'facturas.comision')
DBSetProp('VLCOMISIONVENDEDORREMITOS.comision', 'Field', 'DataType', "C(1)")
* Props for the VLCOMISIONVENDEDORREMITOS.marca field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.marca', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.marca', 'Field', 'UpdateName', 'facturas.marca')
DBSetProp('VLCOMISIONVENDEDORREMITOS.marca', 'Field', 'DataType', "C(1)")
* Props for the VLCOMISIONVENDEDORREMITOS.impcomision field.
DBSetProp('VLCOMISIONVENDEDORREMITOS.impcomision', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.impcomision', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORREMITOS.impcomision', 'Field', 'UpdateName', '')
DBSetProp('VLCOMISIONVENDEDORREMITOS.impcomision', 'Field', 'DataType', "N(14,2)")
ENDFUNC
 
FUNCTION MakeView_VLIVAVENTAS
***************** Ver la configuración para VLIVAVENTAS ***************

CREATE SQL VIEW "VLIVAVENTAS" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.fecha,  Facturas.nombre, Facturas.sitiva, Facturas.cuit,  Facturas.gravado*Codven.mult_ven AS gravado,  Facturas.exento*Codven.mult_ven AS exento,  Facturas.iva*Codven.mult_ven AS iva,  Facturas.acrece*Codven.mult_ven AS acrece,  Facturas.impint*Codven.mult_ven AS impint,  Facturas.total*Codven.mult_ven AS total, Facturas.codimp FROM clientes,   facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.cliente = Clientes.codigo   AND (MONTH(Facturas.fecha) = ?nMes   AND YEAR(Facturas.fecha) = ?nAnio   AND Codven.libroiva = .T.   AND Facturas.sucimp = ?nSucursal) ORDER BY Facturas.fecha, Facturas.letra, Facturas.numero

DBSetProp('VLIVAVENTAS', 'View', 'UpdateType', 1)
DBSetProp('VLIVAVENTAS', 'View', 'WhereType', 3)
DBSetProp('VLIVAVENTAS', 'View', 'FetchMemo', .T.)
DBSetProp('VLIVAVENTAS', 'View', 'SendUpdates', .F.)
DBSetProp('VLIVAVENTAS', 'View', 'UseMemoSize', 255)
DBSetProp('VLIVAVENTAS', 'View', 'FetchSize', 100)
DBSetProp('VLIVAVENTAS', 'View', 'MaxRecords', -1)
DBSetProp('VLIVAVENTAS', 'View', 'Tables', 'facturas')
DBSetProp('VLIVAVENTAS', 'View', 'Prepared', .F.)
DBSetProp('VLIVAVENTAS', 'View', 'CompareMemo', .T.)
DBSetProp('VLIVAVENTAS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLIVAVENTAS', 'View', 'FetchSize', 100)
DBSetProp('VLIVAVENTAS', 'View', 'Comment', "")
DBSetProp('VLIVAVENTAS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLIVAVENTAS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLIVAVENTAS
* Props for the VLIVAVENTAS.compro field.
DBSetProp('VLIVAVENTAS.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLIVAVENTAS.compro', 'Field', 'DataType', "C(2)")
* Props for the VLIVAVENTAS.letra field.
DBSetProp('VLIVAVENTAS.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLIVAVENTAS.letra', 'Field', 'DataType', "C(1)")
* Props for the VLIVAVENTAS.numero field.
DBSetProp('VLIVAVENTAS.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLIVAVENTAS.numero', 'Field', 'DataType', "N(12)")
* Props for the VLIVAVENTAS.fecha field.
DBSetProp('VLIVAVENTAS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLIVAVENTAS.fecha', 'Field', 'DataType', "D")
* Props for the VLIVAVENTAS.nombre field.
DBSetProp('VLIVAVENTAS.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLIVAVENTAS.nombre', 'Field', 'UpdateName', 'facturas.nombre')
DBSetProp('VLIVAVENTAS.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLIVAVENTAS.sitiva field.
DBSetProp('VLIVAVENTAS.sitiva', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.sitiva', 'Field', 'Updatable', .T.)
DBSetProp('VLIVAVENTAS.sitiva', 'Field', 'UpdateName', 'facturas.sitiva')
DBSetProp('VLIVAVENTAS.sitiva', 'Field', 'DataType', "C(3)")
* Props for the VLIVAVENTAS.cuit field.
DBSetProp('VLIVAVENTAS.cuit', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.cuit', 'Field', 'Updatable', .T.)
DBSetProp('VLIVAVENTAS.cuit', 'Field', 'UpdateName', 'facturas.cuit')
DBSetProp('VLIVAVENTAS.cuit', 'Field', 'DataType', "N(11)")
* Props for the VLIVAVENTAS.gravado field.
DBSetProp('VLIVAVENTAS.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.gravado', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.gravado', 'Field', 'UpdateName', '')
DBSetProp('VLIVAVENTAS.gravado', 'Field', 'DataType', "N(15,2)")
* Props for the VLIVAVENTAS.exento field.
DBSetProp('VLIVAVENTAS.exento', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.exento', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.exento', 'Field', 'UpdateName', 'Clientes.cuit**')
DBSetProp('VLIVAVENTAS.exento', 'Field', 'DataType', "N(15,2)")
* Props for the VLIVAVENTAS.iva field.
DBSetProp('VLIVAVENTAS.iva', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.iva', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.iva', 'Field', 'UpdateName', '')
DBSetProp('VLIVAVENTAS.iva', 'Field', 'DataType', "N(15,2)")
* Props for the VLIVAVENTAS.acrece field.
DBSetProp('VLIVAVENTAS.acrece', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.acrece', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.acrece', 'Field', 'UpdateName', '')
DBSetProp('VLIVAVENTAS.acrece', 'Field', 'DataType', "N(15,2)")
* Props for the VLIVAVENTAS.impint field.
DBSetProp('VLIVAVENTAS.impint', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.impint', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.impint', 'Field', 'UpdateName', '')
DBSetProp('VLIVAVENTAS.impint', 'Field', 'DataType', "N(13,2)")
* Props for the VLIVAVENTAS.total field.
DBSetProp('VLIVAVENTAS.total', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.total', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.total', 'Field', 'UpdateName', '')
DBSetProp('VLIVAVENTAS.total', 'Field', 'DataType', "N(15,2)")
* Props for the VLIVAVENTAS.codimp field.
DBSetProp('VLIVAVENTAS.codimp', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTAS.codimp', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTAS.codimp', 'Field', 'UpdateName', 'facturas.codimp')
DBSetProp('VLIVAVENTAS.codimp', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLVENTAIMPUTACION
***************** Ver la configuración para VLVENTAIMPUTACION ***************

CREATE SQL VIEW "VLVENTAIMPUTACION" ; 
   AS SELECT Facturas.codimp, Codimp.nombre,  SUM(Facturas.gravado*Codven.mult_ven) AS gravado,  SUM(Facturas.iva*Codven.mult_ven) AS iva,  SUM(Facturas.acrece*Codven.mult_ven) AS acrece,  SUM(Facturas.impint*Codven.mult_ven) AS impint,  SUM(Facturas.total*Codven.mult_ven) AS total FROM codimp,   facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.codimp = Codimp.codigo   AND (MONTH(Facturas.fecha) = ?nMes   AND YEAR(Facturas.fecha) = ?nAnio   AND Facturas.sucursal = ?nSucursal   AND Codven.libroiva = .T.) GROUP BY Facturas.codimp ORDER BY Facturas.codimp

DBSetProp('VLVENTAIMPUTACION', 'View', 'UpdateType', 1)
DBSetProp('VLVENTAIMPUTACION', 'View', 'WhereType', 3)
DBSetProp('VLVENTAIMPUTACION', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTAIMPUTACION', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTAIMPUTACION', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTAIMPUTACION', 'View', 'FetchSize', 100)
DBSetProp('VLVENTAIMPUTACION', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTAIMPUTACION', 'View', 'Tables', 'codimp')
DBSetProp('VLVENTAIMPUTACION', 'View', 'Prepared', .F.)
DBSetProp('VLVENTAIMPUTACION', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTAIMPUTACION', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTAIMPUTACION', 'View', 'FetchSize', 100)
DBSetProp('VLVENTAIMPUTACION', 'View', 'Comment', "")
DBSetProp('VLVENTAIMPUTACION', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTAIMPUTACION', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTAIMPUTACION
* Props for the VLVENTAIMPUTACION.codimp field.
DBSetProp('VLVENTAIMPUTACION.codimp', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAIMPUTACION.codimp', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTAIMPUTACION.codimp', 'Field', 'UpdateName', 'facturas.codimp')
DBSetProp('VLVENTAIMPUTACION.codimp', 'Field', 'DataType', "N(2)")
* Props for the VLVENTAIMPUTACION.nombre field.
DBSetProp('VLVENTAIMPUTACION.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAIMPUTACION.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAIMPUTACION.nombre', 'Field', 'UpdateName', 'codimp.nombre')
DBSetProp('VLVENTAIMPUTACION.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLVENTAIMPUTACION.gravado field.
DBSetProp('VLVENTAIMPUTACION.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAIMPUTACION.gravado', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTAIMPUTACION.gravado', 'Field', 'UpdateName', '')
DBSetProp('VLVENTAIMPUTACION.gravado', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTAIMPUTACION.iva field.
DBSetProp('VLVENTAIMPUTACION.iva', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAIMPUTACION.iva', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTAIMPUTACION.iva', 'Field', 'UpdateName', '')
DBSetProp('VLVENTAIMPUTACION.iva', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTAIMPUTACION.acrece field.
DBSetProp('VLVENTAIMPUTACION.acrece', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAIMPUTACION.acrece', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTAIMPUTACION.acrece', 'Field', 'UpdateName', '')
DBSetProp('VLVENTAIMPUTACION.acrece', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTAIMPUTACION.impint field.
DBSetProp('VLVENTAIMPUTACION.impint', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAIMPUTACION.impint', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTAIMPUTACION.impint', 'Field', 'UpdateName', '')
DBSetProp('VLVENTAIMPUTACION.impint', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTAIMPUTACION.total field.
DBSetProp('VLVENTAIMPUTACION.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAIMPUTACION.total', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTAIMPUTACION.total', 'Field', 'UpdateName', '')
DBSetProp('VLVENTAIMPUTACION.total', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLMOVSTOCK
***************** Ver la configuración para VLMOVSTOCK ***************

CREATE SQL VIEW "VLMOVSTOCK" ; 
   AS SELECT Movstock.fecha, Movstock.descripcio, Detven.codigo, Lista.medida,  Marcas.nombre AS marca, Lista.nombre, Detven.cantidad FROM marcas, movstock,   detven INNER JOIN lista    ON  Detven.codigo = Lista.codigo WHERE Lista.marca = Marcas.codigo   AND Detven.compro = Movstock.compro   AND Detven.numero = Movstock.numero   AND (Detven.compro = "MI"   AND Movstock.fecha BETWEEN ?dDesde AND ?dHasta   AND Movstock.sucursal = ?nSucursal) ORDER BY Movstock.fecha

DBSetProp('VLMOVSTOCK', 'View', 'UpdateType', 1)
DBSetProp('VLMOVSTOCK', 'View', 'WhereType', 3)
DBSetProp('VLMOVSTOCK', 'View', 'FetchMemo', .T.)
DBSetProp('VLMOVSTOCK', 'View', 'SendUpdates', .F.)
DBSetProp('VLMOVSTOCK', 'View', 'UseMemoSize', 255)
DBSetProp('VLMOVSTOCK', 'View', 'FetchSize', 100)
DBSetProp('VLMOVSTOCK', 'View', 'MaxRecords', -1)
DBSetProp('VLMOVSTOCK', 'View', 'Tables', '')
DBSetProp('VLMOVSTOCK', 'View', 'Prepared', .F.)
DBSetProp('VLMOVSTOCK', 'View', 'CompareMemo', .T.)
DBSetProp('VLMOVSTOCK', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLMOVSTOCK', 'View', 'FetchSize', 100)
DBSetProp('VLMOVSTOCK', 'View', 'Comment', "")
DBSetProp('VLMOVSTOCK', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLMOVSTOCK', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLMOVSTOCK
* Props for the VLMOVSTOCK.fecha field.
DBSetProp('VLMOVSTOCK.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCK.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCK.fecha', 'Field', 'UpdateName', 'movstock.fecha')
DBSetProp('VLMOVSTOCK.fecha', 'Field', 'DataType', "D")
* Props for the VLMOVSTOCK.descripcio field.
DBSetProp('VLMOVSTOCK.descripcio', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCK.descripcio', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCK.descripcio', 'Field', 'UpdateName', 'movstock.descripcio')
DBSetProp('VLMOVSTOCK.descripcio', 'Field', 'DataType', "C(40)")
* Props for the VLMOVSTOCK.codigo field.
DBSetProp('VLMOVSTOCK.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCK.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCK.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLMOVSTOCK.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLMOVSTOCK.medida field.
DBSetProp('VLMOVSTOCK.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCK.medida', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCK.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLMOVSTOCK.medida', 'Field', 'DataType', "C(10)")
* Props for the VLMOVSTOCK.marca field.
DBSetProp('VLMOVSTOCK.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCK.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCK.marca', 'Field', 'UpdateName', 'marcas.nombre')
DBSetProp('VLMOVSTOCK.marca', 'Field', 'DataType', "C(20)")
* Props for the VLMOVSTOCK.nombre field.
DBSetProp('VLMOVSTOCK.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCK.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCK.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLMOVSTOCK.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLMOVSTOCK.cantidad field.
DBSetProp('VLMOVSTOCK.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCK.cantidad', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCK.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLMOVSTOCK.cantidad', 'Field', 'DataType', "N(7,2)")
ENDFUNC
 
FUNCTION MakeView_VLSTOCK
***************** Ver la configuración para VLSTOCK ***************

CREATE SQL VIEW "VLSTOCK" ; 
   AS SELECT Stock.codigo, Lista.articulo, Lista.modelo, Lista.orden,  Lista.medida, Lista.codfabrica, Lista.fecha, Marcas.nombre AS marca,  Lista.nombre, Stock.stock, Stock.minimo,  Lista.costo*Stock.stock AS costotal, Lista.precio FROM lista, marcas, stock WHERE Stock.codigo = Lista.codigo   AND Lista.marca = Marcas.codigo   AND (Stock.stock <> 0   AND Lista.articulo BETWEEN ?nDesCod AND ?nHasCod   AND Lista.marca BETWEEN ?nDesMarca AND ?nHasMarca   AND Lista.modelo BETWEEN ?nDesMod AND ?nHasMod   AND Stock.deposito = ?nDeposito) ORDER BY Lista.articulo, Lista.modelo, Lista.orden

DBSetProp('VLSTOCK', 'View', 'UpdateType', 1)
DBSetProp('VLSTOCK', 'View', 'WhereType', 3)
DBSetProp('VLSTOCK', 'View', 'FetchMemo', .T.)
DBSetProp('VLSTOCK', 'View', 'SendUpdates', .F.)
DBSetProp('VLSTOCK', 'View', 'UseMemoSize', 255)
DBSetProp('VLSTOCK', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCK', 'View', 'MaxRecords', -1)
DBSetProp('VLSTOCK', 'View', 'Tables', '')
DBSetProp('VLSTOCK', 'View', 'Prepared', .F.)
DBSetProp('VLSTOCK', 'View', 'CompareMemo', .T.)
DBSetProp('VLSTOCK', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSTOCK', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCK', 'View', 'Comment', "")
DBSetProp('VLSTOCK', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSTOCK', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSTOCK
* Props for the VLSTOCK.codigo field.
DBSetProp('VLSTOCK.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.codigo', 'Field', 'UpdateName', 'stock.codigo')
DBSetProp('VLSTOCK.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCK.articulo field.
DBSetProp('VLSTOCK.articulo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.articulo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.articulo', 'Field', 'UpdateName', 'lista.articulo')
DBSetProp('VLSTOCK.articulo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCK.modelo field.
DBSetProp('VLSTOCK.modelo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.modelo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.modelo', 'Field', 'UpdateName', 'lista.modelo')
DBSetProp('VLSTOCK.modelo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCK.orden field.
DBSetProp('VLSTOCK.orden', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.orden', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.orden', 'Field', 'UpdateName', 'lista.orden')
DBSetProp('VLSTOCK.orden', 'Field', 'DataType', "N(3)")
* Props for the VLSTOCK.medida field.
DBSetProp('VLSTOCK.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.medida', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLSTOCK.medida', 'Field', 'DataType', "C(13)")
* Props for the VLSTOCK.codfabrica field.
DBSetProp('VLSTOCK.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.codfabrica', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLSTOCK.codfabrica', 'Field', 'DataType', "C(15)")
* Props for the VLSTOCK.fecha field.
DBSetProp('VLSTOCK.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.fecha', 'Field', 'UpdateName', 'lista.fecha')
DBSetProp('VLSTOCK.fecha', 'Field', 'DataType', "C(6)")
* Props for the VLSTOCK.marca field.
DBSetProp('VLSTOCK.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.marca', 'Field', 'UpdateName', 'marcas.nombre')
DBSetProp('VLSTOCK.marca', 'Field', 'DataType', "C(20)")
* Props for the VLSTOCK.nombre field.
DBSetProp('VLSTOCK.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLSTOCK.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLSTOCK.stock field.
DBSetProp('VLSTOCK.stock', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.stock', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.stock', 'Field', 'UpdateName', 'stock.stock')
DBSetProp('VLSTOCK.stock', 'Field', 'DataType', "N(10,2)")
* Props for the VLSTOCK.minimo field.
DBSetProp('VLSTOCK.minimo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.minimo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.minimo', 'Field', 'UpdateName', 'stock.minimo')
DBSetProp('VLSTOCK.minimo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCK.costotal field.
DBSetProp('VLSTOCK.costotal', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.costotal', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.costotal', 'Field', 'UpdateName', 'Stock.stock*')
DBSetProp('VLSTOCK.costotal', 'Field', 'DataType', "N(20,4)")
* Props for the VLSTOCK.precio field.
DBSetProp('VLSTOCK.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCK.precio', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCK.precio', 'Field', 'UpdateName', 'lista.precio')
DBSetProp('VLSTOCK.precio', 'Field', 'DataType', "N(12,2)")
ENDFUNC
 
FUNCTION MakeView_VLSTOCKVTA
***************** Ver la configuración para VLSTOCKVTA ***************

CREATE SQL VIEW "VLSTOCKVTA" ; 
   AS SELECT Detven.codigo, SUM(Detven.cantidad* Codven.mult_sto) AS stock FROM detven, codven, facturas WHERE Detven.compro = Codven.compro   AND Detven.compro = Facturas.compro   AND Detven.letra = Facturas.letra   AND Detven.numero = Facturas.numero   AND (Detven.codigo BETWEEN ?nDesCod AND ?nHasCod   AND Facturas.fecha <= ?dFecha   AND Detven.compro <> "MI") GROUP BY Detven.codigo ORDER BY Detven.codigo

DBSetProp('VLSTOCKVTA', 'View', 'UpdateType', 1)
DBSetProp('VLSTOCKVTA', 'View', 'WhereType', 3)
DBSetProp('VLSTOCKVTA', 'View', 'FetchMemo', .T.)
DBSetProp('VLSTOCKVTA', 'View', 'SendUpdates', .F.)
DBSetProp('VLSTOCKVTA', 'View', 'UseMemoSize', 255)
DBSetProp('VLSTOCKVTA', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKVTA', 'View', 'MaxRecords', -1)
DBSetProp('VLSTOCKVTA', 'View', 'Tables', 'detven')
DBSetProp('VLSTOCKVTA', 'View', 'Prepared', .F.)
DBSetProp('VLSTOCKVTA', 'View', 'CompareMemo', .T.)
DBSetProp('VLSTOCKVTA', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSTOCKVTA', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKVTA', 'View', 'Comment', "")
DBSetProp('VLSTOCKVTA', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSTOCKVTA', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSTOCKVTA
* Props for the VLSTOCKVTA.codigo field.
DBSetProp('VLSTOCKVTA.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVTA.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVTA.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLSTOCKVTA.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCKVTA.stock field.
DBSetProp('VLSTOCKVTA.stock', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVTA.stock', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKVTA.stock', 'Field', 'UpdateName', '')
DBSetProp('VLSTOCKVTA.stock', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLSTOCKMOVSTOCK
***************** Ver la configuración para VLSTOCKMOVSTOCK ***************

CREATE SQL VIEW "VLSTOCKMOVSTOCK" ; 
   AS SELECT Detven.codigo, SUM(Detven.cantidad) AS Stock FROM  detven INNER JOIN movstock    ON  Detven.numero = Movstock.numero WHERE Detven.codigo BETWEEN ?nDesCod AND ?nHasCod   AND Detven.compro = "MI" GROUP BY Detven.codigo ORDER BY Detven.codigo

DBSetProp('VLSTOCKMOVSTOCK', 'View', 'UpdateType', 1)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'WhereType', 3)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'FetchMemo', .T.)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'SendUpdates', .F.)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'UseMemoSize', 255)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'MaxRecords', -1)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'Tables', '')
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'Prepared', .F.)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'CompareMemo', .T.)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'Comment', "")
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSTOCKMOVSTOCK', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSTOCKMOVSTOCK
* Props for the VLSTOCKMOVSTOCK.codigo field.
DBSetProp('VLSTOCKMOVSTOCK.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKMOVSTOCK.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKMOVSTOCK.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLSTOCKMOVSTOCK.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCKMOVSTOCK.stock field.
DBSetProp('VLSTOCKMOVSTOCK.stock', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKMOVSTOCK.stock', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKMOVSTOCK.stock', 'Field', 'UpdateName', '')
DBSetProp('VLSTOCKMOVSTOCK.stock', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLSTOCKCOM
***************** Ver la configuración para VLSTOCKCOM ***************

CREATE SQL VIEW "VLSTOCKCOM" ; 
   AS SELECT Detcom.codigo, SUM(Detcom.cantidad*Codcom.mult_sto) AS stock FROM detcom, codcom, compras WHERE Detcom.compro = Codcom.codigo   AND Detcom.compro = Compras.compro   AND Detcom.letra = Compras.letra   AND Detcom.numero = Compras.numero   AND (Detcom.codigo BETWEEN ?nDesCod AND ?nHasCod   AND Compras.fecha <= ?dFecha) GROUP BY Detcom.codigo ORDER BY Detcom.codigo

DBSetProp('VLSTOCKCOM', 'View', 'UpdateType', 1)
DBSetProp('VLSTOCKCOM', 'View', 'WhereType', 3)
DBSetProp('VLSTOCKCOM', 'View', 'FetchMemo', .T.)
DBSetProp('VLSTOCKCOM', 'View', 'SendUpdates', .F.)
DBSetProp('VLSTOCKCOM', 'View', 'UseMemoSize', 255)
DBSetProp('VLSTOCKCOM', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKCOM', 'View', 'MaxRecords', -1)
DBSetProp('VLSTOCKCOM', 'View', 'Tables', '')
DBSetProp('VLSTOCKCOM', 'View', 'Prepared', .F.)
DBSetProp('VLSTOCKCOM', 'View', 'CompareMemo', .T.)
DBSetProp('VLSTOCKCOM', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSTOCKCOM', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKCOM', 'View', 'Comment', "")
DBSetProp('VLSTOCKCOM', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSTOCKCOM', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSTOCKCOM
* Props for the VLSTOCKCOM.codigo field.
DBSetProp('VLSTOCKCOM.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCOM.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKCOM.codigo', 'Field', 'UpdateName', 'detcom.codigo')
DBSetProp('VLSTOCKCOM.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCKCOM.stock field.
DBSetProp('VLSTOCKCOM.stock', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCOM.stock', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKCOM.stock', 'Field', 'UpdateName', 'Detcom.codigo*')
DBSetProp('VLSTOCKCOM.stock', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLVENTASMARCA
***************** Ver la configuración para VLVENTASMARCA ***************

CREATE SQL VIEW "VLVENTASMARCA" ; 
   AS SELECT Detven.compro, Detven.letra, Detven.numero, Facturas.fecha,  Facturas.cliente, Detven.codigo, Lista.articulo, Lista.modelo,  Lista.nombre, Lista.medida, Detven.cantidad, Detven.precio,  Detven.descuento, Detven.total,  Detven.cantidad*Lista.precio*Codven.mult_stad AS compra,  Facturas.sucursal FROM facturas, codven,   detven INNER JOIN lista    ON  Detven.codigo = Lista.codigo WHERE Detven.compro = Codven.compro   AND Detven.compro = Facturas.compro   AND Detven.letra = Facturas.letra   AND Detven.numero = Facturas.numero   AND (Lista.marca = ?nMarca   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Codven.mult_stad <> 0   AND Facturas.noestadist <> .T.) ORDER BY Lista.articulo, Lista.modelo, Detven.codigo

DBSetProp('VLVENTASMARCA', 'View', 'UpdateType', 1)
DBSetProp('VLVENTASMARCA', 'View', 'WhereType', 3)
DBSetProp('VLVENTASMARCA', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTASMARCA', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTASMARCA', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTASMARCA', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASMARCA', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTASMARCA', 'View', 'Tables', 'detven,facturas,lista')
DBSetProp('VLVENTASMARCA', 'View', 'Prepared', .F.)
DBSetProp('VLVENTASMARCA', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTASMARCA', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTASMARCA', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASMARCA', 'View', 'Comment', "")
DBSetProp('VLVENTASMARCA', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTASMARCA', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTASMARCA
* Props for the VLVENTASMARCA.compro field.
DBSetProp('VLVENTASMARCA.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLVENTASMARCA.compro', 'Field', 'DataType', "C(2)")
* Props for the VLVENTASMARCA.letra field.
DBSetProp('VLVENTASMARCA.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLVENTASMARCA.letra', 'Field', 'DataType', "C(1)")
* Props for the VLVENTASMARCA.numero field.
DBSetProp('VLVENTASMARCA.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLVENTASMARCA.numero', 'Field', 'DataType', "N(12)")
* Props for the VLVENTASMARCA.fecha field.
DBSetProp('VLVENTASMARCA.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTASMARCA.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTASMARCA.cliente field.
DBSetProp('VLVENTASMARCA.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLVENTASMARCA.cliente', 'Field', 'DataType', "N(5)")
* Props for the VLVENTASMARCA.codigo field.
DBSetProp('VLVENTASMARCA.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLVENTASMARCA.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLVENTASMARCA.articulo field.
DBSetProp('VLVENTASMARCA.articulo', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.articulo', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.articulo', 'Field', 'UpdateName', 'lista.articulo')
DBSetProp('VLVENTASMARCA.articulo', 'Field', 'DataType', "N(4)")
* Props for the VLVENTASMARCA.modelo field.
DBSetProp('VLVENTASMARCA.modelo', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.modelo', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.modelo', 'Field', 'UpdateName', 'lista.modelo')
DBSetProp('VLVENTASMARCA.modelo', 'Field', 'DataType', "N(4)")
* Props for the VLVENTASMARCA.nombre field.
DBSetProp('VLVENTASMARCA.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLVENTASMARCA.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLVENTASMARCA.medida field.
DBSetProp('VLVENTASMARCA.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.medida', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLVENTASMARCA.medida', 'Field', 'DataType', "C(10)")
* Props for the VLVENTASMARCA.cantidad field.
DBSetProp('VLVENTASMARCA.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.cantidad', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLVENTASMARCA.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLVENTASMARCA.precio field.
DBSetProp('VLVENTASMARCA.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.precio', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLVENTASMARCA.precio', 'Field', 'DataType', "N(10,2)")
* Props for the VLVENTASMARCA.descuento field.
DBSetProp('VLVENTASMARCA.descuento', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.descuento', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.descuento', 'Field', 'UpdateName', 'detven.descuento')
DBSetProp('VLVENTASMARCA.descuento', 'Field', 'DataType', "N(6,2)")
* Props for the VLVENTASMARCA.total field.
DBSetProp('VLVENTASMARCA.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.total', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.total', 'Field', 'UpdateName', 'detven.total')
DBSetProp('VLVENTASMARCA.total', 'Field', 'DataType', "N(10,2)")
* Props for the VLVENTASMARCA.compra field.
DBSetProp('VLVENTASMARCA.compra', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.compra', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCA.compra', 'Field', 'UpdateName', '')
DBSetProp('VLVENTASMARCA.compra', 'Field', 'DataType', "N(20,4)")
* Props for the VLVENTASMARCA.sucursal field.
DBSetProp('VLVENTASMARCA.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCA.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCA.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLVENTASMARCA.sucursal', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLVENTASMARCAVENDEDOR
***************** Ver la configuración para VLVENTASMARCAVENDEDOR ***************

CREATE SQL VIEW "VLVENTASMARCAVENDEDOR" ; 
   AS SELECT Detven.compro, Detven.letra, Detven.numero, Facturas.fecha,  Facturas.cliente, Detven.codigo, Lista.articulo, Lista.modelo,  Lista.nombre, Lista.medida, Detven.cantidad,  Lista.costo*Codven.mult_sto*-1 AS precio, Detven.descuento,  (Lista.costo+(Lista.costo*Detven.descuento/100))*Detven.cantidad*Codven.mult_stad AS total,  Facturas.sucursal FROM facturas, codven, clientes,   detven INNER JOIN lista    ON  Detven.codigo = Lista.codigo WHERE Detven.compro = Codven.compro   AND Detven.compro = Facturas.compro   AND Detven.letra = Facturas.letra   AND Detven.numero = Facturas.numero   AND Facturas.cliente = Clientes.codigo   AND (Lista.marca = ?nMarca   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Codven.mult_stad <> 0   AND Clientes.vendedor = ?nVendedor   AND Facturas.noestadist <> .T.) ORDER BY Lista.articulo, Lista.modelo, Detven.codigo

DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'UpdateType', 1)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'WhereType', 3)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'Tables', 'lista,facturas')
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'Prepared', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'Comment', "")
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTASMARCAVENDEDOR', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTASMARCAVENDEDOR
* Props for the VLVENTASMARCAVENDEDOR.compro field.
DBSetProp('VLVENTASMARCAVENDEDOR.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLVENTASMARCAVENDEDOR.compro', 'Field', 'DataType', "C(2)")
* Props for the VLVENTASMARCAVENDEDOR.letra field.
DBSetProp('VLVENTASMARCAVENDEDOR.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLVENTASMARCAVENDEDOR.letra', 'Field', 'DataType', "C(1)")
* Props for the VLVENTASMARCAVENDEDOR.numero field.
DBSetProp('VLVENTASMARCAVENDEDOR.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLVENTASMARCAVENDEDOR.numero', 'Field', 'DataType', "N(12)")
* Props for the VLVENTASMARCAVENDEDOR.fecha field.
DBSetProp('VLVENTASMARCAVENDEDOR.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTASMARCAVENDEDOR.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTASMARCAVENDEDOR.cliente field.
DBSetProp('VLVENTASMARCAVENDEDOR.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLVENTASMARCAVENDEDOR.cliente', 'Field', 'DataType', "N(5)")
* Props for the VLVENTASMARCAVENDEDOR.codigo field.
DBSetProp('VLVENTASMARCAVENDEDOR.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLVENTASMARCAVENDEDOR.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLVENTASMARCAVENDEDOR.articulo field.
DBSetProp('VLVENTASMARCAVENDEDOR.articulo', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.articulo', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCAVENDEDOR.articulo', 'Field', 'UpdateName', 'lista.articulo')
DBSetProp('VLVENTASMARCAVENDEDOR.articulo', 'Field', 'DataType', "N(4)")
* Props for the VLVENTASMARCAVENDEDOR.modelo field.
DBSetProp('VLVENTASMARCAVENDEDOR.modelo', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.modelo', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCAVENDEDOR.modelo', 'Field', 'UpdateName', 'lista.modelo')
DBSetProp('VLVENTASMARCAVENDEDOR.modelo', 'Field', 'DataType', "N(4)")
* Props for the VLVENTASMARCAVENDEDOR.nombre field.
DBSetProp('VLVENTASMARCAVENDEDOR.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLVENTASMARCAVENDEDOR.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLVENTASMARCAVENDEDOR.medida field.
DBSetProp('VLVENTASMARCAVENDEDOR.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.medida', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLVENTASMARCAVENDEDOR.medida', 'Field', 'DataType', "C(10)")
* Props for the VLVENTASMARCAVENDEDOR.cantidad field.
DBSetProp('VLVENTASMARCAVENDEDOR.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.cantidad', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLVENTASMARCAVENDEDOR.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLVENTASMARCAVENDEDOR.precio field.
DBSetProp('VLVENTASMARCAVENDEDOR.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.precio', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.precio', 'Field', 'UpdateName', 'Detven.descuento*')
DBSetProp('VLVENTASMARCAVENDEDOR.precio', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTASMARCAVENDEDOR.descuento field.
DBSetProp('VLVENTASMARCAVENDEDOR.descuento', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.descuento', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.descuento', 'Field', 'UpdateName', 'detven.descuento')
DBSetProp('VLVENTASMARCAVENDEDOR.descuento', 'Field', 'DataType', "N(6,2)")
* Props for the VLVENTASMARCAVENDEDOR.total field.
DBSetProp('VLVENTASMARCAVENDEDOR.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.total', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.total', 'Field', 'UpdateName', '')
DBSetProp('VLVENTASMARCAVENDEDOR.total', 'Field', 'DataType', "N(20,6)")
* Props for the VLVENTASMARCAVENDEDOR.sucursal field.
DBSetProp('VLVENTASMARCAVENDEDOR.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASMARCAVENDEDOR.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASMARCAVENDEDOR.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLVENTASMARCAVENDEDOR.sucursal', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLFICHASTOVEN
***************** Ver la configuración para VLFICHASTOVEN ***************

CREATE SQL VIEW "VLFICHASTOVEN" ; 
   AS SELECT Detven.codigo, Detven.compro, Detven.letra, Detven.numero,  Facturas.fecha, Detven.cantidad*Codven.mult_sto AS cantidad,  Detven.precio, Detven.total, Facturas.cliente, "V" AS marca,  Facturas.noestadist, Facturas.sucursal FROM facturas,   detven INNER JOIN codven    ON  Detven.compro = Codven.compro WHERE Detven.compro = Facturas.compro   AND Detven.letra = Facturas.letra   AND Detven.numero = Facturas.numero   AND (Codven.mult_sto <> 0   AND Detven.codigo = ?nCodigo   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta) ORDER BY Facturas.fecha

DBSetProp('VLFICHASTOVEN', 'View', 'UpdateType', 1)
DBSetProp('VLFICHASTOVEN', 'View', 'WhereType', 3)
DBSetProp('VLFICHASTOVEN', 'View', 'FetchMemo', .T.)
DBSetProp('VLFICHASTOVEN', 'View', 'SendUpdates', .F.)
DBSetProp('VLFICHASTOVEN', 'View', 'UseMemoSize', 255)
DBSetProp('VLFICHASTOVEN', 'View', 'FetchSize', 100)
DBSetProp('VLFICHASTOVEN', 'View', 'MaxRecords', -1)
DBSetProp('VLFICHASTOVEN', 'View', 'Tables', 'facturas')
DBSetProp('VLFICHASTOVEN', 'View', 'Prepared', .F.)
DBSetProp('VLFICHASTOVEN', 'View', 'CompareMemo', .T.)
DBSetProp('VLFICHASTOVEN', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLFICHASTOVEN', 'View', 'FetchSize', 100)
DBSetProp('VLFICHASTOVEN', 'View', 'Comment', "")
DBSetProp('VLFICHASTOVEN', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLFICHASTOVEN', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLFICHASTOVEN
* Props for the VLFICHASTOVEN.codigo field.
DBSetProp('VLFICHASTOVEN.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOVEN.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLFICHASTOVEN.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLFICHASTOVEN.compro field.
DBSetProp('VLFICHASTOVEN.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOVEN.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLFICHASTOVEN.compro', 'Field', 'DataType', "C(2)")
* Props for the VLFICHASTOVEN.letra field.
DBSetProp('VLFICHASTOVEN.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOVEN.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLFICHASTOVEN.letra', 'Field', 'DataType', "C(1)")
* Props for the VLFICHASTOVEN.numero field.
DBSetProp('VLFICHASTOVEN.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOVEN.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLFICHASTOVEN.numero', 'Field', 'DataType', "N(12)")
* Props for the VLFICHASTOVEN.fecha field.
DBSetProp('VLFICHASTOVEN.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOVEN.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLFICHASTOVEN.fecha', 'Field', 'DataType', "D")
* Props for the VLFICHASTOVEN.cantidad field.
DBSetProp('VLFICHASTOVEN.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.cantidad', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOVEN.cantidad', 'Field', 'UpdateName', 'Facturas.fecha*')
DBSetProp('VLFICHASTOVEN.cantidad', 'Field', 'DataType', "N(10,2)")
* Props for the VLFICHASTOVEN.precio field.
DBSetProp('VLFICHASTOVEN.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.precio', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOVEN.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLFICHASTOVEN.precio', 'Field', 'DataType', "N(10,2)")
* Props for the VLFICHASTOVEN.total field.
DBSetProp('VLFICHASTOVEN.total', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.total', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOVEN.total', 'Field', 'UpdateName', 'detven.total')
DBSetProp('VLFICHASTOVEN.total', 'Field', 'DataType', "N(10,2)")
* Props for the VLFICHASTOVEN.cliente field.
DBSetProp('VLFICHASTOVEN.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOVEN.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLFICHASTOVEN.cliente', 'Field', 'DataType', "N(5)")
* Props for the VLFICHASTOVEN.marca field.
DBSetProp('VLFICHASTOVEN.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOVEN.marca', 'Field', 'UpdateName', '')
DBSetProp('VLFICHASTOVEN.marca', 'Field', 'DataType', "C(1)")
* Props for the VLFICHASTOVEN.noestadist field.
DBSetProp('VLFICHASTOVEN.noestadist', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.noestadist', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOVEN.noestadist', 'Field', 'UpdateName', 'facturas.noestadist')
DBSetProp('VLFICHASTOVEN.noestadist', 'Field', 'DataType', "L")
* Props for the VLFICHASTOVEN.sucursal field.
DBSetProp('VLFICHASTOVEN.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOVEN.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOVEN.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLFICHASTOVEN.sucursal', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLFICHASTOCOM
***************** Ver la configuración para VLFICHASTOCOM ***************

CREATE SQL VIEW "VLFICHASTOCOM" ; 
   AS SELECT Detcom.codigo, Detcom.compro, Detcom.letra, Detcom.numero,  Compras.fecha, Detcom.cantidad*Codcom.mult_sto AS cantidad,  Detcom.precio, Detcom.total, Compras.proveedor, "C" AS marca,  Compras.sucursal FROM compras,   detcom INNER JOIN codcom    ON  Detcom.compro = Codcom.codigo WHERE Detcom.compro = Compras.compro   AND Detcom.letra = Compras.letra   AND Detcom.numero = Compras.numero   AND (Codcom.mult_sto <> 0   AND Detcom.codigo = ?nCodigo   AND Compras.fecha BETWEEN ?dDesde AND ?dHasta) ORDER BY Compras.fecha

DBSetProp('VLFICHASTOCOM', 'View', 'UpdateType', 1)
DBSetProp('VLFICHASTOCOM', 'View', 'WhereType', 3)
DBSetProp('VLFICHASTOCOM', 'View', 'FetchMemo', .T.)
DBSetProp('VLFICHASTOCOM', 'View', 'SendUpdates', .F.)
DBSetProp('VLFICHASTOCOM', 'View', 'UseMemoSize', 255)
DBSetProp('VLFICHASTOCOM', 'View', 'FetchSize', 100)
DBSetProp('VLFICHASTOCOM', 'View', 'MaxRecords', -1)
DBSetProp('VLFICHASTOCOM', 'View', 'Tables', 'compras')
DBSetProp('VLFICHASTOCOM', 'View', 'Prepared', .F.)
DBSetProp('VLFICHASTOCOM', 'View', 'CompareMemo', .T.)
DBSetProp('VLFICHASTOCOM', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLFICHASTOCOM', 'View', 'FetchSize', 100)
DBSetProp('VLFICHASTOCOM', 'View', 'Comment', "")
DBSetProp('VLFICHASTOCOM', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLFICHASTOCOM', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLFICHASTOCOM
* Props for the VLFICHASTOCOM.codigo field.
DBSetProp('VLFICHASTOCOM.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOCOM.codigo', 'Field', 'UpdateName', 'detcom.codigo')
DBSetProp('VLFICHASTOCOM.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLFICHASTOCOM.compro field.
DBSetProp('VLFICHASTOCOM.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOCOM.compro', 'Field', 'UpdateName', 'detcom.compro')
DBSetProp('VLFICHASTOCOM.compro', 'Field', 'DataType', "C(2)")
* Props for the VLFICHASTOCOM.letra field.
DBSetProp('VLFICHASTOCOM.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOCOM.letra', 'Field', 'UpdateName', 'detcom.letra')
DBSetProp('VLFICHASTOCOM.letra', 'Field', 'DataType', "C(1)")
* Props for the VLFICHASTOCOM.numero field.
DBSetProp('VLFICHASTOCOM.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOCOM.numero', 'Field', 'UpdateName', 'detcom.numero')
DBSetProp('VLFICHASTOCOM.numero', 'Field', 'DataType', "N(12)")
* Props for the VLFICHASTOCOM.fecha field.
DBSetProp('VLFICHASTOCOM.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOCOM.fecha', 'Field', 'UpdateName', 'compras.fecha')
DBSetProp('VLFICHASTOCOM.fecha', 'Field', 'DataType', "D")
* Props for the VLFICHASTOCOM.cantidad field.
DBSetProp('VLFICHASTOCOM.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.cantidad', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOCOM.cantidad', 'Field', 'UpdateName', 'Compras.fecha*')
DBSetProp('VLFICHASTOCOM.cantidad', 'Field', 'DataType', "N(10,2)")
* Props for the VLFICHASTOCOM.precio field.
DBSetProp('VLFICHASTOCOM.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.precio', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOCOM.precio', 'Field', 'UpdateName', 'detcom.precio')
DBSetProp('VLFICHASTOCOM.precio', 'Field', 'DataType', "N(10,2)")
* Props for the VLFICHASTOCOM.total field.
DBSetProp('VLFICHASTOCOM.total', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.total', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOCOM.total', 'Field', 'UpdateName', 'detcom.total')
DBSetProp('VLFICHASTOCOM.total', 'Field', 'DataType', "N(10,2)")
* Props for the VLFICHASTOCOM.proveedor field.
DBSetProp('VLFICHASTOCOM.proveedor', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.proveedor', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOCOM.proveedor', 'Field', 'UpdateName', 'compras.proveedor')
DBSetProp('VLFICHASTOCOM.proveedor', 'Field', 'DataType', "N(4)")
* Props for the VLFICHASTOCOM.marca field.
DBSetProp('VLFICHASTOCOM.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOCOM.marca', 'Field', 'UpdateName', 'Compras.proveedor*')
DBSetProp('VLFICHASTOCOM.marca', 'Field', 'DataType', "C(1)")
* Props for the VLFICHASTOCOM.sucursal field.
DBSetProp('VLFICHASTOCOM.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOCOM.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOCOM.sucursal', 'Field', 'UpdateName', 'compras.sucursal')
DBSetProp('VLFICHASTOCOM.sucursal', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLFICHASTOMOV
***************** Ver la configuración para VLFICHASTOMOV ***************

CREATE SQL VIEW "VLFICHASTOMOV" ; 
   AS SELECT Detven.codigo, Detven.compro, Detven.letra, Detven.numero,  Movstock.fecha, Detven.cantidad, Detven.precio, Detven.total, 0 AS cliente,  "V" AS marca, Movstock.sucursal FROM detven, movstock WHERE Detven.compro = Movstock.compro   AND Detven.numero = Movstock.numero   AND (Detven.codigo = ?nCodigo   AND Movstock.fecha BETWEEN ?dDesde AND ?dHasta) ORDER BY Movstock.fecha

DBSetProp('VLFICHASTOMOV', 'View', 'UpdateType', 1)
DBSetProp('VLFICHASTOMOV', 'View', 'WhereType', 3)
DBSetProp('VLFICHASTOMOV', 'View', 'FetchMemo', .T.)
DBSetProp('VLFICHASTOMOV', 'View', 'SendUpdates', .F.)
DBSetProp('VLFICHASTOMOV', 'View', 'UseMemoSize', 255)
DBSetProp('VLFICHASTOMOV', 'View', 'FetchSize', 100)
DBSetProp('VLFICHASTOMOV', 'View', 'MaxRecords', -1)
DBSetProp('VLFICHASTOMOV', 'View', 'Tables', 'detven,movstock')
DBSetProp('VLFICHASTOMOV', 'View', 'Prepared', .F.)
DBSetProp('VLFICHASTOMOV', 'View', 'CompareMemo', .T.)
DBSetProp('VLFICHASTOMOV', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLFICHASTOMOV', 'View', 'FetchSize', 100)
DBSetProp('VLFICHASTOMOV', 'View', 'Comment', "")
DBSetProp('VLFICHASTOMOV', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLFICHASTOMOV', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLFICHASTOMOV
* Props for the VLFICHASTOMOV.codigo field.
DBSetProp('VLFICHASTOMOV.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOMOV.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLFICHASTOMOV.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLFICHASTOMOV.compro field.
DBSetProp('VLFICHASTOMOV.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOMOV.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLFICHASTOMOV.compro', 'Field', 'DataType', "C(2)")
* Props for the VLFICHASTOMOV.letra field.
DBSetProp('VLFICHASTOMOV.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOMOV.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLFICHASTOMOV.letra', 'Field', 'DataType', "C(1)")
* Props for the VLFICHASTOMOV.numero field.
DBSetProp('VLFICHASTOMOV.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOMOV.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLFICHASTOMOV.numero', 'Field', 'DataType', "N(12)")
* Props for the VLFICHASTOMOV.fecha field.
DBSetProp('VLFICHASTOMOV.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOMOV.fecha', 'Field', 'UpdateName', 'movstock.fecha')
DBSetProp('VLFICHASTOMOV.fecha', 'Field', 'DataType', "D")
* Props for the VLFICHASTOMOV.cantidad field.
DBSetProp('VLFICHASTOMOV.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.cantidad', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOMOV.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLFICHASTOMOV.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLFICHASTOMOV.precio field.
DBSetProp('VLFICHASTOMOV.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.precio', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOMOV.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLFICHASTOMOV.precio', 'Field', 'DataType', "N(10,2)")
* Props for the VLFICHASTOMOV.total field.
DBSetProp('VLFICHASTOMOV.total', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.total', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOMOV.total', 'Field', 'UpdateName', 'detven.total')
DBSetProp('VLFICHASTOMOV.total', 'Field', 'DataType', "N(10,2)")
* Props for the VLFICHASTOMOV.cliente field.
DBSetProp('VLFICHASTOMOV.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOMOV.cliente', 'Field', 'UpdateName', '')
DBSetProp('VLFICHASTOMOV.cliente', 'Field', 'DataType', "N(1)")
* Props for the VLFICHASTOMOV.marca field.
DBSetProp('VLFICHASTOMOV.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLFICHASTOMOV.marca', 'Field', 'UpdateName', '')
DBSetProp('VLFICHASTOMOV.marca', 'Field', 'DataType', "C(1)")
* Props for the VLFICHASTOMOV.sucursal field.
DBSetProp('VLFICHASTOMOV.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLFICHASTOMOV.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLFICHASTOMOV.sucursal', 'Field', 'UpdateName', 'movstock.sucursal')
DBSetProp('VLFICHASTOMOV.sucursal', 'Field', 'DataType', "N(1)")
ENDFUNC
 
FUNCTION MakeView_VLTOTALRTOSCLIENTES
***************** Ver la configuración para VLTOTALRTOSCLIENTES ***************

CREATE SQL VIEW "VLTOTALRTOSCLIENTES" ; 
   AS SELECT Facturas.cliente, Clientes.nombre, Clientes.domicilio,  Clientes.codpostal, Clientes.sitiva, Clientes.cuit, Clientes.telefono,  SUM(Facturas.total*Codven.mult_sto*-1) AS total FROM clientes,   facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.cliente = Clientes.codigo   AND (Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Codven.mult_cli = 0) GROUP BY Facturas.cliente ORDER BY Clientes.nombre

DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'UpdateType', 1)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'WhereType', 3)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'FetchMemo', .T.)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'SendUpdates', .F.)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'UseMemoSize', 255)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'MaxRecords', -1)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'Tables', '')
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'Prepared', .F.)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'CompareMemo', .T.)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'Comment', "")
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLTOTALRTOSCLIENTES', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLTOTALRTOSCLIENTES
* Props for the VLTOTALRTOSCLIENTES.cliente field.
DBSetProp('VLTOTALRTOSCLIENTES.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLTOTALRTOSCLIENTES.cliente', 'Field', 'DataType', "N(4)")
* Props for the VLTOTALRTOSCLIENTES.nombre field.
DBSetProp('VLTOTALRTOSCLIENTES.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLTOTALRTOSCLIENTES.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLTOTALRTOSCLIENTES.domicilio field.
DBSetProp('VLTOTALRTOSCLIENTES.domicilio', 'Field', 'KeyField', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.domicilio', 'Field', 'Updatable', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.domicilio', 'Field', 'UpdateName', 'clientes.domicilio')
DBSetProp('VLTOTALRTOSCLIENTES.domicilio', 'Field', 'DataType', "C(30)")
* Props for the VLTOTALRTOSCLIENTES.codpostal field.
DBSetProp('VLTOTALRTOSCLIENTES.codpostal', 'Field', 'KeyField', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.codpostal', 'Field', 'Updatable', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.codpostal', 'Field', 'UpdateName', 'clientes.codpostal')
DBSetProp('VLTOTALRTOSCLIENTES.codpostal', 'Field', 'DataType', "C(5)")
* Props for the VLTOTALRTOSCLIENTES.sitiva field.
DBSetProp('VLTOTALRTOSCLIENTES.sitiva', 'Field', 'KeyField', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.sitiva', 'Field', 'Updatable', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.sitiva', 'Field', 'UpdateName', 'clientes.sitiva')
DBSetProp('VLTOTALRTOSCLIENTES.sitiva', 'Field', 'DataType', "C(3)")
* Props for the VLTOTALRTOSCLIENTES.cuit field.
DBSetProp('VLTOTALRTOSCLIENTES.cuit', 'Field', 'KeyField', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.cuit', 'Field', 'Updatable', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.cuit', 'Field', 'UpdateName', 'clientes.cuit')
DBSetProp('VLTOTALRTOSCLIENTES.cuit', 'Field', 'DataType', "N(11)")
* Props for the VLTOTALRTOSCLIENTES.telefono field.
DBSetProp('VLTOTALRTOSCLIENTES.telefono', 'Field', 'KeyField', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.telefono', 'Field', 'Updatable', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.telefono', 'Field', 'UpdateName', 'clientes.telefono')
DBSetProp('VLTOTALRTOSCLIENTES.telefono', 'Field', 'DataType', "C(15)")
* Props for the VLTOTALRTOSCLIENTES.total field.
DBSetProp('VLTOTALRTOSCLIENTES.total', 'Field', 'KeyField', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.total', 'Field', 'Updatable', .F.)
DBSetProp('VLTOTALRTOSCLIENTES.total', 'Field', 'UpdateName', 'Clientes.telefono*')
DBSetProp('VLTOTALRTOSCLIENTES.total', 'Field', 'DataType', "N(18,2)")
ENDFUNC
 
FUNCTION MakeView_VLDETALLECOMPRASPROV
***************** Ver la configuración para VLDETALLECOMPRASPROV ***************

CREATE SQL VIEW "VLDETALLECOMPRASPROV" ; 
   AS SELECT Detcom.proveedor, Detcom.compro, Detcom.letra, Detcom.numero,  Compras.fecha, Lista.codfabrica, Detcom.codigo, Lista.nombre,  Lista.articulo, Articulo.nombre AS nomarticulo, Lista.marca,  Marcas.nombre AS nommarca, Detcom.cantidad, Detcom.precio, Detcom.total,  Compras.sucursal FROM detcom, compras!compras, lista, articulo, marcas WHERE Detcom.id = Compras.id   AND Detcom.codigo = Lista.codigo   AND Lista.articulo = Articulo.codigo   AND Lista.marca = Marcas.codigo   AND (Detcom.proveedor = ?nProveedor   AND Compras.fecha BETWEEN ?dDesde AND ?dHasta) ORDER BY Compras.fecha, Detcom.numero

DBSetProp('VLDETALLECOMPRASPROV', 'View', 'UpdateType', 1)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'WhereType', 3)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'FetchMemo', .T.)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'SendUpdates', .F.)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'UseMemoSize', 255)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'FetchSize', 100)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'MaxRecords', -1)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'Tables', 'lista,articulo,marcas,compras!compras')
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'Prepared', .F.)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'CompareMemo', .T.)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'FetchSize', 100)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'Comment', "")
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLDETALLECOMPRASPROV', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLDETALLECOMPRASPROV
* Props for the VLDETALLECOMPRASPROV.proveedor field.
DBSetProp('VLDETALLECOMPRASPROV.proveedor', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.proveedor', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLECOMPRASPROV.proveedor', 'Field', 'UpdateName', 'detcom.proveedor')
DBSetProp('VLDETALLECOMPRASPROV.proveedor', 'Field', 'DataType', "N(4)")
* Props for the VLDETALLECOMPRASPROV.compro field.
DBSetProp('VLDETALLECOMPRASPROV.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLECOMPRASPROV.compro', 'Field', 'UpdateName', 'detcom.compro')
DBSetProp('VLDETALLECOMPRASPROV.compro', 'Field', 'DataType', "C(2)")
* Props for the VLDETALLECOMPRASPROV.letra field.
DBSetProp('VLDETALLECOMPRASPROV.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLECOMPRASPROV.letra', 'Field', 'UpdateName', 'detcom.letra')
DBSetProp('VLDETALLECOMPRASPROV.letra', 'Field', 'DataType', "C(1)")
* Props for the VLDETALLECOMPRASPROV.numero field.
DBSetProp('VLDETALLECOMPRASPROV.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLECOMPRASPROV.numero', 'Field', 'UpdateName', 'detcom.numero')
DBSetProp('VLDETALLECOMPRASPROV.numero', 'Field', 'DataType', "N(12)")
* Props for the VLDETALLECOMPRASPROV.fecha field.
DBSetProp('VLDETALLECOMPRASPROV.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLECOMPRASPROV.fecha', 'Field', 'UpdateName', 'compras!compras.fecha')
DBSetProp('VLDETALLECOMPRASPROV.fecha', 'Field', 'DataType', "D")
* Props for the VLDETALLECOMPRASPROV.codfabrica field.
DBSetProp('VLDETALLECOMPRASPROV.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.codfabrica', 'Field', 'Updatable', .T.)
DBSetProp('VLDETALLECOMPRASPROV.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLDETALLECOMPRASPROV.codfabrica', 'Field', 'DataType', "C(15)")
* Props for the VLDETALLECOMPRASPROV.codigo field.
DBSetProp('VLDETALLECOMPRASPROV.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLECOMPRASPROV.codigo', 'Field', 'UpdateName', 'detcom.codigo')
DBSetProp('VLDETALLECOMPRASPROV.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLDETALLECOMPRASPROV.nombre field.
DBSetProp('VLDETALLECOMPRASPROV.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLECOMPRASPROV.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLDETALLECOMPRASPROV.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLDETALLECOMPRASPROV.articulo field.
DBSetProp('VLDETALLECOMPRASPROV.articulo', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.articulo', 'Field', 'Updatable', .T.)
DBSetProp('VLDETALLECOMPRASPROV.articulo', 'Field', 'UpdateName', 'lista.articulo')
DBSetProp('VLDETALLECOMPRASPROV.articulo', 'Field', 'DataType', "N(4)")
* Props for the VLDETALLECOMPRASPROV.nomarticulo field.
DBSetProp('VLDETALLECOMPRASPROV.nomarticulo', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.nomarticulo', 'Field', 'Updatable', .T.)
DBSetProp('VLDETALLECOMPRASPROV.nomarticulo', 'Field', 'UpdateName', 'articulo.nombre')
DBSetProp('VLDETALLECOMPRASPROV.nomarticulo', 'Field', 'DataType', "C(30)")
* Props for the VLDETALLECOMPRASPROV.marca field.
DBSetProp('VLDETALLECOMPRASPROV.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.marca', 'Field', 'Updatable', .T.)
DBSetProp('VLDETALLECOMPRASPROV.marca', 'Field', 'UpdateName', 'lista.marca')
DBSetProp('VLDETALLECOMPRASPROV.marca', 'Field', 'DataType', "N(3)")
* Props for the VLDETALLECOMPRASPROV.nommarca field.
DBSetProp('VLDETALLECOMPRASPROV.nommarca', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.nommarca', 'Field', 'Updatable', .T.)
DBSetProp('VLDETALLECOMPRASPROV.nommarca', 'Field', 'UpdateName', 'marcas.nombre')
DBSetProp('VLDETALLECOMPRASPROV.nommarca', 'Field', 'DataType', "C(20)")
* Props for the VLDETALLECOMPRASPROV.cantidad field.
DBSetProp('VLDETALLECOMPRASPROV.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.cantidad', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLECOMPRASPROV.cantidad', 'Field', 'UpdateName', 'detcom.cantidad')
DBSetProp('VLDETALLECOMPRASPROV.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLDETALLECOMPRASPROV.precio field.
DBSetProp('VLDETALLECOMPRASPROV.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.precio', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLECOMPRASPROV.precio', 'Field', 'UpdateName', 'detcom.precio')
DBSetProp('VLDETALLECOMPRASPROV.precio', 'Field', 'DataType', "N(10,2)")
* Props for the VLDETALLECOMPRASPROV.total field.
DBSetProp('VLDETALLECOMPRASPROV.total', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.total', 'Field', 'Updatable', .F.)
DBSetProp('VLDETALLECOMPRASPROV.total', 'Field', 'UpdateName', 'detcom.total')
DBSetProp('VLDETALLECOMPRASPROV.total', 'Field', 'DataType', "N(10,2)")
* Props for the VLDETALLECOMPRASPROV.sucursal field.
DBSetProp('VLDETALLECOMPRASPROV.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLDETALLECOMPRASPROV.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLDETALLECOMPRASPROV.sucursal', 'Field', 'UpdateName', 'compras!compras.sucursal')
DBSetProp('VLDETALLECOMPRASPROV.sucursal', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLCOMISIONRECIBOS
***************** Ver la configuración para VLCOMISIONRECIBOS ***************

CREATE SQL VIEW "VLCOMISIONRECIBOS" ; 
   AS SELECT Recibos.compro, Recibos.letra, Recibos.numero, Facturas.fecha,  Facturas.cliente, Clientes.nombre, Facturas.total, Recibos.cobrado,  Codcomision.comision, Clientes.vendedor, Recibos.fecha AS fecrecibo,  Recibos.recibo, Recibos.cobrado*0 AS impcomision,  Facturas.comision AS tipocomis FROM recibos, facturas, clientes, codcomision WHERE Recibos.compro = Facturas.compro   AND Recibos.letra = Facturas.letra   AND Recibos.numero = Facturas.numero   AND Facturas.cliente = Clientes.codigo   AND Facturas.codcomis = Codcomision.codigo   AND (Recibos.fecha BETWEEN ?dDesde AND ?dHasta   AND Clientes.vendedor = ?nVendedor)

DBSetProp('VLCOMISIONRECIBOS', 'View', 'UpdateType', 1)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'WhereType', 3)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'FetchMemo', .T.)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'SendUpdates', .F.)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'UseMemoSize', 255)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'MaxRecords', -1)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'Tables', 'recibos,facturas,clientes,codcomision')
DBSetProp('VLCOMISIONRECIBOS', 'View', 'Prepared', .F.)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'CompareMemo', .T.)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'Comment', "")
DBSetProp('VLCOMISIONRECIBOS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLCOMISIONRECIBOS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLCOMISIONRECIBOS
* Props for the VLCOMISIONRECIBOS.compro field.
DBSetProp('VLCOMISIONRECIBOS.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.compro', 'Field', 'UpdateName', 'recibos.compro')
DBSetProp('VLCOMISIONRECIBOS.compro', 'Field', 'DataType', "C(2)")
* Props for the VLCOMISIONRECIBOS.letra field.
DBSetProp('VLCOMISIONRECIBOS.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.letra', 'Field', 'UpdateName', 'recibos.letra')
DBSetProp('VLCOMISIONRECIBOS.letra', 'Field', 'DataType', "C(1)")
* Props for the VLCOMISIONRECIBOS.numero field.
DBSetProp('VLCOMISIONRECIBOS.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.numero', 'Field', 'UpdateName', 'recibos.numero')
DBSetProp('VLCOMISIONRECIBOS.numero', 'Field', 'DataType', "N(12)")
* Props for the VLCOMISIONRECIBOS.fecha field.
DBSetProp('VLCOMISIONRECIBOS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLCOMISIONRECIBOS.fecha', 'Field', 'DataType', "D")
* Props for the VLCOMISIONRECIBOS.cliente field.
DBSetProp('VLCOMISIONRECIBOS.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLCOMISIONRECIBOS.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLCOMISIONRECIBOS.nombre field.
DBSetProp('VLCOMISIONRECIBOS.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLCOMISIONRECIBOS.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLCOMISIONRECIBOS.total field.
DBSetProp('VLCOMISIONRECIBOS.total', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.total', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.total', 'Field', 'UpdateName', 'facturas.total')
DBSetProp('VLCOMISIONRECIBOS.total', 'Field', 'DataType', "N(12,2)")
* Props for the VLCOMISIONRECIBOS.cobrado field.
DBSetProp('VLCOMISIONRECIBOS.cobrado', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.cobrado', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.cobrado', 'Field', 'UpdateName', 'recibos.cobrado')
DBSetProp('VLCOMISIONRECIBOS.cobrado', 'Field', 'DataType', "N(12,2)")
* Props for the VLCOMISIONRECIBOS.comision field.
DBSetProp('VLCOMISIONRECIBOS.comision', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.comision', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.comision', 'Field', 'UpdateName', 'codcomision.comision')
DBSetProp('VLCOMISIONRECIBOS.comision', 'Field', 'DataType', "N(6,2)")
* Props for the VLCOMISIONRECIBOS.vendedor field.
DBSetProp('VLCOMISIONRECIBOS.vendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.vendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.vendedor', 'Field', 'UpdateName', 'clientes.vendedor')
DBSetProp('VLCOMISIONRECIBOS.vendedor', 'Field', 'DataType', "N(3)")
* Props for the VLCOMISIONRECIBOS.fecrecibo field.
DBSetProp('VLCOMISIONRECIBOS.fecrecibo', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.fecrecibo', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONRECIBOS.fecrecibo', 'Field', 'UpdateName', 'recibos.fecha')
DBSetProp('VLCOMISIONRECIBOS.fecrecibo', 'Field', 'DataType', "D")
* Props for the VLCOMISIONRECIBOS.recibo field.
DBSetProp('VLCOMISIONRECIBOS.recibo', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.recibo', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.recibo', 'Field', 'UpdateName', 'recibos.recibo')
DBSetProp('VLCOMISIONRECIBOS.recibo', 'Field', 'DataType', "N(12)")
* Props for the VLCOMISIONRECIBOS.impcomision field.
DBSetProp('VLCOMISIONRECIBOS.impcomision', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.impcomision', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONRECIBOS.impcomision', 'Field', 'UpdateName', 'Recibos.recibo*')
DBSetProp('VLCOMISIONRECIBOS.impcomision', 'Field', 'DataType', "N(14,2)")
* Props for the VLCOMISIONRECIBOS.tipocomis field.
DBSetProp('VLCOMISIONRECIBOS.tipocomis', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONRECIBOS.tipocomis', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONRECIBOS.tipocomis', 'Field', 'UpdateName', 'facturas.comision')
DBSetProp('VLCOMISIONRECIBOS.tipocomis', 'Field', 'DataType', "C(1)")
ENDFUNC
 
FUNCTION MakeView_VLVENTASPROV
***************** Ver la configuración para VLVENTASPROV ***************

CREATE SQL VIEW "VLVENTASPROV" ; 
   AS SELECT Facturas.fecha, Localida.codprov, Localida.provincia,  SUM(Facturas.gravado*Codven.mult_ven) AS gravado,  SUM(Facturas.iva*Codven.mult_ven) AS iva,  SUM(Facturas.acrece*Codven.mult_ven) AS acrece,  SUM(Facturas.impint*Codven.mult_ven) AS impint,  SUM(Facturas.total*Codven.mult_ven) AS total FROM clientes, localida,   facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.cliente = Clientes.codigo   AND Clientes.codpostal = Localida.codigo   AND (MONTH(Facturas.fecha) = ?nMes   AND YEAR(Facturas.fecha) = ?nAnio   AND Codven.libroiva = .T.   AND Facturas.sucimp = ?nSucursal) GROUP BY Localida.codprov ORDER BY Localida.codprov

DBSetProp('VLVENTASPROV', 'View', 'UpdateType', 1)
DBSetProp('VLVENTASPROV', 'View', 'WhereType', 3)
DBSetProp('VLVENTASPROV', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTASPROV', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTASPROV', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTASPROV', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASPROV', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTASPROV', 'View', 'Tables', 'localida')
DBSetProp('VLVENTASPROV', 'View', 'Prepared', .F.)
DBSetProp('VLVENTASPROV', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTASPROV', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTASPROV', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASPROV', 'View', 'Comment', "")
DBSetProp('VLVENTASPROV', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTASPROV', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTASPROV
* Props for the VLVENTASPROV.fecha field.
DBSetProp('VLVENTASPROV.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASPROV.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASPROV.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTASPROV.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTASPROV.codprov field.
DBSetProp('VLVENTASPROV.codprov', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASPROV.codprov', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASPROV.codprov', 'Field', 'UpdateName', 'localida.codprov')
DBSetProp('VLVENTASPROV.codprov', 'Field', 'DataType', "C(1)")
* Props for the VLVENTASPROV.provincia field.
DBSetProp('VLVENTASPROV.provincia', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASPROV.provincia', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASPROV.provincia', 'Field', 'UpdateName', 'localida.provincia')
DBSetProp('VLVENTASPROV.provincia', 'Field', 'DataType', "C(20)")
* Props for the VLVENTASPROV.gravado field.
DBSetProp('VLVENTASPROV.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASPROV.gravado', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASPROV.gravado', 'Field', 'UpdateName', '')
DBSetProp('VLVENTASPROV.gravado', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTASPROV.iva field.
DBSetProp('VLVENTASPROV.iva', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASPROV.iva', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASPROV.iva', 'Field', 'UpdateName', '')
DBSetProp('VLVENTASPROV.iva', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTASPROV.acrece field.
DBSetProp('VLVENTASPROV.acrece', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASPROV.acrece', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASPROV.acrece', 'Field', 'UpdateName', '')
DBSetProp('VLVENTASPROV.acrece', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTASPROV.impint field.
DBSetProp('VLVENTASPROV.impint', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASPROV.impint', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASPROV.impint', 'Field', 'UpdateName', '')
DBSetProp('VLVENTASPROV.impint', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTASPROV.total field.
DBSetProp('VLVENTASPROV.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASPROV.total', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASPROV.total', 'Field', 'UpdateName', '')
DBSetProp('VLVENTASPROV.total', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLVENTASSITRIB
***************** Ver la configuración para VLVENTASSITRIB ***************

CREATE SQL VIEW "VLVENTASSITRIB" ; 
   AS SELECT Facturas.fecha, Clientes.sitiva,  SUM(Facturas.gravado*Codven.mult_ven) AS gravado,  SUM(Facturas.iva*Codven.mult_ven) AS iva,  SUM(Facturas.acrece*Codven.mult_ven) AS acrece,  SUM(Facturas.impint*Codven.mult_ven) AS impint,  SUM(Facturas.total*Codven.mult_ven) AS total FROM clientes,   facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.cliente = Clientes.codigo   AND (MONTH(Facturas.fecha) = ?nMes   AND YEAR(Facturas.fecha) = ?nAnio   AND Codven.libroiva = .T.   AND Facturas.sucimp = ?nSucursal) GROUP BY Clientes.sitiva

DBSetProp('VLVENTASSITRIB', 'View', 'UpdateType', 1)
DBSetProp('VLVENTASSITRIB', 'View', 'WhereType', 3)
DBSetProp('VLVENTASSITRIB', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTASSITRIB', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTASSITRIB', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTASSITRIB', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASSITRIB', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTASSITRIB', 'View', 'Tables', '')
DBSetProp('VLVENTASSITRIB', 'View', 'Prepared', .F.)
DBSetProp('VLVENTASSITRIB', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTASSITRIB', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTASSITRIB', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASSITRIB', 'View', 'Comment', "")
DBSetProp('VLVENTASSITRIB', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTASSITRIB', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTASSITRIB
* Props for the VLVENTASSITRIB.fecha field.
DBSetProp('VLVENTASSITRIB.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSITRIB.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASSITRIB.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTASSITRIB.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTASSITRIB.sitiva field.
DBSetProp('VLVENTASSITRIB.sitiva', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSITRIB.sitiva', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASSITRIB.sitiva', 'Field', 'UpdateName', 'clientes.sitiva')
DBSetProp('VLVENTASSITRIB.sitiva', 'Field', 'DataType', "C(3)")
* Props for the VLVENTASSITRIB.gravado field.
DBSetProp('VLVENTASSITRIB.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSITRIB.gravado', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASSITRIB.gravado', 'Field', 'UpdateName', 'Localida.provincia*')
DBSetProp('VLVENTASSITRIB.gravado', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTASSITRIB.iva field.
DBSetProp('VLVENTASSITRIB.iva', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSITRIB.iva', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASSITRIB.iva', 'Field', 'UpdateName', 'Localida.provincia**')
DBSetProp('VLVENTASSITRIB.iva', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTASSITRIB.acrece field.
DBSetProp('VLVENTASSITRIB.acrece', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSITRIB.acrece', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASSITRIB.acrece', 'Field', 'UpdateName', 'Localida.provincia***')
DBSetProp('VLVENTASSITRIB.acrece', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTASSITRIB.impint field.
DBSetProp('VLVENTASSITRIB.impint', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSITRIB.impint', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASSITRIB.impint', 'Field', 'UpdateName', 'Localida.provincia****')
DBSetProp('VLVENTASSITRIB.impint', 'Field', 'DataType', "N(16,2)")
* Props for the VLVENTASSITRIB.total field.
DBSetProp('VLVENTASSITRIB.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSITRIB.total', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASSITRIB.total', 'Field', 'UpdateName', 'Localida.provincia*****')
DBSetProp('VLVENTASSITRIB.total', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLVENTASRESUMENIB
***************** Ver la configuración para VLVENTASRESUMENIB ***************

CREATE SQL VIEW "VLVENTASRESUMENIB" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.fecha,  Clientes.nombre, Clientes.sitiva, Clientes.cuit,  Facturas.gravado*Codven.mult_ven AS gravado,  Facturas.iva*Codven.mult_ven AS iva,  Facturas.acrece*Codven.mult_ven AS acrece,  Facturas.impint*Codven.mult_ven AS impint,  Facturas.total*Codven.mult_ven AS total, Facturas.codimp,  Facturas.cliente,  IIF(ISNULL(Localida.codprov),"S",Localida.codprov) AS codprov FROM facturas, codven,   clientes LEFT OUTER JOIN localida    ON  Clientes.codpostal = Localida.codigo WHERE Facturas.cliente = Clientes.codigo   AND Facturas.compro = Codven.compro   AND (MONTH(Facturas.fecha) = ?nMes   AND YEAR(Facturas.fecha) = ?nAnio   AND Facturas.sucimp = ?nSucursal   AND Codven.libroiva = .T.)

DBSetProp('VLVENTASRESUMENIB', 'View', 'UpdateType', 1)
DBSetProp('VLVENTASRESUMENIB', 'View', 'WhereType', 3)
DBSetProp('VLVENTASRESUMENIB', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTASRESUMENIB', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTASRESUMENIB', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTASRESUMENIB', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASRESUMENIB', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTASRESUMENIB', 'View', 'Tables', 'facturas,clientes')
DBSetProp('VLVENTASRESUMENIB', 'View', 'Prepared', .F.)
DBSetProp('VLVENTASRESUMENIB', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTASRESUMENIB', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTASRESUMENIB', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASRESUMENIB', 'View', 'Comment', "")
DBSetProp('VLVENTASRESUMENIB', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTASRESUMENIB', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTASRESUMENIB
* Props for the VLVENTASRESUMENIB.compro field.
DBSetProp('VLVENTASRESUMENIB.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASRESUMENIB.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLVENTASRESUMENIB.compro', 'Field', 'DataType', "C(2)")
* Props for the VLVENTASRESUMENIB.letra field.
DBSetProp('VLVENTASRESUMENIB.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASRESUMENIB.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLVENTASRESUMENIB.letra', 'Field', 'DataType', "C(1)")
* Props for the VLVENTASRESUMENIB.numero field.
DBSetProp('VLVENTASRESUMENIB.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASRESUMENIB.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLVENTASRESUMENIB.numero', 'Field', 'DataType', "N(12)")
* Props for the VLVENTASRESUMENIB.fecha field.
DBSetProp('VLVENTASRESUMENIB.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASRESUMENIB.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTASRESUMENIB.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTASRESUMENIB.nombre field.
DBSetProp('VLVENTASRESUMENIB.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASRESUMENIB.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLVENTASRESUMENIB.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLVENTASRESUMENIB.sitiva field.
DBSetProp('VLVENTASRESUMENIB.sitiva', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.sitiva', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASRESUMENIB.sitiva', 'Field', 'UpdateName', 'clientes.sitiva')
DBSetProp('VLVENTASRESUMENIB.sitiva', 'Field', 'DataType', "C(3)")
* Props for the VLVENTASRESUMENIB.cuit field.
DBSetProp('VLVENTASRESUMENIB.cuit', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.cuit', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASRESUMENIB.cuit', 'Field', 'UpdateName', 'clientes.cuit')
DBSetProp('VLVENTASRESUMENIB.cuit', 'Field', 'DataType', "N(11)")
* Props for the VLVENTASRESUMENIB.gravado field.
DBSetProp('VLVENTASRESUMENIB.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.gravado', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASRESUMENIB.gravado', 'Field', 'UpdateName', 'facturas.gravado')
DBSetProp('VLVENTASRESUMENIB.gravado', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTASRESUMENIB.iva field.
DBSetProp('VLVENTASRESUMENIB.iva', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.iva', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASRESUMENIB.iva', 'Field', 'UpdateName', 'facturas.iva')
DBSetProp('VLVENTASRESUMENIB.iva', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTASRESUMENIB.acrece field.
DBSetProp('VLVENTASRESUMENIB.acrece', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.acrece', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASRESUMENIB.acrece', 'Field', 'UpdateName', 'facturas.acrece')
DBSetProp('VLVENTASRESUMENIB.acrece', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTASRESUMENIB.impint field.
DBSetProp('VLVENTASRESUMENIB.impint', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.impint', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASRESUMENIB.impint', 'Field', 'UpdateName', 'facturas.impint')
DBSetProp('VLVENTASRESUMENIB.impint', 'Field', 'DataType', "N(13,2)")
* Props for the VLVENTASRESUMENIB.total field.
DBSetProp('VLVENTASRESUMENIB.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.total', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASRESUMENIB.total', 'Field', 'UpdateName', 'facturas.total')
DBSetProp('VLVENTASRESUMENIB.total', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTASRESUMENIB.codimp field.
DBSetProp('VLVENTASRESUMENIB.codimp', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.codimp', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASRESUMENIB.codimp', 'Field', 'UpdateName', 'facturas.codimp')
DBSetProp('VLVENTASRESUMENIB.codimp', 'Field', 'DataType', "N(2)")
* Props for the VLVENTASRESUMENIB.cliente field.
DBSetProp('VLVENTASRESUMENIB.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASRESUMENIB.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLVENTASRESUMENIB.cliente', 'Field', 'DataType', "N(5)")
* Props for the VLVENTASRESUMENIB.codprov field.
DBSetProp('VLVENTASRESUMENIB.codprov', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASRESUMENIB.codprov', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTASRESUMENIB.codprov', 'Field', 'UpdateName', 'Facturas.cliente*')
DBSetProp('VLVENTASRESUMENIB.codprov', 'Field', 'DataType', "C(1)")
ENDFUNC
 
FUNCTION MakeView_VLMARKSERVICIOS
***************** Ver la configuración para VLMARKSERVICIOS ***************

CREATE SQL VIEW "VLMARKSERVICIOS" ; 
   AS SELECT Vehiculo.cliente, Clientes.nombre, Clientes.apeynom,  Clientes.domicilio, Clientes.codpostal, Clientes.telefono, Clientes.fax,  Clientes.movil, Vehiculo.marca, Vehiculo.modelo, Vehiculo.anio,  Vehiculo.patente, Vehiculo.kmxmes, Vehiculo.visita, Trabvehi.fecha,  Trabvehi.km, Trabvehi.proxfecha, Clientes.sucursal, Clientes.mail,  Clientes.mail2 FROM vehiculo, trabvehi, clientes WHERE Vehiculo.cliente = Clientes.codigo   AND Vehiculo.patente = Trabvehi.patente   AND (Trabvehi.proxfecha BETWEEN ?dDesde AND ?dHasta   AND Clientes.sucursal = ?nSucursal   AND Vehiculo.patente <> " ") GROUP BY Vehiculo.visita, Clientes.nombre

DBSetProp('VLMARKSERVICIOS', 'View', 'UpdateType', 1)
DBSetProp('VLMARKSERVICIOS', 'View', 'WhereType', 3)
DBSetProp('VLMARKSERVICIOS', 'View', 'FetchMemo', .T.)
DBSetProp('VLMARKSERVICIOS', 'View', 'SendUpdates', .F.)
DBSetProp('VLMARKSERVICIOS', 'View', 'UseMemoSize', 255)
DBSetProp('VLMARKSERVICIOS', 'View', 'FetchSize', 100)
DBSetProp('VLMARKSERVICIOS', 'View', 'MaxRecords', -1)
DBSetProp('VLMARKSERVICIOS', 'View', 'Tables', 'vehiculo,clientes,trabvehi')
DBSetProp('VLMARKSERVICIOS', 'View', 'Prepared', .F.)
DBSetProp('VLMARKSERVICIOS', 'View', 'CompareMemo', .T.)
DBSetProp('VLMARKSERVICIOS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLMARKSERVICIOS', 'View', 'FetchSize', 100)
DBSetProp('VLMARKSERVICIOS', 'View', 'Comment', "")
DBSetProp('VLMARKSERVICIOS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLMARKSERVICIOS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLMARKSERVICIOS
* Props for the VLMARKSERVICIOS.cliente field.
DBSetProp('VLMARKSERVICIOS.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.cliente', 'Field', 'UpdateName', 'vehiculo.cliente')
DBSetProp('VLMARKSERVICIOS.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLMARKSERVICIOS.nombre field.
DBSetProp('VLMARKSERVICIOS.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLMARKSERVICIOS.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLMARKSERVICIOS.apeynom field.
DBSetProp('VLMARKSERVICIOS.apeynom', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.apeynom', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.apeynom', 'Field', 'UpdateName', 'clientes.apeynom')
DBSetProp('VLMARKSERVICIOS.apeynom', 'Field', 'DataType', "C(50)")
* Props for the VLMARKSERVICIOS.domicilio field.
DBSetProp('VLMARKSERVICIOS.domicilio', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.domicilio', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.domicilio', 'Field', 'UpdateName', 'clientes.domicilio')
DBSetProp('VLMARKSERVICIOS.domicilio', 'Field', 'DataType', "C(30)")
* Props for the VLMARKSERVICIOS.codpostal field.
DBSetProp('VLMARKSERVICIOS.codpostal', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.codpostal', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.codpostal', 'Field', 'UpdateName', 'clientes.codpostal')
DBSetProp('VLMARKSERVICIOS.codpostal', 'Field', 'DataType', "C(5)")
* Props for the VLMARKSERVICIOS.telefono field.
DBSetProp('VLMARKSERVICIOS.telefono', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.telefono', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.telefono', 'Field', 'UpdateName', 'clientes.telefono')
DBSetProp('VLMARKSERVICIOS.telefono', 'Field', 'DataType', "C(15)")
* Props for the VLMARKSERVICIOS.fax field.
DBSetProp('VLMARKSERVICIOS.fax', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.fax', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.fax', 'Field', 'UpdateName', 'clientes.fax')
DBSetProp('VLMARKSERVICIOS.fax', 'Field', 'DataType', "C(15)")
* Props for the VLMARKSERVICIOS.movil field.
DBSetProp('VLMARKSERVICIOS.movil', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.movil', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.movil', 'Field', 'UpdateName', 'clientes.movil')
DBSetProp('VLMARKSERVICIOS.movil', 'Field', 'DataType', "C(15)")
* Props for the VLMARKSERVICIOS.marca field.
DBSetProp('VLMARKSERVICIOS.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.marca', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.marca', 'Field', 'UpdateName', 'vehiculo.marca')
DBSetProp('VLMARKSERVICIOS.marca', 'Field', 'DataType', "C(20)")
* Props for the VLMARKSERVICIOS.modelo field.
DBSetProp('VLMARKSERVICIOS.modelo', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.modelo', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.modelo', 'Field', 'UpdateName', 'vehiculo.modelo')
DBSetProp('VLMARKSERVICIOS.modelo', 'Field', 'DataType', "C(20)")
* Props for the VLMARKSERVICIOS.anio field.
DBSetProp('VLMARKSERVICIOS.anio', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.anio', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.anio', 'Field', 'UpdateName', 'vehiculo.anio')
DBSetProp('VLMARKSERVICIOS.anio', 'Field', 'DataType', "N(4)")
* Props for the VLMARKSERVICIOS.patente field.
DBSetProp('VLMARKSERVICIOS.patente', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.patente', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.patente', 'Field', 'UpdateName', 'vehiculo.patente')
DBSetProp('VLMARKSERVICIOS.patente', 'Field', 'DataType', "C(6)")
* Props for the VLMARKSERVICIOS.kmxmes field.
DBSetProp('VLMARKSERVICIOS.kmxmes', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.kmxmes', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.kmxmes', 'Field', 'UpdateName', 'vehiculo.kmxmes')
DBSetProp('VLMARKSERVICIOS.kmxmes', 'Field', 'DataType', "N(5)")
* Props for the VLMARKSERVICIOS.visita field.
DBSetProp('VLMARKSERVICIOS.visita', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.visita', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.visita', 'Field', 'UpdateName', 'vehiculo.visita')
DBSetProp('VLMARKSERVICIOS.visita', 'Field', 'DataType', "D")
* Props for the VLMARKSERVICIOS.fecha field.
DBSetProp('VLMARKSERVICIOS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.fecha', 'Field', 'UpdateName', 'trabvehi.fecha')
DBSetProp('VLMARKSERVICIOS.fecha', 'Field', 'DataType', "D")
* Props for the VLMARKSERVICIOS.km field.
DBSetProp('VLMARKSERVICIOS.km', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.km', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.km', 'Field', 'UpdateName', 'trabvehi.km')
DBSetProp('VLMARKSERVICIOS.km', 'Field', 'DataType', "N(7)")
* Props for the VLMARKSERVICIOS.proxfecha field.
DBSetProp('VLMARKSERVICIOS.proxfecha', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.proxfecha', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.proxfecha', 'Field', 'UpdateName', 'trabvehi.proxfecha')
DBSetProp('VLMARKSERVICIOS.proxfecha', 'Field', 'DataType', "D")
* Props for the VLMARKSERVICIOS.sucursal field.
DBSetProp('VLMARKSERVICIOS.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.sucursal', 'Field', 'UpdateName', 'clientes.sucursal')
DBSetProp('VLMARKSERVICIOS.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLMARKSERVICIOS.mail field.
DBSetProp('VLMARKSERVICIOS.mail', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.mail', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.mail', 'Field', 'UpdateName', 'clientes.mail')
DBSetProp('VLMARKSERVICIOS.mail', 'Field', 'DataType', "C(50)")
* Props for the VLMARKSERVICIOS.mail2 field.
DBSetProp('VLMARKSERVICIOS.mail2', 'Field', 'KeyField', .F.)
DBSetProp('VLMARKSERVICIOS.mail2', 'Field', 'Updatable', .T.)
DBSetProp('VLMARKSERVICIOS.mail2', 'Field', 'UpdateName', 'clientes.mail2')
DBSetProp('VLMARKSERVICIOS.mail2', 'Field', 'DataType', "C(50)")
ENDFUNC
 
FUNCTION MakeView_VLVENTASSINESTADISTICAS
***************** Ver la configuración para VLVENTASSINESTADISTICAS ***************

CREATE SQL VIEW "VLVENTASSINESTADISTICAS" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.fecha,  Facturas.cliente, Clientes.nombre, Facturas.condicion, Facturas.total,  Facturas.sucursal, Clientes.vendedor, Clientes.subcuenta FROM facturas, clientes WHERE Facturas.cliente = Clientes.codigo   AND (Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Facturas.noestadist = .T.) ORDER BY Facturas.cliente

DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'UpdateType', 1)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'WhereType', 3)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'Tables', 'facturas,clientes')
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'Prepared', .F.)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'FetchSize', 100)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'Comment', "")
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTASSINESTADISTICAS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTASSINESTADISTICAS
* Props for the VLVENTASSINESTADISTICAS.compro field.
DBSetProp('VLVENTASSINESTADISTICAS.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLVENTASSINESTADISTICAS.compro', 'Field', 'DataType', "C(2)")
* Props for the VLVENTASSINESTADISTICAS.letra field.
DBSetProp('VLVENTASSINESTADISTICAS.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLVENTASSINESTADISTICAS.letra', 'Field', 'DataType', "C(1)")
* Props for the VLVENTASSINESTADISTICAS.numero field.
DBSetProp('VLVENTASSINESTADISTICAS.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLVENTASSINESTADISTICAS.numero', 'Field', 'DataType', "N(12)")
* Props for the VLVENTASSINESTADISTICAS.fecha field.
DBSetProp('VLVENTASSINESTADISTICAS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTASSINESTADISTICAS.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTASSINESTADISTICAS.cliente field.
DBSetProp('VLVENTASSINESTADISTICAS.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLVENTASSINESTADISTICAS.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLVENTASSINESTADISTICAS.nombre field.
DBSetProp('VLVENTASSINESTADISTICAS.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLVENTASSINESTADISTICAS.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLVENTASSINESTADISTICAS.condicion field.
DBSetProp('VLVENTASSINESTADISTICAS.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.condicion', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.condicion', 'Field', 'UpdateName', 'facturas.condicion')
DBSetProp('VLVENTASSINESTADISTICAS.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLVENTASSINESTADISTICAS.total field.
DBSetProp('VLVENTASSINESTADISTICAS.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.total', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.total', 'Field', 'UpdateName', 'facturas.total')
DBSetProp('VLVENTASSINESTADISTICAS.total', 'Field', 'DataType', "N(12,2)")
* Props for the VLVENTASSINESTADISTICAS.sucursal field.
DBSetProp('VLVENTASSINESTADISTICAS.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLVENTASSINESTADISTICAS.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLVENTASSINESTADISTICAS.vendedor field.
DBSetProp('VLVENTASSINESTADISTICAS.vendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.vendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.vendedor', 'Field', 'UpdateName', 'clientes.vendedor')
DBSetProp('VLVENTASSINESTADISTICAS.vendedor', 'Field', 'DataType', "N(3)")
* Props for the VLVENTASSINESTADISTICAS.subcuenta field.
DBSetProp('VLVENTASSINESTADISTICAS.subcuenta', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTASSINESTADISTICAS.subcuenta', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTASSINESTADISTICAS.subcuenta', 'Field', 'UpdateName', 'clientes.subcuenta')
DBSetProp('VLVENTASSINESTADISTICAS.subcuenta', 'Field', 'DataType', "N(6)")
ENDFUNC
 
FUNCTION MakeView_VLCOBRANZAVENDEDORDETALLADA
***************** Ver la configuración para VLCOBRANZAVENDEDORDETALLADA ***************

CREATE SQL VIEW "VLCOBRANZAVENDEDORDETALLADA" ; 
   AS SELECT Recibos.recibo, Recibos.fecha, Recibos.compro, Recibos.letra,  Recibos.numero, Facturas.cliente, Clientes.nombre AS nomcliente,  Facturas.fecha AS fecfactura, Lista.nombre, Detven.cantidad,  Detven.precio, Detven.total, Recibos.cobrado FROM recibos, facturas, detven, lista, clientes WHERE Recibos.compro = Facturas.compro   AND Recibos.letra = Facturas.letra   AND Recibos.numero = Facturas.numero   AND Recibos.compro = Detven.compro   AND Recibos.letra = Detven.letra   AND Recibos.numero = Detven.numero   AND Detven.codigo = Lista.codigo   AND Facturas.cliente = Clientes.codigo   AND (Recibos.fecha BETWEEN ?dDesde AND ?dHasta   AND Clientes.vendedor = ?nVendedor) ORDER BY Recibos.recibo, Recibos.numero

DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'UpdateType', 1)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'WhereType', 3)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'FetchMemo', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'SendUpdates', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'UseMemoSize', 255)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'FetchSize', 100)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'MaxRecords', -1)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'Tables', 'recibos,facturas,clientes,lista,detven')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'Prepared', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'CompareMemo', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'FetchSize', 100)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'Comment', "")
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLCOBRANZAVENDEDORDETALLADA
* Props for the VLCOBRANZAVENDEDORDETALLADA.recibo field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.recibo', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.recibo', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.recibo', 'Field', 'UpdateName', 'recibos.recibo')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.recibo', 'Field', 'DataType', "N(12)")
* Props for the VLCOBRANZAVENDEDORDETALLADA.fecha field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.fecha', 'Field', 'UpdateName', 'recibos.fecha')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.fecha', 'Field', 'DataType', "D")
* Props for the VLCOBRANZAVENDEDORDETALLADA.compro field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.compro', 'Field', 'UpdateName', 'recibos.compro')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.compro', 'Field', 'DataType', "C(2)")
* Props for the VLCOBRANZAVENDEDORDETALLADA.letra field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.letra', 'Field', 'UpdateName', 'recibos.letra')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.letra', 'Field', 'DataType', "C(1)")
* Props for the VLCOBRANZAVENDEDORDETALLADA.numero field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.numero', 'Field', 'UpdateName', 'recibos.numero')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.numero', 'Field', 'DataType', "N(12)")
* Props for the VLCOBRANZAVENDEDORDETALLADA.cliente field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cliente', 'Field', 'DataType', "N(5)")
* Props for the VLCOBRANZAVENDEDORDETALLADA.nomcliente field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.nomcliente', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.nomcliente', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.nomcliente', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.nomcliente', 'Field', 'DataType', "C(30)")
* Props for the VLCOBRANZAVENDEDORDETALLADA.fecfactura field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.fecfactura', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.fecfactura', 'Field', 'Updatable', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.fecfactura', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.fecfactura', 'Field', 'DataType', "D")
* Props for the VLCOBRANZAVENDEDORDETALLADA.nombre field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLCOBRANZAVENDEDORDETALLADA.cantidad field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cantidad', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLCOBRANZAVENDEDORDETALLADA.precio field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.precio', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.precio', 'Field', 'DataType', "N(10,2)")
* Props for the VLCOBRANZAVENDEDORDETALLADA.total field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.total', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.total', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.total', 'Field', 'UpdateName', 'detven.total')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.total', 'Field', 'DataType', "N(10,2)")
* Props for the VLCOBRANZAVENDEDORDETALLADA.cobrado field.
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cobrado', 'Field', 'KeyField', .F.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cobrado', 'Field', 'Updatable', .T.)
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cobrado', 'Field', 'UpdateName', 'recibos.cobrado')
DBSetProp('VLCOBRANZAVENDEDORDETALLADA.cobrado', 'Field', 'DataType', "N(12,2)")
ENDFUNC
 
FUNCTION MakeView_VLCOMPRASIMPUTACION
***************** Ver la configuración para VLCOMPRASIMPUTACION ***************

CREATE SQL VIEW "VLCOMPRASIMPUTACION" ; 
   AS SELECT Compras.imputacion, Codimp.nombre,  SUM((Compras.gravado+Compras.nogravado+Compras.monotrib)*Codcom.mult_com) AS neto,  SUM(Compras.iva*Codcom.mult_com) AS iva,  SUM(Compras.total*Codcom.mult_com) AS total FROM compras, codcom, codimp WHERE Compras.compro = Codcom.codigo   AND Compras.imputacion = Codimp.codigo   AND (Codcom.libroiva = .T.   AND month( Compras.fecha) = ?nMes   AND YEAR( Compras.fecha) = ?nAnio) GROUP BY Compras.imputacion ORDER BY Compras.imputacion

DBSetProp('VLCOMPRASIMPUTACION', 'View', 'UpdateType', 1)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'WhereType', 3)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'FetchMemo', .T.)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'SendUpdates', .F.)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'UseMemoSize', 255)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'FetchSize', 100)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'MaxRecords', -1)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'Tables', 'compras,codimp')
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'Prepared', .F.)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'CompareMemo', .T.)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'FetchSize', 100)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'Comment', "")
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLCOMPRASIMPUTACION', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLCOMPRASIMPUTACION
* Props for the VLCOMPRASIMPUTACION.imputacion field.
DBSetProp('VLCOMPRASIMPUTACION.imputacion', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMPRASIMPUTACION.imputacion', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMPRASIMPUTACION.imputacion', 'Field', 'UpdateName', 'compras.imputacion')
DBSetProp('VLCOMPRASIMPUTACION.imputacion', 'Field', 'DataType', "N(2)")
* Props for the VLCOMPRASIMPUTACION.nombre field.
DBSetProp('VLCOMPRASIMPUTACION.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMPRASIMPUTACION.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMPRASIMPUTACION.nombre', 'Field', 'UpdateName', 'codimp.nombre')
DBSetProp('VLCOMPRASIMPUTACION.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLCOMPRASIMPUTACION.neto field.
DBSetProp('VLCOMPRASIMPUTACION.neto', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMPRASIMPUTACION.neto', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMPRASIMPUTACION.neto', 'Field', 'UpdateName', 'Codimp.nombre*')
DBSetProp('VLCOMPRASIMPUTACION.neto', 'Field', 'DataType', "N(16,2)")
* Props for the VLCOMPRASIMPUTACION.iva field.
DBSetProp('VLCOMPRASIMPUTACION.iva', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMPRASIMPUTACION.iva', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMPRASIMPUTACION.iva', 'Field', 'UpdateName', 'Codimp.nombre**')
DBSetProp('VLCOMPRASIMPUTACION.iva', 'Field', 'DataType', "N(16,2)")
* Props for the VLCOMPRASIMPUTACION.total field.
DBSetProp('VLCOMPRASIMPUTACION.total', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMPRASIMPUTACION.total', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMPRASIMPUTACION.total', 'Field', 'UpdateName', 'Codimp.nombre***')
DBSetProp('VLCOMPRASIMPUTACION.total', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLPRECIODIFERENTE
***************** Ver la configuración para VLPRECIODIFERENTE ***************

CREATE SQL VIEW "VLPRECIODIFERENTE" ; 
   AS SELECT Detven.compro, Detven.letra, Detven.numero, Detven.codigo,  Lista.nombre, Detven.cantidad, Detven.precio AS pfacturado,  Facturas.fecha, Facturas.cliente, Lista.precio AS plista,  Detven.descuento,  ROUND(Lista.precio*Lista.descuento/100,2) AS adicional,  Clientes.vendedor, Lista.marca, Lista.articulo FROM detven, facturas, lista, clientes WHERE Detven.id = Facturas.id   AND Detven.codigo = Lista.codigo   AND Facturas.cliente = Clientes.codigo   AND (Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Clientes.vendedor BETWEEN ?nDesde AND ?nHasta   AND Facturas.noestadist = .F.) ORDER BY Clientes.vendedor, Facturas.fecha

DBSetProp('VLPRECIODIFERENTE', 'View', 'UpdateType', 1)
DBSetProp('VLPRECIODIFERENTE', 'View', 'WhereType', 3)
DBSetProp('VLPRECIODIFERENTE', 'View', 'FetchMemo', .T.)
DBSetProp('VLPRECIODIFERENTE', 'View', 'SendUpdates', .F.)
DBSetProp('VLPRECIODIFERENTE', 'View', 'UseMemoSize', 255)
DBSetProp('VLPRECIODIFERENTE', 'View', 'FetchSize', 100)
DBSetProp('VLPRECIODIFERENTE', 'View', 'MaxRecords', -1)
DBSetProp('VLPRECIODIFERENTE', 'View', 'Tables', 'detven,lista,facturas,clientes')
DBSetProp('VLPRECIODIFERENTE', 'View', 'Prepared', .F.)
DBSetProp('VLPRECIODIFERENTE', 'View', 'CompareMemo', .T.)
DBSetProp('VLPRECIODIFERENTE', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLPRECIODIFERENTE', 'View', 'FetchSize', 100)
DBSetProp('VLPRECIODIFERENTE', 'View', 'Comment', "")
DBSetProp('VLPRECIODIFERENTE', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLPRECIODIFERENTE', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLPRECIODIFERENTE
* Props for the VLPRECIODIFERENTE.compro field.
DBSetProp('VLPRECIODIFERENTE.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLPRECIODIFERENTE.compro', 'Field', 'DataType', "C(2)")
* Props for the VLPRECIODIFERENTE.letra field.
DBSetProp('VLPRECIODIFERENTE.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLPRECIODIFERENTE.letra', 'Field', 'DataType', "C(1)")
* Props for the VLPRECIODIFERENTE.numero field.
DBSetProp('VLPRECIODIFERENTE.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLPRECIODIFERENTE.numero', 'Field', 'DataType', "N(12)")
* Props for the VLPRECIODIFERENTE.codigo field.
DBSetProp('VLPRECIODIFERENTE.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLPRECIODIFERENTE.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLPRECIODIFERENTE.nombre field.
DBSetProp('VLPRECIODIFERENTE.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLPRECIODIFERENTE.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLPRECIODIFERENTE.cantidad field.
DBSetProp('VLPRECIODIFERENTE.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.cantidad', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLPRECIODIFERENTE.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLPRECIODIFERENTE.pfacturado field.
DBSetProp('VLPRECIODIFERENTE.pfacturado', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.pfacturado', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIODIFERENTE.pfacturado', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLPRECIODIFERENTE.pfacturado', 'Field', 'DataType', "N(12,2)")
* Props for the VLPRECIODIFERENTE.fecha field.
DBSetProp('VLPRECIODIFERENTE.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLPRECIODIFERENTE.fecha', 'Field', 'DataType', "D")
* Props for the VLPRECIODIFERENTE.cliente field.
DBSetProp('VLPRECIODIFERENTE.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLPRECIODIFERENTE.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLPRECIODIFERENTE.plista field.
DBSetProp('VLPRECIODIFERENTE.plista', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.plista', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIODIFERENTE.plista', 'Field', 'UpdateName', 'lista.precio')
DBSetProp('VLPRECIODIFERENTE.plista', 'Field', 'DataType', "N(12,2)")
* Props for the VLPRECIODIFERENTE.descuento field.
DBSetProp('VLPRECIODIFERENTE.descuento', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.descuento', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.descuento', 'Field', 'UpdateName', 'detven.descuento')
DBSetProp('VLPRECIODIFERENTE.descuento', 'Field', 'DataType', "N(6,2)")
* Props for the VLPRECIODIFERENTE.adicional field.
DBSetProp('VLPRECIODIFERENTE.adicional', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.adicional', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIODIFERENTE.adicional', 'Field', 'UpdateName', 'Lista.precio*')
DBSetProp('VLPRECIODIFERENTE.adicional', 'Field', 'DataType', "N(20,2)")
* Props for the VLPRECIODIFERENTE.vendedor field.
DBSetProp('VLPRECIODIFERENTE.vendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.vendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.vendedor', 'Field', 'UpdateName', 'clientes.vendedor')
DBSetProp('VLPRECIODIFERENTE.vendedor', 'Field', 'DataType', "N(3)")
* Props for the VLPRECIODIFERENTE.marca field.
DBSetProp('VLPRECIODIFERENTE.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.marca', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.marca', 'Field', 'UpdateName', 'lista.marca')
DBSetProp('VLPRECIODIFERENTE.marca', 'Field', 'DataType', "N(3)")
* Props for the VLPRECIODIFERENTE.articulo field.
DBSetProp('VLPRECIODIFERENTE.articulo', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIODIFERENTE.articulo', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIODIFERENTE.articulo', 'Field', 'UpdateName', 'lista.articulo')
DBSetProp('VLPRECIODIFERENTE.articulo', 'Field', 'DataType', "N(4)")
ENDFUNC
 
FUNCTION MakeView_VLVENTAMOSTRADOR
***************** Ver la configuración para VLVENTAMOSTRADOR ***************

CREATE SQL VIEW "VLVENTAMOSTRADOR" ; 
   AS SELECT Detven.compro, Detven.letra, Detven.numero, Facturas.fecha,  Facturas.cliente, Clientes.nombre, Detven.reventa, Lista.tipo,  Detven.codigo, Lista.nombre AS producto, Detven.cantidad, Detven.precio,  Detven.total*Codven.mult_ven AS total, Facturas.sucursal,  Clientes.domicilio, Clientes.codpostal, Clientes.barrio,  Clientes.caractel, Clientes.telefono, Clientes.movil, Clientes.mail,  Clientes.mayorista FROM facturas, codven, clientes,   detven INNER JOIN lista    ON  Detven.codigo = Lista.codigo WHERE Detven.id = Facturas.id   AND Facturas.cliente = Clientes.codigo   AND Detven.compro = Codven.compro   AND (Codven.mult_ven <> 0   AND Facturas.noestadist <> .T.   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta) ORDER BY Facturas.fecha, Detven.numero

DBSetProp('VLVENTAMOSTRADOR', 'View', 'UpdateType', 1)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'WhereType', 3)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'FetchSize', 100)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'Tables', 'detven,facturas,clientes,lista')
DBSetProp('VLVENTAMOSTRADOR', 'View', 'Prepared', .F.)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'FetchSize', 100)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'Comment', "")
DBSetProp('VLVENTAMOSTRADOR', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTAMOSTRADOR', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTAMOSTRADOR
* Props for the VLVENTAMOSTRADOR.compro field.
DBSetProp('VLVENTAMOSTRADOR.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLVENTAMOSTRADOR.compro', 'Field', 'DataType', "C(2)")
* Props for the VLVENTAMOSTRADOR.letra field.
DBSetProp('VLVENTAMOSTRADOR.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLVENTAMOSTRADOR.letra', 'Field', 'DataType', "C(1)")
* Props for the VLVENTAMOSTRADOR.numero field.
DBSetProp('VLVENTAMOSTRADOR.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLVENTAMOSTRADOR.numero', 'Field', 'DataType', "N(12)")
* Props for the VLVENTAMOSTRADOR.fecha field.
DBSetProp('VLVENTAMOSTRADOR.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTAMOSTRADOR.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTAMOSTRADOR.cliente field.
DBSetProp('VLVENTAMOSTRADOR.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLVENTAMOSTRADOR.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLVENTAMOSTRADOR.nombre field.
DBSetProp('VLVENTAMOSTRADOR.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLVENTAMOSTRADOR.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLVENTAMOSTRADOR.reventa field.
DBSetProp('VLVENTAMOSTRADOR.reventa', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.reventa', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.reventa', 'Field', 'UpdateName', 'detven.reventa')
DBSetProp('VLVENTAMOSTRADOR.reventa', 'Field', 'DataType', "C(1)")
* Props for the VLVENTAMOSTRADOR.tipo field.
DBSetProp('VLVENTAMOSTRADOR.tipo', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.tipo', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.tipo', 'Field', 'UpdateName', 'lista.tipo')
DBSetProp('VLVENTAMOSTRADOR.tipo', 'Field', 'DataType', "C(1)")
* Props for the VLVENTAMOSTRADOR.codigo field.
DBSetProp('VLVENTAMOSTRADOR.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLVENTAMOSTRADOR.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLVENTAMOSTRADOR.producto field.
DBSetProp('VLVENTAMOSTRADOR.producto', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.producto', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTAMOSTRADOR.producto', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLVENTAMOSTRADOR.producto', 'Field', 'DataType', "C(50)")
* Props for the VLVENTAMOSTRADOR.cantidad field.
DBSetProp('VLVENTAMOSTRADOR.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.cantidad', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLVENTAMOSTRADOR.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLVENTAMOSTRADOR.precio field.
DBSetProp('VLVENTAMOSTRADOR.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.precio', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLVENTAMOSTRADOR.precio', 'Field', 'DataType', "N(12,2)")
* Props for the VLVENTAMOSTRADOR.total field.
DBSetProp('VLVENTAMOSTRADOR.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.total', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTAMOSTRADOR.total', 'Field', 'UpdateName', 'Detven.precio*')
DBSetProp('VLVENTAMOSTRADOR.total', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTAMOSTRADOR.sucursal field.
DBSetProp('VLVENTAMOSTRADOR.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLVENTAMOSTRADOR.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLVENTAMOSTRADOR.domicilio field.
DBSetProp('VLVENTAMOSTRADOR.domicilio', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.domicilio', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.domicilio', 'Field', 'UpdateName', 'clientes.domicilio')
DBSetProp('VLVENTAMOSTRADOR.domicilio', 'Field', 'DataType', "C(30)")
* Props for the VLVENTAMOSTRADOR.codpostal field.
DBSetProp('VLVENTAMOSTRADOR.codpostal', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.codpostal', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.codpostal', 'Field', 'UpdateName', 'clientes.codpostal')
DBSetProp('VLVENTAMOSTRADOR.codpostal', 'Field', 'DataType', "C(5)")
* Props for the VLVENTAMOSTRADOR.barrio field.
DBSetProp('VLVENTAMOSTRADOR.barrio', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.barrio', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.barrio', 'Field', 'UpdateName', 'clientes.barrio')
DBSetProp('VLVENTAMOSTRADOR.barrio', 'Field', 'DataType', "C(30)")
* Props for the VLVENTAMOSTRADOR.caractel field.
DBSetProp('VLVENTAMOSTRADOR.caractel', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.caractel', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.caractel', 'Field', 'UpdateName', 'clientes.caractel')
DBSetProp('VLVENTAMOSTRADOR.caractel', 'Field', 'DataType', "C(5)")
* Props for the VLVENTAMOSTRADOR.telefono field.
DBSetProp('VLVENTAMOSTRADOR.telefono', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.telefono', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.telefono', 'Field', 'UpdateName', 'clientes.telefono')
DBSetProp('VLVENTAMOSTRADOR.telefono', 'Field', 'DataType', "C(15)")
* Props for the VLVENTAMOSTRADOR.movil field.
DBSetProp('VLVENTAMOSTRADOR.movil', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.movil', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.movil', 'Field', 'UpdateName', 'clientes.movil')
DBSetProp('VLVENTAMOSTRADOR.movil', 'Field', 'DataType', "C(15)")
* Props for the VLVENTAMOSTRADOR.mail field.
DBSetProp('VLVENTAMOSTRADOR.mail', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.mail', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.mail', 'Field', 'UpdateName', 'clientes.mail')
DBSetProp('VLVENTAMOSTRADOR.mail', 'Field', 'DataType', "C(50)")
* Props for the VLVENTAMOSTRADOR.mayorista field.
DBSetProp('VLVENTAMOSTRADOR.mayorista', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTAMOSTRADOR.mayorista', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTAMOSTRADOR.mayorista', 'Field', 'UpdateName', 'clientes.mayorista')
DBSetProp('VLVENTAMOSTRADOR.mayorista', 'Field', 'DataType', "L")
ENDFUNC
 
FUNCTION MakeView_VLHORARIOS
***************** Ver la configuración para VLHORARIOS ***************

CREATE SQL VIEW "VLHORARIOS" ; 
   AS SELECT * FROM horarios WHERE Horarios.fecha BETWEEN ?dDesde AND ?dHasta ORDER BY Horarios.empleado

DBSetProp('VLHORARIOS', 'View', 'UpdateType', 1)
DBSetProp('VLHORARIOS', 'View', 'WhereType', 3)
DBSetProp('VLHORARIOS', 'View', 'FetchMemo', .T.)
DBSetProp('VLHORARIOS', 'View', 'SendUpdates', .F.)
DBSetProp('VLHORARIOS', 'View', 'UseMemoSize', 255)
DBSetProp('VLHORARIOS', 'View', 'FetchSize', 100)
DBSetProp('VLHORARIOS', 'View', 'MaxRecords', -1)
DBSetProp('VLHORARIOS', 'View', 'Tables', 'horarios')
DBSetProp('VLHORARIOS', 'View', 'Prepared', .F.)
DBSetProp('VLHORARIOS', 'View', 'CompareMemo', .T.)
DBSetProp('VLHORARIOS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLHORARIOS', 'View', 'FetchSize', 100)
DBSetProp('VLHORARIOS', 'View', 'Comment', "")
DBSetProp('VLHORARIOS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLHORARIOS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLHORARIOS
* Props for the VLHORARIOS.empleado field.
DBSetProp('VLHORARIOS.empleado', 'Field', 'KeyField', .F.)
DBSetProp('VLHORARIOS.empleado', 'Field', 'Updatable', .T.)
DBSetProp('VLHORARIOS.empleado', 'Field', 'UpdateName', 'horarios.empleado')
DBSetProp('VLHORARIOS.empleado', 'Field', 'DataType', "C(2)")
* Props for the VLHORARIOS.fecha field.
DBSetProp('VLHORARIOS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLHORARIOS.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLHORARIOS.fecha', 'Field', 'UpdateName', 'horarios.fecha')
DBSetProp('VLHORARIOS.fecha', 'Field', 'DataType', "D")
* Props for the VLHORARIOS.hsentrada field.
DBSetProp('VLHORARIOS.hsentrada', 'Field', 'KeyField', .F.)
DBSetProp('VLHORARIOS.hsentrada', 'Field', 'Updatable', .T.)
DBSetProp('VLHORARIOS.hsentrada', 'Field', 'UpdateName', 'horarios.hsentrada')
DBSetProp('VLHORARIOS.hsentrada', 'Field', 'DataType', "N(2)")
* Props for the VLHORARIOS.minentrada field.
DBSetProp('VLHORARIOS.minentrada', 'Field', 'KeyField', .F.)
DBSetProp('VLHORARIOS.minentrada', 'Field', 'Updatable', .T.)
DBSetProp('VLHORARIOS.minentrada', 'Field', 'UpdateName', 'horarios.minentrada')
DBSetProp('VLHORARIOS.minentrada', 'Field', 'DataType', "N(2)")
* Props for the VLHORARIOS.hssalida field.
DBSetProp('VLHORARIOS.hssalida', 'Field', 'KeyField', .F.)
DBSetProp('VLHORARIOS.hssalida', 'Field', 'Updatable', .T.)
DBSetProp('VLHORARIOS.hssalida', 'Field', 'UpdateName', 'horarios.hssalida')
DBSetProp('VLHORARIOS.hssalida', 'Field', 'DataType', "N(2)")
* Props for the VLHORARIOS.minsalida field.
DBSetProp('VLHORARIOS.minsalida', 'Field', 'KeyField', .F.)
DBSetProp('VLHORARIOS.minsalida', 'Field', 'Updatable', .T.)
DBSetProp('VLHORARIOS.minsalida', 'Field', 'UpdateName', 'horarios.minsalida')
DBSetProp('VLHORARIOS.minsalida', 'Field', 'DataType', "N(2)")
* Props for the VLHORARIOS.hsent field.
DBSetProp('VLHORARIOS.hsent', 'Field', 'KeyField', .F.)
DBSetProp('VLHORARIOS.hsent', 'Field', 'Updatable', .T.)
DBSetProp('VLHORARIOS.hsent', 'Field', 'UpdateName', 'horarios.hsent')
DBSetProp('VLHORARIOS.hsent', 'Field', 'DataType', "N(2)")
* Props for the VLHORARIOS.minent field.
DBSetProp('VLHORARIOS.minent', 'Field', 'KeyField', .F.)
DBSetProp('VLHORARIOS.minent', 'Field', 'Updatable', .T.)
DBSetProp('VLHORARIOS.minent', 'Field', 'UpdateName', 'horarios.minent')
DBSetProp('VLHORARIOS.minent', 'Field', 'DataType', "N(2)")
* Props for the VLHORARIOS.hssalt field.
DBSetProp('VLHORARIOS.hssalt', 'Field', 'KeyField', .F.)
DBSetProp('VLHORARIOS.hssalt', 'Field', 'Updatable', .T.)
DBSetProp('VLHORARIOS.hssalt', 'Field', 'UpdateName', 'horarios.hssalt')
DBSetProp('VLHORARIOS.hssalt', 'Field', 'DataType', "N(2)")
* Props for the VLHORARIOS.minsalt field.
DBSetProp('VLHORARIOS.minsalt', 'Field', 'KeyField', .F.)
DBSetProp('VLHORARIOS.minsalt', 'Field', 'Updatable', .T.)
DBSetProp('VLHORARIOS.minsalt', 'Field', 'UpdateName', 'horarios.minsalt')
DBSetProp('VLHORARIOS.minsalt', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLMERCACABECERA
***************** Ver la configuración para VLMERCACABECERA ***************

CREATE SQL VIEW "VLMERCACABECERA" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.remito,  Facturas.fecha, Facturas.condicion, Facturas.total, Facturas.entrega,  Facturas.estado, Facturas.marca, Facturas.operador, Facturas.codcomis,  Facturas.noestadist FROM facturas WHERE Facturas.cliente = ?nCliente ORDER BY Facturas.fecha

DBSetProp('VLMERCACABECERA', 'View', 'UpdateType', 1)
DBSetProp('VLMERCACABECERA', 'View', 'WhereType', 3)
DBSetProp('VLMERCACABECERA', 'View', 'FetchMemo', .T.)
DBSetProp('VLMERCACABECERA', 'View', 'SendUpdates', .F.)
DBSetProp('VLMERCACABECERA', 'View', 'UseMemoSize', 255)
DBSetProp('VLMERCACABECERA', 'View', 'FetchSize', 100)
DBSetProp('VLMERCACABECERA', 'View', 'MaxRecords', -1)
DBSetProp('VLMERCACABECERA', 'View', 'Tables', 'facturas')
DBSetProp('VLMERCACABECERA', 'View', 'Prepared', .F.)
DBSetProp('VLMERCACABECERA', 'View', 'CompareMemo', .T.)
DBSetProp('VLMERCACABECERA', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLMERCACABECERA', 'View', 'FetchSize', 100)
DBSetProp('VLMERCACABECERA', 'View', 'Comment', "")
DBSetProp('VLMERCACABECERA', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLMERCACABECERA', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLMERCACABECERA
* Props for the VLMERCACABECERA.compro field.
DBSetProp('VLMERCACABECERA.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLMERCACABECERA.compro', 'Field', 'DataType', "C(2)")
* Props for the VLMERCACABECERA.letra field.
DBSetProp('VLMERCACABECERA.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLMERCACABECERA.letra', 'Field', 'DataType', "C(1)")
* Props for the VLMERCACABECERA.numero field.
DBSetProp('VLMERCACABECERA.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLMERCACABECERA.numero', 'Field', 'DataType', "N(12)")
* Props for the VLMERCACABECERA.remito field.
DBSetProp('VLMERCACABECERA.remito', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.remito', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.remito', 'Field', 'UpdateName', 'facturas.remito')
DBSetProp('VLMERCACABECERA.remito', 'Field', 'DataType', "C(15)")
* Props for the VLMERCACABECERA.fecha field.
DBSetProp('VLMERCACABECERA.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLMERCACABECERA.fecha', 'Field', 'DataType', "D")
* Props for the VLMERCACABECERA.condicion field.
DBSetProp('VLMERCACABECERA.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.condicion', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.condicion', 'Field', 'UpdateName', 'facturas.condicion')
DBSetProp('VLMERCACABECERA.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLMERCACABECERA.total field.
DBSetProp('VLMERCACABECERA.total', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.total', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.total', 'Field', 'UpdateName', 'facturas.total')
DBSetProp('VLMERCACABECERA.total', 'Field', 'DataType', "N(12,2)")
* Props for the VLMERCACABECERA.entrega field.
DBSetProp('VLMERCACABECERA.entrega', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.entrega', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.entrega', 'Field', 'UpdateName', 'facturas.entrega')
DBSetProp('VLMERCACABECERA.entrega', 'Field', 'DataType', "N(12,2)")
* Props for the VLMERCACABECERA.estado field.
DBSetProp('VLMERCACABECERA.estado', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.estado', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.estado', 'Field', 'UpdateName', 'facturas.estado')
DBSetProp('VLMERCACABECERA.estado', 'Field', 'DataType', "C(1)")
* Props for the VLMERCACABECERA.marca field.
DBSetProp('VLMERCACABECERA.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.marca', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.marca', 'Field', 'UpdateName', 'facturas.marca')
DBSetProp('VLMERCACABECERA.marca', 'Field', 'DataType', "C(1)")
* Props for the VLMERCACABECERA.operador field.
DBSetProp('VLMERCACABECERA.operador', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.operador', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.operador', 'Field', 'UpdateName', 'facturas.operador')
DBSetProp('VLMERCACABECERA.operador', 'Field', 'DataType', "C(2)")
* Props for the VLMERCACABECERA.codcomis field.
DBSetProp('VLMERCACABECERA.codcomis', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.codcomis', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.codcomis', 'Field', 'UpdateName', 'facturas.codcomis')
DBSetProp('VLMERCACABECERA.codcomis', 'Field', 'DataType', "N(2)")
* Props for the VLMERCACABECERA.noestadist field.
DBSetProp('VLMERCACABECERA.noestadist', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCACABECERA.noestadist', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCACABECERA.noestadist', 'Field', 'UpdateName', 'facturas.noestadist')
DBSetProp('VLMERCACABECERA.noestadist', 'Field', 'DataType', "L")
ENDFUNC
 
FUNCTION MakeView_VLMERCADETALLE
***************** Ver la configuración para VLMERCADETALLE ***************

CREATE SQL VIEW "VLMERCADETALLE" ; 
   AS SELECT Detven.codigo, Marcas.nombre AS marca, Lista.medida, Lista.nombre,  Detven.cantidad, Detven.precio, Detven.descuento, Detven.total FROM detven, lista, marcas WHERE Detven.codigo = Lista.codigo   AND Lista.marca = Marcas.codigo   AND (Detven.compro = ?cCompro   AND Detven.letra = ?cLetra   AND Detven.numero = ?nNumero)

DBSetProp('VLMERCADETALLE', 'View', 'UpdateType', 1)
DBSetProp('VLMERCADETALLE', 'View', 'WhereType', 3)
DBSetProp('VLMERCADETALLE', 'View', 'FetchMemo', .T.)
DBSetProp('VLMERCADETALLE', 'View', 'SendUpdates', .F.)
DBSetProp('VLMERCADETALLE', 'View', 'UseMemoSize', 255)
DBSetProp('VLMERCADETALLE', 'View', 'FetchSize', 100)
DBSetProp('VLMERCADETALLE', 'View', 'MaxRecords', -1)
DBSetProp('VLMERCADETALLE', 'View', 'Tables', 'detven,lista')
DBSetProp('VLMERCADETALLE', 'View', 'Prepared', .F.)
DBSetProp('VLMERCADETALLE', 'View', 'CompareMemo', .T.)
DBSetProp('VLMERCADETALLE', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLMERCADETALLE', 'View', 'FetchSize', 100)
DBSetProp('VLMERCADETALLE', 'View', 'Comment', "")
DBSetProp('VLMERCADETALLE', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLMERCADETALLE', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLMERCADETALLE
* Props for the VLMERCADETALLE.codigo field.
DBSetProp('VLMERCADETALLE.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCADETALLE.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCADETALLE.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLMERCADETALLE.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLMERCADETALLE.marca field.
DBSetProp('VLMERCADETALLE.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCADETALLE.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLMERCADETALLE.marca', 'Field', 'UpdateName', 'marcas.nombre')
DBSetProp('VLMERCADETALLE.marca', 'Field', 'DataType', "C(20)")
* Props for the VLMERCADETALLE.medida field.
DBSetProp('VLMERCADETALLE.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCADETALLE.medida', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCADETALLE.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLMERCADETALLE.medida', 'Field', 'DataType', "C(10)")
* Props for the VLMERCADETALLE.nombre field.
DBSetProp('VLMERCADETALLE.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCADETALLE.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCADETALLE.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLMERCADETALLE.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLMERCADETALLE.cantidad field.
DBSetProp('VLMERCADETALLE.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCADETALLE.cantidad', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCADETALLE.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLMERCADETALLE.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLMERCADETALLE.precio field.
DBSetProp('VLMERCADETALLE.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCADETALLE.precio', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCADETALLE.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLMERCADETALLE.precio', 'Field', 'DataType', "N(10,2)")
* Props for the VLMERCADETALLE.descuento field.
DBSetProp('VLMERCADETALLE.descuento', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCADETALLE.descuento', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCADETALLE.descuento', 'Field', 'UpdateName', 'detven.descuento')
DBSetProp('VLMERCADETALLE.descuento', 'Field', 'DataType', "N(6,2)")
* Props for the VLMERCADETALLE.total field.
DBSetProp('VLMERCADETALLE.total', 'Field', 'KeyField', .F.)
DBSetProp('VLMERCADETALLE.total', 'Field', 'Updatable', .T.)
DBSetProp('VLMERCADETALLE.total', 'Field', 'UpdateName', 'detven.total')
DBSetProp('VLMERCADETALLE.total', 'Field', 'DataType', "N(10,2)")
ENDFUNC
 
FUNCTION MakeView_VLCLIENTES
***************** Ver la configuración para VLCLIENTES ***************

CREATE SQL VIEW "VLCLIENTES" ; 
   AS SELECT Clientes.codigo, Clientes.nombre, Clientes.apeynom,  Clientes.domicilio, Clientes.codpostal, Clientes.barrio,  Clientes.tipocli, Clientes.sitiva, Clientes.tipodoc, Clientes.cuit,  Clientes.convta, Clientes.caractel, Clientes.telefono, Clientes.fax,  Clientes.movil, Clientes.transporte, Clientes.mail, Clientes.mail2,  Clientes.vendedor, Clientes.fechanac, Clientes.fechaing, Clientes.msn,  Clientes.observacio, Clientes.sexo, Clientes.actividad, Clientes.hobbie,  Clientes.equipo, Clientes.sucursal, Clientes.autorizado,  Clientes.percepib, Clientes.vip, Clientes.ingbruto, Clientes.mayorista,  Clientes.subcuenta FROM clientes WHERE Clientes.codigo = ?nCliente

DBSetProp('VLCLIENTES', 'View', 'UpdateType', 1)
DBSetProp('VLCLIENTES', 'View', 'WhereType', 3)
DBSetProp('VLCLIENTES', 'View', 'FetchMemo', .T.)
DBSetProp('VLCLIENTES', 'View', 'SendUpdates', .T.)
DBSetProp('VLCLIENTES', 'View', 'UseMemoSize', 255)
DBSetProp('VLCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLCLIENTES', 'View', 'MaxRecords', -1)
DBSetProp('VLCLIENTES', 'View', 'Tables', 'clientes')
DBSetProp('VLCLIENTES', 'View', 'Prepared', .F.)
DBSetProp('VLCLIENTES', 'View', 'CompareMemo', .T.)
DBSetProp('VLCLIENTES', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLCLIENTES', 'View', 'Comment', "")
DBSetProp('VLCLIENTES', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLCLIENTES', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLCLIENTES
* Props for the VLCLIENTES.codigo field.
DBSetProp('VLCLIENTES.codigo', 'Field', 'KeyField', .T.)
DBSetProp('VLCLIENTES.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.codigo', 'Field', 'UpdateName', 'clientes.codigo')
DBSetProp('VLCLIENTES.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLCLIENTES.nombre field.
DBSetProp('VLCLIENTES.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLCLIENTES.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLCLIENTES.apeynom field.
DBSetProp('VLCLIENTES.apeynom', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.apeynom', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.apeynom', 'Field', 'UpdateName', 'clientes.apeynom')
DBSetProp('VLCLIENTES.apeynom', 'Field', 'DataType', "C(50)")
* Props for the VLCLIENTES.domicilio field.
DBSetProp('VLCLIENTES.domicilio', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.domicilio', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.domicilio', 'Field', 'UpdateName', 'clientes.domicilio')
DBSetProp('VLCLIENTES.domicilio', 'Field', 'DataType', "C(30)")
* Props for the VLCLIENTES.codpostal field.
DBSetProp('VLCLIENTES.codpostal', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.codpostal', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.codpostal', 'Field', 'UpdateName', 'clientes.codpostal')
DBSetProp('VLCLIENTES.codpostal', 'Field', 'DataType', "C(5)")
* Props for the VLCLIENTES.barrio field.
DBSetProp('VLCLIENTES.barrio', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.barrio', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.barrio', 'Field', 'UpdateName', 'clientes.barrio')
DBSetProp('VLCLIENTES.barrio', 'Field', 'DataType', "C(30)")
* Props for the VLCLIENTES.tipocli field.
DBSetProp('VLCLIENTES.tipocli', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.tipocli', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.tipocli', 'Field', 'UpdateName', 'clientes.tipocli')
DBSetProp('VLCLIENTES.tipocli', 'Field', 'DataType', "C(1)")
* Props for the VLCLIENTES.sitiva field.
DBSetProp('VLCLIENTES.sitiva', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.sitiva', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.sitiva', 'Field', 'UpdateName', 'clientes.sitiva')
DBSetProp('VLCLIENTES.sitiva', 'Field', 'DataType', "C(3)")
* Props for the VLCLIENTES.tipodoc field.
DBSetProp('VLCLIENTES.tipodoc', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.tipodoc', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.tipodoc', 'Field', 'UpdateName', 'clientes.tipodoc')
DBSetProp('VLCLIENTES.tipodoc', 'Field', 'DataType', "C(4)")
* Props for the VLCLIENTES.cuit field.
DBSetProp('VLCLIENTES.cuit', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.cuit', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.cuit', 'Field', 'UpdateName', 'clientes.cuit')
DBSetProp('VLCLIENTES.cuit', 'Field', 'DataType', "N(11)")
* Props for the VLCLIENTES.convta field.
DBSetProp('VLCLIENTES.convta', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.convta', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.convta', 'Field', 'UpdateName', 'clientes.convta')
DBSetProp('VLCLIENTES.convta', 'Field', 'DataType', "N(1)")
* Props for the VLCLIENTES.caractel field.
DBSetProp('VLCLIENTES.caractel', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.caractel', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.caractel', 'Field', 'UpdateName', 'clientes.caractel')
DBSetProp('VLCLIENTES.caractel', 'Field', 'DataType', "C(5)")
* Props for the VLCLIENTES.telefono field.
DBSetProp('VLCLIENTES.telefono', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.telefono', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.telefono', 'Field', 'UpdateName', 'clientes.telefono')
DBSetProp('VLCLIENTES.telefono', 'Field', 'DataType', "C(15)")
* Props for the VLCLIENTES.fax field.
DBSetProp('VLCLIENTES.fax', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.fax', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.fax', 'Field', 'UpdateName', 'clientes.fax')
DBSetProp('VLCLIENTES.fax', 'Field', 'DataType', "C(15)")
* Props for the VLCLIENTES.movil field.
DBSetProp('VLCLIENTES.movil', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.movil', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.movil', 'Field', 'UpdateName', 'clientes.movil')
DBSetProp('VLCLIENTES.movil', 'Field', 'DataType', "C(15)")
* Props for the VLCLIENTES.transporte field.
DBSetProp('VLCLIENTES.transporte', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.transporte', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.transporte', 'Field', 'UpdateName', 'clientes.transporte')
DBSetProp('VLCLIENTES.transporte', 'Field', 'DataType', "C(30)")
* Props for the VLCLIENTES.mail field.
DBSetProp('VLCLIENTES.mail', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.mail', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.mail', 'Field', 'UpdateName', 'clientes.mail')
DBSetProp('VLCLIENTES.mail', 'Field', 'DataType', "C(50)")
* Props for the VLCLIENTES.mail2 field.
DBSetProp('VLCLIENTES.mail2', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.mail2', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.mail2', 'Field', 'UpdateName', 'clientes.mail2')
DBSetProp('VLCLIENTES.mail2', 'Field', 'DataType', "C(50)")
* Props for the VLCLIENTES.vendedor field.
DBSetProp('VLCLIENTES.vendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.vendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.vendedor', 'Field', 'UpdateName', 'clientes.vendedor')
DBSetProp('VLCLIENTES.vendedor', 'Field', 'DataType', "N(3)")
* Props for the VLCLIENTES.fechanac field.
DBSetProp('VLCLIENTES.fechanac', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.fechanac', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.fechanac', 'Field', 'UpdateName', 'clientes.fechanac')
DBSetProp('VLCLIENTES.fechanac', 'Field', 'DataType', "D")
* Props for the VLCLIENTES.fechaing field.
DBSetProp('VLCLIENTES.fechaing', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.fechaing', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.fechaing', 'Field', 'UpdateName', 'clientes.fechaing')
DBSetProp('VLCLIENTES.fechaing', 'Field', 'DataType', "D")
* Props for the VLCLIENTES.msn field.
DBSetProp('VLCLIENTES.msn', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.msn', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.msn', 'Field', 'UpdateName', 'clientes.msn')
DBSetProp('VLCLIENTES.msn', 'Field', 'DataType', "C(30)")
* Props for the VLCLIENTES.observacio field.
DBSetProp('VLCLIENTES.observacio', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.observacio', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.observacio', 'Field', 'UpdateName', 'clientes.observacio')
DBSetProp('VLCLIENTES.observacio', 'Field', 'DataType', "M")
* Props for the VLCLIENTES.sexo field.
DBSetProp('VLCLIENTES.sexo', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.sexo', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.sexo', 'Field', 'UpdateName', 'clientes.sexo')
DBSetProp('VLCLIENTES.sexo', 'Field', 'DataType', "N(1)")
* Props for the VLCLIENTES.actividad field.
DBSetProp('VLCLIENTES.actividad', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.actividad', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.actividad', 'Field', 'UpdateName', 'clientes.actividad')
DBSetProp('VLCLIENTES.actividad', 'Field', 'DataType', "N(3)")
* Props for the VLCLIENTES.hobbie field.
DBSetProp('VLCLIENTES.hobbie', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.hobbie', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.hobbie', 'Field', 'UpdateName', 'clientes.hobbie')
DBSetProp('VLCLIENTES.hobbie', 'Field', 'DataType', "C(50)")
* Props for the VLCLIENTES.equipo field.
DBSetProp('VLCLIENTES.equipo', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.equipo', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.equipo', 'Field', 'UpdateName', 'clientes.equipo')
DBSetProp('VLCLIENTES.equipo', 'Field', 'DataType', "C(50)")
* Props for the VLCLIENTES.sucursal field.
DBSetProp('VLCLIENTES.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.sucursal', 'Field', 'UpdateName', 'clientes.sucursal')
DBSetProp('VLCLIENTES.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLCLIENTES.autorizado field.
DBSetProp('VLCLIENTES.autorizado', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.autorizado', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.autorizado', 'Field', 'UpdateName', 'clientes.autorizado')
DBSetProp('VLCLIENTES.autorizado', 'Field', 'DataType', "C(15)")
* Props for the VLCLIENTES.percepib field.
DBSetProp('VLCLIENTES.percepib', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.percepib', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.percepib', 'Field', 'UpdateName', 'clientes.percepib')
DBSetProp('VLCLIENTES.percepib', 'Field', 'DataType', "N(1)")
* Props for the VLCLIENTES.vip field.
DBSetProp('VLCLIENTES.vip', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.vip', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.vip', 'Field', 'UpdateName', 'clientes.vip')
DBSetProp('VLCLIENTES.vip', 'Field', 'DataType', "L")
* Props for the VLCLIENTES.ingbruto field.
DBSetProp('VLCLIENTES.ingbruto', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.ingbruto', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.ingbruto', 'Field', 'UpdateName', 'clientes.ingbruto')
DBSetProp('VLCLIENTES.ingbruto', 'Field', 'DataType', "C(15)")
* Props for the VLCLIENTES.mayorista field.
DBSetProp('VLCLIENTES.mayorista', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.mayorista', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.mayorista', 'Field', 'UpdateName', 'clientes.mayorista')
DBSetProp('VLCLIENTES.mayorista', 'Field', 'DataType', "L")
* Props for the VLCLIENTES.subcuenta field.
DBSetProp('VLCLIENTES.subcuenta', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIENTES.subcuenta', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIENTES.subcuenta', 'Field', 'UpdateName', 'clientes.subcuenta')
DBSetProp('VLCLIENTES.subcuenta', 'Field', 'DataType', "N(6)")
ENDFUNC
 
FUNCTION MakeView_VLFACTPENDIENTESUC
***************** Ver la configuración para VLFACTPENDIENTESUC ***************

CREATE SQL VIEW "VLFACTPENDIENTESUC" ; 
   AS SELECT Facturas.compro, Codven.nombre, Facturas.letra, Facturas.numero,  Facturas.fecha, Facturas.cliente, Facturas.remito,  Facturas.total*Codven.mult_cli AS total,  Facturas.entrega*Codven.mult_cli AS entrega,  (Facturas.total-Facturas.entrega)*Codven.mult_cli AS saldo,  Facturas.total*0 AS pagos, Facturas.marca, Facturas.noestadist FROM facturas, codven, clientes WHERE Facturas.cliente = Clientes.codigo   AND Facturas.compro = Codven.compro   AND (Facturas.total <> Facturas.entrega   AND Codven.mult_cli <> 0   AND Clientes.sucursal = ?nSucursal) ORDER BY Facturas.cliente, Facturas.fecha

DBSetProp('VLFACTPENDIENTESUC', 'View', 'UpdateType', 1)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'WhereType', 3)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'FetchMemo', .T.)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'SendUpdates', .F.)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'UseMemoSize', 255)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'FetchSize', 100)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'MaxRecords', -1)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'Tables', 'facturas')
DBSetProp('VLFACTPENDIENTESUC', 'View', 'Prepared', .F.)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'CompareMemo', .T.)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'FetchSize', 100)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'Comment', "")
DBSetProp('VLFACTPENDIENTESUC', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLFACTPENDIENTESUC', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLFACTPENDIENTESUC
* Props for the VLFACTPENDIENTESUC.compro field.
DBSetProp('VLFACTPENDIENTESUC.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTESUC.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLFACTPENDIENTESUC.compro', 'Field', 'DataType', "C(2)")
* Props for the VLFACTPENDIENTESUC.nombre field.
DBSetProp('VLFACTPENDIENTESUC.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTESUC.nombre', 'Field', 'UpdateName', 'codven.nombre')
DBSetProp('VLFACTPENDIENTESUC.nombre', 'Field', 'DataType', "C(20)")
* Props for the VLFACTPENDIENTESUC.letra field.
DBSetProp('VLFACTPENDIENTESUC.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTESUC.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLFACTPENDIENTESUC.letra', 'Field', 'DataType', "C(1)")
* Props for the VLFACTPENDIENTESUC.numero field.
DBSetProp('VLFACTPENDIENTESUC.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTESUC.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLFACTPENDIENTESUC.numero', 'Field', 'DataType', "N(12)")
* Props for the VLFACTPENDIENTESUC.fecha field.
DBSetProp('VLFACTPENDIENTESUC.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTESUC.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLFACTPENDIENTESUC.fecha', 'Field', 'DataType', "D")
* Props for the VLFACTPENDIENTESUC.cliente field.
DBSetProp('VLFACTPENDIENTESUC.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.cliente', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTESUC.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLFACTPENDIENTESUC.cliente', 'Field', 'DataType', "N(5)")
* Props for the VLFACTPENDIENTESUC.remito field.
DBSetProp('VLFACTPENDIENTESUC.remito', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.remito', 'Field', 'Updatable', .T.)
DBSetProp('VLFACTPENDIENTESUC.remito', 'Field', 'UpdateName', 'facturas.remito')
DBSetProp('VLFACTPENDIENTESUC.remito', 'Field', 'DataType', "C(15)")
* Props for the VLFACTPENDIENTESUC.total field.
DBSetProp('VLFACTPENDIENTESUC.total', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.total', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTESUC.total', 'Field', 'UpdateName', 'Facturas.cliente*')
DBSetProp('VLFACTPENDIENTESUC.total', 'Field', 'DataType', "N(15,2)")
* Props for the VLFACTPENDIENTESUC.entrega field.
DBSetProp('VLFACTPENDIENTESUC.entrega', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.entrega', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTESUC.entrega', 'Field', 'UpdateName', 'Facturas.cliente**')
DBSetProp('VLFACTPENDIENTESUC.entrega', 'Field', 'DataType', "N(15,2)")
* Props for the VLFACTPENDIENTESUC.saldo field.
DBSetProp('VLFACTPENDIENTESUC.saldo', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.saldo', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTESUC.saldo', 'Field', 'UpdateName', 'Facturas.cliente***')
DBSetProp('VLFACTPENDIENTESUC.saldo', 'Field', 'DataType', "N(16,2)")
* Props for the VLFACTPENDIENTESUC.pagos field.
DBSetProp('VLFACTPENDIENTESUC.pagos', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.pagos', 'Field', 'Updatable', .F.)
DBSetProp('VLFACTPENDIENTESUC.pagos', 'Field', 'UpdateName', 'Facturas.remito****')
DBSetProp('VLFACTPENDIENTESUC.pagos', 'Field', 'DataType', "N(14,2)")
* Props for the VLFACTPENDIENTESUC.marca field.
DBSetProp('VLFACTPENDIENTESUC.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.marca', 'Field', 'Updatable', .T.)
DBSetProp('VLFACTPENDIENTESUC.marca', 'Field', 'UpdateName', 'facturas.marca')
DBSetProp('VLFACTPENDIENTESUC.marca', 'Field', 'DataType', "C(1)")
* Props for the VLFACTPENDIENTESUC.noestadist field.
DBSetProp('VLFACTPENDIENTESUC.noestadist', 'Field', 'KeyField', .F.)
DBSetProp('VLFACTPENDIENTESUC.noestadist', 'Field', 'Updatable', .T.)
DBSetProp('VLFACTPENDIENTESUC.noestadist', 'Field', 'UpdateName', 'facturas.noestadist')
DBSetProp('VLFACTPENDIENTESUC.noestadist', 'Field', 'DataType', "L")
ENDFUNC
 
FUNCTION MakeView_VLSTOCKUNICO
***************** Ver la configuración para VLSTOCKUNICO ***************

CREATE SQL VIEW "VLSTOCKUNICO" ; 
   AS SELECT Stock.codigo, Lista.medida, Lista.codfabrica, Lista.fecha,  Lista.nombre, Lista.articulo, Articulo.nombre, Lista.modelo,  Modelos.nombre, Marcas.nombre, SUM(Stock.stock) AS stock, Lista.estado,  Lista.orden, Lista.descuento, Lista.costo, Lista.precio FROM stock, lista, marcas, modelos, articulo WHERE Stock.codigo = Lista.codigo   AND Lista.modelo = Modelos.codigo   AND Lista.marca = Marcas.codigo   AND Lista.articulo = Articulo.codigo   AND Stock.stock <> 0 GROUP BY Stock.codigo ORDER BY Lista.articulo, Lista.modelo, Lista.orden

DBSetProp('VLSTOCKUNICO', 'View', 'UpdateType', 1)
DBSetProp('VLSTOCKUNICO', 'View', 'WhereType', 3)
DBSetProp('VLSTOCKUNICO', 'View', 'FetchMemo', .T.)
DBSetProp('VLSTOCKUNICO', 'View', 'SendUpdates', .F.)
DBSetProp('VLSTOCKUNICO', 'View', 'UseMemoSize', 255)
DBSetProp('VLSTOCKUNICO', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKUNICO', 'View', 'MaxRecords', -1)
DBSetProp('VLSTOCKUNICO', 'View', 'Tables', 'lista,articulo')
DBSetProp('VLSTOCKUNICO', 'View', 'Prepared', .F.)
DBSetProp('VLSTOCKUNICO', 'View', 'CompareMemo', .T.)
DBSetProp('VLSTOCKUNICO', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSTOCKUNICO', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKUNICO', 'View', 'Comment', "")
DBSetProp('VLSTOCKUNICO', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSTOCKUNICO', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSTOCKUNICO
* Props for the VLSTOCKUNICO.codigo field.
DBSetProp('VLSTOCKUNICO.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKUNICO.codigo', 'Field', 'UpdateName', 'stock.codigo')
DBSetProp('VLSTOCKUNICO.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCKUNICO.medida field.
DBSetProp('VLSTOCKUNICO.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.medida', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKUNICO.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLSTOCKUNICO.medida', 'Field', 'DataType', "C(13)")
* Props for the VLSTOCKUNICO.codfabrica field.
DBSetProp('VLSTOCKUNICO.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.codfabrica', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKUNICO.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLSTOCKUNICO.codfabrica', 'Field', 'DataType', "C(15)")
* Props for the VLSTOCKUNICO.fecha field.
DBSetProp('VLSTOCKUNICO.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKUNICO.fecha', 'Field', 'UpdateName', 'lista.fecha')
DBSetProp('VLSTOCKUNICO.fecha', 'Field', 'DataType', "C(6)")
* Props for the VLSTOCKUNICO.nombre_a field.
DBSetProp('VLSTOCKUNICO.nombre_a', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.nombre_a', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKUNICO.nombre_a', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLSTOCKUNICO.nombre_a', 'Field', 'DataType', "C(50)")
* Props for the VLSTOCKUNICO.articulo field.
DBSetProp('VLSTOCKUNICO.articulo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.articulo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKUNICO.articulo', 'Field', 'UpdateName', 'lista.articulo')
DBSetProp('VLSTOCKUNICO.articulo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCKUNICO.nombre_b field.
DBSetProp('VLSTOCKUNICO.nombre_b', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.nombre_b', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKUNICO.nombre_b', 'Field', 'UpdateName', 'articulo.nombre')
DBSetProp('VLSTOCKUNICO.nombre_b', 'Field', 'DataType', "C(30)")
* Props for the VLSTOCKUNICO.modelo field.
DBSetProp('VLSTOCKUNICO.modelo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.modelo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKUNICO.modelo', 'Field', 'UpdateName', 'lista.modelo')
DBSetProp('VLSTOCKUNICO.modelo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCKUNICO.nombre_c field.
DBSetProp('VLSTOCKUNICO.nombre_c', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.nombre_c', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKUNICO.nombre_c', 'Field', 'UpdateName', 'modelos.nombre')
DBSetProp('VLSTOCKUNICO.nombre_c', 'Field', 'DataType', "C(30)")
* Props for the VLSTOCKUNICO.nombre_d field.
DBSetProp('VLSTOCKUNICO.nombre_d', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.nombre_d', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKUNICO.nombre_d', 'Field', 'UpdateName', 'marcas.nombre')
DBSetProp('VLSTOCKUNICO.nombre_d', 'Field', 'DataType', "C(20)")
* Props for the VLSTOCKUNICO.stock field.
DBSetProp('VLSTOCKUNICO.stock', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.stock', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKUNICO.stock', 'Field', 'UpdateName', 'SUM(Stock.stock)')
DBSetProp('VLSTOCKUNICO.stock', 'Field', 'DataType', "N(16,2)")
* Props for the VLSTOCKUNICO.estado field.
DBSetProp('VLSTOCKUNICO.estado', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.estado', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKUNICO.estado', 'Field', 'UpdateName', 'lista.estado')
DBSetProp('VLSTOCKUNICO.estado', 'Field', 'DataType', "C(1)")
* Props for the VLSTOCKUNICO.orden field.
DBSetProp('VLSTOCKUNICO.orden', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.orden', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKUNICO.orden', 'Field', 'UpdateName', 'lista.orden')
DBSetProp('VLSTOCKUNICO.orden', 'Field', 'DataType', "N(3)")
* Props for the VLSTOCKUNICO.descuento field.
DBSetProp('VLSTOCKUNICO.descuento', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.descuento', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKUNICO.descuento', 'Field', 'UpdateName', 'lista.descuento')
DBSetProp('VLSTOCKUNICO.descuento', 'Field', 'DataType', "N(6,2)")
* Props for the VLSTOCKUNICO.costo field.
DBSetProp('VLSTOCKUNICO.costo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.costo', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKUNICO.costo', 'Field', 'UpdateName', 'lista.costo')
DBSetProp('VLSTOCKUNICO.costo', 'Field', 'DataType', "N(12,2)")
* Props for the VLSTOCKUNICO.precio field.
DBSetProp('VLSTOCKUNICO.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKUNICO.precio', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKUNICO.precio', 'Field', 'UpdateName', 'lista.precio')
DBSetProp('VLSTOCKUNICO.precio', 'Field', 'DataType', "N(12,2)")
ENDFUNC
 
FUNCTION MakeView_VLVENTACOMISIONVENDEDORDET
***************** Ver la configuración para VLVENTACOMISIONVENDEDORDET ***************

CREATE SQL VIEW "VLVENTACOMISIONVENDEDORDET" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.fecha,  Facturas.condicion, Facturas.cliente, Clientes.nombre AS nomcliente,  Facturas.comision, Detven.codigo, Lista.nombre AS nomlista,  Detven.cantidad, Detven.precio, Detven.descuento,  Detven.total*Codven.mult_com AS total FROM clientes, facturas, codven, detven, lista WHERE Detven.id = Facturas.id   AND Facturas.cliente = Clientes.codigo   AND Facturas.compro = Codven.compro   AND Detven.codigo = Lista.codigo   AND (Clientes.vendedor = ?nVendedor   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Codven.mult_com <> 0) ORDER BY Facturas.cliente, Facturas.fecha

DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'UpdateType', 1)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'WhereType', 3)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'FetchSize', 100)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'Tables', 'facturas,clientes,detven,lista')
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'Prepared', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'FetchSize', 100)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'Comment', "")
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTACOMISIONVENDEDORDET', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTACOMISIONVENDEDORDET
* Props for the VLVENTACOMISIONVENDEDORDET.compro field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLVENTACOMISIONVENDEDORDET.compro', 'Field', 'DataType', "C(2)")
* Props for the VLVENTACOMISIONVENDEDORDET.letra field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLVENTACOMISIONVENDEDORDET.letra', 'Field', 'DataType', "C(1)")
* Props for the VLVENTACOMISIONVENDEDORDET.numero field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLVENTACOMISIONVENDEDORDET.numero', 'Field', 'DataType', "N(12)")
* Props for the VLVENTACOMISIONVENDEDORDET.fecha field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTACOMISIONVENDEDORDET.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTACOMISIONVENDEDORDET.condicion field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.condicion', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.condicion', 'Field', 'UpdateName', 'facturas.condicion')
DBSetProp('VLVENTACOMISIONVENDEDORDET.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLVENTACOMISIONVENDEDORDET.cliente field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLVENTACOMISIONVENDEDORDET.cliente', 'Field', 'DataType', "N(5)")
* Props for the VLVENTACOMISIONVENDEDORDET.nomcliente field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.nomcliente', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.nomcliente', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.nomcliente', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLVENTACOMISIONVENDEDORDET.nomcliente', 'Field', 'DataType', "C(30)")
* Props for the VLVENTACOMISIONVENDEDORDET.comision field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.comision', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.comision', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.comision', 'Field', 'UpdateName', 'facturas.comision')
DBSetProp('VLVENTACOMISIONVENDEDORDET.comision', 'Field', 'DataType', "C(1)")
* Props for the VLVENTACOMISIONVENDEDORDET.codigo field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLVENTACOMISIONVENDEDORDET.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLVENTACOMISIONVENDEDORDET.nomlista field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.nomlista', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.nomlista', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.nomlista', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLVENTACOMISIONVENDEDORDET.nomlista', 'Field', 'DataType', "C(50)")
* Props for the VLVENTACOMISIONVENDEDORDET.cantidad field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.cantidad', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLVENTACOMISIONVENDEDORDET.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLVENTACOMISIONVENDEDORDET.precio field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.precio', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLVENTACOMISIONVENDEDORDET.precio', 'Field', 'DataType', "N(10,2)")
* Props for the VLVENTACOMISIONVENDEDORDET.descuento field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.descuento', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.descuento', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.descuento', 'Field', 'UpdateName', 'detven.descuento')
DBSetProp('VLVENTACOMISIONVENDEDORDET.descuento', 'Field', 'DataType', "N(6,2)")
* Props for the VLVENTACOMISIONVENDEDORDET.total field.
DBSetProp('VLVENTACOMISIONVENDEDORDET.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.total', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMISIONVENDEDORDET.total', 'Field', 'UpdateName', 'Detven.descuento*')
DBSetProp('VLVENTACOMISIONVENDEDORDET.total', 'Field', 'DataType', "N(13,2)")
ENDFUNC
 
FUNCTION MakeView_VLIVAVENTASFULL
***************** Ver la configuración para VLIVAVENTASFULL ***************

CREATE SQL VIEW "VLIVAVENTASFULL" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.fecha,  Facturas.nombre, Facturas.sitiva, Facturas.cuit,  Facturas.gravado*Codven.mult_ven AS gravado,  Facturas.exento*Codven.mult_ven AS exento,  Facturas.iva*Codven.mult_ven AS iva,  Facturas.acrece*Codven.mult_ven AS acrece,  Facturas.impint*Codven.mult_ven AS impint,  Facturas.total*Codven.mult_ven AS total, Facturas.codimp FROM clientes,   facturas INNER JOIN codven    ON  Facturas.compro = Codven.compro WHERE Facturas.cliente = Clientes.codigo   AND (MONTH(Facturas.fecha) = ?nMes   AND YEAR(Facturas.fecha) = ?nAnio   AND Codven.libroiva = .T.) ORDER BY Facturas.fecha, Facturas.letra, Facturas.numero

DBSetProp('VLIVAVENTASFULL', 'View', 'UpdateType', 1)
DBSetProp('VLIVAVENTASFULL', 'View', 'WhereType', 3)
DBSetProp('VLIVAVENTASFULL', 'View', 'FetchMemo', .T.)
DBSetProp('VLIVAVENTASFULL', 'View', 'SendUpdates', .F.)
DBSetProp('VLIVAVENTASFULL', 'View', 'UseMemoSize', 255)
DBSetProp('VLIVAVENTASFULL', 'View', 'FetchSize', 100)
DBSetProp('VLIVAVENTASFULL', 'View', 'MaxRecords', -1)
DBSetProp('VLIVAVENTASFULL', 'View', 'Tables', 'facturas')
DBSetProp('VLIVAVENTASFULL', 'View', 'Prepared', .F.)
DBSetProp('VLIVAVENTASFULL', 'View', 'CompareMemo', .T.)
DBSetProp('VLIVAVENTASFULL', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLIVAVENTASFULL', 'View', 'FetchSize', 100)
DBSetProp('VLIVAVENTASFULL', 'View', 'Comment', "")
DBSetProp('VLIVAVENTASFULL', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLIVAVENTASFULL', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLIVAVENTASFULL
* Props for the VLIVAVENTASFULL.compro field.
DBSetProp('VLIVAVENTASFULL.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.compro', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLIVAVENTASFULL.compro', 'Field', 'DataType', "C(2)")
* Props for the VLIVAVENTASFULL.letra field.
DBSetProp('VLIVAVENTASFULL.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.letra', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLIVAVENTASFULL.letra', 'Field', 'DataType', "C(1)")
* Props for the VLIVAVENTASFULL.numero field.
DBSetProp('VLIVAVENTASFULL.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.numero', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLIVAVENTASFULL.numero', 'Field', 'DataType', "N(12)")
* Props for the VLIVAVENTASFULL.fecha field.
DBSetProp('VLIVAVENTASFULL.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLIVAVENTASFULL.fecha', 'Field', 'DataType', "D")
* Props for the VLIVAVENTASFULL.nombre field.
DBSetProp('VLIVAVENTASFULL.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLIVAVENTASFULL.nombre', 'Field', 'UpdateName', 'facturas.nombre')
DBSetProp('VLIVAVENTASFULL.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLIVAVENTASFULL.sitiva field.
DBSetProp('VLIVAVENTASFULL.sitiva', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.sitiva', 'Field', 'Updatable', .T.)
DBSetProp('VLIVAVENTASFULL.sitiva', 'Field', 'UpdateName', 'facturas.sitiva')
DBSetProp('VLIVAVENTASFULL.sitiva', 'Field', 'DataType', "C(3)")
* Props for the VLIVAVENTASFULL.cuit field.
DBSetProp('VLIVAVENTASFULL.cuit', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.cuit', 'Field', 'Updatable', .T.)
DBSetProp('VLIVAVENTASFULL.cuit', 'Field', 'UpdateName', 'facturas.cuit')
DBSetProp('VLIVAVENTASFULL.cuit', 'Field', 'DataType', "N(11)")
* Props for the VLIVAVENTASFULL.gravado field.
DBSetProp('VLIVAVENTASFULL.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.gravado', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.gravado', 'Field', 'UpdateName', '')
DBSetProp('VLIVAVENTASFULL.gravado', 'Field', 'DataType', "N(15,2)")
* Props for the VLIVAVENTASFULL.exento field.
DBSetProp('VLIVAVENTASFULL.exento', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.exento', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.exento', 'Field', 'UpdateName', 'Clientes.cuit**')
DBSetProp('VLIVAVENTASFULL.exento', 'Field', 'DataType', "N(15,2)")
* Props for the VLIVAVENTASFULL.iva field.
DBSetProp('VLIVAVENTASFULL.iva', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.iva', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.iva', 'Field', 'UpdateName', '')
DBSetProp('VLIVAVENTASFULL.iva', 'Field', 'DataType', "N(15,2)")
* Props for the VLIVAVENTASFULL.acrece field.
DBSetProp('VLIVAVENTASFULL.acrece', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.acrece', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.acrece', 'Field', 'UpdateName', '')
DBSetProp('VLIVAVENTASFULL.acrece', 'Field', 'DataType', "N(15,2)")
* Props for the VLIVAVENTASFULL.impint field.
DBSetProp('VLIVAVENTASFULL.impint', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.impint', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.impint', 'Field', 'UpdateName', '')
DBSetProp('VLIVAVENTASFULL.impint', 'Field', 'DataType', "N(13,2)")
* Props for the VLIVAVENTASFULL.total field.
DBSetProp('VLIVAVENTASFULL.total', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.total', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.total', 'Field', 'UpdateName', '')
DBSetProp('VLIVAVENTASFULL.total', 'Field', 'DataType', "N(15,2)")
* Props for the VLIVAVENTASFULL.codimp field.
DBSetProp('VLIVAVENTASFULL.codimp', 'Field', 'KeyField', .F.)
DBSetProp('VLIVAVENTASFULL.codimp', 'Field', 'Updatable', .F.)
DBSetProp('VLIVAVENTASFULL.codimp', 'Field', 'UpdateName', 'facturas.codimp')
DBSetProp('VLIVAVENTASFULL.codimp', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLCOMISIONPLANILLA
***************** Ver la configuración para VLCOMISIONPLANILLA ***************

CREATE SQL VIEW "VLCOMISIONPLANILLA" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.fecha, Facturas.cliente, Clientes.nombre, Facturas.nombre AS facturado, Facturas.gravado*Codven.mult_com AS gravado, IIF(Facturas.gravado=0,Facturas.total*Codven.mult_ven,total*0) AS cobrado, Clientes.vendedor FROM facturas, codven, clientes INNER JOIN vendedor  ON  Clientes.vendedor = Vendedor.codigo WHERE Facturas.cliente = Clientes.codigo AND Facturas.compro = Codven.compro AND (Facturas.fecha BETWEEN ?dDesde AND ?dHasta AND Codven.mult_ven <> 0) ORDER BY Clientes.vendedor, Facturas.fecha

DBSetProp('VLCOMISIONPLANILLA', 'View', 'UpdateType', 1)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'WhereType', 3)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'FetchMemo', .T.)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'SendUpdates', .F.)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'UseMemoSize', 255)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'MaxRecords', -1)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'Tables', 'facturas,clientes')
DBSetProp('VLCOMISIONPLANILLA', 'View', 'Prepared', .F.)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'CompareMemo', .T.)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'Comment', "")
DBSetProp('VLCOMISIONPLANILLA', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLCOMISIONPLANILLA', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLCOMISIONPLANILLA
* Props for the VLCOMISIONPLANILLA.compro field.
DBSetProp('VLCOMISIONPLANILLA.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONPLANILLA.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONPLANILLA.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLCOMISIONPLANILLA.compro', 'Field', 'DataType', "C(2)")
* Props for the VLCOMISIONPLANILLA.letra field.
DBSetProp('VLCOMISIONPLANILLA.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONPLANILLA.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONPLANILLA.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLCOMISIONPLANILLA.letra', 'Field', 'DataType', "C(1)")
* Props for the VLCOMISIONPLANILLA.numero field.
DBSetProp('VLCOMISIONPLANILLA.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONPLANILLA.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONPLANILLA.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLCOMISIONPLANILLA.numero', 'Field', 'DataType', "N(12)")
* Props for the VLCOMISIONPLANILLA.fecha field.
DBSetProp('VLCOMISIONPLANILLA.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONPLANILLA.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONPLANILLA.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLCOMISIONPLANILLA.fecha', 'Field', 'DataType', "D")
* Props for the VLCOMISIONPLANILLA.cliente field.
DBSetProp('VLCOMISIONPLANILLA.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONPLANILLA.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONPLANILLA.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLCOMISIONPLANILLA.cliente', 'Field', 'DataType', "N(5)")
* Props for the VLCOMISIONPLANILLA.nombre field.
DBSetProp('VLCOMISIONPLANILLA.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONPLANILLA.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONPLANILLA.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLCOMISIONPLANILLA.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLCOMISIONPLANILLA.facturado field.
DBSetProp('VLCOMISIONPLANILLA.facturado', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONPLANILLA.facturado', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONPLANILLA.facturado', 'Field', 'UpdateName', 'facturado')
DBSetProp('VLCOMISIONPLANILLA.facturado', 'Field', 'DataType', "C(30)")
* Props for the VLCOMISIONPLANILLA.gravado field.
DBSetProp('VLCOMISIONPLANILLA.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONPLANILLA.gravado', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONPLANILLA.gravado', 'Field', 'UpdateName', 'facturas.gravado')
DBSetProp('VLCOMISIONPLANILLA.gravado', 'Field', 'DataType', "N(15,2)")
* Props for the VLCOMISIONPLANILLA.cobrado field.
DBSetProp('VLCOMISIONPLANILLA.cobrado', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONPLANILLA.cobrado', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONPLANILLA.cobrado', 'Field', 'UpdateName', 'cobrado')
DBSetProp('VLCOMISIONPLANILLA.cobrado', 'Field', 'DataType', "N(15,2)")
* Props for the VLCOMISIONPLANILLA.vendedor field.
DBSetProp('VLCOMISIONPLANILLA.vendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONPLANILLA.vendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONPLANILLA.vendedor', 'Field', 'UpdateName', 'clientes.vendedor')
DBSetProp('VLCOMISIONPLANILLA.vendedor', 'Field', 'DataType', "N(3)")
ENDFUNC
 
FUNCTION MakeView_VLCLIECUBCAMION
***************** Ver la configuración para VLCLIECUBCAMION ***************

CREATE SQL VIEW "VLCLIECUBCAMION" ; 
   AS SELECT Clientes.codigo, Clientes.nombre, Clientes.domicilio,  Clientes.codpostal, Localida.localidad, Localida.provincia,  Clientes.telefono, Clientes.fax, Clientes.movil, Clientes.mail,  Clientes.sucursal, Clientes.vendedor FROM detven, facturas, clientes, localida, lista, codven WHERE Detven.id = Facturas.id   AND Facturas.cliente = Clientes.codigo   AND Detven.codigo = Lista.codigo   AND Clientes.codpostal = Localida.codigo   AND Detven.compro = Codven.compro   AND (Lista.marca = ?nMarca   AND ALLTRIM(STR(Lista.articulo,4)) IN (?cFlia)   AND Facturas.cliente <> 0   AND Codven.mult_ven <> 0) GROUP BY Clientes.codigo ORDER BY Clientes.nombre

DBSetProp('VLCLIECUBCAMION', 'View', 'UpdateType', 1)
DBSetProp('VLCLIECUBCAMION', 'View', 'WhereType', 3)
DBSetProp('VLCLIECUBCAMION', 'View', 'FetchMemo', .T.)
DBSetProp('VLCLIECUBCAMION', 'View', 'SendUpdates', .F.)
DBSetProp('VLCLIECUBCAMION', 'View', 'UseMemoSize', 255)
DBSetProp('VLCLIECUBCAMION', 'View', 'FetchSize', 100)
DBSetProp('VLCLIECUBCAMION', 'View', 'MaxRecords', -1)
DBSetProp('VLCLIECUBCAMION', 'View', 'Tables', 'clientes,localida')
DBSetProp('VLCLIECUBCAMION', 'View', 'Prepared', .F.)
DBSetProp('VLCLIECUBCAMION', 'View', 'CompareMemo', .T.)
DBSetProp('VLCLIECUBCAMION', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLCLIECUBCAMION', 'View', 'FetchSize', 100)
DBSetProp('VLCLIECUBCAMION', 'View', 'Comment', "")
DBSetProp('VLCLIECUBCAMION', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLCLIECUBCAMION', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLCLIECUBCAMION
* Props for the VLCLIECUBCAMION.codigo field.
DBSetProp('VLCLIECUBCAMION.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.codigo', 'Field', 'UpdateName', 'clientes.codigo')
DBSetProp('VLCLIECUBCAMION.codigo', 'Field', 'DataType', "N(5)")
* Props for the VLCLIECUBCAMION.nombre field.
DBSetProp('VLCLIECUBCAMION.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLCLIECUBCAMION.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLCLIECUBCAMION.domicilio field.
DBSetProp('VLCLIECUBCAMION.domicilio', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.domicilio', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.domicilio', 'Field', 'UpdateName', 'clientes.domicilio')
DBSetProp('VLCLIECUBCAMION.domicilio', 'Field', 'DataType', "C(30)")
* Props for the VLCLIECUBCAMION.codpostal field.
DBSetProp('VLCLIECUBCAMION.codpostal', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.codpostal', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.codpostal', 'Field', 'UpdateName', 'clientes.codpostal')
DBSetProp('VLCLIECUBCAMION.codpostal', 'Field', 'DataType', "C(5)")
* Props for the VLCLIECUBCAMION.localidad field.
DBSetProp('VLCLIECUBCAMION.localidad', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.localidad', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.localidad', 'Field', 'UpdateName', 'localida.localidad')
DBSetProp('VLCLIECUBCAMION.localidad', 'Field', 'DataType', "C(20)")
* Props for the VLCLIECUBCAMION.provincia field.
DBSetProp('VLCLIECUBCAMION.provincia', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.provincia', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.provincia', 'Field', 'UpdateName', 'localida.provincia')
DBSetProp('VLCLIECUBCAMION.provincia', 'Field', 'DataType', "C(20)")
* Props for the VLCLIECUBCAMION.telefono field.
DBSetProp('VLCLIECUBCAMION.telefono', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.telefono', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.telefono', 'Field', 'UpdateName', 'clientes.telefono')
DBSetProp('VLCLIECUBCAMION.telefono', 'Field', 'DataType', "C(15)")
* Props for the VLCLIECUBCAMION.fax field.
DBSetProp('VLCLIECUBCAMION.fax', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.fax', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.fax', 'Field', 'UpdateName', 'clientes.fax')
DBSetProp('VLCLIECUBCAMION.fax', 'Field', 'DataType', "C(15)")
* Props for the VLCLIECUBCAMION.movil field.
DBSetProp('VLCLIECUBCAMION.movil', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.movil', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.movil', 'Field', 'UpdateName', 'clientes.movil')
DBSetProp('VLCLIECUBCAMION.movil', 'Field', 'DataType', "C(15)")
* Props for the VLCLIECUBCAMION.mail field.
DBSetProp('VLCLIECUBCAMION.mail', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.mail', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.mail', 'Field', 'UpdateName', 'clientes.mail')
DBSetProp('VLCLIECUBCAMION.mail', 'Field', 'DataType', "C(50)")
* Props for the VLCLIECUBCAMION.sucursal field.
DBSetProp('VLCLIECUBCAMION.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.sucursal', 'Field', 'UpdateName', 'clientes.sucursal')
DBSetProp('VLCLIECUBCAMION.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLCLIECUBCAMION.vendedor field.
DBSetProp('VLCLIECUBCAMION.vendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLCLIECUBCAMION.vendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLCLIECUBCAMION.vendedor', 'Field', 'UpdateName', 'clientes.vendedor')
DBSetProp('VLCLIECUBCAMION.vendedor', 'Field', 'DataType', "N(3)")
ENDFUNC
 
FUNCTION MakeView_VLCOMISIONSERV
***************** Ver la configuración para VLCOMISIONSERV ***************

CREATE SQL VIEW "VLCOMISIONSERV" ; 
   AS SELECT Detven.operario, Operario.nombre, Detven.compro, Detven.letra,  Detven.numero, Facturas.fecha, Detven.codigo, Articulo.nombre,  Lista.nombre, Detven.total* Codven.mult_stad AS total, Articulo.comisionop FROM lista, articulo, operario, facturas,   detven INNER JOIN codven    ON  Detven.compro = Codven.compro WHERE Detven.id = Facturas.id   AND Detven.codigo = Lista.codigo   AND Lista.articulo = Articulo.codigo   AND Detven.operario = Operario.codigo   AND (Articulo.comisionop <> 0   AND Codven.mult_stad <> 0   AND Detven.operario BETWEEN ?nDesde AND ?nHasta   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta) ORDER BY Detven.operario

DBSetProp('VLCOMISIONSERV', 'View', 'UpdateType', 1)
DBSetProp('VLCOMISIONSERV', 'View', 'WhereType', 3)
DBSetProp('VLCOMISIONSERV', 'View', 'FetchMemo', .T.)
DBSetProp('VLCOMISIONSERV', 'View', 'SendUpdates', .F.)
DBSetProp('VLCOMISIONSERV', 'View', 'UseMemoSize', 255)
DBSetProp('VLCOMISIONSERV', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONSERV', 'View', 'MaxRecords', -1)
DBSetProp('VLCOMISIONSERV', 'View', 'Tables', 'detven,operario,facturas,articulo,lista')
DBSetProp('VLCOMISIONSERV', 'View', 'Prepared', .F.)
DBSetProp('VLCOMISIONSERV', 'View', 'CompareMemo', .T.)
DBSetProp('VLCOMISIONSERV', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLCOMISIONSERV', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONSERV', 'View', 'Comment', "")
DBSetProp('VLCOMISIONSERV', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLCOMISIONSERV', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLCOMISIONSERV
* Props for the VLCOMISIONSERV.operario field.
DBSetProp('VLCOMISIONSERV.operario', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.operario', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONSERV.operario', 'Field', 'UpdateName', 'detven.operario')
DBSetProp('VLCOMISIONSERV.operario', 'Field', 'DataType', "N(3)")
* Props for the VLCOMISIONSERV.nombre_a field.
DBSetProp('VLCOMISIONSERV.nombre_a', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.nombre_a', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONSERV.nombre_a', 'Field', 'UpdateName', 'operario.nombre')
DBSetProp('VLCOMISIONSERV.nombre_a', 'Field', 'DataType', "C(30)")
* Props for the VLCOMISIONSERV.compro field.
DBSetProp('VLCOMISIONSERV.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONSERV.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLCOMISIONSERV.compro', 'Field', 'DataType', "C(2)")
* Props for the VLCOMISIONSERV.letra field.
DBSetProp('VLCOMISIONSERV.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONSERV.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLCOMISIONSERV.letra', 'Field', 'DataType', "C(1)")
* Props for the VLCOMISIONSERV.numero field.
DBSetProp('VLCOMISIONSERV.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONSERV.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLCOMISIONSERV.numero', 'Field', 'DataType', "N(12)")
* Props for the VLCOMISIONSERV.fecha field.
DBSetProp('VLCOMISIONSERV.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONSERV.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLCOMISIONSERV.fecha', 'Field', 'DataType', "D")
* Props for the VLCOMISIONSERV.codigo field.
DBSetProp('VLCOMISIONSERV.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONSERV.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLCOMISIONSERV.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLCOMISIONSERV.nombre_b field.
DBSetProp('VLCOMISIONSERV.nombre_b', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.nombre_b', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONSERV.nombre_b', 'Field', 'UpdateName', 'articulo.nombre')
DBSetProp('VLCOMISIONSERV.nombre_b', 'Field', 'DataType', "C(30)")
* Props for the VLCOMISIONSERV.nombre_c field.
DBSetProp('VLCOMISIONSERV.nombre_c', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.nombre_c', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONSERV.nombre_c', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLCOMISIONSERV.nombre_c', 'Field', 'DataType', "C(50)")
* Props for the VLCOMISIONSERV.total field.
DBSetProp('VLCOMISIONSERV.total', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.total', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONSERV.total', 'Field', 'UpdateName', '')
DBSetProp('VLCOMISIONSERV.total', 'Field', 'DataType', "N(13,2)")
* Props for the VLCOMISIONSERV.comisionop field.
DBSetProp('VLCOMISIONSERV.comisionop', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONSERV.comisionop', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONSERV.comisionop', 'Field', 'UpdateName', 'articulo.comisionop')
DBSetProp('VLCOMISIONSERV.comisionop', 'Field', 'DataType', "N(6,2)")
ENDFUNC
 
FUNCTION MakeView_VLPERCEPIBVENDEDOR
***************** Ver la configuración para VLPERCEPIBVENDEDOR ***************

CREATE SQL VIEW "VLPERCEPIBVENDEDOR" ; 
   AS SELECT Clientes.vendedor,  SUM(Facturas.gravado*Codven.mult_ven) AS neto,  SUM(Facturas.percepib*Codven.mult_ven) AS percepib FROM facturas, clientes, codven WHERE Facturas.cliente = Clientes.codigo   AND Facturas.compro = Codven.codigo   AND (Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Facturas.percepib <> 0   AND Codven.mult_ven <> 0) GROUP BY Clientes.vendedor ORDER BY Clientes.vendedor

DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'UpdateType', 1)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'WhereType', 3)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'FetchMemo', .T.)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'SendUpdates', .F.)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'UseMemoSize', 255)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'FetchSize', 100)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'MaxRecords', -1)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'Tables', 'clientes')
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'Prepared', .F.)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'CompareMemo', .T.)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'FetchSize', 100)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'Comment', "")
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLPERCEPIBVENDEDOR', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLPERCEPIBVENDEDOR
* Props for the VLPERCEPIBVENDEDOR.vendedor field.
DBSetProp('VLPERCEPIBVENDEDOR.vendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDOR.vendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBVENDEDOR.vendedor', 'Field', 'UpdateName', 'clientes.vendedor')
DBSetProp('VLPERCEPIBVENDEDOR.vendedor', 'Field', 'DataType', "N(3)")
* Props for the VLPERCEPIBVENDEDOR.neto field.
DBSetProp('VLPERCEPIBVENDEDOR.neto', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDOR.neto', 'Field', 'Updatable', .F.)
DBSetProp('VLPERCEPIBVENDEDOR.neto', 'Field', 'UpdateName', 'Clientes.vendedor*')
DBSetProp('VLPERCEPIBVENDEDOR.neto', 'Field', 'DataType', "N(16,2)")
* Props for the VLPERCEPIBVENDEDOR.percepib field.
DBSetProp('VLPERCEPIBVENDEDOR.percepib', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDOR.percepib', 'Field', 'Updatable', .F.)
DBSetProp('VLPERCEPIBVENDEDOR.percepib', 'Field', 'UpdateName', 'Clientes.vendedor**')
DBSetProp('VLPERCEPIBVENDEDOR.percepib', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLPERCEPIBVENDEDORDETALLADO
***************** Ver la configuración para VLPERCEPIBVENDEDORDETALLADO ***************

CREATE SQL VIEW "VLPERCEPIBVENDEDORDETALLADO" ; 
   AS SELECT Clientes.vendedor, Facturas.compro, Facturas.letra,  Facturas.numero, Facturas.fecha, Facturas.cliente, Facturas.nombre,  Facturas.cuit, (Facturas.gravado*Codven.mult_ven) AS neto,  (Facturas.percepib*Codven.mult_ven) AS percepib, Facturas.noestadist FROM facturas, clientes, codven WHERE Facturas.cliente = Clientes.codigo   AND Facturas.compro = Codven.codigo   AND (Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Facturas.percepib <> 0   AND Codven.mult_ven <> 0) ORDER BY Clientes.vendedor

DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'UpdateType', 1)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'WhereType', 3)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'FetchMemo', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'SendUpdates', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'UseMemoSize', 255)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'FetchSize', 100)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'MaxRecords', -1)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'Tables', 'clientes,facturas')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'Prepared', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'CompareMemo', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'FetchSize', 100)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'Comment', "")
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLPERCEPIBVENDEDORDETALLADO
* Props for the VLPERCEPIBVENDEDORDETALLADO.vendedor field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.vendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.vendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.vendedor', 'Field', 'UpdateName', 'clientes.vendedor')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.vendedor', 'Field', 'DataType', "N(3)")
* Props for the VLPERCEPIBVENDEDORDETALLADO.compro field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.compro', 'Field', 'DataType', "C(2)")
* Props for the VLPERCEPIBVENDEDORDETALLADO.letra field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.letra', 'Field', 'DataType', "C(1)")
* Props for the VLPERCEPIBVENDEDORDETALLADO.numero field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.numero', 'Field', 'DataType', "N(12)")
* Props for the VLPERCEPIBVENDEDORDETALLADO.fecha field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.fecha', 'Field', 'DataType', "D")
* Props for the VLPERCEPIBVENDEDORDETALLADO.cliente field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLPERCEPIBVENDEDORDETALLADO.nombre field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.nombre', 'Field', 'UpdateName', 'facturas.nombre')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLPERCEPIBVENDEDORDETALLADO.cuit field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.cuit', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.cuit', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.cuit', 'Field', 'UpdateName', 'facturas.cuit')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.cuit', 'Field', 'DataType', "N(11)")
* Props for the VLPERCEPIBVENDEDORDETALLADO.neto field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.neto', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.neto', 'Field', 'Updatable', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.neto', 'Field', 'UpdateName', 'Facturas.cuit*')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.neto', 'Field', 'DataType', "N(15,2)")
* Props for the VLPERCEPIBVENDEDORDETALLADO.percepib field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.percepib', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.percepib', 'Field', 'Updatable', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.percepib', 'Field', 'UpdateName', 'Facturas.cuit**')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.percepib', 'Field', 'DataType', "N(15,2)")
* Props for the VLPERCEPIBVENDEDORDETALLADO.noestadist field.
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.noestadist', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.noestadist', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.noestadist', 'Field', 'UpdateName', 'facturas.noestadist')
DBSetProp('VLPERCEPIBVENDEDORDETALLADO.noestadist', 'Field', 'DataType', "L")
ENDFUNC
 
FUNCTION MakeView_VLPERCEPIBSUBCUENTA
***************** Ver la configuración para VLPERCEPIBSUBCUENTA ***************

CREATE SQL VIEW "VLPERCEPIBSUBCUENTA" ; 
   AS SELECT Clientes.subcuenta,  SUM(Facturas.gravado*Codven.mult_ven) AS neto,  SUM(Facturas.percepib*Codven.mult_ven) AS percepib FROM facturas, clientes, codven WHERE Facturas.cliente = Clientes.codigo   AND Facturas.compro = Codven.codigo   AND (Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Facturas.percepib <> 0   AND Codven.mult_ven <> 0) GROUP BY Clientes.subcuenta ORDER BY Clientes.subcuenta

DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'UpdateType', 1)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'WhereType', 3)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'FetchMemo', .T.)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'SendUpdates', .F.)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'UseMemoSize', 255)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'FetchSize', 100)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'MaxRecords', -1)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'Tables', 'clientes')
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'Prepared', .F.)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'CompareMemo', .T.)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'FetchSize', 100)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'Comment', "")
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLPERCEPIBSUBCUENTA', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLPERCEPIBSUBCUENTA
* Props for the VLPERCEPIBSUBCUENTA.subcuenta field.
DBSetProp('VLPERCEPIBSUBCUENTA.subcuenta', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTA.subcuenta', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBSUBCUENTA.subcuenta', 'Field', 'UpdateName', 'clientes.subcuenta')
DBSetProp('VLPERCEPIBSUBCUENTA.subcuenta', 'Field', 'DataType', "N(6)")
* Props for the VLPERCEPIBSUBCUENTA.neto field.
DBSetProp('VLPERCEPIBSUBCUENTA.neto', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTA.neto', 'Field', 'Updatable', .F.)
DBSetProp('VLPERCEPIBSUBCUENTA.neto', 'Field', 'UpdateName', 'Clientes.vendedor*')
DBSetProp('VLPERCEPIBSUBCUENTA.neto', 'Field', 'DataType', "N(16,2)")
* Props for the VLPERCEPIBSUBCUENTA.percepib field.
DBSetProp('VLPERCEPIBSUBCUENTA.percepib', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTA.percepib', 'Field', 'Updatable', .F.)
DBSetProp('VLPERCEPIBSUBCUENTA.percepib', 'Field', 'UpdateName', 'Clientes.vendedor**')
DBSetProp('VLPERCEPIBSUBCUENTA.percepib', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLPERCEPIBSUBCUENTADETALLADO
***************** Ver la configuración para VLPERCEPIBSUBCUENTADETALLADO ***************

CREATE SQL VIEW "VLPERCEPIBSUBCUENTADETALLADO" ; 
   AS SELECT Clientes.subcuenta, Facturas.compro, Facturas.letra,  Facturas.numero, Facturas.fecha, Facturas.cliente, Facturas.nombre,  Facturas.cuit, (Facturas.gravado*Codven.mult_ven) AS neto,  (Facturas.percepib*Codven.mult_ven) AS percepib, Facturas.noestadist FROM facturas, clientes, codven WHERE Facturas.cliente = Clientes.codigo   AND Facturas.compro = Codven.codigo   AND (Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Facturas.percepib <> 0   AND Codven.mult_ven <> 0) GROUP BY Clientes.subcuenta ORDER BY Clientes.subcuenta

DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'UpdateType', 1)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'WhereType', 3)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'FetchMemo', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'SendUpdates', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'UseMemoSize', 255)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'FetchSize', 100)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'MaxRecords', -1)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'Tables', 'clientes,facturas')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'Prepared', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'CompareMemo', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'FetchSize', 100)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'Comment', "")
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLPERCEPIBSUBCUENTADETALLADO
* Props for the VLPERCEPIBSUBCUENTADETALLADO.subcuenta field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.subcuenta', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.subcuenta', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.subcuenta', 'Field', 'UpdateName', 'clientes.subcuenta')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.subcuenta', 'Field', 'DataType', "N(6)")
* Props for the VLPERCEPIBSUBCUENTADETALLADO.compro field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.compro', 'Field', 'DataType', "C(2)")
* Props for the VLPERCEPIBSUBCUENTADETALLADO.letra field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.letra', 'Field', 'DataType', "C(1)")
* Props for the VLPERCEPIBSUBCUENTADETALLADO.numero field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.numero', 'Field', 'DataType', "N(12)")
* Props for the VLPERCEPIBSUBCUENTADETALLADO.fecha field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.fecha', 'Field', 'DataType', "D")
* Props for the VLPERCEPIBSUBCUENTADETALLADO.cliente field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLPERCEPIBSUBCUENTADETALLADO.nombre field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.nombre', 'Field', 'UpdateName', 'facturas.nombre')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLPERCEPIBSUBCUENTADETALLADO.cuit field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.cuit', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.cuit', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.cuit', 'Field', 'UpdateName', 'facturas.cuit')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.cuit', 'Field', 'DataType', "N(11)")
* Props for the VLPERCEPIBSUBCUENTADETALLADO.neto field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.neto', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.neto', 'Field', 'Updatable', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.neto', 'Field', 'UpdateName', 'Facturas.cuit*')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.neto', 'Field', 'DataType', "N(15,2)")
* Props for the VLPERCEPIBSUBCUENTADETALLADO.percepib field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.percepib', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.percepib', 'Field', 'Updatable', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.percepib', 'Field', 'UpdateName', 'Facturas.cuit**')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.percepib', 'Field', 'DataType', "N(15,2)")
* Props for the VLPERCEPIBSUBCUENTADETALLADO.noestadist field.
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.noestadist', 'Field', 'KeyField', .F.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.noestadist', 'Field', 'Updatable', .T.)
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.noestadist', 'Field', 'UpdateName', 'facturas.noestadist')
DBSetProp('VLPERCEPIBSUBCUENTADETALLADO.noestadist', 'Field', 'DataType', "L")
ENDFUNC
 
FUNCTION MakeView_VLVENTACOMPROREALIZADO
***************** Ver la configuración para VLVENTACOMPROREALIZADO ***************

CREATE SQL VIEW "VLVENTACOMPROREALIZADO" ; 
   AS SELECT Facturas.sucursal, Facturas.fecha, Facturas.compro,  Facturas.letra, Facturas.numero, Facturas.condicion, Facturas.cliente,  Clientes.nombre, Clientes.caractel, Clientes.telefono, Clientes.movil,  Clientes.fax, Clientes.mail, Facturas.total*Codven.mult_ven AS total,  Facturas.entrega*Codven.mult_ven AS entrega, Facturas.estado,  Facturas.operador, Facturas.fechapago, Clientes.vendedor,  Vendedor.nombre AS nomvendedor, Facturas.usuario FROM facturas, codven, clientes, vendedor WHERE Facturas.compro = Codven.compro   AND Facturas.cliente = Clientes.codigo   AND Clientes.vendedor = Vendedor.codigo   AND (Codven.mult_ven <> 0   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta) ORDER BY Facturas.fecha

DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'UpdateType', 1)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'WhereType', 3)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'FetchSize', 100)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'Tables', 'facturas,clientes,vendedor')
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'Prepared', .F.)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'FetchSize', 100)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'Comment', "")
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTACOMPROREALIZADO', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTACOMPROREALIZADO
* Props for the VLVENTACOMPROREALIZADO.sucursal field.
DBSetProp('VLVENTACOMPROREALIZADO.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLVENTACOMPROREALIZADO.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLVENTACOMPROREALIZADO.fecha field.
DBSetProp('VLVENTACOMPROREALIZADO.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTACOMPROREALIZADO.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTACOMPROREALIZADO.compro field.
DBSetProp('VLVENTACOMPROREALIZADO.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLVENTACOMPROREALIZADO.compro', 'Field', 'DataType', "C(2)")
* Props for the VLVENTACOMPROREALIZADO.letra field.
DBSetProp('VLVENTACOMPROREALIZADO.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLVENTACOMPROREALIZADO.letra', 'Field', 'DataType', "C(1)")
* Props for the VLVENTACOMPROREALIZADO.numero field.
DBSetProp('VLVENTACOMPROREALIZADO.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLVENTACOMPROREALIZADO.numero', 'Field', 'DataType', "N(12)")
* Props for the VLVENTACOMPROREALIZADO.condicion field.
DBSetProp('VLVENTACOMPROREALIZADO.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.condicion', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.condicion', 'Field', 'UpdateName', 'facturas.condicion')
DBSetProp('VLVENTACOMPROREALIZADO.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLVENTACOMPROREALIZADO.cliente field.
DBSetProp('VLVENTACOMPROREALIZADO.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLVENTACOMPROREALIZADO.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLVENTACOMPROREALIZADO.nombre field.
DBSetProp('VLVENTACOMPROREALIZADO.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLVENTACOMPROREALIZADO.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLVENTACOMPROREALIZADO.caractel field.
DBSetProp('VLVENTACOMPROREALIZADO.caractel', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.caractel', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.caractel', 'Field', 'UpdateName', 'clientes.caractel')
DBSetProp('VLVENTACOMPROREALIZADO.caractel', 'Field', 'DataType', "C(5)")
* Props for the VLVENTACOMPROREALIZADO.telefono field.
DBSetProp('VLVENTACOMPROREALIZADO.telefono', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.telefono', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.telefono', 'Field', 'UpdateName', 'clientes.telefono')
DBSetProp('VLVENTACOMPROREALIZADO.telefono', 'Field', 'DataType', "C(15)")
* Props for the VLVENTACOMPROREALIZADO.movil field.
DBSetProp('VLVENTACOMPROREALIZADO.movil', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.movil', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.movil', 'Field', 'UpdateName', 'clientes.movil')
DBSetProp('VLVENTACOMPROREALIZADO.movil', 'Field', 'DataType', "C(15)")
* Props for the VLVENTACOMPROREALIZADO.fax field.
DBSetProp('VLVENTACOMPROREALIZADO.fax', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.fax', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.fax', 'Field', 'UpdateName', 'clientes.fax')
DBSetProp('VLVENTACOMPROREALIZADO.fax', 'Field', 'DataType', "C(15)")
* Props for the VLVENTACOMPROREALIZADO.mail field.
DBSetProp('VLVENTACOMPROREALIZADO.mail', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.mail', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.mail', 'Field', 'UpdateName', 'clientes.mail')
DBSetProp('VLVENTACOMPROREALIZADO.mail', 'Field', 'DataType', "C(50)")
* Props for the VLVENTACOMPROREALIZADO.total field.
DBSetProp('VLVENTACOMPROREALIZADO.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.total', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.total', 'Field', 'UpdateName', 'Clientes.movil*')
DBSetProp('VLVENTACOMPROREALIZADO.total', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTACOMPROREALIZADO.entrega field.
DBSetProp('VLVENTACOMPROREALIZADO.entrega', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.entrega', 'Field', 'Updatable', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.entrega', 'Field', 'UpdateName', 'Clientes.mail**')
DBSetProp('VLVENTACOMPROREALIZADO.entrega', 'Field', 'DataType', "N(15,2)")
* Props for the VLVENTACOMPROREALIZADO.estado field.
DBSetProp('VLVENTACOMPROREALIZADO.estado', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.estado', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.estado', 'Field', 'UpdateName', 'facturas.estado')
DBSetProp('VLVENTACOMPROREALIZADO.estado', 'Field', 'DataType', "C(1)")
* Props for the VLVENTACOMPROREALIZADO.operador field.
DBSetProp('VLVENTACOMPROREALIZADO.operador', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.operador', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.operador', 'Field', 'UpdateName', 'facturas.operador')
DBSetProp('VLVENTACOMPROREALIZADO.operador', 'Field', 'DataType', "C(2)")
* Props for the VLVENTACOMPROREALIZADO.fechapago field.
DBSetProp('VLVENTACOMPROREALIZADO.fechapago', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.fechapago', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.fechapago', 'Field', 'UpdateName', 'facturas.fechapago')
DBSetProp('VLVENTACOMPROREALIZADO.fechapago', 'Field', 'DataType', "D")
* Props for the VLVENTACOMPROREALIZADO.vendedor field.
DBSetProp('VLVENTACOMPROREALIZADO.vendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.vendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.vendedor', 'Field', 'UpdateName', 'clientes.vendedor')
DBSetProp('VLVENTACOMPROREALIZADO.vendedor', 'Field', 'DataType', "N(3)")
* Props for the VLVENTACOMPROREALIZADO.nomvendedor field.
DBSetProp('VLVENTACOMPROREALIZADO.nomvendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.nomvendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.nomvendedor', 'Field', 'UpdateName', 'vendedor.nombre')
DBSetProp('VLVENTACOMPROREALIZADO.nomvendedor', 'Field', 'DataType', "C(30)")
* Props for the VLVENTACOMPROREALIZADO.usuario field.
DBSetProp('VLVENTACOMPROREALIZADO.usuario', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROREALIZADO.usuario', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROREALIZADO.usuario', 'Field', 'UpdateName', 'facturas.usuario')
DBSetProp('VLVENTACOMPROREALIZADO.usuario', 'Field', 'DataType', "C(15)")
ENDFUNC
 
FUNCTION MakeView_VLMOVSTOCKTOTAL
***************** Ver la configuración para VLMOVSTOCKTOTAL ***************

CREATE SQL VIEW "VLMOVSTOCKTOTAL" ; 
   AS SELECT Movstock.fecha, Movstock.descripcio, Detven.codigo, Lista.medida,  Marcas.nombre AS marca, Lista.nombre, Detven.cantidad FROM marcas, movstock,   detven INNER JOIN lista    ON  Detven.codigo = Lista.codigo WHERE Lista.marca = Marcas.codigo   AND Detven.compro = Movstock.compro   AND Detven.numero = Movstock.numero   AND (Detven.compro = "MI"   AND Movstock.fecha BETWEEN ?dDesde AND ?dHasta) ORDER BY Movstock.fecha

DBSetProp('VLMOVSTOCKTOTAL', 'View', 'UpdateType', 1)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'WhereType', 3)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'FetchMemo', .T.)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'SendUpdates', .F.)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'UseMemoSize', 255)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'FetchSize', 100)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'MaxRecords', -1)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'Tables', '')
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'Prepared', .F.)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'CompareMemo', .T.)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'FetchSize', 100)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'Comment', "")
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLMOVSTOCKTOTAL', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLMOVSTOCKTOTAL
* Props for the VLMOVSTOCKTOTAL.fecha field.
DBSetProp('VLMOVSTOCKTOTAL.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCKTOTAL.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCKTOTAL.fecha', 'Field', 'UpdateName', 'movstock.fecha')
DBSetProp('VLMOVSTOCKTOTAL.fecha', 'Field', 'DataType', "D")
* Props for the VLMOVSTOCKTOTAL.descripcio field.
DBSetProp('VLMOVSTOCKTOTAL.descripcio', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCKTOTAL.descripcio', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCKTOTAL.descripcio', 'Field', 'UpdateName', 'movstock.descripcio')
DBSetProp('VLMOVSTOCKTOTAL.descripcio', 'Field', 'DataType', "C(40)")
* Props for the VLMOVSTOCKTOTAL.codigo field.
DBSetProp('VLMOVSTOCKTOTAL.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCKTOTAL.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCKTOTAL.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLMOVSTOCKTOTAL.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLMOVSTOCKTOTAL.medida field.
DBSetProp('VLMOVSTOCKTOTAL.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCKTOTAL.medida', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCKTOTAL.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLMOVSTOCKTOTAL.medida', 'Field', 'DataType', "C(10)")
* Props for the VLMOVSTOCKTOTAL.marca field.
DBSetProp('VLMOVSTOCKTOTAL.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCKTOTAL.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCKTOTAL.marca', 'Field', 'UpdateName', 'marcas.nombre')
DBSetProp('VLMOVSTOCKTOTAL.marca', 'Field', 'DataType', "C(20)")
* Props for the VLMOVSTOCKTOTAL.nombre field.
DBSetProp('VLMOVSTOCKTOTAL.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCKTOTAL.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCKTOTAL.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLMOVSTOCKTOTAL.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLMOVSTOCKTOTAL.cantidad field.
DBSetProp('VLMOVSTOCKTOTAL.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLMOVSTOCKTOTAL.cantidad', 'Field', 'Updatable', .F.)
DBSetProp('VLMOVSTOCKTOTAL.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLMOVSTOCKTOTAL.cantidad', 'Field', 'DataType', "N(7,2)")
ENDFUNC
 
FUNCTION MakeView_VLPRECIOS
***************** Ver la configuración para VLPRECIOS ***************

CREATE SQL VIEW "VLPRECIOS" ; 
   AS SELECT Lista.codigo, Lista.orden, Marcas.nombre AS marca, Lista.nombre,  Lista.medida, Lista.precio,  ROUND(Lista.precio*(Param.precio1/100+1),2) AS precio2,  ROUND(Lista.precio*(Param.precio2/100+1),2) AS precio3,  ROUND(Lista.precio*(Param.precio3/100+1),2) AS precio4,  ROUND(Lista.precio-(Lista.precio*Lista.descuento/100),2) AS promo,  Lista.codfabrica, Marcas.otras, SUM(Stock.stock) AS stock, Lista.minimo,  Lista.unidad, Lista.estado, Marcas.moneda, Lista.fecha FROM lista, marcas, param, stock WHERE Lista.marca = Marcas.codigo   AND Lista.codigo = Stock.codigo   AND Lista.medida = ?cMedida GROUP BY Lista.codigo ORDER BY Lista.codfabrica, Lista.fecha

DBSetProp('VLPRECIOS', 'View', 'UpdateType', 1)
DBSetProp('VLPRECIOS', 'View', 'WhereType', 3)
DBSetProp('VLPRECIOS', 'View', 'FetchMemo', .T.)
DBSetProp('VLPRECIOS', 'View', 'SendUpdates', .F.)
DBSetProp('VLPRECIOS', 'View', 'UseMemoSize', 255)
DBSetProp('VLPRECIOS', 'View', 'FetchSize', 100)
DBSetProp('VLPRECIOS', 'View', 'MaxRecords', -1)
DBSetProp('VLPRECIOS', 'View', 'Tables', 'lista')
DBSetProp('VLPRECIOS', 'View', 'Prepared', .F.)
DBSetProp('VLPRECIOS', 'View', 'CompareMemo', .T.)
DBSetProp('VLPRECIOS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLPRECIOS', 'View', 'FetchSize', 100)
DBSetProp('VLPRECIOS', 'View', 'Comment', "")
DBSetProp('VLPRECIOS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLPRECIOS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLPRECIOS
* Props for the VLPRECIOS.codigo field.
DBSetProp('VLPRECIOS.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.codigo', 'Field', 'UpdateName', 'lista.codigo')
DBSetProp('VLPRECIOS.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLPRECIOS.orden field.
DBSetProp('VLPRECIOS.orden', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.orden', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.orden', 'Field', 'UpdateName', 'lista.orden')
DBSetProp('VLPRECIOS.orden', 'Field', 'DataType', "N(3)")
* Props for the VLPRECIOS.marca field.
DBSetProp('VLPRECIOS.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.marca', 'Field', 'UpdateName', 'marcas.nombre')
DBSetProp('VLPRECIOS.marca', 'Field', 'DataType', "C(20)")
* Props for the VLPRECIOS.nombre field.
DBSetProp('VLPRECIOS.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLPRECIOS.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLPRECIOS.medida field.
DBSetProp('VLPRECIOS.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.medida', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLPRECIOS.medida', 'Field', 'DataType', "C(13)")
* Props for the VLPRECIOS.precio field.
DBSetProp('VLPRECIOS.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.precio', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.precio', 'Field', 'UpdateName', 'lista.precio')
DBSetProp('VLPRECIOS.precio', 'Field', 'DataType', "N(12,2)")
* Props for the VLPRECIOS.precio2 field.
DBSetProp('VLPRECIOS.precio2', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.precio2', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.precio2', 'Field', 'UpdateName', 'param.precio2')
DBSetProp('VLPRECIOS.precio2', 'Field', 'DataType', "N(20,2)")
* Props for the VLPRECIOS.precio3 field.
DBSetProp('VLPRECIOS.precio3', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.precio3', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.precio3', 'Field', 'UpdateName', 'param.precio3')
DBSetProp('VLPRECIOS.precio3', 'Field', 'DataType', "N(20,2)")
* Props for the VLPRECIOS.precio4 field.
DBSetProp('VLPRECIOS.precio4', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.precio4', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.precio4', 'Field', 'UpdateName', 'precio4')
DBSetProp('VLPRECIOS.precio4', 'Field', 'DataType', "N(20,2)")
* Props for the VLPRECIOS.promo field.
DBSetProp('VLPRECIOS.promo', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.promo', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.promo', 'Field', 'UpdateName', 'promo')
DBSetProp('VLPRECIOS.promo', 'Field', 'DataType', "N(20,2)")
* Props for the VLPRECIOS.codfabrica field.
DBSetProp('VLPRECIOS.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.codfabrica', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLPRECIOS.codfabrica', 'Field', 'DataType', "C(15)")
* Props for the VLPRECIOS.otras field.
DBSetProp('VLPRECIOS.otras', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.otras', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.otras', 'Field', 'UpdateName', 'marcas.otras')
DBSetProp('VLPRECIOS.otras', 'Field', 'DataType', "L")
* Props for the VLPRECIOS.stock field.
DBSetProp('VLPRECIOS.stock', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.stock', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.stock', 'Field', 'UpdateName', 'stock')
DBSetProp('VLPRECIOS.stock', 'Field', 'DataType', "N(16,2)")
* Props for the VLPRECIOS.minimo field.
DBSetProp('VLPRECIOS.minimo', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.minimo', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIOS.minimo', 'Field', 'UpdateName', 'lista.minimo')
DBSetProp('VLPRECIOS.minimo', 'Field', 'DataType', "N(4)")
* Props for the VLPRECIOS.unidad field.
DBSetProp('VLPRECIOS.unidad', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.unidad', 'Field', 'Updatable', .T.)
DBSetProp('VLPRECIOS.unidad', 'Field', 'UpdateName', 'lista.unidad')
DBSetProp('VLPRECIOS.unidad', 'Field', 'DataType', "N(4)")
* Props for the VLPRECIOS.estado field.
DBSetProp('VLPRECIOS.estado', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.estado', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.estado', 'Field', 'UpdateName', 'lista.estado')
DBSetProp('VLPRECIOS.estado', 'Field', 'DataType', "C(1)")
* Props for the VLPRECIOS.moneda field.
DBSetProp('VLPRECIOS.moneda', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.moneda', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.moneda', 'Field', 'UpdateName', 'marcas.moneda')
DBSetProp('VLPRECIOS.moneda', 'Field', 'DataType', "C(1)")
* Props for the VLPRECIOS.fecha field.
DBSetProp('VLPRECIOS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLPRECIOS.fecha', 'Field', 'Updatable', .F.)
DBSetProp('VLPRECIOS.fecha', 'Field', 'UpdateName', 'lista.fecha')
DBSetProp('VLPRECIOS.fecha', 'Field', 'DataType', "C(6)")
ENDFUNC
 
FUNCTION MakeView_VLSTOCKVENTAS
***************** Ver la configuración para VLSTOCKVENTAS ***************

CREATE SQL VIEW "VLSTOCKVENTAS" ; 
   AS SELECT Detven.compro, Detven.letra, Detven.numero, Facturas.fecha,  Facturas.nombre AS cliente, Detven.codigo, Lista.nombre, Lista.medida,  Lista.codfabrica, Detven.cantidad*Codven.mult_sto AS cantidad,  Facturas.sucursal, Facturas.operador, Facturas.usuario FROM detven, codven, lista, facturas WHERE Detven.id = Facturas.id   AND Detven.compro = Codven.compro   AND Detven.codigo = Lista.codigo   AND (Lista.tipo = "P"   AND Codven.mult_sto <> 0   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Facturas.sucursal = ?nSucursal) ORDER BY Detven.codigo

DBSetProp('VLSTOCKVENTAS', 'View', 'UpdateType', 1)
DBSetProp('VLSTOCKVENTAS', 'View', 'WhereType', 3)
DBSetProp('VLSTOCKVENTAS', 'View', 'FetchMemo', .T.)
DBSetProp('VLSTOCKVENTAS', 'View', 'SendUpdates', .F.)
DBSetProp('VLSTOCKVENTAS', 'View', 'UseMemoSize', 255)
DBSetProp('VLSTOCKVENTAS', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKVENTAS', 'View', 'MaxRecords', -1)
DBSetProp('VLSTOCKVENTAS', 'View', 'Tables', 'detven,facturas,lista')
DBSetProp('VLSTOCKVENTAS', 'View', 'Prepared', .F.)
DBSetProp('VLSTOCKVENTAS', 'View', 'CompareMemo', .T.)
DBSetProp('VLSTOCKVENTAS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSTOCKVENTAS', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKVENTAS', 'View', 'Comment', "")
DBSetProp('VLSTOCKVENTAS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSTOCKVENTAS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSTOCKVENTAS
* Props for the VLSTOCKVENTAS.compro field.
DBSetProp('VLSTOCKVENTAS.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLSTOCKVENTAS.compro', 'Field', 'DataType', "C(2)")
* Props for the VLSTOCKVENTAS.letra field.
DBSetProp('VLSTOCKVENTAS.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLSTOCKVENTAS.letra', 'Field', 'DataType', "C(1)")
* Props for the VLSTOCKVENTAS.numero field.
DBSetProp('VLSTOCKVENTAS.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLSTOCKVENTAS.numero', 'Field', 'DataType', "N(12)")
* Props for the VLSTOCKVENTAS.fecha field.
DBSetProp('VLSTOCKVENTAS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLSTOCKVENTAS.fecha', 'Field', 'DataType', "D")
* Props for the VLSTOCKVENTAS.cliente field.
DBSetProp('VLSTOCKVENTAS.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.cliente', 'Field', 'UpdateName', 'facturas.nombre')
DBSetProp('VLSTOCKVENTAS.cliente', 'Field', 'DataType', "C(30)")
* Props for the VLSTOCKVENTAS.codigo field.
DBSetProp('VLSTOCKVENTAS.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLSTOCKVENTAS.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCKVENTAS.nombre field.
DBSetProp('VLSTOCKVENTAS.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLSTOCKVENTAS.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLSTOCKVENTAS.medida field.
DBSetProp('VLSTOCKVENTAS.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.medida', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLSTOCKVENTAS.medida', 'Field', 'DataType', "C(13)")
* Props for the VLSTOCKVENTAS.codfabrica field.
DBSetProp('VLSTOCKVENTAS.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.codfabrica', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLSTOCKVENTAS.codfabrica', 'Field', 'DataType', "C(15)")
* Props for the VLSTOCKVENTAS.cantidad field.
DBSetProp('VLSTOCKVENTAS.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.cantidad', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKVENTAS.cantidad', 'Field', 'UpdateName', 'Lista.nombre*')
DBSetProp('VLSTOCKVENTAS.cantidad', 'Field', 'DataType', "N(10,2)")
* Props for the VLSTOCKVENTAS.sucursal field.
DBSetProp('VLSTOCKVENTAS.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLSTOCKVENTAS.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLSTOCKVENTAS.operador field.
DBSetProp('VLSTOCKVENTAS.operador', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.operador', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.operador', 'Field', 'UpdateName', 'facturas.operador')
DBSetProp('VLSTOCKVENTAS.operador', 'Field', 'DataType', "C(2)")
* Props for the VLSTOCKVENTAS.usuario field.
DBSetProp('VLSTOCKVENTAS.usuario', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKVENTAS.usuario', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKVENTAS.usuario', 'Field', 'UpdateName', 'facturas.usuario')
DBSetProp('VLSTOCKVENTAS.usuario', 'Field', 'DataType', "C(15)")
ENDFUNC
 
FUNCTION MakeView_VLSTOCKCLIENTES
***************** Ver la configuración para VLSTOCKCLIENTES ***************

CREATE SQL VIEW "VLSTOCKCLIENTES" ; 
   AS SELECT Stockcliente.id, Stockcliente.codigo, Lista.medida,  Lista.codfabrica, Stockcliente.cantidad, Stockcliente.retirado,  Facturas.compro, Facturas.letra, Facturas.numero, Facturas.cliente,  Facturas.fecha, Facturas.sucursal FROM stockcliente, facturas, lista WHERE Stockcliente.id = Facturas.id   AND Stockcliente.codigo = Lista.codigo   AND Stockcliente.cantidad <> Stockcliente.retirado ORDER BY Facturas.cliente, Stockcliente.id

DBSetProp('VLSTOCKCLIENTES', 'View', 'UpdateType', 1)
DBSetProp('VLSTOCKCLIENTES', 'View', 'WhereType', 3)
DBSetProp('VLSTOCKCLIENTES', 'View', 'FetchMemo', .T.)
DBSetProp('VLSTOCKCLIENTES', 'View', 'SendUpdates', .F.)
DBSetProp('VLSTOCKCLIENTES', 'View', 'UseMemoSize', 255)
DBSetProp('VLSTOCKCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKCLIENTES', 'View', 'MaxRecords', -1)
DBSetProp('VLSTOCKCLIENTES', 'View', 'Tables', 'stockcliente,lista,facturas')
DBSetProp('VLSTOCKCLIENTES', 'View', 'Prepared', .F.)
DBSetProp('VLSTOCKCLIENTES', 'View', 'CompareMemo', .T.)
DBSetProp('VLSTOCKCLIENTES', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSTOCKCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKCLIENTES', 'View', 'Comment', "")
DBSetProp('VLSTOCKCLIENTES', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSTOCKCLIENTES', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSTOCKCLIENTES
* Props for the VLSTOCKCLIENTES.id field.
DBSetProp('VLSTOCKCLIENTES.id', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.id', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.id', 'Field', 'UpdateName', 'stockcliente.id')
DBSetProp('VLSTOCKCLIENTES.id', 'Field', 'DataType', "N(7)")
* Props for the VLSTOCKCLIENTES.codigo field.
DBSetProp('VLSTOCKCLIENTES.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.codigo', 'Field', 'UpdateName', 'stockcliente.codigo')
DBSetProp('VLSTOCKCLIENTES.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCKCLIENTES.medida field.
DBSetProp('VLSTOCKCLIENTES.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.medida', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLSTOCKCLIENTES.medida', 'Field', 'DataType', "C(10)")
* Props for the VLSTOCKCLIENTES.codfabrica field.
DBSetProp('VLSTOCKCLIENTES.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.codfabrica', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLSTOCKCLIENTES.codfabrica', 'Field', 'DataType', "C(8)")
* Props for the VLSTOCKCLIENTES.cantidad field.
DBSetProp('VLSTOCKCLIENTES.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.cantidad', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.cantidad', 'Field', 'UpdateName', 'stockcliente.cantidad')
DBSetProp('VLSTOCKCLIENTES.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLSTOCKCLIENTES.retirado field.
DBSetProp('VLSTOCKCLIENTES.retirado', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.retirado', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.retirado', 'Field', 'UpdateName', 'stockcliente.retirado')
DBSetProp('VLSTOCKCLIENTES.retirado', 'Field', 'DataType', "N(7,2)")
* Props for the VLSTOCKCLIENTES.compro field.
DBSetProp('VLSTOCKCLIENTES.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLSTOCKCLIENTES.compro', 'Field', 'DataType', "C(2)")
* Props for the VLSTOCKCLIENTES.letra field.
DBSetProp('VLSTOCKCLIENTES.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLSTOCKCLIENTES.letra', 'Field', 'DataType', "C(1)")
* Props for the VLSTOCKCLIENTES.numero field.
DBSetProp('VLSTOCKCLIENTES.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLSTOCKCLIENTES.numero', 'Field', 'DataType', "N(12)")
* Props for the VLSTOCKCLIENTES.cliente field.
DBSetProp('VLSTOCKCLIENTES.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLSTOCKCLIENTES.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCKCLIENTES.fecha field.
DBSetProp('VLSTOCKCLIENTES.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLSTOCKCLIENTES.fecha', 'Field', 'DataType', "D")
* Props for the VLSTOCKCLIENTES.sucursal field.
DBSetProp('VLSTOCKCLIENTES.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKCLIENTES.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKCLIENTES.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLSTOCKCLIENTES.sucursal', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLSTOCKDEPOSITO
***************** Ver la configuración para VLSTOCKDEPOSITO ***************

CREATE SQL VIEW "VLSTOCKDEPOSITO" ; 
   AS SELECT Stockcliente.codigo, Lista.medida, Lista.modelo, Lista.articulo,  Lista.codfabrica, Lista.marca, Lista.nombre,  SUM(Stockcliente.cantidad-Stockcliente.retirado) AS stock FROM stockcliente, lista WHERE Stockcliente.codigo = Lista.codigo   AND Stockcliente.cantidad <> Stockcliente.retirado GROUP BY Stockcliente.codigo ORDER BY Lista.articulo, Lista.modelo, Lista.marca, Lista.medida

DBSetProp('VLSTOCKDEPOSITO', 'View', 'UpdateType', 1)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'WhereType', 3)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'FetchMemo', .T.)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'SendUpdates', .F.)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'UseMemoSize', 255)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'MaxRecords', -1)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'Tables', 'stockcliente,lista')
DBSetProp('VLSTOCKDEPOSITO', 'View', 'Prepared', .F.)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'CompareMemo', .T.)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'Comment', "")
DBSetProp('VLSTOCKDEPOSITO', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSTOCKDEPOSITO', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSTOCKDEPOSITO
* Props for the VLSTOCKDEPOSITO.codigo field.
DBSetProp('VLSTOCKDEPOSITO.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITO.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKDEPOSITO.codigo', 'Field', 'UpdateName', 'stockcliente.codigo')
DBSetProp('VLSTOCKDEPOSITO.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCKDEPOSITO.medida field.
DBSetProp('VLSTOCKDEPOSITO.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITO.medida', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKDEPOSITO.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLSTOCKDEPOSITO.medida', 'Field', 'DataType', "C(10)")
* Props for the VLSTOCKDEPOSITO.modelo field.
DBSetProp('VLSTOCKDEPOSITO.modelo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITO.modelo', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKDEPOSITO.modelo', 'Field', 'UpdateName', 'lista.modelo')
DBSetProp('VLSTOCKDEPOSITO.modelo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCKDEPOSITO.articulo field.
DBSetProp('VLSTOCKDEPOSITO.articulo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITO.articulo', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKDEPOSITO.articulo', 'Field', 'UpdateName', 'lista.articulo')
DBSetProp('VLSTOCKDEPOSITO.articulo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCKDEPOSITO.codfabrica field.
DBSetProp('VLSTOCKDEPOSITO.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITO.codfabrica', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKDEPOSITO.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLSTOCKDEPOSITO.codfabrica', 'Field', 'DataType', "C(8)")
* Props for the VLSTOCKDEPOSITO.marca field.
DBSetProp('VLSTOCKDEPOSITO.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITO.marca', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKDEPOSITO.marca', 'Field', 'UpdateName', 'lista.marca')
DBSetProp('VLSTOCKDEPOSITO.marca', 'Field', 'DataType', "N(3)")
* Props for the VLSTOCKDEPOSITO.nombre field.
DBSetProp('VLSTOCKDEPOSITO.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITO.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLSTOCKDEPOSITO.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLSTOCKDEPOSITO.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLSTOCKDEPOSITO.stock field.
DBSetProp('VLSTOCKDEPOSITO.stock', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITO.stock', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKDEPOSITO.stock', 'Field', 'UpdateName', '')
DBSetProp('VLSTOCKDEPOSITO.stock', 'Field', 'DataType', "N(16,2)")
ENDFUNC
 
FUNCTION MakeView_VLSTOCKDEPOSITOSUC
***************** Ver la configuración para VLSTOCKDEPOSITOSUC ***************

CREATE SQL VIEW "VLSTOCKDEPOSITOSUC" ; 
   AS SELECT Stockcliente.codigo, Lista.medida, Lista.modelo, Lista.articulo,  Lista.codfabrica, Lista.marca, Lista.nombre,  SUM(Stockcliente.cantidad-Stockcliente.retirado) AS stock,  Facturas.sucursal FROM stockcliente, lista, facturas WHERE Stockcliente.id = Facturas.id   AND Stockcliente.codigo = Lista.codigo   AND (Stockcliente.cantidad <> Stockcliente.retirado   AND Facturas.sucursal = ?nSucursal) GROUP BY Stockcliente.codigo ORDER BY Lista.articulo, Lista.modelo, Lista.marca, Lista.medida

DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'UpdateType', 1)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'WhereType', 3)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'FetchMemo', .T.)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'SendUpdates', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'UseMemoSize', 255)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'MaxRecords', -1)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'Tables', '')
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'Prepared', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'CompareMemo', .T.)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'Comment', "")
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSTOCKDEPOSITOSUC', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSTOCKDEPOSITOSUC
* Props for the VLSTOCKDEPOSITOSUC.codigo field.
DBSetProp('VLSTOCKDEPOSITOSUC.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.codigo', 'Field', 'UpdateName', 'stockcliente.codigo')
DBSetProp('VLSTOCKDEPOSITOSUC.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCKDEPOSITOSUC.medida field.
DBSetProp('VLSTOCKDEPOSITOSUC.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.medida', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLSTOCKDEPOSITOSUC.medida', 'Field', 'DataType', "C(10)")
* Props for the VLSTOCKDEPOSITOSUC.modelo field.
DBSetProp('VLSTOCKDEPOSITOSUC.modelo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.modelo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.modelo', 'Field', 'UpdateName', 'lista.modelo')
DBSetProp('VLSTOCKDEPOSITOSUC.modelo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCKDEPOSITOSUC.articulo field.
DBSetProp('VLSTOCKDEPOSITOSUC.articulo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.articulo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.articulo', 'Field', 'UpdateName', 'lista.articulo')
DBSetProp('VLSTOCKDEPOSITOSUC.articulo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCKDEPOSITOSUC.codfabrica field.
DBSetProp('VLSTOCKDEPOSITOSUC.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.codfabrica', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLSTOCKDEPOSITOSUC.codfabrica', 'Field', 'DataType', "C(8)")
* Props for the VLSTOCKDEPOSITOSUC.marca field.
DBSetProp('VLSTOCKDEPOSITOSUC.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.marca', 'Field', 'UpdateName', 'lista.marca')
DBSetProp('VLSTOCKDEPOSITOSUC.marca', 'Field', 'DataType', "N(3)")
* Props for the VLSTOCKDEPOSITOSUC.nombre field.
DBSetProp('VLSTOCKDEPOSITOSUC.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLSTOCKDEPOSITOSUC.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLSTOCKDEPOSITOSUC.stock field.
DBSetProp('VLSTOCKDEPOSITOSUC.stock', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.stock', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.stock', 'Field', 'UpdateName', '')
DBSetProp('VLSTOCKDEPOSITOSUC.stock', 'Field', 'DataType', "N(16,2)")
* Props for the VLSTOCKDEPOSITOSUC.sucursal field.
DBSetProp('VLSTOCKDEPOSITOSUC.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.sucursal', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKDEPOSITOSUC.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLSTOCKDEPOSITOSUC.sucursal', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLREMITOSPENDIENTES
***************** Ver la configuración para VLREMITOSPENDIENTES ***************

CREATE SQL VIEW "VLREMITOSPENDIENTES" ; 
   AS SELECT Detven.compro, Detven.letra, Detven.numero, Facturas.fecha,  Facturas.cliente, Clientes.nombre, Detven.codigo,  Lista.nombre AS descripcion, Lista.codfabrica, Lista.medida,  Detven.cantidad, Detven.precio, Detven.descuento,  Detven.total*Codven.mult_sto*-1 AS total, Facturas.sucursal,  Clientes.sucursal AS succliente FROM facturas, clientes, codven,   detven INNER JOIN lista    ON  Detven.codigo = Lista.codigo WHERE Detven.compro = Facturas.compro   AND Detven.letra = Facturas.letra   AND Detven.numero = Facturas.numero   AND Facturas.cliente = Clientes.codigo   AND Detven.compro = Codven.compro   AND (Detven.compro$"RF*RD*RT*RM*DM*MR*MD*MS*MM" = .T.   AND Facturas.estado = " "   AND Clientes.vendedor BETWEEN ?nDesVen AND ?nHasVen   AND Facturas.cliente BETWEEN ?nDesCli AND ?nHasCli   AND Codven.mult_ven = 0) ORDER BY Clientes.nombre, Facturas.fecha, Detven.numero

DBSetProp('VLREMITOSPENDIENTES', 'View', 'UpdateType', 1)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'WhereType', 3)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'FetchMemo', .T.)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'SendUpdates', .F.)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'UseMemoSize', 255)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'MaxRecords', -1)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'Tables', 'detven,facturas,clientes,lista')
DBSetProp('VLREMITOSPENDIENTES', 'View', 'Prepared', .F.)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'CompareMemo', .T.)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'Comment', "")
DBSetProp('VLREMITOSPENDIENTES', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLREMITOSPENDIENTES', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLREMITOSPENDIENTES
* Props for the VLREMITOSPENDIENTES.compro field.
DBSetProp('VLREMITOSPENDIENTES.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLREMITOSPENDIENTES.compro', 'Field', 'DataType', "C(2)")
* Props for the VLREMITOSPENDIENTES.letra field.
DBSetProp('VLREMITOSPENDIENTES.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLREMITOSPENDIENTES.letra', 'Field', 'DataType', "C(1)")
* Props for the VLREMITOSPENDIENTES.numero field.
DBSetProp('VLREMITOSPENDIENTES.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLREMITOSPENDIENTES.numero', 'Field', 'DataType', "N(12)")
* Props for the VLREMITOSPENDIENTES.fecha field.
DBSetProp('VLREMITOSPENDIENTES.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLREMITOSPENDIENTES.fecha', 'Field', 'DataType', "D")
* Props for the VLREMITOSPENDIENTES.cliente field.
DBSetProp('VLREMITOSPENDIENTES.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLREMITOSPENDIENTES.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLREMITOSPENDIENTES.nombre field.
DBSetProp('VLREMITOSPENDIENTES.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLREMITOSPENDIENTES.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLREMITOSPENDIENTES.codigo field.
DBSetProp('VLREMITOSPENDIENTES.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.codigo', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.codigo', 'Field', 'UpdateName', 'detven.codigo')
DBSetProp('VLREMITOSPENDIENTES.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLREMITOSPENDIENTES.descripcion field.
DBSetProp('VLREMITOSPENDIENTES.descripcion', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.descripcion', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSPENDIENTES.descripcion', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLREMITOSPENDIENTES.descripcion', 'Field', 'DataType', "C(50)")
* Props for the VLREMITOSPENDIENTES.codfabrica field.
DBSetProp('VLREMITOSPENDIENTES.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.codfabrica', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLREMITOSPENDIENTES.codfabrica', 'Field', 'DataType', "C(15)")
* Props for the VLREMITOSPENDIENTES.medida field.
DBSetProp('VLREMITOSPENDIENTES.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.medida', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLREMITOSPENDIENTES.medida', 'Field', 'DataType', "C(13)")
* Props for the VLREMITOSPENDIENTES.cantidad field.
DBSetProp('VLREMITOSPENDIENTES.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.cantidad', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLREMITOSPENDIENTES.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLREMITOSPENDIENTES.precio field.
DBSetProp('VLREMITOSPENDIENTES.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.precio', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLREMITOSPENDIENTES.precio', 'Field', 'DataType', "N(12,2)")
* Props for the VLREMITOSPENDIENTES.descuento field.
DBSetProp('VLREMITOSPENDIENTES.descuento', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.descuento', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.descuento', 'Field', 'UpdateName', 'detven.descuento')
DBSetProp('VLREMITOSPENDIENTES.descuento', 'Field', 'DataType', "N(6,2)")
* Props for the VLREMITOSPENDIENTES.total field.
DBSetProp('VLREMITOSPENDIENTES.total', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.total', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSPENDIENTES.total', 'Field', 'UpdateName', 'total')
DBSetProp('VLREMITOSPENDIENTES.total', 'Field', 'DataType', "N(18,2)")
* Props for the VLREMITOSPENDIENTES.sucursal field.
DBSetProp('VLREMITOSPENDIENTES.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSPENDIENTES.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLREMITOSPENDIENTES.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLREMITOSPENDIENTES.succliente field.
DBSetProp('VLREMITOSPENDIENTES.succliente', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSPENDIENTES.succliente', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSPENDIENTES.succliente', 'Field', 'UpdateName', 'clientes.sucursal')
DBSetProp('VLREMITOSPENDIENTES.succliente', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLCOMISIONVENDEDORCOBRO
***************** Ver la configuración para VLCOMISIONVENDEDORCOBRO ***************

CREATE SQL VIEW "VLCOMISIONVENDEDORCOBRO" ; 
   AS SELECT Facturas.compro, Facturas.letra, Facturas.numero, Facturas.fecha,   Facturas.condicion, Facturas.cliente, Clientes.nombre, Facturas.gravado,   Facturas.total, Facturas.comision, Facturas.total*0 AS impcomision  FROM clientes,    facturas INNER JOIN codven     ON  Facturas.compro = Codven.compro  WHERE Facturas.cliente = Clientes.codigo    AND (Facturas.compro = "RC"  OR Facturas.compro = "RB" OR Facturas.compro = "RE")    AND Clientes.vendedor = ?nVendedor AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta

DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'UpdateType', 1)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'WhereType', 3)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'FetchMemo', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'SendUpdates', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'UseMemoSize', 255)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'MaxRecords', -1)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'Tables', 'facturas,clientes')
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'Prepared', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'CompareMemo', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'FetchSize', 100)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'Comment', "")
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLCOMISIONVENDEDORCOBRO', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLCOMISIONVENDEDORCOBRO
* Props for the VLCOMISIONVENDEDORCOBRO.compro field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLCOMISIONVENDEDORCOBRO.compro', 'Field', 'DataType', "C(2)")
* Props for the VLCOMISIONVENDEDORCOBRO.letra field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLCOMISIONVENDEDORCOBRO.letra', 'Field', 'DataType', "C(1)")
* Props for the VLCOMISIONVENDEDORCOBRO.numero field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLCOMISIONVENDEDORCOBRO.numero', 'Field', 'DataType', "N(12)")
* Props for the VLCOMISIONVENDEDORCOBRO.fecha field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLCOMISIONVENDEDORCOBRO.fecha', 'Field', 'DataType', "D")
* Props for the VLCOMISIONVENDEDORCOBRO.condicion field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.condicion', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.condicion', 'Field', 'UpdateName', 'facturas.condicion')
DBSetProp('VLCOMISIONVENDEDORCOBRO.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLCOMISIONVENDEDORCOBRO.cliente field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLCOMISIONVENDEDORCOBRO.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLCOMISIONVENDEDORCOBRO.nombre field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLCOMISIONVENDEDORCOBRO.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLCOMISIONVENDEDORCOBRO.gravado field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.gravado', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.gravado', 'Field', 'UpdateName', 'facturas.gravado')
DBSetProp('VLCOMISIONVENDEDORCOBRO.gravado', 'Field', 'DataType', "N(12,2)")
* Props for the VLCOMISIONVENDEDORCOBRO.total field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.total', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.total', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.total', 'Field', 'UpdateName', 'facturas.total')
DBSetProp('VLCOMISIONVENDEDORCOBRO.total', 'Field', 'DataType', "N(12,2)")
* Props for the VLCOMISIONVENDEDORCOBRO.comision field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.comision', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.comision', 'Field', 'Updatable', .T.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.comision', 'Field', 'UpdateName', 'facturas.comision')
DBSetProp('VLCOMISIONVENDEDORCOBRO.comision', 'Field', 'DataType', "C(1)")
* Props for the VLCOMISIONVENDEDORCOBRO.impcomision field.
DBSetProp('VLCOMISIONVENDEDORCOBRO.impcomision', 'Field', 'KeyField', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.impcomision', 'Field', 'Updatable', .F.)
DBSetProp('VLCOMISIONVENDEDORCOBRO.impcomision', 'Field', 'UpdateName', 'impcomision')
DBSetProp('VLCOMISIONVENDEDORCOBRO.impcomision', 'Field', 'DataType', "N(14,2)")
ENDFUNC
 
FUNCTION MakeView_VLREMITOSVENDEDOR
***************** Ver la configuración para VLREMITOSVENDEDOR ***************

CREATE SQL VIEW "VLREMITOSVENDEDOR" ; 
   AS SELECT Detven.compro, Detven.letra, Detven.numero, Facturas.fecha,  Facturas.cliente, Clientes.nombre, Lista.nombre AS descripcion,  Lista.codfabrica, Lista.medida, Detven.cantidad, Detven.precio,  Detven.descuento, Detven.total*Codven.mult_sto*-1 AS total,  Facturas.sucursal, Clientes.sucursal AS succliente FROM facturas, clientes, codven,   detven INNER JOIN lista    ON  Detven.codigo = Lista.codigo WHERE Detven.id = Facturas.id   AND Facturas.cliente = Clientes.codigo   AND Detven.compro = Codven.compro   AND (Codven.mult_ven = 0   AND Clientes.vendedor = ?nVendedor   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta) ORDER BY Clientes.nombre, Facturas.fecha, Detven.numero

DBSetProp('VLREMITOSVENDEDOR', 'View', 'UpdateType', 1)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'WhereType', 3)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'FetchMemo', .T.)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'SendUpdates', .F.)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'UseMemoSize', 255)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'FetchSize', 100)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'MaxRecords', -1)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'Tables', 'detven,facturas,clientes,lista')
DBSetProp('VLREMITOSVENDEDOR', 'View', 'Prepared', .F.)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'CompareMemo', .T.)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'FetchSize', 100)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'Comment', "")
DBSetProp('VLREMITOSVENDEDOR', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLREMITOSVENDEDOR', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLREMITOSVENDEDOR
* Props for the VLREMITOSVENDEDOR.compro field.
DBSetProp('VLREMITOSVENDEDOR.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.compro', 'Field', 'UpdateName', 'detven.compro')
DBSetProp('VLREMITOSVENDEDOR.compro', 'Field', 'DataType', "C(2)")
* Props for the VLREMITOSVENDEDOR.letra field.
DBSetProp('VLREMITOSVENDEDOR.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.letra', 'Field', 'UpdateName', 'detven.letra')
DBSetProp('VLREMITOSVENDEDOR.letra', 'Field', 'DataType', "C(1)")
* Props for the VLREMITOSVENDEDOR.numero field.
DBSetProp('VLREMITOSVENDEDOR.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.numero', 'Field', 'UpdateName', 'detven.numero')
DBSetProp('VLREMITOSVENDEDOR.numero', 'Field', 'DataType', "N(12)")
* Props for the VLREMITOSVENDEDOR.fecha field.
DBSetProp('VLREMITOSVENDEDOR.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLREMITOSVENDEDOR.fecha', 'Field', 'DataType', "D")
* Props for the VLREMITOSVENDEDOR.cliente field.
DBSetProp('VLREMITOSVENDEDOR.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLREMITOSVENDEDOR.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLREMITOSVENDEDOR.nombre field.
DBSetProp('VLREMITOSVENDEDOR.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLREMITOSVENDEDOR.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLREMITOSVENDEDOR.descripcion field.
DBSetProp('VLREMITOSVENDEDOR.descripcion', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.descripcion', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSVENDEDOR.descripcion', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLREMITOSVENDEDOR.descripcion', 'Field', 'DataType', "C(50)")
* Props for the VLREMITOSVENDEDOR.codfabrica field.
DBSetProp('VLREMITOSVENDEDOR.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.codfabrica', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLREMITOSVENDEDOR.codfabrica', 'Field', 'DataType', "C(15)")
* Props for the VLREMITOSVENDEDOR.medida field.
DBSetProp('VLREMITOSVENDEDOR.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.medida', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLREMITOSVENDEDOR.medida', 'Field', 'DataType', "C(13)")
* Props for the VLREMITOSVENDEDOR.cantidad field.
DBSetProp('VLREMITOSVENDEDOR.cantidad', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.cantidad', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.cantidad', 'Field', 'UpdateName', 'detven.cantidad')
DBSetProp('VLREMITOSVENDEDOR.cantidad', 'Field', 'DataType', "N(7,2)")
* Props for the VLREMITOSVENDEDOR.precio field.
DBSetProp('VLREMITOSVENDEDOR.precio', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.precio', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.precio', 'Field', 'UpdateName', 'detven.precio')
DBSetProp('VLREMITOSVENDEDOR.precio', 'Field', 'DataType', "N(12,2)")
* Props for the VLREMITOSVENDEDOR.descuento field.
DBSetProp('VLREMITOSVENDEDOR.descuento', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.descuento', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.descuento', 'Field', 'UpdateName', 'detven.descuento')
DBSetProp('VLREMITOSVENDEDOR.descuento', 'Field', 'DataType', "N(6,2)")
* Props for the VLREMITOSVENDEDOR.total field.
DBSetProp('VLREMITOSVENDEDOR.total', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.total', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSVENDEDOR.total', 'Field', 'UpdateName', 'total')
DBSetProp('VLREMITOSVENDEDOR.total', 'Field', 'DataType', "N(18,2)")
* Props for the VLREMITOSVENDEDOR.sucursal field.
DBSetProp('VLREMITOSVENDEDOR.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLREMITOSVENDEDOR.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLREMITOSVENDEDOR.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLREMITOSVENDEDOR.succliente field.
DBSetProp('VLREMITOSVENDEDOR.succliente', 'Field', 'KeyField', .F.)
DBSetProp('VLREMITOSVENDEDOR.succliente', 'Field', 'Updatable', .F.)
DBSetProp('VLREMITOSVENDEDOR.succliente', 'Field', 'UpdateName', 'clientes.sucursal')
DBSetProp('VLREMITOSVENDEDOR.succliente', 'Field', 'DataType', "N(2)")
ENDFUNC
 
FUNCTION MakeView_VLSALDOSCLIENTES
***************** Ver la configuración para VLSALDOSCLIENTES ***************

CREATE SQL VIEW "VLSALDOSCLIENTES" ; 
   AS SELECT Facturas.cliente, Clientes.nombre, Clientes.domicilio,  Clientes.codpostal, Clientes.telefono, Clientes.fax, Clientes.movil,  Clientes.vendedor, SUM(Facturas.total*Codven.mult_cli) AS saldo,  Facturas.sucursal, {} AS primerfactimpaga,  MAX(Facturas.fechapago) AS ultimopago, Clientes.subcuenta FROM facturas, codven, clientes WHERE Facturas.cliente = Clientes.codigo   AND Facturas.compro = Codven.compro   AND (Facturas.fecha <= ?dFecha   AND Facturas.condicion = 2   AND Codven.mult_cli <> 0) GROUP BY Facturas.cliente ORDER BY Clientes.nombre

DBSetProp('VLSALDOSCLIENTES', 'View', 'UpdateType', 1)
DBSetProp('VLSALDOSCLIENTES', 'View', 'WhereType', 3)
DBSetProp('VLSALDOSCLIENTES', 'View', 'FetchMemo', .T.)
DBSetProp('VLSALDOSCLIENTES', 'View', 'SendUpdates', .F.)
DBSetProp('VLSALDOSCLIENTES', 'View', 'UseMemoSize', 255)
DBSetProp('VLSALDOSCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLSALDOSCLIENTES', 'View', 'MaxRecords', -1)
DBSetProp('VLSALDOSCLIENTES', 'View', 'Tables', 'facturas,clientes')
DBSetProp('VLSALDOSCLIENTES', 'View', 'Prepared', .F.)
DBSetProp('VLSALDOSCLIENTES', 'View', 'CompareMemo', .T.)
DBSetProp('VLSALDOSCLIENTES', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSALDOSCLIENTES', 'View', 'FetchSize', 100)
DBSetProp('VLSALDOSCLIENTES', 'View', 'Comment', "")
DBSetProp('VLSALDOSCLIENTES', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSALDOSCLIENTES', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSALDOSCLIENTES
* Props for the VLSALDOSCLIENTES.cliente field.
DBSetProp('VLSALDOSCLIENTES.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLSALDOSCLIENTES.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLSALDOSCLIENTES.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLSALDOSCLIENTES.nombre field.
DBSetProp('VLSALDOSCLIENTES.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLSALDOSCLIENTES.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLSALDOSCLIENTES.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLSALDOSCLIENTES.domicilio field.
DBSetProp('VLSALDOSCLIENTES.domicilio', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.domicilio', 'Field', 'Updatable', .T.)
DBSetProp('VLSALDOSCLIENTES.domicilio', 'Field', 'UpdateName', 'clientes.domicilio')
DBSetProp('VLSALDOSCLIENTES.domicilio', 'Field', 'DataType', "C(30)")
* Props for the VLSALDOSCLIENTES.codpostal field.
DBSetProp('VLSALDOSCLIENTES.codpostal', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.codpostal', 'Field', 'Updatable', .T.)
DBSetProp('VLSALDOSCLIENTES.codpostal', 'Field', 'UpdateName', 'clientes.codpostal')
DBSetProp('VLSALDOSCLIENTES.codpostal', 'Field', 'DataType', "C(5)")
* Props for the VLSALDOSCLIENTES.telefono field.
DBSetProp('VLSALDOSCLIENTES.telefono', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.telefono', 'Field', 'Updatable', .T.)
DBSetProp('VLSALDOSCLIENTES.telefono', 'Field', 'UpdateName', 'clientes.telefono')
DBSetProp('VLSALDOSCLIENTES.telefono', 'Field', 'DataType', "C(15)")
* Props for the VLSALDOSCLIENTES.fax field.
DBSetProp('VLSALDOSCLIENTES.fax', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.fax', 'Field', 'Updatable', .T.)
DBSetProp('VLSALDOSCLIENTES.fax', 'Field', 'UpdateName', 'clientes.fax')
DBSetProp('VLSALDOSCLIENTES.fax', 'Field', 'DataType', "C(15)")
* Props for the VLSALDOSCLIENTES.movil field.
DBSetProp('VLSALDOSCLIENTES.movil', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.movil', 'Field', 'Updatable', .T.)
DBSetProp('VLSALDOSCLIENTES.movil', 'Field', 'UpdateName', 'clientes.movil')
DBSetProp('VLSALDOSCLIENTES.movil', 'Field', 'DataType', "C(15)")
* Props for the VLSALDOSCLIENTES.vendedor field.
DBSetProp('VLSALDOSCLIENTES.vendedor', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.vendedor', 'Field', 'Updatable', .T.)
DBSetProp('VLSALDOSCLIENTES.vendedor', 'Field', 'UpdateName', 'clientes.vendedor')
DBSetProp('VLSALDOSCLIENTES.vendedor', 'Field', 'DataType', "N(3)")
* Props for the VLSALDOSCLIENTES.saldo field.
DBSetProp('VLSALDOSCLIENTES.saldo', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.saldo', 'Field', 'Updatable', .F.)
DBSetProp('VLSALDOSCLIENTES.saldo', 'Field', 'UpdateName', 'clientes.saldo')
DBSetProp('VLSALDOSCLIENTES.saldo', 'Field', 'DataType', "N(16,2)")
* Props for the VLSALDOSCLIENTES.sucursal field.
DBSetProp('VLSALDOSCLIENTES.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLSALDOSCLIENTES.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLSALDOSCLIENTES.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLSALDOSCLIENTES.primerfactimpaga field.
DBSetProp('VLSALDOSCLIENTES.primerfactimpaga', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.primerfactimpaga', 'Field', 'Updatable', .F.)
DBSetProp('VLSALDOSCLIENTES.primerfactimpaga', 'Field', 'UpdateName', 'Facturas.sucursal*')
DBSetProp('VLSALDOSCLIENTES.primerfactimpaga', 'Field', 'DataType', "D")
* Props for the VLSALDOSCLIENTES.ultimopago field.
DBSetProp('VLSALDOSCLIENTES.ultimopago', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.ultimopago', 'Field', 'Updatable', .F.)
DBSetProp('VLSALDOSCLIENTES.ultimopago', 'Field', 'UpdateName', 'ultimopago')
DBSetProp('VLSALDOSCLIENTES.ultimopago', 'Field', 'DataType', "D")
* Props for the VLSALDOSCLIENTES.subcuenta field.
DBSetProp('VLSALDOSCLIENTES.subcuenta', 'Field', 'KeyField', .F.)
DBSetProp('VLSALDOSCLIENTES.subcuenta', 'Field', 'Updatable', .T.)
DBSetProp('VLSALDOSCLIENTES.subcuenta', 'Field', 'UpdateName', 'clientes.subcuenta')
DBSetProp('VLSALDOSCLIENTES.subcuenta', 'Field', 'DataType', "N(6)")
ENDFUNC
 
FUNCTION MakeView_VLVENTACOMPROLOCALIDAD
***************** Ver la configuración para VLVENTACOMPROLOCALIDAD ***************

CREATE SQL VIEW "VLVENTACOMPROLOCALIDAD" ; 
   AS SELECT Facturas.sucursal, Facturas.fecha, Facturas.compro,  Facturas.letra, Facturas.numero, Facturas.condicion, Facturas.cliente,  Clientes.nombre, Clientes.cuit, Facturas.gravado, Facturas.exento,  Facturas.iva, Facturas.percepib, Facturas.total, Facturas.operador,  Facturas.usuario FROM facturas, codven, clientes WHERE Facturas.compro = Codven.compro   AND Facturas.cliente = Clientes.codigo   AND (Codven.mult_ven <> 0   AND Facturas.fecha BETWEEN ?dDesde AND ?dHasta   AND Clientes.codpostal = ?cCodPostal) ORDER BY Facturas.fecha

DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'UpdateType', 1)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'WhereType', 3)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'FetchMemo', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'SendUpdates', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'UseMemoSize', 255)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'FetchSize', 100)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'MaxRecords', -1)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'Tables', 'facturas,clientes')
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'Prepared', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'CompareMemo', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'FetchSize', 100)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'Comment', "")
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLVENTACOMPROLOCALIDAD', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLVENTACOMPROLOCALIDAD
* Props for the VLVENTACOMPROLOCALIDAD.sucursal field.
DBSetProp('VLVENTACOMPROLOCALIDAD.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLVENTACOMPROLOCALIDAD.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLVENTACOMPROLOCALIDAD.fecha field.
DBSetProp('VLVENTACOMPROLOCALIDAD.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLVENTACOMPROLOCALIDAD.fecha', 'Field', 'DataType', "D")
* Props for the VLVENTACOMPROLOCALIDAD.compro field.
DBSetProp('VLVENTACOMPROLOCALIDAD.compro', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.compro', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.compro', 'Field', 'UpdateName', 'facturas.compro')
DBSetProp('VLVENTACOMPROLOCALIDAD.compro', 'Field', 'DataType', "C(2)")
* Props for the VLVENTACOMPROLOCALIDAD.letra field.
DBSetProp('VLVENTACOMPROLOCALIDAD.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLVENTACOMPROLOCALIDAD.letra', 'Field', 'DataType', "C(1)")
* Props for the VLVENTACOMPROLOCALIDAD.numero field.
DBSetProp('VLVENTACOMPROLOCALIDAD.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLVENTACOMPROLOCALIDAD.numero', 'Field', 'DataType', "N(12)")
* Props for the VLVENTACOMPROLOCALIDAD.condicion field.
DBSetProp('VLVENTACOMPROLOCALIDAD.condicion', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.condicion', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.condicion', 'Field', 'UpdateName', 'facturas.condicion')
DBSetProp('VLVENTACOMPROLOCALIDAD.condicion', 'Field', 'DataType', "N(1)")
* Props for the VLVENTACOMPROLOCALIDAD.cliente field.
DBSetProp('VLVENTACOMPROLOCALIDAD.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLVENTACOMPROLOCALIDAD.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLVENTACOMPROLOCALIDAD.nombre field.
DBSetProp('VLVENTACOMPROLOCALIDAD.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLVENTACOMPROLOCALIDAD.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLVENTACOMPROLOCALIDAD.cuit field.
DBSetProp('VLVENTACOMPROLOCALIDAD.cuit', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.cuit', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.cuit', 'Field', 'UpdateName', 'clientes.cuit')
DBSetProp('VLVENTACOMPROLOCALIDAD.cuit', 'Field', 'DataType', "N(11)")
* Props for the VLVENTACOMPROLOCALIDAD.gravado field.
DBSetProp('VLVENTACOMPROLOCALIDAD.gravado', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.gravado', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.gravado', 'Field', 'UpdateName', 'facturas.gravado')
DBSetProp('VLVENTACOMPROLOCALIDAD.gravado', 'Field', 'DataType', "N(12,2)")
* Props for the VLVENTACOMPROLOCALIDAD.exento field.
DBSetProp('VLVENTACOMPROLOCALIDAD.exento', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.exento', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.exento', 'Field', 'UpdateName', 'facturas.exento')
DBSetProp('VLVENTACOMPROLOCALIDAD.exento', 'Field', 'DataType', "N(12,2)")
* Props for the VLVENTACOMPROLOCALIDAD.iva field.
DBSetProp('VLVENTACOMPROLOCALIDAD.iva', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.iva', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.iva', 'Field', 'UpdateName', 'facturas.iva')
DBSetProp('VLVENTACOMPROLOCALIDAD.iva', 'Field', 'DataType', "N(12,2)")
* Props for the VLVENTACOMPROLOCALIDAD.percepib field.
DBSetProp('VLVENTACOMPROLOCALIDAD.percepib', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.percepib', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.percepib', 'Field', 'UpdateName', 'facturas.percepib')
DBSetProp('VLVENTACOMPROLOCALIDAD.percepib', 'Field', 'DataType', "N(12,2)")
* Props for the VLVENTACOMPROLOCALIDAD.total field.
DBSetProp('VLVENTACOMPROLOCALIDAD.total', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.total', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.total', 'Field', 'UpdateName', 'facturas.total')
DBSetProp('VLVENTACOMPROLOCALIDAD.total', 'Field', 'DataType', "N(12,2)")
* Props for the VLVENTACOMPROLOCALIDAD.operador field.
DBSetProp('VLVENTACOMPROLOCALIDAD.operador', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.operador', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.operador', 'Field', 'UpdateName', 'facturas.operador')
DBSetProp('VLVENTACOMPROLOCALIDAD.operador', 'Field', 'DataType', "C(2)")
* Props for the VLVENTACOMPROLOCALIDAD.usuario field.
DBSetProp('VLVENTACOMPROLOCALIDAD.usuario', 'Field', 'KeyField', .F.)
DBSetProp('VLVENTACOMPROLOCALIDAD.usuario', 'Field', 'Updatable', .T.)
DBSetProp('VLVENTACOMPROLOCALIDAD.usuario', 'Field', 'UpdateName', 'facturas.usuario')
DBSetProp('VLVENTACOMPROLOCALIDAD.usuario', 'Field', 'DataType', "C(15)")
ENDFUNC
 
FUNCTION MakeView_VLWHATSAPPRECIBOS
***************** Ver la configuración para VLWHATSAPPRECIBOS ***************

CREATE SQL VIEW "VLWHATSAPPRECIBOS" ; 
   AS SELECT Codven.nombre AS comprobante, Facturas.letra, Facturas.numero,  Facturas.fecha, Facturas.cliente, Clientes.nombre, Clientes.telefono,  Clientes.movil, Clientes.mail,  Facturas.total*Codven.mult_cli AS importe, .F. AS marca,  Clientes.mail2, Facturas.sucursal, Facturas.usuario, Facturas.operador,  Clientes.saldo FROM facturas, clientes, codven WHERE Facturas.cliente = Clientes.codigo   AND Facturas.compro = Codven.compro   AND (Codven.mult_cli < 0   AND Codven.electronic = .F.   AND Facturas.fecha >= ?dDesde   AND Facturas.sucursal = ?nSuc   AND Facturas.operador = ?cOP)

DBSetProp('VLWHATSAPPRECIBOS', 'View', 'UpdateType', 1)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'WhereType', 3)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'FetchMemo', .T.)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'SendUpdates', .F.)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'UseMemoSize', 255)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'FetchSize', 100)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'MaxRecords', -1)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'Tables', 'codven,facturas,clientes')
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'Prepared', .F.)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'CompareMemo', .T.)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'FetchSize', 100)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'Comment', "")
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLWHATSAPPRECIBOS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLWHATSAPPRECIBOS
* Props for the VLWHATSAPPRECIBOS.comprobante field.
DBSetProp('VLWHATSAPPRECIBOS.comprobante', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.comprobante', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.comprobante', 'Field', 'UpdateName', 'codven.nombre')
DBSetProp('VLWHATSAPPRECIBOS.comprobante', 'Field', 'DataType', "C(30)")
* Props for the VLWHATSAPPRECIBOS.letra field.
DBSetProp('VLWHATSAPPRECIBOS.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLWHATSAPPRECIBOS.letra', 'Field', 'DataType', "C(1)")
* Props for the VLWHATSAPPRECIBOS.numero field.
DBSetProp('VLWHATSAPPRECIBOS.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLWHATSAPPRECIBOS.numero', 'Field', 'DataType', "N(12)")
* Props for the VLWHATSAPPRECIBOS.fecha field.
DBSetProp('VLWHATSAPPRECIBOS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLWHATSAPPRECIBOS.fecha', 'Field', 'DataType', "D")
* Props for the VLWHATSAPPRECIBOS.cliente field.
DBSetProp('VLWHATSAPPRECIBOS.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLWHATSAPPRECIBOS.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLWHATSAPPRECIBOS.nombre field.
DBSetProp('VLWHATSAPPRECIBOS.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLWHATSAPPRECIBOS.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLWHATSAPPRECIBOS.telefono field.
DBSetProp('VLWHATSAPPRECIBOS.telefono', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.telefono', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.telefono', 'Field', 'UpdateName', 'clientes.telefono')
DBSetProp('VLWHATSAPPRECIBOS.telefono', 'Field', 'DataType', "C(15)")
* Props for the VLWHATSAPPRECIBOS.movil field.
DBSetProp('VLWHATSAPPRECIBOS.movil', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.movil', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.movil', 'Field', 'UpdateName', 'clientes.movil')
DBSetProp('VLWHATSAPPRECIBOS.movil', 'Field', 'DataType', "C(15)")
* Props for the VLWHATSAPPRECIBOS.mail field.
DBSetProp('VLWHATSAPPRECIBOS.mail', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.mail', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.mail', 'Field', 'UpdateName', 'clientes.mail')
DBSetProp('VLWHATSAPPRECIBOS.mail', 'Field', 'DataType', "C(50)")
* Props for the VLWHATSAPPRECIBOS.importe field.
DBSetProp('VLWHATSAPPRECIBOS.importe', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.importe', 'Field', 'Updatable', .F.)
DBSetProp('VLWHATSAPPRECIBOS.importe', 'Field', 'UpdateName', 'Clientes.movil*')
DBSetProp('VLWHATSAPPRECIBOS.importe', 'Field', 'DataType', "N(15,2)")
* Props for the VLWHATSAPPRECIBOS.marca field.
DBSetProp('VLWHATSAPPRECIBOS.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLWHATSAPPRECIBOS.marca', 'Field', 'UpdateName', 'Clientes.movil**')
DBSetProp('VLWHATSAPPRECIBOS.marca', 'Field', 'DataType', "L")
* Props for the VLWHATSAPPRECIBOS.mail2 field.
DBSetProp('VLWHATSAPPRECIBOS.mail2', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.mail2', 'Field', 'Updatable', .F.)
DBSetProp('VLWHATSAPPRECIBOS.mail2', 'Field', 'UpdateName', 'clientes.mail2')
DBSetProp('VLWHATSAPPRECIBOS.mail2', 'Field', 'DataType', "C(50)")
* Props for the VLWHATSAPPRECIBOS.sucursal field.
DBSetProp('VLWHATSAPPRECIBOS.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLWHATSAPPRECIBOS.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLWHATSAPPRECIBOS.usuario field.
DBSetProp('VLWHATSAPPRECIBOS.usuario', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.usuario', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.usuario', 'Field', 'UpdateName', 'facturas.usuario')
DBSetProp('VLWHATSAPPRECIBOS.usuario', 'Field', 'DataType', "C(15)")
* Props for the VLWHATSAPPRECIBOS.operador field.
DBSetProp('VLWHATSAPPRECIBOS.operador', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.operador', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.operador', 'Field', 'UpdateName', 'facturas.operador')
DBSetProp('VLWHATSAPPRECIBOS.operador', 'Field', 'DataType', "C(2)")
* Props for the VLWHATSAPPRECIBOS.saldo field.
DBSetProp('VLWHATSAPPRECIBOS.saldo', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPRECIBOS.saldo', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPRECIBOS.saldo', 'Field', 'UpdateName', 'clientes.saldo')
DBSetProp('VLWHATSAPPRECIBOS.saldo', 'Field', 'DataType', "N(10,2)")
ENDFUNC
 
FUNCTION MakeView_VLWHATSAPPFACTURAS
***************** Ver la configuración para VLWHATSAPPFACTURAS ***************

CREATE SQL VIEW "VLWHATSAPPFACTURAS" ; 
   AS SELECT Codven.nombre AS comprobante, Facturas.letra, Facturas.numero,  Facturas.fecha, Facturas.cliente, Clientes.nombre, Clientes.telefono,  Clientes.movil, Clientes.mail,  Facturas.total*Codven.mult_cli AS importe, .F. AS marca,  Clientes.mail2, Facturas.operador, Facturas.sucursal, Clientes.saldo FROM facturas, clientes, codven WHERE Facturas.cliente = Clientes.codigo   AND Facturas.compro = Codven.compro   AND (Codven.electronic = .T.   AND Facturas.fecha >= ?dDesde   AND Facturas.sucursal = ?nSuc   AND Facturas.operador = ?cOP)

DBSetProp('VLWHATSAPPFACTURAS', 'View', 'UpdateType', 1)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'WhereType', 3)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'FetchMemo', .T.)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'SendUpdates', .F.)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'UseMemoSize', 255)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'FetchSize', 100)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'MaxRecords', -1)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'Tables', 'codven,facturas,clientes')
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'Prepared', .F.)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'CompareMemo', .T.)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'FetchSize', 100)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'Comment', "")
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLWHATSAPPFACTURAS', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLWHATSAPPFACTURAS
* Props for the VLWHATSAPPFACTURAS.comprobante field.
DBSetProp('VLWHATSAPPFACTURAS.comprobante', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.comprobante', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.comprobante', 'Field', 'UpdateName', 'codven.nombre')
DBSetProp('VLWHATSAPPFACTURAS.comprobante', 'Field', 'DataType', "C(30)")
* Props for the VLWHATSAPPFACTURAS.letra field.
DBSetProp('VLWHATSAPPFACTURAS.letra', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.letra', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.letra', 'Field', 'UpdateName', 'facturas.letra')
DBSetProp('VLWHATSAPPFACTURAS.letra', 'Field', 'DataType', "C(1)")
* Props for the VLWHATSAPPFACTURAS.numero field.
DBSetProp('VLWHATSAPPFACTURAS.numero', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.numero', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.numero', 'Field', 'UpdateName', 'facturas.numero')
DBSetProp('VLWHATSAPPFACTURAS.numero', 'Field', 'DataType', "N(12)")
* Props for the VLWHATSAPPFACTURAS.fecha field.
DBSetProp('VLWHATSAPPFACTURAS.fecha', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.fecha', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.fecha', 'Field', 'UpdateName', 'facturas.fecha')
DBSetProp('VLWHATSAPPFACTURAS.fecha', 'Field', 'DataType', "D")
* Props for the VLWHATSAPPFACTURAS.cliente field.
DBSetProp('VLWHATSAPPFACTURAS.cliente', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.cliente', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.cliente', 'Field', 'UpdateName', 'facturas.cliente')
DBSetProp('VLWHATSAPPFACTURAS.cliente', 'Field', 'DataType', "N(6)")
* Props for the VLWHATSAPPFACTURAS.nombre field.
DBSetProp('VLWHATSAPPFACTURAS.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.nombre', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.nombre', 'Field', 'UpdateName', 'clientes.nombre')
DBSetProp('VLWHATSAPPFACTURAS.nombre', 'Field', 'DataType', "C(30)")
* Props for the VLWHATSAPPFACTURAS.telefono field.
DBSetProp('VLWHATSAPPFACTURAS.telefono', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.telefono', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.telefono', 'Field', 'UpdateName', 'clientes.telefono')
DBSetProp('VLWHATSAPPFACTURAS.telefono', 'Field', 'DataType', "C(15)")
* Props for the VLWHATSAPPFACTURAS.movil field.
DBSetProp('VLWHATSAPPFACTURAS.movil', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.movil', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.movil', 'Field', 'UpdateName', 'clientes.movil')
DBSetProp('VLWHATSAPPFACTURAS.movil', 'Field', 'DataType', "C(15)")
* Props for the VLWHATSAPPFACTURAS.mail field.
DBSetProp('VLWHATSAPPFACTURAS.mail', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.mail', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.mail', 'Field', 'UpdateName', 'clientes.mail')
DBSetProp('VLWHATSAPPFACTURAS.mail', 'Field', 'DataType', "C(50)")
* Props for the VLWHATSAPPFACTURAS.importe field.
DBSetProp('VLWHATSAPPFACTURAS.importe', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.importe', 'Field', 'Updatable', .F.)
DBSetProp('VLWHATSAPPFACTURAS.importe', 'Field', 'UpdateName', 'Clientes.movil*')
DBSetProp('VLWHATSAPPFACTURAS.importe', 'Field', 'DataType', "N(15,2)")
* Props for the VLWHATSAPPFACTURAS.marca field.
DBSetProp('VLWHATSAPPFACTURAS.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLWHATSAPPFACTURAS.marca', 'Field', 'UpdateName', 'Clientes.movil**')
DBSetProp('VLWHATSAPPFACTURAS.marca', 'Field', 'DataType', "L")
* Props for the VLWHATSAPPFACTURAS.mail2 field.
DBSetProp('VLWHATSAPPFACTURAS.mail2', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.mail2', 'Field', 'Updatable', .F.)
DBSetProp('VLWHATSAPPFACTURAS.mail2', 'Field', 'UpdateName', 'clientes.mail2')
DBSetProp('VLWHATSAPPFACTURAS.mail2', 'Field', 'DataType', "C(50)")
* Props for the VLWHATSAPPFACTURAS.operador field.
DBSetProp('VLWHATSAPPFACTURAS.operador', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.operador', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.operador', 'Field', 'UpdateName', 'facturas.operador')
DBSetProp('VLWHATSAPPFACTURAS.operador', 'Field', 'DataType', "C(2)")
* Props for the VLWHATSAPPFACTURAS.sucursal field.
DBSetProp('VLWHATSAPPFACTURAS.sucursal', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.sucursal', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.sucursal', 'Field', 'UpdateName', 'facturas.sucursal')
DBSetProp('VLWHATSAPPFACTURAS.sucursal', 'Field', 'DataType', "N(2)")
* Props for the VLWHATSAPPFACTURAS.saldo field.
DBSetProp('VLWHATSAPPFACTURAS.saldo', 'Field', 'KeyField', .F.)
DBSetProp('VLWHATSAPPFACTURAS.saldo', 'Field', 'Updatable', .T.)
DBSetProp('VLWHATSAPPFACTURAS.saldo', 'Field', 'UpdateName', 'clientes.saldo')
DBSetProp('VLWHATSAPPFACTURAS.saldo', 'Field', 'DataType', "N(10,2)")
ENDFUNC
 
FUNCTION MakeView_VLSTOCKREPOSICION
***************** Ver la configuración para VLSTOCKREPOSICION ***************

CREATE SQL VIEW "VLSTOCKREPOSICION" ; 
   AS SELECT Stock.deposito, Stock.codigo, Lista.codfabrica, Lista.segmento,  Lista.modelo, Lista.articulo, Lista.marca, Lista.medida, Lista.nombre,  SUM(Stock.stock) AS stock, Listamin.minimo FROM stock, lista, listamin WHERE Stock.codigo = Lista.codigo   AND Stock.deposito = Listamin.sucursal   AND Lista.codfabrica = Listamin.cai   AND Stock.stock <= Listamin.minimo   AND (Listamin.minimo <> 0   AND Stock.deposito = ?nDeposito   AND Lista.articulo BETWEEN ?nDesArt AND ?nHasArt   AND Lista.modelo BETWEEN ?nDesMod AND ?nHasMod   AND Lista.marca BETWEEN ?nDesMar AND ?nHasMar) GROUP BY Lista.codfabrica, Stock.deposito ORDER BY Lista.articulo, Lista.modelo

DBSetProp('VLSTOCKREPOSICION', 'View', 'UpdateType', 1)
DBSetProp('VLSTOCKREPOSICION', 'View', 'WhereType', 3)
DBSetProp('VLSTOCKREPOSICION', 'View', 'FetchMemo', .T.)
DBSetProp('VLSTOCKREPOSICION', 'View', 'SendUpdates', .F.)
DBSetProp('VLSTOCKREPOSICION', 'View', 'UseMemoSize', 255)
DBSetProp('VLSTOCKREPOSICION', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKREPOSICION', 'View', 'MaxRecords', -1)
DBSetProp('VLSTOCKREPOSICION', 'View', 'Tables', '')
DBSetProp('VLSTOCKREPOSICION', 'View', 'Prepared', .F.)
DBSetProp('VLSTOCKREPOSICION', 'View', 'CompareMemo', .T.)
DBSetProp('VLSTOCKREPOSICION', 'View', 'FetchAsNeeded', .F.)
DBSetProp('VLSTOCKREPOSICION', 'View', 'FetchSize', 100)
DBSetProp('VLSTOCKREPOSICION', 'View', 'Comment', "")
DBSetProp('VLSTOCKREPOSICION', 'View', 'BatchUpdateCount', 1)
DBSetProp('VLSTOCKREPOSICION', 'View', 'ShareConnection', .F.)

*!* Field Level Properties for VLSTOCKREPOSICION
* Props for the VLSTOCKREPOSICION.deposito field.
DBSetProp('VLSTOCKREPOSICION.deposito', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.deposito', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.deposito', 'Field', 'UpdateName', 'stock.deposito')
DBSetProp('VLSTOCKREPOSICION.deposito', 'Field', 'DataType', "N(2)")
* Props for the VLSTOCKREPOSICION.codigo field.
DBSetProp('VLSTOCKREPOSICION.codigo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.codigo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.codigo', 'Field', 'UpdateName', 'stock.codigo')
DBSetProp('VLSTOCKREPOSICION.codigo', 'Field', 'DataType', "N(6)")
* Props for the VLSTOCKREPOSICION.codfabrica field.
DBSetProp('VLSTOCKREPOSICION.codfabrica', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.codfabrica', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.codfabrica', 'Field', 'UpdateName', 'lista.codfabrica')
DBSetProp('VLSTOCKREPOSICION.codfabrica', 'Field', 'DataType', "C(15)")
* Props for the VLSTOCKREPOSICION.segmento field.
DBSetProp('VLSTOCKREPOSICION.segmento', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.segmento', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.segmento', 'Field', 'UpdateName', 'lista.segmento')
DBSetProp('VLSTOCKREPOSICION.segmento', 'Field', 'DataType', "C(3)")
* Props for the VLSTOCKREPOSICION.modelo field.
DBSetProp('VLSTOCKREPOSICION.modelo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.modelo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.modelo', 'Field', 'UpdateName', 'lista.modelo')
DBSetProp('VLSTOCKREPOSICION.modelo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCKREPOSICION.articulo field.
DBSetProp('VLSTOCKREPOSICION.articulo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.articulo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.articulo', 'Field', 'UpdateName', 'lista.articulo')
DBSetProp('VLSTOCKREPOSICION.articulo', 'Field', 'DataType', "N(4)")
* Props for the VLSTOCKREPOSICION.marca field.
DBSetProp('VLSTOCKREPOSICION.marca', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.marca', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.marca', 'Field', 'UpdateName', 'lista.marca')
DBSetProp('VLSTOCKREPOSICION.marca', 'Field', 'DataType', "N(3)")
* Props for the VLSTOCKREPOSICION.medida field.
DBSetProp('VLSTOCKREPOSICION.medida', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.medida', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.medida', 'Field', 'UpdateName', 'lista.medida')
DBSetProp('VLSTOCKREPOSICION.medida', 'Field', 'DataType', "C(13)")
* Props for the VLSTOCKREPOSICION.nombre field.
DBSetProp('VLSTOCKREPOSICION.nombre', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.nombre', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.nombre', 'Field', 'UpdateName', 'lista.nombre')
DBSetProp('VLSTOCKREPOSICION.nombre', 'Field', 'DataType', "C(50)")
* Props for the VLSTOCKREPOSICION.stock field.
DBSetProp('VLSTOCKREPOSICION.stock', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.stock', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.stock', 'Field', 'UpdateName', 'SUM(Stock.stock)')
DBSetProp('VLSTOCKREPOSICION.stock', 'Field', 'DataType', "N(16,2)")
* Props for the VLSTOCKREPOSICION.minimo field.
DBSetProp('VLSTOCKREPOSICION.minimo', 'Field', 'KeyField', .F.)
DBSetProp('VLSTOCKREPOSICION.minimo', 'Field', 'Updatable', .F.)
DBSetProp('VLSTOCKREPOSICION.minimo', 'Field', 'UpdateName', 'listamin.minimo')
DBSetProp('VLSTOCKREPOSICION.minimo', 'Field', 'DataType', "N(4)")
ENDFUNC
 

FUNCTION DisplayStatus(lcMessage)
WAIT WINDOW NOWAIT lcMessage
ENDFUNC

*.*
*.* Modificaciones de tablas del programa DEBONA
*.*
CREATE TABLE sucursal (id N(2), nombre C(30), domicilio C(30), telefono C(15), localidad C(15), provincia C(15))
SELECT sucursal 
INDEX ON id TAG id

CREATE TABLE terminal (terminal C(15), login C(15), nombre C(30), sucursal N(2), puntovta N(4), muestro L(1), usuario C(15))
SELECT terminal
INDEX ON login TAG login

USE numeros EXCLUSIVE 
ALTER TABLE numeros ;
	ADD COLUMN sucursal N(2)

USE vendedor EXCLUSIVE 
ALTER TABLE vendedor ;
	ALTER COLUMN codigo N(3)

USE vendesc EXCLUSIVE 
ALTER TABLE vendesc ;
	ALTER COLUMN vendedor N(3)

USE vendescart EXCLUSIVE 
ALTER TABLE vendescart ;
	ALTER COLUMN vendedor N(3)

USE clientes EXCLUSIVE 
ALTER TABLE clientes ;
	ADD COLUMN sucursal N(2) ;
	ADD COLUMN autorizado C(15) ;
	ALTER COLUMN vendedor N(3)

USE facturas EXCLUSIVE 
ALTER TABLE facturas ;
	ADD COLUMN sucursal N(2) ;
	ADD COLUMN usuario C(15)

USE pedidos EXCLUSIVE 
ALTER TABLE pedidos ;
	ADD COLUMN sucursal N(2) ;
	ADD COLUMN usuario C(15)

USE stock EXCLUSIVE 
ALTER TABLE stock ;
	ADD COLUMN minimo N(4) ;
	ADD COLUMN sucursal N(2)
SELECT stock
INDEX ON STR(sucursal,2)+STR(codigo,6) TAG sucursal 

USE compras EXCLUSIVE 
ALTER TABLE compras ;
	ADD COLUMN sucursal N(2) ;
	ADD COLUMN usuario C(15)
	
*---------------------------------------------------------- Pases de Informacion
*---------------------------------------------------------- Para Santa Fe
USE numeros EXCLUSIVE 
REPLACE sucursal WITH 2 ALL 
USE clientes
REPLACE sucursal WITH 2 ALL 
USE facturas
REPLACE sucursal WITH 2 ALL 
USE pedidos EXCLUSIVE 
PACK 
REPLACE sucursal WITH 2 ALL 
USE stock  EXCLUSIVE 
ZAP 
APPEND FROM lista
REPLACE sucursal WITH 2 ALL 
USE compras EXCLUSIVE 
REPLACE sucursal WITH 2 ALL 
USE vendescart EXCLUSIVE
INDEX ON  STR(VENDEDOR,3)+STR(MARCA,3)+STR(ARTICULO,4) TAG articulo
CLOSE TABLES ALL 

*---------------------------------------------------------- Para San Justo
SET DEFAULT TO \sanjusto\data

CREATE TABLE sucursal (id N(2), nombre C(30), domicilio C(30), telefono C(15), localidad C(15), provincia C(15))
SELECT sucursal 
INDEX ON id TAG id

CREATE TABLE terminal (terminal C(15), login C(15), nombre C(30), sucursal N(2), puntovta N(4), muestro L(1), usuario C(15))
SELECT terminal
INDEX ON login TAG login

USE numeros EXCLUSIVE 
ALTER TABLE numeros ;
	ADD COLUMN sucursal N(2)

USE vendedor EXCLUSIVE 
ALTER TABLE vendedor ;
	ALTER COLUMN codigo N(3)

USE vendesc EXCLUSIVE 
ALTER TABLE vendesc ;
	ALTER COLUMN vendedor N(3)

USE vendescart EXCLUSIVE 
ALTER TABLE vendescart ;
	ALTER COLUMN vendedor N(3)

USE clientes EXCLUSIVE 
ALTER TABLE clientes ;
	ADD COLUMN sucursal N(2) ;
	ADD COLUMN autorizado C(15) ;
	ALTER COLUMN vendedor N(3)

USE facturas EXCLUSIVE 
ALTER TABLE facturas ;
	ADD COLUMN sucursal N(2) ;
	ADD COLUMN usuario C(15)

USE pedidos EXCLUSIVE 
ALTER TABLE pedidos ;
	ADD COLUMN sucursal N(2) ;
	ADD COLUMN usuario C(15)

USE stock EXCLUSIVE 
ALTER TABLE stock ;
	ADD COLUMN minimo N(4) ;
	ADD COLUMN sucursal N(2)
SELECT stock
INDEX ON STR(sucursal,2)+STR(codigo,6) TAG sucursal 

USE compras EXCLUSIVE 
ALTER TABLE compras ;
	ADD COLUMN sucursal N(2) ;
	ADD COLUMN usuario C(15)
CLOSE ALL
	

USE numeros EXCLUSIVE 
REPLACE sucursal WITH 1 ALL 
USE vendedor EXCLUSIVE 
REPLACE codigo WITH codigo + 100 ALL 
USE vendesc EXCLUSIVE 
REPLACE vendedor WITH vendedor + 100 ALL 
USE vendescart EXCLUSIVE 
REPLACE vendedor WITH vendedor + 100 ALL 
USE clientes EXCLUSIVE 
REPLACE sucursal WITH 1 ALL 
REPLACE vendedor WITH vendedor + 100 ALL 
REPLACE codigo   WITH codigo + 50000 ALL 
USE facturas
REPLACE sucursal WITH 1 ALL 
REPLACE cliente  WITH cliente + 50000 ALL 
USE pedidos EXCLUSIVE 
REPLACE sucursal WITH 1 ALL 
REPLACE cliente  WITH cliente + 50000 ALL 
USE stock  EXCLUSIVE 
ZAP 
APPEND FROM lista
REPLACE sucursal WITH 1 ALL 
USE compras EXCLUSIVE 
REPLACE sucursal WITH 1 ALL 
CLOSE TABLES ALL 

*---------------------------------------------------------------- Agrego Datos
SET DEFAULT TO \maas\sistema\data
USE numeros  EXCLUSIVE 
APPEND FROM \sanjusto\data\numeros
PACK 

USE vendedor EXCLUSIVE 
APPEND FROM \sanjusto\data\vendedor
PACK

USE clientes EXCLUSIVE 
APPEND FROM \sanjusto\data\clientes
PACK

USE facturas EXCLUSIVE 
APPEND FROM \sanjusto\data\facturas
PACK

USE detven EXCLUSIVE 
APPEND FROM \sanjusto\data\detven
PACK

USE contado EXCLUSIVE 
APPEND FROM \sanjusto\data\contado
PACK

USE empleado EXCLUSIVE 
APPEND FROM \sanjusto\data\empleado
PACK

USE stock EXCLUSIVE 
APPEND FROM \sanjusto\data\stock
PACK

USE movstock  EXCLUSIVE 
APPEND FROM \sanjusto\data\movstock
PACK

USE pedidos EXCLUSIVE 
APPEND FROM \sanjusto\data\pedidos
PACK

USE recibos EXCLUSIVE 
APPEND FROM \sanjusto\data\recibos
PACK

USE vendesc EXCLUSIVE 
APPEND FROM \sanjusto\data\vendesc
PACK

USE vendescart
APPEND FROM \sanjusto\data\vendescart
PACK

USE compras EXCLUSIVE 
APPEND FROM \sanjusto\data\compras
PACK

USE detcom EXCLUSIVE 
APPEND FROM \sanjusto\data\detcom
PACK

USE usuarios EXCLUSIVE 
APPEND FROM \sanjusto\data\usuarios
PACK


*-------------------------------------------- 12/10/2.008
USE terminal EXCLUSIVE 
ALTER TABLE terminal ;
	ADD COLUMN CFmodelo C(15) ;
	ADD COLUMN CFpuerto N(1) ;
	ADD COLUMN CFSeg N(5)
	
CLOSE TABLES ALL 

*-------------------------------------------- 21/10/2.008
USE movstock EXCLUSIVE 
ALTER TABLE movstock ;
	ADD COLUMN sucursal N(1)
	
CLOSE TABLES ALL 


*-------------------------------------------- 6/4/2.009
USE compras EXCLUSIVE 
ALTER TABLE compras ;
	ADD COLUMN monotrib N(10,2) ;
	ADD COLUMN nogravado N(10,2) ;
	ADD COLUMN percepcion N(10,2) ;
	ADD COLUMN imputacion N(2) 
CLOSE TABLES ALL 

USE codimp EXCLUSIVE 
ALTER TABLE codimp ALTER COLUMN codigo n(4)
CLOSE TABLES ALL 

*-------------------------------------------- 6/7/2.009
USE EMPLEADO EXCLUSIVE 
ALTER TABLE EMPLEADO ;
	ADD COLUMN vendedor L(1) ;
	ADD COLUMN codvend N(3)
CLOSE TABLES ALL 

*-------------------------------------------- 10/9/2.009
USE vendedor EXCLUSIVE 
ALTER TABLE vendedor ;
	ADD COLUMN sucursal N(2)

CREATE TABLE VALIDAR (sucursal N(2), solicitado C(20), comentario C(50), fecha D(8), cliente N(5), validacion N(4))
INDEX ON fecha TAG fecha


*-------------------------------------------- 17/3/2010
USE vendedor EXCLUSIVE 
ALTER TABLE vendedor ADD COLUMN diasrtos N(3)


*-------------------------------------------- 27/4/2010
CLOSE TABLES ALL 
USE facturas EXCLUSIVE 
ALTER TABLE facturas ADD COLUMN id N(7)
PACK
REPLACE id WITH RECNO() ALL
INDEX ON id TAG id 
SET ORDER TO numero

USE detven EXCLUSIVE  IN 0 
SELECT detven
ALTER TABLE detven ADD COLUMN id N(7) ADD COLUMN stock N(10,2) ADD COLUMN actstock L(1)
INDEX ON id TAG id 
SET RELATION TO COMPRO+LETRA+STR(NUMERO,12) INTO FACTURAS 
REPLACE id WITH facturas.id ALL 

USE compras EXCLUSIVE
ALTER TABLE compras ADD COLUMN id N(7)
PACK
REPLACE id WITH RECNO() ALL
INDEX ON id TAG id 
SET ORDER TO NUMERO

USE detcom EXCLUSIVE IN 0 
SELECT detcom
ALTER TABLE detcom ADD COLUMN id N(7) ADD COLUMN stock N(10,2)
INDEX ON id TAG id 
SET RELA TO STR(PROVEEDOR,4)+COMPRO+LETRA+STR(NUMERO,12) INTO compras
REPLACE id WITH compras.id ALL 

CLOSE TABLES ALL 
USE movstock EXCLUSIVE
ALTER TABLE movstock ADD COLUMN id N(7)
PACK
REPLACE id WITH RECNO() ALL
INDEX ON id TAG id 
SET ORDER TO numero

USE detven IN 0 
SELECT detven 
SET RELATION TO numero INTO movstock
REPLACE id WITH movstock.id FOR compro="MI"

*
* Crear nueva tabla StockSdo, StockMov
*

*-------------------------------------------- 27/5/2010
CLOSE TABLES ALL 
USE lista EXCLUSIVE 
ALTER TABLE lista ADD COLUMN despacho1 C(15) ADD COLUMN despacho2 C(15) ADD COLUMN despacho3 C(15)

USE pedidos EXCLUSIVE 
ALTER TABLE pedidos ADD COLUMN despacho C(30)


CLOSE TABLES ALL 
USE lista EXCLUSIVE 
ALTER TABLE lista alter COLUMN despacho1 C(16) ALTER COLUMN despacho2 C(16)

USE pedidos EXCLUSIVE 
ALTER TABLE pedidos alter COLUMN despacho C(40)

USE detcom EXCLUSIVE 
ALTER TABLE detcom  ADD COLUMN despacho C(16)
CLOSE TABLES ALL 

*------------------------------------------ 20/7/2010
USE param EXCLUSIVE 
ALTER TABLE param  ADD COLUMN diasvto N(3)
CLOSE TABLES ALL 

*------------------------------------------ 20/10/2010
USE facturas EXCLUSIVE 
ALTER TABLE facturas  ADD COLUMN sucimp N(1)
CLOSE TABLES ALL 

*------------------------------------------ 06/11/2012
USE articulo EXCLUSIVE 
ALTER TABLE articulo ADD COLUMN xTraxtorA L(1) ADD COLUMN xTraxtorC L(1)
USE marcas EXCLUSIVE 
ALTER TABLE marcas ADD COLUMN xTraxtorA L(1) ADD COLUMN xTraxtorC L(1)
USE codven EXCLUSIVE 
ALTER TABLE codven ADD COLUMN xTraxtorA L(1) ADD COLUMN xTraxtorC L(1)

CLOSE TABLES ALL 

*------------------------------------------ 08/10/2013
USE clientes EXCLUSIVE 
ALTER TABLE clientes ADD COLUMN exportado L(1)
CLOSE TABLES ALL 

*------------------------------------------ 16/12/2013
USE lista EXCLUSIVE 
INDEX ON codfabrica TAG codfabrica
CLOSE TABLES ALL 

*------------------------------------------ 04/06/2015
USE clientes EXCLUSIVE
ALTER TABLE clientes ALTER COLUMN codigo N(6)
USE facturas EXCLUSIVE
ALTER TABLE facturas ALTER COLUMN cliente N(6)
USE guia EXCLUSIVE
ALTER TABLE clientes ALTER COLUMN codigo N(6)
USE pedidos EXCLUSIVE
ALTER TABLE pedidos ALTER COLUMN cliente N(6)

USE vehiculo EXCLUSIVE
ALTER TABLE vehiculo ALTER COLUMN cliente N(6)
CLOSE TABLES ALL 

USE codven EXCLUSIVE 
ALTER TABLE codven ADD COLUMN codCITIA C(3) ADD COLUMN codCITIB C(3)

USE codcom EXCLUSIVE 
ALTER TABLE codcom ADD COLUMN codAfipB N(3) ADD COLUMN codAfipC N(3)
CLOSE TABLES ALL 


*-------------------------------------------- 25-4-16
CLOSE TABLES ALL 
USE detven EXCLUSIVE 
ALTER TABLE detven ADD COLUMN operario N(3)
CLOSE TABLES ALL 

USE clientes EXCLUSIVE 
ALTER TABLE clientes ADD COLUMN PercepIB N(1)
CLOSE TABLES 

USE facturas EXCLUSIVE 
ALTER TABLE facturas ADD COLUMN PercepIB N(12,2)
CLOSE TABLES 

USE pedidos EXCLUSIVE 
ALTER TABLE pedidos ADD COLUMN PercepIB N(12,2) ADD COLUMN idFactura N(6)
CLOSE TABLES 

*-------------------------------------------- 16-5-16
CLOSE TABLES ALL 
USE articulo EXCLUSIVE 
ALTER TABLE articulo ADD COLUMN comisionOp N(6,2)
CLOSE TABLES ALL 

*-------------------------------------------- 12-9-16
CLOSE TABLES ALL 
USE terminal EXCLUSIVE 
ALTER TABLE terminal ADD COLUMN RtoFiscal L(1)
CLOSE TABLES ALL 

USE numeros EXCLUSIVE 
ALTER TABLE numeros ADD COLUMN Remitos N(12)
CLOSE TABLES ALL 

USE codven EXCLUSIVE 
ALTER TABLE codven ADD COLUMN codCITIA C(3) ADD COLUMN codCITIB C(3) ADD COLUMN electronica L(1)
CLOSE TABLES ALL 

USE tipodoc EXCLUSIVE 
ALTER TABLE tipodoc ADD COLUMN AFIPws C(2)
CLOSE TABLES ALL 

USE facturas EXCLUSIVE 
ALTER TABLE facturas ADD COLUMN cae N(14) ADD COLUMN caevto D(8)
CLOSE TABLES ALL 

USE detven EXCLUSIVE 
ALTER TABLE detven ADD COLUMN gravado N(12,2) ADD COLUMN aliciva N(6,2) ADD COLUMN iva N(12,2)
CLOSE TABLES ALL 

*--------------------------------------------------------- 01/11/16
USE terminal EXCLUSIVE 
ALTER TABLE terminal ADD COLUMN puntoVtaCF L(1)
CLOSE TABLES ALL 


*--------------------------------------------------------- 04/04/17
USE clientes EXCLUSIVE 
ALTER TABLE clientes ADD COLUMN vip L(1)
CLOSE TABLES ALL 


*--------------------------------------------------------- 24/04/17
USE param EXCLUSIVE 
ALTER TABLE param ADD COLUMN IBInscr N(6,2) ADD COLUMN IBConv N(6,2) ADD COLUMN IBMonto N(12,2)

USE clientes
REPLACE percepib WITH 1 FOR sitiva#"RI"
REPLACE percepib WITH 2 FOR sitiva="RI"
CLOSE TABLES ALL 


*--------------------------------------------------------- 12/05/17
USE clientes EXCLUSIVE 
ALTER TABLE clientes ADD COLUMN ingBruto C(15)
CLOSE TABLES ALL 

*--------------------------------------------------------- 10/06/17
USE clientes EXCLUSIVE 
ALTER TABLE clientes ADD COLUMN mayorista L(1)
CLOSE TABLES ALL 

USE facturas EXCLUSIVE 
ALTER TABLE facturas ALTER COLUMN id N(7)

USE detven EXCLUSIVE 
ALTER TABLE detven ALTER COLUMN id N(7)
CLOSE TABLES ALL 


*--------------------------------------------------------- 27/07/17
USE clientes EXCLUSIVE 
ALTER TABLE clientes ADD COLUMN subcuenta N(6)
CLOSE TABLES ALL 


*--------------------------------------------------------- 19/09/17
USE param EXCLUSIVE 
ALTER TABLE param ADD COLUMN IBinscrER N(6,2) ADD COLUMN IBconvER N(6,2) ADD COLUMN IBMontoER N(10,2)
CLOSE TABLES ALL 


*--------------------------------------------------------- 02/07/18
USE vendedor EXCLUSIVE 
ALTER TABLE vendedor ADD COLUMN emailFAC L(1) ADD COLUMN emailSDO L(1) ADD COLUMN emailEST L(1)
REPLACE emailFAC WITH .T. ALL 
REPLACE emailSDO WITH .T. ALL 
REPLACE emailEST WITH .T. ALL 
CLOSE TABLES ALL 


*--------------------------------------------------------- 024/07/18
USE validar EXCLUSIVE 
ALTER TABLE validar ADD COLUMN compro C(3)
CLOSE TABLES ALL 


*--------------------------------------------------------- 13/11/18
USE validar EXCLUSIVE 
ALTER TABLE validar ADD COLUMN id N(6) ADD COLUMN hora C(5) ADD COLUMN numero N(12) ADD COLUMN hs C(5)
INDEX ON id TAG id
GO BOTTOM 
REPLACE id WITH 1000
CLOSE TABLES ALL 


*--------------------------------------------------------- 25/05/19
USE medioPagos EXCLUSIVE 
ALTER TABLE medioPagos ADD COLUMN caja N(8)
CLOSE TABLES ALL 


*--------------------------------------------------------- 08/07/19
USE facturas EXCLUSIVE 
ALTER TABLE facturas ADD COLUMN Observa C(50)
CLOSE TABLES ALL 


USE caja EXCLUSIVE 
ALTER TABLE caja ADD COLUMN Observa C(50)
CLOSE TABLES ALL 


*--------------------------------------------------------- 29/07/19
USE proveedor EXCLUSIVE 
ALTER TABLE proveedor ADD COLUMN AlicIB N(6,2)
CLOSE TABLES ALL 

USE compras EXCLUSIVE 
ALTER TABLE compras ADD COLUMN AlicIVA N(6,2)
CLOSE TABLES ALL 

*--------------------------------------------------------- 20/08/19
USE codven EXCLUSIVE 
ALTER TABLE codven ADD COLUMN compasoc C(15)
CLOSE TABLES ALL 

*--------------------------------------------------------- 31/01/2020
USE facturas EXCLUSIVE 
ALTER TABLE facturas ADD COLUMN stockClie L(1)
CLOSE TABLES ALL 

USE numeros EXCLUSIVE 
ALTER TABLE numeros ADD COLUMN deposito N(12)
REPLACE deposito WITH sucursal*100000000 ALL 
CLOSE TABLES ALL 


*--------------------------------------------------------- 14/09/2020
USE caja EXCLUSIVE 
ALTER TABLE caja ADD COLUMN usuario C(15)
CLOSE TABLES ALL 


*---------------------------------------------------------- 01/01/2024
*!*	Cambiamos la forma de trabajar los stock, ahora se puede terner mas de un deposito de mercaderia por sucursal
*!*	Antes solo era un stock por sucursal 
*!*	Para eso se modificio la tabla stock el campo sucursal por deposito y se creo una nueva tabla de depositos
*!*	tambien tuve que agregar el campo deposito en la facturacion para saber de donde sale esa mercaderia
*!*	sobre todo para los movimientos internos

USE stock EXCLUSIVE 
ALTER TABLE stock ADD COLUMN deposito N(2) 
REPLACE deposito WITH sucursal ALL 
INDEX ON STR(deposito,2)+STR(codigo,6) TAG deposito 
DELETE TAG sucursal
CLOSE TABLES ALL

USE facturas EXCLUSIVE 
ALTER TABLE facturas ADD COLUMN deposito N(2)
REPLACE deposito WITH sucursal ALL 
CLOSE TABLES ALL 

USE stockSdo EXCLUSIVE 
ALTER TABLE stockSdo ADD COLUMN deposito N(2)
REPLACE deposito WITH sucursal ALL 
*borrar campo sucursal
MODIFY STRUCTURE 
CLOSE TABLES ALL 

USE pedidos EXCLUSIVE 
ALTER TABLE pedidos ADD COLUMN deposito N(2)
REPLACE deposito WITH sucursal ALL 
CLOSE TABLES ALL 

*---------------------------------------------------------- 06-02-2024
USE listamin EXCLUSIVE 
ALTER TABLE listamin ADD COLUMN deposito N(2) 
REPLACE deposito WITH sucursal ALL 
INDEX ON STR(deposito,2)+cai TAG deposito 
INDEX ON cai+STR(deposito,2) TAG stock
DELETE TAG sucursal
*borrar campo sucursal
MODIFY STRUCTURE 
CLOSE TABLES ALL

USE compras EXCLUSIVE 
ALTER TABLE compras ADD COLUMN deposito N(2)
REPLACE deposito WITH sucursal ALL 
CLOSE TABLES ALL 

*---------------------------------------------------------- 20-02-2024
USE movstock EXCLUSIVE 
ALTER TABLE movstock ADD COLUMN deposito N(2)
REPLACE deposito WITH sucursal ALL 
CLOSE TABLES ALL 

*---------------------------------------------------------- 20-05-2024
USE medidasestados EXCLUSIVE 
ALTER TABLE medidasestados ADD COLUMN cai C(15)
INDEX ON cai TAG cai 
USE lista order codigo IN 0 
SET RELATION TO codigo INTO lista
REPLACE cai WITH lista.codfabrica ALL 

CLOSE TABLES ALL 


*---------------------------------------------------------- 19/08/2024
USE lista EXCLUSIVE 
ALTER TABLE lista ALTER COLUMN codfabrica C(21)

USE listamin EXCLUSIVE 
ALTER TABLE listamin ALTER COLUMN cai C(21)

USE medidasestados EXCLUSIVE 
ALTER TABLE medidasestados ALTER COLUMN cai C(21)

USE pedidos EXCLUSIVE 
ALTER TABLE pedidos ALTER COLUMN cai C(21)
CLOSE TABLES ALL 

*---------------------------------------------------------- 1/11/2024
USE facturas EXCLUSIVE 
ALTER TABLE facturas ADD COLUMN promo L(1)

*---------------------------------------------------------- 25/03/2025
USE facturas EXCLUSIVE 
ALTER TABLE facturas ADD COLUMN conocio N(2)

*---------------------------------------------------------- 21/04/2026
USE lista EXCLUSIVE 
ALTER TABLE lista ADD COLUMN ptoPremio N(5) ADD COLUMN ptoCosto N(5)


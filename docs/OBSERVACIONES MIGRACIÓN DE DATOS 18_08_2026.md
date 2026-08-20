**OBSERVACIONES MIGRACIÓN DE DATOS 18/08/2026**

**[1]**

**No es necesario aplicar**

COPY (SELECT...).

para obtener:

comprobante_venta.json

comprobante_compra.json

**01_migra_base.py [✓]**

hubo unos warnings en

empresa_migra.py

punto_venta.json fue actualizado, faltaba el id_punto_venta = 12

**02_migra_producto.py [✓]**

En la tabla lista.dbf para migrar los productos hay dos códigos sin

familia (ARTICULO): 84480 y 9602 les puse ARTICULO = 1 (tenía valor cero)

**[2]**

**Errores en producto_minimo_migra.py**

Registro 86142: Depósito (0) no encontrado.
Omitiendo.

Registro 86143: Depósito (59) no encontrado.
Omitiendo.

Registro 86144: Depósito (35) no encontrado.
Omitiendo.

Registro 86145: Depósito (0) no encontrado.
Omitiendo.

Registro 86146: Depósito (84) no encontrado.
Omitiendo.

Registro 86147: Depósito (38) no encontrado.
Omitiendo.

Registro 86148: Depósito (89) no encontrado.
Omitiendo.

Registro 86149: Depósito (0) no encontrado.
Omitiendo.

Registro 86150: Depósito (74) no encontrado.
Omitiendo.

Registro 86151: Depósito (79) no encontrado.
Omitiendo.

Registro 86152: Depósito (54) no encontrado.
Omitiendo.

Registro 86153: Depósito (24) no encontrado.
Omitiendo.

Registro 86154: Depósito (59) no encontrado.
Omitiendo.

Registro 86155: Depósito (26) no encontrado.
Omitiendo.

Registro 86156: Depósito (36) no encontrado.
Omitiendo.

Registro 86157: Depósito (33) no encontrado.
Omitiendo.

Registro 86158: Depósito (37) no encontrado.
Omitiendo.

Registro 86159: Depósito (35) no encontrado.
Omitiendo.

Registro 86160: Depósito (22) no encontrado.
Omitiendo.

Registro 86161: Depósito (40) no encontrado.
Omitiendo.

Registro 86162: Depósito (24) no encontrado.
Omitiendo.

Registro 86163: Depósito (24) no encontrado.
Omitiendo.

Registro 86164: Depósito (20) no encontrado.
Omitiendo.

Registro 86165: Depósito (22) no encontrado.
Omitiendo.

Registro 86166: Depósito (24) no encontrado.
Omitiendo.

Registro 86167: Depósito (36) no encontrado.
Omitiendo.

Registro 86168: Depósito (20) no encontrado.
Omitiendo.

**03_migra_cliente.py [✓]**

En la tabla vendedor.dbf / vendedor_migra.py

el campo diasrtos del código 238 está en blanco, le puse 7

porque da error

En clientes.dbf / cliente_migra.py el campo sitiva del código 171825

está en blanco, le puse "RI". OJO no tiene CUIT y otros valores

**04_migra_factura.py [✓]**

En la tabla facturas.dbf / factura_migra.py

el campo compro de Id 1759358

tiene valor "rr", le puse "RR"

En la tabla movstock.dbf / factura_mov_stock_migra.py

el campo id = 11728 está duplicado

Eliminé el primero (analizar este caso)

En detalle_factura_migra.py no se encontró

el producto con ID = 37610 (detven.dbf)

Hay que analizar el caso factura_mov_stock_detalle_migra.py

actualmente deshabilitado. Se había creado un DBF previo para procesar

**[3]**
**05_migra_base_recibo.py [v]**

**06_migra_compra.py [v]**

**07_migra_detalle_recibo.py [v]**
En detalle_recibo_migra.py, en la tabla recibo.dbf hay un
registro (GO 00176938) se eliminó
registro (GO 00217739) se eliminó
HAY QUE REVISAR ESTA MIGRACIÓN **OJO OJO**

En cheque_recibo_migra.py Hay muchos datos que no se consiguen

En tarjeta_recibo_migra.py hay muchos datos que no se consiguen

En retencion_recibo_migra.py hay muchos datos que no se consiguen

En deposito_recibo_migra.py hay muchos datos que no se consiguen

En compensa_factura_migra.py hay muchos datos que no se consiguen

**[4]**

**08_migra_caja.py** 
En vincular_factura_caja.py
no se encontraron facturas
id_caja_detalle       idventa    id_caja
16302                     1585046   2197
9622                       1546129   1292

En asocia_muLt_caja_migra.py hay facturas con cajas no encontradas
=> 2168 no encontrada

**OJO con actualiza_factura_id_caja_muLt.py**

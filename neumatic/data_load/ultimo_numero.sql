-- Este NO VA porque es manual
select f.id_factura, f.fecha_comprobante, f.compro, f.letra_comprobante, f.numero_comprobante, f.id_punto_venta_id
from factura f
join comprobante_venta cv on f.id_comprobante_venta_id = cv.id_comprobante_venta
where cv.codigo_comprobante_venta = 'RS' and cv.tipo_numeracion = 2 and f.id_punto_venta_id = 1
order by f.fecha_comprobante DESC, f.numero_comprobante DESC

-- Consulta Todos los Remitos de numeración Automática (2) y de Punto de Venta 2 ordenados por numero_comprobante descendiente
select f.id_factura, f.fecha_comprobante, f.compro, f.letra_comprobante, f.numero_comprobante, f.id_punto_venta_id
from factura f
join comprobante_venta cv on f.id_comprobante_venta_id = cv.id_comprobante_venta
where cv.remito and cv.tipo_numeracion = 2 and f.id_punto_venta_id = 2
order by f.fecha_comprobante DESC, f.numero_comprobante DESC

-- Consulta Todos los Recibo (RB) con tipo_enumeracion 2 (auto) de un pto. de Vta. ordenados por número descendiente.
select f.id_factura, f.fecha_comprobante, f.compro, f.letra_comprobante, f.numero_comprobante, f.id_punto_venta_id
from factura f
join comprobante_venta cv on f.id_comprobante_venta_id = cv.id_comprobante_venta
where cv.codigo_comprobante_venta = 'RB' and cv.tipo_numeracion = 2 and f.id_punto_venta_id = 2
order by f.fecha_comprobante DESC, f.numero_comprobante DESC

-- Consulta Todos los Recibo Sin Comisión (RR) con tipo_enumeracion 2 (auto) de un pto. de Vta. ordenados por número descendiente.
select f.id_factura, f.fecha_comprobante, f.compro, f.letra_comprobante, f.numero_comprobante, f.id_punto_venta_id
from factura f
join comprobante_venta cv on f.id_comprobante_venta_id = cv.id_comprobante_venta
where cv.codigo_comprobante_venta = 'RR' and cv.tipo_numeracion = 2 and f.id_punto_venta_id = 2
order by f.fecha_comprobante DESC, f.numero_comprobante DESC

-- Consulta Todos los Presupuestos (PR) con tipo_enumeracion 2 (auto) de un pto. de Vta. ordenados por número descendiente.
select f.id_factura, f.fecha_comprobante, f.compro, f.letra_comprobante, f.numero_comprobante, f.id_punto_venta_id
from factura f
join comprobante_venta cv on f.id_comprobante_venta_id = cv.id_comprobante_venta
where cv.codigo_comprobante_venta = 'PR' and cv.tipo_numeracion = 2 and f.id_punto_venta_id = 2
order by f.fecha_comprobante DESC, f.numero_comprobante DESC

-- Consulta Todos los Movimientos Internos (MI) con tipo_enumeracion 2 (auto) de un pto. de Vta. ordenados por número descendiente.
select f.id_factura, f.fecha_comprobante, f.compro, f.letra_comprobante, f.numero_comprobante, f.id_punto_venta_id
from factura f
join comprobante_venta cv on f.id_comprobante_venta_id = cv.id_comprobante_venta
where cv.codigo_comprobante_venta = 'MI' and cv.tipo_numeracion = 2 and f.id_punto_venta_id = 2
order by f.fecha_comprobante DESC, f.numero_comprobante DESC

-----------------------------------------------------------
-- Observaciones
-----------------------------------------------------------
/*
- Comprobantes de tipo Ingreso (IN) no existen comprobantes en Factura pero si en en la tabla Numero.
- Ojo que para algunos comprobantes no se han creado en algunos puntos de ventas, consultar otros puntos de venta cambiando el filtro en el where.
- Recibo Camión solo hay 2 en la tabla Factura y para los ptos. de vtas: 2 y 4
- Recibo Camión Manual no existen Comprobantes registrados en Factura
*/
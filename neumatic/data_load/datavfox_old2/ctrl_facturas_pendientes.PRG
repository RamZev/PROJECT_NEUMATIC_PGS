*.* Tambien se puede verlas facturas pendientes mas antigas
USE facturas ORDER id
BROWSE FOR total#entrega

*.* Obtengo las facturas pendietes de cobrar  y comparo con el saldo del cliente
SELECT cliente,sum(total*codven.mult_cli) as total,clientes.saldo ;
	FROM facturas,codven,clientes ;
	WHERE facturas.cliente=clientes.codigo and facturas.compro = codven.compro AND condicion=2 ;
	GROUP BY cliente ORDER BY cliente

BROWSE FOR total#0 AND saldo#0
BROWSE FOR total#saldo


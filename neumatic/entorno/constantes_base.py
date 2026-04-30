# neumatic\entorno\constantes_base.py

# -- Datos estándares aplicables a los modelos base
ESTATUS_GEN = [
	(True, 'Activo'),
	(False, 'Inactivo'),
]

TIPO_PERSONA = [
	("F", 'Física'),
	("J", 'Jurídica'),
]

CONDICION_VENTA = [
	(1, 'Contado'),
	(2, 'Cuenta Corriente'),
]

CONDICION_COMPRA = [
	(1, 'Contado'),
	(2, 'Cuenta Corriente'),
]

SEXO = [
	("M", 'Masculino'),
	("F", 'Femenino'),
]

TIPO_PRODUCTO_SERVICIO = [
	('P', 'Producto'),
	('S', 'Servicio')
]

SI_NO = [
	(True, 'SI'),
	(False, 'NO')
]

# CLIENTE_VIP = [
# 	(True, 'SI'),
# 	(False, 'NO')
# ]

# CLIENTE_MAYORISTA = [
# 	(True, 'SI'),
# 	(False, 'NO')
# ]

# BLACK_LIST = [
# 	(True, 'Si'),
# 	(False, 'No'),
# ]

TIPO_VENTA = [
	('M', 'Mostrador'),
	('R', 'Revendedor'),
	('E', 'E-Commerce'),
]

WS_MODO = [
	(1, 'Homologación'),
	(2, 'Producción'),
]

CONDICION_PAGO = [
	(1, 'Contado'),
	(2, 'Cuenta Corriente'),
]

JERARQUIA = [
	('A', 'A'),
	('B', 'B'),
	('C', 'C'),
	('D', 'D'),
	('E', 'E'),
	('F', 'F'),
	('G', 'G'),
	('H', 'H'),
	('I', 'I'),
	('J', 'J'),
	('K', 'K'),
	('L', 'L'),
	('M', 'M'),
	('N', 'N'),
	('Ñ', 'Ñ'),
	('O', 'O'),
	('P', 'P'),
	('Q', 'Q'),
	('R', 'R'),
	('S', 'S'),
	('T', 'T'),
	('U', 'U'),
	('V', 'V'),
	('W', 'W'),
	('X', 'X'),
	('Y', 'Y'),
	('Z', 'Z'),
]

JERARQUIAS_CON_ACCESO_TOTAL = ['A', 'B', 'C']

ESTATUS_CHOICES = [ 
	('activos', 'Activos'),
	('inactivos', 'Inactivos'), 
	('todos', 'Todos'), 
]

ORDEN_CHOICES = [ 
	('nombre', 'Nombre'),
	('codigo', 'Código'), 
]

# PRECIO_DESCRIPCION = [
# 	(True, 'SI'),
# 	(False, 'NO')
# ]

MESES = [
		('01', 'Enero'),
		('02', 'Febrero'),
		('03', 'Marzo'),
		('04', 'Abril'),
		('05', 'Mayo'),
		('06', 'Junio'),
		('07', 'Julio'),
		('08', 'Agosto'),
		('09', 'Septiembre'),
		('10', 'Octubre'),
		('11', 'Noviembre'),
		('12', 'Diciembre'),
	]

AGRUPAR = [
	("Producto", "Produto Individual"),
	("Familia", "Familia"),
	("Modelo", "Modelo"),
	("Marca", "Marca")
]
MOSTRAR = [
	("Cantidad", "Cantidad"),
	("Importe", "Importe"),
]
	
ESTADISTICAS = [
	(False, 'Participan en Estadísticas'),
	(True, 'NO Participan en Estadísticas')
]

ORDEN = [
	("Alf", 'Orden Alfabético'),
	("Asc", 'Fecha Ascendente'),
	("Des", 'Fecha Descendente'),
]

TIPO_CUENTA = [
	(1, 'Caja de Ahorros'),
	(2, 'Cuenta Corriente'),
	(3, 'Mcdo/Pago Transferencia'),
]

TIPO_COMPROBANTE = [
	("FACTURA","FACTURA"),
	("NOTA DE CRÉDITO","NOTA DE CRÉDITO"),
	("NOTA DE DÉBITO","NOTA DE DÉBITO"),
	("RECIBO","RECIBO"),
	("AJUSTE","AJUSTE"),
	("MOVIMIENTO INTERNO","MOVIMIENTO INTERNO"),
	("PRESUPUESTO","PRESUPUESTO"),
	("REMITO","REMITO"),
	("EGRESO DE CAJA","EGRESO DE CAJA"),
	("INGRESO DE CAJA","INGRESO DE CAJA"),
]

TIPO_COMPROBANTE_COMPRA = [
	("FACTURA","FACTURA"),
	("NOTA DE CRÉDITO","NOTA DE CRÉDITO"),
	("NOTA DE DÉBITO","NOTA DE DÉBITO"),
	("ORDEN DE PAGO","ORDEN DE PAGO"),
	("AJUSTE","AJUSTE"),
	("RETENCIÓN","RETENCIÓN"),
	("REMITOS","REMITO"),
	("DEVOLUCIÓN","DEVOLUCIÓN"),
]

TIPO_NUMERACION = [
	(1, 'Manual'),
	(2, 'Automática Sistema'),
	(3, 'Automática ARCA'),
]
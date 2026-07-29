# neumatic\entorno\constantes_base.py

# -- Datos estándares aplicables a los modelos base
ESTATUS_GEN = [
	(True, 'Activo'),
	(False, 'Inactivo'),
]

ICON_CHOICES = [
    # Documentos
    ('fas fa-file-invoice-dollar', 'Factura (dólar)'),
    ('fas fa-file-signature', 'Firma / Comprobante manual'),
    ('fas fa-hand-holding-usd', 'Recibo'),
    ('fas fa-file-invoice', 'Factura / Presupuesto'),
    ('fas fa-file-alt', 'Documento'),
    ('fas fa-file-pdf', 'PDF'),
    ('fas fa-file-excel', 'Excel'),
    ('fas fa-file-word', 'Word'),
    ('fas fa-file-image', 'Imagen'),
    # Clientes y personas
    ('fas fa-users', 'Clientes / Usuarios'),
    ('fas fa-user', 'Usuario'),
    ('fas fa-user-plus', 'Agregar usuario'),
    ('fas fa-user-edit', 'Editar usuario'),
    ('fas fa-user-times', 'Eliminar usuario'),
    ('fas fa-id-card', 'Identificación'),
    ('fas fa-address-book', 'Agenda'),
    # Productos e inventario
    ('fas fa-boxes', 'Productos / Cajas'),
    ('fas fa-box', 'Caja'),
    ('fas fa-cube', 'Cubo'),
    ('fas fa-cubes', 'Cubos'),
    ('fas fa-tag', 'Etiqueta'),
    ('fas fa-tags', 'Etiquetas'),
    ('fas fa-barcode', 'Código de barras'),
    ('fas fa-qrcode', 'QR'),
    ('fas fa-shopping-cart', 'Carrito'),
    ('fas fa-cart-plus', 'Agregar al carrito'),
    # Finanzas y gráficos
    ('fas fa-chart-pie', 'Gráfico circular'),
    ('fas fa-chart-bar', 'Gráfico de barras'),
    ('fas fa-chart-line', 'Gráfico de líneas'),
    ('fas fa-chart-area', 'Área'),
    ('fas fa-dollar-sign', 'Dólar'),
    ('fas fa-euro-sign', 'Euro'),
    ('fas fa-pound-sign', 'Libra'),
    ('fas fa-credit-card', 'Tarjeta de crédito'),
    ('fas fa-coins', 'Monedas'),
    ('fas fa-wallet', 'Billetera'),
    ('fas fa-calculator', 'Calculadora'),
    # Acciones comunes
    ('fas fa-home', 'Inicio'),
    ('fas fa-cog', 'Configuración'),
    ('fas fa-cogs', 'Engranajes'),
    ('fas fa-edit', 'Editar'),
    ('fas fa-pencil-alt', 'Lápiz'),
    ('fas fa-trash', 'Eliminar'),
    ('fas fa-plus', 'Agregar'),
    ('fas fa-plus-circle', 'Agregar (círculo)'),
    ('fas fa-minus', 'Quitar'),
    ('fas fa-minus-circle', 'Quitar (círculo)'),
    ('fas fa-search', 'Buscar'),
    ('fas fa-search-plus', 'Buscar (más)'),
    ('fas fa-search-minus', 'Buscar (menos)'),
    ('fas fa-sync', 'Sincronizar'),
    ('fas fa-sync-alt', 'Sincronizar (alternativo)'),
    ('fas fa-undo', 'Deshacer'),
    ('fas fa-redo', 'Rehacer'),
    ('fas fa-save', 'Guardar'),
    ('fas fa-print', 'Imprimir'),
    ('fas fa-eye', 'Ver'),
    ('fas fa-eye-slash', 'Ocultar'),
    ('fas fa-lock', 'Bloqueado'),
    ('fas fa-unlock', 'Desbloqueado'),
    ('fas fa-key', 'Llave'),
    # Navegación
    ('fas fa-arrow-left', 'Flecha izquierda'),
    ('fas fa-arrow-right', 'Flecha derecha'),
    ('fas fa-arrow-up', 'Flecha arriba'),
    ('fas fa-arrow-down', 'Flecha abajo'),
    ('fas fa-chevron-left', 'Chevron izquierda'),
    ('fas fa-chevron-right', 'Chevron derecha'),
    ('fas fa-chevron-up', 'Chevron arriba'),
    ('fas fa-chevron-down', 'Chevron abajo'),
    ('fas fa-angle-left', 'Ángulo izquierdo'),
    ('fas fa-angle-right', 'Ángulo derecho'),
    ('fas fa-angle-up', 'Ángulo arriba'),
    ('fas fa-angle-down', 'Ángulo abajo'),
    # Menú / estructura
    ('fas fa-bars', 'Barras (menú)'),
    ('fas fa-th-large', 'Cuadrícula grande'),
    ('fas fa-th', 'Cuadrícula'),
    ('fas fa-th-list', 'Lista con cuadrícula'),
    ('fas fa-list', 'Lista'),
    ('fas fa-list-alt', 'Lista (alternativa)'),
    ('fas fa-sitemap', 'Mapa del sitio'),
    ('fas fa-folder', 'Carpeta'),
    ('fas fa-folder-open', 'Carpeta abierta'),
    ('fas fa-folder-plus', 'Carpeta agregar'),
    ('fas fa-folder-minus', 'Carpeta quitar'),
    ('fas fa-file', 'Archivo'),
    ('fas fa-file-archive', 'Archivo comprimido'),
    # Comunicación
    ('fas fa-envelope', 'Correo'),
    ('fas fa-envelope-open', 'Correo abierto'),
    ('fas fa-phone', 'Teléfono'),
    ('fas fa-phone-alt', 'Teléfono (alternativo)'),
    ('fas fa-fax', 'Fax'),
    ('fas fa-comment', 'Comentario'),
    ('fas fa-comments', 'Comentarios'),
    ('fas fa-message', 'Mensaje'),
    # Estado
    ('fas fa-check', 'Aceptar'),
    ('fas fa-check-circle', 'Aceptar (círculo)'),
    ('fas fa-times', 'Cancelar'),
    ('fas fa-times-circle', 'Cancelar (círculo)'),
    ('fas fa-exclamation', 'Advertencia'),
    ('fas fa-exclamation-circle', 'Advertencia (círculo)'),
    ('fas fa-exclamation-triangle', 'Triángulo de advertencia'),
    ('fas fa-info', 'Información'),
    ('fas fa-info-circle', 'Información (círculo)'),
    ('fas fa-question', 'Pregunta'),
    ('fas fa-question-circle', 'Pregunta (círculo)'),
    # Otros
    ('fas fa-clock', 'Reloj'),
    ('fas fa-calendar', 'Calendario'),
    ('fas fa-calendar-alt', 'Calendario (alternativo)'),
    ('fas fa-flag', 'Bandera'),
    ('fas fa-flag-checkered', 'Bandera a cuadros'),
    ('fas fa-heart', 'Corazón'),
    ('fas fa-star', 'Estrella'),
    ('fas fa-star-half-alt', 'Media estrella'),
    ('fas fa-download', 'Descargar'),
    ('fas fa-upload', 'Subir'),
    ('fas fa-cloud', 'Nube'),
    ('fas fa-cloud-upload-alt', 'Nube (subir)'),
    ('fas fa-cloud-download-alt', 'Nube (descargar)'),
    ('fas fa-database', 'Base de datos'),
    ('fas fa-server', 'Servidor'),
    ('fas fa-wifi', 'Wi-Fi'),
    ('fas fa-bluetooth', 'Bluetooth'),
    ('fas fa-camera', 'Cámara'),
    ('fas fa-video', 'Video'),
    ('fas fa-music', 'Música'),
    ('fas fa-play', 'Reproducir'),
    ('fas fa-stop', 'Detener'),
    ('fas fa-pause', 'Pausa'),
    ('fas fa-fast-forward', 'Avance rápido'),
    ('fas fa-fast-backward', 'Retroceso rápido'),
    ('fas fa-step-forward', 'Siguiente'),
    ('fas fa-step-backward', 'Anterior'),
    ('fas fa-volume-up', 'Volumen alto'),
    ('fas fa-volume-down', 'Volumen bajo'),
    ('fas fa-volume-off', 'Silencio'),
    ('fas fa-headphones', 'Auriculares'),
    ('fas fa-microphone', 'Micrófono'),
    ('fas fa-microphone-slash', 'Micrófono silenciado'),
    ('fas fa-crown', 'Corona'),
    ('fas fa-gem', 'Gema'),
    ('fas fa-trophy', 'Trofeo'),
    ('fas fa-gift', 'Regalo'),
    ('fas fa-globe', 'Globo terráqueo'),
    ('fas fa-map-marker-alt', 'Marcador de mapa'),
    ('fas fa-road', 'Carretera'),
    ('fas fa-shipping-fast', 'Envío rápido'),
    ('fas fa-truck', 'Camión'),
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

# JERARQUIA = [
# 	('A', 'A'),
# 	('B', 'B'),
# 	('C', 'C'),
# 	('D', 'D'),
# 	('E', 'E'),
# 	('F', 'F'),
# 	('G', 'G'),
# 	('H', 'H'),
# 	('I', 'I'),
# 	('J', 'J'),
# 	('K', 'K'),
# 	('L', 'L'),
# 	('M', 'M'),
# 	('N', 'N'),
# 	('Ñ', 'Ñ'),
# 	('O', 'O'),
# 	('P', 'P'),
# 	('Q', 'Q'),
# 	('R', 'R'),
# 	('S', 'S'),
# 	('T', 'T'),
# 	('U', 'U'),
# 	('V', 'V'),
# 	('W', 'W'),
# 	('X', 'X'),
# 	('Y', 'Y'),
# 	('Z', 'Z'),
# ]
JERARQUIA = [
	('A', 'A'),
	('B', 'B'),
	('C', 'C'),
	#-------------
	('D', 'D'),
	('E', 'E'),
	('F', 'F'),
	#-------------
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

FILTRO_CONDICION_VENTA = [
	(1, 'Contado'),
	(2, 'Cuenta Corriente'),
	(0, 'Ambos'),
]

# Motivos de autorización para el modelo Valida (solo para comprobantes de venta)
MOTIVO_AUTORIZACION = [
    ('VENCIMIENTO', 'Documentos vencidos'),
    ('LIMITE_CREDITO', 'Límite de crédito excedido'),
]
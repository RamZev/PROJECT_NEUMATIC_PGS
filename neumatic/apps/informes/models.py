from django.db import models


#-----------------------------------------------------------------------------
# Saldos Clientes.
#-----------------------------------------------------------------------------
class SaldosClientesManager(models.Manager):

	def obtener_saldos_clientes(self, fecha_hasta, id_vendedor=None):
		
		#-- Se crea la consulta.
		query = """
			SELECT
				id_cliente_id,
				nombre_cliente,
				domicilio_cliente,
				nombre_localidad,
				codigo_postal,
				telefono_cliente,
				sub_cuenta,
				id_vendedor_id,
				nombre_vendedor,
				SUM(total * (mult_saldo * 1.00)) AS saldo,
				MIN(CASE WHEN condicion_comprobante = 2 AND mult_saldo <> 0 AND total <> entrega THEN fecha_comprobante END) AS primer_fact_impaga,
				MAX(fecha_pago) AS ultimo_pago
			FROM
				VLSaldosClientes
			WHERE 
				fecha_comprobante <= %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_hasta]
		
		#-- Filtros adicionales.
		if id_vendedor:
			query += " AND id_vendedor_id = %s"
			params.append(id_vendedor)
		
		#-- Se completa la consulta.
		query += """
			GROUP BY 
				id_cliente_id, nombre_cliente, domicilio_cliente, nombre_localidad, codigo_postal, telefono_cliente, sub_cuenta, id_vendedor_id, nombre_vendedor
			HAVING 
				ROUND(SUM(total * (mult_saldo * 1.00)), 2) <> 0
			ORDER BY
				nombre_cliente
		"""
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


#-- Modelo asociado a una consulta RAW SQL con parámetros dinámicos.
class VLSaldosClientes(models.Model):
	id_cliente_id = models.IntegerField(primary_key=True)
	fecha_comprobante = models.DateField()
	nombre_cliente = models.CharField(max_length=50)
	domicilio_cliente = models.CharField(max_length=50)
	nombre_localidad = models.CharField(max_length=30)
	codigo_postal = models.CharField(max_length=5)
	telefono_cliente = models.CharField(max_length=15)
	sub_cuenta = models.CharField(max_length=6)
	id_vendedor_id = models.IntegerField()
	total = models.DecimalField(max_digits=14, decimal_places=2)
	
	objects = SaldosClientesManager()
	
	class Meta:
		managed = False  #-- No gestionamos la creación/edición de la vista (Ignorado para migraciones).
		db_table = 'vlsaldosclientes'  #-- Nombre de la vista en la base de datos.
		verbose_name = ('Saldos de Clientes')
		verbose_name_plural = ('Saldos de Clientes')
		ordering = ['nombre_cliente']


#-----------------------------------------------------------------------------
# Resumen Cuenta Corriente.
#-----------------------------------------------------------------------------
class ResumenCtaCteManager(models.Manager):
	
	def obtener_saldo_anterior(self, id_cliente, fecha_desde):
		""" Método que calcula y devuelve el saldo anterior a la fecha desde de un cliente dado. """
		
		from decimal import Decimal
		
		#-- Se crea la consulta.
		query = """
			SELECT 
				v.id_cliente_id, 
				COALESCE(ROUND(SUM(v.total * 1.0), 2), 0.00) AS saldo_anterior 
			FROM
				VLResumenCtaCte v 
			WHERE
				v.id_cliente_id = %s
				AND v.fecha_comprobante < %s
				AND v.condicion_comprobante = 2;
		"""
		
		#-- Ejecutar la consulta y extraer el valor.
		resultados = self.raw(query, [id_cliente, fecha_desde])
		
		#-- Extraer el primer valor del resultado.
		for resultado in resultados:
			return Decimal(str(resultado.saldo_anterior)) if resultado.saldo_anterior else Decimal('0.00')
		
		return Decimal('0.00')
		
	def obtener_fact_pendientes(self, id_cliente):
		""" Se determina los comprobantes pendientes de un cliente determinado. """
		
		from decimal import Decimal
		
		#-- Se crea la consulta.
		query = """
			SELECT 
				v.id_cliente_id, 
				v.razon_social, 
				v.nombre_comprobante_venta, 
				v.letra_comprobante, 
				v.numero_comprobante, 
				v.numero, 
				v.fecha_comprobante, 
				v.remito, 
				v.condicion_comprobante, 
				v.condicion, 
				v.total, 
				v.entrega, 
				v.debe, 
				v.haber,
				(v.debe + v.haber) AS saldo_movimiento,
				v.intereses,
				v.marca,
				v.no_estadist
			FROM
				VLResumenCtaCte v
			WHERE
				v.id_cliente_id = %s
				AND v.total <> v.entrega
				AND v.condicion_comprobante = 2
		"""
		
		#-- Se añaden parámetros.
		params = [id_cliente]
		
		#-- Se ejecuta la consulta.
		resultados_raw = self.raw(query, params)
		
		resultados = []
		saldo_acumulado = Decimal('0.00')
		
		for item in resultados_raw:
			saldo_movimiento = Decimal(str(item.saldo_movimiento)) if hasattr(item, 'saldo_movimiento') and item.saldo_movimiento is not None else Decimal('0.00')
			saldo_acumulado += saldo_movimiento
			item.saldo_acumulado = saldo_acumulado
			resultados.append(item)
		
		return resultados
	
	def obtener_resumen_cta_cte(self, id_cliente, fecha_desde, fecha_hasta, condicion_venta1, condicion_venta2):
		""" Determina el Resumen de Cuenta Corriente de un cliente y período determinados. """
		
		from decimal import Decimal
		
		#-- Obtener el saldo anterior.
		saldo_anterior = self.obtener_saldo_anterior(id_cliente, fecha_desde)
		
		#-- Se crea la consulta.
		query = """
			SELECT 
				v.id_cliente_id, 
				v.razon_social, 
				v.nombre_comprobante_venta, 
				v.letra_comprobante, 
				v.numero_comprobante, 
				v.numero, 
				v.fecha_comprobante, 
				v.remito, 
				v.condicion_comprobante, 
				v.condicion, 
				v.total, 
				v.entrega, 
				v.debe, 
				v.haber,
				CASE
					WHEN v.condicion_comprobante = 2 THEN (v.debe + v.haber)
					ELSE 0
				END AS saldo_movimiento,
				v.intereses,
				v.marca,
				v.no_estadist
			FROM
				VLResumenCtaCte v
			WHERE
				v.id_cliente_id = %s 
				AND v.fecha_comprobante BETWEEN %s AND %s 
				AND v.condicion_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [id_cliente, fecha_desde, fecha_hasta, condicion_venta1, condicion_venta2]
		
		#-- Se ejecuta la consulta.
		resultados_raw = self.raw(query, params)
		
		#-- Calcular saldo acumulado en Python.
		resultados = []
		saldo_acumulado = saldo_anterior
		
		for item in resultados_raw:
			#-- Convertir saldo_movimiento a Decimal.
			saldo_movimiento = Decimal(str(item.saldo_movimiento)) if hasattr(item, 'saldo_movimiento') and item.saldo_movimiento is not None else Decimal('0.00')
			
			#-- Acumular.
			saldo_acumulado += saldo_movimiento
			
			#-- Asignar el saldo acumulado al objeto.
			item.saldo_acumulado = saldo_acumulado
			resultados.append(item)
		
		return resultados


class VLResumenCtaCte(models.Model):
	id_cliente_id = models.IntegerField(primary_key=True)
	razon_social = models.CharField(max_length=50)
	nombre_comprobante_venta = models.CharField(max_length=50)
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	numero = models.CharField(max_length=13)
	fecha_comprobante = models.DateField()
	remito = models.CharField(max_length=15)
	condicion_comprobante = models.IntegerField()
	total = models.DecimalField(max_digits=14, decimal_places=2)
	entrega = models.DecimalField(max_digits=14, decimal_places=2)
	saldo_acumulado = models.DecimalField(max_digits=14, decimal_places=2)
	intereses = models.DecimalField(max_digits=14, decimal_places=2)
	marca = models.CharField(max_length=1)
	
	objects = ResumenCtaCteManager()
	
	class Meta:
		managed = False
		db_table = 'vlresumenctacte'
		verbose_name = ('Resumen de Cta. Cte.')
		verbose_name_plural = ('Resumen de Cta. Cte.')
		ordering = ['razon_social']


#-----------------------------------------------------------------------------
# Mercadería por Cliente.
#-----------------------------------------------------------------------------
class MercaderiaPorClienteManager(models.Manager):

	def obtener_mercaderia_por_cliente(self, id_cliente, fecha_desde, fecha_hasta):
		""" Se determina los comprobantes pendientes de un cliente determinado. """
		
		#-- Se crea la consulta.
		query = """
			SELECT
				* 
			FROM
				VLMercaderiaPorCliente v 
			WHERE
				v.id_cliente_id = %s
				AND v.fecha_comprobante BETWEEN %s AND %s
			ORDER BY
				v.fecha_comprobante, v.numero_comprobante;
		"""
		
		#-- Se añaden parámetros.
		params = [id_cliente, fecha_desde, fecha_hasta]
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)

		
class VLMercaderiaPorCliente(models.Model):
	id_cliente_id = models.IntegerField(primary_key=True)
	nombre_comprobante_venta = models.CharField(max_length=50)
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	numero = models.CharField(max_length=13)
	fecha_comprobante = models.DateField()
	nombre_producto_marca = models.CharField(max_length=50)
	medida = models.CharField(max_length=15)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=6, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	
	objects = MercaderiaPorClienteManager()
	
	class Meta:
		managed = False
		db_table = 'vlmercaderiaporcliente'
		verbose_name = ('Mercadería por Cliente')
		verbose_name_plural = ('Mercadería por Cliente')
		ordering = ['id_cliente_id', 'fecha_comprobante']


#-----------------------------------------------------------------------------
# Remitos por Clientes.
#-----------------------------------------------------------------------------
class RemitosClientesManager(models.Manager):

	def obtener_remitos_por_cliente(self, id_cliente, fecha_desde, fecha_hasta):
		""" Se determina los Remitos de un cliente determinado. """
		
		#-- Se crea la consulta parametrizada.
		query = """
			SELECT
				*
			FROM
				VLRemitosClientes
			WHERE
				id_cliente_id = %s
				AND codigo_comprobante_venta BETWEEN %s AND %s
				AND fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [id_cliente, "RD", "RT", fecha_desde, fecha_hasta]
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by fecha_comprobante, numero_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLRemitosClientes(models.Model):
	id_cliente_id = models.IntegerField(primary_key=True)
	id_comprobante_venta_id = models.IntegerField()
	codigo_comprobante_venta = models.CharField(max_length=3)
	nombre_comprobante_venta = models.CharField(max_length=50)
	fecha_comprobante = models.DateField()
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	numero = models.CharField(max_length=13)
	nombre_producto = models.CharField(max_length=50)
	medida = models.CharField(max_length=15)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=6, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	
	objects = RemitosClientesManager()
	
	class Meta:
		managed = False
		db_table = 'vlremitosclientes'
		verbose_name = ('Remitos por Clientes')
		verbose_name_plural = ('Remitos por Clientes')
		ordering = ['id_cliente_id', 'fecha_comprobante', 'numero_comprobante']


#-----------------------------------------------------------------------------
# Total Remitos por Clientes.
#-----------------------------------------------------------------------------
class TotalRemitosClientesManager(models.Manager):

	def obtener_total_remitos_cliente(self, id_cliente, fecha_desde, fecha_hasta):
		""" Se determina los Totales de Remitos por clientes. """
		
		#-- Se crea la consulta parametrizada.
		query = """
			SELECT 
				id_cliente_id, 
				fecha_comprobante, 
				nombre_cliente, 
				domicilio_cliente, 
				codigo_postal, 
				nombre_iva, 
				cuit, 
				telefono_cliente, 
				SUM(total) AS total
			FROM
				VLTotalRemitosClientes 
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if id_cliente:
			query += " AND id_cliente_id = %s "
			params.append(id_cliente)
		
		#-- Completar la consulta.
		query += "GROUP BY id_cliente_id, fecha_comprobante, nombre_cliente, domicilio_cliente, codigo_postal, nombre_iva, cuit, telefono_cliente"
	
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by nombre_cliente"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLTotalRemitosClientes(models.Model):
	id_cliente_id = models.IntegerField(primary_key=True)
	fecha_comprobante = models.DateField()
	nombre_cliente = models.CharField(max_length=50)
	domicilio_cliente = models.CharField(max_length=50)
	codigo_postal = models.CharField(max_length=5)
	nombre_iva = models.CharField(max_length=25)
	cuit = models.IntegerField()
	telefono_cliente = models.CharField(max_length=15)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	
	objects = TotalRemitosClientesManager()
	
	class Meta:
		managed = False
		db_table = 'vltotalremitosclientes'
		verbose_name = ('Totales de Remitos por Clientes')
		verbose_name_plural = ('Totales de Remitos por Clientes')
		ordering = ['nombre_cliente']


#-----------------------------------------------------------------------------
# Ventas por Localidad.
#-----------------------------------------------------------------------------
class VentaComproLocalidadManager(models.Manager):

	def obtener_venta_compro_localidad(self, fecha_desde, fecha_hasta, sucursal=None, codigo_postal=None):
		"""
		Retorna un RawQuerySet con las ventas dentro del rango de fechas, y opcionalmente
		filtra por sucursal y código postal, aplicando todo el filtrado directamente en SQL.
		"""
		
		#-- Se crea la consulta parametrizada.
		query = """
			SELECT
				*
			FROM
				VLVentaComproLocalidad 
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(sucursal.id_sucursal)
		
		if codigo_postal:
			query += " AND codigo_postal = %s"
			params.append(codigo_postal)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by fecha_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLVentaComproLocalidad(models.Model):
	id_cliente_id = models.IntegerField(primary_key=True)
	id_sucursal_id = models.IntegerField()
	fecha_comprobante = models.DateField()
	nombre_cliente = models.CharField(max_length=50)
	cuit = models.IntegerField()
	codigo_postal = models.CharField(max_length=5)
	codigo_comprobante_venta = models.CharField(max_length=3)
	nombre_comprobante_venta = models.CharField(max_length=50)
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	comprobante = models.CharField(max_length=17)
	gravado = models.DecimalField(max_digits=14, decimal_places=2)
	exento = models.DecimalField(max_digits=14, decimal_places=2)
	iva = models.DecimalField(max_digits=14, decimal_places=2)
	percep_ib = models.DecimalField(max_digits=14, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	iniciales = models.CharField(max_length=3)
	
	objects = VentaComproLocalidadManager()
	
	class Meta:
		managed = False
		db_table = 'vlventacomprololocalidad'
		verbose_name = ('Ventas por Localidad')
		verbose_name_plural = ('Ventas por Localidad')
		ordering = ['fecha_comprobante']


#-----------------------------------------------------------------------------
# Ventas por Mostrador.
#-----------------------------------------------------------------------------
class VentaMostradorManager(models.Manager):

	def obtener_venta_mostrador(self, fecha_desde, fecha_hasta, sucursal=None, tipo_venta=None, tipo_cliente=None, tipo_producto=None):
		""" Se determina las Ventas por Mostrador por un rango de fechas, aplicando filtros. """
		
		#-- Se crea la consulta.
		query = """
			SELECT
				*
			FROM
				VLVentaMostrador 
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(sucursal.id_sucursal)
		
		if tipo_venta and tipo_venta != "T":
			query += " AND reventa = %s"
			params.append(tipo_venta)
		
		if tipo_cliente == "M":
			query += " AND mayorista = %s"
			params.append(True)
		elif tipo_cliente == "R":
			query += " AND mayorista = %s"
			params.append(False)
		
		if tipo_producto and tipo_producto != "T":
			query += " AND tipo_producto = %s"
			params.append(tipo_producto)		
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by fecha_comprobante, numero_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLVentaMostrador(models.Model):
	id_detalle_factura = models.IntegerField(primary_key=True)
	nombre_comprobante_venta = models.CharField(max_length=50)
	codigo_comprobante_venta = models.CharField(max_length=3)
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	comprobante = models.CharField(max_length=17)
	fecha_comprobante = models.DateField()
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	mayorista = models.BooleanField()
	reventa = models.CharField(max_length=1)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	tipo_producto = models.CharField(max_length=1)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	precio = models.DecimalField(max_digits=14, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	id_sucursal_id = models.IntegerField()
	
	objects = VentaMostradorManager()
	
	class Meta:
		managed = False
		db_table = 'vlventamostrador'
		verbose_name = ('Ventas por Mostrador')
		verbose_name_plural = ('Ventas por Mostrador')
		ordering = ['fecha_comprobante', 'numero_comprobante']


#-----------------------------------------------------------------------------
# Ventas por Comprobantes.
#-----------------------------------------------------------------------------
class VentaComproManager(models.Manager):

	def obtener_venta_compro(self, fecha_desde, fecha_hasta, sucursal=None):
		""" Se determina las Ventas por Comprobante por un rango de fechas, aplicando filtros. """
		
		#-- Se crea la consulta parametrizada.
		query = """
			SELECT
				*
			FROM
				VLVentaCompro 
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(sucursal.id_sucursal)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by nombre_comprobante_venta, letra_comprobante, numero_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLVentaCompro(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	nombre_comprobante_venta = models.CharField(max_length=50)
	codigo_comprobante_venta = models.CharField(max_length=3)
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	comprobante = models.CharField(max_length=17)
	fecha_comprobante = models.DateField()
	dias_vencimiento = models.IntegerField()
	condicion = models.CharField(max_length=9)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	gravado = models.DecimalField(max_digits=14, decimal_places=2)
	iva = models.DecimalField(max_digits=14, decimal_places=2)
	percep_ib = models.DecimalField(max_digits=14, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	id_sucursal_id = models.IntegerField()
	
	objects = VentaComproManager()
	
	class Meta:
		managed = False
		db_table = 'vlventacompro'
		verbose_name = ('Ventas por Comprobantes')
		verbose_name_plural = ('Ventas por Comprobantes')
		ordering = ['comprobante']


#-----------------------------------------------------------------------------
# Comprobantes Vencidos.
#-----------------------------------------------------------------------------
class ComprobantesVencidosManager(models.Manager):
	
	def obtener_compro_vencidos(self, dias, id_vendedor=None, id_sucursal=None):
		""" Se determina los Comprobantes vencidos según parámetro indicado por vendedor o todos los vendedores,
		una sucursal o todas. """
		
		#-- Se crea la consulta.
		query = """
			SELECT
				* 
			FROM
				VLComprobantesVencidos 
			WHERE
				dias_vencidos > %s
		"""
		
		#-- Se añaden parámetros.
		params = [dias]
		
		#-- Filtros adicionales.
		if id_vendedor:
			query += " AND id_vendedor_id = %s"
			params.append(id_vendedor)
		
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by fecha_comprobante, numero_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLComprobantesVencidos(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	fecha_comprobante = models.DateField()
	dias_vencidos = models.IntegerField()
	codigo_comprobante_venta = models.CharField(max_length=3)
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	comprobante = models.CharField(max_length=17)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	entrega = models.DecimalField(max_digits=14, decimal_places=2)
	saldo = models.DecimalField(max_digits=14, decimal_places=2)
	id_sucursal_id = models.IntegerField()
	id_vendedor_id = models.IntegerField()
	
	objects = ComprobantesVencidosManager()
	
	class Meta:
		managed = False
		db_table = 'vlcomprobantesvencidos'
		verbose_name = ('Comprobantes Vencidos')
		verbose_name_plural = ('Comprobantes Vencidos')
		ordering = ['fecha_comprobante']


#-----------------------------------------------------------------------------
# Remitos Pendientes.
#-----------------------------------------------------------------------------
class RemitosPendientesManager(models.Manager):
	
	def obtener_remitos_pendientes(self, filtrar_por, id_vendedor=None, id_cli_desde=0, id_cli_hasta=0, id_sucursal=None):
		""" Permite obtener los Remitos Pendientes por procesar según parámetros indicados: por Vendedor, rango de Ids de Cliente, 
		Sucursal de Facturación o Sucursal del Cliente. """
		
		#-- Se crea la consulta.
		query = """
			SELECT
				*
			FROM
				VLRemitosPendientes
		"""
		
		#-- Filtros adicionales.
		match filtrar_por:
			case "vendedor":
				query += " WHERE id_vendedor_id = %s"
				params = [id_vendedor]
				
			case "clientes":
				query += " WHERE id_cliente_id BETWEEN %s AND %s"
				params = [id_cli_desde, id_cli_hasta]
				
			case "sucursal_fac":
				query += " WHERE id_sucursal_fac = %s"
				params = [id_sucursal]
				
			case "sucursal_cli":
				query += " WHERE id_sucursal_cli = %s"
				params = [id_sucursal]
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by nombre_cliente, fecha_comprobante, numero_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLRemitosPendientes(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	nombre_comprobante_venta = models.CharField(max_length=50)
	fecha_comprobante = models.DateField()
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	comprobante = models.CharField(max_length=17)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	medida = models.CharField(max_length=15)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=6, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	id_vendedor_id = models.IntegerField()
	id_sucursal_fac = models.IntegerField()
	id_sucursal_cli = models.IntegerField()
	
	
	objects = RemitosPendientesManager()
	
	class Meta:
		managed = False
		db_table = 'vlremitospendientes'
		verbose_name = ('Remitos Pendientes')
		verbose_name_plural = ('Remitos Pendientes')
		ordering = ['nombre_cliente', 'fecha_comprobante', 'numero_comprobante']


#-----------------------------------------------------------------------------
# Remitos por Vendedor.
#-----------------------------------------------------------------------------
class RemitosVendedorManager(models.Manager):
	
	def obtener_remitos_vendedor(self, id_vendedor, fecha_desde, fecha_hasta):
		""" Permite obtener los Remitos de un Vendedor específico en un período de tiempo. """
		
		#-- Se crea la consulta.
		query = """
			SELECT
				* 
			FROM
				VLRemitosVendedor 
			WHERE
				id_vendedor_id = %s
				AND fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [id_vendedor, fecha_desde, fecha_hasta]
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by nombre_cliente, fecha_comprobante, numero_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLRemitosVendedor(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	nombre_comprobante_venta = models.CharField(max_length=50)
	fecha_comprobante = models.DateField()
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	comprobante = models.CharField(max_length=17)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	medida = models.CharField(max_length=15)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=6, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	id_vendedor_id = models.IntegerField()
	
	objects = RemitosVendedorManager()
	
	class Meta:
		managed = False
		db_table = 'vlremitosvendedor'
		verbose_name = ('Remitos por Vendedor')
		verbose_name_plural = ('Remitos por Vendedor')
		ordering = ['nombre_cliente', 'fecha_comprobante', 'numero_comprobante']


#-----------------------------------------------------------------------------
# Libro I.V.A. Ventas - Detalle.
#-----------------------------------------------------------------------------
class IVAVentasFULLManager(models.Manager):
	
	def obtener_datos(self, id_sucursal, anno, mes):
		
		#-- Se crea la consulta.
		query = """
			SELECT
				*
			FROM
				VLIVAVentasFULL
			WHERE
			 	EXTRACT(YEAR FROM fecha_comprobante) = %s
				AND EXTRACT(MONTH FROM fecha_comprobante) = %s
		"""
		
		#-- Se añaden parámetros.
		params = [str(anno), str(mes)]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		#-- Agregar el ordenamiento.
		query += " ORDER by fecha_comprobante, letra_comprobante, numero_comprobante"
		
		#-- Ejecutar la consulta y devolver los resultados.
		return self.raw(query, params)


class VLIVAVentasFULL(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	nombre_cliente = models.CharField(max_length=50)
	codigo_iva = models.CharField(max_length=4)
	cuit = models.IntegerField()
	nombre_comprobante_venta = models.CharField(max_length=50)
	codigo_comprobante_venta = models.CharField(max_length=3)
	fecha_comprobante = models.DateField()
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	comprobante = models.CharField(max_length=17)
	gravado = models.DecimalField(max_digits=14, decimal_places=2)
	exento = models.DecimalField(max_digits=14, decimal_places=2)
	iva = models.DecimalField(max_digits=14, decimal_places=2)
	percep_ib = models.DecimalField(max_digits=14, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	id_sucursal_id = models.IntegerField()
	
	objects = IVAVentasFULLManager()
	
	class Meta:
		managed = False
		db_table = 'vlivaventasfull'
		verbose_name = ('Libro de I.V.A. Ventas - Detalle')
		verbose_name_plural = ('Libro de I.V.A. Ventas - Detalle')
		ordering = ['fecha_comprobante', 'numero_comprobante']


#-----------------------------------------------------------------------------
# Libro I.V.A. Ventas - Totales por Provincias.
#-----------------------------------------------------------------------------
class VLIVAVentasProvinciasManager(models.Manager):
	
	def obtener_datos(self, id_sucursal, anno, mes):
		
		#-- Se crea la consulta.
		query = """
			SELECT 
				ROW_NUMBER() OVER (ORDER BY nombre_provincia) as id_factura,
				nombre_provincia,
				ROUND(SUM(gravado), 2) AS gravado,
				ROUND(SUM(exento), 2) AS exento,
				ROUND(SUM(iva), 2) AS iva,
				ROUND(SUM(percep_ib), 2) AS percep_ib,
				ROUND(SUM(total), 2) AS total,
				0 as id_provincia,					-- Valor por defecto
				CURRENT_DATE as fecha_comprobante,	-- Fecha actual
				0 as id_sucursal_id					-- Valor por defecto
			FROM
				VLIVAVentasProvincias
			WHERE
				EXTRACT(YEAR FROM fecha_comprobante) = %s
				AND EXTRACT(MONTH FROM fecha_comprobante) = %s
		"""
		
		#-- Se añaden parámetros.
		params = [str(anno), str(mes)]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		#-- Se completa la consulta.
		query += " GROUP BY nombre_provincia"
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by nombre_provincia"
		
		#-- Ejecutar la consulta y devolver los resultados.
		return self.raw(query, params)


class VLIVAVentasProvincias(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	id_provincia = models.IntegerField()
	nombre_provincia = models.CharField(max_length=30)
	fecha_comprobante = models.DateField()
	gravado = models.DecimalField(max_digits=14, decimal_places=2)
	exento = models.DecimalField(max_digits=14, decimal_places=2)
	iva = models.DecimalField(max_digits=14, decimal_places=2)
	percep_ib = models.DecimalField(max_digits=14, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	id_sucursal_id = models.IntegerField()
	
	objects = VLIVAVentasProvinciasManager()
	
	class Meta:
		managed = False
		db_table = 'vlivaventasprovincias'
		verbose_name = ('Libro de I.V.A. Ventas - Totales por Provincias')
		verbose_name_plural = ('Libro de I.V.A. Ventas - Totales por Provincias')
		ordering = ['nombre_provincia']


#-----------------------------------------------------------------------------
# Libro I.V.A. Ventas - Totales para SITRIB.
#-----------------------------------------------------------------------------
class VLIVAVentasSitribManager(models.Manager):
	
	def obtener_datos(self, id_sucursal, anno, mes):
		
		#-- Se crea la consulta.
		query = """
			SELECT 
				ROW_NUMBER() OVER (ORDER BY codigo_iva) as id_factura,
				codigo_iva,
				nombre_iva,
				ROUND(SUM(gravado), 2) AS gravado, 
				ROUND(SUM(exento), 2) AS exento, 
				ROUND(SUM(iva), 2) AS iva, 
				ROUND(SUM(percep_ib), 2) AS percep_ib, 
				ROUND(SUM(total), 2) AS total,
				CURRENT_DATE as fecha_comprobante,	-- Fecha actual
				0 as id_sucursal_id					-- Valor por defecto
			FROM
				VLIVAVentasSitrib
			WHERE
			 	EXTRACT(YEAR FROM fecha_comprobante) = %s
				AND EXTRACT(MONTH FROM fecha_comprobante) = %s
		"""
		
		#-- Se añaden parámetros.
		params = [str(anno), str(mes)]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		#-- Se completa la consulta.
		query += " GROUP BY codigo_iva, nombre_iva"
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by codigo_iva"
		
		#-- Ejecutar la consulta y devolver los resultados.
		return self.raw(query, params)


class VLIVAVentasSitrib(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	fecha_comprobante = models.DateField()
	codigo_iva = models.CharField(max_length=4)
	nombre_iva = models.CharField(max_length=25)
	gravado = models.DecimalField(max_digits=14, decimal_places=2)
	exento = models.DecimalField(max_digits=14, decimal_places=2)
	iva = models.DecimalField(max_digits=14, decimal_places=2)
	percep_ib = models.DecimalField(max_digits=14, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	id_sucursal_id = models.IntegerField()
	
	objects = VLIVAVentasSitribManager()
	
	class Meta:
		managed = False
		db_table = 'vlivaventassitrib'
		verbose_name = ('Libro de I.V.A. Ventas - Totales para SITRIB')
		verbose_name_plural = ('Libro de I.V.A. Ventas - Totales para SITRIB')
		ordering = ['codigo_iva']


#-----------------------------------------------------------------------------
# Percepción IB por Vendedores - Totales.
#-----------------------------------------------------------------------------
class VLPercepIBVendedorTotalesManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, orden='nombre'):
		
		#-- Mapeo seguro de opciones de orden.
		orden_map = {
			'nombre': 'nombre_vendedor',
			'codigo': 'id_vendedor_id'
		}
		order_by = orden_map.get(orden, 'id_vendedor_id')
		
		#-- Se crea la consulta con ORDER BY directo (no placeholder).
		query = f"""
			SELECT 
				ROW_NUMBER() OVER (ORDER BY id_vendedor_id) as id_factura,
				id_vendedor_id,
				nombre_vendedor,
				ROUND(SUM(neto), 2) AS neto, 
				ROUND(SUM(percep_ib), 2) AS percep_ib,
				CURRENT_DATE as fecha_comprobante	-- Fecha actual
			FROM
				VLPercepIBVendedorTotales
			WHERE
				fecha_comprobante BETWEEN %s AND %s
			GROUP BY
				id_vendedor_id, nombre_vendedor
			ORDER BY
				{order_by}
		"""
		
		#-- Se añaden parámetros (solo las fechas, sin el ORDER BY).
		params = [fecha_desde, fecha_hasta]
		
		#-- Ejecutar la consulta y devolver los resultados.
		return self.raw(query, params)


class VLPercepIBVendedorTotales(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	fecha_comprobante = models.DateField()
	id_vendedor_id = models.IntegerField()
	nombre_vendedor = models.CharField(max_length=30)
	neto = models.DecimalField(max_digits=14, decimal_places=2)
	percep_ib = models.DecimalField(max_digits=14, decimal_places=2)
	
	objects = VLPercepIBVendedorTotalesManager()
	
	class Meta:
		managed = False
		db_table = 'vlpercepibvendedortotales'
		verbose_name = ('Percepciones por Vendedor - Totales')
		verbose_name_plural = ('Percepciones por Vendedor - Totales')


#-----------------------------------------------------------------------------
# Percepción IB por Vendedores - Detallado.
#-----------------------------------------------------------------------------
class VLPercepIBVendedorDetalladoManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, orden='nombre'):
		
		#-- Mapeo seguro de opciones de orden.
		orden_map = {
			'nombre': 'nombre_vendedor',
			'codigo': 'id_vendedor_id'
		}
		order_by = orden_map.get(orden, 'id_vendedor_id')
		
		#-- Se crea la consulta.
		query = """
			SELECT
				* 
			FROM
				VLPercepIBVendedorDetallado
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Lista de parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		# query += " ORDER by nombre_vendedor, fecha_comprobante, numero_comprobante"
		query += f" ORDER by {order_by}, fecha_comprobante, numero_comprobante"
		
		#-- Ejecutar la consulta y devolver los resultados.
		return self.raw(query, params)


class VLPercepIBVendedorDetallado(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	id_vendedor_id = models.IntegerField()
	nombre_vendedor = models.CharField(max_length=30)
	compro = models.CharField(max_length=3)	
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	fecha_comprobante = models.DateField()
	comprobante = models.CharField(max_length=30)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	cuit = models.IntegerField()
	neto = models.DecimalField(max_digits=14, decimal_places=2)
	percep_ib = models.DecimalField(max_digits=14, decimal_places=2)
	
	objects = VLPercepIBVendedorDetalladoManager()
	
	class Meta:
		managed = False
		db_table = 'vlpercepibvendedordetallado'
		verbose_name = ('Percepciones por Vendedor - Detallado')
		verbose_name_plural = ('Percepciones por Vendedor - Detallado')


#-----------------------------------------------------------------------------
# Percepción IB por Sub Cuentas - Totales.
#-----------------------------------------------------------------------------
class VLPercepIBSubcuentaTotalesManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta):
		
		#-- Base de la consulta SQL.
		query = """
			SELECT 
				ROW_NUMBER() OVER (ORDER BY sub_cuenta) as id_factura,
				sub_cuenta,
				nombre_cliente_padre,
				ROUND(SUM(neto), 2) AS neto, 
				ROUND(SUM(percep_ib), 2) AS percep_ib,
				CURRENT_DATE as fecha_comprobante,	-- Fecha actual
			    0 AS id_cliente_id,
    			'' AS nombre_cliente
			FROM
				VLPercepIBSubcuentaTotales
			WHERE
				fecha_comprobante BETWEEN %s AND %s
			GROUP BY 
				sub_cuenta, nombre_cliente_padre
			ORDER by 
				sub_cuenta
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Ejecutar la consulta y devolver los resultados.
		return self.raw(query, params)


class VLPercepIBSubcuentaTotales(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	fecha_comprobante = models.DateField()
	sub_cuenta = models.IntegerField()
	nombre_cliente_padre = models.CharField(max_length=50)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	neto = models.DecimalField(max_digits=14, decimal_places=2)
	percep_ib = models.DecimalField(max_digits=14, decimal_places=2)
	
	objects = VLPercepIBSubcuentaTotalesManager()
	
	class Meta:
		managed = False
		db_table = 'vlpercepibsubcuentatotales'
		verbose_name = ('Percepciones por Sub Cuentas - Totales')
		verbose_name_plural = ('Percepciones por Sub Cuentas - Totales')
		ordering = ['sub_cuenta']


#-----------------------------------------------------------------------------
# Percepción IB por Sub Cuentas - Detallado.
#-----------------------------------------------------------------------------
class VLPercepIBSubcuentaDetalladoManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta):
		
		#-- Se crea la consulta.
		query = """
			SELECT
				*
			FROM
				VLPercepIBSubcuentaDetallado
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by sub_cuenta, fecha_comprobante, numero_comprobante"
		
		#-- Ejecutar la consulta y devolver los resultados.
		return self.raw(query, params)


class VLPercepIBSubcuentaDetallado(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	sub_cuenta = models.IntegerField()
	nombre_cliente_padre = models.CharField(max_length=50)
	compro = models.CharField(max_length=3)	
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	fecha_comprobante = models.DateField()
	comprobante = models.CharField(max_length=30)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	cuit = models.IntegerField()
	neto = models.DecimalField(max_digits=14, decimal_places=2)
	percep_ib = models.DecimalField(max_digits=14, decimal_places=2)
	
	objects = VLPercepIBSubcuentaDetalladoManager()
	
	class Meta:
		managed = False
		db_table = 'vlpercepibsubcuentadetallado'
		verbose_name = ('Percepciones por Sub Cuentas - Detallado')
		verbose_name_plural = ('Percepciones por Sub Cuentas - Detallado')
		ordering = ['sub_cuenta']


#-----------------------------------------------------------------------------
# Comisión a Vendedor Según Facturaras.
#-----------------------------------------------------------------------------
class ComisionVendedorIBManager(models.Manager):
	
	def obtener_datos(self, id_vendedor, fecha_desde, Fecha_hasta, orden='nombre'):
		
		#-- Mapeo seguro de opciones de orden.
		orden_map = {
			'nombre': 'nombre_vendedor',
			'codigo': 'id_vendedor_id'
		}
		order_by = orden_map.get(orden, 'id_vendedor_id')
		
		#-- Se crea la primera consulta (Recibos).
		query1 = """
			SELECT 
				*,
				ROUND(gravado*pje_comision/100, 2) AS monto_comision
			FROM 
				VLComisionVendedor
			WHERE 
				pje_comision <> 0
				AND fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se crea la segunda consulta (Detalle).
		query2 = """
			SELECT 
				*,
				ROUND(gravado*pje_comision/100, 2) AS monto_comision
			FROM 
				VLComisionVendedorDetalle
			WHERE 
				pje_comision <> 0
				AND fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, Fecha_hasta]
		
		#-- Filtros adicionales.
		if id_vendedor:
			query1 += " AND id_vendedor_id = %s"
			query2 += " AND id_vendedor_id = %s"
			params.append(id_vendedor)
		
		#-- Unir las consultas.
		query_full = f"{query1} UNION {query2} ORDER BY {order_by}, consulta, fecha_comprobante, comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query_full, params*2)


class VLComisionVendedor(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	compro = models.CharField(max_length=3)	
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	comprobante = models.CharField(max_length=19)
	fecha_comprobante = models.DateField()
	nombre_cliente = models.CharField(max_length=50)
	reventa = models.CharField(max_length=1)
	id_producto_id = models.IntegerField()
	medida = models.CharField(max_length=15)
	nombre_producto_marca = models.CharField(max_length=50)
	nombre_producto_familia = models.CharField(max_length=50)
	gravado = models.DecimalField(max_digits=14, decimal_places=2)
	pje_comision = models.DecimalField(max_digits=4, decimal_places=2)
	monto_comision = models.DecimalField(max_digits=14, decimal_places=2)
	id_vendedor_id = models.IntegerField()
	nombre_vendedor = models.CharField(max_length=30)
	
	objects = ComisionVendedorIBManager()
	
	class Meta:
		managed = False
		db_table = 'vlcomisionvendedor'
		verbose_name = ('Comisión Según Facturación')
		verbose_name_plural = ('Comisión Según Facturación')
		# ordering = ['nombre_vendedor','fecha_comprobante','numero_comprobante']
		ordering = ['id_vendedor_id','fecha_comprobante','numero_comprobante']


#-----------------------------------------------------------------------------
# Comisiones a Operarios.
#-----------------------------------------------------------------------------
class ComisionOperarioManager(models.Manager):
	
	def obtener_datos(self, id_operario, fecha_desde, fecha_hasta, orden='nombre'):
		
		#-- Mapeo seguro de opciones de orden.
		orden_map = {
			'nombre': 'nombre_operario',
			'codigo': 'id_operario_id'
		}
		order_by = orden_map.get(orden, 'id_operario_id')
		
		#-- Se crea la consulta.
		query = """
			SELECT 
				* 
			FROM 
				VLComisionOperario 
			WHERE 
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if id_operario:
			query += " AND id_operario_id = %s"
			params.append(id_operario)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += f" ORDER by {order_by}, fecha_comprobante, numero_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLComisionOperario(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	id_operario_id = models.IntegerField()
	nombre_operario = models.CharField(max_length=50)
	codigo_comprobante_venta = models.CharField(max_length=3)
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	comprobante = models.CharField(max_length=19)
	fecha_comprobante = models.DateField()
	id_producto_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	comision_operario = models.DecimalField(max_digits=5, decimal_places=2)
	monto_comision = models.DecimalField(max_digits=14, decimal_places=2)
	
	objects = ComisionOperarioManager()
	
	class Meta:
		managed = False
		db_table = 'vlcomisionoperario'
		verbose_name = ('Comisiones a Operarios')
		verbose_name_plural = ('Comisiones a Operarios')
		ordering = ['nombre_operario', 'fecha_comprobante', 'numero_comprobante']


#-----------------------------------------------------------------------------
# Deferencias de Precios en Facturación.
#-----------------------------------------------------------------------------
class PrecioDiferenteManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, id_vendedor_desde, id_vendedor_hasta, comprobantes, dif_mayor=0, orden='nombre'):
		
		#-- Mapeo seguro de opciones de orden.
		orden_map = {
			'nombre': 'nombre_vendedor',
			'codigo': 'id_vendedor_id'
		}
		order_by = orden_map.get(orden, 'id_vendedor_id')
		
		#-- Determinar cantidad de marcas de parámetros para los comprobantes.
		placeholders = ','.join(['%s'] * len(comprobantes))
		
		#-- Se crea la consulta.
		query = """
			SELECT 
				* 
			FROM 
				VLPrecioDiferente 
			WHERE 
				fecha_comprobante BETWEEN %s AND %s 
				AND id_vendedor_id BETWEEN %s AND %s 
				AND ABS(precio - precio_lista) > %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta, id_vendedor_desde, id_vendedor_hasta, dif_mayor]
		
		#-- Añadir filtro por comprobantes.
		query += f" AND compro IN ({placeholders})"
		params.extend(comprobantes)  # Extender con los elementos de la lista
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += f" ORDER by {order_by}, fecha_comprobante, numero_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLPrecioDiferente(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	id_vendedor_id = models.IntegerField()
	nombre_vendedor = models.CharField(max_length=30)
	codigo_comprobante_venta = models.CharField(max_length=3)
	letra_comprobante = models.CharField(max_length=1)
	fecha_comprobante = models.DateField()
	numero_comprobante = models.IntegerField()
	comprobante = models.CharField(max_length=19)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	precio_lista = models.DecimalField(max_digits=12, decimal_places=2)
	diferencia = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=6, decimal_places=2)
	adicional = models.DecimalField(max_digits=12, decimal_places=2)
	
	objects = PrecioDiferenteManager()
	
	class Meta:
		managed = False
		db_table = 'vlpreciodiferente'
		verbose_name = ('Diferencias de Precios en Facturación')
		verbose_name_plural = ('Diferencias de Precios en Facturación')
		ordering = ['nombre_vendedor', 'fecha_comprobante', 'numero_comprobante']


#-----------------------------------------------------------------------------
# Resumen de Ventas Ing. Brutos Mercadolibre.
#-----------------------------------------------------------------------------
class VentasResumenIBManager(models.Manager):
	
	def obtener_datos(self, anno, mes, id_sucursal=0):
		
		#-- Se crea la consulta.
		query = """
			SELECT
				*
			FROM 
				VLVentasResumenIB
			WHERE 
				EXTRACT(YEAR FROM fecha_comprobante) = %s
				AND EXTRACT(MONTH FROM fecha_comprobante) = %s
				AND suc_imp = %s
		"""
		
		#-- Se añaden parámetros.
		params = [str(anno), str(mes), id_sucursal]
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLVentasResumenIB(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	fecha_comprobante = models.DateField()
	gravado = models.DecimalField(max_digits=14, decimal_places=2)
	iva = models.DecimalField(max_digits=14, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	id_provincia_id = models.IntegerField()
	nombre_provincia = models.CharField(max_length=30)	
	suc_imp = models.IntegerField()
	
	objects = VentasResumenIBManager()
	
	class Meta:
		managed = False
		db_table = 'vlventasresumenib'
		verbose_name = ('Resumen de Ventas por Provincias')
		verbose_name_plural = ('Resumen de Ventas por Provincias')
		ordering = ['fecha_comprobante']


#-----------------------------------------------------------------------------
# Estadísticas de Ventas.
#-----------------------------------------------------------------------------
class EstadisticasVentasManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, id_marca_desde, id_marca_hasta, agrupar, mostrar, id_sucursal=None, id_cliente=None):
		
		select_columns = {
			"Producto": """
				id_producto_id,
				cai,
				nombre_producto,
				unidad,
				id_familia_id,
				nombre_producto_familia,
				id_modelo_id,
				nombre_modelo,
				id_marca_id,
				nombre_producto_marca
			""",
			"Familia": """
				id_familia_id,
				nombre_producto_familia,
				id_marca_id,
				nombre_producto_marca
			""",
			"Modelo": """
				id_modelo_id,
				nombre_modelo,
				id_marca_id,
				nombre_producto_marca
			""",
			"Marca": """
				id_marca_id,
				nombre_producto_marca
			"""
		}
		
		# query = """
		# 	SELECT 
		# 		ROW_NUMBER() OVER (ORDER BY nombre_producto_marca) AS id_factura,
		# 		id_producto_id,
		# 		cai,
		# 		nombre_producto,
		# 		unidad,
		# 		id_familia_id,
		# 		nombre_producto_familia,
		# 		id_modelo_id,
		# 		nombre_modelo,
		# 		id_marca_id,
		# 		nombre_producto_marca,
		# 		SUM(cantidad) AS cantidad,
		# 		SUM(total) AS total,
		# 		id_cliente_id
		# 	FROM 
		# 		VLEstadisticasVentas
		# 	WHERE 
		# 		fecha_comprobante BETWEEN %s AND %s
		# 		AND id_marca_id BETWEEN %s AND %s
		# """
		
        #-- Construir la consulta.
		query = f"""
			SELECT 
				ROW_NUMBER() OVER (ORDER BY nombre_producto_marca) AS id_factura,
				{select_columns[agrupar]},
				SUM(cantidad) AS cantidad,
				SUM(total) AS total
			FROM 
				VLEstadisticasVentas
			WHERE 
				fecha_comprobante BETWEEN %s AND %s
				AND id_marca_id BETWEEN %s AND %s
		"""
			
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta, id_marca_desde, id_marca_hasta]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		if id_cliente:
			query += " AND id_cliente_id = %s"
			params.append(id_cliente)
		
		# match agrupar:
		# 	case "Producto":
		# 		query += " GROUP BY id_producto_id"
		# 	case "Familia":
		# 		query += " GROUP BY id_familia_id, id_marca_id"
		# 	case "Modelo":
		# 		query += " GROUP BY id_modelo_id, id_marca_id"
		# 		# query += " GROUP BY id_modelo_id"
		# 	case "Marca":
		# 		query += " GROUP BY id_marca_id"
		
		#-- Agregar GROUP BY.
		query += f" GROUP BY {select_columns[agrupar]}"
		
		if mostrar:
			match mostrar:
				case "Cantidad":
					query += " ORDER BY cantidad DESC"
				case "Importe":
					query += " ORDER BY total DESC"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLEstadisticasVentas(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	id_producto_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	nombre_producto = models.CharField(max_length=50)
	nombre_producto_familia = models.CharField(max_length=50)
	nombre_modelo = models.CharField(max_length=50)
	nombre_producto_marca = models.CharField(max_length=50)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	fecha_comprobante = models.DateField()
	id_cliente_id = models.IntegerField()
	id_sucursal_id = models.IntegerField()
	
	objects = EstadisticasVentasManager()
	
	class Meta:
		managed = False
		db_table = 'vlestadisticasventas'
		verbose_name = ('Estadísticas de Ventas')
		verbose_name_plural = ('Estadísticas de Ventas')


#-----------------------------------------------------------------------------
# Estadísticas de Ventas por Vendedor.
#-----------------------------------------------------------------------------
class EstadisticasVentasVendedorManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, id_marca_desede, id_marca_hasta, agrupar, mostrar, id_sucursal=None, id_vendedor=None):
		
		select_columns = {
			"Producto": """
				id_producto_id,
				nombre_producto,
				id_familia_id,
				nombre_producto_familia,
				id_modelo_id,
				nombre_modelo,
				id_marca_id,
				nombre_producto_marca
			""",
			"Familia": """
				id_familia_id,
				nombre_producto_familia,
				id_marca_id,
				nombre_producto_marca
			""",
			"Modelo": """
				id_modelo_id,
				nombre_modelo,
				id_marca_id,
				nombre_producto_marca
			""",
			"Marca": """
				id_marca_id,
				nombre_producto_marca
			"""
		}
		
		# query = """
		# 	SELECT 
		# 		id_factura,
		# 		id_producto_id,
		# 		nombre_producto,
		# 		nombre_producto_familia,
		# 		nombre_modelo,
		# 		nombre_producto_marca,
		# 		SUM(cantidad) AS cantidad, 
		# 		SUM(total) AS total
		# 	FROM 
		# 		VLEstadisticasVentasVendedor
		# 	WHERE fecha_comprobante BETWEEN %s AND %s 
		# 		AND id_marca_id BETWEEN %s AND %s
		# """
		query = f"""
			SELECT 
				ROW_NUMBER() OVER (ORDER BY nombre_producto_marca) AS id_factura,
				{select_columns[agrupar]},
				SUM(cantidad) AS cantidad, 
				SUM(total) AS total
			FROM 
				VLEstadisticasVentasVendedor
			WHERE
				fecha_comprobante BETWEEN %s AND %s 
				AND id_marca_id BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta, id_marca_desede, id_marca_hasta]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		if id_vendedor:
			query += " AND id_vendedor_id = %s"
			params.append(id_vendedor)
		
		# match agrupar:
		# 	case "Producto":
		# 		query += " GROUP BY id_producto_id"
		# 	case "Familia":
		# 		query += " GROUP BY id_familia_id, id_marca_id"
		# 	case "Modelo":
		# 		query += " GROUP BY id_modelo_id, id_marca_id"
		# 	case "Marca":
		# 		query += " GROUP BY id_marca_id"
		
		#-- Agregar GROUP BY.
		query += f" GROUP BY {select_columns[agrupar]}"
		
		if mostrar:
			match mostrar:
				case "Cantidad":
					query += " ORDER BY cantidad DESC"
				case "Importe":
					query += " ORDER BY total DESC"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		print("Consulta SQL:", query)  # Debug: Imprimir la consulta SQL generada
		return self.raw(query, params)


class VLEstadisticasVentasVendedor(models.Model):
	id_factura = models.IntegerField(primary_key=True)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	nombre_producto_familia = models.CharField(max_length=50)
	nombre_modelo = models.CharField(max_length=50)
	nombre_producto_marca = models.CharField(max_length=50)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	fecha_comprobante = models.DateField()
	id_sucursal_id = models.IntegerField()
	id_vendedor_id = models.IntegerField()
	
	objects = EstadisticasVentasVendedorManager()
	
	class Meta:
		managed = False
		db_table = 'vlestadisticasventasvendedor'
		verbose_name = ('Estadísticas de Ventas por Vendedor')
		verbose_name_plural = ('Estadísticas de Ventas por Vendedor')


#-----------------------------------------------------------------------------
# Estadísticas de Ventas por Vendedor Clientes.
#-----------------------------------------------------------------------------
class EstadisticasVentasVendedorClienteManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, id_marca_desede, id_marca_hasta, agrupar, mostrar, estadisticas, id_sucursal=None, id_vendedor=None):
		
		#-- Convertir el parámetro estadisticas a booleano.
		estadisticas = estadisticas.lower() == 'true' if isinstance(estadisticas, str) else bool(estadisticas)
		
		select_columns = {
			"Producto": """
				id_sucursal_id,
				id_vendedor_id,
				nombre_vendedor,
				id_cliente_id,
				nombre_cliente,
				id_producto_id,
				nombre_producto,
				id_familia_id,
				nombre_producto_familia,
				id_modelo_id,
				nombre_modelo,
				id_marca_id,
				nombre_producto_marca
			""",
			"Familia": """
				id_sucursal_id,
				id_vendedor_id,
				nombre_vendedor,
				id_cliente_id,
				nombre_cliente,
				id_familia_id,
				nombre_producto_familia,
				id_marca_id,
				nombre_producto_marca
			""",
			"Modelo": """
				id_sucursal_id,
				id_vendedor_id,
				nombre_vendedor,
				id_cliente_id,
				nombre_cliente,
				id_modelo_id,
				nombre_modelo,
				id_marca_id,
				nombre_producto_marca
			""",
			"Marca": """
				id_sucursal_id,
				id_vendedor_id,
				nombre_vendedor,
				id_cliente_id,
				nombre_cliente,
				id_marca_id,
				nombre_producto_marca
			"""
		}
		
		# query = """
		# 	SELECT 
		# 		ROW_NUMBER() OVER() AS id,
		# 		id_producto_id,
		# 		nombre_producto,
		# 		nombre_producto_familia,
		# 		nombre_modelo,
		# 		nombre_producto_marca,
		# 		id_vendedor_id,
		# 		nombre_vendedor,
		# 		id_cliente_id,
		# 		nombre_cliente,
		# 		SUM(cantidad) AS cantidad, 
		# 		SUM(total) AS total
		# 	FROM 
		# 		VLEstadisticasVentasVendedorCliente
		# 	WHERE 
		# 		no_estadist = %s
		# 	 	AND fecha_comprobante BETWEEN %s AND %s
		# 		AND id_marca_id BETWEEN %s AND %s
		# """
		query = f"""
			SELECT 
				ROW_NUMBER() OVER() AS id,
				{select_columns[agrupar]},
				SUM(cantidad) AS cantidad,
				SUM(total) AS total
			FROM 
				VLEstadisticasVentasVendedorCliente
			WHERE 
				no_estadist = %s
			 	AND fecha_comprobante BETWEEN %s AND %s
				AND id_marca_id BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [estadisticas, fecha_desde, fecha_hasta, id_marca_desede, id_marca_hasta]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		if id_vendedor:
			query += " AND id_vendedor_id = %s"
			params.append(id_vendedor)
		
		# match agrupar:
		# 	case "Producto":
		# 		query += " GROUP BY id_sucursal_id, id_vendedor_id, id_cliente_id, id_producto_id"
		# 	case "Familia":
		# 		query += " GROUP BY id_sucursal_id, id_vendedor_id, id_cliente_id, id_familia_id, id_marca_id"
		# 	case "Modelo":
		# 		query += " GROUP BY id_sucursal_id, id_vendedor_id, id_cliente_id, id_modelo_id, id_marca_id"
		# 	case "Marca":
		# 		query += " GROUP BY id_sucursal_id, id_vendedor_id, id_cliente_id, id_marca_id"
		
		#-- Agregar GROUP BY.
		query += f" GROUP BY {select_columns[agrupar]}"
		
		query += " ORDER BY id_sucursal_id DESC, id_vendedor_id DESC, id_cliente_id DESC"
		
		if mostrar:
			match mostrar:
				case "Cantidad":
					query += ", cantidad DESC"
				case "Importe":
					query += ", total DESC"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		print("Consulta SQL:", query)  # Debug: Imprimir la consulta SQL generada
		return self.raw(query, params)


class VLEstadisticasVentasVendedorCliente(models.Model):
	id = models.AutoField(primary_key=True)
	id_vendedor_id = models.IntegerField()
	nombre_vendedor = models.CharField(max_length=30)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	nombre_producto_familia = models.CharField(max_length=50)
	nombre_modelo = models.CharField(max_length=50)
	nombre_producto_marca = models.CharField(max_length=50)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	fecha_comprobante = models.DateField()
	id_sucursal_id = models.IntegerField()
	no_estadist = models.BooleanField()
	
	objects = EstadisticasVentasVendedorClienteManager()
	
	class Meta:
		managed = False
		db_table = 'vlestadisticasventasvendedorcliente'
		verbose_name = ('Estadísticas de Ventas Vendedor Clientes')
		verbose_name_plural = ('Estadísticas de Ventas Vendedor Clientes')


#-----------------------------------------------------------------------------
# Ventas de Productos según Condición.
#-----------------------------------------------------------------------------
class EstadisticasSegunCondicionManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, id_marca_desede, id_marca_hasta, agrupar, id_sucursal=None):
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				nombre_producto_familia,
				nombre_producto_marca,
				nombre_modelo,
				id_producto_id,
				nombre_producto,
				SUM(CASE WHEN reventa = 'M' THEN cantidad ELSE 0 END) AS cantidad_m,
				SUM(CASE WHEN reventa = 'M' THEN importe ELSE 0 END) AS importe_m,
				SUM(CASE WHEN reventa = 'M' THEN costo ELSE 0 END) AS costo_m,
				SUM(CASE WHEN reventa = 'M' THEN (importe - costo) ELSE 0 END) AS ganancia_m,
				SUM(CASE WHEN reventa = 'R' THEN cantidad ELSE 0 END) AS cantidad_r,
				SUM(CASE WHEN reventa = 'R' THEN importe ELSE 0 END) AS importe_r,
				SUM(CASE WHEN reventa = 'R' THEN costo ELSE 0 END) AS costo_r,
				SUM(CASE WHEN reventa = 'R' THEN (importe - costo) ELSE 0 END) AS ganancia_r,
				SUM(CASE WHEN reventa = 'E' THEN cantidad ELSE 0 END) AS cantidad_e,
				SUM(CASE WHEN reventa = 'E' THEN importe ELSE 0 END) AS importe_e,
				SUM(CASE WHEN reventa = 'E' THEN costo ELSE 0 END) AS costo_e,
				SUM(CASE WHEN reventa = 'E' THEN (importe - costo) ELSE 0 END) AS ganancia_e
			FROM
				VLEstadisticasSegunCondicion
			WHERE
				fecha_comprobante BETWEEN %s AND %s
				AND id_marca_id BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta, id_marca_desede, id_marca_hasta]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		match agrupar:
			case "Producto":
				query += " GROUP BY id_familia_id, id_modelo_id, id_producto_id"
			case "Familia":
				query += " GROUP BY id_familia_id, id_marca_id"
			case "Modelo":
				query += " GROUP BY id_marca_id, id_modelo_id"
			case "Marca":
				query += " GROUP BY id_marca_id"
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by id_familia_id, id_marca_id, id_modelo_id, id_producto_id"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLEstadisticasSegunCondicion(models.Model):
	id = models.IntegerField(primary_key=True)
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	id_modelo_id = models.IntegerField()
	nombre_modelo = models.CharField(max_length=50)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	reventa = models.CharField(max_length=1)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	importe = models.DecimalField(max_digits=14, decimal_places=2)
	costo = models.DecimalField(max_digits=14, decimal_places=2)
	fecha_comprobante = models.DateField()
	id_sucursal_id = models.IntegerField()
	
	objects = EstadisticasSegunCondicionManager()
	
	class Meta:
		managed = False
		db_table = 'vlestadisticaseguncondicion'
		verbose_name = ('Ventas Según Condición')
		verbose_name_plural = ('Ventas Según Condición')


#-----------------------------------------------------------------------------
# Estadísticas de Ventas por Marcas.
#-----------------------------------------------------------------------------
class EstadisticasVentasMarcaManager(models.Manager):
	
	def obtener_datos(self, id_marca, fecha_desde, fecha_hasta, id_sucursal=None):
		
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLEstadisticasVentasMarca
			WHERE
				id_marca_id = %s
			 	AND fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [id_marca, fecha_desde, fecha_hasta ]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by id_marca_id, id_familia_id, id_modelo_id, id_producto_id"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLEstadisticasVentasMarca(models.Model):
	id = models.IntegerField(primary_key=True)
	comprobante = models.CharField(max_length=19)
	fecha_comprobante = models.DateField()
	id_cliente_id = models.IntegerField()
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	medida = models.CharField(max_length=15)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=6, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	compra = models.DecimalField(max_digits=14, decimal_places=2)
	id_sucursal_id = models.IntegerField()
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_modelo_id = models.IntegerField()
	nombre_modelo = models.CharField(max_length=50)
	
	objects = EstadisticasVentasMarcaManager()
	
	class Meta:
		managed = False
		db_table = 'vlestadisticasventasmarca'
		verbose_name = ('Estadísticas de Ventas por Marca y Artículo')
		verbose_name_plural = ('Estadísticas de Ventas por Marca y Artículo')


#-----------------------------------------------------------------------------
# Estadísticas de Ventas por Marcas-Vendedor.
#-----------------------------------------------------------------------------
class EstadisticasVentasMarcaVendedorManager(models.Manager):
	
	def obtener_datos(self, id_marca, id_vendedor, fecha_desde, fecha_hasta, id_sucursal=None):
		
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLEstadisticasVentasMarcaVendedor
			WHERE
				id_marca_id = %s
				AND id_vendedor_id = %s
			 	AND fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [id_marca, id_vendedor, fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by id_marca_id, id_familia_id, id_modelo_id, id_producto_id"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLEstadisticasVentasMarcaVendedor(models.Model):
	id = models.IntegerField(primary_key=True)
	comprobante = models.CharField(max_length=19)
	fecha_comprobante = models.DateField()
	id_cliente_id = models.IntegerField()
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	medida = models.CharField(max_length=15)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=6, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	# comision = models.DecimalField(max_digits=14, decimal_places=2)
	id_sucursal_id = models.IntegerField()
	id_vendedor_id = models.IntegerField()
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_modelo_id = models.IntegerField()
	nombre_modelo = models.CharField(max_length=50)
	
	objects = EstadisticasVentasMarcaVendedorManager()
	
	class Meta:
		managed = False
		db_table = 'vlestadisticasventasmarcavendedor'
		verbose_name = ('Estadísticas de Ventas por Marca y Familia por Vendedor')
		verbose_name_plural = ('Estadísticas de Ventas por Marca y Familia por Vendedor')


#-----------------------------------------------------------------------------
# Estadísticas de Clientes sin Movimiento.
#-----------------------------------------------------------------------------
class ClienteUltimaVentaManager(models.Manager):
	
	def obtener_datos(self, id_vendedor, fecha_consulta, orden="Alf"):
		
		query = """
			SELECT
				*
			FROM
				VLClienteUltimaVenta
			WHERE
				id_vendedor_id = %s
			 	AND fecha_ultimo_comprobante < %s
		"""
		
		#-- Se añaden parámetros.
		params = [id_vendedor, fecha_consulta]
		
		#-- Ordenar resultados.
		if orden == "Alf":
			query += " ORDER BY nombre_cliente"
		elif orden == "Asc":
			query += " ORDER BY fecha_ultimo_comprobante ASC"
		else:
			query += " ORDER BY fecha_ultimo_comprobante DESC"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLClienteUltimaVenta(models.Model):
	id_cliente_id = models.IntegerField(primary_key=True)
	nombre_cliente = models.CharField(max_length=50)
	fecha_ultimo_comprobante = models.DateField()
	id_vendedor_id = models.IntegerField()	
	
	objects = ClienteUltimaVentaManager()
	
	class Meta:
		managed = False
		db_table = 'vlclienteultimaventa'
		verbose_name = ('Estadísticas de Clientes sin Ventas')
		verbose_name_plural = ('Estadísticas de Clientes sin Ventas')


#-----------------------------------------------------------------------------
# Estadísticas de Ventas por Provincia.
#-----------------------------------------------------------------------------
class EstadisticasVentasProvinciaManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, id_marca_desede, id_marca_hasta, agrupar, mostrar, id_vendedor, id_sucursal=None, id_provincia=None):
		
		query = """
			SELECT 
				ROW_NUMBER() OVER() AS id,
				id_provincia,
				nombre_provincia,
				id_producto_id,
				nombre_producto,
				nombre_producto_familia,
				nombre_modelo,
				nombre_producto_marca,
				SUM(cantidad) AS cantidad, 
				SUM(total) AS total
			FROM 
				VLEstadisticasVentasProvincia
			WHERE 
				fecha_comprobante BETWEEN %s AND %s
				AND id_marca_id BETWEEN %s AND %s
				AND id_vendedor_id = %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta, id_marca_desede, id_marca_hasta, id_vendedor]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		if id_provincia:
			query += " AND id_provincia = %s"
			params.append(id_provincia)
		
		query += " GROUP BY id_sucursal_id, id_vendedor_id, id_provincia"
		match agrupar:
			case "Producto":
				# query += " GROUP BY id_producto_id"
				query += ", id_producto_id"
			case "Familia":
				# query += " GROUP BY id_familia_id, id_marca_id"
				query += ", id_familia_id, id_marca_id"
			case "Modelo":
				# query += " GROUP BY id_modelo_id, id_marca_id"
				# query += " GROUP BY id_modelo_id"
				query += ", id_modelo_id"
			case "Marca":
				# query += " GROUP BY id_marca_id"
				query += ", id_marca_id"
		
		query += " ORDER BY nombre_provincia"
		
		if mostrar:
			match mostrar:
				case "Cantidad":
					query += ", cantidad DESC"
				case "Importe":
					query += ", total DESC"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLEstadisticasVentasProvincia(models.Model):
	id = models.AutoField(primary_key=True)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	nombre_producto_familia = models.CharField(max_length=50)
	nombre_modelo = models.CharField(max_length=50)
	nombre_producto_marca = models.CharField(max_length=50)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	fecha_comprobante = models.DateField()
	id_sucursal_id = models.IntegerField()
	id_vendedor_id = models.IntegerField()
	id_provincia = models.IntegerField()
	nombre_provincia = models.CharField(max_length=30)
	
	objects = EstadisticasVentasProvinciaManager()
	
	class Meta:
		managed = False
		db_table = 'vlestadisticasventasprovincia'
		verbose_name = ('Estadísticas de Ventas por Provincia')
		verbose_name_plural = ('Estadísticas de Ventas por Provincia')


#-----------------------------------------------------------------------------
# Comprobantes sin Estadísticas.
#-----------------------------------------------------------------------------
class VLVentaSinEstadisticaManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, id_sucursal=None, orden="nombre"):
		
		#-- Mapeo seguro de opciones de orden.
		orden_map = {
			'nombre': 'nombre_cliente',
			'codigo': 'id_cliente_id'
		}
		order_by = orden_map.get(orden, 'id_cliente_id')
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLVentaSinEstadistica
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if id_sucursal:
			query += " AND id_sucursal_id = %s"
			params.append(id_sucursal)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += f" ORDER by {order_by}, fecha_comprobante, comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLVentaSinEstadistica(models.Model):
	id = models.AutoField(primary_key=True)
	fecha_comprobante = models.DateField()
	comprobante = models.CharField(max_length=19)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	id_vendedor_id = models.IntegerField()
	nombre_vendedor = models.CharField(max_length=30)
	sub_cuenta = models.IntegerField()
	id_sucursal_id = models.IntegerField()
	nombre_sucursal = models.CharField(max_length=50)
	
	objects = VLVentaSinEstadisticaManager()
	
	class Meta:
		managed = False
		db_table = 'vlventasinestadistica'
		verbose_name = ('Comprobantes sin Estadísticas')
		verbose_name_plural = ('Comprobantes sin Estadísticas')


#-----------------------------------------------------------------------------
# Tablas Dinámicas de Ventas - Ventas por Comprobantes.
#-----------------------------------------------------------------------------
class VLTablaDinamicaVentasManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, comprobantes_impositivos=True):
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLTablaDinamicaVentas
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if comprobantes_impositivos:
			query += " AND libro_iva = %s"
			params.append(comprobantes_impositivos)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by fecha_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLTablaDinamicaVentas(models.Model):
	id = models.IntegerField(primary_key=True)
	nombre_sucursal = models.CharField(max_length=50)
	nombre_comprobante_venta = models.CharField(max_length=50)
	fecha_comprobante = models.DateField()
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	condicion_comprobante = models.IntegerField()
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	mayorista = models.BooleanField()
	gravado = models.DecimalField(max_digits=14, decimal_places=2)
	exento = models.DecimalField(max_digits=14, decimal_places=2)
	iva = models.DecimalField(max_digits=12, decimal_places=2)
	percepcion = models.DecimalField(max_digits=14, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	no_estadist = models.BooleanField()
	id_user_id = models.IntegerField()
	codigo_postal = models.CharField(max_length=5)
	nombre_localidad = models.CharField(max_length=30)
	nombre_provincia = models.CharField(max_length=30)
	nombre_vendedor = models.CharField(max_length=30)
	comision = models.CharField(max_length=1)
	promo = models.BooleanField()
	libro_iva = models.BooleanField()
	nombre_marketing_origen = models.CharField(max_length=30)
	
	objects = VLTablaDinamicaVentasManager()
	
	class Meta:
		managed = False
		db_table = 'vltabladinamicaventas'
		verbose_name = ('Tablas Dinámicas de Ventas - Ventas por Comprobantes')
		verbose_name_plural = ('Tablas Dinámicas de Ventas - Ventas por Comprobantes')


#-----------------------------------------------------------------------------
# Tablas Dinámicas de Ventas - Detalle de Ventas por Productos.
#-----------------------------------------------------------------------------
class VLTablaDinamicaDetalleVentasManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, comprobantes_impositivos=True):
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLTablaDinamicaDetalleVentas
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if comprobantes_impositivos:
			query += " AND libro_iva = %s"
			params.append(comprobantes_impositivos)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by fecha_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLTablaDinamicaDetalleVentas(models.Model):
	id = models.IntegerField(primary_key=True)
	id_factura_id = models.IntegerField()
	nombre_sucursal = models.CharField(max_length=50)
	nombre_comprobante_venta = models.CharField(max_length=50)
	fecha_comprobante = models.DateField()
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	condicion_comprobante = models.IntegerField()
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	mayorista = models.BooleanField()
	reventa = models.CharField(max_length=1)
	id_producto_id = models.IntegerField()
	cai = models.CharField(max_length=20)	
	nombre_producto = models.CharField(max_length=50)
	nombre_producto_marca = models.CharField(max_length=50)
	nombre_producto_familia = models.CharField(max_length=50)
	segmento = models.CharField(max_length=3)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	costo = models.DecimalField(max_digits=12, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=6, decimal_places=2)
	gravado = models.DecimalField(max_digits=14, decimal_places=2)
	no_gravado = models.DecimalField(max_digits=14, decimal_places=2)
	iva = models.DecimalField(max_digits=12, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	no_estadist = models.BooleanField()
	id_user_id = models.IntegerField()
	codigo_postal = models.CharField(max_length=5)
	nombre_localidad = models.CharField(max_length=30)
	nombre_provincia = models.CharField(max_length=30)
	nombre_vendedor = models.CharField(max_length=30)
	comision = models.CharField(max_length=1)
	id_operario_id = models.IntegerField()
	nombre_operario = models.CharField(max_length=50)
	promo = models.BooleanField()
	libro_iva = models.BooleanField()
	nombre_marketing_origen = models.CharField(max_length=30)
	
	objects = VLTablaDinamicaDetalleVentasManager()
	
	class Meta:
		managed = False
		db_table = 'vltabladinamicadetalleventas'
		verbose_name = ('Tablas Dinámicas de Ventas - Detalle de Ventas por Productos')
		verbose_name_plural = ('Tablas Dinámicas de Ventas - Detalle de Ventas por Productos')


#-----------------------------------------------------------------------------
# Tablas Dinámicas de Ventas - Tablas para Estadísticas.
#-----------------------------------------------------------------------------
class VLTablaDinamicaEstadisticaManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, comprobantes_impositivos):
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLTablaDinamicaEstadistica
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if comprobantes_impositivos:
			query += " AND libro_iva = %s"
			params.append(comprobantes_impositivos)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER by fecha_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLTablaDinamicaEstadistica(models.Model):
	id = models.IntegerField(primary_key=True)
	id_factura_id = models.IntegerField()
	nombre_sucursal = models.CharField(max_length=50)
	nombre_comprobante_venta = models.CharField(max_length=50)
	fecha_comprobante = models.DateField()
	letra_comprobante = models.CharField(max_length=1)
	numero_comprobante = models.IntegerField()
	condicion_comprobante = models.IntegerField()
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	mayorista = models.BooleanField()
	reventa = models.CharField(max_length=1)
	id_producto_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	nombre_producto = models.CharField(max_length=50)
	nombre_producto_marca = models.CharField(max_length=50)
	nombre_producto_familia = models.CharField(max_length=50)
	segmento = models.CharField(max_length=3)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	costo = models.DecimalField(max_digits=12, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=6, decimal_places=2)
	gravado = models.DecimalField(max_digits=14, decimal_places=2)
	no_gravado = models.DecimalField(max_digits=14, decimal_places=2)
	total = models.DecimalField(max_digits=14, decimal_places=2)
	no_estadist = models.BooleanField()
	id_user_id = models.IntegerField()
	codigo_postal = models.CharField(max_length=5)
	nombre_localidad = models.CharField(max_length=30)
	nombre_provincia = models.CharField(max_length=30)
	nombre_vendedor = models.CharField(max_length=30)
	comision = models.CharField(max_length=1)
	id_operario_id = models.IntegerField()
	nombre_operario = models.CharField(max_length=50)
	promo = models.BooleanField()
	nombre_marketing_origen = models.CharField(max_length=30)
	
	objects = VLTablaDinamicaEstadisticaManager()
	
	class Meta:
		managed = False
		db_table = 'vltabladinamicaestadistica'
		verbose_name = ('Tablas Dinámicas de Ventas - Tablas para Estadísticas')
		verbose_name_plural = ('Tablas Dinámicas de Ventas - Tablas para Estadísticas')


#-----------------------------------------------------------------------------
# Lista de Precio.
#-----------------------------------------------------------------------------
class VLListaManager(models.Manager):
	
	def obtener_datos(self, id_familia_desde, id_familia_hasta, id_marca_desde, id_marca_hasta, id_modelo_desde, id_modelo_hasta):
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLLista
		"""
		
		#-- Filtros y parámetros.
		conditions = []
		params = []
		
		if id_familia_desde and id_familia_hasta:
			conditions.append("id_familia_id BETWEEN %s AND %s")
			params.extend([id_familia_desde, id_familia_hasta])
		elif id_familia_desde:
			conditions.append("id_familia_id >= %s")
			params.extend([id_familia_desde])
		elif id_familia_hasta:
			conditions.append("id_familia_id <= %s")
			params.extend([id_familia_hasta])
		
		if id_marca_desde and id_marca_hasta:
			conditions.append("id_marca_id BETWEEN %s AND %s")
			params.extend([id_marca_desde, id_marca_hasta])
		elif id_marca_desde:
			conditions.append("id_marca_id >= %s")
			params.extend([id_marca_desde])
		elif id_marca_hasta:
			conditions.append("id_marca_id <= %s")
			params.extend([id_marca_hasta])
		
		if id_modelo_desde and id_modelo_hasta:
			conditions.append("id_modelo_id BETWEEN %s AND %s")
			params.extend([id_modelo_desde, id_modelo_hasta])
		elif id_modelo_desde:
			conditions.append("id_modelo_id >= %s")
			params.extend([id_modelo_desde])
		elif id_modelo_hasta:
			conditions.append("id_modelo_id <= %s")
			params.extend([id_modelo_hasta])
		
		if conditions:
			query += " WHERE "
			query += " AND ".join(conditions)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER BY id_familia_id, id_marca_id"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLLista(models.Model):
	id_producto_id = models.IntegerField()
	id_cai_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	tipo_producto = models.CharField(max_length=1)
	medida = models.CharField(max_length=15)
	segmento = models.CharField(max_length=3)
	unidad = models.IntegerField()
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_modelo_id = models.IntegerField()
	nombre_modelo = models.CharField(max_length=50)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	nombre_producto = models.CharField(max_length=50)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	costo = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=6, decimal_places=2)
	id_alicuota_iva_id = models.IntegerField()
	alicuota_iva = models.DecimalField(max_digits=6, decimal_places=2)
	minimo = models.IntegerField()
	despacho_1 = models.CharField(max_length=16)
	despacho_2 = models.CharField(max_length=16)
	fecha_fabricacion = models.CharField(max_length=6)
	id_producto_estado = models.IntegerField()
	nombre_producto_estado = models.CharField(max_length=15)
	
	objects = VLListaManager()
	
	class Meta:
		managed = False
		db_table = 'vllista'
		verbose_name = ('Lista de Precios')
		verbose_name_plural = ('Lista de Precios')


#-----------------------------------------------------------------------------
# Lista de Precio a Revendedor.
#-----------------------------------------------------------------------------
class VLListaRevendedorManager(models.Manager):
	
	def obtener_datos(self, id_familia_desde, id_familia_hasta, id_marca_desde, id_marca_hasta, id_modelo_desde, id_modelo_hasta):
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLListaRevendedor
		"""
		
		#-- Filtros y parámetros.
		conditions = []
		params = []
		
		if id_familia_desde and id_familia_hasta:
			conditions.append("id_familia_id BETWEEN %s AND %s")
			params.extend([id_familia_desde, id_familia_hasta])
		elif id_familia_desde:
			conditions.append("id_familia_id >= %s")
			params.extend([id_familia_desde])
		elif id_familia_hasta:
			conditions.append("id_familia_id <= %s")
			params.extend([id_familia_hasta])
		
		if id_marca_desde and id_marca_hasta:
			conditions.append("id_marca_id BETWEEN %s AND %s")
			params.extend([id_marca_desde, id_marca_hasta])
		elif id_marca_desde:
			conditions.append("id_marca_id >= %s")
			params.extend([id_marca_desde])
		elif id_marca_hasta:
			conditions.append("id_marca_id <= %s")
			params.extend([id_marca_hasta])
		
		if id_modelo_desde and id_modelo_hasta:
			conditions.append("id_modelo_id BETWEEN %s AND %s")
			params.extend([id_modelo_desde, id_modelo_hasta])
		elif id_modelo_desde:
			conditions.append("id_modelo_id >= %s")
			params.extend([id_modelo_desde])
		elif id_modelo_hasta:
			conditions.append("id_modelo_id <= %s")
			params.extend([id_modelo_hasta])
		
		if conditions:
			query += " WHERE "
			query += " AND ".join(conditions)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER BY id_familia_id, id_producto"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLListaRevendedor(models.Model):
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_producto_id = models.IntegerField()
	id_cai_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	medida = models.CharField(max_length=15)
	nombre_producto = models.CharField(max_length=50)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	id_marca_id = models.IntegerField()
	id_modelo_id = models.IntegerField()
	
	objects = VLListaRevendedorManager()
	
	class Meta:
		managed = False
		db_table = 'vllistarevendedor'
		verbose_name = ('Lista de Precios a Revendedor')
		verbose_name_plural = ('Lista de Precios a Revendedor')


#-----------------------------------------------------------------------------
# Listado de Stock por Sucursal.
#-----------------------------------------------------------------------------
class VLStockSucursalManager(models.Manager):
	
	def obtener_datos(self, id_deposito, id_familia_desde, id_familia_hasta, id_marca_desde, id_marca_hasta, id_modelo_desde, id_modelo_hasta):
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLStockSucursal
			WHERE
				id_deposito_id = %s
		"""
		
		#-- Filtros y parámetros.
		conditions = []
		params = [id_deposito]
		
		if id_familia_desde and id_familia_hasta:
			conditions.append("id_familia_id BETWEEN %s AND %s")
			params.extend([id_familia_desde, id_familia_hasta])
		elif id_familia_desde:
			conditions.append("id_familia_id >= %s")
			params.extend([id_familia_desde])
		elif id_familia_hasta:
			conditions.append("id_familia_id <= %s")
			params.extend([id_familia_hasta])
		
		if id_marca_desde and id_marca_hasta:
			conditions.append("id_marca_id BETWEEN %s AND %s")
			params.extend([id_marca_desde, id_marca_hasta])
		elif id_marca_desde:
			conditions.append("id_marca_id >= %s")
			params.extend([id_marca_desde])
		elif id_marca_hasta:
			conditions.append("id_marca_id <= %s")
			params.extend([id_marca_hasta])
		
		if id_modelo_desde and id_modelo_hasta:
			conditions.append("id_modelo_id BETWEEN %s AND %s")
			params.extend([id_modelo_desde, id_modelo_hasta])
		elif id_modelo_desde:
			conditions.append("id_modelo_id >= %s")
			params.extend([id_modelo_desde])
		elif id_modelo_hasta:
			conditions.append("id_modelo_id <= %s")
			params.extend([id_modelo_hasta])
		
		if conditions:
			query += " AND "
			query += " AND ".join(conditions)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER BY id_familia_id, id_modelo_id, id_marca_id"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLStockSucursal(models.Model):
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_modelo_id = models.IntegerField()
	nombre_modelo = models.CharField(max_length=50)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	id_producto_id = models.IntegerField()
	id_cai_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	medida = models.CharField(max_length=15)
	nombre_producto = models.CharField(max_length=50)
	stock = models.IntegerField()
	costo_inventario = models.DecimalField(max_digits=12, decimal_places=2)
	id_deposito_id = models.IntegerField()
	
	objects = VLStockSucursalManager()
	
	class Meta:
		managed = False
		db_table = 'vlstocksucursal'
		verbose_name = ('Listado de Stock por Sucursal')
		verbose_name_plural = ('Listado de Stock por Sucursal')


#-----------------------------------------------------------------------------
# Stock General por Sucursal.
#-----------------------------------------------------------------------------
class VLStockGeneralSucursalManager(models.Manager):
	
	def obtener_datos(self, id_familia_desde, id_familia_hasta, id_marca_desde, id_marca_hasta, id_modelo_desde, id_modelo_hasta, sucursales_seleccionadas):
		from django.db import connection
		from collections import namedtuple
		
		#-- Construcción de la consulta base.
		query = """
			SELECT
				p.id_familia_id,
				pf.nombre_producto_familia,
				p.id_modelo_id,
				pm.nombre_modelo,
				p.id_marca_id,
				SUBSTR(px.nombre_producto_marca, 1, 90) AS nombre_producto_marca,
				ps.id_producto_id,
				p.id_cai_id,
				pc.cai,
				p.medida,
				SUBSTR(p.nombre_producto, 1, 200) AS nombre_producto,
				{sucursal_columns},
				{otras_sucursales},
				{total_general}
			FROM 
				producto_stock ps
				JOIN producto p ON ps.id_producto_id = p.id_producto
				JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
				JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
				JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
				JOIN producto_marca px ON p.id_marca_id = px.id_producto_marca
				JOIN producto_deposito pd ON ps.id_deposito_id = pd.id_producto_deposito
				JOIN sucursal s ON pd.id_sucursal_id = s.id_sucursal
			WHERE
				p.tipo_producto = 'P' {filters}
			GROUP BY
				p.id_familia_id, pf.nombre_producto_familia,
				p.id_modelo_id, pm.nombre_modelo,
				p.id_marca_id, px.nombre_producto_marca,
				ps.id_producto_id, p.id_cai_id, pc.cai, p.medida, p.nombre_producto
			HAVING
				SUM(ps.stock) <> 0
		"""
		
		#-- Parámetros para la consulta.
		params = []
		sucursal_columns = []
		
		#-- IDs de sucursales seleccionadas para usar en los filtros.
		sucursales_ids = [s.id_sucursal for s in sucursales_seleccionadas] if sucursales_seleccionadas else []
		
		#-- Columnas dinámicas para sucursales seleccionadas.
		if sucursales_seleccionadas:
			for sucursal in sucursales_seleccionadas:
				sucursal_columns.append(
					f'SUM(CASE WHEN s.id_sucursal = %s THEN ps.stock ELSE 0 END) AS stock_suc_{sucursal.id_sucursal}'
				)
				params.append(sucursal.id_sucursal)
			
			#-- Columna para stock en sucursales NO seleccionadas.
			otras_sucursales = """
				SUM(CASE WHEN s.id_sucursal NOT IN ({}) THEN ps.stock ELSE 0 END) AS otras_suc
			""".format(','.join(['%s']*len(sucursales_ids)))
			params.extend(sucursales_ids)
			
			#-- Columna para el stock total.
			total_general = "SUM(ps.stock) AS stock_total"
		else:
			sucursal_columns.append("0 AS stock")
			otras_sucursales = "0 AS otras_suc"
			total_general = "0 AS stock_total"
		
		#-- 2. Construcción de filtros.
		conditions = []
		
		#-- Filtros por rango.
		range_filters = [
			('p.id_familia_id', id_familia_desde, id_familia_hasta),
			('p.id_marca_id', id_marca_desde, id_marca_hasta),
			('p.id_modelo_id', id_modelo_desde, id_modelo_hasta)
		]
		
		for field, desde, hasta in range_filters:
			if desde and hasta:
				conditions.append(f"{field} BETWEEN %s AND %s")
				params.extend([desde, hasta])
			elif desde:
				conditions.append(f"{field} >= %s")
				params.append(desde)
			elif hasta:
				conditions.append(f"{field} <= %s")
				params.append(hasta)
		
		filters = "AND " + " AND ".join(conditions) if conditions else ""
		
		#-- 4. Ensamblar consulta final.
		final_query = query.format(
			sucursal_columns=", ".join(sucursal_columns),
			otras_sucursales=otras_sucursales,
			total_general=total_general,
			filters=filters
		)
		
		#-- 5. Ejecutar con cursor y mapear a objetos del modelo.
		with connection.cursor() as cursor:
			cursor.execute(final_query, params)
			columns = [col[0] for col in cursor.description]
			rows = cursor.fetchall()
		
		#-- Crear objetos modelo simulados.
		ModelProxy = namedtuple('ModelProxy', columns)
		return [ModelProxy(*row) for row in rows]
	
	def obtener_datos_tabulares(self, id_familia_desde, id_familia_hasta, id_marca_desde, id_marca_hasta, id_modelo_desde, id_modelo_hasta, sucursales):
		from django.db import connection
		from collections import namedtuple
		
		#-- Construcción de la consulta base.
		query = """
			SELECT
				p.id_familia_id,
				pf.nombre_producto_familia,
				p.id_modelo_id,
				pm.nombre_modelo,
				p.id_marca_id,
				SUBSTR(px.nombre_producto_marca, 1, 90) AS nombre_producto_marca,
				ps.id_producto_id,
				p.id_cai_id,
				pc.cai,
				p.medida,
				SUBSTR(p.nombre_producto, 1, 200) AS nombre_producto,
				{sucursal_columns},
				{total_general}
			FROM 
				producto_stock ps
				JOIN producto p ON ps.id_producto_id = p.id_producto
				JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
				JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
				JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
				JOIN producto_marca px ON p.id_marca_id = px.id_producto_marca
				JOIN producto_deposito pd ON ps.id_deposito_id = pd.id_producto_deposito
				JOIN sucursal s ON pd.id_sucursal_id = s.id_sucursal
			WHERE
				p.tipo_producto = 'P'
				{filters}
			GROUP BY
				p.id_familia_id, pf.nombre_producto_familia,
				p.id_modelo_id, pm.nombre_modelo,
				p.id_marca_id, px.nombre_producto_marca,
				ps.id_producto_id, p.id_cai_id, pc.cai, p.medida, p.nombre_producto
			HAVING
				SUM(ps.stock) <> 0
		"""
		
		#-- Parámetros para la consulta.
		params = []
		sucursal_columns = []
		
		#-- Columnas de stock por cada sucursal.
		for sucursal in sucursales:
			sucursal_columns.append(
				f'SUM(CASE WHEN s.id_sucursal = %s THEN ps.stock ELSE 0 END) AS stock_suc_{sucursal.id_sucursal}'
			)
			params.append(sucursal.id_sucursal)
		
		#-- Columna para el stock total.
		total_general = "SUM(ps.stock) AS stock_total"
		
		#-- 2. Construcción de filtros.
		conditions = []
		
		#-- Filtros por rango.
		range_filters = [
			('p.id_familia_id', id_familia_desde, id_familia_hasta),
			('p.id_marca_id', id_marca_desde, id_marca_hasta),
			('p.id_modelo_id', id_modelo_desde, id_modelo_hasta)
		]
		
		for field, desde, hasta in range_filters:
			if desde and hasta:
				conditions.append(f"{field} BETWEEN %s AND %s")
				params.extend([desde, hasta])
			elif desde:
				conditions.append(f"{field} >= %s")
				params.append(desde)
			elif hasta:
				conditions.append(f"{field} <= %s")
				params.append(hasta)
		
		filters = "AND " + " AND ".join(conditions) if conditions else ""
		
		#-- 4. Ensamblar consulta final.
		final_query = query.format(
			sucursal_columns=", ".join(sucursal_columns),
			total_general=total_general,
			filters=filters
		)
		
		#-- 5. Ejecutar con cursor y mapear a objetos del modelo.
		with connection.cursor() as cursor:
			cursor.execute(final_query, params)
			columns = [col[0] for col in cursor.description]
			rows = cursor.fetchall()
		
		#-- Crear objetos modelo simulados.
		ModelProxy = namedtuple('ModelProxy', columns)
		return [ModelProxy(*row) for row in rows]


class VLStockGeneralSucursal(models.Model):
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_modelo_id = models.IntegerField()
	nombre_modelo = models.CharField(max_length=50)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	id_producto = models.IntegerField()
	id_cai_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	medida = models.CharField(max_length=15)
	nombre_producto = models.CharField(max_length=50)
	stock = models.IntegerField()
	otras_suc = models.IntegerField()
	stock_total = models.IntegerField()
	
	objects = VLStockGeneralSucursalManager()
	
	class Meta:
		managed = False
		db_table = 'vlstockgeneralsucursal'
		verbose_name = ('Stock General por Sucursal')
		verbose_name_plural = ('Stock General por Sucursal')


#-----------------------------------------------------------------------------
# Listado de Stock a Fecha.
#-----------------------------------------------------------------------------
class VLStockFechaManager(models.Manager):
	
	def obtener_datos(self, id_producto_desde, id_producto_hasta, fecha):
		
		#-- La consulta SQL.
		query = """
			SELECT
				*
			FROM
				VLStockFecha
		"""
		
		#-- Filtros y parámetros.
		condition = []
		params = []
		
		if id_producto_desde and id_producto_hasta:
			condition.append("id_producto_id BETWEEN %s AND %s")
			params.extend([id_producto_desde, id_producto_hasta])
		elif id_producto_desde:
			condition.append("id_producto_id >= %s")
			params.extend([id_producto_desde])
		elif id_producto_hasta:
			condition.append("id_producto_id <= %s")
			params.extend([id_producto_hasta])
		
		if condition:
			# query += f" WHERE {condition}"
			query += " WHERE "
			query += " ".join(condition)
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLStockFecha(models.Model):
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_modelo_id = models.IntegerField()
	nombre_modelo = models.CharField(max_length=50)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	id_producto_id = models.IntegerField()
	id_cai_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	medida = models.CharField(max_length=15)
	nombre_producto = models.CharField(max_length=50)
	stock = models.IntegerField()
	
	objects = VLStockFechaManager()
	
	class Meta:
		managed = False
		db_table = 'vlstockfecha'
		verbose_name = ('Listado de Stock a Fecha')
		verbose_name_plural = ('Listado de Stock a Fecha')


#-----------------------------------------------------------------------------
# Listado de Stock Único.
#-----------------------------------------------------------------------------
class VLStockUnicoManager(models.Manager):
	
	def obtener_datos(self):
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLStockUnico
			ORDER by
				id_familia_id, id_modelo_id, id_marca_id, id_producto_id
		"""
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query)


class VLStockUnico(models.Model):
	id = models.IntegerField(primary_key=True)
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_modelo_id = models.IntegerField()
	nombre_modelo = models.CharField(max_length=50)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	id_producto_id = models.IntegerField()
	id_cai_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	medida = models.CharField(max_length=15)
	nombre_producto = models.CharField(max_length=50)
	stock = models.IntegerField()
	
	objects = VLStockUnicoManager()
	
	class Meta:
		managed = False
		db_table = 'vlstockunico'
		verbose_name = ('Listado de Stock Único')
		verbose_name_plural = ('Listado de Stock Único')


#-----------------------------------------------------------------------------
# Reposición de Stock.
#-----------------------------------------------------------------------------
class VLReposicionStockManager(models.Manager):
	
	def obtener_datos(self, id_deposito, id_familia_desde, id_familia_hasta, id_marca_desde, id_marca_hasta, id_modelo_desde, id_modelo_hasta, sucursales):
		from django.db import connection
		from collections import namedtuple
		
		#-- Construcción de la consulta base.
		query = """
			SELECT
				ps.id_deposito_id,
				pd.nombre_producto_deposito,
				p.id_familia_id,
				pf.nombre_producto_familia,
				p.id_modelo_id,
				pm.nombre_modelo,
				p.id_marca_id,
				px.nombre_producto_marca,
				ps.id_producto_id,
				p.id_cai_id,
				pc.cai,
				p.medida,
				p.segmento,
				p.nombre_producto,
				CASE 
					WHEN pn.minimo is not null THEN pn.minimo ELSE 0
				END AS minimo,
				SUM(ps.stock) AS stock,
				CASE
					WHEN pn.minimo is not null THEN pn.minimo - SUM(ps.stock) ELSE 0
				END AS faltante,
				{sucursal_columns}
			FROM
				producto_stock ps
				JOIN producto p ON ps.id_producto_id = p.id_producto
				JOIN producto_cai pc ON p.id_cai_id = pc.id_cai
				JOIN producto_minimo pn ON p.id_cai_id = pn.id_cai_id AND ps.id_deposito_id = pn.id_deposito_id
				JOIN producto_familia pf ON p.id_familia_id = pf.id_producto_familia
				JOIN producto_modelo pm ON p.id_modelo_id = pm.id_modelo
				JOIN producto_marca px ON p.id_marca_id = px.id_producto_marca
				JOIN producto_deposito pd ON ps.id_deposito_id = pd.id_producto_deposito
			WHERE
				ps.stock < pn.minimo
				AND pn.minimo <> 0
				AND p.tipo_producto = 'P'
				{filters}
			GROUP by
				pc.cai, ps.id_deposito_id
			HAVING
				pn.minimo - SUM(ps.stock) > 0
			ORDER by
				p.id_familia_id, p.id_modelo_id, p.id_marca_id
		"""
		
		#-- Parámetros para la consulta.
		params = []
		sucursal_columns = []
		
		#-- Subconsultas para obtener stock por sucursal.
		for sucursal in sucursales:
			subquery = """
				COALESCE((
					SELECT SUM(ps2.stock)
					FROM producto_stock ps2
					JOIN producto_deposito pd2 ON ps2.id_deposito_id = pd2.id_producto_deposito
					WHERE pd2.id_sucursal_id = %s AND ps2.id_producto_id = p.id_producto
					--GROUP BY pd2.id_sucursal_id AND ps2.id_producto_id
					GROUP BY pd2.id_sucursal_id, ps2.id_producto_id
					HAVING SUM(ps2.stock) > 0
				), 0) AS stock_suc_{sucursal_id}
			""".format(sucursal_id=sucursal.id_sucursal)
			
			sucursal_columns.append(subquery)
			params.append(sucursal.id_sucursal)
		
		#-- Filtros principales.
		conditions = ["ps.id_deposito_id = %s"]
		params.append(id_deposito)
		
		#-- Filtros por rango.
		range_filters = [
			('p.id_familia_id', id_familia_desde, id_familia_hasta),
			('p.id_marca_id', id_marca_desde, id_marca_hasta),
			('p.id_modelo_id', id_modelo_desde, id_modelo_hasta)
		]
		
		for field, desde, hasta in range_filters:
			if desde and hasta:
				conditions.append(f"{field} BETWEEN %s AND %s")
				params.extend([desde, hasta])
			elif desde:
				conditions.append(f"{field} >= %s")
				params.append(desde)
			elif hasta:
				conditions.append(f"{field} <= %s")
				params.append(hasta)
		
		filters = "AND " + " AND ".join(conditions) if conditions else ""
		
		#-- Ensamblar consulta final.
		final_query = query.format(
			sucursal_columns=", ".join(sucursal_columns),
			filters=filters
		)
		
		#-- Ejecutar con cursor y mapear a objetos del modelo.
		with connection.cursor() as cursor:
			cursor.execute(final_query, params)
			columns = [col[0] for col in cursor.description]
			rows = cursor.fetchall()
		
		#-- Crear objetos modelo simulados.
		ModelProxy = namedtuple('ModelProxy', columns)
		return [ModelProxy(*row) for row in rows]

class VLReposicionStock(models.Model):
	id_deposito = models.IntegerField()
	nombre_producto_deposito = models.CharField(max_length=50)
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_modelo_id = models.IntegerField()
	nombre_modelo = models.CharField(max_length=50)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	id_producto_id = models.IntegerField()
	id_cai_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	medida = models.CharField(max_length=15)
	segmento = models.CharField(max_length=3)
	nombre_producto = models.CharField(max_length=50)
	minimo = models.IntegerField()
	stock = models.IntegerField()
	faltante = models.IntegerField()
	
	objects = VLReposicionStockManager()
	
	class Meta:
		managed = False
		db_table = 'vlreposicionstock'
		verbose_name = ('Reposición de Stock')
		verbose_name_plural = ('Reposición de Stock')


#-----------------------------------------------------------------------------
# Movimiento Interno de Stock.
#-----------------------------------------------------------------------------
class VLMovimientoInternoStockManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, id_deposito=None):
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLMovimientoInternoStock
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros adicionales.
		if id_deposito:
			query += " AND id_deposito_id = %s"
			params.append(id_deposito)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER BY fecha_comprobante, numero_comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLMovimientoInternoStock(models.Model):
	id = models.IntegerField(primary_key=True)
	fecha_comprobante = models.DateField()
	numero_comprobante = models.IntegerField()
	observa_comprobante = models.CharField(max_length=100)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	medida = models.CharField(max_length=15)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	id_deposito = models.IntegerField()
	
	objects = VLMovimientoInternoStockManager()
	
	class Meta:
		managed = False
		db_table = 'vlmovimientoinfernostock'
		verbose_name = ('Movimiento Interno de Stock')
		verbose_name_plural = ('Movimiento Interno de Stock')


#-----------------------------------------------------------------------------
# Stock por Clientes en Depósitos.
#-----------------------------------------------------------------------------
class VLStockClienteManager(models.Manager):
	
	def obtener_datos(self, id_sucursal=None, id_vendedor=None):
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLStockCliente
		"""
		
		#-- Filtros y parámetros adicionales.
		params = []
		condicion = []
		
		if id_sucursal:
			condicion.append("id_sucursal_id = %s")
			params.append(id_sucursal)
		
		if id_vendedor:
			condicion.append("id_vendedor_id = %s")
			params.append(id_vendedor)
		
		if condicion:
			query += " WHERE " + " AND ".join(condicion)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER BY id_cliente_id, id_stock_cliente"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLStockCliente(models.Model):
	id = models.IntegerField(primary_key=True)
	id_cliente_id = models.IntegerField()
	nombre_cliente = models.CharField(max_length=50)
	id_producto_id = models.IntegerField()
	medida = models.CharField(max_length=15)
	cai = models.CharField(max_length=20)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	retirado = models.DecimalField(max_digits=7, decimal_places=2)
	stock = models.DecimalField(max_digits=7, decimal_places=2)
	comprobante = models.CharField(max_length=19)
	id_sucursal_id = models.IntegerField()
	id_vendedor_id = models.IntegerField()
	
	objects = VLStockClienteManager()
	
	class Meta:
		managed = False
		db_table = 'vlstockcliente'
		verbose_name = ('Stock por Clientes en Depósitos')
		verbose_name_plural = ('Stock por Clientes en Depósitos')


#-----------------------------------------------------------------------------
# Stock en Depósitos de Clientes.
#-----------------------------------------------------------------------------
class VLStockDepositoManager(models.Manager):
	
	def obtener_datos(self, id_sucursal=None):
		
		#-- La consulta SQL.
		query = """
			SELECT
				ROW_NUMBER() OVER() AS id,
				*
			FROM
				VLStockDeposito
		"""
		
		#-- Filtros y parámetros adicionales.
		params = []
		condicion = []
		
		if id_sucursal:
			condicion.append("id_sucursal_id = %s")
			params.append(id_sucursal)
		
		if condicion:
			query += " WHERE " + " AND ".join(condicion)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER BY id_familia_id, id_modelo_id, id_marca_id, medida"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLStockDeposito(models.Model):
	id = models.IntegerField(primary_key=True)
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_modelo_id = models.IntegerField()
	nombre_modelo = models.CharField(max_length=50)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	id_producto_id = models.IntegerField()
	medida = models.CharField(max_length=15)
	cai = models.CharField(max_length=20)
	nombre_producto = models.CharField(max_length=50)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	stock = models.DecimalField(max_digits=7, decimal_places=2)
	id_sucursal_id = models.IntegerField()
	
	objects = VLStockDepositoManager()
	
	class Meta:
		managed = False
		db_table = 'vlstockdeposito'
		verbose_name = ('Stock en Depósitos de Clientes')
		verbose_name_plural = ('Stock en Depósitos de Clientes')


#-----------------------------------------------------------------------------
# Ficha de Seguimiento de Stock por Código o CAI.
#-----------------------------------------------------------------------------
class VLFichaSeguimientoStockManager(models.Manager):
	
	def obtener_datos(self, id_producto, id_cai, fecha_desde, fecha_hasta, id_sucursal=None):
		
		#-- La consulta SQL.
		query = """
			SELECT
				(ROW_NUMBER() OVER(ORDER BY fecha_comprobante, comprobante, marca)) AS id,
				*
			FROM
				VLFichaSeguimientoStock
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Filtros y parámetros adicionales.
		condicion = []
		
		if id_producto:
			condicion.append("id_producto_id = %s")
			params.append(id_producto)
		
		if id_cai:
			condicion.append("id_cai_id = %s")
			params.append(id_cai)
		
		if id_sucursal:
			condicion.append("id_sucursal_id = %s")
			params.append(id_sucursal)
		
		if condicion:
			query += " AND " + " AND ".join(condicion)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER BY fecha_comprobante, comprobante, marca"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLFichaSeguimientoStock(models.Model):
	# id = models.AutoField(primary_key=True)
	id = models.IntegerField(primary_key=True)
	id_producto_id = models.IntegerField()
	id_cai_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	medida = models.CharField(max_length=15)
	nombre_producto = models.CharField(max_length=50)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	fecha_comprobante = models.DateField()
	comprobante = models.CharField(max_length=19)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	total = models.DecimalField(max_digits=12, decimal_places=2)
	id_cliente_proveedor = models.IntegerField()
	nombre_cliente_proveedor = models.CharField(max_length=50)
	no_estadist = models.BooleanField()	
	id_sucursal_id = models.IntegerField()
	id_deposito = models.IntegerField()
	marca = models.CharField(max_length=4)
	
	objects = VLFichaSeguimientoStockManager()
	
	class Meta:
		managed = False
		db_table = 'vlfichaseguimientostock'
		verbose_name = ('Ficha de Seguimiento de Stock')
		verbose_name_plural = ('Ficha de Seguimiento de Stock')


#-----------------------------------------------------------------------------
# Detalle de Compras por Proveedor.
#-----------------------------------------------------------------------------
class VLDetalleCompraProveedorManager(models.Manager):
	
	def obtener_datos(self, id_proveedor, fecha_desde, fecha_hasta, id_sucursal=None):
		
		#-- La consulta SQL.
		query = """
			SELECT
				(ROW_NUMBER() OVER(ORDER BY fecha_comprobante, comprobante)) AS id,
				*
			FROM
				VLDetalleCompraProveedor
			WHERE
				id_proveedor_id = %s
				AND fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [id_proveedor, fecha_desde, fecha_hasta]
		
		#-- Filtros y parámetros adicionales.
		condicion = []
		
		if id_sucursal:
			condicion.append("id_sucursal_id = %s")
			params.append(id_sucursal)
		
		if condicion:
			query += " AND " + " AND ".join(condicion)
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER BY fecha_comprobante, comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLDetalleCompraProveedor(models.Model):
	id = models.IntegerField(primary_key=True)
	id_proveedor_id = models.IntegerField()
	nombre_proveedor = models.CharField(max_length=50)
	comprobante = models.CharField(max_length=21)
	fecha_comprobante = models.DateField()
	id_cai_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	id_producto_id = models.IntegerField()
	nombre_producto = models.CharField(max_length=50)
	id_familia_id = models.IntegerField()
	nombre_producto_familia = models.CharField(max_length=50)
	id_marca_id = models.IntegerField()
	nombre_producto_marca = models.CharField(max_length=50)
	cantidad = models.DecimalField(max_digits=7, decimal_places=2)
	unidad = models.IntegerField()
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	total = models.DecimalField(max_digits=12, decimal_places=2)
	id_sucursal_id = models.IntegerField()
	nombre_sucursal = models.CharField(max_length=50)
	id_deposito = models.IntegerField()
	nombre_producto_deposito = models.CharField(max_length=50)
	
	objects = VLDetalleCompraProveedorManager()
	
	class Meta:
		managed = False
		db_table = 'vldetallecompraproveedor'
		verbose_name = ('Detalle de Compras por Proveedor')
		verbose_name_plural = ('Detalle de Compras por Proveedor')


#-----------------------------------------------------------------------------
# Comprobantes Ingresados.
#-----------------------------------------------------------------------------
class VLCompraIngresadaManager(models.Manager):
	
	def obtener_datos(self, fecha_desde, fecha_hasta, tipo_compro=None):
		
		if tipo_compro is None or tipo_compro == []:
			tipo_compro = ["IB"]
		
		#-- Determinar cantidad de marcas de parámetros para los comprobantes.
		placeholders = ','.join(['%s'] * len(tipo_compro))
		
		#-- La consulta SQL.
		query = """
			SELECT
				(ROW_NUMBER() OVER(ORDER BY codigo_comprobante_compra, fecha_comprobante, comprobante)) AS id,
				*
			FROM
				VLCompraIngresada
			WHERE
				fecha_comprobante BETWEEN %s AND %s
		"""
		
		#-- Se añaden parámetros.
		params = [fecha_desde, fecha_hasta]
		
		#-- Añadir filtro por tipos de comprobantes.
		query += f" AND codigo_comprobante_compra IN ({placeholders})"
		params.extend(tipo_compro)  # Extender con los elementos de la lista
		
		#-- Agregar el ordenamiento acá por rendimiento en la consulta.
		query += " ORDER BY codigo_comprobante_compra, fecha_comprobante, comprobante"
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLCompraIngresada(models.Model):
	id = models.IntegerField(primary_key=True)
	fecha_comprobante = models.DateField()
	codigo_comprobante_compra = models.CharField(max_length=3)
	comprobante = models.CharField(max_length=21)
	id_proveedor_id = models.IntegerField()
	nombre_proveedor = models.CharField(max_length=50)
	total = models.DecimalField(max_digits=12, decimal_places=2)
	observa_comprobante = models.CharField(max_length=50)
	
	objects = VLCompraIngresadaManager()
	
	class Meta:
		managed = False
		db_table = 'vlcompraingresada'
		verbose_name = ('Comprobantes Ingresados')
		verbose_name_plural = ('Comprobantes Ingresados')


#-----------------------------------------------------------------------------
# Stock Mínimo por CAI.
#-----------------------------------------------------------------------------
class VLProductoMinimoManager(models.Manager):
	
	def obtener_datos(self, id_cai=None, id_deposito=None):
		
		#-- La consulta SQL.
		query = """
			SELECT
				(ROW_NUMBER() OVER(ORDER BY cai, id_deposito_id)) AS id,
				*
			FROM
				VLProductoMinimo
		"""
		
		#-- Se añaden parámetros.
		params = []
		
		#-- Filtros y parámetros adicionales.
		condicion = []
		
		if id_cai:
			condicion.append("id_cai_id = %s")
			params.append(id_cai)
		
		if id_deposito:
			condicion.append("id_deposito_id = %s")
			params.append(id_deposito)
		
		if condicion:
			query += " WHERE " + " AND ".join(condicion)
		
		#-- Se ejecuta la consulta con `raw` y se devueven los resultados.
		return self.raw(query, params)


class VLProductoMinimo(models.Model):
	id = models.IntegerField(primary_key=True)
	id_cai_id = models.IntegerField()
	cai = models.CharField(max_length=20)
	id_deposito_id = models.IntegerField()
	nombre_producto_deposito = models.CharField(max_length=50)
	minimo = models.IntegerField()

	objects = VLProductoMinimoManager()

	class Meta:
		managed = False
		db_table = 'vlproductominimo'
		verbose_name = ('Stock Mínimo por CAI')
		verbose_name_plural = ('Stock Mínimo por CAI')


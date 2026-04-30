# Define las columnas Bootstrap y sección para cada campo


class Design:
	checkbox = "checkbox"


estructura_campos = {
	'persona': {
		'Información Personal': {
			'fila_1': [
					{'field_name': 'estatus_persona', 'columna': 2, 'design': None},
					{'field_name': 'nombre_persona', 'columna': 4, 'design': None},
					{'field_name': 'apellido_persona', 'columna': 4, 'design': None},
					{'field_name': 'fecha_ingreso', 'columna': 2, 'design': None},
			],
			'fila_2': [
				{'field_name': 'email_persona1', 'columna': 5, 'design': None},
				{'field_name': 'email_persona2', 'columna': 5, 'design': None},
				{'field_name': 'fecha_nacimiento', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'direccion_persona', 'columna': 12, 'design': None},
			],
			'fila_4': [
				{'field_name': 'id_pais_telefono', 'columna': 2, 'design': None},
				{'field_name': 'telefono_persona', 'columna': 2, 'design': None},
				{'field_name': 'id_pais_telefmov1', 'columna': 2, 'design': None},
				{'field_name': 'telefmov_persona1', 'columna': 2, 'design': None},
				{'field_name': 'id_pais_telefmov2', 'columna': 2, 'design': None},
				{'field_name': 'telefmov_persona2', 'columna': 2, 'design': None},
			],
			'fila_5': [
				{'field_name': 'ciudad_residencia', 'columna': 3, 'design': None},
				{'field_name': 'id_pais_residencia', 'columna': 3, 'design': None},
				{'field_name': 'codigo_postal', 'columna': 3, 'design': None},
				{'field_name': 'aeropuerto_cercano', 'columna': 3, 'design': None},
			],
			'fila_6': [
				{'field_name': 'id_pais_nacimiento', 'columna': 4, 'design': None},
				{'field_name': 'id_pais_nacionalidad', 'columna': 4, 'design': None},
			],
			'fila_7': [
				{'field_name': 'imagen_persona1', 'columna': 4, 'design': None},
				{'field_name': 'imagen_persona2', 'columna': 4, 'design': None},
			],
			# Agrega más filas o campos según sea necesario
		},
		'Black List': {
			'fila_1': [
				{'field_name': 'estatus_black', 'columna': 3, 'design': None},
				{'field_name': 'fecha_black', 'columna': 3, 'design': None},
				{'field_name': 'motivo_black', 'columna': 6, 'design': None},
			],
		},
		'Apariencia Personal y Tallas': {
			'fila_1': [
				{'field_name': 'id_color_cabello', 'columna': 3, 'design': None},
				{'field_name': 'id_color_ojos', 'columna': 3, 'design': None},
				{'field_name': 'estatura', 'columna': 3, 'design': None},
				{'field_name': 'peso', 'columna': 3, 'design': None},
			],
			'fila_2': [
				{'field_name': 'talla_tshirt', 'columna': 4, 'design': None},
				{'field_name': 'talla_coverall', 'columna': 4, 'design': None},
				{'field_name': 'talla_pantalon', 'columna': 4, 'design': None},
			],
			# Agrega más filas o campos según sea necesario
		},
		'Información en caso de Emergencia': {
			'fila_1': [
				{'field_name': 'nombre_apellidos_contacto', 'columna': 12, 'design': None},
			],
			'fila_2': [
				{'field_name': 'id_pais_telefcont', 'columna': 4, 'design': None},
				{'field_name': 'telefono_contacto', 'columna': 4, 'design': None},
				{'field_name': 'email_contacto', 'columna': 4, 'design': None},
			],
			# Agrega más filas o campos según sea necesario
		},
		'Pasaporte Visa y Documentos de Viaje': {
			'fila_1': [
				{'field_name': 'nombre_apellidos_contacto', 'columna': 12, 'design': None},
			],
			'fila_2': [
				{'field_name': 'id_pais_telefcont', 'columna': 4, 'design': None},
				{'field_name': 'telefono_contacto', 'columna': 4, 'design': None},
				{'field_name': 'email_contacto', 'columna': 4, 'design': None},
			],
			# Agrega más filas o campos según sea necesario
		},
	},
	
	'actividad': {
		'Información Actividad': {
			'fila_1': [
				{'field_name': 'estatus_actividad', 'columna': 2, 'design': None},
				{'field_name': 'descripcion_actividad', 'columna': 4, 'design': None},
				{'field_name': 'fecha_registro_actividad', 'columna': 2, 'design': None}
			]
		}
	},
	
	'producto_deposito': {
		'Información Producto Depósito': {
			'fila_1': [
				{'field_name': 'estatus_producto_deposito', 'columna': 2, 'design': None},
				{'field_name': 'id_sucursal', 'columna': 4, 'design': None},
				{'field_name': 'nombre_producto_deposito', 'columna': 4, 'design': None}
			]
		}
	},
	
	'producto_familia': {
		'Información Producto Familia': {
			'fila_1': [
						{'field_name': 'estatus_producto_familia', 'columna': 2, 'design': None},
						{'field_name': 'nombre_producto_familia', 'columna': 4, 'design': None},
						{'field_name': 'comision_operario', 'columna': 2, 'design': None}
			],
			'fila_2': [
						{'field_name': 'info_michelin_auto', 'columna': 2, 'design': Design.checkbox},
						{'field_name': 'info_michelin_camion', 'columna': 2, 'design': Design.checkbox},
			]
		}
	},
	
	'moneda': {
		'Información Moneda': {
			'fila_1': [
				{'field_name': 'estatus_moneda', 'columna': 2, 'design': None},
				{'field_name': 'nombre_moneda', 'columna': 2, 'design': None},
				{'field_name': 'simbolo_moneda', 'columna': 1, 'design': None}
			],
			'fila_2': [
				{'field_name': 'cotizacion_moneda', 'columna': 2, 'design': None},
				{'field_name': 'ws_afip', 'columna': 1, 'design': None},
				{'field_name': 'predeterminada', 'columna': 2, 'design': Design.checkbox}
			],
		}
	},
	
	'producto_marca': {
		'Información Producto Marca': {
			'fila_1': [
				{'field_name': 'estatus_producto_marca', 'columna': 2, 'design': None},
				{'field_name': 'nombre_producto_marca', 'columna': 4, 'design': None},
				{'field_name': 'id_moneda', 'columna': 2, 'design': None},
			],
			'fila_2': [
				{'field_name': 'principal', 'columna': 2, 'design': Design.checkbox},
				{'field_name': 'info_michelin_auto', 'columna': 2, 'design': Design.checkbox},
				{'field_name': 'info_michelin_camion', 'columna': 2, 'design': Design.checkbox},
			],
		}
	},
	
	'producto_modelo': {
		'Información Producto Modelo': {
			'fila_1': [
				{'field_name': 'estatus_modelo', 'columna': 2, 'design': None},
				{'field_name': 'nombre_modelo', 'columna': 4, 'design': None},
			]
		}
	},
	
	'producto_minimo': {
		'Información Producto Mínimo': {
			'fila_1': [
				{'field_name': 'cai', 'columna': 2, 'design': None},
				{'field_name': 'minimo', 'columna': 2, 'design': None},
				{'field_name': 'id_deposito', 'columna': 4, 'design': None},
			]
		}
	},
	
	'producto_stock': {
		'Información Producto Stock': {
			'fila_1': [
				{'field_name': 'id_producto', 'columna': 3, 'design': None},
				{'field_name': 'id_deposito', 'columna': 3, 'design': None},
				{'field_name': 'stock', 'columna': 2, 'design': None},
				{'field_name': 'minimo', 'columna': 2, 'design': None},
				{'field_name': 'fecha_producto_stock', 'columna': 2, 'design': None},
			]
		}
	},
	
	'producto_estado': {
		'Información Producto Estado': {
			'fila_1': [
				{'field_name': 'estatus_producto_estado', 'columna': 2, 'design': None},
				{'field_name': 'estado_producto', 'columna': 2, 'design': None},
				{'field_name': 'nombre_impresion', 'columna': 2, 'design': None},
			]
		}
	},
	
	'comprobante_venta': {
		'Información Comprobante Venta': {
			'fila_1': [
				{'field_name': 'estatus_comprobante_venta', 'columna': 2, 'design': None},
				{'field_name': 'codigo_comprobante_venta', 'columna': 2, 'design': None},
				{'field_name': 'nombre_comprobante_venta', 'columna': 4, 'design': None},
				{'field_name': 'compro_asociado', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'mult_venta', 'columna': 2, 'design': None},
				{'field_name': 'mult_saldo', 'columna': 2, 'design': None},
				{'field_name': 'mult_stock', 'columna': 2, 'design': None},
				{'field_name': 'mult_comision', 'columna': 2, 'design': None},
				{'field_name': 'mult_caja', 'columna': 2, 'design': None},
				{'field_name': 'mult_estadistica', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'libro_iva', 'columna': 2, 'design': Design.checkbox},
				{'field_name': 'estadistica', 'columna': 2, 'design': Design.checkbox},
				{'field_name': 'electronica', 'columna': 2, 'design': Design.checkbox},
				{'field_name': 'presupuesto', 'columna': 2, 'design': Design.checkbox},
				{'field_name': 'pendiente', 'columna': 2, 'design': Design.checkbox},
			],
			'fila_4': [
				{'field_name': 'codigo_afip_a', 'columna': 2, 'design': None},
				{'field_name': 'codigo_afip_b', 'columna': 2, 'design': None},
				{'field_name': 'compro_asociado', 'columna': 4, 'design': None},
				{'field_name': 'recibo', 'columna': 2, 'design': Design.checkbox},
				{'field_name': 'manual', 'columna': 2, 'design': Design.checkbox},
			],
			'fila_5': [
				{'field_name': 'info_michelin_auto', 'columna': 2, 'design': Design.checkbox},
				{'field_name': 'info_michelin_camion', 'columna': 2, 'design': Design.checkbox},
			],
		}
	},
	
	'comprobante_compra': {
		'Información Comprobante Compra': {
			'fila_1': [
				{'field_name': 'estatus_comprobante_compra', 'columna': 2, 'design': None},
				{'field_name': 'codigo_comprobante_compra', 'columna': 2, 'design': None},
				{'field_name': 'nombre_comprobante_compra', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'mult_compra', 'columna': 2, 'design': None},
				{'field_name': 'mult_saldo', 'columna': 2, 'design': None},
				{'field_name': 'mult_stock', 'columna': 2, 'design': None},
				{'field_name': 'mult_caja', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'codigo_afip_a', 'columna': 2, 'design': None},
				{'field_name': 'codigo_afip_b', 'columna': 2, 'design': None},
				{'field_name': 'codigo_afip_c', 'columna': 2, 'design': None},
				{'field_name': 'codigo_afip_m', 'columna': 2, 'design': None},
			],
			'fila_4': [
				{'field_name': 'libro_iva', 'columna': 2, 'design': Design.checkbox},
			],
		}
	},
	
	'provincia': {
		'Información Provincia': {
			'fila_1': [
				{'field_name': 'estatus_provincia', 'columna': 2, 'design': None},
				{'field_name': 'codigo_provincia', 'columna': 1, 'design': None},
				{'field_name': 'nombre_provincia', 'columna': 3, 'design': None},
			]
		}
	},
	
	'localidad': {
		'Información Localidad': {
			'fila_1': [
				{'field_name': 'estatus_localidad', 'columna': 2, 'design': None},
				{'field_name': 'nombre_localidad', 'columna': 3, 'design': None},
				{'field_name': 'codigo_postal', 'columna': 2, 'design': None},
				{'field_name': 'id_provincia', 'columna': 3, 'design': None},
			]
		}
	},
	
	'tipo_documento_identidad': {
		'Información Tipo Documento Identidad': {
			'fila_1': [
				{'field_name': 'estatus_tipo_documento_identidad', 'columna': 2, 'design': None},
				{'field_name': 'nombre_documento_identidad', 'columna': 2, 'design': None},
				{'field_name': 'tipo_documento_identidad', 'columna': 2, 'design': None},
				{'field_name': 'codigo_afip', 'columna': 2, 'design': None},
				{'field_name': 'ws_afip', 'columna': 2, 'design': None},
			]
		}
	},
	
	'tipo_iva': {
		'Información Tipo I.V.A.': {
			'fila_1': [
				{'field_name': 'estatus_tipo_iva', 'columna': 2, 'design': None},
				{'field_name': 'codigo_iva', 'columna': 2, 'design': None},
				{'field_name': 'nombre_iva', 'columna': 3, 'design': None},
				{'field_name': 'discrimina_iva', 'columna': 2, 'design': Design.checkbox},
			]
		}
	},
	
	'tipo_percepcion_ib': {
		'Información Tipo Percepción IB': {
			'fila_1': [
				{'field_name': 'estatus_tipo_percepcion_ib', 'columna': 2, 'design': None},
				{'field_name': 'descripcion_tipo_percepcion_ib', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'alicuota', 'columna': 2, 'design': None},
				{'field_name': 'monto', 'columna': 2, 'design': None},
				{'field_name': 'minimo', 'columna': 2, 'design': None},
				{'field_name': 'neto_total', 'columna': 2, 'design': Design.checkbox},
			],
		}
	},
	
	'tipo_retencion_ib': {
		'Información Tipo Retención IB': {
			'fila_1': [
				{'field_name': 'estatus_tipo_retencion_ib', 'columna': 2, 'design': None},
				{'field_name': 'descripcion_tipo_retencion_ib', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'alicuota_inscripto', 'columna': 2, 'design': None},
				{'field_name': 'alicuota_no_inscripto', 'columna': 2, 'design': None},
				{'field_name': 'monto', 'columna': 2, 'design': None},
				{'field_name': 'minimo', 'columna': 2, 'design': None},
			],
		}
	},
	
	'operario': {
		'Información Operario': {
			'fila_1': [
				{'field_name': 'estatus_operario', 'columna': 2, 'design': None},
				{'field_name': 'nombre_operario', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'telefono_operario', 'columna': 2, 'design': None},
				{'field_name': 'email_operario', 'columna': 4, 'design': None},
			],
		}
	},
	
	'producto': {
		'Información Producto': {
			'fila_1': [
				{'field_name': 'estatus_producto', 'columna': 2, 'design': None},
				{'field_name': 'codigo_producto', 'columna': 2, 'design': None, 'design': None},
				{'field_name': 'nombre_producto', 'columna': 4, 'design': None},
				{'field_name': 'tipo_producto', 'columna': 2, 'design': None},
			],
			'fila_2': [
				{'field_name': 'id_familia', 'columna': 4, 'design': None},
				{'field_name': 'id_marca', 'columna': 4, 'design': None},
				{'field_name': 'id_modelo', 'columna': 4, 'design': None},
			],
			'fila_3': [
				{'field_name': 'cai', 'columna': 2, 'design': None},
				{'field_name': 'medida', 'columna': 2, 'design': None},
				{'field_name': 'segmento', 'columna': 2, 'design': None},
				{'field_name': 'unidad', 'columna': 2, 'design': None},
				{'field_name': 'fecha_fabricacion', 'columna': 2, 'design': None},
			],
			'fila_4': [
				{'field_name': 'costo', 'columna': 2, 'design': None},
				{'field_name': 'alicuota_iva', 'columna': 2, 'design': None},
				{'field_name': 'precio', 'columna': 2, 'design': None},
				{'field_name': 'descuento', 'columna': 2, 'design': None},
			],
			'fila_5': [
				{'field_name': 'stock', 'columna': 2, 'design': None},
				{'field_name': 'minimo', 'columna': 2, 'design': None},
				{'field_name': 'despacho_1', 'columna': 2, 'design': None},
				{'field_name': 'despacho_2', 'columna': 2, 'design': None},
			],
			'fila_6': [
				{'field_name': 'descripcion_producto', 'columna': 4, 'design': None},
				{'field_name': 'carrito', 'columna': 2, 'design': Design.checkbox},
			],
		}
	},
	
	'cliente': {
		'Información General': {
			'fila_1': [
				{'field_name': 'estatus_cliente', 'columna': 2, 'design': None},
				{'field_name': 'nombre_cliente', 'columna': 4, 'design': None},
				{'field_name': 'domicilio_cliente', 'columna': 6, 'design': None},
			],
			'fila_2': [
				{'field_name': 'codigo_postal', 'columna': 2, 'design': None},
				{'field_name': 'id_provincia', 'columna': 4, 'design': None},
				{'field_name': 'id_localidad', 'columna': 4, 'design': None},
			],
			'fila_3': [
				{'field_name': 'tipo_persona', 'columna': 2, 'design': None},
				{'field_name': 'id_tipo_documento_identidad', 'columna': 2, 'design': None},
				{'field_name': 'cuit', 'columna': 2, 'design': None},
				{'field_name': 'id_tipo_iva', 'columna': 2, 'design': None},
				{'field_name': 'condicion_venta', 'columna': 2, 'design': None},
			],
			'fila_4': [
				{'field_name': 'telefono_cliente', 'columna': 2, 'design': None},
				{'field_name': 'fax_cliente', 'columna': 2, 'design': None},
				{'field_name': 'movil_cliente', 'columna': 2, 'design': None},
				{'field_name': 'email_cliente', 'columna': 3, 'design': None},
				{'field_name': 'email2_cliente', 'columna': 3, 'design': None},
			],
			'fila_5': [
				{'field_name': 'transporte_cliente', 'columna': 3, 'design': None},
				{'field_name': 'id_vendedor', 'columna': 3, 'design': None},
				{'field_name': 'fecha_nacimiento', 'columna': 2, 'design': None},
				{'field_name': 'fecha_alta', 'columna': 2, 'design': None},
				{'field_name': 'sexo', 'columna': 2, 'design': None},
			],
			'fila_6': [
				{'field_name': 'id_actividad', 'columna': 3, 'design': None},
				{'field_name': 'id_sucursal', 'columna': 3, 'design': None},
				{'field_name': 'id_percepcion_ib', 'columna': 3, 'design': None},
				{'field_name': 'numero_ib', 'columna': 3, 'design': None},
			],
			'fila_7': [
				{'field_name': 'vip', 'columna': 2, 'design': None},
				{'field_name': 'mayorista', 'columna': 2, 'design': None},
				{'field_name': 'sub_cuenta', 'columna': 2, 'design': None},
				{'field_name': 'observaciones_cliente', 'columna': 6, 'design': None},
			],
			# Agrega más filas o campos según sea necesario
		},
		'Black List': {
			'fila_1': [
				{'field_name': 'black_list', 'columna': 2, 'design': None},
				{'field_name': 'black_list_motivo', 'columna': 5, 'design': None},
				{'field_name': 'black_list_usuario', 'columna': 3, 'design': None},
				{'field_name': 'fecha_baja', 'columna': 2, 'design': None},
			],
		},
	},
	
	'proveedor': {
		'Información Proveedor': {
			'fila_1': [
				{'field_name': 'estatus_proveedor', 'columna': 2, 'design': None},
				{'field_name': 'nombre_proveedor', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'domicilio_proveedor', 'columna': 4, 'design': None},
				{'field_name': 'id_localidad', 'columna': 2, 'design': None},
				{'field_name': 'codigo_postal', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'telefono_proveedor', 'columna': 2, 'design': None},
				{'field_name': 'movil_proveedor', 'columna': 2, 'design': None},
				{'field_name': 'email_proveedor', 'columna': 4, 'design': None},
			],
			'fila_4': [
				{'field_name': 'ib_numero', 'columna': 2, 'design': None},
				{'field_name': 'cuit', 'columna': 2, 'design': None},
				{'field_name': 'id_tipo_iva', 'columna': 2, 'design': None},
			],
			'fila_5': [
				{'field_name': 'id_tipo_retencion_ib', 'columna': 4, 'design': None},
				{'field_name': 'ib_alicuota', 'columna': 2, 'design': None},
				{'field_name': 'ib_exento', 'columna': 2, 'design': Design.checkbox},
				{'field_name': 'multilateral', 'columna': 3, 'design': Design.checkbox},
			],
			'fila_6': [
				{'field_name': 'observacion_proveedor', 'columna': 10, 'design': None},
			],
		}
	},
	
	'parametro': {
		'Información Parámetros': {
			'fila_1': [
				{'field_name': 'estatus_parametro', 'columna': 2, 'design': None},
				{'field_name': 'id_empresa', 'columna': 8, 'design': None},
			],
			'fila_2': [
				{'field_name': 'interes', 'columna': 2, 'design': None},
				{'field_name': 'interes_dolar', 'columna': 2, 'design': None},
				{'field_name': 'cotizacion_dolar', 'columna': 2, 'design': None},
				{'field_name': 'dias_vencimiento', 'columna': 2, 'design': None},
				{'field_name': 'descuento_maximo', 'columna': 2, 'design': None},
			],
		}
	},
	
	'numero': {
		'Información Numeración de Comprobantes': {
			'fila_1': [
				{'field_name': 'estatus_numero', 'columna': 2, 'design': None},
				{'field_name': 'id_sucursal', 'columna': 4, 'design': None},
				{'field_name': 'punto_venta', 'columna': 2, 'design': None},
			],
			'fila_2': [
				{'field_name': 'comprobante', 'columna': 2, 'design': None},
				{'field_name': 'letra', 'columna': 2, 'design': None},
				{'field_name': 'numero', 'columna': 2, 'design': None},
				{'field_name': 'lineas', 'columna': 2, 'design': None},
				{'field_name': 'copias', 'columna': 2, 'design': None},
			],
		}
	},
	
	'sucursal': {
		'Información Sucursal': {
			'fila_1': [
				{'field_name': 'estatus_sucursal', 'columna': 2, 'design': None},
				{'field_name': 'nombre_sucursal', 'columna': 4, 'design': None},
				{'field_name': 'codigo_michelin', 'columna': 2, 'design': None},
			],
			'fila_2': [
				{'field_name': 'domicilio_sucursal', 'columna': 4, 'design': None},
				{'field_name': 'id_localidad', 'columna': 2, 'design': None},
				{'field_name': 'id_provincia', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'telefono_sucursal', 'columna': 2, 'design': None},
				{'field_name': 'email_sucursal', 'columna': 4, 'design': None},
				{'field_name': 'inicio_actividad', 'columna': 2, 'design': None},
			],
		}
	},
	
	'vendedor': {
		'Información Vendedor': {
			'fila_1': [
				{'field_name': 'estatus_vendedor', 'columna': 2, 'design': None},
				{'field_name': 'nombre_vendedor', 'columna': 3, 'design': None},
			],
			'fila_2': [
				{'field_name': 'telefono_vendedor', 'columna': 2, 'design': None},
				{'field_name': 'domicilio_vendedor', 'columna': 3, 'design': None},
				{'field_name': 'email_vendedor', 'columna': 4, 'design': None},
			],
			'fila_3': [
				{'field_name': 'pje_auto', 'columna': 2, 'design': None},
				{'field_name': 'pje_camion', 'columna': 2, 'design': None},
				{'field_name': 'vence_factura', 'columna': 2, 'design': None},
				{'field_name': 'vence_remito', 'columna': 2, 'design': None},
			],
			'fila_4': [
				{'field_name': 'id_sucursal', 'columna': 4, 'design': None},
				{'field_name': 'tipo_venta', 'columna': 2, 'design': None},
				{'field_name': 'col_descuento', 'columna': 2, 'design': None},
			],
			'fila_5': [
				{'field_name': 'email_venta', 'columna': 4, 'design': Design.checkbox},
				{'field_name': 'info_saldo', 'columna': 4, 'design': Design.checkbox},
				{'field_name': 'info_estadistica', 'columna': 4, 'design': Design.checkbox},
			],
		}
	},
	
	'medio_pago': {
		'Información Medio de Pago': {
			'fila_1': [
				{'field_name': 'estatus_medio_pago', 'columna': 2, 'design': None},
				{'field_name': 'nombre_medio_pago', 'columna': 4, 'design': None},
				{'field_name': 'condicion_medio_pago', 'columna': 2, 'design': None},
				{'field_name': 'plazo_medio_pago', 'columna': 2, 'design': None},
			]
		}
	},
	
	'empresa': {
		'Información Empresa': {
			'fila_1': [
				{'field_name': 'estatus_empresa', 'columna': 2, 'design': None},
				{'field_name': 'nombre_fiscal', 'columna': 4, 'design': None},
				{'field_name': 'nombre_comercial', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'domicilio_empresa', 'columna': 4, 'design': None},
				{'field_name': 'codigo_postal', 'columna': 2, 'design': None},
				{'field_name': 'id_localidad', 'columna': 3, 'design': None},
				{'field_name': 'id_provincia', 'columna': 3, 'design': None},
			],
			'fila_3': [
				{'field_name': 'telefono', 'columna': 2, 'design': None},
				{'field_name': 'email_empresa', 'columna': 4, 'design': None},
				{'field_name': 'web_empresa', 'columna': 4, 'design': None},
				{'field_name': 'logo_empresa', 'columna': 2, 'design': None},
			],
			'fila_4': [
				{'field_name': 'id_iva', 'columna': 3, 'design': None},
				{'field_name': 'cuit', 'columna': 2, 'design': None},
				{'field_name': 'ingresos_bruto', 'columna': 2, 'design': None},
				{'field_name': 'inicio_actividad', 'columna': 2, 'design': None},
			],
			'fila_5': [
				{'field_name': 'cbu', 'columna': 3, 'design': None},
				{'field_name': 'cbu_alias', 'columna': 4, 'design': None},
				{'field_name': 'cbu_vence', 'columna': 2, 'design': None},
			],
			'fila_6': [
				{'field_name': 'ws_archivo_crt', 'columna': 4, 'design': None},
				{'field_name': 'ws_archivo_key', 'columna': 4, 'design': None},
				{'field_name': 'ws_vence', 'columna': 2, 'design': None},
			],
			'fila_7': [
				{'field_name': 'ws_expiracion', 'columna': 2, 'design': None},
				{'field_name': 'ws_token', 'columna': 4, 'design': None},
				{'field_name': 'ws_sign', 'columna': 4, 'design': None},
			],
			'fila_8': [
				{'field_name': 'ws_modo', 'columna': 2, 'design': None},
			],
		},
		'Parámetros': {
			'fila_1': [
				{'field_name': 'interes', 'columna': 2, 'design': None},
				{'field_name': 'interes_dolar', 'columna': 2, 'design': None},
				{'field_name': 'cotizacion_dolar', 'columna': 2, 'design': None},
				{'field_name': 'dias_vencimiento', 'columna': 2, 'design': None},
				{'field_name': 'descuento_maximo', 'columna': 2, 'design': None},
			],
		},
	},
	
	'punto_venta': {
		'Información del Punto de Venta': {
			'fila_1': [
				{'field_name': 'estatus_punto_venta', 'columna': 2, 'design': None},
				{'field_name': 'punto_venta', 'columna': 2, 'design': None},
				{'field_name': 'descripcion_punto_venta', 'columna': 4, 'design': None},
			],
		}
	},
	
	'alicuota_iva': {
		'Información de Alícuotas de IVA': {
			'fila_1': [
				{'field_name': 'estatus_alicuota_iva', 'columna': 2, 'design': None},
				{'field_name': 'codigo_alicuota', 'columna': 2, 'design': None},
				{'field_name': 'alicuota_iva', 'columna': 2, 'design': None},
				{'field_name': 'descripcion_alicuota_iva', 'columna': 4, 'design': None},
			],
		}
	},
	
	'banco': {
		'Información Banco': {
			'fila_1': [
				{'field_name': 'estatus_banco', 'columna': 2, 'design': None},
				{'field_name': 'nombre_banco', 'columna': 4, 'design': None},
				{'field_name': 'codigo_banco', 'columna': 2, 'design': None},
				{'field_name': 'cuit_banco', 'columna': 2, 'design': None},
			],
		}
	},
	
	'cuenta_banco': {
		'Información Cuentas de Banco': {
			'fila_1': [
				{'field_name': 'estatus_cuenta_banco', 'columna': 2, 'design': None},
				{'field_name': 'numero_cuenta', 'columna': 2, 'design': None},
				{'field_name': 'tipo_cuenta', 'columna': 2, 'design': None},
				{'field_name': 'id_banco', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'sucursal', 'columna': 2, 'design': None},
				{'field_name': 'codigo_postal', 'columna': 2, 'design': None},
				{'field_name': 'id_proveedor', 'columna': 2, 'design': None},
				{'field_name': 'id_moneda', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'cbu', 'columna': 2, 'design': None},
				{'field_name': 'codigo_imputacion', 'columna': 2, 'design': None},
				{'field_name': 'tope_negociacion', 'columna': 2, 'design': None},
				{'field_name': 'reporte_reques', 'columna': 2, 'design': None},
			],
		}
	},
	
	'tarjeta': {
		'Información Tarjeta': {
			'fila_1': [
				{'field_name': 'estatus_tarjeta', 'columna': 2, 'design': None},
				{'field_name': 'nombre_tarjeta', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'imputacion', 'columna': 2, 'design': None},
				{'field_name': 'banco_acreditacion', 'columna': 2, 'design': None},
				{'field_name': 'propia', 'columna': 2, 'design': Design.checkbox},
			],
		}
	},
	
	'codigo_retencion': {
		'Información Código de Terención': {
			'fila_1': [
				{'field_name': 'estatus_cod_retencion', 'columna': 2, 'design': None},
				{'field_name': 'nombre_codigo_retencion', 'columna': 3, 'design': None},
				{'field_name': 'imputacion', 'columna': 2, 'design': None},
			],
		}
	},
	
	'concepto_banco': {
		'Información Concepto Banco': {
			'fila_1': [
				{'field_name': 'estatus_concepto_banco', 'columna': 2, 'design': None},
				{'field_name': 'nombre_concepto_banco', 'columna': 3, 'design': None},
				{'field_name': 'factor', 'columna': 2, 'design': None},
			],
		}
	},
	
	'marketing_origen': {
		'Información Marketing Origen': {
			'fila_1': [
				{'field_name': 'estatus_marketing_origen', 'columna': 2, 'design': None},
				{'field_name': 'nombre_marketing_origen', 'columna': 3, 'design': None},
			],
		}
	},
	
	'medidas_estados': {
		'Información Medidas Estados': {
			'fila_1': [
				# {'field_name': 'estatus_medida_estado', 'columna': 2, 'design': None},
				{'field_name': 'id_cai', 'columna': 2, 'design': None},
				{'field_name': 'medida', 'columna': 2, 'design': None},
				{'field_name': 'descripcion', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'stock_desde', 'columna': 2, 'design': None},
				{'field_name': 'stock_hasta', 'columna': 2, 'design': None},
				{'field_name': 'id_estado', 'columna': 2, 'design': None},
			],
		}
	},	
	
	'compra_otros': {
		'Información Compras - Otros': {
			'fila_1': [
				{'field_name': 'estatus_comprabante', 'columna': 2, 'design': None},
				{'field_name': 'id_sucursal', 'columna': 4, 'design': None},
				{'field_name': 'id_punto_venta', 'columna': 2, 'design': None},
				{'field_name': 'id_deposito', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'id_comprobante_compra', 'columna': 2, 'design': None},
				{'field_name': 'compro', 'columna': 2, 'design': None},
				{'field_name': 'letra_comprobante', 'columna': 2, 'design': None},
				{'field_name': 'numero_comprobante', 'columna': 2, 'design': None},
				{'field_name': 'fecha_comprobante', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'id_proveedor', 'columna': 4, 'design': None},
				{'field_name': 'condicion_comprobante', 'columna': 2, 'design': None},
				{'field_name': 'fecha_registro', 'columna': 2, 'design': None},
				{'field_name': 'fecha_vencimiento', 'columna': 2, 'design': None},
			],
			'fila_4': [
				{'field_name': 'id_comprobante_venta', 'columna': 4, 'design': None},
				{'field_name': 'numero_comprobante_venta', 'columna': 2, 'design': None},
				{'field_name': 'fecha_comprobante_venta', 'columna': 2, 'design': None},
				{'field_name': 'total_comprobante_venta', 'columna': 2, 'design': None},
			],
			'fila_5': [
				{'field_name': 'exento', 'columna': 4, 'design': None},
				{'field_name': 'alicuota_iva', 'columna': 2, 'design': None},
				{'field_name': 'retencion_ingreso_bruto', 'columna': 2, 'design': None},
				{'field_name': 'total', 'columna': 2, 'design': None},
			],
		}
	},	
	
	'descuento_revendedor': {
		'Información Descuento Revendedor': {
			'fila_1': [
				{'field_name': 'estatus_descuento_revendedor', 'columna': 2, 'design': None},
				{'field_name': 'id_marca', 'columna': 4, 'design': None},
				{'field_name': 'id_familia', 'columna': 4, 'design': None},
				{'field_name': 'descuento', 'columna': 2, 'design': None},
			],
		}
	},	
	
	'descuento_vendedor': {
		'Información Descuento Vendedor': {
			'fila_1': [
				{'field_name': 'estatus_descuento_vendedor', 'columna': 2, 'design': None},
				{'field_name': 'id_marca', 'columna': 4, 'design': None},
				{'field_name': 'id_familia', 'columna': 4, 'design': None},
			],
			'fila_2': [
				{'field_name': 'desc1', 'columna': 2, 'design': None},
				{'field_name': 'desc2', 'columna': 2, 'design': None},
				{'field_name': 'desc3', 'columna': 2, 'design': None},
				{'field_name': 'desc4', 'columna': 2, 'design': None},
				{'field_name': 'desc5', 'columna': 2, 'design': None},
			],
			'fila_3': [
				{'field_name': 'desc6', 'columna': 2, 'design': None},
				{'field_name': 'desc7', 'columna': 2, 'design': None},
				{'field_name': 'desc8', 'columna': 2, 'design': None},
				{'field_name': 'desc9', 'columna': 2, 'design': None},
				{'field_name': 'desc10', 'columna': 2, 'design': None},
			],
			'fila_4': [
				{'field_name': 'desc11', 'columna': 2, 'design': None},
				{'field_name': 'desc12', 'columna': 2, 'design': None},
				{'field_name': 'desc13', 'columna': 2, 'design': None},
				{'field_name': 'desc14', 'columna': 2, 'design': None},
				{'field_name': 'desc15', 'columna': 2, 'design': None},
			],
			'fila_5': [
				{'field_name': 'desc16', 'columna': 2, 'design': None},
				{'field_name': 'desc17', 'columna': 2, 'design': None},
				{'field_name': 'desc18', 'columna': 2, 'design': None},
				{'field_name': 'desc19', 'columna': 2, 'design': None},
				{'field_name': 'desc20', 'columna': 2, 'design': None},
			],
			'fila_6': [
				{'field_name': 'desc21', 'columna': 2, 'design': None},
				{'field_name': 'desc22', 'columna': 2, 'design': None},
				{'field_name': 'desc23', 'columna': 2, 'design': None},
				{'field_name': 'desc24', 'columna': 2, 'design': None},
				{'field_name': 'desc25', 'columna': 2, 'design': None},
			],
		}
	},	
}

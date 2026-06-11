// Selección del Cliente desde buscar_cliente
const buscarClienteInput = document.getElementById('buscar_cliente');
buscarClienteInput.addEventListener('blur', function () {
	let busqueda = buscarClienteInput.value.trim();
	
	// alert("Aquí es");
	
	// Si está vacío, no hacer nada
	if (!busqueda) return;
	
	// Verificar que solo contenga números
	if (!/^\d+$/.test(busqueda)) {
		alert("Solo se permiten valores numéricos enteros.");
		buscarClienteInput.value = '';
		buscarClienteInput.focus();
		return;
	}
	
	// Construir la URL para la búsqueda
	const url = new URL('/ventas/buscar/cliente/', window.location.origin);
	url.searchParams.append('busqueda', busqueda);
	
	fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
		},
	})
	.then(response => response.json())
	.then(data => {
		if (data.error) {
			alert(data.error);
			buscarClienteInput.value = '';
			buscarClienteInput.focus();
		} else {
			// Verificar primero si el cliente está en blacklist
			if (data.black_list) {
				alert(`🚨 CLIENTE EN LISTA NEGRA 🚨\nMotivo: ${data.black_list_motivo || 'No especificado'}`);
				buscarClienteInput.value = '';
				buscarClienteInput.focus();
				return;
			}

			///-
			// VERIFICAR NOTA DE CRÉDITO (NCR)
			if (esNotaCredito()) {
				// CASO 1: Nota de Crédito
				mostrarModalAutorizacionNc(data, function(autorizada) {
					if (autorizada) {
						completarDatosCliente(data);  // ✅ Siempre completar datos
					} else {
						// Canceló - limpiar
						alert("No autorizó!");
						buscarClienteInput.value = '';
						buscarClienteInput.focus();
						document.getElementById('id_id_cliente').value = '';
						return;
					}
				});
			} else {
				alert("No es nota de Crédito!");
			}
			///-
			
			// Validar vencimientos de documentos
			const clienteId = data.id_cliente;
			if (clienteId) {
				fetch(`/ventas/clientes/${clienteId}/validar-vencimientos/`)
				.then(response => response.json())
				.then(vencimientoData => {
					///
					// Limpiar el campo buscar_cliente cuando se cierra el modal (ya sea por cancelar o por X)
					const modalElement = document.getElementById('autorizacionModal');
					modalElement.addEventListener('hidden.bs.modal', function () {
						// Limpiar el campo de búsqueda de cliente
						const buscarClienteInput = document.getElementById('buscar_cliente');
						if (buscarClienteInput) {
							buscarClienteInput.value = '';
							buscarClienteInput.focus();
						}
						
						// Limpiar también el campo oculto id_cliente por si acaso
						const idClienteInput = document.getElementById('id_id_cliente');
						if (idClienteInput) {
							idClienteInput.value = '';
						}
						
						// Limpiar campos del modal para la próxima vez
						document.getElementById('codigoAutorizacion').value = '';
						document.getElementById('mensajeErrorAutorizacion').style.display = 'none';
					});								
					///
					if (vencimientoData.requiere_autorizacion) {
						// ========== MODAL DE AUTORIZACIÓN ==========
						const autorizacionModal = new bootstrap.Modal(document.getElementById('autorizacionModal'));
						const datosComprobante = vencimientoData.datos_comprobante || {};
						
						// 1. Actualizar título del modal
						document.getElementById('modalTitulo').innerHTML = `
							<i class="bi bi-exclamation-triangle-fill me-2"></i>
							Autorización Requerida - Documento Vencido
						`;
						
						// 2. Actualizar mensaje principal
						const mensajePrincipal = document.getElementById('mensajePrincipal');
						mensajePrincipal.innerHTML = `
							<div class="alert alert-warning mb-0">
								<i class="bi bi-clock-history me-2"></i>
								<strong>Cliente con documentos vencidos</strong><br>
								El cliente <strong>${data.nombre || data.nombre_cliente}</strong> tiene documentos pendientes que requieren autorización de un supervisor.
							</div>
						`;
						
						// 3. Llenar datos del comprobante en el modal
						document.getElementById('modalComprobante').textContent = 
							`${datosComprobante.tipo_comprobante || 'N/A'}-${datosComprobante.letra_comprobante || 'N/A'}`;
						document.getElementById('modalNumero').textContent = datosComprobante.numero_comprobante || 'N/A';
						document.getElementById('modalFecha').textContent = datosComprobante.fecha_comprobante || 'N/A';
						document.getElementById('modalDiasCredito').textContent = `${datosComprobante.dias_credito || 0} días`;
						document.getElementById('modalVencimiento').textContent = datosComprobante.fecha_vencimiento || 'N/A';
						
						const diasVencidos = datosComprobante.dias_vencidos || 0;
						const diasVencidosElement = document.getElementById('modalDiasVencidos');
						diasVencidosElement.textContent = `${diasVencidos} días`;
						if (diasVencidos > 0) {
							diasVencidosElement.classList.add('text-danger', 'fw-bold');
						}
						
						document.getElementById('modalMonto').textContent = 
							`$${(datosComprobante.monto_pendiente || 0).toLocaleString('es-AR', {minimumFractionDigits: 2})}`;
						document.getElementById('modalVendedor').textContent = datosComprobante.vendedor || 'No asignado';
						
						// 4. Guardar datos del cliente
						const clienteData = {
							id_cliente: data.id_cliente,
							cuit: data.cuit,
							nombre: data.nombre,
							direccion: data.direccion,
							movil: data.movil,
							email: data.email,
							id_vendedor: data.id_vendedor,
							nombre_vendedor: data.nombre_vendedor,
							tipo_venta: data.tipo_venta,
							condicion_venta: data.condicion_venta,
							discrimina_iva: data.discrimina_iva,
							vip: data.vip,
							id_sucursal: data.id_sucursal
						};
						
						// 5. Configurar botón de confirmación
						const btnConfirmar = document.getElementById('btnConfirmarAutorizacion');
						const nuevoBtnConfirmar = btnConfirmar.cloneNode(true);
						btnConfirmar.parentNode.replaceChild(nuevoBtnConfirmar, btnConfirmar);
						
						nuevoBtnConfirmar.onclick = function() {
							const codigo = document.getElementById('codigoAutorizacion').value.trim();
							
							if (!codigo) {
								document.getElementById('mensajeErrorAutorizacion').textContent = 'Ingrese el código de autorización';
								document.getElementById('mensajeErrorAutorizacion').style.display = 'block';
								return;
							}
							
							fetch('/ventas/valida-autorizacion/', {
								method: 'POST',
								headers: {
									'Content-Type': 'application/json',
									'X-CSRFToken': getCookie('csrftoken')
								},
								body: JSON.stringify({
									codigo: codigo,
									cliente_id: clienteData.id_cliente,
									sucursal_id: document.getElementById('id_id_sucursal').value,
									fecha_comprobante: document.getElementById('id_fecha_comprobante').value
								})
							})
							.then(response => response.json())
							.then(authData => {
								if (authData.valido) {
									document.getElementById('id_id_valida').value = authData.datos_autorizacion.codigo;
									autorizacionModal.hide();
									document.getElementById('codigoAutorizacion').value = '';
									document.getElementById('mensajeErrorAutorizacion').style.display = 'none';
									completarDatosCliente(clienteData);
								} else {
									document.getElementById('mensajeErrorAutorizacion').textContent = 
										authData.mensaje || 'Código de autorización incorrecto';
									document.getElementById('mensajeErrorAutorizacion').style.display = 'block';
								}
							})
							.catch(error => {
								console.error('Error:', error);
								document.getElementById('mensajeErrorAutorizacion').textContent = 'Error de conexión';
								document.getElementById('mensajeErrorAutorizacion').style.display = 'block';
							});
						};
						
						// 6. Limpiar y mostrar modal
						document.getElementById('codigoAutorizacion').value = '';
						document.getElementById('mensajeErrorAutorizacion').style.display = 'none';
						autorizacionModal.show();
						
						return; // ← IMPORTANTE: Salir para no ejecutar el else
						
					} else {
						// Continuar con el flujo normal si no hay vencimientos
						completarDatosCliente(data);
					}								

				})
				.catch(error => {
					console.error('Error validando vencimientos:', error);
					// Continuar con el flujo normal si hay error en la validación
					completarDatosCliente(data);
				});
			} else {
				completarDatosCliente(data);
			}
		}
	})
	.catch(error => {
		console.error('Error en la búsqueda:', error);
		alert("Hubo un error en la búsqueda.");
	});
	
	///
	// buscar_cliente
	///
	
	// Función para completar los datos del cliente (extraída para reutilización)
	function completarDatosCliente(data) {
		document.getElementById('id_id_cliente').value = data.id_cliente || '';
		document.getElementById('id_nombre_factura').value = data.nombre || '';
		document.getElementById('id_domicilio_factura').value = data.direccion || '';
		document.getElementById('id_cuit').value = data.cuit || '';
		document.getElementById('id_movil_factura').value = data.movil || '';
		document.getElementById('id_email_factura').value = data.email || '';
		document.getElementById('id_id_vendedor').value = data.id_vendedor || '';
		document.getElementById('id_vendedor_factura').value = data.nombre_vendedor || '';
		document.getElementById('id_tipo_venta').value = data.tipo_venta || '';
		document.getElementById('id_condicion_comprobante').value = data.condicion_venta || '';
		document.getElementById('id_discrimina_iva').checked = data.discrimina_iva;
		
		// Verificación de sucursal
		const id_sucursal_factura = document.getElementById('id_id_sucursal').value;
		if (data.id_sucursal !== id_sucursal_factura) {
			alert('Atención: El cliente pertenece a otra sucursal.');
		}
		
		// Verificación VIP
		if (data.vip) {
			alert("⚠️ Este es un Cliente VIP - Trato Especial ⚠️");
			document.getElementById('id_cliente_vip').value = "Cliente VIP"; 
		}
		
		// Deshabilitar botones
		document.getElementById('listar_agenda').disabled = true;
		document.getElementById('buscar_cliente').disabled = true;
		
		///
		calcularNumeroComprobante();
		///
	}
});
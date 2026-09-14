document.addEventListener('DOMContentLoaded', function () {
	const selectSucursal = document.getElementById('id_id_sucursal');
	const selectPuntoVenta = document.getElementById('id_id_punto_venta');
	const form = document.getElementById('usuario-form');
	
	if (!selectSucursal || !selectPuntoVenta || !form) return;
	
	const urlPuntosVenta = form.dataset.urlPuntosVenta;
	const valorInicial = selectPuntoVenta.value;
	
	function cargarPuntosVenta(sucursalId, valorPreseleccionado = null) {
		selectPuntoVenta.innerHTML = '<option value="">---------</option>';
		
		if (!sucursalId) return;
		
		fetch(`${urlPuntosVenta}?sucursal_id=${sucursalId}`)
			.then(response => response.json())
			.then(data => {
				data.puntos_venta.forEach(pv => {
					const option = document.createElement('option');
					option.value = pv.id;
					option.textContent = pv.texto;
					selectPuntoVenta.appendChild(option);
				});
				if (valorPreseleccionado) {
					selectPuntoVenta.value = valorPreseleccionado;
				}
			})
			.catch(error => console.error('Error al cargar puntos de venta:', error));
	}
	
	selectSucursal.addEventListener('change', function () {
		cargarPuntosVenta(this.value);
	});
	
	if (selectSucursal.value) {
		cargarPuntosVenta(selectSucursal.value, valorInicial);
	}
});
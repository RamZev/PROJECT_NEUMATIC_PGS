# \apps\maestros\urls.py
from django.urls import path

#-- Tablas
from .views.actividad_views import *
from .views.producto_deposito_views import *
from .views.producto_familia_views import *
from .views.producto_marca_views import *
from .views.producto_modelo_views import *
from .views.producto_cai_views import *
from .views.producto_minimo_views import *
from .views.producto_stock_views import *
from .views.producto_estado_views import *
from .views.comprobante_venta_views import *
from .views.comprobante_compra_views import *
from .views.moneda_views import *
from .views.provincia_views import *
from .views.localidad_views import *
from .views.tipo_documento_identidad_views import *
from .views.tipo_iva_views import *
from .views.alicuota_iva_views import *
from .views.tipo_percepcion_ib_views import *
from .views.tipo_retencion_ib_views import *
from .views.operario_views import *
from .views.medio_pago_views import *
from .views.punto_venta_views import *
from .views.banco_views import *
from .views.cuenta_banco_views import *
from .views.tarjeta_views import *
from .views.codigo_retencion_views import *
from .views.concepto_banco_views import *
from .views.marketing_origen_views import *
from .views.cai_estados_views import *
from .views.forma_pago_views import *
from .views.descuento_vendedor_views import *
from .views.descuento_revendedor_views import *

#-- Catálogos
from .views.cliente_views import *
from .views.proveedor_views import *
from .views.producto_views import *
from .views.cliente_views import *
from .views.vendedor_views import *
from .views.empresa_views import *
from .views.sucursal_views import *
from .views.parametro_views import *
from .views.numero_views import *
from .views.valida_views import *

#-- Otras rutas.
from .views.consulta_views_maestros import filtrar_localidad
from .views.consulta_views_maestros import verificar_codigo_postal
from utils.validator.validaciones import buscar_cuit_view, buscar_cliente_id_view
from .views.actualizar_producto_estado_views import ActualizarEstadosProductosView

urlpatterns = [
	#-- Tablas:
	#-- Actividad.
	path('actividad/', ActividadListView.as_view(), name='actividad_list'),
	path('actividad/nueva/', ActividadCreateView.as_view(), name='actividad_create'),
	path('actividad/<int:pk>/editar/', ActividadUpdateView.as_view(), name='actividad_update'),
	path('actividad/<int:pk>/eliminar/', ActividadDeleteView.as_view(), name='actividad_delete'),
	
	#-- ProductoDeposito.
	path('producto_deposito/', ProductoDepositoListView.as_view(), name='producto_deposito_list'),
	path('producto_deposito/nueva/', ProductoDepositoCreateView.as_view(), name='producto_deposito_create'),
	path('producto_deposito/<int:pk>/editar/', ProductoDepositoUpdateView.as_view(), name='producto_deposito_update'),
	path('producto_deposito/<int:pk>/eliminar/', ProductoDepositoDeleteView.as_view(), name='producto_deposito_delete'),
	
	#-- ProductoFamilia.
	path('producto_familia/', ProductoFamiliaListView.as_view(), name='producto_familia_list'),
	path('producto_familia/nueva/', ProductoFamiliaCreateView.as_view(), name='producto_familia_create'),
	path('producto_familia/<int:pk>/editar/', ProductoFamiliaUpdateView.as_view(), name='producto_familia_update'),
	path('producto_familia/<int:pk>/eliminar/', ProductoFamiliaDeleteView.as_view(), name='producto_familia_delete'),
	
	#-- ProductoMarca.
	path('producto_marca/', ProductoMarcaListView.as_view(), name='producto_marca_list'),
	path('producto_marca/nueva/', ProductoMarcaCreateView.as_view(), name='producto_marca_create'),
	path('producto_marca/<int:pk>/editar/', ProductoMarcaUpdateView.as_view(), name='producto_marca_update'),
	path('producto_marca/<int:pk>/eliminar/', ProductoMarcaDeleteView.as_view(), name='producto_marca_delete'),
	
	#-- ProductoModelo.
	path('producto_modelo/', ProductoModeloListView.as_view(), name='producto_modelo_list'),
	path('producto_modelo/nueva/', ProductoModeloCreateView.as_view(), name='producto_modelo_create'),
	path('producto_modelo/<int:pk>/editar/', ProductoModeloUpdateView.as_view(), name='producto_modelo_update'),
	path('producto_modelo/<int:pk>/eliminar/', ProductoModeloDeleteView.as_view(), name='producto_modelo_delete'),
 
	#-- ProductoCai.
	path('producto_cai/', ProductoCaiListView.as_view(), name='producto_cai_list'),
	path('producto_cai/nueva/', ProductoCaiCreateView.as_view(), name='producto_cai_create'),
	path('producto_cai/<int:pk>/editar/', ProductoCaiUpdateView.as_view(), name='producto_cai_update'),
	path('producto_cai/<int:pk>/eliminar/', ProductoCaiDeleteView.as_view(), name='producto_cai_delete'),
	
	#-- ProductoMinimo.
	path('producto_minimo/', ProductoMinimoListView.as_view(), name='producto_minimo_list'),
	path('producto_minimo/nueva/', ProductoMinimoCreateView.as_view(), name='producto_minimo_create'),
	path('producto_minimo/<int:pk>/editar/', ProductoMinimoUpdateView.as_view(), name='producto_minimo_update'),
	path('producto_minimo/<int:pk>/eliminar/', ProductoMinimoDeleteView.as_view(), name='producto_minimo_delete'),
	
	#-- ProductoStock.
	path('producto_stock/', ProductoStockListView.as_view(), name='producto_stock_list'),
	path('producto_stock/nueva/', ProductoStockCreateView.as_view(), name='producto_stock_create'),
	path('producto_stock/<int:pk>/editar/', ProductoStockUpdateView.as_view(), name='producto_stock_update'),
	path('producto_stock/<int:pk>/eliminar/', ProductoStockDeleteView.as_view(), name='producto_stock_delete'),
	
	#-- ProductoEstado.
	path('producto_estado/', ProductoestadoListView.as_view(), name='producto_estado_list'),
	path('producto_estado/nueva/', ProductoestadoCreateView.as_view(), name='producto_estado_create'),
	path('producto_estado/<int:pk>/editar/', ProductoestadoUpdateView.as_view(), name='producto_estado_update'),
	path('producto_estado/<int:pk>/eliminar/', ProductoestadoDeleteView.as_view(), name='producto_estado_delete'),
	
	#-- ComprobanteVenta.
	path('comprobante_venta/', ComprobanteVentaListView.as_view(), name='comprobante_venta_list'),
	path('comprobante_venta/nueva/', ComprobanteVentaCreateView.as_view(), name='comprobante_venta_create'),
	path('comprobante_venta/<int:pk>/editar/', ComprobanteVentaUpdateView.as_view(), name='comprobante_venta_update'),
	path('comprobante_venta/<int:pk>/eliminar/', ComprobanteVentaDeleteView.as_view(), name='comprobante_venta_delete'),
	
	#-- ComprobanteCompra.
	path('comprobante_compra/', ComprobantecompraListView.as_view(), name='comprobante_compra_list'),
	path('comprobante_compra/nueva/', ComprobantecompraCreateView.as_view(), name='comprobante_compra_create'),
	path('comprobante_compra/<int:pk>/editar/', ComprobantecompraUpdateView.as_view(), name='comprobante_compra_update'),
	path('comprobante_compra/<int:pk>/eliminar/', ComprobantecompraDeleteView.as_view(), name='comprobante_compra_delete'),
	
	#-- Moneda.
	path('moneda/', MonedaListView.as_view(), name='moneda_list'),
	path('moneda/nueva/', MonedaCreateView.as_view(), name='moneda_create'),
	path('moneda/<int:pk>/editar/', MonedaUpdateView.as_view(), name='moneda_update'),
	path('moneda/<int:pk>/eliminar/', MonedaDeleteView.as_view(), name='moneda_delete'),
	
	#-- Provincia.
	path('provincia/', ProvinciaListView.as_view(), name='provincia_list'),
	path('provincia/nueva/', ProvinciaCreateView.as_view(), name='provincia_create'),
	path('provincia/<int:pk>/editar/', ProvinciaUpdateView.as_view(), name='provincia_update'),
	path('provincia/<int:pk>/eliminar/', ProvinciaDeleteView.as_view(), name='provincia_delete'),
	
	#-- Localidad.
	path('localidad/', LocalidadListView.as_view(), name='localidad_list'),
	path('localidad/nueva/', LocalidadCreateView.as_view(), name='localidad_create'),
	path('localidad/<int:pk>/editar/', LocalidadUpdateView.as_view(), name='localidad_update'),
	path('localidad/<int:pk>/eliminar/', LocalidadDeleteView.as_view(), name='localidad_delete'),
	
	#-- TipoDocumentoIdentidad.
	path('tipo_documento_identidad/', TipoDocumentoIdentidadListView.as_view(), name='tipo_documento_identidad_list'),
	path('tipo_documento_identidad/nueva/', TipoDocumentoIdentidadCreateView.as_view(), name='tipo_documento_identidad_create'),
	path('tipo_documento_identidad/<int:pk>/editar/', TipoDocumentoIdentidadUpdateView.as_view(), name='tipo_documento_identidad_update'),
	path('tipo_documento_identidad/<int:pk>/eliminar/', TipoDocumentoIdentidadDeleteView.as_view(), name='tipo_documento_identidad_delete'),
	
	#-- TipoIva.
	path('tipo_iva/', TipoIvaListView.as_view(), name='tipo_iva_list'),
	path('tipo_iva/nueva/', TipoIvaCreateView.as_view(), name='tipo_iva_create'),
	path('tipo_iva/<int:pk>/editar/', TipoIvaUpdateView.as_view(), name='tipo_iva_update'),
	path('tipo_iva/<int:pk>/eliminar/', TipoIvaDeleteView.as_view(), name='tipo_iva_delete'),
	
	#-- AlicuotaIva.
	path('alicuota_iva/', AlicuotaIvaListView.as_view(), name='alicuota_iva_list'),
	path('alicuota_iva/nueva/', AlicuotaIvaCreateView.as_view(), name='alicuota_iva_create'),
	path('alicuota_iva/<int:pk>/editar/', AlicuotaIvaUpdateView.as_view(), name='alicuota_iva_update'),
	path('alicuota_iva/<int:pk>/eliminar/', AlicuotaIvaDeleteView.as_view(), name='alicuota_iva_delete'),
	
	#-- TipoPercepcionIb.
	path('tipo_percepcion_ib/', TipoPercepcionIbListView.as_view(), name='tipo_percepcion_ib_list'),
	path('tipo_percepcion_ib/nueva/', TipoPercepcionIbCreateView.as_view(), name='tipo_percepcion_ib_create'),
	path('tipo_percepcion_ib/<int:pk>/editar/', TipoPercepcionIbUpdateView.as_view(), name='tipo_percepcion_ib_update'),
	path('tipo_percepcion_ib/<int:pk>/eliminar/', TipoPercepcionIbDeleteView.as_view(), name='tipo_percepcion_ib_delete'),
	
	#-- TipoRetencionIb.
	path('tipo_retencion_ib/', TipoRetencionIbListView.as_view(), name='tipo_retencion_ib_list'),
	path('tipo_retencion_ib/nueva/', TipoRetencionIbCreateView.as_view(), name='tipo_retencion_ib_create'),
	path('tipo_retencion_ib/<int:pk>/editar/', TipoRetencionIbUpdateView.as_view(), name='tipo_retencion_ib_update'),
	path('tipo_retencion_ib/<int:pk>/eliminar/', TipoRetencionIbDeleteView.as_view(), name='tipo_retencion_ib_delete'),
	
	#-- Operario.
	path('operario/', OperarioListView.as_view(), name='operario_list'),
	path('operario/nueva/', OperarioCreateView.as_view(), name='operario_create'),
	path('operario/<int:pk>/editar/', OperarioUpdateView.as_view(), name='operario_update'),
	path('operario/<int:pk>/eliminar/', OperarioDeleteView.as_view(), name='operario_delete'),
	
	#-- Catálogos:
	#-- Cliente.
	path('cliente/', ClienteListView.as_view(), name='cliente_list'),
	path('cliente/nueva/', ClienteCreateView.as_view(), name='cliente_create'),
	path('cliente/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
	path('cliente/<int:pk>/eliminar/', ClienteDeleteView.as_view(), name='cliente_delete'),
	
	#-- Proveedor.
	path('proveedor/', ProveedorListView.as_view(), name='proveedor_list'),
	path('proveedor/nueva/', ProveedorCreateView.as_view(), name='proveedor_create'),
	path('proveedor/<int:pk>/editar/', ProveedorUpdateView.as_view(), name='proveedor_update'),
	path('proveedor/<int:pk>/eliminar/', ProveedorDeleteView.as_view(), name='proveedor_delete'),
	
	#-- Producto.
	path('producto/', ProductoListView.as_view(), name='producto_list'),
	path('producto/nueva/', ProductoCreateView.as_view(), name='producto_create'),
	path('producto/<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_update'),
	path('producto/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto_delete'),
	
	#-- Vendedor.
	path('vendedor/', VendedorListView.as_view(), name='vendedor_list'),
	path('vendedor/nueva/', VendedorCreateView.as_view(), name='vendedor_create'),
	path('vendedor/<int:pk>/editar/', VendedorUpdateView.as_view(), name='vendedor_update'),
	path('vendedor/<int:pk>/eliminar/', VendedorDeleteView.as_view(), name='vendedor_delete'),
	
	#-- Empresa.
	path('empresa/', EmpresaListView.as_view(), name='empresa_list'),
	path('empresa/nueva/', EmpresaCreateView.as_view(), name='empresa_create'),
	path('empresa/<int:pk>/editar/', EmpresaUpdateView.as_view(), name='empresa_update'),
	path('empresa/<int:pk>/eliminar/', EmpresaDeleteView.as_view(), name='empresa_delete'),
	
	#-- Sucursal.
	path('sucursal/', SucursalListView.as_view(), name='sucursal_list'),
	path('sucursal/nueva/', SucursalCreateView.as_view(), name='sucursal_create'),
	path('sucursal/<int:pk>/editar/', SucursalUpdateView.as_view(), name='sucursal_update'),
	path('sucursal/<int:pk>/eliminar/', SucursalDeleteView.as_view(), name='sucursal_delete'),
	
	#-- Parametro.
	path('parametro/', ParametroListView.as_view(), name='parametro_list'),
	path('parametro/nueva/', ParametroCreateView.as_view(), name='parametro_create'),
	path('parametro/<int:pk>/editar/', ParametroUpdateView.as_view(), name='parametro_update'),
	path('parametro/<int:pk>/eliminar/', ParametroDeleteView.as_view(), name='parametro_delete'),
	
	#-- Numero.
	path('numero/', NumeroListView.as_view(), name='numero_list'),
	path('numero/nueva/', NumeroCreateView.as_view(), name='numero_create'),
	path('numero/<int:pk>/editar/', NumeroUpdateView.as_view(), name='numero_update'),
	path('numero/<int:pk>/eliminar/', NumeroDeleteView.as_view(), name='numero_delete'),
	
	#-- MedioPago.
	path('medio_pago/', MedioPagoListView.as_view(), name='medio_pago_list'),
	path('medio_pago/nueva/', MedioPagoCreateView.as_view(), name='medio_pago_create'),
	path('medio_pago/<int:pk>/editar/', MedioPagoUpdateView.as_view(), name='medio_pago_update'),
	path('medio_pago/<int:pk>/eliminar/', MedioPagoDeleteView.as_view(), name='medio_pago_delete'),
	
	#-- PuntoVenta.
	path('punto_venta/', PuntoVentaListView.as_view(), name='punto_venta_list'),
	path('punto_venta/nueva/', PuntoVentaCreateView.as_view(), name='punto_venta_create'),
	path('punto_venta/<int:pk>/editar/', PuntoVentaUpdateView.as_view(), name='punto_venta_update'),
	path('punto_venta/<int:pk>/eliminar/', PuntoVentaDeleteView.as_view(), name='punto_venta_delete'),
	
	#-- Valida.
	path('valida/', ValidaListView.as_view(), name='valida_list'),
	path('valida/nueva/', ValidaCreateView.as_view(), name='valida_create'),
	path('valida/<int:pk>/editar/', ValidaUpdateView.as_view(), name='valida_update'),
	path('valida/<int:pk>/eliminar/', ValidaDeleteView.as_view(), name='valida_delete'),
	
	#-- Banco.
	path('banco/', BancoListView.as_view(), name='banco_list'),
	path('banco/nueva/', BancoCreateView.as_view(), name='banco_create'),
	path('banco/<int:pk>/editar/', BancoUpdateView.as_view(), name='banco_update'),
	path('banco/<int:pk>/eliminar/', BancoDeleteView.as_view(), name='banco_delete'),
	
	#-- Cuenta Banco.
	path('cuenta_banco/', CuentaBancoListView.as_view(), name='cuenta_banco_list'),
	path('cuenta_banco/nueva/', CuentaBancoCreateView.as_view(), name='cuenta_banco_create'),
	path('cuenta_banco/<int:pk>/editar/', CuentaBancoUpdateView.as_view(), name='cuenta_banco_update'),
	path('cuenta_banco/<int:pk>/eliminar/', CuentaBancoDeleteView.as_view(), name='cuenta_banco_delete'),
	
	#-- Tarjeta.
	path('tarjeta/', TarjetaListView.as_view(), name='tarjeta_list'),
	path('tarjeta/nueva/', TarjetaCreateView.as_view(), name='tarjeta_create'),
	path('tarjeta/<int:pk>/editar/', TarjetaUpdateView.as_view(), name='tarjeta_update'),
	path('tarjeta/<int:pk>/eliminar/', TarjetaDeleteView.as_view(), name='tarjeta_delete'),
	
	#-- Código de Retención.
	path('codigo_retencion/', CodigoRetencionListView.as_view(), name='codigo_retencion_list'),
	path('codigo_retencion/nueva/', CodigoRetencionCreateView.as_view(), name='codigo_retencion_create'),
	path('codigo_retencion/<int:pk>/editar/', CodigoRetencionUpdateView.as_view(), name='codigo_retencion_update'),
	path('codigo_retencion/<int:pk>/eliminar/', CodigoRetencionDeleteView.as_view(), name='codigo_retencion_delete'),
	
	#-- Concepto Banco.
	path('concepto_banco/', ConceptoBancoListView.as_view(), name='concepto_banco_list'),
	path('concepto_banco/nueva/', ConceptoBancoCreateView.as_view(), name='concepto_banco_create'),
	path('concepto_banco/<int:pk>/editar/', ConceptoBancoUpdateView.as_view(), name='concepto_banco_update'),
	path('concepto_banco/<int:pk>/eliminar/', ConceptoBancoDeleteView.as_view(), name='concepto_banco_delete'),
	
	#-- Marketing Origen.
	path('marketing_origen/', MarketingOrigenListView.as_view(), name='marketing_origen_list'),
	path('marketing_origen/nueva/', MarketingOrigenCreateView.as_view(), name='marketing_origen_create'),
	path('marketing_origen/<int:pk>/editar/', MarketingOrigenUpdateView.as_view(), name='marketing_origen_update'),
	path('marketing_origen/<int:pk>/eliminar/', MarketingOrigenDeleteView.as_view(), name='marketing_origen_delete'),
	
	#-- Cai Estados.
	path('cai-estados/', CaiEstadosListView.as_view(), name='cai_estados_list'),
	path('cai-estados/nueva/', CaiEstadosCreateView.as_view(), name='cai_estados_create'),
	path('cai-estados/<int:pk>/editar/', CaiEstadosUpdateView.as_view(), name='cai_estados_update'),
	path('cai-estados/<int:pk>/eliminar/', CaiEstadosDeleteView.as_view(), name='cai_estados_delete'),
	
	#-- FormaPago.
	path('forma_pago/', FormaPagoListView.as_view(), name='forma_pago_list'),
	path('forma_pago/nueva/', FormaPagoCreateView.as_view(), name='forma_pago_create'),
	path('forma_pago/<int:pk>/editar/', FormaPagoUpdateView.as_view(), name='forma_pago_update'),
	path('forma_pago/<int:pk>/eliminar/', FormaPagoDeleteView.as_view(), name='forma_pago_delete'),	
	
	#-- Descuento Vendedor.
	path('descuento_vendedor/', DescuentoVendedorListView.as_view(), name='descuento_vendedor_list'),
	path('descuento_vendedor/nueva/', DescuentoVendedorCreateView.as_view(), name='descuento_vendedor_create'),
	path('descuento_vendedor/<int:pk>/editar/', DescuentoVendedorUpdateView.as_view(), name='descuento_vendedor_update'),
	path('descuento_vendedor/<int:pk>/eliminar/', DescuentoVendedorDeleteView.as_view(), name='descuento_vendedor_delete'),	

	#-- Descuento Revendedor.
	path('descuento_revendedor/', DescuentoRevendedorListView.as_view(), name='descuento_revendedor_list'),
	path('descuento_revendedor/nueva/', DescuentoRevendedorCreateView.as_view(), name='descuento_revendedor_create'),
	path('descuento_revendedor/<int:pk>/editar/', DescuentoRevendedorUpdateView.as_view(), name='descuento_revendedor_update'),
	path('descuento_revendedor/<int:pk>/eliminar/', DescuentoRevendedorDeleteView.as_view(), name='descuento_revendedor_delete'),	


	#-- Otras rutas.
	path('filtrar-localidad/', filtrar_localidad, name='filtrar_localidad'),
	path('verificar-codigo-postal/', verificar_codigo_postal, name='verificar_codigo_postal'),
	path('actualizar_minimo/', actualizar_minimo, name='actualizar_minimo'),
	path('buscar-cuit/', buscar_cuit_view, name='buscar_cuit'),
	path('buscar-cliente-id/', buscar_cliente_id_view, name='buscar_cliente_id'),
	path('api/cai/<int:pk>/datos/', CAIDatosAPIView.as_view(), name='cai-datos-api'),
	path('actualizar-estados-productos/', ActualizarEstadosProductosView.as_view(), name='actualizar_estados_productos'),
	path('get-descuentos-columna/<str:columna>/', get_descuentos_columna, name='get_descuentos_columna'),
	
	#-- URLs para carga de certificados.
	path('empresa/cargar-certificado/', CargarCertificadoView.as_view(), name='cargar_certificado'),
	path('empresa/cargar-clave/', CargarClaveView.as_view(), name='cargar_clave'),
]
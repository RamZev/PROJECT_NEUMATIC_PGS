# neumatic\apps\informes\urls.py
from django.urls import path

#-- Catálogos.
from .views.cliente_list_views import *
from .views.proveedor_list_views import *
from .views.producto_list_views import *
from .views.vendedor_list_views import *
from .views.sucursal_list_views import *

#-- Tablas.
from .views.actividad_list_views import *
from .views.productodeposito_list_views import *
from .views.productofamilia_list_views import *
from .views.productomarca_list_views import *
from .views.productomodelo_list_views import *
from .views.productocai_list_views import *
from .views.productoestado_list_views import *
from .views.comprobanteventa_list_views import *
from .views.comprobantecompra_list_views import *
from .views.moneda_list_views import *
from .views.provincia_list_views import *
from .views.localidad_list_views import *
from .views.tipodocumentoidentidad_list_views import *
from .views.tipoiva_list_views import *
from .views.alicuotaiva_list_views import *
from .views.tipopercepcionib_list_views import *
from .views.tiporetencionib_list_views import *
from .views.operario_list_views import *
from .views.mediopago_list_views import *
from .views.puntoventa_list_views import *
from .views.banco_list_views import *
from .views.cuentabanco_list_views import *
from .views.tarjeta_list_views import *
from .views.codigoretencion_list_views import *
from .views.conceptobanco_list_views import *
from .views.marketingorigen_list_views import *
from .views.vlproductominimo_list_views import *
from .views.descuentovendedor_list_views import *
from .views.descuentorevendedor_list_views import *
from .views.caiestados_list_views import *

#-- Procesos.
#- Lote 1:
from apps.informes.views.vlsaldosclientes_list_views import *
from apps.informes.views.vlresumenctacte_list_views import *
from apps.informes.views.vlmercaderiaporcliente_list_views import *
from apps.informes.views.vlremitosclientes_list_views import *
from apps.informes.views.vltotalremitosclientes_list_views import *
from apps.informes.views.vlventacomprolocalidad_list_views import *
from apps.informes.views.vlventamostrador_list_views import *
from apps.informes.views.vlventacompro_list_views import *

#- Lote 2:
from apps.informes.views.vlcomprobantesvencidos_list_views import *
from apps.informes.views.vlremitospendientes_list_views import *
from apps.informes.views.vlremitosvendedor_list_views import *
from apps.informes.views.vlivaventasfull_list_views import *
from apps.informes.views.vlivaventasprovincias_list_views import *
from apps.informes.views.vlivaventassitrib_list_views import *
from apps.informes.views.vlpercepibvendedortotales_list_views import *
from apps.informes.views.vlpercepibvendedordetallado_list_views import *
from apps.informes.views.vlpercepibsubcuentatotales_list_views import *
from apps.informes.views.vlpercepibsubcuentadetallado_list_views import *

#- Lote 3:
from apps.informes.views.vlcomisionvendedor_list_views import *
from apps.informes.views.vlcomisionoperario_list_views import *
from apps.informes.views.vlpreciodiferente_list_views import *
from apps.informes.views.vlventasresumenib_list_views import *

#- Lote 4:
from apps.informes.views.vlestadisticasventas_list_views import *
from apps.informes.views.vlestadisticasventasvendedor_list_views import *
from apps.informes.views.vlestadisticasventasprovincia_list_views import *
from apps.informes.views.vlestadisticasseguncondicion_list_views import *
from apps.informes.views.vlestadisticasventasmarca_list_views import *
from apps.informes.views.vlestadisticasventasmarcavendedor_list_views import *
from apps.informes.views.vlclienteultimaventa_list_views import *
from apps.informes.views.vlestadisticasventasvendedorcliente_list_views import *
from apps.informes.views.vlventasinestadistica_list_views import *
from apps.informes.views.vltabladinamicaventas_list_views import *
from apps.informes.views.vltabladinamicadetalleventas_list_views import *
from apps.informes.views.vltabladinamicaestadistica_list_views import *

#- Lote 5 (Stock):
from apps.informes.views.vllista_list_views import *
from apps.informes.views.vllistarevendedor_list_views import *
from apps.informes.views.vlstocksucursal_list_views import *
from apps.informes.views.vlstockgeneralsucursal_list_views import *
# from apps.informes.views.vlstockfecha_list_views import *
from apps.informes.views.vlstockunico_list_views import *
from apps.informes.views.vlreposicionstock_list_views import *
from apps.informes.views.vlmovimientointernostock_list_views import *
from apps.informes.views.vlstockcliente_list_views import *
from apps.informes.views.vlstockdeposito_list_views import *
from apps.informes.views.vlfichaseguimientostock_list_views import *

#- Lote 6 (Compras):
from apps.informes.views.vldetallecompraproveedor_list_views import *
from apps.informes.views.vlcompraingresada_list_views import *

#- Lote 7 (Caja):
from apps.informes.views.chequerecibo_list_views import *
from apps.informes.views.detallecupones_list_views import *
from apps.informes.views.cuponesfecha_list_views import *
from apps.informes.views.egresoscaja_list_views import *
from apps.informes.views.cajaarqueo_list_views import *
from apps.informes.views.detallecomprobantes_list_views import *
from apps.informes.views.planillacaja_list_views import *
from apps.informes.views.chequesfecha_list_views import *


#-- Otras rutas.
from apps.maestros.views.consulta_views_maestros import filtrar_localidad
from apps.informes.views.consultas_informes_views import *

urlpatterns = [
	#-- Catálogos.
	#-- Clientes.
	path('cliente_informe/', ClienteInformeView.as_view(), 
		 name='cliente_informe_list'),
	path('cliente/vista-preliminar/', cliente_vista_pantalla, 
		 name="cliente_vista_pantalla"),
	path("cliente/vista-pdf/", cliente_vista_pdf, 
		 name="cliente_vista_pdf"),
	path("cliente/vista-excel/", cliente_vista_excel, 
		 name="cliente_vista_excel"),
	path("cliente/vista-csv/", cliente_vista_csv, 
		 name="cliente_vista_csv"),
	
	#-- Proveedores.
	path('proveedor_informe/', ProveedorInformeView.as_view(), 
		 name='proveedor_informe_list'),
	path('proveedor/vista-preliminar/', proveedor_vista_pantalla, 
		 name="proveedor_vista_pantalla"),
	path("proveedor/vista-pdf/", proveedor_vista_pdf, 
		 name="proveedor_vista_pdf"),
	path("proveedor/vista-excel/", proveedor_vista_excel, 
		 name="proveedor_vista_excel"),
	path("proveedor/vista-csv/", proveedor_vista_csv, 
		 name="proveedor_vista_csv"),
	
	#-- Productos.
	path('producto_informe/', ProductoInformeView.as_view(), 
		 name='producto_informe_list'),
	path('producto/vista-preliminar/', producto_vista_pantalla, 
		 name="producto_vista_pantalla"),
	path("producto/vista-pdf/", producto_vista_pdf, 
		 name="producto_vista_pdf"),
	path("producto/vista-excel/", producto_vista_excel, 
		 name="producto_vista_excel"),
	path("producto/vista-csv/", producto_vista_csv, 
		 name="producto_vista_csv"),
	
	#-- Vendedores.
	path('vendedor_informe/', VendedorInformeView.as_view(), 
		 name='vendedor_informe_list'),
	path('vendedor/vista-preliminar/', vendedor_vista_pantalla, 
		 name="vendedor_vista_pantalla"),
	path("vendedor/vista-pdf/", vendedor_vista_pdf, 
		 name="vendedor_vista_pdf"),
	path("vendedor/vista-excel/", vendedor_vista_excel, 
		 name="vendedor_vista_excel"),
	path("vendedor/vista-csv/", vendedor_vista_csv, 
		 name="vendedor_vista_csv"),
	
	# #-- Sucursales.
	path('sucursal_informe/', SucursalInformeView.as_view(), 
		 name='sucursal_informe_list'),
	path('sucursal/vista-preliminar/', sucursal_vista_pantalla, 
		 name="sucursal_vista_pantalla"),
	path("sucursal/vista-pdf/", sucursal_vista_pdf, 
		 name="sucursal_vista_pdf"),
	path("sucursal/vista-excel/", sucursal_vista_excel, 
		 name="sucursal_vista_excel"),
	path("sucursal/vista-csv/", sucursal_vista_csv, 
		 name="sucursal_vista_csv"),
	
	#-- Tablas.
	# #-- Actividades.
	path('actividad_informe/', ActividadInformeView.as_view(), 
		 name='actividad_informe_list'),
	path('actividad/vista-preliminar/', actividad_vista_pantalla, 
		 name="actividad_vista_pantalla"),
	path("actividad/vista-pdf/", actividad_vista_pdf, 
		 name="actividad_vista_pdf"),
	path("actividad/vista-excel/", actividad_vista_excel, 
		 name="actividad_vista_excel"),
	path("actividad/vista-csv/", actividad_vista_csv, 
		 name="actividad_vista_csv"),
	
	#-- Producto Depósitos.
	path('productodeposito_informe/', ProductoDepositoInformeView.as_view(), 
		 name='productodeposito_informe_list'),
	path('productodeposito/vista-preliminar/', productodeposito_vista_pantalla, 
		 name="productodeposito_vista_pantalla"),
	path("productodeposito/vista-pdf/", productodeposito_vista_pdf, 
		 name="productodeposito_vista_pdf"),
	path("productodeposito/vista-excel/", productodeposito_vista_excel, 
		 name="productodeposito_vista_excel"),
	path("productodeposito/vista-csv/", productodeposito_vista_csv, 
		 name="productodeposito_vista_csv"),
	
	#-- Producto Familia.
	path('productofamilia_informe/', ProductoFamiliaInformeView.as_view(), 
		 name='productofamilia_informe_list'),
	path('productofamilia/vista-preliminar/', productofamilia_vista_pantalla, 
		 name="productofamilia_vista_pantalla"),
	path("productofamilia/vista-pdf/", productofamilia_vista_pdf, 
		 name="productofamilia_vista_pdf"),
	path("productofamilia/vista-excel/", productofamilia_vista_excel, 
		 name="productofamilia_vista_excel"),
	path("productofamilia/vista-csv/", productofamilia_vista_csv, 
		 name="productofamilia_vista_csv"),
	
	#-- Producto Marca.
	path('productomarca_informe/', ProductoMarcaInformeView.as_view(), 
		 name='productomarca_informe_list'),
	path('productomarca/vista-preliminar/', productomarca_vista_pantalla, 
		 name="productomarca_vista_pantalla"),
	path("productomarca/vista-pdf/", productomarca_vista_pdf, 
		 name="productomarca_vista_pdf"),
	path("productomarca/vista-excel/", productomarca_vista_excel, 
		 name="productomarca_vista_excel"),
	path("productomarca/vista-csv/", productomarca_vista_csv, 
		 name="productomarca_vista_csv"),
	
	#-- Producto Modelo.
	path('productomodelo_informe/', ProductoModeloInformeView.as_view(), 
		 name='productomodelo_informe_list'),
	path('productomodelo/vista-preliminar/', productomodelo_vista_pantalla, 
		 name="productomodelo_vista_pantalla"),
	path("productomodelo/vista-pdf/", productomodelo_vista_pdf, 
		 name="productomodelo_vista_pdf"),
	path("productomodelo/vista-excel/", productomodelo_vista_excel, 
		 name="productomodelo_vista_excel"),
	path("productomodelo/vista-csv/", productomodelo_vista_csv, 
		 name="productomodelo_vista_csv"),
	
	#-- Producto CAI.
	path('productocai_informe/', ProductoCaiInformeView.as_view(), 
		 name='productocai_informe_list'),
	path('productocai/vista-preliminar/', productocai_vista_pantalla, 
		 name="productocai_vista_pantalla"),
	path("productocai/vista-pdf/", productocai_vista_pdf, 
		 name="productocai_vista_pdf"),
	path("productocai/vista-excel/", productocai_vista_excel, 
		 name="productocai_vista_excel"),
	path("productocai/vista-csv/", productocai_vista_csv, 
		 name="productocai_vista_csv"),
	
	#-- Producto Estado.
	path('productoestado_informe/', ProductoEstadoInformeView.as_view(), 
		 name='productoestado_informe_list'),
	path('productoestado/vista-preliminar/', productoestado_vista_pantalla, 
		 name="productoestado_vista_pantalla"),
	path("productoestado/vista-pdf/", productoestado_vista_pdf, 
		 name="productoestado_vista_pdf"),
	path("productoestado/vista-excel/", productoestado_vista_excel, 
		 name="productoestado_vista_excel"),
	path("productoestado/vista-csv/", productoestado_vista_csv, 
		 name="productoestado_vista_csv"),
	
	#-- Comprobante Venta.
	path('comprobanteventa_informe/', ComprobanteVentaInformeView.as_view(), 
		 name='comprobanteventa_informe_list'),
	path('comprobanteventa/vista-preliminar/', comprobanteventa_vista_pantalla, 
		 name="comprobanteventa_vista_pantalla"),
	path("comprobanteventa/vista-pdf/", comprobanteventa_vista_pdf, 
		 name="comprobanteventa_vista_pdf"),
	path("comprobanteventa/vista-excel/", comprobanteventa_vista_excel, 
		 name="comprobanteventa_vista_excel"),
	path("comprobanteventa/vista-csv/", comprobanteventa_vista_csv, 
		 name="comprobanteventa_vista_csv"),
	
	#-- Comprobante Compra.
	path('comprobantecompra_informe/', ComprobanteCompraInformeView.as_view(), 
		 name='comprobantecompra_informe_list'),
	path('comprobantecompra/vista-preliminar/', comprobantecompra_vista_pantalla, 
		 name="comprobantecompra_vista_pantalla"),
	path("comprobantecompra/vista-pdf/", comprobantecompra_vista_pdf, 
		 name="comprobantecompra_vista_pdf"),
	path("comprobantecompra/vista-excel/", comprobantecompra_vista_excel, 
		 name="comprobantecompra_vista_excel"),
	path("comprobantecompra/vista-csv/", comprobantecompra_vista_csv, 
		 name="comprobantecompra_vista_csv"),
	
	#-- Moneda.
	path('moneda_informe/', MonedaInformeView.as_view(), 
		 name='moneda_informe_list'),
	path('moneda/vista-preliminar/', moneda_vista_pantalla, 
		 name="moneda_vista_pantalla"),
	path("moneda/vista-pdf/", moneda_vista_pdf, 
		 name="moneda_vista_pdf"),
	path("moneda/vista-excel/", moneda_vista_excel, 
		 name="moneda_vista_excel"),
	path("moneda/vista-csv/", moneda_vista_csv, 
		 name="moneda_vista_csv"),
	
	#-- Provincia.
	path('provincia_informe/', ProvinciaInformeView.as_view(), 
		 name='provincia_informe_list'),
	path('provincia/vista-preliminar/', provincia_vista_pantalla, 
		 name="provincia_vista_pantalla"),
	path("provincia/vista-pdf/", provincia_vista_pdf, 
		 name="provincia_vista_pdf"),
	path("provincia/vista-excel/", provincia_vista_excel, 
		 name="provincia_vista_excel"),
	path("provincia/vista-csv/", provincia_vista_csv, 
		 name="provincia_vista_csv"),
	
	#-- Localidades.
	path('localidad_informe/', LocalidadInformeView.as_view(), 
		 name='localidad_informe_list'),
	path('localidad/vista-preliminar/', localidad_vista_pantalla, 
		 name="localidad_vista_pantalla"),
	path("localidad/vista-pdf/", localidad_vista_pdf, 
		 name="localidad_vista_pdf"),
	path("localidad/vista-excel/", localidad_vista_excel, 
		 name="localidad_vista_excel"),
	path("localidad/vista-csv/", localidad_vista_csv, 
		 name="localidad_vista_csv"),
	
	#-- Tipo Documento Identidad.
	path('tipodocumentoidentidad_informe/', TipoDocumentoIdentidadInformeView.as_view(), 
		 name='tipodocumentoidentidad_informe_list'),
	path('tipodocumentoidentidad/vista-preliminar/', tipodocumentoidentidad_vista_pantalla, 
		 name="tipodocumentoidentidad_vista_pantalla"),
	path("tipodocumentoidentidad/vista-pdf/", tipodocumentoidentidad_vista_pdf, 
		 name="tipodocumentoidentidad_vista_pdf"),
	path("tipodocumentoidentidad/vista-excel/", tipodocumentoidentidad_vista_excel, 
		 name="tipodocumentoidentidad_vista_excel"),
	path("tipodocumentoidentidad/vista-csv/", tipodocumentoidentidad_vista_csv, 
		 name="tipodocumentoidentidad_vista_csv"),
	
	#-- Tipo IVA.
	path('tipoiva_informe/', TipoIvaInformeView.as_view(), 
		 name='tipoiva_informe_list'),
	path('tipoiva/vista-preliminar/', tipoiva_vista_pantalla, 
		 name="tipoiva_vista_pantalla"),
	path("tipoiva/vista-pdf/", tipoiva_vista_pdf, 
		 name="tipoiva_vista_pdf"),
	path("tipoiva/vista-excel/", tipoiva_vista_excel, 
		 name="tipoiva_vista_excel"),
	path("tipoiva/vista-csv/", tipoiva_vista_csv, 
		 name="tipoiva_vista_csv"),
	
	#-- Alícuota IVA.
	path('alicuotaiva_informe/', AlicuotaIvaInformeView.as_view(), 
		 name='alicuotaiva_informe_list'),
	path('alicuotaiva/vista-preliminar/', alicuotaiva_vista_pantalla, 
		 name="alicuotaiva_vista_pantalla"),
	path("alicuotaiva/vista-pdf/", alicuotaiva_vista_pdf, 
		 name="alicuotaiva_vista_pdf"),
	path("alicuotaiva/vista-excel/", alicuotaiva_vista_excel, 
		 name="alicuotaiva_vista_excel"),
	path("alicuotaiva/vista-csv/", alicuotaiva_vista_csv, 
		 name="alicuotaiva_vista_csv"),
	
	#-- Tipo Percepción Ib.
	path('tipopercepcionib_informe/', TipoPercepcionIbInformeView.as_view(), 
		 name='tipopercepcionib_informe_list'),
	path('tipopercepcionib/vista-preliminar/', tipopercepcionib_vista_pantalla, 
		 name="tipopercepcionib_vista_pantalla"),
	path("tipopercepcionib/vista-pdf/", tipopercepcionib_vista_pdf, 
		 name="tipopercepcionib_vista_pdf"),
	path("tipopercepcionib/vista-excel/", tipopercepcionib_vista_excel, 
		 name="tipopercepcionib_vista_excel"),
	path("tipopercepcionib/vista-csv/", tipopercepcionib_vista_csv, 
		 name="tipopercepcionib_vista_csv"),
	
	#-- Tipo Retención Ib.
	path('tiporetencionib_informe/', TipoRetencionIbInformeView.as_view(), 
		 name='tiporetencionib_informe_list'),
	path('tiporetencionib/vista-preliminar/', tiporetencionib_vista_pantalla, 
		 name="tiporetencionib_vista_pantalla"),
	path("tiporetencionib/vista-pdf/", tiporetencionib_vista_pdf, 
		 name="tiporetencionib_vista_pdf"),
	path("tiporetencionib/vista-excel/", tiporetencionib_vista_excel, 
		 name="tiporetencionib_vista_excel"),
	path("tiporetencionib/vista-csv/", tiporetencionib_vista_csv, 
		 name="tiporetencionib_vista_csv"),
	
	#-- Operario.
	path('operario_informe/', OperarioInformeView.as_view(), 
		 name='operario_informe_list'),
	path('operario/vista-preliminar/', operario_vista_pantalla, 
		 name="operario_vista_pantalla"),
	path("operario/vista-pdf/", operario_vista_pdf, 
		 name="operario_vista_pdf"),
	path("operario/vista-excel/", operario_vista_excel, 
		 name="operario_vista_excel"),
	path("operario/vista-csv/", operario_vista_csv, 
		 name="operario_vista_csv"),
	
	#-- Medio Pago.
	path('mediopago_informe/', MedioPagoInformeView.as_view(), 
		 name='mediopago_informe_list'),
	path('mediopago/vista-preliminar/', mediopago_vista_pantalla, 
		 name="mediopago_vista_pantalla"),
	path("mediopago/vista-pdf/", mediopago_vista_pdf, 
		 name="mediopago_vista_pdf"),
	path("mediopago/vista-excel/", mediopago_vista_excel, 
		 name="mediopago_vista_excel"),
	path("mediopago/vista-csv/", mediopago_vista_csv, 
		 name="mediopago_vista_csv"),
	
	#-- Punto Venta.
	path('puntoventa_informe/', PuntoVentaInformeView.as_view(), 
		 name='puntoventa_informe_list'),
	path('puntoventa/vista-preliminar/', puntoventa_vista_pantalla, 
		 name="puntoventa_vista_pantalla"),
	path("puntoventa/vista-pdf/", puntoventa_vista_pdf, 
		 name="puntoventa_vista_pdf"),
	path("puntoventa/vista-excel/", puntoventa_vista_excel, 
		 name="puntoventa_vista_excel"),
	path("puntoventa/vista-csv/", puntoventa_vista_csv, 
		 name="puntoventa_vista_csv"),
	
	#-- Banco.
	path('banco_informe/', BancoInformeView.as_view(), 
		 name='banco_informe_list'),
	path('banco/vista-preliminar/', banco_vista_pantalla, 
		 name="banco_vista_pantalla"),
	path("banco/vista-pdf/", banco_vista_pdf, 
		 name="banco_vista_pdf"),
	path("banco/vista-excel/", banco_vista_excel, 
		 name="banco_vista_excel"),
	path("banco/vista-csv/", banco_vista_csv, 
		 name="banco_vista_csv"),
	
	#-- Cuenta Banco.
	path('cuentabanco_informe/', CuentaBancoInformeView.as_view(), 
		 name='cuentabanco_informe_list'),
	path('cuentabanco/vista-preliminar/', cuentabanco_vista_pantalla, 
		 name="cuentabanco_vista_pantalla"),
	path("cuentabanco/vista-pdf/", cuentabanco_vista_pdf, 
		 name="cuentabanco_vista_pdf"),
	path("cuentabanco/vista-excel/", cuentabanco_vista_excel, 
		 name="cuentabanco_vista_excel"),
	path("cuentabanco/vista-csv/", cuentabanco_vista_csv, 
		 name="cuentabanco_vista_csv"),
	
	#-- Tarjeta.
	path('tarjeta_informe/', TarjetaInformeView.as_view(), 
		 name='tarjeta_informe_list'),
	path('tarjeta/vista-preliminar/', tarjeta_vista_pantalla, 
		 name="tarjeta_vista_pantalla"),
	path("tarjeta/vista-pdf/", tarjeta_vista_pdf, 
		 name="tarjeta_vista_pdf"),
	path("tarjeta/vista-excel/", tarjeta_vista_excel, 
		 name="tarjeta_vista_excel"),
	path("tarjeta/vista-csv/", tarjeta_vista_csv, 
		 name="tarjeta_vista_csv"),
	
	#-- Códigos de Retención.
	path('codigoretencion_informe/', CodigoRetencionInformeView.as_view(), 
		 name='codigoretencion_informe_list'),
	path('codigoretencion/vista-preliminar/', codigoretencion_vista_pantalla, 
		 name="codigoretencion_vista_pantalla"),
	path("codigoretencion/vista-pdf/", codigoretencion_vista_pdf, 
		 name="codigoretencion_vista_pdf"),
	path("codigoretencion/vista-excel/", codigoretencion_vista_excel, 
		 name="codigoretencion_vista_excel"),
	path("codigoretencion/vista-csv/", codigoretencion_vista_csv, 
		 name="codigoretencion_vista_csv"),
	
	#-- Conceptos de Banco.
	path('conceptobanco_informe/', ConceptoBancoInformeView.as_view(), 
		 name='conceptobanco_informe_list'),
	path('conceptobanco/vista-preliminar/', conceptobanco_vista_pantalla, 
		 name="conceptobanco_vista_pantalla"),
	path("conceptobanco/vista-pdf/", conceptobanco_vista_pdf, 
		 name="conceptobanco_vista_pdf"),
	path("conceptobanco/vista-excel/", conceptobanco_vista_excel, 
		 name="conceptobanco_vista_excel"),
	path("conceptobanco/vista-csv/", conceptobanco_vista_csv, 
		 name="conceptobanco_vista_csv"),
	
	#-- Marketing Origen.
	path('marketingorigen_informe/', MarketingOrigenInformeView.as_view(), 
		 name='marketingorigen_informe_list'),
	path('marketingorigen/vista-preliminar/', marketingorigen_vista_pantalla, 
		 name="marketingorigen_vista_pantalla"),
	path("marketingorigen/vista-pdf/", marketingorigen_vista_pdf, 
		 name="marketingorigen_vista_pdf"),
	path("marketingorigen/vista-excel/", marketingorigen_vista_excel, 
		 name="marketingorigen_vista_excel"),
	path("marketingorigen/vista-csv/", marketingorigen_vista_csv, 
		 name="marketingorigen_vista_csv"),
	
	#-- Producto Minimo.
	path('vlproductominimo_informe/', VLProductoMinimoInformeView.as_view(), 
		 name='vlproductominimo_informe_list'),
	path('vlproductominimo/vista-preliminar/', vlproductominimo_vista_pantalla, 
		 name="vlproductominimo_vista_pantalla"),
	path("vlproductominimo/vista-pdf/", vlproductominimo_vista_pdf, 
		 name="vlproductominimo_vista_pdf"),
	path("vlproductominimo/vista-excel/", vlproductominimo_vista_excel, 
		 name="vlproductominimo_vista_excel"),
	path("vlproductominimo/vista-csv/", vlproductominimo_vista_csv, 
		 name="vlproductominimo_vista_csv"),
	
	#-- Descuento Revendedor.
	path('descuentovendedor_informe/', DescuentoVendedorInformeView.as_view(), 
		 name='descuentovendedor_informe_list'),
	path('descuentovendedor/vista-preliminar/', descuentovendedor_vista_pantalla, 
		 name="descuentovendedor_vista_pantalla"),
	path("descuentovendedor/vista-pdf/", descuentovendedor_vista_pdf, 
		 name="descuentovendedor_vista_pdf"),
	path("descuentovendedor/vista-excel/", descuentovendedor_vista_excel, 
		 name="descuentovendedor_vista_excel"),
	path("descuentovendedor/vista-csv/", descuentovendedor_vista_csv, 
		 name="descuentovendedor_vista_csv"),
	
	#-- Descuento Revendedor.
	path('descuentorevendedor_informe/', DescuentoRevendedorInformeView.as_view(), 
		 name='descuentorevendedor_informe_list'),
	path('descuentorevendedor/vista-preliminar/', descuentorevendedor_vista_pantalla, 
		 name="descuentorevendedor_vista_pantalla"),
	path("descuentorevendedor/vista-pdf/", descuentorevendedor_vista_pdf, 
		 name="descuentorevendedor_vista_pdf"),
	path("descuentorevendedor/vista-excel/", descuentorevendedor_vista_excel, 
		 name="descuentorevendedor_vista_excel"),
	path("descuentorevendedor/vista-csv/", descuentorevendedor_vista_csv, 
		 name="descuentorevendedor_vista_csv"),
	
	#-- Cai Estados.
	path('caiestados_informe/', CaiEstadosInformeView.as_view(), 
		 name='caiestados_informe_list'),
	path('caiestados/vista-preliminar/', caiestados_vista_pantalla, 
		 name="caiestados_vista_pantalla"),
	path("caiestados/vista-pdf/", caiestados_vista_pdf, 
		 name="caiestados_vista_pdf"),
	path("caiestados/vista-excel/", caiestados_vista_excel, 
		 name="caiestados_vista_excel"),
	path("caiestados/vista-csv/", caiestados_vista_csv, 
		 name="caiestados_vista_csv"),
	
	#-- Informes-Procesos. --------------------------------------------------------
	
	#-- 1er. Lote.
	
	# #-- VL Saldos Clientes.
	path('vlsaldosclientes_informe/', VLSaldosClientesInformeView.as_view(), 
		 name='vlsaldosclientes_informe_list'),
	path('vlsaldosclientes/vista-preliminar/', vlsaldosclientes_vista_pantalla, 
		 name="vlsaldosclientes_vista_pantalla"),
	path("vlsaldosclientes/vista-pdf/", vlsaldosclientes_vista_pdf, 
		 name="vlsaldosclientes_vista_pdf"),
	path("vlsaldosclientes/vista-excel/", vlsaldosclientes_vista_excel, 
		 name="vlsaldosclientes_vista_excel"),
	path("vlsaldosclientes/vista-csv/", vlsaldosclientes_vista_csv, 
		 name="vlsaldosclientes_vista_csv"),
	
	#-- VL Resumen Cuenta Corriente.
	path('vlresumenctacte_informe/', VLResumenCtaCteInformeView.as_view(), 
		 name='vlresumenctacte_informe_list'),
	path('vlresumenctacte/vista-preliminar/', vlresumenctacte_vista_pantalla, 
		 name="vlresumenctacte_vista_pantalla"),
	path("vlresumenctacte/vista-pdf/", vlresumenctacte_vista_pdf, 
		 name="vlresumenctacte_vista_pdf"),	
	path("vlresumenctacte/vista-excel/", vlresumenctacte_vista_excel, 
		 name="vlresumenctacte_vista_excel"),
	path("vlresumenctacte/vista-csv/", vlresumenctacte_vista_csv, 
		 name="vlresumenctacte_vista_csv"),
	
	#-- VL Mercadería por Cliente.
	path('vlmercaderiaporcliente_informe/', VLMercaderiaPorClienteInformeView.as_view(), 
		 name='vlmercaderiaporcliente_informe_list'),
	path('vlmercaderiaporcliente/vista-preliminar/', vlmercaderiaporcliente_vista_pantalla, 
		 name="vlmercaderiaporcliente_vista_pantalla"),
	path("vlmercaderiaporcliente/vista-pdf/", vlmercaderiaporcliente_vista_pdf, 
		 name="vlmercaderiaporcliente_vista_pdf"),
	path("vlmercaderiaporcliente/vista-excel/", vlmercaderiaporcliente_vista_excel, 
		 name="vlmercaderiaporcliente_vista_excel"),
	path("vlmercaderiaporcliente/vista-csv/", vlmercaderiaporcliente_vista_csv, 
		 name="vlmercaderiaporcliente_vista_csv"),
	
	#-- VL Remitos por Cliente.
	path('vlremitosclientes_informe/', VLRemitosClientesInformeView.as_view(), 
		 name='vlremitosclientes_informe_list'),
	path('vlremitosclientes/vista-preliminar/', vlremitosclientes_vista_pantalla, 
		 name="vlremitosclientes_vista_pantalla"),
	path("vlremitosclientes/vista-pdf/", vlremitosclientes_vista_pdf, 
		 name="vlremitosclientes_vista_pdf"),
	path("vlremitosclientes/vista-excel/", vlremitosclientes_vista_excel, 
		 name="vlremitosclientes_vista_excel"),
	path("vlremitosclientes/vista-csv/", vlremitosclientes_vista_csv, 
		 name="vlremitosclientes_vista_csv"),
	
	#-- VL Total Remitos por Cliente.
	path('vltotalremitosclientes_informe/', VLTotalRemitosClientesInformeView.as_view(), 
		 name='vltotalremitosclientes_informe_list'),
	path('vltotalremitosclientes/vista-preliminar/', vltotalremitosclientes_vista_pantalla, 
		 name="vltotalremitosclientes_vista_pantalla"),
	path("vltotalremitosclientes/vista-pdf/", vltotalremitosclientes_vista_pdf, 
		 name="vltotalremitosclientes_vista_pdf"),
	path("vltotalremitosclientes/vista-excel/", vltotalremitosclientes_vista_excel, 
		 name="vltotalremitosclientes_vista_excel"),
	path("vltotalremitosclientes/vista-csv/", vltotalremitosclientes_vista_csv, 
		 name="vltotalremitosclientes_vista_csv"),
	
	#-- VL Venta Compro Localidad.
	path('vlventacomprolocalidad_informe/', VLVentaComproLocalidadInformeView.as_view(), 
		 name='vlventacomprolocalidad_informe_list'),
	path('vlventacomprolocalidad/vista-preliminar/', vlventacomprolocalidad_vista_pantalla, 
		 name="vlventacomprolocalidad_vista_pantalla"),
	path("vlventacomprolocalidad/vista-pdf/", vlventacomprolocalidad_vista_pdf, 
		 name="vlventacomprolocalidad_vista_pdf"),
	path("vlventacomprolocalidad/vista-excel/", vlventacomprolocalidad_vista_excel, 
		 name="vlventacomprolocalidad_vista_excel"),
	path("vlventacomprolocalidad/vista-csv/", vlventacomprolocalidad_vista_csv, 
		 name="vlventacomprolocalidad_vista_csv"),
	
	#-- VL Venta Mostrador.
	path('vlventamostrador_informe/', VLVentaMostradorInformeView.as_view(), 
		 name='vlventamostrador_informe_list'),
	path('vlventamostrador/vista-preliminar/', vlventamostrador_vista_pantalla, 
		 name="vlventamostrador_vista_pantalla"),
	path("vlventamostrador/vista-pdf/", vlventamostrador_vista_pdf, 
		 name="vlventamostrador_vista_pdf"),
	path("vlventamostrador/vista-excel/", vlventamostrador_vista_excel, 
		 name="vlventamostrador_vista_excel"),
	path("vlventamostrador/vista-csv/", vlventamostrador_vista_csv, 
		 name="vlventamostrador_vista_csv"),
	
	#-- VL Venta Compro.
	path('vlventacompro_informe/', VLVentaComproInformeView.as_view(), 
		 name='vlventacompro_informe_list'),
	path('vlventacompro/vista-preliminar/', vlventacompro_vista_pantalla, 
		 name="vlventacompro_vista_pantalla"),
	path("vlventacompro/vista-pdf/", vlventacompro_vista_pdf, 
		 name="vlventacompro_vista_pdf"),
	path("vlventacompro/vista-excel/", vlventacompro_vista_excel, 
		 name="vlventacompro_vista_excel"),
	path("vlventacompro/vista-csv/", vlventacompro_vista_csv, 
		 name="vlventacompro_vista_csv"),
	
	#-- 2do. Lote.
	
	#-- VL Comprobantes Vencidos.
	path('vlcomprobantesvencidos_informe/', VLComprobantesVencidosInformeView.as_view(), 
		 name='vlcomprobantesvencidos_informe_list'),
	path('vlcomprobantesvencidos/vista-preliminar/', vlcomprobantesvencidos_vista_pantalla, 
		 name="vlcomprobantesvencidos_vista_pantalla"),
	path("vlcomprobantesvencidos/vista-pdf/", vlcomprobantesvencidos_vista_pdf, 
		 name="vlcomprobantesvencidos_vista_pdf"),
	path("vlcomprobantesvencidos/vista-excel/", vlcomprobantesvencidos_vista_excel, 
		 name="vlcomprobantesvencidos_vista_excel"),
	path("vlcomprobantesvencidos/vista-csv/", vlcomprobantesvencidos_vista_csv, 
		 name="vlcomprobantesvencidos_vista_csv"),
	
	#-- VL Remitos Pendientes.
	path('vlremitospendientes_informe/', VLRemitosPendientesInformeView.as_view(), 
		 name='vlremitospendientes_informe_list'),
	path('vlremitospendientes/vista-preliminar/', vlremitospendientes_vista_pantalla, 
		 name="vlremitospendientes_vista_pantalla"),
	path("vlremitospendientes/vista-pdf/", vlremitospendientes_vista_pdf, 
		 name="vlremitospendientes_vista_pdf"),
	path("vlremitospendientes/vista-excel/", vlremitospendientes_vista_excel, 
		 name="vlremitospendientes_vista_excel"),
	path("vlremitospendientes/vista-csv/", vlremitospendientes_vista_csv, 
		 name="vlremitospendientes_vista_csv"),
	
	#-- VL Remitos por Vendedor.
	path('vlremitosvendedor_informe/', VLRemitosVendedorInformeView.as_view(), 
		 name='vlremitosvendedor_informe_list'),
	path('vlremitosvendedor/vista-preliminar/', vlremitosvendedor_vista_pantalla, 
		 name="vlremitosvendedor_vista_pantalla"),
	path("vlremitosvendedor/vista-pdf/", vlremitosvendedor_vista_pdf, 
		 name="vlremitosvendedor_vista_pdf"),
	path("vlremitosvendedor/vista-excel/", vlremitosvendedor_vista_excel, 
		 name="vlremitosvendedor_vista_excel"),
	path("vlremitosvendedor/vista-csv/", vlremitosvendedor_vista_csv, 
		 name="vlremitosvendedor_vista_csv"),
	
	#-- VL IVA Ventas FULL.
	path('vlivaventasfull_informe/', VLIVAVentasFULLInformeView.as_view(), 
		 name='vlivaventasfull_informe_list'),
	path('vlivaventasfull/vista-preliminar/', vlivaventasfull_vista_pantalla, 
		 name="vlivaventasfull_vista_pantalla"),
	path("vlivaventasfull/vista-pdf/", vlivaventasfull_vista_pdf, 
		 name="vlivaventasfull_vista_pdf"),
	path("vlivaventasfull/vista-excel/", vlivaventasfull_vista_excel, 
		 name="vlivaventasfull_vista_excel"),
	path("vlivaventasfull/vista-csv/", vlivaventasfull_vista_csv, 
		 name="vlivaventasfull_vista_csv"),
	
	#-- VL IVA Ventas - Totales por Provincias.
	path('vlivaventasprovincias_informe/', VLIVAVentasProvinciasInformeView.as_view(), 
		 name='vlivaventasprovincias_informe_list'),
	path('vlivaventasprovincias/vista-preliminar/', vlivaventasprovincias_vista_pantalla, 
		 name="vlivaventasprovincias_vista_pantalla"),
	path("vlivaventasprovincias/vista-pdf/", vlivaventasprovincias_vista_pdf, 
		 name="vlivaventasprovincias_vista_pdf"),
	path("vlivaventasprovincias/vista-excel/", vlivaventasprovincias_vista_excel, 
		 name="vlivaventasprovincias_vista_excel"),
	path("vlivaventasprovincias/vista-csv/", vlivaventasprovincias_vista_csv, 
		 name="vlivaventasprovincias_vista_csv"),
	
	#-- VL IVA Ventas - Totales para SITRIB.
	path('vlivaventassitrib_informe/', VLIVAVentasSitribInformeView.as_view(), 
		 name='vlivaventassitrib_informe_list'),
	path('vlivaventassitrib/vista-preliminar/', vlivaventassitrib_vista_pantalla, 
		 name="vlivaventassitrib_vista_pantalla"),
	path("vlivaventassitrib/vista-pdf/", vlivaventassitrib_vista_pdf, 
		 name="vlivaventassitrib_vista_pdf"),
	path("vlivaventassitrib/vista-excel/", vlivaventassitrib_vista_excel, 
		 name="vlivaventassitrib_vista_excel"),
	path("vlivaventassitrib/vista-csv/", vlivaventassitrib_vista_csv, 
		 name="vlivaventassitrib_vista_csv"),
	
	#-- VL Percep IB Vendedor - Totales.
	path('vlpercepibvendedortotales_informe/', VLPercepIBVendedorTotalesInformeView.as_view(), 
		 name='vlpercepibvendedortotales_informe_list'),
	path('vlpercepibvendedortotales/vista-preliminar/', vlpercepibvendedortotales_vista_pantalla, 
		 name="vlpercepibvendedortotales_vista_pantalla"),
	path("vlpercepibvendedortotales/vista-pdf/", vlpercepibvendedortotales_vista_pdf, 
		 name="vlpercepibvendedortotales_vista_pdf"),
	path("vlpercepibvendedortotales/vista-excel/", vlpercepibvendedortotales_vista_excel, 
		 name="vlpercepibvendedortotales_vista_excel"),
	path("vlpercepibvendedortotales/vista-csv/", vlpercepibvendedortotales_vista_csv, 
		 name="vlpercepibvendedortotales_vista_csv"),
	
	#-- VL Percep IB Vendedor - Detallado.
	path('vlpercepibvendedordetallado_informe/', VLPercepIBVendedorDetalladoInformeView.as_view(), 
		 name='vlpercepibvendedordetallado_informe_list'),
	path('vlpercepibvendedordetallado/vista-preliminar/', vlpercepibvendedordetallado_vista_pantalla, 
		 name="vlpercepibvendedordetallado_vista_pantalla"),
	path("vlpercepibvendedordetallado/vista-pdf/", vlpercepibvendedordetallado_vista_pdf, 
		 name="vlpercepibvendedordetallado_vista_pdf"),
	path("vlpercepibvendedordetallado/vista-excel/", vlpercepibvendedordetallado_vista_excel, 
		 name="vlpercepibvendedordetallado_vista_excel"),
	path("vlpercepibvendedordetallado/vista-csv/", vlpercepibvendedordetallado_vista_csv, 
		 name="vlpercepibvendedordetallado_vista_csv"),
	
	#-- VL Percep IB Subcuenta - Totales.
	path('vlpercepibsubcuentatotales_informe/', VLPercepIBSubcuentaTotalesInformeView.as_view(), 
		 name='vlpercepibsubcuentatotales_informe_list'),
	path('vlpercepibsubcuentatotales/vista-preliminar/', vlpercepibsubcuentatotales_vista_pantalla, 
		 name="vlpercepibsubcuentatotales_vista_pantalla"),
	path("vlpercepibsubcuentatotales/vista-pdf/", vlpercepibsubcuentatotales_vista_pdf, 
		 name="vlpercepibsubcuentatotales_vista_pdf"),
	path("vlpercepibsubcuentatotales/vista-excel/", vlpercepibsubcuentatotales_vista_excel, 
		 name="vlpercepibsubcuentatotales_vista_excel"),
	path("vlpercepibsubcuentatotales/vista-csv/", vlpercepibsubcuentatotales_vista_csv, 
		 name="vlpercepibsubcuentatotales_vista_csv"),
	
	#-- VL Percep IB Subcuenta - Detallado.
	path('vlpercepibsubcuentadetallado_informe/', VLPercepIBSubcuentaDetalladoInformeView.as_view(), 
		 name='vlpercepibsubcuentadetallado_informe_list'),
	path('vlpercepibsubcuentadetallado/vista-preliminar/', vlpercepibsubcuentadetallado_vista_pantalla, 
		 name="vlpercepibsubcuentadetallado_vista_pantalla"),
	path("vlpercepibsubcuentadetallado/vista-pdf/", vlpercepibsubcuentadetallado_vista_pdf, 
		 name="vlpercepibsubcuentadetallado_vista_pdf"),
	path("vlpercepibsubcuentadetallado/vista-excel/", vlpercepibsubcuentadetallado_vista_excel, 
		 name="vlpercepibsubcuentadetallado_vista_excel"),
	path("vlpercepibsubcuentadetallado/vista-csv/", vlpercepibsubcuentadetallado_vista_csv, 
		 name="vlpercepibsubcuentadetallado_vista_csv"),
	
	#-- 3er. Lote.
	
	#-- VL Comisión Vendedor.
	path('vlcomisionvendedor_informe/', VLComisionVendedorInformeView.as_view(), 
		 name='vlcomisionvendedor_informe_list'),
	path('vlcomisionvendedor/vista-preliminar/', vlcomisionvendedor_vista_pantalla, 
		 name="vlcomisionvendedor_vista_pantalla"),
	path("vlcomisionvendedor/vista-pdf/", vlcomisionvendedor_vista_pdf, 
		 name="vlcomisionvendedor_vista_pdf"),
	path("vlcomisionvendedor/vista-excel/", vlcomisionvendedor_vista_excel, 
		 name="vlcomisionvendedor_vista_excel"),
	path("vlcomisionvendedor/vista-csv/", vlcomisionvendedor_vista_csv, 
		 name="vlcomisionvendedor_vista_csv"),
	
	#-- VL Comisión Operario.
	path('vlcomisionoperario_informe/', VLComisionOperarioInformeView.as_view(), 
		 name='vlcomisionoperario_informe_list'),
	path('vlcomisionoperario/vista-preliminar/', vlcomisionoperario_vista_pantalla, 
		 name="vlcomisionoperario_vista_pantalla"),
	path("vlcomisionoperario/vista-pdf/", vlcomisionoperario_vista_pdf, 
		 name="vlcomisionoperario_vista_pdf"),
	path("vlcomisionoperario/vista-excel/", vlcomisionoperario_vista_excel, 
		 name="vlcomisionoperario_vista_excel"),
	path("vlcomisionoperario/vista-csv/", vlcomisionoperario_vista_csv, 
		 name="vlcomisionoperario_vista_csv"),
	
	#-- VL Precio Diferente.
	path('vlpreciodiferente_informe/', VLPrecioDiferenteInformeView.as_view(), 
		 name='vlpreciodiferente_informe_list'),
	path('vlpreciodiferente/vista-preliminar/', vlpreciodiferente_vista_pantalla, 
		 name="vlpreciodiferente_vista_pantalla"),
	path("vlpreciodiferente/vista-pdf/", vlpreciodiferente_vista_pdf, 
		 name="vlpreciodiferente_vista_pdf"),
	path("vlpreciodiferente/vista-excel/", vlpreciodiferente_vista_excel, 
		 name="vlpreciodiferente_vista_excel"),
	path("vlpreciodiferente/vista-csv/", vlpreciodiferente_vista_csv, 
		 name="vlpreciodiferente_vista_csv"),
	
	#-- VL Ventas Resumne IB.
	path('vlventasresumenib_informe/', VLVentasResumenIBInformeView.as_view(), 
		 name='vlventasresumenib_informe_list'),
	path('vlventasresumenib/vista-preliminar/', vlventasresumenib_vista_pantalla, 
		 name="vlventasresumenib_vista_pantalla"),
	path("vlventasresumenib/vista-pdf/", vlventasresumenib_vista_pdf, 
		 name="vlventasresumenib_vista_pdf"),
	path("vlventasresumenib/vista-excel/", vlventasresumenib_vista_excel, 
		 name="vlventasresumenib_vista_excel"),
	path("vlventasresumenib/vista-csv/", vlventasresumenib_vista_csv, 
		 name="vlventasresumenib_vista_csv"),
	
	#-- 4to. Lote.
	
	#-- VL Estadísticas de Ventas.
	path('vlestadisticasventas_informe/', VLEstadisticasVentasInformeView.as_view(), 
		 name='vlestadisticasventas_informe_list'),
	path('vlestadisticasventas/vista-preliminar/', vlestadisticasventas_vista_pantalla, 
		 name="vlestadisticasventas_vista_pantalla"),
	path("vlestadisticasventas/vista-pdf/", vlestadisticasventas_vista_pdf, 
		 name="vlestadisticasventas_vista_pdf"),
	path("vlestadisticasventas/vista-excel/", vlestadisticasventas_vista_excel, 
		 name="vlestadisticasventas_vista_excel"),
	path("vlestadisticasventas/vista-csv/", vlestadisticasventas_vista_csv, 
		 name="vlestadisticasventas_vista_csv"),
	
	#-- VL Estadísticas de Ventas Vendedor.
	path('vlestadisticasventasvendedor_informe/', VLEstadisticasVentasVendedorInformeView.as_view(), 
		 name='vlestadisticasventasvendedor_informe_list'),
	path('vlestadisticasventasvendedor/vista-preliminar/', vlestadisticasventasvendedor_vista_pantalla, 
		 name="vlestadisticasventasvendedor_vista_pantalla"),
	path("vlestadisticasventasvendedor/vista-pdf/", vlestadisticasventasvendedor_vista_pdf, 
		 name="vlestadisticasventasvendedor_vista_pdf"),
	path("vlestadisticasventasvendedor/vista-excel/", vlestadisticasventasvendedor_vista_excel, 
		 name="vlestadisticasventasvendedor_vista_excel"),
	path("vlestadisticasventasvendedor/vista-csv/", vlestadisticasventasvendedor_vista_csv, 
		 name="vlestadisticasventasvendedor_vista_csv"),
	
		#-- VL Estadísticas de Ventas Vendedor Cliente.
	path('vlestadisticasventasvendedorcliente_informe/', VLEstadisticasVentasVendedorClienteInformeView.as_view(), 
		 name='vlestadisticasventasvendedorcliente_informe_list'),
	path('vlestadisticasventasvendedorcliente/vista-preliminar/', vlestadisticasventasvendedorcliente_vista_pantalla, 
		 name="vlestadisticasventasvendedorcliente_vista_pantalla"),
	path("vlestadisticasventasvendedorcliente/vista-pdf/", vlestadisticasventasvendedorcliente_vista_pdf, 
		 name="vlestadisticasventasvendedorcliente_vista_pdf"),
	path("vlestadisticasventasvendedorcliente/vista-excel/", vlestadisticasventasvendedorcliente_vista_excel, 
		 name="vlestadisticasventasvendedorcliente_vista_excel"),
	path("vlestadisticasventasvendedorcliente/vista-csv/", vlestadisticasventasvendedorcliente_vista_csv, 
		 name="vlestadisticasventasvendedorcliente_vista_csv"),
	
	#-- VL Estadísticas Según Condición.
	path('vlestadisticasseguncondicion_informe/', VLEstadisticasSegunCondicionInformeView.as_view(), 
		 name='vlestadisticasseguncondicion_informe_list'),
	path('vlestadisticasseguncondicion/vista-preliminar/', vlestadisticasseguncondicion_vista_pantalla, 
		 name="vlestadisticasseguncondicion_vista_pantalla"),
	path("vlestadisticasseguncondicion/vista-pdf/", vlestadisticasseguncondicion_vista_pdf, 
		 name="vlestadisticasseguncondicion_vista_pdf"),
	path("vlestadisticasseguncondicion/vista-excel/", vlestadisticasseguncondicion_vista_excel, 
		 name="vlestadisticasseguncondicion_vista_excel"),
	path("vlestadisticasseguncondicion/vista-csv/", vlestadisticasseguncondicion_vista_csv, 
		 name="vlestadisticasseguncondicion_vista_csv"),
	
	#-- VL Estadísticas de Ventas Marca.
	path('vlestadisticasventasmarca_informe/', VLEstadisticasVentasMarcaInformeView.as_view(), 
		 name='vlestadisticasventasmarca_informe_list'),
	path('vlestadisticasventasmarca/vista-preliminar/', vlestadisticasventasmarca_vista_pantalla, 
		 name="vlestadisticasventasmarca_vista_pantalla"),
	path("vlestadisticasventasmarca/vista-pdf/", vlestadisticasventasmarca_vista_pdf, 
		 name="vlestadisticasventasmarca_vista_pdf"),
	path("vlestadisticasventasmarca/vista-excel/", vlestadisticasventasmarca_vista_excel, 
		 name="vlestadisticasventasmarca_vista_excel"),
	path("vlestadisticasventasmarca/vista-csv/", vlestadisticasventasmarca_vista_csv, 
		 name="vlestadisticasventasmarca_vista_csv"),
	
	#-- VL Estadísticas de Ventas Marca Vendedor.
	path('vlestadisticasventasmarcavendedor_informe/', VLEstadisticasVentasMarcaVendedorInformeView.as_view(), 
		 name='vlestadisticasventasmarcavendedor_informe_list'),
	path('vlestadisticasventasmarcavendedor/vista-preliminar/', vlestadisticasventasmarcavendedor_vista_pantalla, 
		 name="vlestadisticasventasmarcavendedor_vista_pantalla"),
	path("vlestadisticasventasmarcavendedor/vista-pdf/", vlestadisticasventasmarcavendedor_vista_pdf, 
		 name="vlestadisticasventasmarcavendedor_vista_pdf"),
	path("vlestadisticasventasmarcavendedor/vista-excel/", vlestadisticasventasmarcavendedor_vista_excel, 
		 name="vlestadisticasventasmarcavendedor_vista_excel"),
	path("vlestadisticasventasmarcavendedor/vista-csv/", vlestadisticasventasmarcavendedor_vista_csv, 
		 name="vlestadisticasventasmarcavendedor_vista_csv"),
	
	#-- VL Estadísticas de Clientes sin Ventas.
	path('vlclienteultimaventa_informe/', VLClienteUltimaVentaInformeView.as_view(), 
		 name='vlclienteultimaventa_informe_list'),
	path('vlclienteultimaventa/vista-preliminar/', vlclienteultimaventa_vista_pantalla, 
		 name="vlclienteultimaventa_vista_pantalla"),
	path("vlclienteultimaventa/vista-pdf/", vlclienteultimaventa_vista_pdf, 
		 name="vlclienteultimaventa_vista_pdf"),
	path("vlclienteultimaventa/vista-excel/", vlclienteultimaventa_vista_excel, 
		 name="vlclienteultimaventa_vista_excel"),
	path("vlclienteultimaventa/vista-csv/", vlclienteultimaventa_vista_csv, 
		 name="vlclienteultimaventa_vista_csv"),
	
	#-- VL Estadísticas de Ventas Provincia.
	path('vlestadisticasventasprovincia_informe/', VLEstadisticasVentasProvinciaInformeView.as_view(), 
		 name='vlestadisticasventasprovincia_informe_list'),
	path('vlestadisticasventasprovincia/vista-preliminar/', vlestadisticasventasprovincia_vista_pantalla, 
		 name="vlestadisticasventasprovincia_vista_pantalla"),
	path("vlestadisticasventasprovincia/vista-pdf/", vlestadisticasventasprovincia_vista_pdf, 
		 name="vlestadisticasventasprovincia_vista_pdf"),
	path("vlestadisticasventasprovincia/vista-excel/", vlestadisticasventasprovincia_vista_excel, 
		 name="vlestadisticasventasprovincia_vista_excel"),
	path("vlestadisticasventasprovincia/vista-csv/", vlestadisticasventasprovincia_vista_csv, 
		 name="vlestadisticasventasprovincia_vista_csv"),
	
	#-- VL Venta sin Estadística.
	path('vlventasinestadistica_informe/', VLVentaSinEstadisticaInformeView.as_view(), 
		 name='vlventasinestadistica_informe_list'),
	path('vlventasinestadistica/vista-preliminar/', vlventasinestadistica_vista_pantalla, 
		 name="vlventasinestadistica_vista_pantalla"),
	path("vlventasinestadistica/vista-pdf/", vlventasinestadistica_vista_pdf, 
		 name="vlventasinestadistica_vista_pdf"),
	path("vlventasinestadistica/vista-excel/", vlventasinestadistica_vista_excel, 
		 name="vlventasinestadistica_vista_excel"),
	path("vlventasinestadistica/vista-csv/", vlventasinestadistica_vista_csv, 
		 name="vlventasinestadistica_vista_csv"),
	
	#-- VL Tablas Dinámicas de Ventas - Ventas por Comprobantes.
	path('vltabladinamicaventas_informe/', VLTablaDinamicaVentasInformeView.as_view(), 
		 name='vltabladinamicaventas_informe_list'),
	path('vltabladinamicaventas/vista-preliminar/', vltabladinamicaventas_vista_pantalla, 
		 name="vltabladinamicaventas_vista_pantalla"),
	path("vltabladinamicaventas/vista-pdf/", vltabladinamicaventas_vista_pdf, 
		 name="vltabladinamicaventas_vista_pdf"),
	path("vltabladinamicaventas/vista-excel/", vltabladinamicaventas_vista_excel, 
		 name="vltabladinamicaventas_vista_excel"),
	path("vltabladinamicaventas/vista-csv/", vltabladinamicaventas_vista_csv, 
		 name="vltabladinamicaventas_vista_csv"),
	
	#-- VL Tablas Dinámicas de Ventas - Detalle de Ventas por Productos.
	path('vltabladinamicadetalleventas_informe/', VLTablaDinamicaDetalleVentasInformeView.as_view(), 
		 name='vltabladinamicadetalleventas_informe_list'),
	path('vltabladinamicadetalleventas/vista-preliminar/', vltabladinamicadetalleventas_vista_pantalla, 
		 name="vltabladinamicadetalleventas_vista_pantalla"),
	path("vltabladinamicadetalleventas/vista-pdf/", vltabladinamicadetalleventas_vista_pdf, 
		 name="vltabladinamicadetalleventas_vista_pdf"),
	path("vltabladinamicadetalleventas/vista-excel/", vltabladinamicadetalleventas_vista_excel, 
		 name="vltabladinamicadetalleventas_vista_excel"),
	path("vltabladinamicadetalleventas/vista-csv/", vltabladinamicadetalleventas_vista_csv, 
		 name="vltabladinamicadetalleventas_vista_csv"),
	
	#-- VL Tablas Dinámicas de Ventas - Tablas para Estadísticas.
	path('vltabladinamicaestadistica_informe/', VLTablaDinamicaEstadisticaInformeView.as_view(), 
		 name='vltabladinamicaestadistica_informe_list'),
	path('vltabladinamicaestadistica/vista-preliminar/', vltabladinamicaestadistica_vista_pantalla, 
		 name="vltabladinamicaestadistica_vista_pantalla"),
	path("vltabladinamicaestadistica/vista-pdf/", vltabladinamicaestadistica_vista_pdf, 
		 name="vltabladinamicaestadistica_vista_pdf"),
	path("vltabladinamicaestadistica/vista-excel/", vltabladinamicaestadistica_vista_excel, 
		 name="vltabladinamicaestadistica_vista_excel"),
	path("vltabladinamicaestadistica/vista-csv/", vltabladinamicaestadistica_vista_csv, 
		 name="vltabladinamicaestadistica_vista_csv"),
	
	#-- 5to. Lote (Stock).
	
	#-- VL Lista de Precios.
	path('vllista_informe/', VLListaInformeView.as_view(), 
		 name='vllista_informe_list'),
	path('vllista/vista-preliminar/', vllista_vista_pantalla, 
		 name="vllista_vista_pantalla"),
	path("vllista/vista-pdf/", vllista_vista_pdf, 
		 name="vllista_vista_pdf"),
	path("vllista/vista-excel/", vllista_vista_excel, 
		 name="vllista_vista_excel"),
	path("vllista/vista-csv/", vllista_vista_csv, 
		 name="vllista_vista_csv"),
	
	#-- VL Lista de Precios a Revendedores.
	path('vllistarevendedor_informe/', VLListaRevendedorInformeView.as_view(), 
		 name='vllistarevendedor_informe_list'),
	path('vllistarevendedor/vista-preliminar/', vllistarevendedor_vista_pantalla, 
		 name="vllistarevendedor_vista_pantalla"),
	path("vllistarevendedor/vista-pdf/", vllistarevendedor_vista_pdf, 
		 name="vllistarevendedor_vista_pdf"),
	path("vllistarevendedor/vista-excel/", vllistarevendedor_vista_excel, 
		 name="vllistarevendedor_vista_excel"),
	path("vllistarevendedor/vista-csv/", vllistarevendedor_vista_csv, 
		 name="vllistarevendedor_vista_csv"),
	
	#-- VL Listado de Stock por Sucursal.
	path('vlstocksucursal_informe/', VLStockSucursalInformeView.as_view(), 
		 name='vlstocksucursal_informe_list'),
	path('vlstocksucursal/vista-preliminar/', vlstocksucursal_vista_pantalla, 
		 name="vlstocksucursal_vista_pantalla"),
	path("vlstocksucursal/vista-pdf/", vlstocksucursal_vista_pdf, 
		 name="vlstocksucursal_vista_pdf"),
	path("vlstocksucursal/vista-excel/", vlstocksucursal_vista_excel, 
		 name="vlstocksucursal_vista_excel"),
	path("vlstocksucursal/vista-csv/", vlstocksucursal_vista_csv, 
		 name="vlstocksucursal_vista_csv"),
	
	#-- VL Stock General por Sucursal.
	path('vlstockgeneralsucursal_informe/', VLStockGeneralSucursalInformeView.as_view(), 
		 name='vlstockgeneralsucursal_informe_list'),
	path('vlstockgeneralsucursal/vista-preliminar/', vlstockgeneralsucursal_vista_pantalla, 
		 name="vlstockgeneralsucursal_vista_pantalla"),
	path("vlstockgeneralsucursal/vista-pdf/", vlstockgeneralsucursal_vista_pdf, 
		 name="vlstockgeneralsucursal_vista_pdf"),
	path("vlstockgeneralsucursal/vista-excel/", vlstockgeneralsucursal_vista_excel, 
		 name="vlstockgeneralsucursal_vista_excel"),
	path("vlstockgeneralsucursal/vista-csv/", vlstockgeneralsucursal_vista_csv, 
		 name="vlstockgeneralsucursal_vista_csv"),
	
	# #-- VL Listado Stock a Fecha.
	# path('vlstockfecha_informe/', VLStockFechaInformeView.as_view(), 
	# 	 name='vlstockfecha_informe_list'),
	# path('vlstockfecha/vista-preliminar/', vlstockfecha_vista_pantalla, 
	# 	 name="vlstockfecha_vista_pantalla"),
	# path("vlstockfecha/vista-pdf/", vlstockfecha_vista_pdf, 
	# 	 name="vlstockfecha_vista_pdf"),
	# path("vlstockfecha/vista-excel/", vlstockfecha_vista_excel, 
	# 	 name="vlstockfecha_vista_excel"),
	# path("vlstockfecha/vista-csv/", vlstockfecha_vista_csv, 
	# 	 name="vlstockfecha_vista_csv"),
	
	#-- VL Listado Stock Único.
	path('vlstockunico_informe/', VLStockUnicoInformeView.as_view(), 
		 name='vlstockunico_informe_list'),
	path('vlstockunico/vista-preliminar/', vlstockunico_vista_pantalla, 
		 name="vlstockunico_vista_pantalla"),
	path("vlstockunico/vista-pdf/", vlstockunico_vista_pdf, 
		 name="vlstockunico_vista_pdf"),
	path("vlstockunico/vista-excel/", vlstockunico_vista_excel, 
		 name="vlstockunico_vista_excel"),
	path("vlstockunico/vista-csv/", vlstockunico_vista_csv, 
		 name="vlstockunico_vista_csv"),
	
	#-- VL Reposición de Stock.
	path('vlreposicionstock_informe/', VLReposicionStockInformeView.as_view(), 
		 name='vlreposicionstock_informe_list'),
	path('vlreposicionstock/vista-preliminar/', vlreposicionstock_vista_pantalla, 
		 name="vlreposicionstock_vista_pantalla"),
	path("vlreposicionstock/vista-pdf/", vlreposicionstock_vista_pdf, 
		 name="vlreposicionstock_vista_pdf"),
	path("vlreposicionstock/vista-excel/", vlreposicionstock_vista_excel, 
		 name="vlreposicionstock_vista_excel"),
	path("vlreposicionstock/vista-csv/", vlreposicionstock_vista_csv, 
		 name="vlreposicionstock_vista_csv"),
	
	#-- VL Movimiento Interno de Stock.
	path('vlmovimientointernostock_informe/', VLMovimientoInternoStockInformeView.as_view(), 
		 name='vlmovimientointernostock_informe_list'),
	path('vlmovimientointernostock/vista-preliminar/', vlmovimientointernostock_vista_pantalla, 
		 name="vlmovimientointernostock_vista_pantalla"),
	path("vlmovimientointernostock/vista-pdf/", vlmovimientointernostock_vista_pdf, 
		 name="vlmovimientointernostock_vista_pdf"),
	path("vlmovimientointernostock/vista-excel/", vlmovimientointernostock_vista_excel, 
		 name="vlmovimientointernostock_vista_excel"),
	path("vlmovimientointernostock/vista-csv/", vlmovimientointernostock_vista_csv, 
		 name="vlmovimientointernostock_vista_csv"),
	
	#-- VL Stock por Cliente en Depósito.
	path('vlstockcliente_informe/', VLStockClienteInformeView.as_view(), 
		 name='vlstockcliente_informe_list'),
	path('vlstockcliente/vista-preliminar/', vlstockcliente_vista_pantalla, 
		 name="vlstockcliente_vista_pantalla"),
	path("vlstockcliente/vista-pdf/", vlstockcliente_vista_pdf, 
		 name="vlstockcliente_vista_pdf"),
	path("vlstockcliente/vista-excel/", vlstockcliente_vista_excel, 
		 name="vlstockcliente_vista_excel"),
	path("vlstockcliente/vista-csv/", vlstockcliente_vista_csv, 
		 name="vlstockcliente_vista_csv"),
	
	#-- VL Stock en Depósitos de Clientes.
	path('vlstockdeposito_informe/', VLStockDepositoInformeView.as_view(), 
		 name='vlstockdeposito_informe_list'),
	path('vlstockdeposito/vista-preliminar/', vlstockdeposito_vista_pantalla, 
		 name="vlstockdeposito_vista_pantalla"),
	path("vlstockdeposito/vista-pdf/", vlstockdeposito_vista_pdf, 
		 name="vlstockdeposito_vista_pdf"),
	path("vlstockdeposito/vista-excel/", vlstockdeposito_vista_excel, 
		 name="vlstockdeposito_vista_excel"),
	path("vlstockdeposito/vista-csv/", vlstockdeposito_vista_csv, 
		 name="vlstockdeposito_vista_csv"),
	
	#-- VL Ficha de Seguimiento de Stock.
	path('vlfichaseguimientostock_informe/', VLFichaSeguimientoStockInformeView.as_view(), 
		 name='vlfichaseguimientostock_informe_list'),
	path('vlfichaseguimientostock/vista-preliminar/', vlfichaseguimientostock_vista_pantalla, 
		 name="vlfichaseguimientostock_vista_pantalla"),
	path("vlfichaseguimientostock/vista-pdf/", vlfichaseguimientostock_vista_pdf, 
		 name="vlfichaseguimientostock_vista_pdf"),
	path("vlfichaseguimientostock/vista-excel/", vlfichaseguimientostock_vista_excel, 
		 name="vlfichaseguimientostock_vista_excel"),
	path("vlfichaseguimientostock/vista-csv/", vlfichaseguimientostock_vista_csv, 
		 name="vlfichaseguimientostock_vista_csv"),
	
	#-- 6to. Lote (Compras).
	
	#-- VL Detalle de Compras por Proveedor.
	path('vldetallecompraproveedor_informe/', VLDetalleCompraProveedorInformeView.as_view(), 
		 name='vldetallecompraproveedor_informe_list'),
	path('vldetallecompraproveedor/vista-preliminar/', vldetallecompraproveedor_vista_pantalla, 
		 name="vldetallecompraproveedor_vista_pantalla"),
	path("vldetallecompraproveedor/vista-pdf/", vldetallecompraproveedor_vista_pdf, 
		 name="vldetallecompraproveedor_vista_pdf"),
	path("vldetallecompraproveedor/vista-excel/", vldetallecompraproveedor_vista_excel, 
		 name="vldetallecompraproveedor_vista_excel"),
	path("vldetallecompraproveedor/vista-csv/", vldetallecompraproveedor_vista_csv, 
		 name="vldetallecompraproveedor_vista_csv"),
	
	#-- VL Compra Ingresada.
	path('vlcompraingresada_informe/', VLCompraIngresadaInformeView.as_view(), 
		 name='vlcompraingresada_informe_list'),
	path('vlcompraingresada/vista-preliminar/', vlcompraingresada_vista_pantalla, 
		 name="vlcompraingresada_vista_pantalla"),
	path("vlcompraingresada/vista-pdf/", vlcompraingresada_vista_pdf, 
		 name="vlcompraingresada_vista_pdf"),
	path("vlcompraingresada/vista-excel/", vlcompraingresada_vista_excel, 
		 name="vlcompraingresada_vista_excel"),
	path("vlcompraingresada/vista-csv/", vlcompraingresada_vista_csv, 
		 name="vlcompraingresada_vista_csv"),
	
	#-- 7mo. Lote (Caja).
	
	#-- Detalle de Cheques.
	path('chequerecibo_informe/', ChequeReciboInformeView.as_view(), 
		 name='chequerecibo_informe_list'),
	path('chequerecibo/vista-preliminar/', chequerecibo_vista_pantalla, 
		 name="chequerecibo_vista_pantalla"),
	path("chequerecibo/vista-pdf/", chequerecibo_vista_pdf, 
		 name="chequerecibo_vista_pdf"),
	path("chequerecibo/vista-excel/", chequerecibo_vista_excel, 
		 name="chequerecibo_vista_excel"),
	path("chequerecibo/vista-csv/", chequerecibo_vista_csv, 
		 name="chequerecibo_vista_csv"),
	
	#-- Detalle de Cupones.
	path('tarjetarecibo_informe/', TarjetaReciboInformeView.as_view(), 
		 name='tarjetarecibo_informe_list'),
	path('tarjetarecibo/vista-preliminar/', tarjetarecibo_vista_pantalla, 
		 name="tarjetarecibo_vista_pantalla"),
	path("tarjetarecibo/vista-pdf/", tarjetarecibo_vista_pdf, 
		 name="tarjetarecibo_vista_pdf"),
	path("tarjetarecibo/vista-excel/", tarjetarecibo_vista_excel, 
		 name="tarjetarecibo_vista_excel"),
	path("tarjetarecibo/vista-csv/", tarjetarecibo_vista_csv, 
		 name="tarjetarecibo_vista_csv"),
	
	#-- Cupones por Fecha.
	path('cuponesfecha_informe/', CuponesFechaInformeView.as_view(), 
		 name='cuponesfecha_informe_list'),
	path('cuponesfecha/vista-preliminar/', cuponesfecha_vista_pantalla, 
		 name="cuponesfecha_vista_pantalla"),
	path("cuponesfecha/vista-pdf/", cuponesfecha_vista_pdf, 
		 name="cuponesfecha_vista_pdf"),
	path("cuponesfecha/vista-excel/", cuponesfecha_vista_excel, 
		 name="cuponesfecha_vista_excel"),
	path("cuponesfecha/vista-csv/", cuponesfecha_vista_csv, 
		 name="cuponesfecha_vista_csv"),
	
	#-- Egresos de Caja.
	path('egresoscaja_informe/', EgresosCajaInformeView.as_view(), 
		 name='egresoscaja_informe_list'),
	path('egresoscaja/vista-preliminar/', egresoscaja_vista_pantalla, 
		 name="egresoscaja_vista_pantalla"),
	path("egresoscaja/vista-pdf/", egresoscaja_vista_pdf, 
		 name="egresoscaja_vista_pdf"),
	path("egresoscaja/vista-excel/", egresoscaja_vista_excel, 
		 name="egresoscaja_vista_excel"),
	path("egresoscaja/vista-csv/", egresoscaja_vista_csv, 
		 name="egresoscaja_vista_csv"),
	
	#-- Arqueo de Caja.
	path('cajaarqueo_informe/', CajaArqueoInformeView.as_view(), 
		 name='cajaarqueo_informe_list'),
	path('cajaarqueo/vista-preliminar/', cajaarqueo_vista_pantalla, 
		 name="cajaarqueo_vista_pantalla"),
	path("cajaarqueo/vista-pdf/", cajaarqueo_vista_pdf, 
		 name="cajaarqueo_vista_pdf"),
	path("cajaarqueo/vista-excel/", cajaarqueo_vista_excel, 
		 name="cajaarqueo_vista_excel"),
	path("cajaarqueo/vista-csv/", cajaarqueo_vista_csv, 
		 name="cajaarqueo_vista_csv"),
	
	#-- Detalle de Comprobantes.
	path('detallecomprobantes_informe/', DetalleComprobantesInformeView.as_view(), 
		 name='detallecomprobantes_informe_list'),
	path('detallecomprobantes/vista-preliminar/', detallecomprobantes_vista_pantalla, 
		 name="detallecomprobantes_vista_pantalla"),
	path("detallecomprobantes/vista-pdf/", detallecomprobantes_vista_pdf, 
		 name="detallecomprobantes_vista_pdf"),
	path("detallecomprobantes/vista-excel/", detallecomprobantes_vista_excel, 
		 name="detallecomprobantes_vista_excel"),
	path("detallecomprobantes/vista-csv/", detallecomprobantes_vista_csv, 
		 name="detallecomprobantes_vista_csv"),
	
	#-- Planilla de Caja.
	path('planillacaja_informe/', PlanillaCajaInformeView.as_view(), 
		 name='planillacaja_informe_list'),
	path('planillacaja/vista-preliminar/', planillacaja_vista_pantalla, 
		 name="planillacaja_vista_pantalla"),
	path("planillacaja/vista-pdf/", planillacaja_vista_pdf, 
		 name="planillacaja_vista_pdf"),
	path("planillacaja/vista-excel/", planillacaja_vista_excel, 
		 name="planillacaja_vista_excel"),
	path("planillacaja/vista-csv/", planillacaja_vista_csv, 
		 name="planillacaja_vista_csv"),
	
	#-- Cheques por Fecha.
	path('chequesfecha_informe/', ChequesFechaInformeView.as_view(), 
		 name='chequesfecha_informe_list'),
	path('chequesfecha/vista-preliminar/', chequesfecha_vista_pantalla, 
		 name="chequesfecha_vista_pantalla"),
	path("chequesfecha/vista-pdf/", chequesfecha_vista_pdf, 
		 name="chequesfecha_vista_pdf"),
	path("chequesfecha/vista-excel/", chequesfecha_vista_excel, 
		 name="chequesfecha_vista_excel"),
	path("chequesfecha/vista-csv/", chequesfecha_vista_csv, 
		 name="chequesfecha_vista_csv"),
	
	
	
	#-- Otras rutas.
	path('filtrar-localidad/', filtrar_localidad, name='filtrar_localidad'),
	path('buscar/cliente/id/', buscar_cliente_id, name='buscar_cliente_id'),
	path('buscar/cliente/', buscar_cliente, name='buscar_cliente'),
	
	path('buscar/producto/id/', buscar_producto_por_id, name='buscar_producto_por_id'),
	path('buscar/producto/cai/', buscar_producto_por_cai, name='buscar_producto_por_cai'),

]

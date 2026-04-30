# neumatic\apps\ventas\urls.py
from django.urls import path
from .views.factura_views import (
	FacturaListView,
	FacturaCreateView,
	FacturaUpdateView,
	FacturaDeleteView
)
from .views.factura2_views import (
	FacturaManualListView,
	FacturaManualCreateView,
	FacturaManualUpdateView,
	FacturaManualDeleteView
)
from .views.factura3_views import (
	PresupuestoListView,
	PresupuestoCreateView,
	PresupuestoUpdateView,
	PresupuestoDeleteView
)
from .views.factura4_views import (
	MovimientoInternoListView,
	MovimientoInternoCreateView,
	MovimientoInternoUpdateView,
	MovimientoInternoDeleteView
)
from .views.recibo_views import (
	ReciboListView,
	ReciboCreateView,
	ReciboUpdateView,
	ReciboDeleteView
)
from .views.compra_views import (
	CompraListView,
	CompraCreateView,
	CompraUpdateView,
	CompraDeleteView
)
from .views.caja_views import (
	CajaListView,
	CajaCreateView,
	CajaUpdateView,
	CajaDeleteView
)
from .views.caja_detalle_views import (
    CajaDetalleListView, 
	CajaDetalleCreateView,
	CajaDetalleUpdateView,
	CajaDetalleDeleteView
)
from .views.consultas_factura_views import (
	buscar_agenda, 
	buscar_producto,
	buscar_cliente,
	validar_documento,
	detalle_producto,
	datos_comprobante,
	obtener_numero_comprobante,
	obtener_numero_comprobante2,
	obtener_numero_comprobante3,
	validar_vencimientos_cliente,
	validar_deudas_cliente,
	valida_autorizacion,
	verificar_remito,
	buscar_banco,
	buscar_codigo_banco,
	obtener_libro_iva,
	buscar_factura
)
from .views.consultas_compra_views import (
	obtener_numero_compra,
	obtener_alicuota_proveedor
)
from .views.crear_agenda import crear_agenda
from .views.genera_pdf import GeneraPDFView
from .views.fe_afiparca_views import fe_dummy

from .views.compra_retencion_views import (
	CompraRetencionListView,
	CompraRetencionCreateView,
	CompraRetencionUpdateView,
	CompraRetencionDeleteView
)
from .views.pdf_retenciones import PDFRetencionView


urlpatterns = [
	path('factura/listar/', FacturaListView.as_view(), name='factura_list'),
	path('factura/crear/', FacturaCreateView.as_view(), name='factura_create'),
	path('factura/editar/<int:pk>/', FacturaUpdateView.as_view(), name='factura_update'),
	path('factura/eliminar/<int:pk>/', FacturaDeleteView.as_view(), name='factura_delete'),
	
	#-- Opción 2: Comprobante Manual.
	path('facturamanual/listar/', FacturaManualListView.as_view(), name='factura_manual_list'),
	path('facturamanual/crear/', FacturaManualCreateView.as_view(), name='factura_manual_create'),
	path('facturamanual/editar/<int:pk>/', FacturaManualUpdateView.as_view(), name='factura_manual_update'),
	path('facturamanual/eliminar/<int:pk>/', FacturaManualDeleteView.as_view(), name='factura_manual_delete'),
	
	#-- Opción 3: Presupuesto.
	path('presupuesto/listar/', PresupuestoListView.as_view(), name='presupuesto_list'),
	path('presupeusto/crear/', PresupuestoCreateView.as_view(), name='presupuesto_create'),
	path('presupuesto/editar/<int:pk>/', PresupuestoUpdateView.as_view(), name='presupuesto_update'),
	path('presupuesto/eliminar/<int:pk>/', PresupuestoDeleteView.as_view(), name='presupuesto_delete'),

	#-- Opción 4: Movimiento Interno.
	path('movimientointerno/listar/', MovimientoInternoListView.as_view(), name='movimiento_interno_list'),
	path('movimientointerno/crear/', MovimientoInternoCreateView.as_view(), name='movimiento_interno_create'),
	path('movimientointerno/editar/<int:pk>/', MovimientoInternoUpdateView.as_view(), name='movimiento_interno_update'),
	path('movimientointerno/eliminar/<int:pk>/', MovimientoInternoDeleteView.as_view(), name='movimiento_interno_delete'),
	###

	path('recibo/listar/', ReciboListView.as_view(), name='recibo_list'),
	path('recibo/crear/', ReciboCreateView.as_view(), name='recibo_create'),
	path('recibo/editar/<int:pk>/', ReciboUpdateView.as_view(), name='recibo_update'),
	path('recibo/eliminar/<int:pk>/', ReciboDeleteView.as_view(), name='recibo_delete'),
	
	#-- Compra - Remitos.
	path('compra/listar/', CompraListView.as_view(), name='compra_list'),
	path('compra/crear/', CompraCreateView.as_view(), name='compra_create'),
	path('compra/editar/<int:pk>/', CompraUpdateView.as_view(), name='compra_update'),
	path('compra/eliminar/<int:pk>/', CompraDeleteView.as_view(), name='compra_delete'),
	
	path('buscar/producto/', buscar_producto, name='buscar_producto'),
	path('validar/documento/', validar_documento, name='validar_documento'),
	path('buscar/agenda/', buscar_agenda, name='buscar_agenda'),
	path('buscar/cliente/', buscar_cliente, name='buscar_agenda'),
	
	path('crear/agenda/', crear_agenda, name='crear_agenda'),
	path('detalle_producto/<int:id_producto>/', detalle_producto, name='detalle_producto'),
	path('comprobante/<int:pk>/codigo/', datos_comprobante, name='comprobante_codigo'),
	path('obtener-numero-comprobante/', obtener_numero_comprobante, name='obtener_numero_comprobante'),
	path('obtener-numero-comprobante2/', obtener_numero_comprobante2, name='obtener_numero_comprobante2'),
	path('obtener-numero-comprobante3/', obtener_numero_comprobante3, name='obtener_numero_comprobante3'),
	
	path('pdf/<int:pk>/', GeneraPDFView.as_view(), name='generic_pdf'),
	path('clientes/<int:cliente_id>/validar-vencimientos/', validar_vencimientos_cliente, name='validar_vencimientos'),
	path('clientes/<int:cliente_id>/validar-deudas-cliente/', validar_deudas_cliente, name='validar_deudas_cliente'),
	path('clientes/validar-autorizacion/', valida_autorizacion, name='validar_autorizacion'),
	path('verificar/remito/', verificar_remito, name='verificar_remito'),
	path('buscar/banco/', buscar_banco, name='buscar_banco'),
	path('buscar/codigo_banco/', buscar_codigo_banco, name='buscar_codigo_banco'),
	path('obtener/libro_iva/', obtener_libro_iva, name='obtener_libro_iva'),
	path('buscar/factura/', buscar_factura, name='buscar_factura'),
	
	#-- Vista para obtener datos de AFIPArca.
	path('obtener/estado-servidores/', fe_dummy, name='estado_servidores'),
	
	#-- Compra - Retención.
	path('compra-retencion/', CompraRetencionListView.as_view(), name='compra_retencion_list'),
	path('compra-retencion/nueva/', CompraRetencionCreateView.as_view(), name='compra_retencion_create'),
	path('compra-retencion/<int:pk>/editar/', CompraRetencionUpdateView.as_view(), name='compra_retencion_update'),
	path('compra-retencion/<int:pk>/eliminar/', CompraRetencionDeleteView.as_view(), name='compra_retencion_delete'),
	path('compra-retencion/pdf/<int:pk>/', PDFRetencionView.as_view(), name='pdf_retencion'),
    
	#-- Caja.
	path('caja/', CajaListView.as_view(), name='caja_list'),
	path('caja/nueva/', CajaCreateView.as_view(), name='caja_create'),
	path('caja/<int:pk>/editar/', CajaUpdateView.as_view(), name='caja_update'),
	path('caja/<int:pk>/eliminar/', CajaDeleteView.as_view(), name='caja_delete'),
    
	#-- Caja.
	path('cajadetalle/', CajaDetalleListView.as_view(), name='caja_detalle_list'),
	path('cajadetalle/nueva/', CajaDetalleCreateView.as_view(), name='caja_detalle_create'),
	path('cajadetalle/<int:pk>/editar/', CajaDetalleUpdateView.as_view(), name='caja_detalle_update'),
	path('cajadetalle/<int:pk>/eliminar/', CajaDetalleDeleteView.as_view(), name='caja_detalle_delete'),
	
	path('obtener-numero-compra/', obtener_numero_compra, name='obtener_numero_compra'),
	path('obtener-alicuota-proveedor/', obtener_alicuota_proveedor, name='obtener_alicuota_proveedor'),
	
]
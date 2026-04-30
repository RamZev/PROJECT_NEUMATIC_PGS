# neumatic\apps\datatools\urls.py
from django.urls import path
from .views.consulta_facturas_views import (
    ConsultaFacturasClienteView,
    ConsultaProductosView,
    CrearStockClienteView, 
    AdministrarStockClienteView,
    # NUEVAS IMPORTACIONES
    stock_cliente_detalle,
    generar_entrega_cliente,
    descargar_pdf_entrega
)
from .views.excel_views import (
	ExcelUploadView, 
	ExcelPreviewView, 
	MostrarErroresExcelView,
	ActualizarProductosView, 
	AgregarProductosView,
)
from .views.actualizar_minimo_views import (
	ActualizarMinimoCargarView,
	ActualizarMinimoPrevisualizarView,
	ActualizarMinimoErroresView,
	ActualizarMinimoView
)
from .views.actualizar_estados_views import (
	ActualizarEstadosCargarView,
	ActualizarEstadosPrevisualizarView,
	ActualizarEstadosErroresView,
	ActualizarEstadosView
)

urlpatterns = [
    path('facturas-cliente/', ConsultaFacturasClienteView.as_view(), name='consulta_facturas_cliente'),
    path('productos/', ConsultaProductosView.as_view(), name='consulta_productos_stock'),
    
	# --- NUEVAS RUTAS ---
    path('facturas-cliente/crear-stock/<int:id_factura>/', CrearStockClienteView.as_view(), name='crear_stock_cliente'),
    path('facturas-cliente/administrar-stock/<int:id_factura>/', AdministrarStockClienteView.as_view(), name='administrar_stock_cliente'),
    
	 # === NUEVAS RUTAS PARA GESTIÓN DE ENTREGAS ===
    path('stock/cliente/<int:factura_id>/', stock_cliente_detalle, name='stock_cliente_detalle'),
    path('stock/cliente/<int:factura_id>/generar-entrega/', generar_entrega_cliente, name='generar_entrega_cliente'),
    path('stock/cliente/<int:factura_id>/descargar-pdf/', descargar_pdf_entrega, name='descargar_pdf_entrega'),
	
	#-- Actualizar/Agregar Productos (Excel).
	path('cargar/excel/', ExcelUploadView.as_view(), name='cargar_excel'),
	path('previsualizar/excel/', ExcelPreviewView.as_view(), name='excel_preview'),
	path('mostrar-errores/excel/', MostrarErroresExcelView.as_view(), name='mostrar_errores_excel'),
	path('actualizar/productos/', ActualizarProductosView.as_view(), name='actualizar_productos'),
	path('agregar/productos/', AgregarProductosView.as_view(), name='agregar_productos'),
	
	#-- Actualizar Mínimo por CAI (Excel).
	path('actualizar/minimo/cargar/', ActualizarMinimoCargarView.as_view(), name='actualizar_minimo_cargar'),
	path('actualizar/minimo/previsualizar/', ActualizarMinimoPrevisualizarView.as_view(), name='actualizar_minimo_previsualizar'),
	path('actualizar/minimo/errores/', ActualizarMinimoErroresView.as_view(), name='actualizar_minimo_errores'),
	path('actualizar/minimo/', ActualizarMinimoView.as_view(), name='actualizar_minimo'),
	
	#-- Actualizar Estados de Productos por CAI (Excel).
	path('actualizar/estados/cargar/', ActualizarEstadosCargarView.as_view(), name='actualizar_estados_cargar'),
	path('actualizar/estados/previsualizar/', ActualizarEstadosPrevisualizarView.as_view(), name='actualizar_estados_previsualizar'),
	path('actualizar/estados/errores/', ActualizarEstadosErroresView.as_view(), name='actualizar_estados_errores'),
	path('actualizar/estados/', ActualizarEstadosView.as_view(), name='actualizar_estados'),
]
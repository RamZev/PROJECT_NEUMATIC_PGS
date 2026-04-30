# \apps\maestros\urls.py
from django.urls import path

from .views.actividad_views import *
from .views.sucursal_views import *
from .views.vendedor_views import *
from .views.empresa_views import *
from .views.producto_views import *
from .views.listado_producto_views import *

urlpatterns = [
    path('actividad/', ActividadListView.as_view(), name='actividad_list'),
    path('actividad/nueva/', ActividadCreateView.as_view(), name='actividad_create'),
    path('actividad/<int:pk>/editar/', ActividadUpdateView.as_view(), name='actividad_update'),
    path('actividad/<int:pk>/eliminar/', ActividadDeleteView.as_view(), name='actividad_delete'),

    path('vendedor/', VendedorListView.as_view(), name='vendedor_list'),
    path('vendedor/nueva/', VendedorCreateView.as_view(), name='vendedor_create'),
    path('vendedor/<int:pk>/editar/', VendedorUpdateView.as_view(), name='vendedor_update'),
    path('vendedor/<int:pk>/eliminar/', VendedorDeleteView.as_view(), name='vendedor_delete'),

    path('empresa/', EmpresaListView.as_view(), name='empresa_list'),
    path('empresa/nueva/', EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresa/<int:pk>/editar/', EmpresaUpdateView.as_view(), name='empresa_update'),
    path('empresa/<int:pk>/eliminar/', EmpresaDeleteView.as_view(), name='empresa_delete'),

    path('sucursal/', SucursalListView.as_view(), name='sucursal_list'),
    path('sucursal/nueva/', SucursalCreateView.as_view(), name='sucursal_create'),
    path('sucursal/<int:pk>/editar/', SucursalUpdateView.as_view(), name='sucursal_update'),
    path('sucursal/<int:pk>/eliminar/', SucursalDeleteView.as_view(), name='sucursal_delete'),

    path('producto/', ProductoListView.as_view(), name='producto_list'),
    path('producto/nueva/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto_delete'),

    path('listado_producto/', ListadoProductoListView.as_view(), name='listado_producto_list'),
    path('listado_producto/nueva/', ListadoProductoCreateView.as_view(), name='listado_producto_create'),
    path('listado_producto/<int:pk>/editar/', ListadoProductoUpdateView.as_view(), name='listado_producto_update'),
    path('listado_producto/<int:pk>/eliminar/', ListadoProductoDeleteView.as_view(), name='listado_producto_delete'),

    path('listado_producto_generado/', ListadoProductoInformeView.as_view(), name='listado_producto_pdf'),
    path('send_email_with_attachments/', ListadoProductoInformeView.as_view(), name='listado_producto_informe'),
]
# neumatic\neumatic\urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('usuarios/', include('apps.usuarios.urls')),
    path('maestros/', include('apps.maestros.urls')),
    path('ventas/', include('apps.ventas.urls')),
    path('informes/', include('apps.informes.urls')),
    path('datatools/', include('apps.datatools.urls')),
    path('menu/', include('apps.menu.urls')),
]

#-- Manejo de archivos estáticos en modo DEBUG.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

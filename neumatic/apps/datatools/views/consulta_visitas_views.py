# neumatic/apps/datatools/views/consulta_visitas_views.py
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from apps.ventas.models.servicio_vehiculo_models import ServicioVehiculo
from apps.maestros.models.sucursal_models import Sucursal

class ConsultaProximasVisitasView(TemplateView):
    template_name = 'datatools/consulta_visitas_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Parámetros de búsqueda
        id_sucursal = self.request.GET.get('id_sucursal', '').strip()
        desde_fecha = self.request.GET.get('desde_fecha', '').strip()
        hasta_fecha = self.request.GET.get('hasta_fecha', '').strip()
        
        # Si es la primera vez que carga la página, sugerimos la sucursal del usuario
        if not id_sucursal and not desde_fecha and not hasta_fecha:
            if self.request.user.is_authenticated and self.request.user.id_sucursal:
                id_sucursal = str(self.request.user.id_sucursal.id_sucursal)
            
            # Sugerimos el rango de fechas (hoy hasta dentro de 30 días)
            hoy = timezone.now().date()
            desde_fecha = hoy.strftime('%Y-%m-%d')
            hasta_fecha = (hoy + timezone.timedelta(days=30)).strftime('%Y-%m-%d')

        servicios = ServicioVehiculo.objects.none()
        page_obj = None
        error = None
        
        # Solo buscar si hay fechas
        if desde_fecha and hasta_fecha:
            try:
                # Convertir a fechas
                f_desde = datetime.strptime(desde_fecha, '%Y-%m-%d').date()
                f_hasta = datetime.strptime(hasta_fecha, '%Y-%m-%d').date()

                # 👇 CORRECCIÓN: Solo filtramos por fecha aquí
                query = Q(
                    proxima_visita__range=(f_desde, f_hasta),
                    proxima_visita__isnull=False
                )
                
                # 👇 Si hay sucursal seleccionada, agregamos el filtro de sucursal de forma segura
                if id_sucursal:
                    query &= Q(id_cliente__id_sucursal_id=id_sucursal)

                # Obtener servicios, optimizando las consultas con select_related
                servicios = ServicioVehiculo.objects.filter(query).select_related(
                    'id_cliente',
                    'id_cliente__id_sucursal',
                    'id_cliente__id_localidad',
                    'id_vehiculo',
                    'id_vehiculo__id_marca_vehiculo',
                    'id_vehiculo__id_modelo_vehiculo'
                ).order_by('proxima_visita', 'id_vehiculo__patente')

                # Paginación
                paginator = Paginator(servicios, 20) # 20 por página
                page_number = self.request.GET.get('page')
                page_obj = paginator.get_page(page_number)

            except Exception as e:
                error = f"Error al realizar la búsqueda: {str(e)}"

        # Obtener sucursales para el select
        sucursales = Sucursal.objects.filter(estatus_sucursal=True).order_by('nombre_sucursal')

        context.update({
            'servicios': page_obj.object_list if page_obj else [],
            'page_obj': page_obj,
            'sucursales': sucursales,
            'id_sucursal': id_sucursal,
            'desde_fecha': desde_fecha,
            'hasta_fecha': hasta_fecha,
            'error': error,
            'fecha': timezone.now()
        })
        return context
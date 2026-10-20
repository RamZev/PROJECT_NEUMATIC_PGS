# neumatic/apps/datatools/views/consulta_servicios_views.py

from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from apps.ventas.models.servicio_vehiculo_models import ServicioVehiculo, DetalleServicioVehiculo
from apps.maestros.models.cliente_models import Cliente
from apps.maestros.models.vehiculo_models import Vehiculo

class ConsultaServiciosVehiculoView(TemplateView):
    template_name = 'datatools/consulta_servicios_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        id_cliente = self.request.GET.get('id_cliente', '').strip()
        id_vehiculo = self.request.GET.get('id_vehiculo', '').strip()
        
        servicios = ServicioVehiculo.objects.none()
        cliente_sel = None
        vehiculo_sel = None
        error = None
        page_obj = None

        if id_cliente or id_vehiculo:
            try:
                query = Q()
                if id_cliente:
                    query &= Q(id_cliente_id=id_cliente)
                    cliente_sel = Cliente.objects.filter(id_cliente=id_cliente).first()
                    
                if id_vehiculo:
                    query &= Q(id_vehiculo_id=id_vehiculo)
                    vehiculo_sel = Vehiculo.objects.filter(id_vehiculo=id_vehiculo).first()

                servicios = ServicioVehiculo.objects.filter(query).select_related(
                    'id_cliente', 'id_vehiculo',
                    'id_vehiculo__id_marca_vehiculo', 'id_vehiculo__id_modelo_vehiculo'
                ).order_by('-id_servicio_vehiculo')

                paginator = Paginator(servicios, 10)
                page_number = self.request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                # Pre-cargar detalles solo para los servicios de esta página
                if page_obj.object_list:
                    servicios_ids = [s.id_servicio_vehiculo for s in page_obj]
                    detalles = DetalleServicioVehiculo.objects.filter(
                        id_servicio_vehiculo__in=servicios_ids
                    ).select_related('id_producto', 'id_vendedor')
                    
                    # Crear un diccionario temporal para agrupar
                    detalles_dict = {}
                    for detalle in detalles:
                        sid = detalle.id_servicio_vehiculo_id
                        if sid not in detalles_dict:
                            detalles_dict[sid] = []
                        detalles_dict[sid].append(detalle)
                    
                    # Asignar la lista de detalles a cada servicio
                    for servicio in page_obj:
                        servicio.detalles_lista = detalles_dict.get(servicio.id_servicio_vehiculo, [])

            except Exception as e:
                error = f"Error al realizar la búsqueda: {str(e)}"

        context.update({
            'servicios': page_obj.object_list if page_obj else [],
            'page_obj': page_obj,
            'id_cliente': id_cliente,
            'id_vehiculo': id_vehiculo,
            'cliente_sel': cliente_sel,
            'vehiculo_sel': vehiculo_sel,
            'error': error,
            'fecha': timezone.now()
        })
        return context
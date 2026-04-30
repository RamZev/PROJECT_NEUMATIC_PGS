# neumatic\apps\ventas\views\caja_views.py
from django.urls import reverse_lazy
from apps.maestros.views.cruds_views_generics import *
from ..models.caja_models import Caja, CajaDetalle
from ..forms.caja_detalle_forms import CajaDetalleForm


class ConfigViews():
    # Modelo
    model = CajaDetalle
    
    # Formulario asociado al modelo
    form_class = CajaDetalleForm
    
    # Aplicación asociada al modelo
    app_label = model._meta.app_label
    
    #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
    model_string = model.__name__.lower()  # "caja"
    model_string = "caja_detalle"
    
    # Permisos
    permission_add = f"{app_label}.add_{model.__name__.lower()}"
    permission_change = f"{app_label}.change_{model.__name__.lower()}"
    permission_delete = f"{app_label}.delete_{model.__name__.lower()}"
    
    # Vistas del CRUD del modelo
    list_view_name = f"{model_string}_list"
    create_view_name = f"{model_string}_create"
    update_view_name = f"{model_string}_update"
    delete_view_name = f"{model_string}_delete"
    
    # Plantilla para crear o actualizar el modelo
    template_form = f"{app_label}/{model_string}_form.html"
    
    # Plantilla para confirmar eliminación de un registro
    template_delete = "base_confirm_delete.html"
    
    # Plantilla de la lista del CRUD
    template_list = f'{app_label}/maestro_list.html'
    
    # Contexto de los datos de la lista
    context_object_name = 'objetos'
    
    # Vista del home del proyecto
    home_view_name = "home"
    
    # Nombre de la url 
    success_url = reverse_lazy(list_view_name)


class DataViewList():
    search_fields = ['id_caja__numero_caja']
    
    ordering = ['-id_caja']
    
    paginate_by = 10
      
    table_headers = {
        'id_caja': (1, 'Número'),
        'idventas': (1, 'idventas'),
        'id_forma_pago': (1, 'F. Pago'),
        'tipo_movimiento': (1, 'I(1)-E(2)'),
        'importe': (1, 'Importe'),
        'observacion': (4, 'Observación'),

    }
    
    table_data = [
        {'field_name': 'id_caja', 'date_format': None},
        {'field_name': 'idventas', 'date_format': None},
        {'field_name': 'id_forma_pago', 'date_format': None},
        {'field_name': 'tipo_movimiento', 'date_format': None},
        {'field_name': 'importe', 'date_format': None},
        {'field_name': 'observacion', 'date_format': None},

    ]


# CajaListView - Inicio
class CajaDetalleListView(MaestroListView):
    model = ConfigViews.model
    template_name = ConfigViews.template_list
    context_object_name = ConfigViews.context_object_name
    
    search_fields = DataViewList.search_fields
    ordering = DataViewList.ordering
    paginate_by = DataViewList.paginate_by
    
    extra_context = {
        "master_title": ConfigViews.model._meta.verbose_name_plural,
        "home_view_name": ConfigViews.home_view_name,
        "list_view_name": ConfigViews.list_view_name,
        "create_view_name": ConfigViews.create_view_name,
        "update_view_name": ConfigViews.update_view_name,
        "delete_view_name": ConfigViews.delete_view_name,
        "table_headers": DataViewList.table_headers,
        "table_data": DataViewList.table_data,
        "model_string": ConfigViews.model_string,
    }


class CajaDetalleCreateView(MaestroCreateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url
    permission_required = ConfigViews.permission_add
    
    def get_form_kwargs(self):
        """Pasar el request al formulario"""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_context_data(self, **kwargs):
        """Agregar información adicional al contexto"""
        context = super().get_context_data(**kwargs)
        
        # Verificar si hay caja abierta para mostrar mensaje en template
        usuario = self.request.user
        caja_abierta = None
        
        if usuario and usuario.id_sucursal:
            try:
                caja_abierta = Caja.objects.filter(
                    id_sucursal=usuario.id_sucursal,
                    caja_cerrada=False,
                    estatus_caja=True
                ).latest('fecha_caja')
            except Caja.DoesNotExist:
                pass
        
        context['caja_abierta'] = caja_abierta
        context['puede_crear'] = caja_abierta is not None
        
        return context
    
    def form_valid(self, form):
        """Guardar el detalle asociado a la caja abierta"""
        # El formulario ya validó que haya caja abierta
        # y asignó automáticamente id_caja en el clean()
        detalle = form.save()
        
        messages.success(
            self.request, 
            f"Movimiento registrado exitosamente en la caja {detalle.id_caja.numero_caja}"
        )
        return super().form_valid(form)

class CajaDetalleUpdateView(MaestroUpdateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url
    permission_required = ConfigViews.permission_change
    
    def get_form_kwargs(self):
        """Pasar el request al formulario"""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_context_data(self, **kwargs):
        """Agregar información de solo lectura para modificaciones"""
        context = super().get_context_data(**kwargs)
        context['modo_lectura'] = True  # Indicar que estamos en modo lectura
        return context


# CajaDeleteView
class CajaDetalleDeleteView(MaestroDeleteView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    template_name = ConfigViews.template_delete
    success_url = ConfigViews.success_url
    
    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_delete
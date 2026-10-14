# neumatic/apps/maestros/views/marca_vehiculo_views.py
from ..views.cruds_views_generics import *
from ..models.vehiculo_models import MarcaVehiculo
from ..forms.marca_vehiculo_forms import MarcaVehiculoForm


class ConfigViews(BaseConfigViews):
    #-- Modelo.
    model = MarcaVehiculo

    #-- Formulario asociado al modelo.
    form_class = MarcaVehiculoForm
    
    model_string = "marca_vehiculo"


class DataViewList():
    search_fields = [
        'marca_vehiculo',
    ]

    ordering = ['marca_vehiculo']

    paginate_by = 8

    table_headers = {
        'estatus_marca_vehiculo': (1, 'Estatus'),
        'marca_vehiculo': (6, 'Marca Vehículo'),
        'acciones': (2, 'Acciones'),
    }

    table_data = [
        {'field_name': 'estatus_marca_vehiculo', 'date_format': None},
        {'field_name': 'marca_vehiculo', 'date_format': None},
    ]


class MarcaVehiculoListView(MaestroListView):
    model = ConfigViews.model
    template_name = ConfigViews.template_list
    context_object_name = ConfigViews.context_object_name

    search_fields = DataViewList.search_fields
    ordering = DataViewList.ordering

    extra_context = {
        "master_title": ConfigViews.model._meta.verbose_name_plural,
        "home_view_name": ConfigViews.home_view_name,
        "list_view_name": ConfigViews.list_view_name,
        "create_view_name": ConfigViews.create_view_name,
        "update_view_name": ConfigViews.update_view_name,
        "detail_view_name": ConfigViews.detail_view_name,
        "delete_view_name": ConfigViews.delete_view_name,
        "table_headers": DataViewList.table_headers,
        "table_data": DataViewList.table_data,
    }


class MarcaVehiculoCreateView(MaestroCreateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_add


class MarcaVehiculoUpdateView(MaestroUpdateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_change


class MarcaVehiculoDetailView(MaestroDetailView):
    model = ConfigViews.model
    form_class = ConfigViews.form_class
    list_view_name = ConfigViews.list_view_name
    update_view_name = ConfigViews.update_view_name
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_view


class MarcaVehiculoDeleteView(MaestroDeleteView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    template_name = ConfigViews.template_delete
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_delete
# neumatic/apps/maestros/views/modelo_vehiculo_views.py
from ..views.cruds_views_generics import *
from ..models.vehiculo_models import ModeloVehiculo
from ..forms.modelo_vehiculo_forms import ModeloVehiculoForm


class ConfigViews(BaseConfigViews):
    #-- Modelo.
    model = ModeloVehiculo

    #-- Formulario asociado al modelo.
    form_class = ModeloVehiculoForm

    #-- Nombre compuesto por más de una palabra: sobreescribir model_string.
    model_string = "modelo_vehiculo"


class DataViewList():
    search_fields = [
        'modelo_vehiculo',
        'id_marca_vehiculo__marca_vehiculo',
    ]

    ordering = ['id_marca_vehiculo', 'modelo_vehiculo']

    paginate_by = 8

    table_headers = {
        'estatus_modelo_vehiculo': (1, 'Estatus'),
        'id_marca_vehiculo': (3, 'Marca'),
        'modelo_vehiculo': (4, 'Modelo'),
        'acciones': (2, 'Acciones'),
    }

    table_data = [
        {'field_name': 'estatus_modelo_vehiculo', 'date_format': None},
        {'field_name': 'id_marca_vehiculo', 'date_format': None},
        {'field_name': 'modelo_vehiculo', 'date_format': None},
    ]


class ModeloVehiculoListView(MaestroListView):
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


class ModeloVehiculoCreateView(MaestroCreateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_add


class ModeloVehiculoUpdateView(MaestroUpdateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_change


class ModeloVehiculoDetailView(MaestroDetailView):
    model = ConfigViews.model
    form_class = ConfigViews.form_class
    list_view_name = ConfigViews.list_view_name
    update_view_name = ConfigViews.update_view_name
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_view


class ModeloVehiculoDeleteView(MaestroDeleteView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    template_name = ConfigViews.template_delete
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_delete
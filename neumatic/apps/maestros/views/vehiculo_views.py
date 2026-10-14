# neumatic/apps/maestros/views/vehiculo_views.py
from ..views.cruds_views_generics import *
from ..models.vehiculo_models import Vehiculo
from ..forms.vehiculo_forms import VehiculoForm


class ConfigViews(BaseConfigViews):
    #-- Modelo.
    model = Vehiculo

    #-- Formulario asociado al modelo.
    form_class = VehiculoForm

    #-- Nombre compuesto por más de una palabra: sobreescribir model_string.
    model_string = "vehiculo"


class DataViewList():
    search_fields = [
        'patente',
        'id_marca_vehiculo__marca_vehiculo',
        'id_modelo_vehiculo__modelo_vehiculo',
    ]

    ordering = ['id_marca_vehiculo', 'id_modelo_vehiculo', 'anio']

    paginate_by = 8

    table_headers = {
        'estatus_vehiculo': (1, 'Estatus'),
        'tipo_vehiculo': (2, 'Tipo'),
        'id_marca_vehiculo': (2, 'Marca'),
        'id_modelo_vehiculo': (2, 'Modelo'),
        'segmento': (1, 'Seg.'),
        'anio': (1, 'Año'),
        'patente': (2, 'Patente'),
        'acciones': (2, 'Acciones'),
    }

    table_data = [
        {'field_name': 'estatus_vehiculo', 'date_format': None},
        {'field_name': 'tipo_vehiculo', 'date_format': None},
        {'field_name': 'id_marca_vehiculo', 'date_format': None},
        {'field_name': 'id_modelo_vehiculo', 'date_format': None},
        {'field_name': 'segmento', 'date_format': None},
        {'field_name': 'anio', 'date_format': None},
        {'field_name': 'patente', 'date_format': None},
    ]


class VehiculoListView(MaestroListView):
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


class VehiculoCreateView(MaestroCreateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_add


class VehiculoUpdateView(MaestroUpdateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_change


class VehiculoDetailView(MaestroDetailView):
    model = ConfigViews.model
    form_class = ConfigViews.form_class
    list_view_name = ConfigViews.list_view_name
    update_view_name = ConfigViews.update_view_name
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_view


class VehiculoDeleteView(MaestroDeleteView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    template_name = ConfigViews.template_delete
    success_url = ConfigViews.success_url

    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_delete
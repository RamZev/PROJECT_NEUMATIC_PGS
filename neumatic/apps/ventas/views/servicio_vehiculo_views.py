# neumatic/apps/ventas/views/servicio_vehiculo_views.py
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages

from .msdt_views_generics import (
    MaestroDetalleListView,
    MaestroDetalleCreateView,
    MaestroDetalleUpdateView,
    MaestroDetalleDeleteView,
)
from ..models.servicio_vehiculo_models import ServicioVehiculo
from ..forms.servicio_vehiculo_forms import (
    ServicioVehiculoForm,
    DetalleServicioVehiculoFormSet,
)

modelo = ServicioVehiculo
model_string = "servicio_vehiculo"
formulario = ServicioVehiculoForm
template_form = f"{model_string}_form.html"

home_view_name = "home"
list_view_name = f"{model_string}_list"
create_view_name = f"{model_string}_create"
update_view_name = f"{model_string}_update"
delete_view_name = f"{model_string}_delete"


class ServicioVehiculoListView(MaestroDetalleListView):
    model = modelo
    template_name = "ventas/maestro_detalle_list.html"
    context_object_name = 'objetos'

    search_fields = [
        'id_servicio_vehiculo',
        'id_cliente__nombre_cliente',
        'id_vehiculo__patente',
    ]
    ordering = ['-id_servicio_vehiculo']

    table_headers = {
        'id_servicio_vehiculo': (1, 'ID'),
        'fcontrol': (2, 'Fecha'),
        'id_cliente': (3, 'Cliente'),
        'id_vehiculo': (3, 'Vehículo'),
        'kmxmes': (1, 'Km'),
        'opciones': (1, 'Opciones'),
    }

    table_data = [
        {'field_name': 'id_servicio_vehiculo', 'date_format': None},
        {'field_name': 'fcontrol', 'date_format': 'd/m/Y'},
        {'field_name': 'id_cliente', 'date_format': None},
        {'field_name': 'id_vehiculo', 'date_format': None},
        {'field_name': 'kmxmes', 'date_format': None},
    ]

    extra_context = {
        "master_title": "Servicios de Vehículos",
        "home_view_name": home_view_name,
        "list_view_name": list_view_name,
        "create_view_name": create_view_name,
        "update_view_name": update_view_name,
        "delete_view_name": delete_view_name,
        "table_headers": table_headers,
        "table_data": table_data,
        "model_string": model_string,
    }


class ServicioVehiculoCreateView(MaestroDetalleCreateView):
    model = modelo
    list_view_name = list_view_name
    form_class = formulario
    template_name = f"ventas/{template_form}"
    success_url = reverse_lazy(list_view_name)

    app_label = model._meta.app_label
    permission_required = f"{app_label}.add_{model.__name__.lower()}"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['formset_detalle'] = DetalleServicioVehiculoFormSet(self.request.POST)
        else:
            data['formset_detalle'] = DetalleServicioVehiculoFormSet(instance=self.object)

        data['is_edit'] = False
        data['titulo'] = "Crear Servicio de Vehículo"
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        formset_detalle = context['formset_detalle']

        if not formset_detalle.is_valid():
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                self.object = form.save()
                formset_detalle.instance = self.object
                formset_detalle.save()

                messages.success(
                    self.request,
                    f"✅ Servicio #{self.object.id_servicio_vehiculo} creado correctamente."
                )
                return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"❌ Error al guardar: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("Errores form principal:", form.errors)
        context = self.get_context_data()
        fs = context['formset_detalle']
        if fs:
            for i, f in enumerate(fs):
                if f.errors:
                    print(f"Formset row {i}:", f.errors)
        return super().form_invalid(form)


class ServicioVehiculoUpdateView(MaestroDetalleUpdateView):
    model = modelo
    list_view_name = list_view_name
    form_class = formulario
    template_name = f"ventas/{template_form}"
    success_url = reverse_lazy(list_view_name)

    app_label = model._meta.app_label
    permission_required = f"{app_label}.change_{model.__name__.lower()}"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['formset_detalle'] = DetalleServicioVehiculoFormSet(
                self.request.POST, instance=self.object
            )
        else:
            data['formset_detalle'] = DetalleServicioVehiculoFormSet(instance=self.object)

        data['is_edit'] = True
        data['titulo'] = "Editar Servicio de Vehículo"
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        formset_detalle = context['formset_detalle']

        if not formset_detalle.is_valid():
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                self.object = form.save()
                formset_detalle.instance = self.object
                formset_detalle.save()

                messages.success(self.request, "✅ Servicio actualizado correctamente.")
                return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f"❌ Error al actualizar: {str(e)}")
            return self.form_invalid(form)


class ServicioVehiculoDeleteView(MaestroDetalleDeleteView):
    model = modelo
    list_view_name = list_view_name
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy(list_view_name)

    app_label = model._meta.app_label
    permission_required = f"{app_label}.delete_{model.__name__.lower()}"

    extra_context = {
        "accion": f"Eliminar {model._meta.verbose_name}",
        "list_view_name": list_view_name,
        "mensaje": "¿Está seguro que desea eliminar el registro?",
    }
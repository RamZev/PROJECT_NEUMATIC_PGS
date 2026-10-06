# neumatic/apps/ventas/views/movimiento_interno_views.py
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.db import transaction
from django.db.models import F, Q
from django.db import DatabaseError
from django.utils import timezone
from django.contrib import messages

from datetime import date

from .msdt_views_generics import (
    MaestroDetalleListView,
    MaestroDetalleCreateView,
    MaestroDetalleUpdateView,
    MaestroDetalleDeleteView,
)
from ..models.movimiento_interno_models import (
    MovimientoInterno,
    DetalleMovimientoInterno,
)
from ..forms.movimiento_interno_forms import (
    MovimientoInternoForm,
    DetalleMovimientoInternoFormSet,
)
from ...maestros.models.base_models import (
    ProductoStock,
    ComprobanteVenta,
)
from ...maestros.models.numero_models import Numero


modelo = MovimientoInterno
model_string = "movimiento_interno"

formulario = MovimientoInternoForm
template_form = f"{model_string}_form.html"
home_view_name = "home"
list_view_name = f"{model_string}_list"
create_view_name = f"{model_string}_create"
update_view_name = f"{model_string}_update"
delete_view_name = f"{model_string}_delete"


# =====================================================================
# HELPERS
# =====================================================================

def obtener_comprobante_interno():
    """
    Devuelve el ComprobanteVenta marcado como interno=True.
    Si no existe, lanza excepción.
    """
    comprobante = ComprobanteVenta.objects.filter(
        interno=True,
        estatus_comprobante_venta=True
    ).first()
    if not comprobante:
        raise ValueError(
            "No existe un ComprobanteVenta con 'interno=True'. "
            "Cree uno en Maestros → Comprobantes de Venta."
        )
    return comprobante


def calcular_siguiente_numero(sucursal, punto_venta, comprobante_afip, letra):
    """
    Calcula el siguiente número para un movimiento interno.
    Reutiliza el modelo Numero con bloqueo select_for_update.
    Devuelve el número formado (PtoVta2d + Num8d).
    """
    numero_obj, created = Numero.objects.select_for_update(nowait=True).get_or_create(
        id_sucursal=sucursal,
        id_punto_venta=punto_venta,
        comprobante=comprobante_afip,
        letra=letra,
        defaults={'numero': 0, 'lineas': 1, 'copias': 1}
    )
    siguiente = numero_obj.numero + 1
    Numero.objects.filter(pk=numero_obj.pk).update(numero=F('numero') + 1)

    pv_2d = f"{int(punto_venta.punto_venta):02d}"
    num_8d = f"{siguiente:08d}"
    return f"{pv_2d}{num_8d}", siguiente


def actualizar_stock(detalles, deposito, fecha, signo=1, revertir=False):
    """
    Actualiza ProductoStock sumando (o restando si revertir=True)
    la cantidad de cada detalle.
    - Si el registro ProductoStock no existe, lo crea con stock=0 antes de aplicar el delta.
    - signo: multiplicador general (normalmente 1).
    - revertir: invierte el signo (para eliminación o reversión previa a edición).
    """
    multiplicador = -1 if revertir else 1

    for detalle in detalles:
        if not detalle.id_producto:
            continue
        if detalle.id_producto.tipo_producto != 'P':
            continue  # Solo productos físicos
        if not detalle.cantidad:
            continue

        # ─── 1. Asegurar que exista el registro (idempotente) ───
        ProductoStock.objects.get_or_create(
            id_producto=detalle.id_producto,
            id_deposito=deposito,
            defaults={
                'stock': 0,
                'minimo': 0,
                'fecha_producto_stock': fecha,
            }
        )

        # ─── 2. Bloquear y actualizar ───
        try:
            producto_stock = ProductoStock.objects.select_for_update().get(
                id_producto=detalle.id_producto,
                id_deposito=deposito
            )
        except ProductoStock.DoesNotExist:
            print(f"ADVERTENCIA: ProductoStock no existe pese al get_or_create "
                  f"(producto={detalle.id_producto_id}, deposito={deposito.pk})")
            continue

        producto_stock.stock += (detalle.cantidad * signo * multiplicador)
        producto_stock.fecha_producto_stock = fecha
        producto_stock.save()

# =====================================================================
# VISTAS
# =====================================================================

class MovimientoInternoListView(MaestroDetalleListView):
    model = modelo
    template_name = "ventas/maestro_detalle_list.html"
    context_object_name = 'objetos'

    search_fields = [
        'id_movimiento_interno',
        'compro',
        'numero_comprobante',
        'observa_comprobante',
        'id_deposito__nombre_producto_deposito',
    ]

    ordering = ['-id_movimiento_interno']

    table_headers = {
        'id_movimiento_interno': (1, 'ID'),
        'compro': (1, 'Compro'),
        'numero_comprobante': (2, 'Nro Comp'),
        'fecha_comprobante': (1, 'Fecha'),
        'id_deposito': (3, 'Depósito'),
        'observa_comprobante': (3, 'Observaciones'),
        'opciones': (1, 'Opciones'),
    }

    table_data = [
        {'field_name': 'id_movimiento_interno', 'date_format': None},
        {'field_name': 'compro', 'date_format': None},
        {'field_name': 'numero_comprobante', 'date_format': None},
        {'field_name': 'fecha_comprobante', 'date_format': 'd/m/Y'},
        {'field_name': 'id_deposito', 'date_format': None},
        {'field_name': 'observa_comprobante', 'date_format': None},
    ]

    extra_context = {
        "master_title": "Movimientos Internos de Stock",
        "home_view_name": home_view_name,
        "list_view_name": list_view_name,
        "create_view_name": create_view_name,
        "update_view_name": update_view_name,
        "delete_view_name": delete_view_name,
        "table_headers": table_headers,
        "table_data": table_data,
        "model_string_for_pdf": "movimiento_interno",
        "model_string": model_string,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if not (user.is_superuser or user.jerarquia == "A"):
            queryset = queryset.filter(id_sucursal=user.id_sucursal)

        query = self.request.GET.get('busqueda', None)
        if query:
            search_conditions = Q()
            for field in self.search_fields:
                search_conditions |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(search_conditions)

        return queryset.select_related('id_deposito', 'id_comprobante_venta').order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_string'] = model_string
        if hasattr(self, 'extra_context'):
            context.update(self.extra_context)
        return context


class MovimientoInternoCreateView(MaestroDetalleCreateView):
    model = modelo
    list_view_name = list_view_name
    form_class = formulario
    template_name = f"ventas/{template_form}"
    success_url = reverse_lazy(list_view_name)

    app_label = model._meta.app_label
    permission_required = f"{app_label}.add_{model.__name__.lower()}"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        usuario = self.request.user

        if self.request.POST:
            data['formset_detalle'] = DetalleMovimientoInternoFormSet(
                self.request.POST, instance=self.object
            )
        else:
            data['formset_detalle'] = DetalleMovimientoInternoFormSet(
                instance=self.object
            )

        data['is_edit'] = False
        data['titulo'] = "Crear Movimiento Interno"
        data['tipo_comprobante'] = "interno"

        # Datos para el JS (buscador de productos)
        data['operario_dict'] = "{}"  # No aplica, pero la plantilla lo espera
        data['cliente_empresa_id'] = ""

        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        usuario = self.request.user
        initial['id_sucursal'] = usuario.id_sucursal
        initial['fecha_comprobante'] = date.today()
        return initial

    def form_valid(self, form):
        context = self.get_context_data()
        formset_detalle = context['formset_detalle']

        if not formset_detalle.is_valid():
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                # 1. Validar depósito
                deposito = form.cleaned_data.get('id_deposito')
                if not deposito:
                    form.add_error('id_deposito', 'Debe seleccionar un depósito')
                    return self.form_invalid(form)

                # 2. Obtener comprobante interno
                try:
                    comprobante = obtener_comprobante_interno()
                except ValueError as e:
                    form.add_error(None, str(e))
                    return self.form_invalid(form)

                # 3. Asignar valores automáticos al encabezado
                form.instance.id_sucursal = self.request.user.id_sucursal
                form.instance.id_comprobante_venta = comprobante
                form.instance.compro = comprobante.codigo_comprobante_venta
                form.instance.letra_comprobante = "X"
                form.instance.estatus_comprobante = True

                # 4. Numeración vía modelo Numero
                nuevo_numero, numero_secuencial = calcular_siguiente_numero(
                    sucursal=form.instance.id_sucursal,
                    punto_venta=self.request.user.id_punto_venta,
                    comprobante_afip=comprobante.codigo_comprobante_venta,
                    letra=form.instance.letra_comprobante,
                )
                form.instance.numero_comprobante = int(nuevo_numero)

                # 5. Guardar encabezado
                self.object = form.save()

                # 6. Guardar detalle
                formset_detalle.instance = self.object
                detalles = formset_detalle.save()

                # 7. Impactar stock
                actualizar_stock(
                    detalles=detalles,
                    deposito=deposito,
                    fecha=form.instance.fecha_comprobante,
                    signo=1,
                    revertir=False,
                )

                messages.success(
                    self.request,
                    f"Movimiento Interno {nuevo_numero} creado correctamente."
                )
                return redirect(self.get_success_url())

        except DatabaseError as e:
            messages.error(self.request, f"Error de concurrencia: {e}")
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f"Error inesperado: {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("Errores form encabezado:", form.errors)
        context = self.get_context_data()
        formset_detalle = context['formset_detalle']
        if formset_detalle:
            for i, form_d in enumerate(formset_detalle):
                if form_d.errors:
                    print(f"Errores formset[{i}]:", form_d.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse(list_view_name)


class MovimientoInternoUpdateView(MaestroDetalleUpdateView):
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
            data['formset_detalle'] = DetalleMovimientoInternoFormSet(
                self.request.POST, instance=self.object
            )
        else:
            data['formset_detalle'] = DetalleMovimientoInternoFormSet(
                instance=self.object
            )
        data['is_edit'] = True
        data['titulo'] = "Editar Movimiento Interno"
        data['tipo_comprobante'] = "interno"
        data['operario_dict'] = "{}"
        data['cliente_empresa_id'] = ""
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
                # 1. Revertir stock anterior
                detalles_anteriores = list(
                    DetalleMovimientoInterno.objects.filter(
                        id_movimiento_interno=self.object
                    )
                )
                if detalles_anteriores:
                    actualizar_stock(
                        detalles=detalles_anteriores,
                        deposito=self.object.id_deposito,
                        fecha=self.object.fecha_comprobante,
                        signo=1,
                        revertir=True,  # Invierte el signo
                    )

                # 2. Guardar encabezado actualizado
                self.object = form.save()

                # 3. Guardar detalle
                formset_detalle.instance = self.object
                detalles_nuevos = formset_detalle.save()

                # 4. Impactar stock nuevo
                actualizar_stock(
                    detalles=detalles_nuevos,
                    deposito=self.object.id_deposito,
                    fecha=self.object.fecha_comprobante,
                    signo=1,
                    revertir=False,
                )

                messages.success(self.request, "Movimiento Interno actualizado correctamente.")
                return redirect(self.get_success_url())

        except Exception as e:
            messages.error(self.request, f"Error al actualizar: {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("Errores form encabezado:", form.errors)
        context = self.get_context_data()
        formset_detalle = context['formset_detalle']
        if formset_detalle:
            for i, form_d in enumerate(formset_detalle):
                if form_d.errors:
                    print(f"Errores formset[{i}]:", form_d.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return self.success_url


class MovimientoInternoDeleteView(MaestroDetalleDeleteView):
    model = modelo
    list_view_name = list_view_name
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy(list_view_name)

    app_label = model._meta.app_label
    permission_required = f"{app_label}.delete_{model.__name__.lower()}"

    extra_context = {
        "accion": "Eliminar Movimiento Interno",
        "list_view_name": list_view_name,
        "mensaje": "¿Estás seguro que deseas eliminar el Movimiento Interno? Se revertirá el stock impactado."
    }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            with transaction.atomic():
                # Revertir stock antes de eliminar
                detalles = list(
                    DetalleMovimientoInterno.objects.filter(
                        id_movimiento_interno=self.object
                    )
                )
                if detalles:
                    actualizar_stock(
                        detalles=detalles,
                        deposito=self.object.id_deposito,
                        fecha=self.object.fecha_comprobante,
                        signo=1,
                        revertir=True,
                    )

                # Eliminar (el CASCADE borra los detalles)
                return super().post(request, *args, **kwargs)

        except Exception as e:
            messages.error(request, f"Error al eliminar: {e}")
            return redirect(self.success_url)
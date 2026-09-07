# neumatic/apps/datatools/views/productos_mercado_libre_views.py
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.base_models import ProductoStock
from apps.datatools.forms.productos_mercado_libre_forms import ExportarProductosForm


class ExportarProductosCarritoView(LoginRequiredMixin, TemplateView):
    template_name = 'datatools/productos_mercado_libre_form.html'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = ExportarProductosForm(request.GET)
        context['form'] = form

        # Verificar si hay filtros aplicados (excepto 'page')
        tiene_filtros = any(key for key in request.GET.keys() if key != 'page')
        productos = Producto.objects.none()  # Por defecto vacío

        if tiene_filtros and form.is_valid():
            # Base: solo productos activos
            productos = Producto.objects.filter(estatus_producto=True).select_related(
                'id_marca', 'id_familia', 'id_modelo', 'id_cai'
            )

            # Aplicar filtros
            tipo_producto = form.cleaned_data.get('tipo_producto')
            if tipo_producto:
                productos = productos.filter(tipo_producto=tipo_producto)

            marca = form.cleaned_data.get('marca')
            if marca:
                productos = productos.filter(id_marca=marca)

            familia = form.cleaned_data.get('familia')
            if familia:
                productos = productos.filter(id_familia=familia)

            modelo = form.cleaned_data.get('modelo')
            if modelo:
                productos = productos.filter(id_modelo=modelo)

            medida = form.cleaned_data.get('medida')
            if medida:
                productos = productos.filter(medida__icontains=medida)

            cai = form.cleaned_data.get('cai')
            if cai:
                productos = productos.filter(id_cai__cai__icontains=cai)

            busqueda = form.cleaned_data.get('busqueda')
            if busqueda:
                productos = productos.filter(
                    Q(nombre_producto__icontains=busqueda)
                )

            solo_con_stock = form.cleaned_data.get('solo_con_stock')
            if solo_con_stock:
                productos = productos.annotate(
                    stock_total=Sum('productostock__stock')
                ).filter(stock_total__gt=0)

            # Paginación
            paginator = Paginator(productos, self.paginate_by)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
            context['page_obj'] = page_obj
            context['productos'] = page_obj.object_list
        else:
            context['page_obj'] = None
            context['productos'] = []

        return self.render_to_response(context)
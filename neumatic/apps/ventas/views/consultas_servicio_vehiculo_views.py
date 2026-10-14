# neumatic/apps/ventas/views/consultas_servicio_vehiculo_views.py
from django.http import JsonResponse
from django.db.models import Q

from apps.maestros.models.vehiculo_models import Vehiculo
from apps.maestros.models.producto_models import Producto


def buscar_vehiculo_select2(request):
    """
    Endpoint Select2 para buscar Vehículos por patente, marca o modelo.
    Devuelve: { results: [...], pagination: { more: bool } }
    """
    term = request.GET.get('term', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    qs = Vehiculo.objects.filter(estatus_vehiculo=True).select_related(
        'id_marca_vehiculo', 'id_modelo_vehiculo'
    )

    if term:
        filtro = (
            Q(patente__icontains=term) |
            Q(id_marca_vehiculo__marca_vehiculo__icontains=term) |
            Q(id_modelo_vehiculo__modelo_vehiculo__icontains=term)
        )
        if term.isdigit():
            filtro |= Q(id_vehiculo=int(term))
        qs = qs.filter(filtro)

    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size
    vehiculos = qs.order_by('patente')[start:end]

    results = []
    for v in vehiculos:
        marca = v.id_marca_vehiculo.marca_vehiculo if v.id_marca_vehiculo else ''
        modelo = v.id_modelo_vehiculo.modelo_vehiculo if v.id_modelo_vehiculo else ''
        descripcion = f"{v.patente or 'S/P'} - {marca} {modelo}".strip(' -')
        results.append({
            'id': v.id_vehiculo,
            'text': descripcion,
            'patente': v.patente or '',
            'marca': marca,
            'modelo': modelo,
            'anio': v.anio or '',
        })

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total}
    })


def buscar_producto_servicio_select2(request):
    """
    Endpoint Select2 para buscar Productos de tipo SERVICIO (tipo_producto='S').
    Formato de respuesta compatible con Select2:
        { results: [...], pagination: { more: bool } }
    """
    term = request.GET.get('term', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    qs = Producto.objects.filter(
        estatus_producto=True,
        tipo_producto='S'      # ← SOLO SERVICIOS
    ).select_related('id_marca')

    if term:
        filtro = Q(nombre_producto__icontains=term)
        if term.isdigit():
            filtro |= Q(id_producto=int(term))
            filtro |= Q(codigo_producto__icontains=term)
        qs = qs.filter(filtro)

    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size
    productos = qs.order_by('nombre_producto')[start:end]

    results = []
    for p in productos:
        marca = p.id_marca.nombre_producto_marca if p.id_marca else ''
        results.append({
            'id': p.id_producto,
            'text': f"{p.id_producto} - {p.nombre_producto}",
            'codigo': p.id_producto,
            'medida': p.medida or '',
            'nombre': p.nombre_producto or '',
            'marca': marca,
        })

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total}
    })
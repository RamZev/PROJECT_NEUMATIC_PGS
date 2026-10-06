# neumatic/apps/ventas/views/consultas_movimiento_interno_views.py
from django.http import JsonResponse
from django.db.models import Q

from ...maestros.models.producto_models import Producto
from ...maestros.models.base_models import ProductoStock


def buscar_producto_select2(request):
    """
    Endpoint para el Select2 del panel inline.
    Busca productos por id_producto o nombre_producto.
    Devuelve JSON con el formato esperado por Select2:
      {
        "results": [{"id": ..., "text": "...", "codigo": ..., "medida": ..., "marca": ...}],
        "pagination": {"more": false}
      }
    """
    term = request.GET.get('term', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 20

    qs = Producto.objects.filter(
        estatus_producto=True,
        tipo_producto='P'  # Solo productos físicos (no servicios)
    ).select_related('id_marca')

    if term:
        # Buscar por ID exacto o por nombre (contains)
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
        results.append({
            'id': p.id_producto,
            'text': f"{p.id_producto} - {p.nombre_producto}",
            'codigo': p.id_producto,           # guardamos el id como "código"
            'medida': p.medida or '',
            'nombre': p.nombre_producto or '',
            'marca': p.id_marca.nombre_producto_marca if p.id_marca else '',
        })

    return JsonResponse({
        'results': results,
        'pagination': {'more': end < total}
    })


def detalle_producto_mi(request, id_producto):
    """
    Devuelve los datos de un producto para el panel de previsualización.
    Incluye medida, nombre, marca y código (id_producto).
    """
    try:
        p = Producto.objects.select_related('id_marca').get(id_producto=id_producto)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

    return JsonResponse({
        'id': p.id_producto,
        'codigo': p.id_producto,
        'medida': p.medida or '',
        'nombre': p.nombre_producto or '',
        'marca': p.id_marca.nombre_producto_marca if p.id_marca else '',
    })
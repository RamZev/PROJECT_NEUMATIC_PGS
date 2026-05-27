# neumatic\apps\maestros\views\select2_views.py
# ============================================
# ENDPOINT PARA SELECT2 - BÚSQUEDA DE CLIENTES
# ============================================
from django.http import JsonResponse
from django.db.models import Q
from ..models.cliente_models import Cliente

def buscar_cliente_select2(request):
    """
    Endpoint para Select2 con búsqueda eficiente de clientes
    Soporta búsqueda por ID, nombre o CUIT
    Retorna JSON en formato compatible con Select2
    """
    # Obtener parámetros de la request
    term = request.GET.get('term', '').strip()  # Término de búsqueda
    page = int(request.GET.get('page', 1))       # Número de página
    page_size = 20                               # Resultados por página
    
    # Si no hay término de búsqueda, retornar vacío
    if not term:
        return JsonResponse({'results': [], 'more': False})
    
    # ============================================
    # BÚSQUEDA: Por ID, nombre o CUIT
    # ============================================
    queryset = Cliente.objects.filter(
        Q(id_cliente__icontains=term) |        # Buscar por ID
        Q(nombre_cliente__icontains=term) |    # Buscar por nombre
        Q(cuit__icontains=term)                # Buscar por CUIT
    ).only('id_cliente', 'nombre_cliente', 'cuit').order_by('nombre_cliente')
    
    # Calcular paginación
    total = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    
    # Formatear resultados para Select2
    results = []
    for cliente in queryset[start:end]:
        results.append({
            'id': cliente.id_cliente,
            'text': cliente.nombre_cliente,
            'cuit': cliente.cuit
        })
    
    # Respuesta JSON
    return JsonResponse({
        'results': results,
        'pagination': {
            'more': end < total  # Si hay más resultados para la siguiente página
        }
    })
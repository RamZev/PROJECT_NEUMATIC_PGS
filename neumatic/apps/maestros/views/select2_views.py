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
    Reglas de búsqueda:
    1. Si toda la cadena son dígitos:
       1.1. Primero buscar por id_cliente exacto
       1.2. Si no hay resultado, buscar por id_cliente que contenga los dígitos
       1.3. Si tiene 11 dígitos, buscar por CUIT exacto
    2. Si la cadena tiene caracteres (mezcla de letras y números): buscar por nombre
    """
    # Obtener parámetros de la request
    term = request.GET.get('term', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = 100
    
    # Si no hay término de búsqueda, retornar vacío
    if not term:
        return JsonResponse({'results': [], 'more': False})
    
    # ============================================
    # REGLA 1: Si toda la cadena son dígitos
    # ============================================
    if term.isdigit():
        term_int = int(term)
        queryset = None
        
        # REGLA 1.1: Buscar por id_cliente EXACTO primero
        if Cliente.objects.filter(id_cliente=term_int).exists():
            queryset = Cliente.objects.filter(id_cliente=term_int)
        else:
            # REGLA 1.2: Buscar por id_cliente que CONTENGA los dígitos
            queryset = Cliente.objects.filter(
                Q(id_cliente__icontains=term)
            )
            
            # REGLA 1.3: Si tiene 11 dígitos, también buscar por CUIT exacto
            if len(term) == 11:
                # Unir con búsqueda por CUIT exacto
                queryset = queryset | Cliente.objects.filter(cuit=term_int)
        
        # Eliminar duplicados si los hay
        queryset = queryset.distinct()
    
    # ============================================
    # REGLA 2: Si tiene caracteres (no son solo dígitos)
    # ============================================
    else:
        # Buscar por nombre (contiene el texto)
        queryset = Cliente.objects.filter(
            Q(nombre_cliente__icontains=term)
        )
    
    # ============================================
    # Ordenar y paginar resultados
    # ============================================
    queryset = queryset.only('id_cliente', 'nombre_cliente', 'cuit').order_by('nombre_cliente')
    
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
            'more': end < total
        }
    })
# neumatic\apps\ventas\views\buscar_clientes.py
from django.http import JsonResponse
from apps.maestros.models.cliente_models import Cliente

# Vista para buscar cliente por ID
def buscar_cliente_por_id(request, id_cliente):
    # print("id_cliente::", id_cliente)
    
    try:
        cliente = Cliente.objects.get(id_cliente=id_cliente)
        
        # print("cliente.nombre_cliente", cliente.nombre_cliente)
        return JsonResponse({
            'encontrado': True,
            'id_cliente': cliente.id_cliente,
            'nombre_cliente': cliente.nombre_cliente,
            'cuit': cliente.cuit
        })
    except Cliente.DoesNotExist:
        return JsonResponse({
            'encontrado': False
        })

# Vista para buscar cliente por nombre
def buscar_cliente_por_nombre(request, nombre_cliente):
    clientes = Cliente.objects.filter(nombre__icontains=nombre_cliente)  # Filtramos por nombre que contenga las letras dadas
    if clientes.exists():
        # Si hay coincidencias, retornamos los primeros resultados
        return JsonResponse({
            'encontrado': True,
            'clientes': [{'id_cliente': c.id, 'nombre_cliente': c.nombre, 'cuit': c.cuit} for c in clientes[:5]]  # Limitar a 5 resultados
        })
    else:
        return JsonResponse({
            'encontrado': False
        })

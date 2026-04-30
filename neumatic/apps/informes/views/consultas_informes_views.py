# neumatic\apps\informes\views\consultas_informes_views.py
from django.http import JsonResponse
from django.db.models import Q

from apps.maestros.models.cliente_models import Cliente
from apps.maestros.models.producto_models import Producto
from apps.maestros.models.base_models import ProductoCai


#-- Buscar un cliente por su id.
def buscar_cliente_id(request):
	id_cliente = request.GET.get('id_cliente', '')
	
	if id_cliente:
		try:
			cliente = Cliente.objects.get(id_cliente=id_cliente)
			return JsonResponse({'id_cliente': cliente.id_cliente, 'nombre_cliente': cliente.nombre_cliente})
		except Cliente.DoesNotExist:
			return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
	
	return JsonResponse({'error': 'Código del Cliente no proporcionado'}, status=400)


#-- Búsqueda en Agenda para la ventana Modal de Informes.
def buscar_cliente(request):
	busqueda_general = request.GET.get('busqueda_general', '')
	
	try:
		id_cliente = int(busqueda_general)
		clientes = Cliente.objects.filter(
			Q(id_cliente=id_cliente) |
			Q(nombre_cliente__icontains=busqueda_general)
		)
	except ValueError:
		clientes = Cliente.objects.filter(
			Q(nombre_cliente__icontains=busqueda_general)
		)
	
	resultados = clientes.values(
		'id_cliente',
		'cuit',
		'nombre_cliente',
		'domicilio_cliente',
		'codigo_postal',
		'movil_cliente',
		'email_cliente',
	)
	
	return JsonResponse(list(resultados), safe=False)


#-- Buscar un Producto por su id.
def buscar_producto_por_id(request):
    id_producto = request.GET.get('id_producto', '')
    
    if id_producto:
        try:
            producto = Producto.objects.get(id_producto=id_producto)
            return JsonResponse({
                'encontrado': True,
                'id_producto': producto.id_producto,
                'nombre_producto': producto.nombre_producto,
                'medida': producto.medida,
                'marca_producto': producto.id_marca.nombre_producto_marca,
            })
        except Producto.DoesNotExist:
            return JsonResponse({
                'encontrado': False,
                'error': 'Producto no encontrado',
            })
    
    return JsonResponse({'encontrado': False, 'error': 'Código del Producto no proporcionado'})


#-- Buscar un Producto por CAI.
def buscar_producto_por_cai(request):
	cai = request.GET.get('cai', '')
	
	if cai:
		try:
			#-- Primero buscar el ProductoCai por el campo cai.
			producto_cai = ProductoCai.objects.get(cai=cai)
			
			#-- Luego buscar el primer Producto que tenga este id_cai.
			producto = Producto.objects.filter(id_cai=producto_cai).first()
			
			if producto:
				return JsonResponse({
					'encontrado': True,
					'id_producto': producto.id_producto,
					'nombre_producto': producto.nombre_producto,
					'medida': producto.medida,
					'marca_producto': producto.id_marca.nombre_producto_marca,
				})
			else:
				return JsonResponse({
					'encontrado': False,
					'error': 'No se encontró producto asociado a este CAI',
				})
				
		except ProductoCai.DoesNotExist:
			return JsonResponse({
				'encontrado': False,
				'error': 'CAI no encontrado',
			})
	
	return JsonResponse({'encontrado': False, 'error': 'CAI no proporcionado'})



# neumatic\apps\maestros\views\consulta_views_maestros.py
from django.http import JsonResponse
from ..models.base_models import Localidad

def filtrar_localidad(request):
	id_provincia = request.GET.get('id_provincia')
	
	if id_provincia:
		#-- Filtrar las localidades según la provincia seleccionada.
		localidades = Localidad.objects.filter(
			id_provincia_id=id_provincia, estatus_localidad=True
		).order_by('nombre_localidad').values('id_localidad', 'nombre_localidad', 'codigo_postal')
		
		#-- Convertir los resultados en una lista de diccionarios con nombre completo.
		localidades = [
			{
				'id_localidad': loc['id_localidad'],
				'nombre_completo': f"{loc['nombre_localidad']} - {loc['codigo_postal']}",
				'codigo_postal': loc['codigo_postal']
			}
			for loc in localidades
		]
		
		#-- Devolver los resultados en formato JSON.
		return JsonResponse({'localidad': localidades})
	
	return JsonResponse({'error': 'No se proporcionó el tipo de Provincia'}, status=400)


def verificar_codigo_postal(request):
	codigo_postal = request.GET.get('codigo_postal')
	
	if codigo_postal:
		#-- Obtener la primera localidad que coincida con el código postal.
		localidad = Localidad.objects.filter(codigo_postal=codigo_postal).first()
		
		if localidad:
			#-- Obtener la provincia asociada a la localidad.
			provincia = localidad.id_provincia
			
			#-- Devolver datos de existencia, provincia y localidad en formato JSON.
			return JsonResponse({
				'existe': True,
				'provincia_id': provincia.id_provincia,
				'localidad_id': localidad.id_localidad,
				'localidad_nombre': localidad.nombre_localidad
			})
		else:
			#-- Si no se encuentra ninguna localidad.
			return JsonResponse({'existe': False})
	
	return JsonResponse({'error': 'No se proporcionó el código postal'}, status=400)

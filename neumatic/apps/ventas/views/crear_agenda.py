# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.db import IntegrityError
from apps.maestros.models.cliente_models import Cliente

@csrf_exempt
@login_required
@require_POST
def crear_agenda(request):
    print("Entró a crear Cliente!")
    data = json.loads(request.body)
    
    nro_doc_identidad = data.get('nro_doc_identidad')
    nombre_agenda = data.get('nombre_agenda')
    direccion = data.get('direccion')
    email_1 =  data.get('email_1')
    telefono1 = data.get('telefono1')

    try:
        
        agenda = Cliente(
            nro_doc_identidad=nro_doc_identidad,
            nombre_agenda=nombre_agenda,
            direccion=direccion,
            email_1=email_1,
            telefono1=telefono1
        )
        agenda.save()
        return JsonResponse({'success': True})
    except IntegrityError:
        return JsonResponse({'success': False, 'error': 'Error de integridad en la base de datos'})
    except ValueError as e:
        return JsonResponse({'success': False, 'error': f'Error en los datos: {str(e)}'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error desconocido: {str(e)}'})

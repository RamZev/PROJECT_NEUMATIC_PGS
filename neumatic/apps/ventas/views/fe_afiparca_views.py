# neumatic\apps\ventas\views\fe_afiparca_views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from afip import Afip
# from zeep import Client
# from zeep.exceptions import Fault
import json

@require_GET
def fe_dummy(request):
    """
    Verifica el estado de la infraestructura de AFIP mediante el método FEDummy.
    """
    from zeep import Client
    from zeep.exceptions import Fault

    # Configuración del entorno
    environment = request.GET.get('environment', 'homologacion')
    
    wsdl_url = (
        "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL" if environment == "homologacion"
        else "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL"
    )
    
    result = {"success": False, "AppServer": None, "DbServer": None, "AuthServer": None, "error": None}
    
    try:
        # Crear cliente SOAP
        client = Client(wsdl_url)
        
        # Llamar al método FEDummy
        response = client.service.FEDummy()
        
        # Procesar la respuesta
        result.update({
            "success": True,
            "AppServer": response.AppServer,
            "DbServer": response.DbServer,
            "AuthServer": response.AuthServer
        })
        
    except Fault as fault:
        result["error"] = f"Error SOAP: {fault.message}"
    except Exception as e:
        result["error"] = f"Error general: {str(e)}"
    
    print("result", result)
    
    # Retornar como JSON
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})
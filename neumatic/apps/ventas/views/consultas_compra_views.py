# neumatic\apps\ventas\views\consultas_compra_views.py
from django.http import JsonResponse
from django.db.models import Max
from django.views.decorators.http import require_POST, require_GET

from apps.ventas.models.compra_models import Compra
from apps.maestros.models.proveedor_models import Proveedor
from apps.maestros.models.base_models import ComprobanteCompra


@require_GET
def obtener_numero_compra(request):
    """
    Vista AJAX que devuelve el próximo número de comprobante para una compra
    basado en el id_comprobante_compra seleccionado.
    """
    if request.method == "GET":
        id_comprobante = request.GET.get("id_comprobante")
        if not id_comprobante:
            return JsonResponse({"error": "ID de comprobante no proporcionado"}, status=400)

        try:
            # Obtener el comprobante seleccionado
            comprobante = ComprobanteCompra.objects.get(id_comprobante_compra=id_comprobante)
            compro_codigo = comprobante.codigo_comprobante_compra
            letra = "B"  # letra fija según requerimiento

            # Buscar el último número usado en Compra con esos criterios
            ultimo_numero = Compra.objects.filter(
                id_comprobante_compra_id=id_comprobante,
                compro=compro_codigo,
                letra_comprobante=letra
            ).aggregate(Max('numero_comprobante'))['numero_comprobante__max']

            # Si no hay registros, empezar desde 1
            siguiente_numero = (ultimo_numero or 0) + 1

            return JsonResponse({
                "compro": compro_codigo,
                "letra": letra,
                "numero_comprobante": siguiente_numero
            })

        except ComprobanteCompra.DoesNotExist:
            return JsonResponse({"error": "Comprobante no encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@require_GET
def obtener_alicuota_proveedor(request):
    """
    Vista AJAX que devuelve la alícuota de IVA del proveedor seleccionado.
    """
    id_proveedor = request.GET.get("id_proveedor")
    if not id_proveedor:
        return JsonResponse({"error": "ID de proveedor no proporcionado"}, status=400)

    try:
        proveedor = Proveedor.objects.get(id_proveedor=id_proveedor)
        alicuota = proveedor.ib_alicuota or 0.0  # Si es None, usar 0.0
        return JsonResponse({"alicuota_iva": str(alicuota)})
    except Proveedor.DoesNotExist:
        return JsonResponse({"error": "Proveedor no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


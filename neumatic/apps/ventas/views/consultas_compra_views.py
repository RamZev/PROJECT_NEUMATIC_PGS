# neumatic\apps\ventas\views\consultas_compra_views.py
from django.http import JsonResponse
from django.db.models import Max
from django.views.decorators.http import require_POST, require_GET

from apps.ventas.models.compra_models import Compra
from apps.maestros.models.proveedor_models import Proveedor
from apps.maestros.models.base_models import ComprobanteCompra
from ..models.factura_models import Factura, DetalleFactura


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


@require_GET
def buscar_remito_origen(request):
    import traceback
    from django.http import JsonResponse
    from ..models.factura_models import Factura, DetalleFactura
    
    try:
        numero = request.GET.get('numero', '').strip()
        compro = request.GET.get('compro', '').strip()
        letra = request.GET.get('letra', '').strip()
        
        print("=" * 60)
        print("🔍 DEBUG buscar_remito_origen")
        print(f"   Número: '{numero}'")
        print(f"   Compro: '{compro}'")
        print(f"   Letra: '{letra}'")
        print("=" * 60)
        
        if not numero:
            return JsonResponse({'error': 'Número de remito requerido'}, status=400)
        
        if not compro or not letra:
            return JsonResponse({'error': 'Faltan datos del comprobante (compro o letra)'}, status=400)
        
        if not numero.isdigit() or len(numero) != 10:
            return JsonResponse({'error': 'El número debe tener 10 dígitos'}, status=400)
        
        # BÚSQUEDA POR LOS TRES CAMPOS
        factura = Factura.objects.select_related('id_comprobante_venta').get(
            numero_comprobante=int(numero),
            compro=compro,
            letra_comprobante=letra
        )
        
        # Verificar que no esté facturado
        if factura.estado == 'F':
            return JsonResponse({'error': 'El remito ya fue facturado'}, status=400)
        
        # Verificar que no esté ya utilizado
        from ..models.compra_models import Compra
        if Compra.objects.filter(id_factura_origen=factura).exists():
            return JsonResponse({'error': 'Este remito ya fue utilizado en otra compra'}, status=400)
        
        # Obtener detalles
        detalles = DetalleFactura.objects.filter(id_factura=factura).select_related('id_producto')
        
        if not detalles.exists():
            return JsonResponse({'error': 'El remito no tiene detalles'}, status=404)
        
        data = {
            'id_factura': factura.id_factura,
            'numero_comprobante': factura.numero_comprobante,
            'detalles': []
        }
        
        for detalle in detalles:
            data['detalles'].append({
                'id_producto': detalle.id_producto.id_producto,
                'medida': detalle.id_producto.medida or '',
                'nombre': detalle.producto_venta,
                'cantidad': float(detalle.cantidad),
                'precio': float(detalle.precio),
                'total': float(detalle.total),
            })
        
        return JsonResponse(data)
        
    except Factura.DoesNotExist:
        return JsonResponse({'error': f'Remito no encontrado: {compro} {letra} {numero}'}, status=404)
    except Exception as e:
        # 🔥 ESTO ES LO IMPORTANTE: capturar cualquier error y devolver JSON
        print("❌ ERROR EN buscar_remito_origen:")
        traceback.print_exc()
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
def validar_vencimientos_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.filter(pk=cliente_id).first()
        if not cliente:
            return JsonResponse({'error': 'Cliente no encontrado', 'requiere_autorizacion': False}, status=404)

        factura_antigua = Factura.objects.filter(
            id_cliente_id=cliente_id,
            condicion_comprobante=2,
            total__gt=0
        ).exclude(
            total=F('entrega')
        ).select_related('id_vendedor', 'id_comprobante_venta'
        ).order_by('fecha_comprobante').first()

        if not factura_antigua:
            return JsonResponse({'requiere_autorizacion': False})

        dias_credito = factura_antigua.id_vendedor.vence_factura if factura_antigua.id_vendedor else 0
        fecha_vencimiento = factura_antigua.fecha_comprobante + timedelta(days=dias_credito)
        dias_vencidos = (date.today() - fecha_vencimiento).days

        return JsonResponse({
            'requiere_autorizacion': dias_vencidos > 0,
            'datos_comprobante': {
                'tipo_comprobante': factura_antigua.id_comprobante_venta.nombre_comprobante_venta if factura_antigua.id_comprobante_venta else 'N/A',
                'letra_comprobante': factura_antigua.letra_comprobante or 'N/A',
                'numero_comprobante': factura_antigua.numero_comprobante or 'N/A',
                'fecha_comprobante': factura_antigua.fecha_comprobante.strftime('%d/%m/%Y') if factura_antigua.fecha_comprobante else 'N/A',
                'dias_credito': dias_credito,
                'fecha_vencimiento': fecha_vencimiento.strftime('%d/%m/%Y') if fecha_vencimiento else 'N/A',
                'dias_vencidos': dias_vencidos,
                'monto_pendiente': float((factura_antigua.total or 0) - (factura_antigua.entrega or 0)),
                'vendedor': factura_antigua.id_vendedor.nombre_vendedor if factura_antigua.id_vendedor else 'No asignado'
            }
        })

    except Exception as e:
        print(f"Error completo en validar_vencimientos_cliente - Cliente ID: {cliente_id}: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'Error interno al validar vencimientos',
            'requiere_autorizacion': True,  # Importante: fallar hacia la seguridad
            'detalle_error': str(e),
            'cliente_id': cliente_id  # Para debugging
        }, status=500)


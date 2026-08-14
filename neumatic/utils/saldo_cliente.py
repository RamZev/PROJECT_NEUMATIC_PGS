# neumatic\utils\saldo_cliente.py
from django.db import connection
from apps.maestros.models.cliente_models import Cliente


def obtener_saldo_cliente(cliente_id):
    """
    Obtiene el saldo y datos financieros de un cliente desde la vista VLSaldosClientes
    
    Args:
        cliente_id (int): ID del cliente
    
    Returns:
        dict: Diccionario con los datos del saldo o None si no existe
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                id_cliente_id,
                nombre_cliente,
                id_vendedor_id,
                nombre_vendedor,
                CAST(SUM(total * (mult_saldo * 1.00)) AS NUMERIC(14,2)) AS saldo,
                MIN(CASE WHEN condicion_comprobante = 2 AND mult_saldo <> 0 AND total <> entrega 
                    THEN fecha_comprobante END) AS primer_fact_impaga,
                MAX(fecha_pago) AS ultimo_pago
            FROM VLSaldosClientes
            WHERE id_cliente_id = %s
            GROUP BY
                id_cliente_id,
                nombre_cliente,
                id_vendedor_id,
                nombre_vendedor
        """, [cliente_id])
        
        row = cursor.fetchone()
        
        if row:
            return {
                'id_cliente': row[0],
                'nombre_cliente': row[1],
                'id_vendedor': row[2],
                'nombre_vendedor': row[3],
                'saldo': float(row[4]) if row[4] else 0.0,
                'primer_fact_impaga': row[5].strftime('%Y-%m-%d') if row[5] else None,
                'ultimo_pago': row[6].strftime('%Y-%m-%d') if row[6] else None,
            }
    
    return None


def check_limite_credito(cliente_id, monto_operacion=None):
    """
    Verifica si un cliente supera su límite de crédito.
    Retorna un dict con toda la información, o None si el cliente no existe.

    Args:
        cliente_id (int): ID del cliente.
        monto_operacion (float, optional): Monto de la nueva operación (ej. total factura).
            Si se omite, solo evalúa el saldo actual.

    Returns:
        dict: {
            'cliente': Objeto Cliente,
            'saldo': float,
            'limite': float,
            'supera_limite': bool,
            'necesita_autorizacion': bool,
            'saldo_proyectado': float (si se pasó monto_operacion),
            'primer_fact_impaga': str o None,
            'ultimo_pago': str o None,
        }
    """
    try:
        cliente = Cliente.objects.get(id_cliente=cliente_id)
    except Cliente.DoesNotExist:
        return None

    limite = cliente.limite_credito or 0.0
    saldo_data = obtener_saldo_cliente(cliente_id)
    saldo = saldo_data['saldo'] if saldo_data else 0.0

    if monto_operacion is not None:
        saldo_proyectado = saldo + monto_operacion
        supera = saldo_proyectado > limite
    else:
        saldo_proyectado = saldo
        supera = saldo > limite

    return {
        'cliente': cliente,
        'saldo': saldo,
        'limite': float(limite),
        'supera_limite': supera,
        'necesita_autorizacion': supera,
        'saldo_proyectado': saldo_proyectado,
        'primer_fact_impaga': saldo_data.get('primer_fact_impaga') if saldo_data else None,
        'ultimo_pago': saldo_data.get('ultimo_pago') if saldo_data else None,
    }
# neumatic\utils\saldo_cliente.py
from django.db import connection


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
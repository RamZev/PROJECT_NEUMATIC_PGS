# services/numeracion_cache.py
import time
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

def obtener_proximo_numero_afip(pto_vta, cbte_tipo, afip_client):
    """
    Obtiene el próximo número de AFIP con control de concurrencia
    
    Args:
        pto_vta: Punto de venta (ej: "0001")
        cbte_tipo: Tipo de comprobante (ej: 1)
        afip_client: Instancia de AFIPSimpleClient
    
    Returns:
        int: Próximo número a usar
    
    Raises:
        Exception: Si no se puede obtener después de reintentos
    """
    max_intentos = 3
    
    for intento in range(max_intentos):
        try:
            # 1. Crear clave única para el lock
            lock_key = f"afip_lock:{pto_vta}:{cbte_tipo}"
            
            # 2. Generar valor único para identificar quién tiene el lock
            lock_valor = f"{time.time():.6f}"  # Timestamp con microsegundos
            
            # 3. INTENTAR OBTENER LOCK (operación atómica)
            # cache.add() solo devuelve True si la clave NO existía
            lock_obtenido = cache.add(lock_key, lock_valor, timeout=10)
            
            if not lock_obtenido:
                # Otro proceso tiene el lock, esperar un poco
                tiempo_espera = 0.1 * (intento + 1)
                logger.debug(f"Lock ocupado, esperando {tiempo_espera}s...")
                time.sleep(tiempo_espera)
                continue
            
            # 4. ¡TENEMOS EL LOCK! Consultar AFIP
            try:
                logger.info(f"Lock obtenido para {pto_vta}-{cbte_tipo:03d}")
                
                # Consultar último número autorizado por AFIP
                ultimo_afip = afip_client.obtener_ultimo_autorizado(pto_vta, cbte_tipo)
                
                # Calcular próximo número
                proximo_numero = ultimo_afip + 1
                
                logger.info(f"Número obtenido: {pto_vta}-{proximo_numero:08d}")
                return proximo_numero
                
            finally:
                # 5. LIBERAR LOCK (siempre se ejecuta, incluso con errores)
                # Solo liberar si todavía somos los dueños
                if cache.get(lock_key) == lock_valor:
                    cache.delete(lock_key)
                    logger.debug(f"Lock liberado para {pto_vta}-{cbte_tipo:03d}")
                    
        except Exception as e:
            logger.warning(f"Intento {intento + 1} falló: {str(e)}")
            
            if intento < max_intentos - 1:
                # Esperar antes de reintentar (backoff exponencial)
                tiempo_espera = 0.5 * (2 ** intento)
                time.sleep(tiempo_espera)
                continue
            
            # Último intento falló
            logger.error(f"No se pudo obtener número después de {max_intentos} intentos")
            raise Exception(f"No se pudo obtener número: {str(e)}")
    
    # Nunca debería llegar aquí, pero por seguridad
    raise Exception("Error inesperado en obtención de número")
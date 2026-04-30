# utils/afip_simple.py
import requests
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

class AFIPSimpleClient:
    """
    Cliente mínimo para consultar AFIP
    Solo hace lo esencial: consultar último número autorizado
    """
    
    def __init__(self, token, sign, cuit, ambiente="homologacion"):
        """
        Inicializar con credenciales
        
        Args:
            token: Token de autenticación
            sign: Firma digital
            cuit: CUIT del emisor
            ambiente: "homologacion" o "produccion"
        """
        self.token = token
        self.sign = sign
        self.cuit = cuit
        
        # URLs según ambiente
        self.wsfe_url = (
            "https://wswhomo.afip.gov.ar/wsfev1/service.asmx" 
            if ambiente == "homologacion" 
            else "https://servicios1.afip.gov.ar/wsfev1/service.asmx"
        )
    
    def obtener_ultimo_autorizado(self, pto_vta, cbte_tipo):
        """
        Consulta AFIP por el último número autorizado
        
        Args:
            pto_vta: Punto de venta (ej: "0001")
            cbte_tipo: Tipo de comprobante (ej: 1 para Factura A)
        
        Returns:
            int: Último número autorizado (0 si no hay)
        """
        try:
            # Construir XML de consulta
            xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <FECompUltimoAutorizado xmlns="http://ar.gov.afip.dif.FEV1/">
            <Auth>
                <Token>{self.token}</Token>
                <Sign>{self.sign}</Sign>
                <Cuit>{self.cuit}</Cuit>
            </Auth>
            <PtoVta>{pto_vta}</PtoVta>
            <CbteTipo>{cbte_tipo:03d}</CbteTipo>
        </FECompUltimoAutorizado>
    </soap:Body>
</soap:Envelope>"""
            
            # Headers necesarios
            headers = {
                'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': 'http://ar.gov.afip.dif.FEV1/FECompUltimoAutorizado'
            }
            
            # Enviar consulta a AFIP
            response = requests.post(
                self.wsfe_url,
                data=xml,
                headers=headers,
                timeout=30  # 30 segundos timeout
            )
            
            # Verificar respuesta HTTP
            if response.status_code != 200:
                logger.error(f"AFIP respondió con error HTTP {response.status_code}")
                return 0
            
            # Parsear respuesta XML
            root = ET.fromstring(response.content)
            ns = {'ns': 'http://ar.gov.afip.dif.FEV1/'}
            
            # Buscar resultado
            resultado = root.find('.//ns:Resultado', ns)
            cbte_nro = root.find('.//ns:CbteNro', ns)
            
            if resultado is not None and resultado.text == 'A' and cbte_nro is not None:
                numero = int(cbte_nro.text)
                logger.debug(f"AFIP último autorizado: {pto_vta}-{cbte_tipo:03d} = {numero}")
                return numero
            else:
                # No hay comprobantes o error
                logger.debug(f"No hay comprobantes para {pto_vta}-{cbte_tipo:03d}, devolviendo 0")
                return 0
                
        except requests.exceptions.Timeout:
            logger.error("Timeout consultando AFIP")
            return 0
        except requests.exceptions.ConnectionError:
            logger.error("Error de conexión con AFIP")
            return 0
        except Exception as e:
            logger.error(f"Error inesperado consultando AFIP: {str(e)}")
            return 0
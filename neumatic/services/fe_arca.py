# neumatic\services\fe_arca.py
import base64
import xml.etree.ElementTree as ET
import json
import requests
import os
import ssl
import urllib3
import time
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

from apps.maestros.models.empresa_models import Empresa

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AFIPAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_context=ctx)

class FacturadorARCA:
    def __init__(self, homologacion=True, empresa=None):
        """
        Inicializa el facturador.
        homologacion: True para homologación, False para producción
        empresa: instancia de Empresa (opcional). Si no se provee, se obtiene de la BD
        """
        # Si se proporciona empresa, usar sus datos para determinar homologacion
        if empresa:
            self.empresa = empresa
            # El modo de la empresa tiene prioridad sobre el parámetro homologacion
            self.homologacion = (empresa.ws_modo == 1)
        else:
            self.empresa = Empresa.objects.first()
            self.homologacion = homologacion
        
        self.entorno = "homologacion" if self.homologacion else "produccion"
        
        if self.homologacion:
            self.url_wsaa = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms"
            self.url_wsfe = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx"
        else:
            self.url_wsaa = "https://wsaa.afip.gov.ar/ws/services/LoginCms"
            self.url_wsfe = "https://servicios1.afip.gov.ar/wsfev1/service.asmx"

        self.session = requests.Session()
        self.session.mount("https://", AFIPAdapter())


    def verificar_vigencia_certificado(self):
        """Verifica si el certificado está vigente"""
        from django.utils import timezone
        
        if not hasattr(self, 'empresa') or not self.empresa:
            return True, "No hay empresa configurada, se omite validación"
        
        vence = self.empresa.ws_vence_h if self.homologacion else self.empresa.ws_vence_p
        if not vence:
            return True, "Certificado sin fecha de vencimiento"
        
        # Asegurar que vence sea aware para comparar
        if timezone.is_naive(vence):
            vence = timezone.make_aware(vence)
        
        ahora = timezone.now()
        if ahora > vence:
            return False, f"Certificado vencido el {vence.strftime('%d/%m/%Y')}"
        
        return True, f"Certificado vigente hasta {vence.strftime('%d/%m/%Y')}"

    
    def verificar_token_vigente(self):
        """Verifica si el token guardado en BD está vigente"""
        from django.utils import timezone
        
        if not hasattr(self, 'empresa') or not self.empresa:
            return False
        
        if self.homologacion:
            token = self.empresa.ws_token_h
            sign = self.empresa.ws_sign_h
            expiracion = self.empresa.ws_expiracion_h
        else:
            token = self.empresa.ws_token_p
            sign = self.empresa.ws_sign_p
            expiracion = self.empresa.ws_expiracion_p
        
        if not token or not sign or not expiracion:
            return False
        
        # ===== CORRECCIÓN: Asegurar que expiracion sea aware para comparar =====
        if timezone.is_naive(expiracion):
            expiracion = timezone.make_aware(expiracion)
        # ========================================================================
        
        ahora = timezone.now()
        
        # Dar 5 minutos de margen
        if ahora < (expiracion - timedelta(minutes=5)):
            return True
        
        return False
    
    def guardar_token_sign(self, token, sign, expiracion):
        """Guarda token y sign en el modelo Empresa"""
        from django.utils import timezone
        
        if not hasattr(self, 'empresa') or not self.empresa:
            return
        
        try:
            # Asegurar que expiracion sea naive si la BD espera naive
            if timezone.is_aware(expiracion):
                expiracion = timezone.make_naive(expiracion)
            
            if self.homologacion:
                self.empresa.ws_token_h = token
                self.empresa.ws_sign_h = sign
                self.empresa.ws_expiracion_h = expiracion
            else:
                self.empresa.ws_token_p = token
                self.empresa.ws_sign_p = sign
                self.empresa.ws_expiracion_p = expiracion
            
            self.empresa.save(update_fields=[
                f'ws_token_{"h" if self.homologacion else "p"}',
                f'ws_sign_{"h" if self.homologacion else "p"}',
                f'ws_expiracion_{"h" if self.homologacion else "p"}'
            ])
            print(f"✅ Token guardado en base de datos ({self.entorno})")
        except Exception as e:
            print(f"⚠️ Error guardando token en BD: {e}")
    
    def realizar_request_afip(self, url, data=None, headers=None, metodo='POST'):
        try:
            response = self.session.post(url, data=data, headers=headers, timeout=60, verify=False)
            return response
        except Exception as e:
            print(f"❌ Error en conexión {self.entorno}: {str(e)[:100]}")
            raise

    def obtener_token_sign(self, cert_path=None, key_path=None, service="wsfe"):
        """
        Obtiene token y sign.
        Si hay empresa configurada, usa BD para caché y certificados de BD.
        Si no, usa el método original con archivos.
        """
        from django.utils import timezone
        
        # Si tenemos empresa, intentar usar BD para caché
        if hasattr(self, 'empresa') and self.empresa:
            # Verificar vigencia del certificado
            vigente, mensaje = self.verificar_vigencia_certificado()
            if not vigente:
                raise ValueError(f"❌ {mensaje}")
            print(f"✅ {mensaje}")
            
            # Verificar si hay token vigente en BD
            if self.verificar_token_vigente():
                print(f"✅ Token vigente cargado desde BD ({self.entorno})")
                if self.homologacion:
                    return self.empresa.ws_token_h, self.empresa.ws_sign_h
                else:
                    return self.empresa.ws_token_p, self.empresa.ws_sign_p
        
        # Si no tenemos empresa o no hay token vigente, usar método original con archivos
        archivo_json = f"acceso_arca_{self.entorno}.json"
        
        # Intentar cargar desde archivo JSON (método original)
        if os.path.exists(archivo_json):
            with open(archivo_json, "r") as f:
                data = json.load(f)
                if datetime.now() < datetime.strptime(data["expira"], "%Y-%m-%d %H:%M:%S"):
                    print(f"✅ Token cargado desde caché ({self.entorno})")
                    return data["token"], data["sign"]

        # Determinar rutas de certificados
        if cert_path is None or key_path is None:
            # Si no se proporcionaron rutas pero tenemos empresa, usar contenido de BD
            if hasattr(self, 'empresa') and self.empresa:
                cert_content = self.empresa.ws_archivo_crt2 if self.homologacion else self.empresa.ws_archivo_crt_p
                key_content = self.empresa.ws_archivo_key2 if self.homologacion else self.empresa.ws_archivo_key_p
                
                # Crear archivos temporales
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.crt', delete=False) as f_cert:
                    f_cert.write(cert_content)
                    cert_path_temp = f_cert.name
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.key', delete=False) as f_key:
                    f_key.write(key_content)
                    key_path_temp = f_key.name
                
                cert_path = cert_path_temp
                key_path = key_path_temp
                usar_temp = True
            else:
                raise ValueError("Se requieren rutas de certificados o una empresa configurada")
        else:
            usar_temp = False

        print(f"🔐 Firmando TRA con certificado: {cert_path}")
        
        # ===== CORRECCIÓN: Usar timezone.now() en lugar de datetime.now() =====
        # Usar datetime.now() en UTC para evitar problemas de zona horaria
        now_utc = datetime.now() - timedelta(minutes=5)
        exp_utc = now_utc + timedelta(hours=12)
        
        # Convertir a string ISO sin información de zona horaria
        now_str = now_utc.strftime("%Y-%m-%dT%H:%M:%S")
        exp_str = exp_utc.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Guardar exp como aware para la BD (si es necesario)
        from django.utils import timezone
        exp = timezone.make_aware(exp_utc) if timezone.is_naive(exp_utc) else exp_utc
        # ======================================================================
        
        tra = f"""<?xml version="1.0" encoding="UTF-8"?>
        <loginTicketRequest version="1.0">
          <header>
            <uniqueId>{int(now_utc.timestamp())}</uniqueId>
            <generationTime>{now_str}</generationTime>
            <expirationTime>{exp_str}</expirationTime>
          </header>
          <service>{service}</service>
        </loginTicketRequest>""".encode('utf-8')

        with open(cert_path, "rb") as f: cert = x509.load_pem_x509_certificate(f.read())
        with open(key_path, "rb") as f: key = serialization.load_pem_private_key(f.read(), password=None)
        
        builder = pkcs7.PKCS7SignatureBuilder().set_data(tra).add_signer(cert, key, hashes.SHA256())
        cms = base64.b64encode(builder.sign(serialization.Encoding.DER, options=[])).decode('utf-8')

        soap = f"""<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsaa="http://wsaa.view.xfire.ao.do.afip.gov.ar">
          <soapenv:Body><wsaa:loginCms><wsaa:in0>{cms}</wsaa:in0></wsaa:loginCms></soapenv:Body>
        </soapenv:Envelope>"""
        
        resp = self.realizar_request_afip(self.url_wsaa, soap, {'Content-Type': 'text/xml;charset=UTF-8', 'SOAPAction': ''})
        
        # === DEBUG: Ver qué devuelve WSAA ===
        print(f"📥 Código respuesta WSAA: {resp.status_code}")
        print(f"📥 Respuesta WSAA completa:")
        print(resp.text)
        print("="*60)
        # ====================================
        
        if resp.status_code != 200:
            raise ValueError(f"Error en WSAA: Código {resp.status_code}")
        
        root = ET.fromstring(resp.text)
        ticket_xml = root.find(".//{http://wsaa.view.xfire.ao.do.afip.gov.ar}loginCmsReturn").text
        ticket_root = ET.fromstring(ticket_xml)
        token, sign = ticket_root.find(".//token").text, ticket_root.find(".//sign").text

        # Guardar en archivo JSON (usando formato string, no afecta)
        with open(archivo_json, "w") as f:
            json.dump({"token": token, "sign": sign, "expira": exp.strftime("%Y-%m-%d %H:%M:%S")}, f, indent=4)
        print(f"✅ Nuevo token guardado en {archivo_json}")
        
        # Si tenemos empresa, guardar también en BD (exp ya es aware)
        if hasattr(self, 'empresa') and self.empresa:
            self.guardar_token_sign(token, sign, exp)
        
        # Limpiar archivos temporales si se crearon
        if usar_temp:
            os.unlink(cert_path)
            os.unlink(key_path)
        
        return token, sign

    
    def obtener_proximo_numero(self, pv, tipo, token, sign, cuit):
        print(f"🔍 Consultando último comprobante autorizado ({self.entorno})...")
        soap = f"""<?xml version="1.0" encoding="UTF-8"?>
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
          <soap12:Body>
            <FECompUltimoAutorizado xmlns="http://ar.gov.afip.dif.FEV1/">
              <Auth><Token>{token}</Token><Sign>{sign}</Sign><Cuit>{cuit}</Cuit></Auth>
              <PtoVta>{pv}</PtoVta><CbteTipo>{tipo}</CbteTipo>
            </FECompUltimoAutorizado>
          </soap12:Body>
        </soap12:Envelope>"""
        
        headers = {'Content-Type': 'text/xml; charset=utf-8', 'SOAPAction': '"http://ar.gov.afip.dif.FEV1/FECompUltimoAutorizado"'}
        resp = self.realizar_request_afip(self.url_wsfe, soap, headers)
        root = ET.fromstring(resp.text)
        ns = {'ar': 'http://ar.gov.afip.dif.FEV1/'}
        cbte_nro = root.find('.//ar:CbteNro', ns)
        
        if cbte_nro is not None and cbte_nro.text:
            ultimo = int(cbte_nro.text)
            return ultimo + 1, ultimo
        return 1, 0

    def enviar_solicitud_cae(self, xml_content):
        headers = {'Content-Type': 'text/xml; charset=utf-8', 'SOAPAction': 'http://ar.gov.afip.dif.FEV1/FECAESolicitar'}
        resp = self.realizar_request_afip(self.url_wsfe, xml_content, headers)
        return resp.text
    
    def formatear_xml(self, xml_string):
        """Formatea el XML para que sea legible (pretty print)"""
        from xml.dom import minidom
        try:
            dom = minidom.parseString(xml_string)
            xml_formateado = dom.toprettyxml(indent="    ", encoding='utf-8').decode('utf-8')
            xml_formateado = '\n'.join([line for line in xml_formateado.splitlines() if line.strip()])
            return xml_formateado
        except Exception as e:
            print(f"⚠️ Error al formatear XML: {e}")
            return xml_string

    def procesar_respuesta_cae(self, respuesta_xml):
        """Procesa la respuesta de ARCA y extrae el CAE y otros datos"""
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(respuesta_xml)
            ns = {'ar': 'http://ar.gov.afip.dif.FEV1/'}
            
            resultado = root.find('.//ar:Resultado', ns)
            
            if resultado is not None and resultado.text == 'A':
                cae = root.find('.//ar:CAE', ns)
                vencimiento = root.find('.//ar:CAEFchVto', ns)
                cbte_desde = root.find('.//ar:CbteDesde', ns)
                cbte_hasta = root.find('.//ar:CbteHasta', ns)
                
                eventos = []
                for evt in root.findall('.//ar:Evt', ns):
                    codigo = evt.find('ar:Code', ns)
                    msg = evt.find('ar:Msg', ns)
                    if codigo is not None and msg is not None:
                        eventos.append(f"{codigo.text}: {msg.text}")
                
                return {
                    'aprobado': True,
                    'cae': cae.text if cae is not None else None,
                    'vencimiento': vencimiento.text if vencimiento is not None else None,
                    'cbte_desde': cbte_desde.text if cbte_desde is not None else None,
                    'cbte_hasta': cbte_hasta.text if cbte_hasta is not None else None,
                    'errores': [],
                    'eventos': eventos,
                    'respuesta_completa': respuesta_xml
                }
            else:
                errores = []
                for error in root.findall('.//ar:Err', ns):
                    codigo = error.find('ar:Codigo', ns)
                    descripcion = error.find('ar:Descripcion', ns)
                    if codigo is not None and descripcion is not None:
                        errores.append(f"{codigo.text}: {descripcion.text}")
                
                eventos = []
                for evt in root.findall('.//ar:Evt', ns):
                    codigo = evt.find('ar:Code', ns)
                    msg = evt.find('ar:Msg', ns)
                    if codigo is not None and msg is not None:
                        eventos.append(f"{codigo.text}: {msg.text}")
                
                return {
                    'aprobado': False,
                    'cae': None,
                    'vencimiento': None,
                    'cbte_desde': None,
                    'cbte_hasta': None,
                    'errores': errores,
                    'eventos': eventos,
                    'respuesta_completa': respuesta_xml
                }
                
        except Exception as e:
            return {
                'aprobado': False,
                'cae': None,
                'vencimiento': None,
                'cbte_desde': None,
                'cbte_hasta': None,
                'errores': [f"Error procesando respuesta: {str(e)}"],
                'eventos': [],
                'respuesta_completa': respuesta_xml
            }
# neumatic\services\fe_arca_test.py
import os
import re
import time
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from fe_arca import FacturadorARCA

load_dotenv()

MODO_HOMOLOGACION = True
XML_FILE = os.getenv("XML_FILE", "001_0021_00058812_Solicitud2.xml")
CUIT = os.getenv("CUIT_CERTIFICADO")
CERT = os.getenv("CERT_PATH") if MODO_HOMOLOGACION else os.getenv("CERT_PATH_P")
KEY = os.getenv("KEY_PATH") if MODO_HOMOLOGACION else os.getenv("KEY_PATH_P")

def extraer_datos_xml(path):
    print(f"\n🔍 Extrayendo datos del XML: {path}")
    tree = ET.parse(path)
    root = tree.getroot()
    ns = {'ar': 'http://ar.gov.afip.dif.FEV1/'}
    
    fe_cab = root.find('.//ar:FeCabReq', ns)
    pv = int(fe_cab.find('ar:PtoVta', ns).text.strip())
    tipo = int(fe_cab.find('ar:CbteTipo', ns).text.strip())
    
    det = root.find('.//ar:FECAEDetRequest', ns)
    desde = int(det.find('ar:CbteDesde', ns).text.strip())
    
    print(f"✅ PtoVta: {pv} | Tipo: {tipo} | Número actual en XML: {desde}")
    return pv, tipo, desde

def actualizar_xml_arca(path, token, sign, numero):
    print(f"✏️  Actualizando Token, Sign y Número ({numero}) en XML...")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'<Token>.*?</Token>', f'<Token>{token}</Token>', content, flags=re.DOTALL)
    content = re.sub(r'<Sign>.*?</Sign>', f'<Sign>{sign}</Sign>', content, flags=re.DOTALL)
    num_fmt = f"{numero:8d}"
    content = re.sub(r'<CbteDesde>.*?</CbteDesde>', f'<CbteDesde>{num_fmt}</CbteDesde>', content, flags=re.DOTALL)
    content = re.sub(r'<CbteHasta>.*?</CbteHasta>', f'<CbteHasta>{num_fmt}</CbteHasta>', content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return content

def main():
    arca = FacturadorARCA(homologacion=MODO_HOMOLOGACION)
    print("="*60)
    print(f"📄 PROCESO DE AUTORIZACIÓN DE COMPROBANTE ({arca.entorno.upper()})")
    print("="*60)

    try:
        pv, tipo, desde_orig = extraer_datos_xml(XML_FILE)
        token, sign = arca.obtener_token_sign(CERT, KEY)

        for intento in range(4):
            print(f"\n" + "-"*30)
            print(f"🔄 INTENTO #{intento + 1} de 4")
            print("-"*30)
            
            proximo, ultimo = arca.obtener_proximo_numero(pv, tipo, token, sign, CUIT)
            print(f"✅ WSFE Status: 200")
            print(f"✅ Último autorizado: {ultimo} → PRÓXIMO NÚMERO A USAR: {proximo}")

            xml_final = actualizar_xml_arca(XML_FILE, token, sign, proximo)

            print(f"\n🚀 ENVIANDO SOLICITUD DE CAE A AFIP ({arca.entorno.upper()})")
            respuesta = arca.enviar_solicitud_cae(xml_final)
            print(f"✅ Respuesta recibida")

            if "<Resultado>A</Resultado>" in respuesta:
                print("\n" + "="*60)
                print("🎉 ¡CAE OBTENIDO EXITOSAMENTE!")
                print("="*60)
                return True
            
            if "10016" in respuesta:
                print(f"⚠️  Error 10016 detectado (colisión numérica o fecha inválida)")
                if intento < 3:
                    espera = 0.5 * (intento + 1)
                    print(f"⏳ Esperando {espera}s para reintentar con número fresco...")
                    time.sleep(espera)
                    continue
            
            print(f"❌ Error ARCA no recuperable:\n{respuesta[:500]}")
            break
                
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    main()
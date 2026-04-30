# neumatic\services\fe_arca_test2.py
import os
import re
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
from dotenv import load_dotenv
from pathlib import Path

# Configurar Django para acceder a los modelos
import django
import sys

# Agregar la ruta del proyecto al sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.maestros.models.empresa_models import Empresa
from fe_arca import FacturadorARCA

load_dotenv()

MODO_HOMOLOGACION = True  # Se usará como fallback si no hay empresa
XML_FILE = os.getenv("XML_FILE", "001_0022_00024542_Solicitud.xml")

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
    # Para ARCA, el número va sin formato especial (solo el número)
    content = re.sub(r'<CbteDesde>.*?</CbteDesde>', f'<CbteDesde>{numero}</CbteDesde>', content, flags=re.DOTALL)
    content = re.sub(r'<CbteHasta>.*?</CbteHasta>', f'<CbteHasta>{numero}</CbteHasta>', content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return content

def formatear_xml(xml_string):
    """Formatea el XML para que sea legible (pretty print)"""
    try:
        # Parsear el XML
        dom = minidom.parseString(xml_string)
        # Formatear con indentación
        xml_formateado = dom.toprettyxml(indent="    ", encoding='utf-8').decode('utf-8')
        # Eliminar líneas en blanco extras (opcional)
        xml_formateado = '\n'.join([line for line in xml_formateado.splitlines() if line.strip()])
        return xml_formateado
    except Exception as e:
        print(f"⚠️ Error al formatear XML: {e}")
        return xml_string  # Devolver el original si hay error

def procesar_respuesta_cae(respuesta_xml):
    """Procesa la respuesta de ARCA y extrae el CAE y otros datos"""
    try:
        root = ET.fromstring(respuesta_xml)
        ns = {'ar': 'http://ar.gov.afip.dif.FEV1/'}
        
        # Buscar resultado en FeDetResp
        resultado = root.find('.//ar:Resultado', ns)
        
        if resultado is not None and resultado.text == 'A':
            # Extraer datos del comprobante
            cae = root.find('.//ar:CAE', ns)
            vencimiento = root.find('.//ar:CAEFchVto', ns)
            cbte_desde = root.find('.//ar:CbteDesde', ns)
            cbte_hasta = root.find('.//ar:CbteHasta', ns)
            
            # Extraer eventos/observaciones
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
            # Buscar errores
            errores = []
            for error in root.findall('.//ar:Err', ns):
                codigo = error.find('ar:Codigo', ns)
                descripcion = error.find('ar:Descripcion', ns)
                if codigo is not None and descripcion is not None:
                    errores.append(f"{codigo.text}: {descripcion.text}")
            
            # También buscar eventos (pueden haber aunque no esté aprobado)
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

def guardar_xml_respuesta(respuesta_xml, xml_path):
    """Guarda la respuesta XML formateada en la misma carpeta que el XML de solicitud"""
    # Formatear el XML para que sea legible
    xml_formateado = formatear_xml(respuesta_xml)
    
    # Generar nombre de archivo para la respuesta
    archivo_respuesta = xml_path.parent / f"{xml_path.stem}_Respuesta.xml"
    
    with open(archivo_respuesta, 'w', encoding='utf-8') as f:
        f.write(xml_formateado)
    
    print(f"✅ Respuesta guardada (formateada) en: {archivo_respuesta}")
    return archivo_respuesta

def main():
    print("="*60)
    print("📄 TEST DE INTEGRACIÓN CON ARCA - SOLICITUD DE CAE")
    print("="*60)
    
    try:
        # Obtener la empresa desde la base de datos
        empresa = Empresa.objects.first()
        if not empresa:
            print("❌ No hay empresas configuradas en el sistema")
            return
        
        print(f"🏢 Empresa: {empresa.nombre_fiscal}")
        print(f"🔢 CUIT: {empresa.cuit}")
        print(f"🌐 Modo: {'Homologación' if empresa.ws_modo == 1 else 'Producción'}")
        
        # Crear facturador con la empresa
        arca = FacturadorARCA(empresa=empresa)
        print(f"✅ Facturador inicializado en entorno: {arca.entorno.upper()}")
        
        # Obtener ruta completa del XML
        xml_path = Path(XML_FILE)
        if not xml_path.is_absolute():
            # Si es ruta relativa, asumir que está en el mismo directorio
            xml_path = Path(__file__).parent / XML_FILE
        
        # Extraer datos del XML
        pv, tipo, desde_orig = extraer_datos_xml(str(xml_path))
        
        # Obtener token y sign (automáticamente usa caché de BD si está vigente)
        print(f"\n🔐 Solicitando token...")
        token, sign = arca.obtener_token_sign()
        print(f"✅ Token obtenido")
        
        # Intentar hasta 4 veces en caso de error 10016
        for intento in range(4):
            print(f"\n" + "-"*30)
            print(f"🔄 INTENTO #{intento + 1} de 4")
            print("-"*30)
            
            # Obtener el próximo número de ARCA
            print(f"\n🔍 Consultando último comprobante autorizado...")
            proximo, ultimo = arca.obtener_proximo_numero(pv, tipo, token, sign, empresa.cuit)
            print(f"✅ Último autorizado: {ultimo} → PRÓXIMO NÚMERO: {proximo}")
            
            # Actualizar XML con token y número
            xml_final = actualizar_xml_arca(str(xml_path), token, sign, proximo)
            print(f"✅ XML actualizado")
            
            # Enviar solicitud de CAE
            print(f"\n🚀 ENVIANDO SOLICITUD DE CAE A ARCA ({arca.entorno.upper()})...")
            respuesta = arca.enviar_solicitud_cae(xml_final)
            print(f"✅ Respuesta recibida")
            
            # Procesar respuesta
            resultado = procesar_respuesta_cae(respuesta)
            
            # Guardar XML de respuesta formateado en la misma carpeta
            guardar_xml_respuesta(respuesta, xml_path)
            
            # Mostrar resultado
            if resultado['aprobado']:
                print("\n" + "="*60)
                print("🎉 ¡CAE OBTENIDO EXITOSAMENTE!")
                print("="*60)
                print(f"🔢 CAE: {resultado['cae']}")
                print(f"📅 Vencimiento: {resultado['vencimiento']}")
                print(f"📄 Cbte Desde: {resultado['cbte_desde']}")
                print(f"📄 Cbte Hasta: {resultado['cbte_hasta']}")
                
                if resultado['eventos']:
                    print("\n📢 Eventos/Observaciones:")
                    for evento in resultado['eventos']:
                        print(f"   • {evento}")
                
                # Mostrar número formateado para Factura
                pv_2d = f"{pv:02d}"
                num_8d = f"{proximo:08d}"
                numero_factura = f"{pv_2d}{num_8d}"
                print(f"\n📄 Número para Factura.numero_comprobante: {numero_factura}")
                
                return True
            
            # Si hay error 10016, reintentar
            if any("10016" in error for error in resultado.get('errores', [])):
                print(f"⚠️  Error 10016 detectado (colisión numérica o fecha inválida)")
                if intento < 3:
                    espera = 0.5 * (intento + 1)
                    print(f"⏳ Esperando {espera}s para reintentar con número fresco...")
                    time.sleep(espera)
                    continue
            
            # Mostrar errores
            print("\n❌ ERRORES:")
            for error in resultado.get('errores', []):
                print(f"   • {error}")
            
            if resultado.get('eventos'):
                print("\n📢 Eventos:")
                for evento in resultado['eventos']:
                    print(f"   • {evento}")
            
            break  # Salir del bucle si no es recuperable
                
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
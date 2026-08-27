import base64
import json
import qrcode

# 1. Definir los datos reales del comprobante autorizado
datos_factura = {
    "ver": 1,                      # Versión del formato (siempre 1)
    "fecha": "2026-08-27",         # Fecha de emisión (AAAA-MM-DD)
    "cuit": 20123456789,           # CUIT del emisor (entero)
    "ptoVta": 5,                   # Punto de venta (entero)
    "tipoCmp": 11,                 # Tipo de comprobante (ej: 11 = Factura C)
    "nroCmp": 123,                 # Número de comprobante (entero)
    "importe": 25500.00,           # Importe total (float)
    "moneda": "PES",               # Moneda ("PES" para pesos argentinos)
    "ctz": 1.0,                    # Cotización de la moneda (float)
    "tipoDocRec": 96,              # Tipo doc receptor (ej: 96 = DNI, 80 = CUIT)
    "nroDocRec": 35123456,         # Número de documento receptor (entero)
    "tipoCodAut": "E",             # Tipo de código de autorización ("E" para CAE)
    "codAut": 76543210987654       # Número de CAE (entero)
}

# 2. Convertir el diccionario a un string JSON compacto (sin espacios innecesarios)
json_string = json.dumps(datos_factura, separators=(',', ':'))

# 3. Codificar el string JSON en Base64 seguro para URLs
json_base64 = base64.urlsafe_b64encode(json_string.encode('utf-8')).decode('utf-8')

# 4. Construir la URL oficial de ARCA/AFIP
url_qr = f"https://afip.gob.ar{json_base64}"
print(f"URL generada: {url_qr}")

# 5. Crear y guardar la imagen del código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M, # ARCA recomienda nivel M o H
    box_size=10,
    border=4,
)
qr.add_data(url_qr)
qr.make(fit=True)

imagen_qr = qr.make_image(fill_color="black", back_color="white")
imagen_qr.save("qr_factura_arca.png")

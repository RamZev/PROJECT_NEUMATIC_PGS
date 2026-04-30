# from afip import Afip

# # Certificado (Puede estar guardado en archivos, DB, etc)
# cert = open("MAASDEMO.crt").read()

# # Key (Puede estar guardado en archivos, DB, etc)
# key = open("MAASDEMO.key").read()

# # CUIT del certificado
# tax_id = 20207882950

# afip = Afip({
#     "CUIT": tax_id,
#     "cert": cert,
#     "key": key
# })

# print(afip.access_token)

from afip import Afip

# Certificado (Puede estar guardado en archivos, DB, etc)
cert = open("MAASDEMO.crt").read()

# Key (Puede estar guardado en archivos, DB, etc)
key = open("MAASDEMO.key").read()

# CUIT del certificado
tax_id = 20207882950

# Instanciamos la clase Afip con las credenciales
afip = Afip({
    "CUIT": tax_id,
    "cert": cert,
    "key": key
})

# URL al archivo WSDL de test
#
# Esta URL la podes encontrar en el manual del web service
WSDL_TEST = "https://fwshomo.afip.gov.ar/wsct/CTService?wsdl"

# URL al archivo WSDL de produccion
#
# Esta URL la podes encontrar en el manual del web service
WSDL = "https://serviciosjava.afip.gob.ar/wsct/CTService?wsdl"

# URL del Web service de produccion
#
# Esta URL la podes encontrar en el manual del web service
URL = "https://serviciosjava.afip.gob.ar/wsct/CTService"

# URL del Web service de test
#
# Esta URL la podes encontrar en el manual del web service
URL_TEST = "https://fwshomo.afip.gov.ar/wsct/CTService"

# Seterar en true si el web service requiere usar soap v1.2
#
# Si no estas seguro de que necesita v1.2 proba con ambas opciones
soapV1_2 = True

# Nombre del web service.
#
# El nombre por el cual se llama al web service en ARCA.
# Esto lo podes encontrar en el manual correspondiente.
# Por ej. el de factura electronica se llama "wsfe", el de
# comprobantes T se llama "wsct"
# servicio = "wsct"
servicio = "wsfe"

# A partir de aca ya no debes cambiar ninguna variable

# Preparamos las opciones para el web service
options = {
  "WSDL": WSDL,
  "WSDL_TEST": WSDL_TEST,
  "URL": URL,
  "URL_TEST": URL_TEST,
  "soapV1_2": soapV1_2
}

# Consumimos el web service con el objeto sfip
genericWebService = afip.webService(servicio, options)

# Obtenemos el Token Authorizataion
ta = genericWebService.getTokenAuthorization()

print(ta)
print(ta)
print('expiration', ta['expiration'])
print('token', ta['token'])
print('sign', ta['sign'])
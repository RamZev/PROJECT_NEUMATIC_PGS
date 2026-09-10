# neumatic/entorno/constantes_padron.py

PADRON_CONFIG = {
    6: {  # ← id_provincia de Entre Ríos
        'modelo': 'PadronEntreRiosIIBB',   # ← Cambiado
        'app': 'maestros',
        'campos': {
            'cuit': 'cuit',
            'fecha_desde': 'fecha_vigencia_desde',
            'fecha_hasta': 'fecha_vigencia_hasta',
            'alicuota_percepcion': 'alicuota_percepcion',
            'alicuota_retencion': 'alicuota_retencion',
            'razon_social': 'razon_social',
        }
    },
    13: {  # ← id_provincia de Santa Fe
        'modelo': 'PadronSantaFeIIBB',     # ← Cambiado
        'app': 'maestros',
        'campos': {
            'cuit': 'cuit',
            'fecha_desde': 'fecha_vigencia_desde',
            'fecha_hasta': 'fecha_vigencia_hasta',
            'alicuota_percepcion': 'alicuota_percepcion',
            'alicuota_retencion': 'alicuota_retencion',
            'razon_social': 'razon_social',
        }
    },
}
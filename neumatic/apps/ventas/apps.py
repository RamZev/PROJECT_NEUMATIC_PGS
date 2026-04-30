from django.apps import AppConfig


class VentasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ventas'
    
    def ready(self):
        import apps.ventas.models.factura_models
        import apps.ventas.models.recibo_models
        import apps.ventas.models.venta_models
        import apps.ventas.models.compra_models
        import apps.ventas.models.caja_models


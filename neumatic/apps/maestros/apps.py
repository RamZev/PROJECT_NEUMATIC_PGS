# neumatic\apps\maestros\apps.py
from django.apps import AppConfig


class MaestrosConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'apps.maestros'
	
	def ready(self):
		import apps.maestros.models.base_gen_models
		import apps.maestros.models.base_models
		import apps.maestros.models.cliente_models
		import apps.maestros.models.empresa_models
		import apps.maestros.models.numero_models
		import apps.maestros.models.parametro_models
		import apps.maestros.models.producto_models
		import apps.maestros.models.proveedor_models
		import apps.maestros.models.sucursal_models
		import apps.maestros.models.vendedor_models
		import apps.maestros.models.descuento_vendedor_models
		import apps.maestros.signals.signals
		import apps.maestros.models.vendedor_comision_models
		import apps.maestros.models.valida_models

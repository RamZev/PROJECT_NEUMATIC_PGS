# neumatic\apps\maestros\models\base_gen_models.py
from django.db import models

import socket
from datetime import datetime

# from django.contrib.auth.models import User  

# Importa el modelo User Personalizado
from apps.usuarios.models import User       


class ModeloBaseGenerico(models.Model):
	id_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuario", null=True, blank=True, default=1)
	usuario = models.CharField(max_length=20, null=True, blank=True)
	estacion = models.CharField(max_length=20, null=True, blank=True)
	fcontrol = models.CharField(max_length=22, null=True, blank=True)
	
	
	class Meta:
		abstract = True
	
	def save(self, *args, **kwargs):
		
		#-- Obtiene el nombre del equipo (estación) en Windows.
		if not self.estacion:
			self.estacion = socket.gethostname()
		
		#-- Obtiene la fecha y hora actual en el formato deseado.
		if not self.fcontrol:
			#-- Reemplaza con el formato deseado.
			self.fcontrol = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		super(ModeloBaseGenerico, self).save(*args, **kwargs)

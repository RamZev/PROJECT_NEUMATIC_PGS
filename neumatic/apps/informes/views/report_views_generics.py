# neumatic\apps\informes\views\report_views_generics.py

import uuid
from django.views.generic import FormView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.cache import cache

#-- Recursos necesarios para proteger las rutas.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from utils.utils import serializar_datos, obtener_logo

from apps.maestros.models.empresa_models import Empresa


# -- Vistas Genéricas Basada en Clases -----------------------------------------------
@method_decorator(login_required, name='dispatch')
class InformeFormView(FormView):
	"""
	Clase base para informes.
	Se encarga de:
	  - Validar el formulario.
	  - Ejecutar la consulta mediante obtener_queryset().
	  - Obtener el contexto final para el reporte mediante obtener_contexto_reporte().
	  - Procesar la salida según el parámetro 'tipo_salida'.
	Las vistas hijas deberán implementar, al menos, obtener_queryset()
	y, en caso de necesitar transformación de datos, obtener_contexto_reporte().
	"""
	
	'''
	def _obtener_logo(self):
		"""Método auxiliar para obtener el logo de la empresa de forma segura"""
		
		logo_url = None
		logo_path = None
		
		try:
			empresa = Empresa.objects.first()
			if empresa:
				logo_url = empresa.logo_url_safe
				logo_path = empresa.logo_path_safe
		except Exception:
			pass
		
		return logo_url, logo_path
	'''
	
	def get(self, request, *args, **kwargs):
		#-- Para evitar posibles errores por formulario no ligado a un modelo.
		self.object = None
		#-- Instanciar el Form vacío para su renderización.
		form = self.get_form()
		
		#-- Si el formulario se ha enviado y hay parámetros establecidos se procesa.
		if request.GET and any(value for key, value in request.GET.items() if value):
			if form.is_valid():
				tipo_salida = request.GET.get("tipo_salida")
				
				#-- Se ejecuta la consulta a la Base de Datos.
				queryset = self.obtener_queryset(form.cleaned_data)
				
				#-- Obtiene el contexto del reporte; por defecto, puede ser simplemente el queryset.
				contexto_reporte = self.obtener_contexto_reporte(queryset, form.cleaned_data)
				
				#-- Agregar logo al contexto del reporte (si no fue proporcionado explícitamente por la vista hija).
				if "logo_url" not in contexto_reporte or "logo_path" not in contexto_reporte:
					#-- Si las claves no existen, obtener logos por defecto.
					# logo_url, logo_path = self._obtener_logo()
					logo_url, logo_path = obtener_logo()
					contexto_reporte['logo_url'] = logo_url
					contexto_reporte['logo_path'] = logo_path
				#-- Si las claves existen, se respetan sus valores (incluso si son None).
				
				#-- Procesa la salida.
				return self.procesar_reporte(contexto_reporte, tipo_salida, form.cleaned_data)
			else:
				return self.form_invalid(form)
		
		context_data = self.get_context_data(form=form)
		return self.render_to_response(context_data)
	
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		#-- Sólo asignar data si la querystring contiene datos.
		if len(self.request.GET) > 0:
			kwargs['data'] = self.request.GET
		#-- Pasar como parámetro el usuario autenticado.
		kwargs['user'] = self.request.user
		return kwargs
	
	def form_invalid(self, form):
		context = self.get_context_data(form=form)
		if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
			#-- Renderizar el modal con los errores de validación y enviado en la respuesta JSON.
			html = render_to_string("modal_errors.html", context, request=self.request)
			return JsonResponse({"success": False, "html": html})
		else:
			return super().render_to_response(context)
	
	def procesar_reporte(self, contexto_reporte, tipo_salida, cleaned_data):
		"""
		Una vez validado el formulario, genera un token, guarda el contexto en la sesión y
		devuelve un JSON con la URL de salida (para pantalla, PDF, etc).
		"""
		
		#-- Limpiar posibles reportes previos en la sesión.
		for key in list(self.request.session.keys()):
			if key.startswith("reporte_"):  #-- Opcional: prefijo para identificar tokens de reportes.
				del self.request.session[key]
		
		token = f"reporte_{uuid.uuid4()}"  #-- Agregar prefijo para fácil identificación.
		self.request.session[token] = serializar_datos(contexto_reporte)
		# self.request.session[token] = contexto_reporte
		self.request.session.save()
		
		#----------------------------------------
		#-- Guarda en la cache el diccionario con los datos necesarios.
		#-- Por ejemplo, puedes guardar el cleaned_data y el contexto sin necesidad de convertirlos a JSON.
		# cache.set(token, {"cleaned_data": cleaned_data, "contexto_reporte": contexto_reporte}, timeout=600)  # timeout en segundos
		cache.set(token, {"cleaned_data": cleaned_data}, timeout=600)  # timeout en segundos
		
		#----------------------------------------
		
		if tipo_salida == "pantalla":
			url = reverse(self.config.url_pantalla) + f"?token={token}"
		elif tipo_salida == "pdf_preliminar":
			url = reverse(self.config.url_pdf) + f"?token={token}"
		elif tipo_salida == "excel_preliminar":
			url = reverse(self.config.url_excel) + f"?token={token}&tipo_salida={tipo_salida}"
		elif tipo_salida == "csv_preliminar":
			url = reverse(self.config.url_csv) + f"?token={token}&tipo_salida={tipo_salida}"
		else:
			url = reverse(self.config.url_pantalla) + f"?token={token}"
		
		if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
			return JsonResponse({"success": True, "url": url})
		else:
			return HttpResponseRedirect(url)
	
	def obtener_queryset(self, cleaned_data):
		"""
		Debe devolver el queryset filtrado según los datos del formulario.
		DEBE implementarse en la vista hija.
		"""
		
		raise NotImplementedError("Debe implementarse el método obtener_queryset.")
		
	def obtener_contexto_reporte(self, queryset, cleaned_data):
		"""
		Retorna el contexto que se pasará al template para renderizar el reporte.
		Por defecto, se retorna un contexto con los datos tal cual:
		  {
			 "objetos": queryset
		  }
		Si el listado requiere agrupar, subtotalizar o totalizar, la vista hija
		debe sobreescribir este método.
		"""
		
		return {"objetos": queryset}

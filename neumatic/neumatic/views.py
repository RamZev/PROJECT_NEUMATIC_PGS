# neumatic\neumatic\views.py
from django.shortcuts import render, redirect
from django.utils import timezone


def home_view(request):
	#-- Limpiar parámetros de consulta de la sesión (Cambio Costo/Precio por porcentaje).
	request.session.pop('filtros_actualizacion', None)
	request.session.pop('post_realizado', None)
	
	if request.user.is_authenticated:
		fecha_actual = timezone.now()
		return render(request, 'home.html', {'fecha': fecha_actual})
	else:
		return redirect('iniciar_sesion')
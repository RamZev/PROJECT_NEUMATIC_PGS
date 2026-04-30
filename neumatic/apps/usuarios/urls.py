# D:\PROJECT_NEUMATIC\neumatic\apps\usuarios\urls.py
from django.urls import path
from apps.usuarios.views.user_views import *

urlpatterns = [
	#-- Login/Logout
	path('sesion/iniciar/', CustomLoginView.as_view(), name='iniciar_sesion'),
	path('sesion/cerrar/', CustomLogoutView.as_view(), name='cerrar_sesion'),
	
	#-- Grupos
	path('grupo/listar/', GrupoListView.as_view(), name='grupo_listar'),
	path('grupo/crear/', GrupoCreateView.as_view(), name='grupo_crear'),
	path('grupo/editar/<int:pk>/', GrupoUpdateView.as_view(), name='grupo_editar'),
	path('grupo/eliminar/<int:pk>/', GrupoDeleteView.as_view(), name='grupo_eliminar'),
	
	#-- Usuarios
	path('usuario/listar/', UsuarioListView.as_view(), name='usuario_listar'),
	path('usuario/crear/', UsuarioCreateView.as_view(), name='usuario_crear'),
	path('usuario/editar/<int:pk>/', UsuarioUpdateView.as_view(), name='usuario_editar'),
	path('usuario/eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_eliminar')
]

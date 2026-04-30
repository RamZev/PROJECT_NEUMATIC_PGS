# generar_plantilla.py
import os
import django
import sys

''' Estos imports ya no son necesarios
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
'''

from estructuras_maestros import estructura_campos

# Agregar la ruta del directorio principal del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neumatic.settings")

django.setup()

# OJO: la estructura de datos debe venir desde el formulario
modelo = sys.argv[1]
estructura_campos = estructura_campos[modelo]
# print(estructura_campos)

# Validar si la estructura de de campos es válida

# Generar la estructura HTML en base a la estructura de datos
html_code = """{% extends 'maestro_form.html' %}
{% load static %}
<!-- -------------------------------------------------------------------- -->
{% block maincomponent %}
	{% block principalcomponent %}
		<div id="layoutSidenav_content">
			<main>
				<div class="container-fluid">
					
					<div class="card border-light mb-3 mt-2">
						<div class="card-header text-white bg-primary opacity-75 d-flex 
									justify-content-between">
							{{ accion }}
							<div class="flex align-items-center">
								<a 
									class="me-2 text-white" 
									data-bs-toggle="modal" 
									data-bs-target="#helpModal" 
									style="cursor: pointer;">
									<i class="bi bi-question-lg"></i></a>
								
								<button type="button" class="btn-close btn-close-white" 
									aria-label="Close"
									onclick="window.location.href='{% url list_view_name %}'">
								</button>
							</div>
						</div>
						
						<div class="card-body bg-body-secondary">
							<form method="post" enctype="multipart/form-data" novalidate>
								{% csrf_token %}
								<div class="accordion" id="accordionPanelsStayOpenExample">
									<!-- Estructura generada -->
"""

primera_iteracion = True

#-- Insertar elementos del acordeón.
for seccion, filas in estructura_campos.items():
		html_code += f"""									
									<div class="accordion-item">
										<h2 class="accordion-header">
											<button 
												class="accordion-button py-2 {'collapsed' if not primera_iteracion else ''}" 
												type="button" 
												data-bs-toggle="collapse" 
												data-bs-target="#{seccion.replace(" ", "_")}" 
												aria-expanded="{'true' if primera_iteracion else 'false'}" 
												aria-controls="{seccion.replace(" ", "_")}">
												<strong>{seccion}</strong>
											</button>
										</h2>
										<div class="accordion-collapse collapse {'show' if primera_iteracion else ''}"
											id="{seccion.replace(" ", "_")}">
											<div class="accordion-body bg-secondary-subtle">
		"""
		
		#-- Insertar elementos fila.
		for fila, campos in filas.items():
				html_code += '''										
												<div class="row">
								'''
				
				#-- Insertar inputs.
				for campo in campos:
						field_name = campo['field_name']
						columna = campo['columna']
						
						match campo.get('design'):
							case "checkbox":
								html_code += f"""					
													<div class="col-md-{columna} d-flex align-items-center">
														<div class="form-check mt-lg-3">
															<label class="form-check-label form-label text-primary" for="{{{{ form.{field_name}.id_for_label }}}}">
																{{{{ form.{field_name} }}}}
																{{{{ form.{field_name}.label }}}}
															</label>
														</div>
													</div>
								"""
							case _:
								html_code += f"""					
													<div class="col-md-{columna}">
														<label class="form-label text-primary mb-0" for="{{{{ form.{field_name}.id_for_label }}}}">
															{{{{ form.{field_name}.label }}}}
														</label>
														{{{{ form.{field_name} }}}}
													</div>
								"""
				
				html_code += '				</div>'
		
		html_code += """
											</div>
										</div>
									</div>
		"""
		
		primera_iteracion = False

# Continuación del código HTML
html_code += """						
								</div>
								
								<div class="container mt-3">
									<button class="btn btn-primary" type="submit" id="guardarBtn">
										Guardar
									</button>
									<a class="btn btn-secondary" href="{% url list_view_name %}">
										Cancelar
									</a>
								</div>
							</form>
						</div>
					</div>
				</div>
			</main>
		</div>
	{% endblock principalcomponent %}
{% endblock maincomponent %}
<!-- -------------------------------------------------------------------- -->
{% block modals %}
	<!-- Modal para mostrar errores -->
	{% include 'modal_errors.html' %}
	
	<!-- Modal para mostrar los requerimientos de los campos -->
	{% include 'maestros/modal_fields_requirements.html' %}
{% endblock modals %}
<!-- -------------------------------------------------------------------- -->
"""

''' Este código ya no es necesario
# Crear un objeto BeautifulSoup
# soup = BeautifulSoup(html_code, "html.parser")

# Obtener el código HTML con indentación
# indented_html_code = soup.prettify(formatter=HTMLFormatter(indent=2))
'''

# Guardar el código HTML en el archivo
# with open("persona3_form.html", "w", encoding="utf-8") as file:
with open(f"{modelo}_form.html", "w", encoding="utf-8") as file:
  file.write(html_code)
  # file.write(indented_html_code)
				
# s = '<section><article><h1></h1><p></p></article></section>'
# formatter = formatter.HTMLFormatter(indent=4)
# print(BeautifulSoup(s, 'html.parser').prettify(formatter=formatter))
import json
import os

def generate_crud_views(data):
    # Extraer información del JSON
    model_name = data["model_name"]  # Nombre del modelo desde el JSON
    model_string = data["model_string"]
    file_path = data["file_path"]
    
    # Acceso a los campos de búsqueda, ordenamiento, etc.
    search_fields = data["data_view_list"]["search_fields"]
    ordering = data["data_view_list"]["ordering"]
    paginate_by = data["data_view_list"]["paginate_by"]
    table_headers = data["data_view_list"]["table_headers"]
    table_data = data["data_view_list"]["table_data"]

    # Construir el contenido del archivo de vistas
    content = f"""# {file_path}{model_string}_views.py
from django.urls import reverse_lazy
from ..views.cruds_views_generics import *
from {data['model_import_path']} import {model_name}
from {data['form_import_path']} import {data['form_name']}


class ConfigViews():
    # Modelo
    model = {model_name}
    
    # Formulario asociado al modelo
    form_class = {data['form_name']}
    
    # Aplicación asociada al modelo
    app_label = model._meta.app_label
    
    #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
    model_string = "{model_string}"  #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
    
    # Permisos
    permission_add = f"{ConfigViews.app_label}.add_{model_string}"
    permission_change = f"{ConfigViews.app_label}.change_{model_string}"
    permission_delete = f"{ConfigViews.app_label}.delete_{model_string}"
    
    # Vistas del CRUD del modelo
    list_view_name = "{data['views']['list_view_name']}"
    create_view_name = "{data['views']['create_view_name']}"
    update_view_name = "{data['views']['update_view_name']}"
    delete_view_name = "{data['views']['delete_view_name']}"
    
    # Plantilla para crear o actualizar el modelo
    template_form = "{data['template_form']}"
    
    # Plantilla para confirmar eliminación de un registro
    template_delete = "base_confirm_delete.html"
    
    # Plantilla de la lista del CRUD
    template_list = "{data['template_list']}"
    
    # Contexto de los datos de la lista
    context_object_name = "{data['context_object_name']}"
    
    # Vista del home del proyecto
    home_view_name = "{data['home_view_name']}"
    
    # Nombre de la url 
    success_url = reverse_lazy(list_view_name)


class DataViewList():
    search_fields = {search_fields}
    
    ordering = {ordering}
    
    paginate_by = {paginate_by}
      
    table_headers = {{
        {', '.join([f'"{k}": ({v[0]}, "{v[1]}")' for k, v in table_headers.items()])}
    }}
    
    table_data = [
        {',\n        '.join([f'{{"field_name": "{item["field_name"]}", "date_format": {item["date_format"]}}}' for item in table_data])}
    ]


# {model_name}ListView - Inicio
class {model_name}ListView(MaestroListView):
    model = ConfigViews.model
    template_name = ConfigViews.template_list
    context_object_name = ConfigViews.context_object_name
    
    search_fields = DataViewList.search_fields
    ordering = DataViewList.ordering
    
    extra_context = {{
        "master_title": ConfigViews.model._meta.verbose_name_plural,
        "home_view_name": ConfigViews.home_view_name,
        "list_view_name": ConfigViews.list_view_name,
        "create_view_name": ConfigViews.create_view_name,
        "update_view_name": ConfigViews.update_view_name,
        "delete_view_name": ConfigViews.delete_view_name,
        "table_headers": DataViewList.table_headers,
        "table_data": DataViewList.table_data,
    }}


# {model_name}CreateView - Inicio
class {model_name}CreateView(MaestroCreateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url
    
    permission_required = ConfigViews.permission_add
    
    extra_context = {{
        "accion": f"Crear {ConfigViews.model._meta.verbose_name}",
        "list_view_name": ConfigViews.list_view_name
    }}


# {model_name}UpdateView - Inicio
class {model_name}UpdateView(MaestroUpdateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url
    
    permission_required = ConfigViews.permission_change
    
    extra_context = {{
        "accion": f"Editar {ConfigViews.model._meta.verbose_name}",
        "list_view_name": ConfigViews.list_view_name
    }}


# {model_name}DeleteView - Inicio
class {model_name}DeleteView(MaestroDeleteView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    template_name = ConfigViews.template_delete
    success_url = ConfigViews.success_url
    
    permission_required = ConfigViews.permission_delete
    
    extra_context = {{
        "accion": f"Eliminar {ConfigViews.model._meta.verbose_name}",
        "list_view_name": ConfigViews.list_view_name,
        "mensaje": "Estás seguro de eliminar el Registro"
    }}
"""

    # Guardar el contenido en un archivo
    output_file_path = os.path.join(file_path, f"{model_string}_views.py")
    with open(output_file_path, "w") as output_file:
        output_file.write(content)

    print(f"El archivo {model_string}_views.py se ha creado correctamente.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python generar_vistas.py <nombre_del_archivo_json>")
        sys.exit(1)

    json_file = sys.argv[1]

    # Verificar si el archivo JSON existe
    if not os.path.isfile(json_file):
        print(f"Error: El archivo {json_file} no se encuentra.")
        sys.exit(1)

    # Leer el archivo JSON
    with open(json_file, "r") as file:
        json_data = json.load(file)

    print("El archivo JSON se ha leído correctamente.")
    
    # Generar las vistas CRUD a partir de la estructura JSON
    generate_crud_views(json_data)

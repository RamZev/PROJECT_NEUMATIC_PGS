# neumatic/data_load/usuarios_menu_migra.py
import os
import sys
import django

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

# --- CÓDIGO ORIGINAL (con mejoras) ---
from django.db import connection

SQL_FILES_TO_RUN = [
    'auth_group.sql',
    'auth_group_permissions.sql',
    'usuarios_user.sql',
    'usuarios_user_groups.sql',
    'menu_menuheading.sql',
    'menu_menuitem.sql',
    'menu_menuitem_groups.sql',
]

def execute_sql_data_load():
    """
    Función principal para ejecutar todos los archivos SQL directamente.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"\n--- Iniciando Carga de Datos SQL desde: {base_dir} ---")
    
    success_count = 0
    error_count = 0
    
    for sql_file_name in SQL_FILES_TO_RUN:
        sql_path = os.path.join(base_dir, sql_file_name)

        if not os.path.exists(sql_path):
            print(f"⚠️ Archivo SQL no encontrado: {sql_file_name} en {sql_path}")
            error_count += 1
            continue

        print(f"🔄 Ejecutando: {sql_file_name}...")
        
        try:
            with open(sql_path, 'r', encoding='utf-8') as file:
                sql_content = file.read().strip()
                
            if not sql_content:
                print(f"ℹ️ Archivo vacío: {sql_file_name}")
                continue
                
            with connection.cursor() as cursor:
                # Ejecutar cada sentencia SQL por separado
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                for statement in statements:
                    if statement:
                        cursor.execute(statement)
            
            print(f"✅ {sql_file_name} ejecutado con éxito.")
            success_count += 1
            
        except Exception as e:
            print(f"❌ ERROR en {sql_file_name}: {e}")
            error_count += 1
    
    print(f"\n--- Resumen de Ejecución ---")
    print(f"✅ Archivos ejecutados correctamente: {success_count}")
    print(f"❌ Archivos con errores: {error_count}")
    print(f"📊 Total procesado: {success_count + error_count} de {len(SQL_FILES_TO_RUN)}")
    print("--- Carga de Datos Finalizada ---\n")

# Ejecutar directamente si se llama el script
if __name__ == "__main__":
    execute_sql_data_load()
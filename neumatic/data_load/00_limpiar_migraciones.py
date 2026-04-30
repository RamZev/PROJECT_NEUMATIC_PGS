import os
import shutil
import sys

def limpiar_migraciones():
    # Configurar el BASE_DIR del proyecto
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    apps = ['informes', 'maestros', 'usuarios', 'ventas', 'menu']
    
    for app in apps:
        # Construir la ruta completa a las migraciones
        migraciones_path = os.path.join(BASE_DIR, 'apps', app, 'migrations')
        
        if os.path.exists(migraciones_path):
            print(f"Procesando: {migraciones_path}")
            
            # Eliminar __pycache__
            pycache_path = os.path.join(migraciones_path, '__pycache__')
            if os.path.exists(pycache_path):
                shutil.rmtree(pycache_path)
                print(f"  Eliminada carpeta __pycache__ en {pycache_path}")
            
            # Eliminar archivos de migración (excepto __init__.py)
            for filename in os.listdir(migraciones_path):
                file_path = os.path.join(migraciones_path, filename)
                if filename != '__init__.py' and filename.endswith('.py'):
                    os.remove(file_path)
                    print(f"  Eliminado archivo {filename}")
        else:
            print(f"Advertencia: No se encontró la carpeta {migraciones_path}")

if __name__ == "__main__":
    print("Iniciando limpieza de migraciones...")
    limpiar_migraciones()
    print("Proceso completado.")
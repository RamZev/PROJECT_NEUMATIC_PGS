import os
import subprocess
import sys
from time import sleep

# Configuración del entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')

# Lista de scripts a ejecutar en orden
SCRIPTS = [
    'banco_migra.py',
    'cuenta_banco_migra.py',
    'tarjeta_migra.py',
    'codigo_retencion_migra.py',
    'concepto_banco_migra.py',
    'cheque_recibo_migra.py',
    'tarjeta_recibo_migra.py',
    'retencion_recibo_migra.py',
    'deposito_recibo_migra.py',
    'compensa_factura_migra.py'
    
]

def configurar_entorno():
    """Configura el entorno Django"""
    try:
        import django
        django.setup()
        print("✅ Entorno Django configurado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error configurando Django: {str(e)}")
        return False

def ejecutar_script(script_name):
    """Ejecuta un script individual"""
    script_path = os.path.join(BASE_DIR, 'data_load', script_name)
    
    if not os.path.exists(script_path):
        print(f"⚠️ Error: No se encontró el script {script_name}")
        return False
    
    print(f"\n{'='*50}")
    print(f"Ejecutando {script_name}...")
    print(f"{'='*50}\n")
    
    try:
        # Usamos el mismo intérprete que está ejecutando este script
        python_exec = sys.executable
        result = subprocess.run([python_exec, script_path], check=True)
        if result.returncode == 0:
            print(f"\n✅ {script_name} completado exitosamente")
            return True
        else:
            print(f"\n❌ {script_name} falló con código {result.returncode}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error al ejecutar {script_name}: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado en {script_name}: {str(e)}")
        return False

def main():
    print("\n" + "="*50)
    print("INICIANDO PROCESO DE MIGRACIÓN COMPLETO")
    print("="*50 + "\n")
    
    # Configurar entorno Django primero
    if not configurar_entorno():
        print("\n" + "!"*50)
        print("ERROR: No se pudo configurar el entorno Django")
        print("!"*50 + "\n")
        return
    
    # Ejecutar cada script en orden
    for script in SCRIPTS:
        if not ejecutar_script(script):
            print("\n" + "!"*50)
            print(f"ERROR: El proceso se detuvo por falla en {script}")
            print("Revisa el error antes de continuar")
            print("!"*50 + "\n")
            break
        
        # Pequeña pausa entre scripts
        sleep(1)
    
    print("\n" + "="*50)
    print("PROCESO DE MIGRACIÓN COMPLETADO")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
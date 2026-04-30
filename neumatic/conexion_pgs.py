# neumatic\conexion_pgs.py
# -*- coding: utf-8 -*-
"""
Prueba de conexión a PostgreSQL 18 desde Django
Ejecutar: python conexion_psg.py
"""

import os
import sys
import django

# Configurar entorno Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')

# Configuración temporal de PostgreSQL para la prueba
# (sin modificar el settings.py original)
POSTGRES_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'db_neumatic',           # Nombre de la base de datos
    'USER': 'postgres',               # Usuario de PostgreSQL
    'PASSWORD': 'AdminOpc2026',      # ¡CAMBIAR POR TU CONTRASEÑA!
    'HOST': 'localhost',
    'PORT': '5432',
}

def test_conexion_postgres():
    """Prueba la conexión a PostgreSQL"""
    print("=" * 60)
    print("PRUEBA DE CONEXIÓN A POSTGRESQL 18")
    print("=" * 60)
    
    try:
        # Intentar conectar usando psycopg2 directamente
        import psycopg2
        print("\n1. Probando conexión directa con psycopg2...")
        
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='postgres',  # Conectar a base por defecto primero
            user='postgres',
            password='AdminOpc2026'  # ¡CAMBIAR!
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"   ✅ Conexión exitosa!")
        print(f"   📌 Versión: {version[0][:50]}...")
        cursor.close()
        conn.close()
        
    except ImportError:
        print("   ❌ psycopg2 no está instalado. Ejecutar: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        print("\n   Posibles soluciones:")
        print("   1. Verificar que PostgreSQL esté corriendo")
        print("   2. Verificar la contraseña del usuario postgres")
        print("   3. Ejecutar: pip install psycopg2-binary")
        return False
    
    # Probar creación de la base de datos si no existe
    print("\n2. Verificando base de datos 'db_neumatic'...")
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='postgres',
            user='postgres',
            password='AdminOpc2026'  # ¡CAMBIAR!
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'db_neumatic';")
        exists = cursor.fetchone()
        
        if not exists:
            print("   ⚠️ La base de datos 'db_neumatic' no existe. Creándola...")
            cursor.execute("CREATE DATABASE db_neumatic;")
            print("   ✅ Base de datos 'db_neumatic' creada exitosamente")
        else:
            print("   ✅ Base de datos 'db_neumatic' ya existe")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODO ESTÁ LISTO PARA CONECTAR POSTGRESQL CON DJANGO")
    print("=" * 60)
    print("\nPara usar PostgreSQL en Django, cambia en settings.py:")
    print("""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_neumatic',
        'USER': 'postgres',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
    """)
    
    return True

def test_django_con_postgres():
    """Prueba la configuración de Django con PostgreSQL"""
    print("\n" + "=" * 60)
    print("PRUEBA DE CONFIGURACIÓN DJANGO + POSTGRESQL")
    print("=" * 60)
    
    # Cambiar temporalmente la configuración de bases de datos
    from django.conf import settings
    from django.db import connection
    
    original_databases = settings.DATABASES.copy()
    
    try:
        # Sobrescribir la configuración
        settings.DATABASES['default'] = POSTGRES_CONFIG
        
        # Probar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Django conectado exitosamente a PostgreSQL")
            print(f"📌 Versión: {version[0][:50]}...")
            print(f"📌 Base de datos: {connection.settings_dict['NAME']}")
            return True
            
    except Exception as e:
        print(f"❌ Error configurando Django con PostgreSQL: {e}")
        return False
        
    finally:
        # Restaurar configuración original
        settings.DATABASES = original_databases

if __name__ == '__main__':
    print("\n🔧 CONEXIÓN A POSTGRESQL 18")
    print("⚠️  ANTES DE EJECUTAR: Cambia la contraseña en POSTGRES_CONFIG")
    print("   Línea 23: 'PASSWORD': 'tu_contraseña' → tu contraseña real")
    print()
    
    input("Presiona ENTER para continuar...")
    
    # Instalar psycopg2 si no está
    try:
        import psycopg2
    except ImportError:
        print("\n📦 Instalando psycopg2-binary...")
        os.system("pip install psycopg2-binary")
        import psycopg2
    
    if test_conexion_postgres():
        test_django_con_postgres()
    
    print("\n" + "=" * 60)
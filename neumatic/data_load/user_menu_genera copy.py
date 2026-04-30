# user_menu_genera.py
import sqlite3
import sys
import os
from datetime import datetime
from pathlib import Path

def encontrar_base_datos():
    """
    Encuentra automáticamente la ruta de la base de datos
    """
    try:
        # Rutas específicas basadas en tu estructura
        rutas_a_probar = [
            # Si el script está en data_load/
            Path(__file__).parent.parent / "data" / "db_neumatic.db",
            # Ruta absoluta desde la raíz del proyecto
            Path("D:/PROJECT_NEUMATIC/neumatic/data/db_neumatic.db"),
            # Ruta relativa común
            Path("data/db_neumatic.db"),
            Path("../data/db_neumatic.db"),
        ]
        
        print("🔍 Buscando base de datos...")
        for ruta in rutas_a_probar:
            ruta_abs = ruta.absolute()
            print(f"   Probando: {ruta_abs}")
            if ruta_abs.exists():
                print(f"✅ Encontrada: {ruta_abs}")
                return str(ruta_abs)
        
        print("❌ No se encontró la base de datos en las rutas probadas")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def generar_inserts_en_un_archivo(db_path):
    """
    Genera un solo archivo SQL con todas las inserciones
    EXCLUYENDO el usuario con id=1 en usuarios_user
    """
    
    # Tablas en el orden CORRECTO
    tablas = [
        'auth_group',
        'auth_group_permissions', 
        'usuarios_user',
        'usuarios_user_groups',
        'menu_menuheading',
        'menu_menuitem',
        'menu_menuitem_groups'
    ]
    
    try:
        print(f"📂 Conectando a: {db_path}")
        conexion = sqlite3.connect(db_path)
        conexion.text_factory = lambda x: str(x, 'utf-8', 'ignore')  # Manejo mejorado de encoding
        
        print("🔧 Generando user_menu.sql...")
        print("-" * 50)
        
        # Verificar qué tablas existen realmente
        cursor = conexion.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas_existentes = [row[0] for row in cursor.fetchall()]
        print(f"📊 Tablas en la base de datos: {len(tablas_existentes)}")
        
        # Filtrar solo las tablas que existen
        tablas_a_procesar = [t for t in tablas if t in tablas_existentes]
        print(f"📋 Tablas a exportar: {', '.join(tablas_a_procesar)}")
        
        # Crear el archivo SQL
        with open('user_menu.sql', 'w', encoding='utf-8') as archivo:
            # Encabezado
            archivo.write("-- ============================================\n")
            archivo.write("-- SCRIPT DE INSERCIÓN: USUARIOS Y MENÚ\n")
            archivo.write("-- ============================================\n")
            archivo.write(f"-- Generado desde: {db_path}\n")
            archivo.write(f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            archivo.write("-- NOTA: Se excluye el usuario con id=1\n")
            archivo.write("-- ============================================\n\n")
            
            # Configuración para SQLite
            archivo.write("-- Desactivar verificación temporal de claves foráneas\n")
            archivo.write("PRAGMA foreign_keys = OFF;\n\n")
            
            archivo.write("-- Iniciar transacción\n")
            archivo.write("BEGIN TRANSACTION;\n\n")
            
            total_registros = 0
            
            # Procesar cada tabla
            for tabla in tablas_a_procesar:
                try:
                    print(f"📝 Procesando: {tabla}")
                    
                    # CONSULTA ESPECIAL PARA usuarios_user - EXCLUIR id=1
                    if tabla == 'usuarios_user':
                        # Obtener datos EXCLUYENDO id=1
                        cursor = conexion.execute(f"SELECT * FROM {tabla} WHERE id != 1")
                        excluir_nota = " (excluye id=1)"
                    else:
                        # Obtener todos los datos para otras tablas
                        cursor = conexion.execute(f'SELECT * FROM {tabla}')
                        excluir_nota = ""
                    
                    registros = cursor.fetchall()
                    
                    if not registros:
                        print(f"   ⚠ Vacía{excluir_nota}")
                        archivo.write(f"-- Tabla {tabla} está vacía{excluir_nota}\n\n")
                        continue
                    
                    # Obtener columnas
                    nombres_columnas = [desc[0] for desc in cursor.description]
                    
                    # Escribir en archivo
                    archivo.write(f"-- {'='*50}\n")
                    archivo.write(f"-- TABLA: {tabla} ({len(registros)} registros){excluir_nota}\n")
                    archivo.write(f"-- {'='*50}\n\n")
                    
                    # Generar INSERTs
                    for i, registro in enumerate(registros, 1):
                        valores = []
                        for valor in registro:
                            if valor is None:
                                valores.append('NULL')
                            elif isinstance(valor, str):
                                # Escapar comillas
                                valor_escapado = valor.replace("'", "''")
                                valores.append(f"'{valor_escapado}'")
                            elif isinstance(valor, (int, float)):
                                valores.append(str(valor))
                            elif isinstance(valor, bytes):
                                # Para BLOBs, intentar decodificar
                                try:
                                    valor_str = valor.decode('utf-8', errors='ignore')
                                    valores.append(f"'{valor_str}'")
                                except:
                                    valores.append('NULL')
                            else:
                                valores.append(f"'{str(valor)}'")
                        
                        # Solo escribir si tenemos valores
                        if len(valores) == len(registro):
                            insert_sql = f"INSERT INTO {tabla} ({', '.join(nombres_columnas)}) VALUES ({', '.join(valores)});\n"
                            archivo.write(insert_sql)
                        
                        # Mostrar progreso cada 100 registros
                        if i % 100 == 0:
                            print(f"   ... {i}/{len(registros)} registros")
                    
                    archivo.write(f"\n-- Fin de {tabla}\n\n")
                    total_registros += len(registros)
                    print(f"   ✅ {len(registros)} registros{excluir_nota}")
                    
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    archivo.write(f"-- ERROR procesando {tabla}: {e}\n\n")
            
            # Finalizar
            archivo.write("-- Finalizar transacción\n")
            archivo.write("COMMIT;\n\n")
            
            archivo.write("-- Reactivar verificación de claves foráneas\n")
            archivo.write("PRAGMA foreign_keys = ON;\n\n")
            
            # Resumen
            archivo.write("-- ============================================\n")
            archivo.write("-- RESUMEN\n")
            archivo.write("-- ============================================\n")
            archivo.write(f"-- Total registros insertados: {total_registros}\n")
            archivo.write(f"-- Total tablas procesadas: {len(tablas_a_procesar)}\n")
            archivo.write("-- ============================================\n")
        
        conexion.close()
        
        print("-" * 50)
        print(f"🎉 ¡Archivo generado: user_menu.sql!")
        print(f"📊 Total: {total_registros} registros")
        
        # Mostrar tamaño del archivo
        tamaño = os.path.getsize('user_menu.sql')
        print(f"📏 Tamaño: {tamaño:,} bytes ({tamaño/1024:.1f} KB)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal"""
    print("=" * 60)
    print("🛠️  GENERADOR DE SCRIPT SQL - NEUMATIC")
    print("=" * 60)
    
    # Opción 1: Ruta específica (la que mencionaste)
    ruta_especifica = "D:/PROJECT_NEUMATIC/neumatic/data/db_neumatic.db"
    
    if os.path.exists(ruta_especifica):
        print(f"📂 Usando ruta específica: {ruta_especifica}")
        generar_inserts_en_un_archivo(ruta_especifica)
    else:
        # Opción 2: Buscar automáticamente
        print("🔍 Buscando base de datos...")
        db_path = encontrar_base_datos()
        
        if db_path:
            generar_inserts_en_un_archivo(db_path)
        else:
            print("\n❌ No se encontró la base de datos.")
            print("\n💡 Especifica la ruta manualmente:")
            print(f"   python genera_user_menu.py ruta\\a\\db_neumatic.db")
            
            # Preguntar al usuario
            ruta_manual = input("\n📁 Ingresa la ruta de la base de datos: ").strip()
            if ruta_manual and os.path.exists(ruta_manual):
                generar_inserts_en_un_archivo(ruta_manual)
            else:
                print("❌ Ruta no válida o archivo no existe.")

# Punto de entrada
if __name__ == "__main__":
    main()
# user_menu_genera.py
import sqlite3
import os
from datetime import datetime

# RUTA DIRECTA - Modifica esta línea con tu ruta exacta
DB_PATH = "D:/PROJECT_NEUMATIC/neumatic/data/db_neumatic.db"

def generar_sql():
    """Genera script SQL excluyendo registros problemáticos"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ No se encuentra: {DB_PATH}")
        return
    
    print(f"📂 Conectando a: {DB_PATH}")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Tablas en orden con reglas de exclusión
        tablas_config = {
            'auth_group': {
                'where': None,  # No excluir ningún grupo
                'exclude_ids': []  # Mantener todos los grupos
            },
            'auth_group_permissions': {
                'where': None,
                'exclude_ids': []
            },
            'usuarios_user': {
                'where': "id != 1",  # Excluir el superusuario (id=1)
                'exclude_ids': [1]
            },
            'usuarios_user_groups': {
                'where': "user_id != 1",  # Excluir grupos del superusuario
                'exclude_ids': []  # Se filtra por WHERE
            },
            'menu_menuheading': {
                'where': None,
                'exclude_ids': []
            },
            'menu_menuitem': {
                'where': None,
                'exclude_ids': []
            },
            'menu_menuitem_groups': {
                'where': None,
                'exclude_ids': []
            }
        }
        
        print("🔧 Generando user_menu.sql...")
        print("-" * 50)
        
        with open('user_menu.sql', 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("-- ============================================\n")
            f.write("-- SCRIPT DE INSERCIÓN: USUARIOS Y MENÚ\n")
            f.write("-- ============================================\n")
            f.write(f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Desde: {DB_PATH}\n")
            f.write("-- NOTA: Se excluye el superusuario (id=1)\n")
            f.write("-- ============================================\n\n")
            
            f.write("PRAGMA foreign_keys = OFF;\n")
            f.write("BEGIN TRANSACTION;\n\n")
            
            total_registros = 0
            tabla_info = []
            
            for tabla, config in tablas_config.items():
                try:
                    # Verificar si existe
                    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabla}'")
                    if not cursor.fetchone():
                        print(f"⚠  {tabla}: No existe")
                        continue
                    
                    # Construir consulta
                    where_clause = f" WHERE {config['where']}" if config['where'] else ""
                    query = f"SELECT COUNT(*) FROM {tabla}{where_clause}"
                    
                    cursor.execute(query)
                    count = cursor.fetchone()[0]
                    
                    if count == 0:
                        print(f"📭 {tabla}: Vacía o todos excluidos")
                        f.write(f"-- {tabla}: No hay registros o todos fueron excluidos\n")
                        continue
                    
                    # Obtener total original (para comparación)
                    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                    total_original = cursor.fetchone()[0]
                    
                    excluidos = total_original - count
                    info_msg = f"{tabla}: {count} registros"
                    if excluidos > 0:
                        info_msg += f" (excluidos: {excluidos})"
                    
                    print(f"📝 {info_msg}")
                    
                    # Obtener columnas
                    cursor.execute(f"SELECT * FROM {tabla} LIMIT 1")
                    columnas = [desc[0] for desc in cursor.description]
                    
                    # Escribir comentario
                    f.write(f"\n-- {tabla}\n")
                    if config['where']:
                        f.write(f"-- WHERE: {config['where']}\n")
                    
                    # Obtener datos con WHERE si aplica
                    select_query = f"SELECT * FROM {tabla}{where_clause} ORDER BY id"
                    cursor.execute(select_query)
                    
                    registros_insertados = 0
                    for registro in cursor.fetchall():
                        # Verificar si está en exclude_ids
                        if 'id' in columnas:
                            id_index = columnas.index('id')
                            record_id = registro[id_index]
                            
                            if record_id in config.get('exclude_ids', []):
                                continue
                        
                        # Construir valores
                        valores = []
                        for valor in registro:
                            if valor is None:
                                valores.append('NULL')
                            elif isinstance(valor, str):
                                # Escapar comillas simples
                                valor_escapado = valor.replace("'", "''")
                                valores.append(f"'{valor_escapado}'")
                            elif isinstance(valor, (int, float)):
                                valores.append(str(valor))
                            elif isinstance(valor, bytes):
                                # Para BLOBs (como contraseñas encriptadas)
                                try:
                                    valor_str = valor.decode('utf-8')
                                    valores.append(f"'{valor_str}'")
                                except:
                                    # Si no se puede decodificar, usar NULL
                                    valores.append('NULL')
                            else:
                                valores.append(f"'{str(valor)}'")
                        
                        # Escribir INSERT
                        f.write(f"INSERT INTO {tabla} ({','.join(columnas)}) VALUES ({','.join(valores)});\n")
                        registros_insertados += 1
                        total_registros += 1
                    
                    tabla_info.append((tabla, registros_insertados, excluidos))
                    print(f"   ✅ Insertados: {registros_insertados}")
                    
                except Exception as e:
                    print(f"❌ Error en {tabla}: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Finalizar
            f.write("\nCOMMIT;\n")
            f.write("PRAGMA foreign_keys = ON;\n\n")
            
            # Resumen detallado
            f.write("-- ============================================\n")
            f.write("-- RESUMEN DETALLADO\n")
            f.write("-- ============================================\n")
            for tabla, insertados, excluidos in tabla_info:
                if excluidos > 0:
                    f.write(f"-- {tabla}: {insertados} insertados, {excluidos} excluidos\n")
                else:
                    f.write(f"-- {tabla}: {insertados} insertados\n")
            
            f.write(f"-- TOTAL REGISTROS INSERTADOS: {total_registros}\n")
            f.write("-- ============================================\n")
        
        conn.close()
        
        print("-" * 50)
        print(f"🎉 ¡user_menu.sql generado exitosamente!")
        print(f"📊 Total registros insertados: {total_registros}")
        
        # Mostrar resumen por tabla
        if tabla_info:
            print("\n📋 Resumen por tabla:")
            for tabla, insertados, excluidos in tabla_info:
                if excluidos > 0:
                    print(f"   • {tabla}: {insertados} registros ({excluidos} excluidos)")
                else:
                    print(f"   • {tabla}: {insertados} registros")
        
        # Verificar archivo
        if os.path.exists('user_menu.sql'):
            size = os.path.getsize('user_menu.sql')
            print(f"📏 Tamaño del archivo: {size:,} bytes ({size/1024:.1f} KB)")
            
            # Mostrar primeras líneas como verificación
            print("\n👀 Vista previa (primeras 3 líneas de usuarios):")
            try:
                with open('user_menu.sql', 'r', encoding='utf-8') as check:
                    lines = check.readlines()
                    usuarios_lines = [l for l in lines if 'usuarios_user' in l][:3]
                    for line in usuarios_lines[:3]:
                        if line.strip():
                            print(f"   {line.strip()[:100]}...")
            except:
                pass
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def verificar_exclusiones():
    """Verifica qué registros se están excluyendo"""
    
    if not os.path.exists(DB_PATH):
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n🔍 Verificando exclusiones:")
    print("-" * 40)
    
    # Verificar usuarios
    cursor.execute("SELECT id, username, email, is_superuser FROM usuarios_user ORDER BY id")
    usuarios = cursor.fetchall()
    
    print("👥 Usuarios en la base de datos:")
    for user in usuarios:
        id_user, username, email, is_super = user
        marca = "👑" if is_super else "👤"
        excluir = " (🚫 EXCLUIR)" if id_user == 1 else ""
        print(f"   {marca} ID {id_user}: {username} ({email}){excluir}")
    
    # Verificar si hay más superusuarios
    cursor.execute("SELECT COUNT(*) FROM usuarios_user WHERE is_superuser = 1")
    super_count = cursor.fetchone()[0]
    print(f"\n   Superusuarios totales: {super_count}")
    
    conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 GENERADOR SQL - EXCLUYENDO SUPERUSUARIO")
    print("=" * 60)
    
    # Primero verificar qué se va a excluir
    verificar_exclusiones()
    
    print("\n" + "=" * 60)
    
    # Preguntar confirmación
    respuesta = input("\n¿Continuar generando el script? (s/n): ").strip().lower()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        generar_sql()
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
        print("\n💡 INSTRUCCIONES DE USO:")
        print("   1. Asegúrate de tener las tablas creadas (python manage.py migrate)")
        print("   2. Crea primero el superusuario: python manage.py createsuperuser")
        print("   3. Ejecuta el script: sqlite3 tu_base.db < user_menu.sql")
        print("\n⚠️  NOTA: El superusuario (id=1) ha sido excluido del script")
    else:
        print("❌ Proceso cancelado")
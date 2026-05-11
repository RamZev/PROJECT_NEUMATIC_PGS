# neumatic/data_load/actualiza_user2.py
import os
import sys
import django
import json
import traceback

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.insert(0, BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.usuarios.models import User
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.base_models import PuntoVenta
from apps.maestros.models.vendedor_models import Vendedor


def actualizar_usuarios_desde_json():
    """Recorre el archivo JSON y actualiza todos los usuarios"""
    
    # Obtener la ruta del archivo JSON (misma carpeta que este script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'usuarios_user.json')
    
    # Verificar si el archivo existe
    if not os.path.exists(json_path):
        print(f"❌ Error: No se encuentra el archivo {json_path}")
        return
    
    try:
        # Leer el archivo JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            usuarios_json = json.load(file)
        
        print(f"📖 Archivo JSON cargado correctamente. Total de usuarios: {len(usuarios_json)}")
        print("=" * 60)
        
        # Contadores para estadísticas
        total_usuarios = 0
        usuarios_actualizados = 0
        errores = []
        usuarios_no_encontrados = []
        
        # Recorrer cada usuario en el JSON
        for usuario_data in usuarios_json:
            total_usuarios += 1
            user_id = usuario_data.get('id')
            username = usuario_data.get('username', 'Sin nombre')
            
            print(f"\n🔄 Procesando usuario ID: {user_id} ({username})")
            
            try:
                # Buscar el usuario en la base de datos
                usuario = User.objects.get(id=user_id)
                
                # Obtener los valores del JSON
                jerarquia = usuario_data.get('jerarquia')
                iniciales = usuario_data.get('iniciales')
                id_punto_venta_valor = usuario_data.get('id_punto_venta_id')
                id_sucursal_valor = usuario_data.get('id_sucursal_id')
                id_vendedor_valor = usuario_data.get('id_vendedor_id')
                
                # Variables para almacenar si hubo cambios
                cambios = []
                
                # Actualizar campos simples
                if jerarquia is not None and usuario.jerarquia != jerarquia:
                    usuario.jerarquia = jerarquia
                    cambios.append(f"jerarquia: {jerarquia}")
                
                if iniciales is not None and usuario.iniciales != iniciales:
                    usuario.iniciales = iniciales
                    cambios.append(f"iniciales: {iniciales}")
                
                # Actualizar id_punto_venta (campo ForeignKey)
                if id_punto_venta_valor is not None:
                    try:
                        punto_venta = PuntoVenta.objects.get(id_punto_venta=id_punto_venta_valor)
                        if usuario.id_punto_venta != punto_venta:
                            usuario.id_punto_venta = punto_venta
                            cambios.append(f"id_punto_venta: {id_punto_venta_valor}")
                    except PuntoVenta.DoesNotExist:
                        errores.append(f"Usuario ID {user_id}: No existe PuntoVenta con id_punto_venta={id_punto_venta_valor}")
                        print(f"  ⚠️  Advertencia: No existe Punto de Venta con ID {id_punto_venta_valor}")
                
                # Actualizar id_sucursal (campo ForeignKey)
                if id_sucursal_valor is not None:
                    try:
                        sucursal = Sucursal.objects.get(id_sucursal=id_sucursal_valor)
                        if usuario.id_sucursal != sucursal:
                            usuario.id_sucursal = sucursal
                            cambios.append(f"id_sucursal: {id_sucursal_valor}")
                    except Sucursal.DoesNotExist:
                        errores.append(f"Usuario ID {user_id}: No existe Sucursal con id_sucursal={id_sucursal_valor}")
                        print(f"  ⚠️  Advertencia: No existe Sucursal con ID {id_sucursal_valor}")
                
                # Actualizar id_vendedor (campo ForeignKey)
                if id_vendedor_valor is not None:
                    try:
                        vendedor = Vendedor.objects.get(id_vendedor=id_vendedor_valor)
                        if usuario.id_vendedor != vendedor:
                            usuario.id_vendedor = vendedor
                            cambios.append(f"id_vendedor: {id_vendedor_valor}")
                    except Vendedor.DoesNotExist:
                        errores.append(f"Usuario ID {user_id}: No existe Vendedor con id_vendedor={id_vendedor_valor}")
                        print(f"  ⚠️  Advertencia: No existe Vendedor con ID {id_vendedor_valor}")
                
                # Guardar cambios si los hay
                if cambios:
                    usuario.save()
                    usuarios_actualizados += 1
                    print(f"  ✅ Usuario actualizado - Cambios: {', '.join(cambios)}")
                else:
                    print(f"  ℹ️  Sin cambios para este usuario")
                    
            except User.DoesNotExist:
                usuarios_no_encontrados.append(f"ID {user_id} ({username})")
                print(f"  ❌ Usuario no encontrado en la base de datos")
            except Exception as e:
                errores.append(f"Usuario ID {user_id}: {str(e)}")
                print(f"  ❌ Error al procesar: {str(e)}")
                traceback.print_exc()
        
        # Mostrar estadísticas finales
        print("\n" + "=" * 60)
        print("📊 ESTADÍSTICAS DE ACTUALIZACIÓN")
        print("=" * 60)
        print(f"✅ Total de usuarios procesados: {total_usuarios}")
        print(f"✅ Usuarios actualizados: {usuarios_actualizados}")
        print(f"⚠️ Usuarios no encontrados: {len(usuarios_no_encontrados)}")
        print(f"⚠️ Errores/Advertencias: {len(errores)}")
        
        if usuarios_no_encontrados:
            print("\n❌ Usuarios no encontrados en BD:")
            for usuario in usuarios_no_encontrados:
                print(f"  - {usuario}")
        
        if errores:
            print("\n⚠️ Lista de errores/advertencias:")
            for error in errores:
                print(f"  - {error}")
        
        print("\n✨ Proceso completado!")
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar el archivo JSON: {str(e)}")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        print("\n=== TRACEBACK COMPLETO ===")
        traceback.print_exc()
        print("===========================")


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 INICIANDO ACTUALIZACIÓN MASIVA DE USUARIOS")
    print("=" * 60)
    print("📁 Fuente: usuarios_user.json")
    print("📋 Campos a actualizar:")
    print("   - jerarquia")
    print("   - iniciales") 
    print("   - id_punto_venta (desde id_punto_venta_id del JSON)")
    print("   - id_sucursal (desde id_sucursal_id del JSON)")
    print("   - id_vendedor (desde id_vendedor_id del JSON)")
    print("=" * 60)
    
    actualizar_usuarios_desde_json()
    
    print("\n" + "=" * 60)
    print("🏁 FIN DEL PROCESO")
    print("=" * 60)
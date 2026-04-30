# neumatic/data_load/actualizar_usuario_admin.py
import os
import sys
import django
import traceback

# Añadir el directorio base del proyecto al sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.insert(0, BASE_DIR)  # Forzar que el directorio base esté en el path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neumatic.settings')
django.setup()

from apps.usuarios.models import User
from apps.maestros.models.sucursal_models import Sucursal
from apps.maestros.models.base_models import PuntoVenta
from apps.maestros.models.vendedor_models import Vendedor


def actualizar_usuario_administrador():
    """Actualiza el usuario con ID=1 con los valores específicos"""
    try:
        # Obtener el usuario con ID=1
        usuario = User.objects.get(id=1)

        print("pasó 1")
        
        # Obtener las instancias relacionadas
        punto_venta = PuntoVenta.objects.get(id_punto_venta=2)
        sucursal = Sucursal.objects.get(id_sucursal=2)
        vendedor = Vendedor.objects.get(id_vendedor=1)

        print("pasó 2")
        
        # Actualizar los campos
        usuario.id_punto_venta = punto_venta
        usuario.id_sucursal = sucursal
        usuario.id_vendedor = vendedor

        print("pasó 3")
        
        # Guardar los cambios
        usuario.save()
        
        print("✅ Usuario actualizado correctamente:")
        print(f"ID: {usuario.id}")
        print(f"Username: {usuario.username}")
        print(f"Punto de Venta: {punto_venta.id_punto_venta} - {punto_venta}")
        print(f"Sucursal: {sucursal.id_sucursal} - {sucursal}")
        print(f"Vendedor: {vendedor.id_vendedor} - {vendedor}")
        
    except User.DoesNotExist:
        print("❌ Error: No existe un usuario con ID=1")
        # Listar usuarios existentes
        usuarios = User.objects.all()[:5]
        if usuarios:
            print("\nUsuarios disponibles:")
            for u in usuarios:
                print(f"  ID: {u.id} - {u.username}")
    except PuntoVenta.DoesNotExist:
        print("❌ Error: No existe el Punto de Venta con ID=2")
        # Listar puntos de venta existentes
        puntos = PuntoVenta.objects.all()[:5]
        if puntos:
            print("\nPuntos de Venta disponibles:")
            for p in puntos:
                print(f"  ID: {p.id_punto_venta} - {p}")
    except Sucursal.DoesNotExist:
        print("❌ Error: No existe la Sucursal con ID=2")
        # Listar sucursales existentes
        sucursales = Sucursal.objects.all()[:5]
        if sucursales:
            print("\nSucursales disponibles:")
            for s in sucursales:
                print(f"  ID: {s.id_sucursal} - {s}")
    except Vendedor.DoesNotExist:
        print("❌ Error: No existe el Vendedor con ID=1")
        # Listar vendedores existentes
        vendedores = Vendedor.objects.all()[:5]
        if vendedores:
            print("\nVendedores disponibles:")
            for v in vendedores:
                print(f"  ID: {v.id_vendedor} - {v}")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        print("\n=== TRACEBOOK COMPLETO ===")
        traceback.print_exc()
        print("===========================")

if __name__ == '__main__':
    print("=" * 50)
    print("Iniciando actualización del usuario administrador...")
    print("=" * 50)
    actualizar_usuario_administrador()
# Pasos generales de Migración - Neumatic



1. Ejecutar en la carpeta data_load:  
   
   python 00_limpiar_migraciones.py

2. Eliminar manualmente la base de datos:
   
   neumatic\data\db_neumatic.db

3. Realizar las migraciones en la carpeta neumatic:
   
   python manage.py makemigrations
   
   python manage.py migrate

4. Crear el superusaurio en la carpeta neumatic:
   
   python manage.py createsuperuser

5. Ejecutar en la carpeta data_load:
   
   python 01_migra_base.py

6. Ejecutar en la carpeta data_load:
   
   python 02_migra_producto.py

7. Ejecutar en la carpeta data_load:
   
   python 03_migra_cliente.py

8. Ejecutar en la carpeta data_load:
   
   python 04_migra_factura.py

9. Ejecutar en la carpeta data_load:
   
   python 05_migra_recibo.py

10. Ejecutar en la carpeta data_load:
    
    python actualiza_user.py

11. Crear las vistas en DB Browser

12. Actualizar datos en el Sistema



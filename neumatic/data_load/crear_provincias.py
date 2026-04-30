import csv

def extraer_provincias(archivo_entrada, archivo_salida):
    """Extrae valores únicos de Provincia y Cod_Provincia de un archivo CSV y crea un nuevo archivo."""
    # Crear un conjunto para almacenar las provincias únicas
    provincias_unicas = set()

    # Leer el archivo de entrada
    with open(archivo_entrada, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Iterar sobre cada fila
        for row in reader:
            nombre_provincia = row['Provincia'].strip()
            codigo_provincia = row['Cod_Provincia'].strip()
            
            # Agregar al conjunto para evitar duplicados
            provincias_unicas.add((nombre_provincia, codigo_provincia))

    # Ordenar las provincias por código de provincia numéricamente
    provincias_ordenadas = sorted(provincias_unicas, key=lambda x: int(x[1]))

    # Escribir el archivo de salida
    with open(archivo_salida, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        # Escribir encabezados
        writer.writerow(['Provincia', 'Cod_Provincia'])

        # Escribir las filas únicas
        for nombre_provincia, codigo_provincia in provincias_ordenadas:
            writer.writerow([nombre_provincia, codigo_provincia])

    print(f"Archivo {archivo_salida} creado con éxito. Total de provincias: {len(provincias_ordenadas)}")

# Ruta del archivo de entrada y salida
archivo_entrada = 'Codigos-Postales-Argentina.csv'
archivo_salida = 'provincia.csv'

# Ejecutar la función
extraer_provincias(archivo_entrada, archivo_salida)

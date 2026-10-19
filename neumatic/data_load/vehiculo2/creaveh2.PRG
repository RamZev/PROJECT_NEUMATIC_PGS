CLOSE DATABASES
CLEAR ALL

* 1. Crear vehiculo2 copiando la estructura y datos
SELECT * FROM vehiculo INTO TABLE vehiculo2

* 2. Agregar los nuevos campos
ALTER TABLE vehiculo2 ADD COLUMN id_marca I
ALTER TABLE vehiculo2 ADD COLUMN id_modelo I

* 3. Limpiar REGISTROS VIEJOS y clientes no asignados
SELECT vehiculo2
DELETE FOR EMPTY(CLIENTE) OR EMPTY(VISITA) OR VISITA < {^2024-12-31}
DELETE FOR EMPTY(MARCA)
PACK

* 4. Limpiar espacios en blanco en marca y modelo
SELECT vehiculo2
REPLACE ALL MARCA WITH ALLTRIM(MARCA)
REPLACE ALL MODELO WITH ALLTRIM(MODELO)

* 5. Crear el archivo reporte_marcas.csv no repetidos
SELECT Marca, COUNT(*) as Cantidad;
	FROM vehiculo2; 
	GROUP BY Marca; 
	ORDER BY Marca; 
	INTO CURSOR marca_reporte
	
*SELECT marca_reporte
*BROWSE

COPY TO "reporte_marcas.csv" TYPE CSV

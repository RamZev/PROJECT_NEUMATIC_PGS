CLOSE ALL
USE stock EXCLUSIVE

* Paso 1: Cursor con todos los registros y su RECNO() real
SELECT deposito, codigo, RECNO() AS registro FROM stock ORDER BY codigo, deposito INTO CURSOR todos

* Paso 2: Registros a conservar (el primero de cada grupo)
SELECT MIN(registro) as registro_conservar FROM todos GROUP BY codigo, deposito INTO CURSOR conservar

* Paso 3: Registros a eliminar
SELECT t.registro, t.codigo, t.deposito FROM todos t WHERE t.registro NOT IN (SELECT registro_conservar FROM conservar) INTO CURSOR a_eliminar

* Crear índice en a_eliminar para poder usar SEEK
SELECT a_eliminar
INDEX ON registro TAG reg_idx

* Verlos
SELECT a_eliminar
BROWSE NORMAL TITLE "REGISTROS A ELIMINAR - CIERRE ESTA VENTANA PARA CONTINUAR"

* Preguntar si eliminar
IF MESSAGEBOX("¿Eliminar " + STR(RECCOUNT("a_eliminar")) + " registros?", 36, "Confirmar") = 6
    * Backup
    SELECT stock
    tabla = "stock_backup" + DTOS(DATE()) + ".dbf"
    COPY TO &tabla
    
	* Eliminar
    SCAN
        IF SEEK(RECNO(), "a_eliminar", "reg_idx")
            DELETE
        ENDIF
    ENDSCAN 
    PACK
    
    MESSAGEBOX("Eliminación completada", 64, "OK")
ENDIF

CLOSE ALL
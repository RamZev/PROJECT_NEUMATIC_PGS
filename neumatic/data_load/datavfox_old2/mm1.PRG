CLEAR 
CLOSE ALL 
SET DELETED ON 


USE usuarios  IN 0 
USE symdeperf IN 0 

SELECT symdeperf
GO BOTTOM 
SCATTER MEMVAR 

SELECT usuarios
SCAN 
	m.sec_usuperfil=usuarios.usuario
	INSERT INTO symdeperf FROM MEMVAR
	SELECT usuarios
ENDSCAN 
CLOSE DATABASES
CLEAR ALL

UPDATE detcom ;
SET id = compras.id ;
FROM compras ;
WHERE detcom.compro = compras.compro ;
  AND detcom.letra = compras.letra ;
  AND detcom.numero = compras.numero ;
  AND detcom.id = 0
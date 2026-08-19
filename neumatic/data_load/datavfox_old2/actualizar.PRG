
*---------------------------------------------------------- 19/08/2024
USE lista EXCLUSIVE 
ALTER TABLE lista ALTER COLUMN codfabrica C(21)

USE listamin EXCLUSIVE 
ALTER TABLE listamin ALTER COLUMN cai C(21)

USE medidasestados EXCLUSIVE 
ALTER TABLE medidasestados ALTER COLUMN cai C(21)

USE pedidos EXCLUSIVE 
ALTER TABLE pedidos ALTER COLUMN cai C(21)
CLOSE TABLES ALL 

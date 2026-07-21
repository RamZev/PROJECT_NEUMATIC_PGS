## Comprobantes Electrónicos



### **Modelos y Relaciones Clave**

- **`Factura` (Cabecera):** Es el modelo central. Almacena toda la información del comprobante (cliente, fechas, números, totales, estado, etc.). Sus relaciones más relevantes son:
  
  - `id_cliente`: Un cliente (obligatorio para la mayoría).
  
  - `id_comprobante_venta`: Define el tipo de comprobante (Factura A/B, Remito, Nota de Crédito, Presupuesto, etc.).
  
  - `id_sucursal` y `id_punto_venta`: Determinan la ubicación y numeración del comprobante.
  
  - `id_caja`: La caja a la que se asocia el movimiento, si corresponde.
  
  - `id_deposito`: El depósito desde el cual se descuenta/aumenta el stock.
  
  - `id_vendedor`: El vendedor asociado al cliente.
  
  - `cae`, `cae_vto`: Datos de la respuesta de ARCA para comprobantes electrónicos.
  
  - `estado`: Indica si el comprobante está "Pendiente", "Cobrado" o "Facturado" (en el caso de remitos).

- **`DetalleFactura` (Líneas):** Representa cada ítem del comprobante. Almacena el producto, cantidad, precios, descuentos e impuestos calculados.
  
  - `id_factura`: Relación con la cabecera (borrado en cascada).
  
  - `id_producto`: El producto o servicio vendido.
  
  - `id_operario`: Un operario asociado al detalle, obligatorio para ciertos servicios.

- **Modelos Relacionados Relevantes:**
  
  - **`Numero`:** Controla la numeración secuencial de los comprobantes por sucursal, punto de venta, tipo de comprobante y letra.
  
  - **`ProductoStock`:** Almacena el stock de cada producto por depósito. Se actualiza al crear o anular comprobantes.
  
  - **`Caja` / `CajaDetalle`:** Gestionan el estado de la caja (abierta/cerrada) y los movimientos de dinero.
  
  - **`Valida`:** Almacena autorizaciones temporales para operaciones especiales (vencimiento, límite de crédito, Nota de Crédito).
  
  - **`ComprobanteVenta`:** Actúa como un catálogo de tipos de comprobante, definiendo su comportamiento a través de múltiples flags y multiplicadores.

---

### **Casos de Uso (Enfocados en `factura_views.py`)**

1. **Listar Comprobantes Electrónicos (`FacturaListView`):**
   
   - **Descripción:** Muestra una lista paginada y filtrable de comprobantes.
   
   - **Filtros:**
     
     - Por sucursal (si el usuario no es superusuario o de jerarquía "A").
     
     - Por tipo de comprobante: Solo muestra los que son `electronica=True` o `remito=True`, excluyendo `recibo=True` y `presupuesto=True`.
     
     - Por búsqueda libre (ID, comprobante, número, CUIT, nombre del cliente).
   
   - **Alerta de Caja:** Verifica si existe una caja abierta para la sucursal y fecha actual. Si no, muestra una alerta en la vista.

2. **Crear Comprobante Electrónico (`FacturaCreateView`):**
   
   - **Descripción:** Es el proceso más complejo. Maneja la creación de un nuevo comprobante, desde la selección de cliente y productos hasta la emisión ante ARCA y la actualización de inventario.
   
   - **Flujo de Alto Nivel:**
     
     1. **Inicialización:** Se cargan diccionarios en el frontend (libro_iva, mult_venta, tipo_comprobante, etc.) para manejar la lógica del lado del cliente.
     
     2. **Validaciones de Caja y Depósito:** Se valida que exista un depósito seleccionado y que, para comprobantes con `mult_caja != 0`, exista una caja abierta para la fecha y sucursal.
     
     3. **Procesamiento del Cliente:** Se actualiza la información de contacto del cliente (móvil y email) con los datos ingresados en el comprobante si el cliente no los tenía registrados previamente.
     
     4. **Numeración y CAE:**
        
        - Se determina el tipo de numeración (`electronica`, `manual`, `automatica`) según el `ComprobanteVenta`.
        
        - **Si es `electronica`:**
        
        - Se obtiene un token de ARCA.
        
        - Se consulta el próximo número de comprobante a ARCA.
        
        - Se construye y envía un XML para obtener el CAE.
        
        - Se manejan reintentos en caso de error (código 10016).
        
        - Se guarda el CAE y su vencimiento en el modelo `Factura`.
        
        - Se actualiza la tabla `Numero` con el número asignado por ARCA.
     
     5. **Registro Contable y de Caja:**
        
        - Si la condición de venta es "Contado" (`condicion_comprobante=1`) y no es un remito, el comprobante se marca como "Cobrado".
        
        - Se crea un registro en `CajaDetalle` con el importe total.
     
     6. **Gestión de Notas de Crédito:** Se gestiona la lógica para actualizar el saldo del comprobante asociado.
     
     7. **Guardado:** Se guarda la cabecera (`Factura`), los detalles (`DetalleFactura`) y los seriales (`SerialFactura`).
     
     8. **Actualización de Inventario:** Se actualiza el stock en `ProductoStock` usando la fórmula `stock += (cantidad * mult_stock)`.
     
     9. **Actualización de Documentos Asociados:** Si el comprobante es un "pendiente" (ej. factura de un remito), se actualiza el estado del documento origen a "Facturado" ('F').

3. **Ver un Comprobante (`FacturaUpdateView`):**
   
   - **Descripción:** Muestra los detalles de un comprobante existente en modo de solo lectura. Aunque la URL usa "update", la lógica y el contexto (`is_edit = True`) se utilizan para deshabilitar todos los campos del formulario en el frontend. La funcionalidad de actualización real no está implementada en el código de `factura_views.py` (la vista hereda de `MaestroDetalleUpdateView` pero no define lógica de actualización de datos significativa).

4. **Eliminar un Comprobante (`FacturaDeleteView`):**
   
   - **Descripción:** Prohíbe la eliminación de comprobantes electrónicos. Solo permite la eliminación de otros tipos de comprobantes, y siempre que no tengan relaciones protegidas (integridad referencial).

---

### **Reglas de Negocio (Enfocadas en `factura_views.py`)**

#### **Reglas de Validación y Flujo**

1. **Validación de Caja:**
   
   - **Regla:** Antes de crear un comprobante, si `ComprobanteVenta.mult_caja != 0`, se debe validar la existencia de una caja.
   
   - **Condición:** Debe existir una `Caja` para la `id_sucursal` y `fecha_comprobante` del comprobante, y su campo `caja_cerrada` debe ser `False`.
   
   - **Consecuencia:** Si no se cumple, se muestra un mensaje de error y se redirige a la lista de comprobantes.

2. **Numeración de Comprobantes:**
   
   - **Regla:** El número del comprobante se obtiene de manera diferente según el tipo.
   
   - **`electronica`:** El número es asignado directamente por ARCA. El sistema solo lo almacena y actualiza la tabla `Numero` para llevar un control interno, pero sin afectar la numeración, ya que ARCA es la fuente de la verdad.
   
   - **`manual`:** El número es ingresado por el usuario. El sistema valida que sea mayor que el último número registrado en la tabla `Numero`.
   
   - **`automatica` (Remitos):** El número es autoincremental, obtenido de la tabla `Numero`.

3. **Cálculo y Estructura del IVA para ARCA:**
   
   - **Regla:** Para comprobantes electrónicos, el IVA se debe agrupar por código de alícuota de ARCA (`codigo_alicuota`).
   
   - **Proceso:**
     
     1. Se crea un mapeo entre el porcentaje de IVA (`alic_iva`) del detalle y el `codigo_alicuota` correspondiente.
     
     2. Se recorre cada detalle del comprobante y se acumulan las bases imponibles (`gravado`) y los importes de IVA por código.
     
     3. Esta estructura acumulada es la que se envía en el XML a ARCA.

4. **Lógica de la Nota de Crédito:**
   
   - **Regla:** La creación de una Nota de Crédito (libro_iva=True y mult_venta < 0) implica una operación que afecta el comprobante original.
   
   - **Proceso:**
     
     1. Se debe seleccionar un `id_comprobante_asociado`.
     
     2. El monto de la Nota de Crédito se suma al campo `entrega` del comprobante asociado.
     
     3. Si el nuevo `entrega` es igual o superior al `total` del comprobante asociado, se marca como "Cobrado" (estado='C').
     
     4. La Nota de Crédito en sí se marca como "Cobrada".
   
   - **Restricción:** Se utiliza `select_for_update()` para bloquear el registro del comprobante asociado y evitar condiciones de carrera durante la actualización.

5. **Actualización de Cliente:**
   
   - **Regla:** El sistema actualiza la información de contacto del cliente en el momento de la facturación para mantener los datos al día.
   
   - **Lógica:**
     
     - **Móvil:** Si el campo `movil_factura` del formulario tiene valor:
       
       - Si el cliente no tiene `movil_cliente`, se actualiza `movil_cliente`.
       
       - Si el cliente tiene un `movil_cliente` diferente, se actualiza su `telefono_cliente` con el nuevo valor.
     
     - **Email:** Si el campo `email_factura` del formulario tiene valor:
       
       - Si el cliente no tiene `email_cliente`, se actualiza `email_cliente`.
       
       - Si el cliente tiene un `email_cliente` diferente, se actualiza su `email2_cliente` con el nuevo valor.

6. **Anulación de Remitos:**
   
   - **Regla:** La anulación de un remito es una operación irreversible que debe ser segura.
   
   - **Validaciones Previas:**
     
     1. El documento debe ser un remito (`ComprobanteVenta.remito = True`).
     
     2. El remito no debe estar facturado (`estado != 'F'`).
     
     3. No deben existir otras facturas que lo referencien como `id_comprobante_asociado` o a través de los campos `comprobante_remito`/`remito`.
   
   - **Proceso de Anulación (Transacción Atómica):**
     
     1. **Revertir Stock:** Se invierte la lógica de actualización de inventario. El stock se incrementa o decrementa en la cantidad opuesta a la que se aplicó al crear el remito.
     
     2. **Revertir Caja:** Se eliminan los registros de `CajaDetalle` asociados al remito (los que tienen `tipo_movimiento=1`).
     
     3. **Eliminar Físicamente:** Se elimina el registro del remito de la base de datos, lo que por cascada elimina sus detalles y seriales.

#### **Reglas de Integridad Referencial y Control de Concurrencia**

7. **Uso de `select_for_update()`:** Se utiliza en puntos críticos para evitar condiciones de carrera, como en la obtención y actualización de la tabla `Numero` y en la actualización del stock (`ProductoStock`).

8. **Transacciones Atómicas:** Todo el proceso de creación (`form_valid` en `FacturaCreateView`) y anulación de remitos se ejecuta dentro de un bloque `with transaction.atomic():`. Esto asegura que si falla alguna operación (ej. error de ARCA, falla de base de datos), todos los cambios realizados hasta ese punto se revierten, manteniendo la consistencia de los datos.

9. **Integridad Referencial:** El modelo está diseñado para que la eliminación de una factura elimine en cascada sus detalles y seriales (`on_delete=models.CASCADE` en `DetalleFactura` y `SerialFactura`). Las relaciones con otros modelos clave (`Cliente`, `Producto`, `Caja`, `ComprobanteVenta`) usan `PROTECT` para evitar la eliminación de registros que estén siendo referenciados.





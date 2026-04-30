# Manual de Construcción: Módulo de Compras

## 1. MODELOS - Estructura de Datos

### 1.1 Modelo Base Genérico (`ModeloBaseGenerico`)

**Propósito**: Proporcionar campos de auditoría comunes a todos los modelos.

```python
class ModeloBaseGenerico(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.PROTECT)  # Usuario que realiza la acción
    usuario = models.CharField(max_length=20)                    # Nombre de usuario
    estacion = models.CharField(max_length=20)                   # Nombre del equipo
    fcontrol = models.CharField(max_length=22)                   # Fecha/hora de control

    class Meta:
        abstract = True  # No crea tabla en BD, solo para herencia
```

**Método `save()` automáticamente**:

- Captura el nombre del equipo (`socket.gethostname()`)
- Registra fecha/hora actual en formato `YYYY-MM-DD HH:MM:SS`

### 1.2 Modelo Principal: `Compra`

**Campos Clasificados**:

#### A. Identificación y Control

```python
id_compra = models.AutoField(primary_key=True)           # ID único autoincremental
estatus_comprabante = models.BooleanField(default=True)  # Activo/Inactivo
```

#### B. Relaciones con Catálogos

```python
id_sucursal = models.ForeignKey(Sucursal)               # Sucursal origen
id_punto_venta = models.ForeignKey(PuntoVenta)          # Punto de venta
id_deposito = models.ForeignKey(ProductoDeposito)       # Depósito destino
id_comprobante_compra = models.ForeignKey(ComprobanteCompra)  # Tipo de comprobante
id_proveedor = models.ForeignKey(Proveedor)             # Proveedor
id_provincia = models.ForeignKey(Provincia)             # Provincia fiscal
```

#### C. Datos del Comprobante

```python
compro = models.CharField(max_length=3)                 # Código (ej: "FAC")
letra_comprobante = models.CharField(max_length=1)      # Letra (A, B, C)
numero_comprobante = models.IntegerField()              # Número único
fecha_comprobante = models.DateField()                  # Fecha emisión
fecha_vencimiento = models.DateField()                  # Fecha vencimiento
```

#### D. Montos e Impuestos

```python
gravado = models.DecimalField(max_digits=14, decimal_places=2)      # Base imponible
exento = models.DecimalField(max_digits=14, decimal_places=2)       # Monto exento
iva = models.DecimalField(max_digits=14, decimal_places=2)          # IVA calculado
total = models.DecimalField(max_digits=14, decimal_places=2)        # Total general
```

#### E. Propiedades Especiales

```python
@property
def numero_comprobante_formateado(self):
    # Convierte 12345678 → "1234-5678"
    numero = str(self.numero_comprobante).strip().zfill(12)
    return f"{numero[:4]}-{numero[4:]}"
```

#### F. Validaciones Personalizadas

```python
def clean(self):
    # Validaciones de negocio
    if not self.fecha_comprobante:
        raise ValidationError("Fecha de emisión obligatoria")
    if self.fecha_vencimiento < self.fecha_comprobante:
        raise ValidationError("Vencimiento no puede ser anterior a emisión")
```

### 1.3 Modelo Detalle: `DetalleCompra`

**Relación 1-a-Muchos** con `Compra`:

```python
id_detalle_compra = models.AutoField(primary_key=True)
id_compra = models.ForeignKey(Compra, on_delete=models.CASCADE)  # Elimina en cascada
id_producto = models.ForeignKey(Producto)                        # Producto comprado
cantidad = models.DecimalField(max_digits=7, decimal_places=2)   # Cantidad
precio = models.DecimalField(max_digits=12, decimal_places=2)    # Precio unitario
total = models.DecimalField(max_digits=12, decimal_places=2)     # Total línea
despacho = models.CharField(max_length=16)                       # Número de despacho
```

## 2. CARACTERÍSTICAS TÉCNICAS DE LOS MODELOS

### 2.1 Configuración de Base de Datos

```python
class Meta:
    db_table = "compra"                          # Nombre real en BD
    verbose_name = 'Compra'                      # Nombre singular
    verbose_name_plural = 'Compras'              # Nombre plural
```

### 2.2 Representación de Objetos

```python
def __str__(self):
    # Ejemplo: "FAC A 0001-234567"
    return f"{self.compro} {self.letra} {self.numero_comprobante_formateado}"
```

### 2.3 Validaciones Automáticas

- **Campos obligatorios**: Comprobante, número, fechas
- **Rangos numéricos**: Números entre 1-99,999,999
- **Consistencia temporal**: Vencimiento ≥ Emisión

## 3. RELACIONES CLAVE

### 3.1 Con Catálogos del Sistema

```
Compra → Sucursal (PROTECT)
Compra → PuntoVenta (PROTECT)  
Compra → ProductoDeposito (PROTECT)
Compra → ComprobanteCompra (PROTECT)
Compra → Proveedor (PROTECT)
```

### 3.2 Con Detalles

```
Compra ←→ DetalleCompra (CASCADE)
```

### 3.3 Política de Eliminación

- **PROTECT**: Previene eliminación si hay relaciones
- **CASCADE**: Elimina detalles si se borra la compra

## 4. PATRONES DE DISEÑO IMPLEMENTADOS

### 4.1 Modelo Base Abstracto

- **Ventaja**: Auditoría consistente en todos los modelos
- **Reutilización**: Campos comunes sin duplicación

### 4.2 Separación Encabezado-Detalle

- **Normalización**: Evita redundancia de datos
- **Flexibilidad**: Múltiples productos por compra

### 4.3 Propiedades Calculadas

- **Formateo**: Presentación amigable de números
- **Mantenibilidad**: Lógica centralizada

## 5. FORMULARIOS - Capa de Presentación y Validación

### 5.1 Formulario Principal: `CompraForm`

**Configuración Básica**:

```python
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = "__all__"  # Incluye todos los campos del modelo
```

#### Campos Personalizados para UX:

```python
buscar_proveedor = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={
        'readonly': 'readonly',
        'id': 'buscar_proveedor'
    })
)

nombre_sucursal = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={'readonly': 'readonly'})
)
```

#### Configuración de Widgets por Tipo:

```python
widgets = {
    # Campos ocultos
    "id_compra": forms.HiddenInput(),

    # Selects
    "id_deposito": forms.Select(attrs=formclassselect),
    "id_comprobante_compra": forms.Select(attrs=formclassselect),

    # Campos de solo lectura
    "compro": forms.TextInput(attrs={'readonly': 'readonly'}),
    "numero_comprobante": forms.TextInput(attrs={'readonly': 'readonly'}),

    # Campos de fecha
    "fecha_comprobante": forms.TextInput(attrs={'type': 'date'}),

    # Montos (solo lectura, calculados)
    "total": forms.TextInput(attrs={'readonly': 'readonly'}),
}
```

#### Filtrado Dinámico en `__init__`:

```python
def __init__(self, *args, **kwargs):
    usuario = kwargs.pop('usuario', None)
    super().__init__(*args, **kwargs)

    # Filtrar depósitos por sucursal del usuario
    if usuario and usuario.id_sucursal:
        self.fields['id_deposito'].queryset = ProductoDeposito.objects.filter(
            id_sucursal=usuario.id_sucursal
        )

    # 🔥 FILTRAR SOLO COMPROBANTES CON REMITO = TRUE
    self.fields['id_comprobante_compra'].queryset = ComprobanteCompra.objects.filter(
        estatus_comprobante_compra=True,
        remito=True
    ).order_by('nombre_comprobante_compra')
```

### 5.2 Formulario de Detalle: `DetalleCompraForm`

**Campos Especiales para Interfaz**:

```python
medida = forms.CharField(
    label="Medida",
    required=False,
    widget=forms.TextInput(attrs={'readonly': 'readonly'})
)

producto_venta = forms.CharField(
    label="Nombre producto", 
    required=False,
    widget=forms.TextInput(attrs={'readonly': 'readonly'})
)
```

**Configuración de Widgets**:

```python
widgets = {
    'id_detalle_compra': forms.HiddenInput(),
    'id_compra': forms.HiddenInput(),
    'id_producto': forms.HiddenInput(),

    'cantidad': forms.NumberInput(attrs={
        'class': 'form-control form-control-sm border border-primary text-end',
        'step': '0.01'
    }),

    'despacho': forms.TextInput(attrs={
        'class': 'form-control form-control-sm border border-primary'
    }),
}
```

**Inicialización con Datos del Producto**:

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if self.instance and self.instance.id_producto:
        # Autocompletar medida y nombre del producto
        self.fields['medida'].initial = self.instance.id_producto.medida
        self.fields['producto_venta'].initial = self.instance.id_producto.nombre_producto
```

### 5.3 FormSet para Múltiples Detalles

**Creación del FormSet**:

```python
DetalleCompraFormSet = inlineformset_factory(
    Compra,                           # Modelo padre
    DetalleCompra,                    # Modelo hijo  
    form=DetalleCompraForm,           # Formulario a usar
    extra=0                           # Filas vacías iniciales
)
```

## 6. VISTAS - Lógica de Negocio

### 6.1 Vistas Genéricas Base (`msdt_views_generics.py`)

#### `MaestroDetalleListView` - Listado con Búsqueda

```python
class MaestroDetalleListView(ListView):
    search_fields = []        # Campos donde buscar
    ordering = []            # Ordenamiento por defecto
    paginate_by = 8          # Paginación

    def get_queryset(self):
        # Búsqueda dinámica sobre search_fields
        query = self.request.GET.get('busqueda', None)
        if query:
            search_conditions = Q()
            for field in self.search_fields:
                search_conditions |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(search_conditions)

        return queryset.order_by(*self.ordering)
```

#### `MaestroDetalleCreateView` - Creación con Permisos

```python
class MaestroDetalleCreateView(PermissionRequiredMixin, CreateView):
    def form_valid(self, form):
        # Auditoría automática
        form.instance.id_user = self.request.user
        form.instance.usuario = self.request.user.username

        try:
            with transaction.atomic():  # Transacción atómica
                return super().form_valid(form)
        except Exception as e:
            # Manejo elegante de errores
            context = self.get_context_data(form)
            context['transaction_error'] = str(e)
            return self.render_to_response(context)
```

### 6.2 Vista Específica: `CompraListView`

**Configuración para Compras**:

```python
class CompraListView(MaestroDetalleListView):
    model = Compra
    template_name = "ventas/maestro_detalle_list.html"

    search_fields = [
        'id_compra',
        'compro', 
        'numero_comprobante',
        'id_proveedor__nombre_proveedor',
    ]

    ordering = ['-id_compra']  # Más recientes primero

    # 🔥 FILTRO CRÍTICO: Solo comprobantes con remito
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id_comprobante_compra__remito=True)

        # Filtro por sucursal del usuario
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(id_sucursal=user.id_sucursal)

        return queryset
```

### 6.3 Vista Específica: `CompraCreateView`

#### Preparación del Contexto

```python
def get_context_data(self, **kwargs):
    data = super().get_context_data(**kwargs)

    # Formsets para detalles
    if self.request.POST:
        data['formset_detalle'] = DetalleCompraFormSet(self.request.POST)
    else:
        data['formset_detalle'] = DetalleCompraFormSet(instance=self.object)

    # Diccionarios para JavaScript
    libro_iva_dict = {str(c.id_comprobante_compra): c.libro_iva 
                     for c in ComprobanteCompra.objects.all()}
    data['libro_iva_dict'] = json.dumps(libro_iva_dict)

    data['is_edit'] = False  # Indicar modo creación

    return data
```

#### Lógica Principal de Grabación

```python
def form_valid(self, form):
    context = self.get_context_data()
    formset_detalle = context['formset_detalle']

    if not formset_detalle.is_valid():
        return self.form_invalid(form)

    try:
        with transaction.atomic():
            # 1. Validación de depósito
            deposito = form.cleaned_data.get('id_deposito')
            if not deposito:
                form.add_error('id_deposito', 'Debe seleccionar un depósito')
                return self.form_invalid(form)

            # 2. Guardar compra (encabezado)
            self.object = form.save()

            # 3. Guardar detalles
            formset_detalle.instance = self.object
            detalles = formset_detalle.save()

            # 4. ACTUALIZAR INVENTARIO Y DESPACHOS
            for detalle in detalles:
                if (hasattr(detalle.id_producto, 'tipo_producto') and
                    detalle.id_producto.tipo_producto == "P" and
                    detalle.cantidad):

                    # A. Actualizar stock
                    ProductoStock.objects.select_for_update().filter(
                        id_producto=detalle.id_producto,
                        id_deposito=deposito
                    ).update(
                        stock=F('stock') + (detalle.cantidad * 
                                self.object.id_comprobante_compra.mult_stock),
                        fecha_producto_stock=form.cleaned_data['fecha_comprobante']
                    )

                    # B. Actualizar despachos en Producto
                    if hasattr(detalle, 'despacho') and detalle.despacho:
                        producto_obj = detalle.id_producto
                        Producto.objects.filter(id_producto=producto_obj.id_producto).update(
                            despacho_2=producto_obj.despacho_1,  # Mover a histórico
                            despacho_1=detalle.despacho          # Nuevo valor
                        )

            messages.success(self.request, f"Compra {self.object.numero_comprobante} creada")
            return redirect(self.get_success_url())

    except Exception as e:
        messages.error(self.request, f"Error inesperado: {str(e)}")
        return self.form_invalid(form)
```

#### Valores Iniciales por Usuario

```python
def get_initial(self):
    initial = super().get_initial()
    usuario = self.request.user

    initial['id_sucursal'] = usuario.id_sucursal
    initial['id_punto_venta'] = usuario.id_punto_venta
    initial['fecha_comprobante'] = timezone.now().date()
    initial['fecha_registro'] = timezone.now().date()

    return initial
```

## 7. RUTAS - Configuración de URLs

### 7.1 Archivo Principal `urls.py`

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('ventas/', include('apps.ventas.urls')),  # Incluye rutas de ventas
]
```

### 7.2 Rutas Específicas de Compras

```python
from .views.compra_views import (
    CompraListView, CompraCreateView, 
    CompraUpdateView, CompraDeleteView
)

urlpatterns = [
    path('compra/listar/', CompraListView.as_view(), name='compra_list'),
    path('compra/crear/', CompraCreateView.as_view(), name='compra_create'),
    path('compra/editar/<int:pk>/', CompraUpdateView.as_view(), name='compra_update'),
    path('compra/eliminar/<int:pk>/', CompraDeleteView.as_view(), name='compra_delete'),
]
```

## 8. PLANTILLA - Interfaz de Usuario

### 8.1 Estructura Base

```django
{% extends 'proceso_form.html' %}
{% load static %}
{% load custom_tags %}
```

### 8.2 Estilos CSS Personalizados

```css
.tbl-fixed {
    overflow-x: scroll;
    overflow-y: scroll;
    height: fit-content;
    max-height: 60vh;
    font-size: 80%;
}

.formatted-number {
    background-color: #e7f5ff;
    border: 1px solid #0d6efd;
    font-family: monospace;
}
```

### 8.3 Estructura de Acordeones

```django
<div class="accordion" id="accordionCompra">
    <!-- Acordeón 1: Encabezado -->
    <div class="accordion-item">
        <h2 class="accordion-header">
            <button class="accordion-button">Encabezado de Compra</button>
        </h2>
        <div class="accordion-collapse collapse show">
            <!-- Formulario principal -->
        </div>
    </div>

    <!-- Acordeón 2: Detalle -->
    <div class="accordion-item">
        <h2 class="accordion-header">
            <button class="accordion-button collapsed">Detalle de la Compra</button>
        </h2>
        <div class="accordion-collapse collapse">
            <!-- Tabla de detalles con FormSet -->
        </div>
    </div>
</div>
```

### 8.4 Tabla de Detalles con FormSet

```django
<table class="detalle-form table table-striped table-hover">
    <thead class="table-primary">
        <tr>
            <th>Medida</th>
            <th>Producto</th>
            <th>Despacho</th>
            <th>Cantidad</th>
            <th>Precio</th>
            <th>Total</th>
            <th>Elim</th>
        </tr>
    </thead>
    <tbody>
        {% for formdet in formset_detalle %}
        <tr data-form-index="{{ forloop.counter0 }}">
            <!-- Campos del detalle -->
        </tr>
        {% endfor %}
    </tbody>
</table>
```

## 9. JAVASCRIPT - Interactividad

### 9.1 Funcionalidades Principales

#### Gestión de FormSet Dinámico

```javascript
// Insertar nueva fila de detalle
function agregarFilaDetalle(producto) {
    const currentIndex = formsetContainer.querySelectorAll('.table tbody tr').length;

    const newRow = `
    <tr data-form-index="${currentIndex}">
        <input type="hidden" name="detallecompra_set-${currentIndex}-id_producto" 
               value="${producto.id}">
        <td>${producto.medida}</td>
        <td>${producto.nombre}</td>
        <td><input type="text" name="detallecompra_set-${currentIndex}-despacho"></td>
        <td><input type="number" name="detallecompra_set-${currentIndex}-cantidad"></td>
        <td><input type="number" name="detallecompra_set-${currentIndex}-precio"></td>
        <td><input type="number" name="detallecompra_set-${currentIndex}-total" readonly></td>
    </tr>`;
}
```

#### Cálculo de Totales en Tiempo Real

```javascript
function actualizarTotalCompra() {
    let totalFactura = 0;

    document.querySelectorAll('.table tbody tr').forEach(row => {
        const cantidad = parseFloat(row.querySelector('[name*="-cantidad"]').value) || 0;
        const precio = parseFloat(row.querySelector('[name*="-precio"]').value) || 0;
        const total = cantidad * precio;

        // Actualizar total de línea
        row.querySelector('[name*="-total"]').value = total.toFixed(2);
        totalFactura += total;
    });

    // Actualizar total general
    document.getElementById('id_total').value = totalFactura.toFixed(2);
}
```

#### Comunicación con Backend

```javascript
// Buscar productos
document.getElementById('detalleForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const url = new URL('/ventas/buscar/producto/', window.location.origin);
    url.searchParams.append('medida', medidaProducto);
    url.searchParams.append('nombre', nombreProducto);

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Actualizar tabla de resultados
        });
});
```

## 10. FLUJO COMPLETO DE COMPRA

### 10.1 Paso a Paso del Usuario

1. **Selección de Proveedor**
   
   - Buscar en lista de proveedores
   - Validar datos fiscales

2. **Configuración de Comprobante**
   
   - Seleccionar tipo (solo con remito=True)
   - Asignar número automático
   - Definir fechas

3. **Carga de Productos**
   
   - Buscar en catálogo
   - Especificar cantidades y precios
   - Registrar números de despacho

4. **Revisión y Confirmación**
   
   - Verificación de totales
   - Validación de stock
   - Confirmación de grabación

### 10.2 Procesos Automáticos

#### Al Guardar Compra:

- **Actualización de inventario** según `mult_stock`
- **Rotación de despachos** (despacho_1 → despacho_2)
- **Auditoría** (usuario, estación, fecha)
- **Cálculo de impuestos**

#### Validaciones:

- **Depósito obligatorio**
- **Productos físicos** afectan inventario
- **Consistencia temporal** de fechas
- **Permisos de usuario** por sucursal

## 11. CONSIDERACIONES DE SEGURIDAD

### 11.1 Control de Acceso

```python
# En vistas
permission_required = f"ventas.add_compra"

# Filtrado por usuario
if not user.is_superuser:
    queryset = queryset.filter(id_sucursal=user.id_sucursal)
```

### 11.2 Protección de Datos

- **Transacciones atómicas** para consistencia
- **Validación server-side** además de client-side
- **Sanitización de inputs** mediante Django Forms

### 11.3 Auditoría Completa

- **Usuario** que realizó la acción
- **Estación** desde donde se ejecutó
- **Timestamp** exacto de la operación

Este módulo representa una implementación robusta y escalable para la gestión de compras, con especial atención a la integridad de datos, experiencia de usuario y cumplimiento de reglas de negocio.

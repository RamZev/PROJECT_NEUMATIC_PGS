# neumatic\apps\ventas\views\caja_views.py
from django.urls import reverse_lazy
from django import forms
from django.db.models import Max
from decimal import Decimal
import json

from apps.maestros.views.cruds_views_generics import *
from ..models.caja_models import Caja, CajaDetalle, CajaArqueo
from ..forms.caja_forms import CajaForm


class ConfigViews():
    # Modelo
    model = Caja
    
    # Formulario asociado al modelo
    form_class = CajaForm
    
    # Aplicación asociada al modelo
    app_label = model._meta.app_label
    
    #-- Usar esta forma cuando el modelo esté compuesto de una sola palabra: Ej. Color.
    model_string = model.__name__.lower()  # "caja"
    
    # Permisos
    permission_add = f"{app_label}.add_{model.__name__.lower()}"
    permission_change = f"{app_label}.change_{model.__name__.lower()}"
    permission_delete = f"{app_label}.delete_{model.__name__.lower()}"
    
    # Vistas del CRUD del modelo
    list_view_name = f"{model_string}_list"
    create_view_name = f"{model_string}_create"
    update_view_name = f"{model_string}_update"
    delete_view_name = f"{model_string}_delete"
    
    # Plantilla para crear o actualizar el modelo
    template_form = f"{app_label}/{model_string}_form.html"
    
    # Plantilla para confirmar eliminación de un registro
    template_delete = "base_confirm_delete.html"
    
    # Plantilla de la lista del CRUD
    template_list = f'{app_label}/maestro_list.html'
    
    # Contexto de los datos de la lista
    context_object_name = 'objetos'
    
    # Vista del home del proyecto
    home_view_name = "home"
    
    # Nombre de la url 
    success_url = reverse_lazy(list_view_name)


class DataViewList():
    search_fields = ['numero_caja', 'observacion_caja']
    
    ordering = ['-fecha_caja', '-numero_caja']
    
    paginate_by = 10
      
    table_headers = {
        'numero_caja': (1, 'Número'),
        'fecha_caja': (1, 'Fecha'),
        'id_sucursal': (1, 'Sucursal'),
        'ingresos': (1, 'Ingresos'),
        'egresos': (1, 'Egresos'),
        'saldo': (1, 'Saldo'),
        'diferencia': (1, 'Diferencia'),
        'observacion_caja': (2, 'Observaciones'),
        'caja_cerrada': (1, 'Cerrada'),
        'acciones': (2, 'Acciones'),
    }
    
    table_data = [
        {'field_name': 'numero_caja', 'date_format': None},
        {'field_name': 'fecha_caja', 'date_format': 'd/m/Y'},
        {'field_name': 'id_sucursal', 'date_format': None},
        {'field_name': 'ingresos', 'date_format': None},
        {'field_name': 'egresos', 'date_format': None},
        {'field_name': 'saldo', 'date_format': None},
        {'field_name': 'diferencia', 'date_format': None},
        {'field_name': 'observacion_caja', 'date_format': None},
        {'field_name': 'caja_cerrada', 'date_format': None},
    ]


# CajaListView - Inicio
class CajaListView(MaestroListView):
    model = ConfigViews.model
    template_name = ConfigViews.template_list
    context_object_name = ConfigViews.context_object_name
    
    search_fields = DataViewList.search_fields
    ordering = DataViewList.ordering
    paginate_by = DataViewList.paginate_by
    
    extra_context = {
        "master_title": ConfigViews.model._meta.verbose_name_plural,
        "home_view_name": ConfigViews.home_view_name,
        "list_view_name": ConfigViews.list_view_name,
        "create_view_name": ConfigViews.create_view_name,
        "update_view_name": ConfigViews.update_view_name,
        "delete_view_name": ConfigViews.delete_view_name,
        "table_headers": DataViewList.table_headers,
        "table_data": DataViewList.table_data,
        "model_string": ConfigViews.model_string,
    }


# CajaCreateView - Inicio
# neumatic\apps\ventas\views\caja_views.py
# CajaCreateView - con cálculo de saldoanterior visible al usuario
class CajaCreateView(MaestroCreateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url
    
    permission_required = ConfigViews.permission_add

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # DEBUG PUNTO 1
        print(f"[DEBUG] get_context_data - Usuario: {user.username}, Sucursal: {user.id_sucursal}")
        
        ultima_caja_cerrada = None
        saldo_anterior_calculado = 0
        
        if user.id_sucursal:
            caja_abierta = Caja.objects.filter(
                id_sucursal=user.id_sucursal,
                caja_cerrada=False
            ).exists()
            context['caja_abierta'] = caja_abierta
            print(f"[DEBUG] get_context_data - Caja abierta existe: {caja_abierta}")
            
            ultima_caja_cerrada = Caja.objects.filter(
                id_sucursal=user.id_sucursal,
                caja_cerrada=True
            ).order_by('-fecha_caja', '-id_caja').first()
            
            if ultima_caja_cerrada:
                saldo_anterior_calculado = ultima_caja_cerrada.saldo
                print(f"[DEBUG] get_context_data - Última caja cerrada ID: {ultima_caja_cerrada.id_caja}")
        
        context['user'] = user
        context['ultima_caja_cerrada'] = ultima_caja_cerrada
        context['saldo_anterior_calculado'] = saldo_anterior_calculado
        
        return context

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        
        # DEBUG PUNTO 2
        print(f"[DEBUG] dispatch - Usuario: {user.username}, Sucursal: {user.id_sucursal}")
        
        if not user.id_sucursal:
            print(f"[DEBUG] dispatch - ERROR: Usuario sin sucursal")
            messages.error(
                request,
                'No tiene una sucursal asignada. Contacte al administrador.'
            )
            return redirect(self.list_view_name)
        
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        
        # DEBUG PUNTO 3
        print(f"[DEBUG] get_initial - Usuario: {user.username}")
        
        if user.id_sucursal:
            initial['id_sucursal'] = user.id_sucursal
            initial['nombre_sucursal'] = user.id_sucursal.nombre_sucursal
            print(f"[DEBUG] get_initial - Sucursal asignada: {user.id_sucursal.nombre_sucursal}")
            
            ultima_caja_cerrada = Caja.objects.filter(
                id_sucursal=user.id_sucursal,
                caja_cerrada=True
            ).order_by('-fecha_caja', '-id_caja').first()
            
            if ultima_caja_cerrada:
                initial['saldoanterior'] = ultima_caja_cerrada.saldo
                print(f"[DEBUG] get_initial - Saldo anterior: {ultima_caja_cerrada.saldo}")
            else:
                initial['saldoanterior'] = 0
                print(f"[DEBUG] get_initial - Sin caja cerrada previa, saldo = 0")
        
        fecha_actual = timezone.now().date()
        initial['fecha_caja'] = fecha_actual.strftime('%Y-%m-%d')
        initial['caja_cerrada'] = False
        
        print(f"[DEBUG] get_initial - Initial final: {initial}")
        
        return initial
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        
        if user.id_sucursal:
            form.fields['id_sucursal'].queryset = Caja._meta.get_field('id_sucursal').related_model.objects.filter(
                id_sucursal=user.id_sucursal.id_sucursal
            )
            # DEBUG PUNTO 4
            print(f"[DEBUG] get_form - Queryset de sucursal filtrado para ID: {user.id_sucursal.id_sucursal}")
        
        return form
    
    def generar_numero_caja(self, sucursal):
        # DEBUG PUNTO 5
        print(f"[DEBUG] generar_numero_caja - Sucursal ID: {sucursal.id_sucursal if sucursal else 'None'}")
        
        if not sucursal:
            raise forms.ValidationError('Debe proporcionar una sucursal para generar el número de caja')
        
        sucursal_id = sucursal.id_sucursal
        
        if sucursal_id > 99:
            raise forms.ValidationError('El ID de sucursal debe ser de máximo 2 dígitos')
        
        sucursal_str = f"{sucursal_id:02d}"
        rango_min = sucursal_id * 1000000
        rango_max = (sucursal_id + 1) * 1000000 - 1
        
        ultimo = Caja.objects.filter(
            numero_caja__gte=rango_min,
            numero_caja__lte=rango_max
        ).aggregate(Max('numero_caja'))
        
        print(f"[DEBUG] generar_numero_caja - Último número encontrado: {ultimo['numero_caja__max']}")
        
        if ultimo['numero_caja__max']:
            correlativo_actual = ultimo['numero_caja__max'] % 1000000
            nuevo_correlativo = correlativo_actual + 1
        else:
            nuevo_correlativo = 1
        
        correlativo_str = f"{nuevo_correlativo:06d}"
        numero_generado = int(f"{sucursal_str}{correlativo_str}")
        
        print(f"[DEBUG] generar_numero_caja - Número generado: {numero_generado}")
        
        return numero_generado
    
    @transaction.atomic
    def form_valid(self, form):
        # DEBUG PUNTO 6 - INICIO DEL MÉTODO
        print("\n" + "="*60)
        print("[DEBUG] form_valid - INICIO")
        print(f"[DEBUG] form_valid - Usuario: {self.request.user.username}")
        print(f"[DEBUG] form_valid - POST data: {self.request.POST}")
        print(f"[DEBUG] form_valid - cleaned_data: {form.cleaned_data}")
        print("="*60)
        
        user = self.request.user
        
        # 1. Validar que el usuario tenga sucursal
        sucursal = user.id_sucursal
        print(f"[DEBUG] form_valid - Sucursal obtenida: {sucursal}")
        
        if not sucursal:
            print("[DEBUG] form_valid - ERROR: No tiene sucursal")
            form.add_error(None, 'No tiene una sucursal asignada')
            return self.form_invalid(form)
        
        # 2. Validar que no haya caja abierta en la sucursal
        caja_abierta = Caja.objects.filter(
            id_sucursal=sucursal,
            caja_cerrada=False
        ).select_for_update().exists()
        
        print(f"[DEBUG] form_valid - Caja abierta existe: {caja_abierta}")
        
        if caja_abierta:
            print("[DEBUG] form_valid - ERROR: Ya existe caja abierta")
            form.add_error(
                None,
                f'Existe una caja abierta en la sucursal {sucursal.nombre_sucursal}. '
                f'Debe cerrarla antes de crear una nueva.'
            )
            return self.form_invalid(form)
        
        # 3. Validaciones de fecha
        fecha_caja = form.cleaned_data.get('fecha_caja')
        print(f"[DEBUG] form_valid - Fecha de caja: {fecha_caja}")
        
        caja_misma_fecha = Caja.objects.filter(
            id_sucursal=sucursal,
            fecha_caja=fecha_caja
        ).exists()
        
        print(f"[DEBUG] form_valid - Existe caja misma fecha: {caja_misma_fecha}")
        
        if caja_misma_fecha:
            print("[DEBUG] form_valid - ERROR: Misma fecha ya existe")
            form.add_error(
                'fecha_caja',
                f'Ya existe una caja para la fecha {fecha_caja.strftime("%d/%m/%Y")} en esta sucursal.'
            )
            return self.form_invalid(form)
        
        ultima_caja = Caja.objects.filter(
            id_sucursal=sucursal
        ).order_by('-fecha_caja', '-id_caja').first()
        
        if ultima_caja and fecha_caja < ultima_caja.fecha_caja:
            print(f"[DEBUG] form_valid - ERROR: Fecha anterior a última caja ({ultima_caja.fecha_caja})")
            form.add_error(
                'fecha_caja',
                f'La fecha no puede ser anterior a la última caja ({ultima_caja.fecha_caja.strftime("%d/%m/%Y")}).'
            )
            return self.form_invalid(form)
        
        if fecha_caja and fecha_caja > timezone.now().date():
            print(f"[DEBUG] form_valid - ERROR: Fecha futura ({fecha_caja})")
            form.add_error('fecha_caja', 'La fecha de la caja no puede ser futura.')
            return self.form_invalid(form)
        
        # 4. FORZAR valores críticos
        form.instance.id_sucursal = sucursal
        form.instance.caja_cerrada = False
        print(f"[DEBUG] form_valid - Instance sucursal asignada: {form.instance.id_sucursal}")
        
        # 5. Generar número de caja
        try:
            numero_generado = self.generar_numero_caja(sucursal)
            form.instance.numero_caja = numero_generado
            print(f"[DEBUG] form_valid - Número generado y asignado: {numero_generado}")
        except forms.ValidationError as e:
            print(f"[DEBUG] form_valid - ERROR generando número: {e}")
            form.add_error('numero_caja', str(e))
            return self.form_invalid(form)
        
        # 6. Calcular saldo anterior
        ultima_caja_cerrada = Caja.objects.filter(
            id_sucursal=sucursal,
            caja_cerrada=True
        ).order_by('-fecha_caja', '-id_caja').first()
        
        if ultima_caja_cerrada:
            form.instance.saldoanterior = ultima_caja_cerrada.saldo
            print(f"[DEBUG] form_valid - Saldo anterior desde última cerrada: {ultima_caja_cerrada.saldo}")
        else:
            form.instance.saldoanterior = 0
            print(f"[DEBUG] form_valid - Sin caja cerrada previa, saldo anterior = 0")
        
        # 7. Inicializar otros campos
        form.instance.ingresos = 0
        form.instance.egresos = 0
        form.instance.saldo = form.instance.saldoanterior
        form.instance.diferencia = 0
        form.instance.recuento = 0
        
        print(f"[DEBUG] form_valid - Campos inicializados: ingresos=0, egresos=0, saldo={form.instance.saldoanterior}, diferencia=0")
        
        # 8. GUARDAR
        try:
            print("[DEBUG] form_valid - Intentando guardar...")
            self.object = form.save()
            print(f"[DEBUG] form_valid - ✅ GUARDADO EXITOSO! ID: {self.object.id_caja}, Número: {self.object.numero_caja}")
            
            messages.success(
                self.request,
                f'Caja #{self.object.numero_caja} creada exitosamente. '
                f'Saldo inicial: ${self.object.saldoanterior:.2f}'
            )
            
            print("[DEBUG] form_valid - Redirigiendo a success_url")
            return redirect(self.success_url)
            
        except Exception as e:
            print(f"[DEBUG] form_valid - ❌ ERROR AL GUARDAR: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()  # Esto imprime el traceback completo
            form.add_error(None, f'Error al guardar en la base de datos: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        # DEBUG PUNTO 7
        print("\n" + "="*60)
        print("[DEBUG] form_invalid - FORMULARIO INVÁLIDO")
        print(f"[DEBUG] form_invalid - Errores del formulario: {form.errors}")
        print(f"[DEBUG] form_invalid - Non-field errors: {form.non_field_errors()}")
        print("="*60 + "\n")
        
        if form.non_field_errors():
            for error in form.non_field_errors():
                messages.error(self.request, error)
        
        return super().form_invalid(form)

# En neumatic\apps\ventas\views\caja_views.py
# En neumatic\apps\ventas\views\caja_views.py
class CajaUpdateView(MaestroUpdateView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    form_class = ConfigViews.form_class
    template_name = ConfigViews.template_form
    success_url = ConfigViews.success_url
    permission_required = ConfigViews.permission_change
    
    def dispatch(self, request, *args, **kwargs):
        """Validar antes de mostrar el formulario"""
        self.object = self.get_object()
        
        if self.object.caja_cerrada:
            messages.error(
                request,
                f'No se puede modificar la caja #{self.object.numero_caja} porque está cerrada.'
            )
            return redirect(self.list_view_name)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        """Sobreescribir get_initial para asignar valores calculados"""
        initial = super().get_initial()
        
        # Solo para cajas abiertas
        if not self.object.caja_cerrada:
            # Calcular totales desde CajaDetalle
            detalles = CajaDetalle.objects.filter(id_caja=self.object)
            
            total_ingresos = sum(
                detalle.importe for detalle in detalles 
                if detalle.tipo_movimiento == 1  # Ingreso
            )
            
            total_egresos = sum(
                detalle.importe for detalle in detalles 
                if detalle.tipo_movimiento == 2  # Egreso
            )
            
            # Asignar valores calculados a los campos del formulario
            initial['ingresos'] = total_ingresos
            initial['egresos'] = total_egresos
            
            # Calcular diferencia según la fórmula: 
            # diferencia = saldoanterior + ingresos - (egresos + recuento)
            recuento = self.object.recuento or 0
            diferencia = self.object.saldoanterior + total_ingresos - (total_egresos + recuento)
            initial['diferencia'] = diferencia
            
            # El saldo siempre será 0 porque la diferencia ya incluye todo
            initial['saldo'] = 0
        
        return initial
    
    def get_context_data(self, **kwargs):
        """Agregar información adicional al contexto"""
        context = super().get_context_data(**kwargs)
        
        # Obtener los detalles de caja para mostrar información
        detalles = CajaDetalle.objects.filter(id_caja=self.object)
        
        # Calcular totales a partir de los detalles
        total_ingresos = sum(
            detalle.importe for detalle in detalles 
            if detalle.tipo_movimiento == 1  # Ingreso
        )
        
        total_egresos = sum(
            detalle.importe for detalle in detalles 
            if detalle.tipo_movimiento == 2  # Egreso
        )
        
        # Calcular diferencia según la nueva fórmula
        recuento = self.object.recuento or 0
        diferencia_calculada = self.object.saldoanterior + total_ingresos - (total_egresos + recuento)
        
        # Agregar al contexto para mostrar en template
        context['detalles_caja'] = detalles
        context['total_detalles'] = detalles.count()
        context['total_ingresos_calculado'] = total_ingresos
        context['total_egresos_calculado'] = total_egresos
        context['diferencia_calculada'] = diferencia_calculada
        
        # Agregar fórmula para mostrar en template
        context['formula_diferencia'] = (
            f"${self.object.saldoanterior:.2f} + ${total_ingresos:.2f} - "
            f"(${total_egresos:.2f} + ${recuento:.2f}) = ${diferencia_calculada:.2f}"
        )
        
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        """
        Control de grabación para edición - CIERRE DE CAJA
        """
        caja = self.get_object()
        
        # Calcular totales desde los detalles
        detalles = CajaDetalle.objects.filter(id_caja=caja)
        
        total_ingresos = sum(
            detalle.importe for detalle in detalles 
            if detalle.tipo_movimiento == 1  # Ingreso
        )
        
        total_egresos = sum(
            detalle.importe for detalle in detalles 
            if detalle.tipo_movimiento == 2  # Egreso
        )
        
        # FORZAR valores calculados desde detalles
        form.instance.ingresos = total_ingresos
        form.instance.egresos = total_egresos
        
        # Si el usuario marca "cerrada", realizar validaciones adicionales
        if form.cleaned_data.get('caja_cerrada'):
            # 1. Validar que se haya ingresado el recuento
            recuento = form.cleaned_data.get('recuento') or 0
            if not recuento or recuento <= 0:
                messages.error(
                    self.request,
                    'Error: Debe ingresar el recuento físico para cerrar la caja.'
                )
                return self.form_invalid(form)
            
            # 2. Calcular diferencia según la nueva fórmula
            form.instance.diferencia = (
                form.instance.saldoanterior + 
                total_ingresos - 
                (total_egresos + recuento)
            )
            
            # 3. Saldo siempre será 0 al cerrar
            form.instance.saldo = 0
            
            # 4. Asignar fecha/hora actual
            form.instance.hora_cierre = timezone.now()
            
            # 5. Asignar usuario actual
            form.instance.id_usercierre = self.request.user
            
            ##################################################
            # 6. GUARDAR RECUENTO DEL MODAL (NUEVO - LO IMPORTANTE)
            recuento_data_json = self.request.POST.get('recuento_data')
            if recuento_data_json:
                try:
                    # Parsear JSON
                    recuento_data = json.loads(recuento_data_json)
                    
                    # Eliminar arqueos anteriores de esta caja
                    CajaArqueo.objects.filter(id_caja=caja).delete()
                    
                    # Guardar cada denominación
                    for item in recuento_data:
                        cantidad = Decimal(str(item.get('cantidad', 0)))
                        if cantidad > 0:  # Solo guardar si hay cantidad
                            CajaArqueo.objects.create(
                                id_caja=caja,
                                cantidad=cantidad,
                                valor=Decimal(str(item.get('valor', 0))),
                                detalle=item.get('detalle', ''),
                                total=Decimal(str(item.get('total', 0)))
                            )
                            
                except Exception as e:
                    # Si falla el recuento detallado, igual se cierra la caja
                    # pero mostramos advertencia
                    messages.warning(
                        self.request,
                        f'Caja cerrada pero el recuento detallado no se guardó: {str(e)}'
                    )
            
            ##################################################
            

            messages.info(
                self.request,
                f'✅ *Caja #{caja.numero_caja} cerrada. '
                f'Ingresos: ${total_ingresos:.2f}, '
                f'Egresos: ${total_egresos:.2f}, '
                f'Diferencia: ${form.instance.diferencia:+.2f}'
            )
        
        # Llamar al padre para guardar
        return super().form_valid(form)

# CajaDeleteView
class CajaDeleteView(MaestroDeleteView):
    model = ConfigViews.model
    list_view_name = ConfigViews.list_view_name
    template_name = ConfigViews.template_delete
    success_url = ConfigViews.success_url
    
    #-- Indicar el permiso que requiere para ejecutar la acción.
    permission_required = ConfigViews.permission_delete
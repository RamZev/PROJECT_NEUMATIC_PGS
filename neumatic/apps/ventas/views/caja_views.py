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
        """Agregar contexto adicional a la plantilla"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Información sobre caja anterior
        ultima_caja_cerrada = None
        saldo_anterior_calculado = 0
        
        if user.id_sucursal:
            # Verificar si hay caja abierta
            caja_abierta = Caja.objects.filter(
                id_sucursal=user.id_sucursal,
                caja_cerrada=False
            ).exists()
            context['caja_abierta'] = caja_abierta
            
            # Buscar última caja cerrada para mostrar información
            ultima_caja_cerrada = Caja.objects.filter(
                id_sucursal=user.id_sucursal,
                caja_cerrada=True
            ).order_by('-fecha_caja', '-id_caja').first()
            
            if ultima_caja_cerrada:
                saldo_anterior_calculado = ultima_caja_cerrada.saldo
        
        context['user'] = user
        context['ultima_caja_cerrada'] = ultima_caja_cerrada
        context['saldo_anterior_calculado'] = saldo_anterior_calculado
        
        return context

    def dispatch(self, request, *args, **kwargs):
        """Interceptar la solicitud antes de mostrar el formulario"""
        user = request.user
        
        # TODOS los usuarios deben tener sucursal asignada
        if not user.id_sucursal:
            messages.error(
                request,
                'No tiene una sucursal asignada. Contacte al administrador.'
            )
            return redirect(self.list_view_name)
        
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """Valores iniciales para el formulario"""
        initial = super().get_initial()
        user = self.request.user
        
        if user.id_sucursal:
            initial['id_sucursal'] = user.id_sucursal
            initial['nombre_sucursal'] = user.id_sucursal.nombre_sucursal
            
            # Calcular saldoanterior basado en última caja cerrada
            ultima_caja_cerrada = Caja.objects.filter(
                id_sucursal=user.id_sucursal,
                caja_cerrada=True
            ).order_by('-fecha_caja', '-id_caja').first()
            
            if ultima_caja_cerrada:
                initial['saldoanterior'] = ultima_caja_cerrada.saldo
            else:
                initial['saldoanterior'] = 0
        
        # Establecer fecha actual por defecto
        fecha_actual = timezone.now().date()
        initial['fecha_caja'] = fecha_actual.strftime('%Y-%m-%d')
        
        # Para nuevas cajas, caja_cerrada debe ser False
        initial['caja_cerrada'] = False
        
        return initial
    
    def get_form(self, form_class=None):
        """Configurar el formulario"""
        form = super().get_form(form_class)
        user = self.request.user
        
        # Solo necesitamos limitar el queryset de id_sucursal
        if user.id_sucursal:
            form.fields['id_sucursal'].queryset = Caja._meta.get_field('id_sucursal').related_model.objects.filter(
                id_sucursal=user.id_sucursal.id_sucursal
            )
        
        return form
    
    def generar_numero_caja(self, sucursal):
        """
        GENERAR EL NÚMERO DE CAJA EN LA VISTA
        Lógica completa de generación
        """
        if not sucursal:
            raise forms.ValidationError('Debe proporcionar una sucursal para generar el número de caja')
        
        sucursal_id = sucursal.id_sucursal
        
        # Validar que id_sucursal tenga máximo 2 dígitos
        if sucursal_id > 99:
            raise forms.ValidationError('El ID de sucursal debe ser de máximo 2 dígitos')
        
        # Formatear id_sucursal a 2 dígitos
        sucursal_str = f"{sucursal_id:02d}"
        
        # Buscar el último numero_caja para esta sucursal
        rango_min = sucursal_id * 1000000
        rango_max = (sucursal_id + 1) * 1000000 - 1
        
        ultimo = Caja.objects.filter(
            numero_caja__gte=rango_min,
            numero_caja__lte=rango_max
        ).aggregate(Max('numero_caja'))
        
        if ultimo['numero_caja__max']:
            # Extraer correlativo actual
            correlativo_actual = ultimo['numero_caja__max'] % 1000000
            nuevo_correlativo = correlativo_actual + 1
        else:
            # Primera caja de esta sucursal
            nuevo_correlativo = 1
        
        # Formatear correlativo a 6 dígitos y combinar
        correlativo_str = f"{nuevo_correlativo:06d}"
        return int(f"{sucursal_str}{correlativo_str}")
    
    @transaction.atomic
    def form_valid(self, form):
        """
        CONTROL COMPLETO DE LA GRABACIÓN EN LA VISTA
        """
        user = self.request.user
        
        # 1. Validar que el usuario tenga sucursal
        sucursal = user.id_sucursal
        if not sucursal:
            form.add_error(None, 'No tiene una sucursal asignada')
            return self.form_invalid(form)
        
        # 2. Validar que no haya caja abierta en la sucursal
        caja_abierta = Caja.objects.filter(
            id_sucursal=sucursal,
            caja_cerrada=False
        ).select_for_update().exists()
        
        if caja_abierta:
            messages.error(
                self.request,
                f'Existe una caja abierta en la sucursal {sucursal.nombre_sucursal}. '
                f'Debe cerrarla antes de crear una nueva.'
            )
            return redirect(self.list_view_name)
        
        # ===== NUEVAS VALIDACIONES DE FECHA =====
        fecha_caja = form.cleaned_data.get('fecha_caja')
        
        # 3. Validar que no exista caja en la misma fecha para esta sucursal
        caja_misma_fecha = Caja.objects.filter(
            id_sucursal=sucursal,
            fecha_caja=fecha_caja
        ).exists()
        
        if caja_misma_fecha:
            messages.error(
                self.request,
                f'Ya existe una caja para la fecha {fecha_caja.strftime("%d/%m/%Y")} en la sucursal {sucursal.nombre_sucursal}.'
            )
            return redirect(self.list_view_name)
        
        # 4. Validar que la fecha no sea anterior a la última caja creada
        ultima_caja = Caja.objects.filter(
            id_sucursal=sucursal
        ).order_by('-fecha_caja', '-id_caja').first()
        
        if ultima_caja and fecha_caja < ultima_caja.fecha_caja:
            messages.error(
                self.request,
                f'La fecha de la nueva caja ({fecha_caja.strftime("%d/%m/%Y")}) no puede ser anterior '
                f'a la última caja creada ({ultima_caja.fecha_caja.strftime("%d/%m/%Y")}) en la sucursal {sucursal.nombre_sucursal}.'
            )
            return redirect(self.list_view_name)
        
        # 5. Validar fecha no puede ser futura
        if fecha_caja and fecha_caja > timezone.now().date():
            messages.error(
                self.request,
                f'La fecha de la caja ({fecha_caja.strftime("%d/%m/%Y")}) no puede ser futura.'
            )
            return redirect(self.list_view_name)
        # ===== FIN DE NUEVAS VALIDACIONES =====
        
        # 6. FORZAR valores críticos
        form.instance.id_sucursal = sucursal
        form.instance.caja_cerrada = False
        
        # 7. GENERAR NÚMERO DE CAJA
        try:
            numero_generado = self.generar_numero_caja(sucursal)
            form.instance.numero_caja = numero_generado
        except forms.ValidationError as e:
            messages.error(self.request, str(e))
            return redirect(self.list_view_name)
        
        # 8. CALCULAR SALDO ANTERIOR
        ultima_caja_cerrada = Caja.objects.filter(
            id_sucursal=sucursal,
            caja_cerrada=True
        ).order_by('-fecha_caja', '-id_caja').first()
        
        if ultima_caja_cerrada:
            form.instance.saldoanterior = ultima_caja_cerrada.saldo
        else:
            form.instance.saldoanterior = 0
        
        # 9. INICIALIZAR OTROS CAMPOS
        form.instance.ingresos = 0
        form.instance.egresos = 0
        form.instance.saldo = form.instance.saldoanterior
        form.instance.diferencia = 0
        form.instance.recuento = 0
        
        # 10. GUARDAR
        try:
            self.object = form.save()
            
            # messages.success(
            #     self.request,
            #     f'Caja #{self.object.numero_caja} creada exitosamente. '
            #     f'Saldo inicial: ${self.object.saldoanterior:.2f}',
            #     extra_tags='success'
            # )
            
            return redirect(self.success_url)
            
        except Exception as e:
            messages.error(self.request, f'Error al guardar la caja: {str(e)}')
            return redirect(self.list_view_name)

        # def form_valid(self, form):
        #     """
        #     CONTROL COMPLETO DE LA GRABACIÓN EN LA VISTA
        #     """
        #     user = self.request.user
            
        #     # 1. Validar que el usuario tenga sucursal
        #     sucursal = user.id_sucursal
        #     if not sucursal:
        #         form.add_error(None, 'No tiene una sucursal asignada')
        #         return self.form_invalid(form)
            
        #     # 2. Validar que no haya caja abierta en la sucursal
        #     caja_abierta = Caja.objects.filter(
        #         id_sucursal=sucursal,
        #         caja_cerrada=False
        #     ).select_for_update().exists()  # Bloquear para evitar concurrencia
            
        #     if caja_abierta:
        #         form.add_error(
        #             None,
        #             f'Existe una caja abierta en la sucursal {sucursal.nombre_sucursal}. '
        #             f'Debe cerrarla antes de crear una nueva.'
        #         )
        #         return self.form_invalid(form)
            
        #     # 3. FORZAR valores críticos
        #     form.instance.id_sucursal = sucursal
        #     form.instance.caja_cerrada = False  # Nueva caja siempre abierta
            
        #     # 4. GENERAR NÚMERO DE CAJA
        #     try:
        #         numero_generado = self.generar_numero_caja(sucursal)
        #         form.instance.numero_caja = numero_generado
        #     except forms.ValidationError as e:
        #         form.add_error('numero_caja', str(e))
        #         return self.form_invalid(form)
            
        #     # 5. CALCULAR SALDO ANTERIOR
        #     ultima_caja_cerrada = Caja.objects.filter(
        #         id_sucursal=sucursal,
        #         caja_cerrada=True
        #     ).order_by('-fecha_caja', '-id_caja').first()
            
        #     if ultima_caja_cerrada:
        #         form.instance.saldoanterior = ultima_caja_cerrada.saldo
        #     else:
        #         form.instance.saldoanterior = 0
            
        #     # 6. INICIALIZAR OTROS CAMPOS
        #     form.instance.ingresos = 0
        #     form.instance.egresos = 0
        #     form.instance.saldo = form.instance.saldoanterior
        #     form.instance.diferencia = 0
        #     form.instance.recuento = 0
            
        #     # 7. VALIDAR FECHA (no puede ser futura)
        #     fecha_caja = form.cleaned_data.get('fecha_caja')
        #     if fecha_caja and fecha_caja > timezone.now().date():
        #         form.add_error('fecha_caja', 'La fecha de la caja no puede ser futura')
        #         return self.form_invalid(form)
            
        #     # 8. GUARDAR
        #     try:
        #         # Llamar al padre para guardar
        #         # response = super().form_valid(form)
        #         self.object = form.save()
                
        #         # Mensaje de éxito
        #         # messages.success(
        #         #     self.request,
        #         #     f'Caja #{self.object.numero_caja} creada exitosamente. '
        #         #     f'Saldo inicial: ${self.object.saldoanterior:.2f}',
        #         #     extra_tags='success'  # Forzar la etiqueta
        #         # )
                
        #         # return response
        #         return redirect(self.success_url)
                
        #     except Exception as e:
        #         # Manejar cualquier error durante el guardado
        #         form.add_error(None, f'Error al guardar la caja: {str(e)}')
        #         return self.form_invalid(form)


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
# neumatic/apps/datatools/views/padron_entrerios_views.py
import io
import csv
from datetime import datetime
from decimal import Decimal
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connection, transaction
from django.http import JsonResponse
from django.core.cache import cache

from apps.maestros.models.padron_models import PadronEntreRiosIIBB
from apps.datatools.forms.padron_entrerios_forms import PadronEntreRiosUploadForm

LOTE = 5000 

class PadronEntreRiosUploadView(FormView):
    template_name = 'datatools/padron_entrerios_upload.html'
    form_class = PadronEntreRiosUploadForm
    success_url = reverse_lazy('padron_entrerios_upload')

    def form_valid(self, form):
        archivo = self.request.FILES['archivo_csv']
        
        if not archivo.name.endswith('.csv'):
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'El archivo debe tener extensión .csv'})
            messages.error(self.request, "El archivo debe tener extensión .csv")
            return self.form_invalid(form)

        total_procesados = 0
        errores = 0

        try:
            file_data = io.TextIOWrapper(archivo.file, encoding='latin-1')
            
            # 1. Contar total de líneas para calcular el porcentaje exacto
            total_lineas = sum(1 for _ in file_data)
            file_data.seek(0)
            total_lineas = max(1, total_lineas - 1) # Restamos el encabezado, evitando división por cero

            reader = csv.reader(file_data, delimiter=';')
            next(reader, None) # Saltar encabezado

            # Inicializar progreso en caché
            cache.set('padron_er_progreso', 0)

            with transaction.atomic():
                PadronEntreRiosIIBB.objects.all().delete()
                
                lote = []
                for row in reader:
                    if len(row) < 12:
                        errores += 1
                        continue
                    
                    try:
                        fecha_publicacion = datetime.strptime(row[0].strip().zfill(8), '%d%m%Y').date()
                        fecha_vigencia_desde = datetime.strptime(row[1].strip().zfill(8), '%d%m%Y').date()
                        fecha_vigencia_hasta = datetime.strptime(row[2].strip().zfill(8), '%d%m%Y').date()
                        
                        cuit = int(row[3].strip())
                        tipo_contr = row[4].strip() if row[4].strip() in ('D', 'C') else None
                        marca_alta = row[5].strip().upper() == 'S'
                        marca_alicuota = row[6].strip().upper() == 'S'
                        
                        alicuota_percepcion = Decimal(row[7].replace(',', '.')) if row[7] else Decimal('0.00')
                        alicuota_retencion = Decimal(row[8].replace(',', '.')) if row[8] else Decimal('0.00')
                        
                        nro_grupo_percepcion = row[9].strip() or '0'
                        nro_grupo_retencion = row[10].strip() or '0'
                        razon_social = row[11].strip()[:100]

                        lote.append(
                            PadronEntreRiosIIBB(
                                fecha_publicacion=fecha_publicacion,
                                fecha_vigencia_desde=fecha_vigencia_desde,
                                fecha_vigencia_hasta=fecha_vigencia_hasta,
                                cuit=cuit,
                                tipo_contr_insc=tipo_contr,
                                marca_alta_sujeto=marca_alta,
                                marca_alicuota=marca_alicuota,
                                alicuota_percepcion=alicuota_percepcion,
                                alicuota_retencion=alicuota_retencion,
                                nro_grupo_percepcion=nro_grupo_percepcion,
                                nro_grupo_retencion=nro_grupo_retencion,
                                razon_social=razon_social
                            )
                        )
                        total_procesados += 1
                    except Exception as e:
                        errores += 1
                        continue

                    if len(lote) >= LOTE:
                        PadronEntreRiosIIBB.objects.bulk_create(lote)
                        lote = []
                        
                        # 2. Actualizar el progreso en caché cada 5000 registros
                        progreso = int((total_procesados / total_lineas) * 100)
                        cache.set('padron_er_progreso', progreso)

                if lote:
                    PadronEntreRiosIIBB.objects.bulk_create(lote)

                # Resetear secuencia
                if 'postgresql' in connection.vendor:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT setval(pg_get_serial_sequence('padron_entre_rios', 'id_padron'), (SELECT COALESCE(MAX(id_padron), 1) FROM padron_entre_rios), true);")

            # Marcar como completado
            cache.set('padron_er_progreso', 100)
            
            mensaje_exito = f"✅ Migración de Entre Ríos completada. Procesados: {total_procesados}. Omitidos: {errores}."
            messages.success(self.request, mensaje_exito)

            # Si es AJAX, devolvemos JSON
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': mensaje_exito})
                
            return super().form_valid(form)

        except Exception as e:
            cache.set('padron_er_progreso', 0)
            mensaje_error = f"❌ Error crítico al procesar el archivo: {str(e)}"
            messages.error(self.request, mensaje_error)
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': mensaje_error})
                
            return self.form_invalid(form)

# 👇 NUEVA VISTA: Para consultar el progreso
class PadronEntreRiosProgressView(View):
    def get(self, request, *args, **kwargs):
        progreso = cache.get('padron_er_progreso', 0)
        return JsonResponse({'progreso': progreso})
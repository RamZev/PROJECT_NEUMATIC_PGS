# neumatic/apps/datatools/views/padron_santafe_views.py
import io
import csv
from datetime import datetime
from decimal import Decimal
from collections import Counter # 👈 NUEVO IMPORT
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connection, transaction
from django.http import JsonResponse
from django.core.cache import cache

from apps.maestros.models.padron_models import PadronSantaFeIIBB
from apps.datatools.forms.padron_santafe_forms import PadronSantaFeUploadForm

LOTE = 5000 

class PadronSantaFeUploadView(FormView):
    template_name = 'datatools/padron_santafe_upload.html'
    form_class = PadronSantaFeUploadForm
    success_url = reverse_lazy('padron_santafe_upload')

    def form_valid(self, form):
        archivo = self.request.FILES['archivo_csv']
        
        if not archivo.name.endswith('.csv'):
            return self._error_response("El archivo debe tener extensión .csv", form)

        try:
            file_data = io.TextIOWrapper(archivo.file, encoding='latin-1')
            
            # 1. Contar total de líneas
            total_lineas = sum(1 for _ in file_data)
            file_data.seek(0)
            total_lineas = max(1, total_lineas) 

            # 👇 2. PRE-VALIDACIÓN: DETECTAR DUPLICADOS DE CUIT
            reader_check = csv.reader(file_data, delimiter=';')
            cuits = []
            for row in reader_check:
                if len(row) >= 4:
                    cuit_raw = row[3].strip()
                    if cuit_raw:
                        cuits.append(cuit_raw)
            
            contador_cuits = Counter(cuits)
            duplicados = {cuit: cant for cuit, cant in contador_cuits.items() if cant > 1}
            
            if duplicados:
                # Formatear un mensaje con los primeros 15 duplicados encontrados
                lista_dup = [f"CUIT {k} (x{v})" for k, v in list(duplicados.items())[:15]]
                mensaje = (
                    f"❌ Se encontraron {len(duplicados)} CUITs duplicados en el archivo. "
                    f"Ejemplos: {', '.join(lista_dup)}. "
                    f"Corrija el archivo antes de migrar."
                )
                return self._error_response(mensaje, form)

            # 3. Si no hay duplicados, reiniciamos el puntero del archivo para procesar
            file_data.seek(0)
            reader = csv.reader(file_data, delimiter=';')
            
            total_procesados = 0
            errores = 0

            cache.set('padron_sf_progreso', 0)

            with transaction.atomic():
                PadronSantaFeIIBB.objects.all().delete()
                
                lote = []
                for row in reader:
                    if len(row) < 12:
                        errores += 1
                        continue
                    
                    try:
                        # ... (tu código de transformación de fechas y decimales igual) ...
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
                            PadronSantaFeIIBB(
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
                        PadronSantaFeIIBB.objects.bulk_create(lote)
                        lote = []
                        
                        progreso = int((total_procesados / total_lineas) * 100)
                        cache.set('padron_sf_progreso', progreso)

                if lote:
                    PadronSantaFeIIBB.objects.bulk_create(lote)

                if 'postgresql' in connection.vendor:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT setval(pg_get_serial_sequence('padron_santa_fe', 'id_padron'), (SELECT COALESCE(MAX(id_padron), 1) FROM padron_santa_fe), true);")

            cache.set('padron_sf_progreso', 100)
            
            mensaje_exito = f"✅ Migración de Santa Fe completada. Procesados: {total_procesados}. Omitidos: {errores}."
            messages.success(self.request, mensaje_exito)

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': mensaje_exito})
                
            return super().form_valid(form)

        except Exception as e:
            cache.set('padron_sf_progreso', 0)
            return self._error_response(f"❌ Error crítico al procesar el archivo: {str(e)}", form)

    # 👇 Función auxiliar para no repetir código de error
    def _error_response(self, mensaje, form):
        messages.error(self.request, mensaje)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': mensaje})
        return self.form_invalid(form)

class PadronSantaFeProgressView(View):
    def get(self, request, *args, **kwargs):
        progreso = cache.get('padron_sf_progreso', 0)
        return JsonResponse({'progreso': progreso})
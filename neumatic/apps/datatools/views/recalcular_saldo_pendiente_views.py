# neumatic\apps\datatools\views\recalcular_saldo_pendiente_views.py
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.maestros.models.cliente_models import Cliente
from apps.datatools.forms.recalcular_saldo_pendiente_forms import RecalcularSaldoPendienteForm
from utils.recalcular_saldo_pendiente import recalcular_saldo_pendiente_cliente


class RecalcularSaldoPendienteView(FormView):
	template_name = 'datatools/recalcular_saldo_pendiente_cargar.html'
	form_class = RecalcularSaldoPendienteForm
	success_url = reverse_lazy('datatools:recalcular_saldo_pendiente')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['titulo'] = 'Recalcular Saldo Pendiente'
		context.setdefault('mostrar_resultado', False)
		context.setdefault('transaction_error', None)
		return context
	
	def form_valid(self, form):
		id_cliente = form.cleaned_data['id_cliente']
		cliente = Cliente.objects.get(id_cliente=id_cliente)
		
		try:
			resumen = recalcular_saldo_pendiente_cliente(cliente.id_cliente)
		except Exception as e:
			context = self.get_context_data(form=form)
			context['transaction_error'] = str(e)
			return self.render_to_response(context, status=500)
		
		context = self.get_context_data(form=form)
		context.update({
			'cliente': cliente,
			'resumen': resumen,
			'mostrar_resultado': True,
		})
		return self.render_to_response(context)

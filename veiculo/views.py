from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from estada.models import Estada
from .models import Veiculo
from .forms import VeiculoForm  # importe seu form personalizado

class VeiculoListView(LoginRequiredMixin,ListView):
    model = Veiculo
    template_name = 'lista.html'
    context_object_name = 'veiculos'

class VeiculoCreateView(LoginRequiredMixin,CreateView):
    model = Veiculo
    form_class = VeiculoForm  # usa o form personalizado
    template_name = 'form.html'
    success_url = reverse_lazy('lista_veiculos')

class VeiculoUpdateView(LoginRequiredMixin,UpdateView):
    model = Veiculo
    form_class = VeiculoForm  # também aqui
    template_name = 'form.html'
    success_url = reverse_lazy('lista_veiculos')

class VeiculoDeleteView(LoginRequiredMixin,DeleteView):
    model = Veiculo
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('lista_veiculos')



from django.views.generic import DetailView
class VeiculoDetailView(LoginRequiredMixin, DetailView):
    model = Veiculo
    template_name = 'detalhe_veiculo.html'
    context_object_name = 'veiculo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        veiculo = self.get_object()

        # Busca a estada ativa (sem data de saída)
        estada_ativa = Estada.objects.filter(veiculo=veiculo, data_saida__isnull=True).select_related('vaga').first()

        context['estada_ativa'] = estada_ativa
        return context

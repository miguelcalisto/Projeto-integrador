from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from estada.models import Estada
from .models import Veiculo
from .forms import VeiculoForm  




class VeiculoListView(LoginRequiredMixin,ListView):
    model = Veiculo
    template_name = 'lista.html'
    context_object_name = 'veiculos'

class VeiculoCreateView(LoginRequiredMixin,CreateView):
    model = Veiculo
    form_class = VeiculoForm  #
    template_name = 'veiculo-criar.html'
    success_url = reverse_lazy('lista_veiculos')

class VeiculoUpdateView(LoginRequiredMixin,UpdateView):
    model = Veiculo
    form_class = VeiculoForm  
    template_name = 'veiculo-editar.html'
    success_url = reverse_lazy('lista_veiculos')

class VeiculoDeleteView(LoginRequiredMixin,DeleteView):
    model = Veiculo
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('lista_veiculos')


    def dispatch(self, request, *args, **kwargs):
        veiculo = self.get_object()
        if Estada.objects.filter(veiculo=veiculo, data_saida__isnull=True).exists():
            messages.warning(request, "Este veículo está em estada ativa e não pode ser excluído.")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

from django.contrib import messages

from django.views.generic import DetailView
class VeiculoDetailView(LoginRequiredMixin, DetailView):
    model = Veiculo
    template_name = 'detalhe_veiculo.html'
    context_object_name = 'veiculo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        veiculo = self.get_object()

        estada_ativa = Estada.objects.filter(veiculo=veiculo, data_saida__isnull=True).select_related('vaga').first()

        context['estada_ativa'] = estada_ativa
        return context
    

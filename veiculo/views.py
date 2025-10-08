from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
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

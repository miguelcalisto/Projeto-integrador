from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Veiculo

class VeiculoListView(ListView):
    model = Veiculo
    template_name = 'lista.html'
    context_object_name = 'veiculos'

class VeiculoCreateView(CreateView):
    model = Veiculo
    fields = ['placa', 'modelo', 'cor' , 'dono']
    template_name = 'form.html'
    success_url = reverse_lazy('lista_veiculos')

class VeiculoUpdateView(UpdateView):
    model = Veiculo
    fields = ['placa', 'modelo', 'cor']
    template_name = 'form.html'
    success_url = reverse_lazy('lista_veiculos')

class VeiculoDeleteView(DeleteView):
    model = Veiculo
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('lista_veiculos')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from estada.models import Estada
from .models import Cliente
from django.core.exceptions import ValidationError
from .forms import ClienteForm  

class ClienteListView(LoginRequiredMixin,ListView):
    model = Cliente
    template_name = 'cliente_list.html'
    context_object_name = 'clientes'

class ClienteDetailView(LoginRequiredMixin,DetailView):
    model = Cliente
    template_name = 'cliente_detail.html'
    context_object_name = 'cliente'

class ClienteCreateView(LoginRequiredMixin,CreateView):
    model = Cliente
    form_class = ClienteForm  
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('cliente_list')

  

class ClienteUpdateView(LoginRequiredMixin,UpdateView):
    model = Cliente
    form_class = ClienteForm  
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('cliente_list')

from django.contrib import messages

class ClienteDeleteView(LoginRequiredMixin,DeleteView):
    model = Cliente
    template_name = 'cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

    def dispatch(self, request, *args, **kwargs):
        cliente = self.get_object()

        if Estada.objects.filter(veiculo__dono=cliente, data_saida__isnull=True).exists():
            messages.warning(request, "Este cliente possui veículos em estada e não pode ser excluído.")
            return redirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

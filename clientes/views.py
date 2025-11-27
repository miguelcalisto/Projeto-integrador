from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
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


class ClienteDeleteView(LoginRequiredMixin,DeleteView):
    model = Cliente
    template_name = 'cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')

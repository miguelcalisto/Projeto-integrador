from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Estada
from .forms import EstadaForm  # Você precisará criar esse form

class EstadaListView(ListView):
    model = Estada
    template_name = 'listar-estada.html'       # Ajuste o caminho conforme seu template
    context_object_name = 'estadas'


class EstadaDetailView(DetailView):
    model = Estada
    template_name = 'detalhe-estada.html'
    context_object_name = 'estada'


class EstadaCreateView(CreateView):
    model = Estada
    form_class = EstadaForm
    template_name = 'criar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')  # Ajuste o namespace e nome da url


class EstadaUpdateView(UpdateView):
    model = Estada
    form_class = EstadaForm
    template_name = 'editar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')


class EstadaDeleteView(DeleteView):
    model = Estada
    template_name = 'deletar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')

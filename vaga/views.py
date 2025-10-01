from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Vaga
from .forms import VagaForm

class VagaListView(ListView):
    model = Vaga
    template_name = 'listar-vagas.html'
    context_object_name = 'vagas'

class VagaDetailView(DetailView):
    model = Vaga
    template_name = 'detalhe-vaga.html'
    context_object_name = 'vaga'

class VagaCreateView(CreateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'criar-vaga.html'
    success_url = reverse_lazy('vaga:lista-vagas')



class VagaUpdateView(UpdateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'editar-vaga.html'
    success_url = reverse_lazy('vaga:lista-vagas')


class VagaDeleteView(DeleteView):
    model = Vaga
    template_name = 'deletar-vaga.html'
    success_url = reverse_lazy('vaga:lista-vagas')

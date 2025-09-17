from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Funcionario
from .forms import FuncionarioForm

class FuncionarioListView(ListView):
    model = Funcionario
    template_name = 'listar.html'
    context_object_name = 'funcionarios'

class FuncionarioDetailView(DetailView):
    model = Funcionario
    template_name = 'detalhe.html'
    context_object_name = 'funcionario'

class FuncionarioCreateView(CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'criar.html'
    success_url = reverse_lazy('funcionarios:lista-funcionarios')


class FuncionarioUpdateView(UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'editar.html'
    success_url = reverse_lazy('funcionarios:lista-funcionarios')


class FuncionarioDeleteView(DeleteView):
    model = Funcionario
    template_name = 'deletar.html'
    success_url = reverse_lazy('funcionarios:lista-funcionarios')


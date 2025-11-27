from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Funcionario
from .forms import FuncionarioForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class FuncionarioListView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = Funcionario
    template_name = 'listar.html'
    context_object_name = 'funcionarios'
    permission_required = 'funcionarios.view_funcionario'
    raise_exception = True  

class FuncionarioDetailView(DetailView):
    model = Funcionario
    template_name = 'detalhe.html'
    context_object_name = 'funcionario'
    permission_required = 'funcionarios.view_funcionario'
    raise_exception = True

class FuncionarioCreateView(CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'criar.html'
    success_url = reverse_lazy('funcionarios:lista-funcionarios')
    permission_required = 'funcionarios.add_funcionario'
    raise_exception = True


class FuncionarioUpdateView(UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'editar.html'
    success_url = reverse_lazy('funcionarios:lista-funcionarios')
    permission_required = 'funcionarios.change_funcionario'
    raise_exception = True


class FuncionarioDeleteView(DeleteView):
    model = Funcionario
    template_name = 'deletar.html'
    success_url = reverse_lazy('funcionarios:lista-funcionarios')
    permission_required = 'funcionarios.delete_funcionario'
    raise_exception = True


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Funcionario
from .forms import FuncionarioForm



class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('login')  # se não estiver logado, vai para login

    def test_func(self):
        # Só permite superusuário
        return self.request.user.is_superuser

    def handle_no_permission(self):
        # Se o usuário estiver logado mas não for superuser
        if self.request.user.is_authenticated:
            # Redireciona para a página inicial (index)
            return redirect('acesso_negado')
        # Se não estiver logado, vai para o login
        return redirect('login')


class FuncionarioListView(SuperuserRequiredMixin,ListView):
    model = Funcionario
    template_name = 'listar.html'
    context_object_name = 'funcionarios'

class FuncionarioDetailView(SuperuserRequiredMixin,DetailView):
    model = Funcionario
    template_name = 'detalhe.html'
    context_object_name = 'funcionario'

class FuncionarioCreateView(SuperuserRequiredMixin,CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'criar.html'
    success_url = reverse_lazy('funcionarios:lista-funcionarios')


class FuncionarioUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'editar.html'
    success_url = reverse_lazy('funcionarios:lista-funcionarios')


class FuncionarioDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Funcionario
    template_name = 'deletar.html'
    success_url = reverse_lazy('funcionarios:lista-funcionarios')


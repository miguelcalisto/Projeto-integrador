from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Vaga
from .forms import VagaForm

class VagaListView(LoginRequiredMixin,ListView):
    model = Vaga
    template_name = 'listar-vagas.html'
    context_object_name = 'vagas'

class VagaDetailView(LoginRequiredMixin,DetailView):
    model = Vaga
    template_name = 'detalhe-vaga.html'
    context_object_name = 'vaga'

# views.py
from django.shortcuts import redirect
from django.contrib import messages
from .models import ConfiguracaoVaga

class VagaCreateView(LoginRequiredMixin, CreateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'criar-vaga.html'
    success_url = reverse_lazy('vaga:lista-vagas')

    def dispatch(self, request, *args, **kwargs):
        try:
            config = ConfiguracaoVaga.objects.first()
            limite = config.limite_maximo
        except AttributeError:
            limite = None  # Sem limite

        if limite is not None and Vaga.objects.count() >= limite:
            messages.warning(request, f"Limite de {limite} vagas atingido. Não é possível adicionar mais.")
            return redirect('vaga:lista-vagas')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        config = ConfiguracaoVaga.objects.first()  # pega a configuração (supondo só 1 registro)
        limite = config.limite_maximo if config else 10  # valor default se não tiver config

        if Vaga.objects.count() >= limite:
            messages.error(self.request, "Limite máximo de vagas atingido. Não é possível adicionar mais vagas.")
            return self.form_invalid(form)

        return super().form_valid(form)




class VagaUpdateView(LoginRequiredMixin,UpdateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'editar-vaga.html'
    success_url = reverse_lazy('vaga:lista-vagas')


class VagaDeleteView(LoginRequiredMixin,DeleteView):
    model = Vaga
    template_name = 'deletar-vaga.html'
    success_url = reverse_lazy('vaga:lista-vagas')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Exemplo: Contagem de vagas por status
        vagas_livre = Vaga.objects.filter(status='livre').count()
        vagas_ocupada = Vaga.objects.filter(status='ocupada').count()

        context['vagas_livre'] = vagas_livre
        context['vagas_ocupada'] = vagas_ocupada
        return context
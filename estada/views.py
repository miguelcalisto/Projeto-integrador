from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.checks import messages
from django.contrib import messages

from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Estada, PagamentoLog
from .forms import EstadaForm, ConfirmarPagamentoForm
from django.conf import settings
from django.utils import timezone


class EstadaListView(LoginRequiredMixin, ListView):
    model = Estada
    template_name = 'listar-estada.html'
    context_object_name = 'estadas'


class EstadaDetailView(LoginRequiredMixin, DetailView):
    model = Estada
    template_name = 'detalhe-estada.html'
    context_object_name = 'estada'


class EstadaCreateView(LoginRequiredMixin, CreateView):
    model = Estada
    form_class = EstadaForm
    template_name = 'criar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')

    def form_valid(self, form):
        response = super().form_valid(form)
        estada = self.object
        vaga = estada.vaga
        if vaga:
            vaga.status = 'ocupada'
            vaga.save()
        return response


class EstadaUpdateView(LoginRequiredMixin, UpdateView):
    model = Estada
    form_class = EstadaForm
    template_name = 'editar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')


class EstadaDeleteView(LoginRequiredMixin, DeleteView):
    model = Estada
    template_name = 'deletar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        vaga = self.object.vaga
        if vaga:
            vaga.status = 'livre'
            vaga.save()
        response = super().delete(request, *args, **kwargs)
        return response

@login_required(login_url='login')
def confirmar_pagamento(request, pk):
    estada = get_object_or_404(Estada, pk=pk)

    if request.method == 'POST':
        form = ConfirmarPagamentoForm(request.POST, instance=estada)
        if form.is_valid():
            estada = form.save(commit=False)
            estada.data_saida = estada.data_saida or timezone.now()
            estada.tempo_total = estada.calcular_tempo_total()
            estada.valor_pagamento = estada.calcular_valor_pagamento()
            estada.pago = True
            estada.save()

            # Salvar o log de pagamento
            PagamentoLog.objects.create(
                veiculo=estada.veiculo,
                vaga=estada.vaga,
                funcionario=estada.funcionario_responsavel,
                data_pagamento=timezone.now(),
                valor_pago=estada.valor_pagamento,
                modalidade_pagamento=estada.modalidade_pagamento,
                tempo_total=estada.tempo_total,
            )

            messages.success(request, 'Pagamento confirmado e registrado com sucesso!')
            return redirect('estada:lista-estadas')

    else:
        form = ConfirmarPagamentoForm(instance=estada)

    context = {'estada': estada, 'form': form}
    return render(request, 'confirmar_pagamento.html', context)

def historico_pagamentos(request):
    pagamentos = PagamentoLog.objects.all().order_by('-data_pagamento')
    return render(request, 'historico_pagamentos.html', {'pagamentos': pagamentos})
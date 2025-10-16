from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Estada
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
            estada.data_saida = timezone.now()
            estada.tempo_total = estada.data_saida - estada.data_entrada
            estada.valor_pagamento = estada.calcular_valor_pagamento()
            estada.pago = True
            estada.save()

            print("Data saída:", estada.data_saida)
            print("Tempo total:", estada.tempo_total)
            print("Valor pagamento:", estada.valor_pagamento)

            # Monta e envia o email (ajuste o e-mail e configs depois)
            subject = f'Pagamento confirmado para Estada {estada.pk}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to = ['miguelcalistors@gmail.com']  # Coloque seu email

            context_email = {
                'estada': estada,
                'veiculo': estada.veiculo,
                'vaga': estada.vaga,
                'cliente': estada.veiculo.dono if estada.veiculo.dono else None,
                'tempo_total': estada.tempo_total,
                'valor_pagamento': estada.valor_pagamento,
                'modalidade_pagamento': estada.modalidade_pagamento,
            }

            html_content = render_to_string('emails/pagamento_confirmado.html', context_email)
            text_content = render_to_string('emails/pagamento_confirmado.txt', context_email)

            email = EmailMultiAlternatives(subject, text_content, from_email, to)
            email.attach_alternative(html_content, "text/html")
            email.send()

            return redirect('estada:lista-estadas')

    else:
        form = ConfirmarPagamentoForm(instance=estada)

    context = {
        'form': form,
        'estada': estada,
    }

    return render(request, 'confirmar_pagamento.html', context)
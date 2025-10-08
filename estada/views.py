from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Estada
from .forms import EstadaForm  # Você precisará criar esse form

from django.conf import settings

class EstadaListView(LoginRequiredMixin,ListView):
    model = Estada
    template_name = 'listar-estada.html'       # Ajuste o caminho conforme seu template
    context_object_name = 'estadas'


class EstadaDetailView(LoginRequiredMixin,DetailView):
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

        estada = self.object  # já salvo

        # Atualiza a vaga para "ocupada", se necessário
        vaga = estada.vaga
        if vaga:
            vaga.status = 'ocupada'
            vaga.save()

        # Se já está pago, envia o e-mail
        if estada.pago:
            self.enviar_email_pagamento(estada)

        return response

    def enviar_email_pagamento(self, estada):
        subject = f'Pagamento confirmado para Estada {estada.pk}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to = ['EMAIL']

        context = {
            'estada': estada,
            'veiculo': estada.veiculo,
            'vaga': estada.vaga,
            'cliente': estada.veiculo.dono if estada.veiculo.dono else None,
            'tempo_total': estada.tempo_total,
        }

        html_content = render_to_string('emails/pagamento_confirmado.html', context)
        text_content = render_to_string('emails/pagamento_confirmado.txt', context)

        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, "text/html")
        email.send()



class EstadaUpdateView(LoginRequiredMixin, UpdateView):
    model = Estada
    form_class = EstadaForm
    template_name = 'editar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')

    def form_valid(self, form):
        # Pega o estado anterior do objeto
        estada_antiga = self.get_object()

        response = super().form_valid(form)

        estada = self.object  # objeto atualizado

        # Verifica se o campo 'pago' mudou de False para True
        if not estada_antiga.pago and estada.pago:
            self.enviar_email_pagamento(estada)

        return response

    def enviar_email_pagamento(self, estada):
        subject = f'Pagamento confirmado para Estada {estada.pk}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to = ['EMAIL']

        context = {
            'estada': estada,
            'veiculo': estada.veiculo,
            'vaga': estada.vaga,
            'cliente': estada.veiculo.dono if estada.veiculo.dono else None,
            'tempo_total': estada.tempo_total,
        }

        html_content = render_to_string('emails/pagamento_confirmado.html', context)
        text_content = render_to_string('emails/pagamento_confirmado.txt', context)

        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, "text/html")
        email.send()


# altera para livre quando a vaga eh att
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #
    #     vaga = self.object.vaga
    #     if vaga and self.object.data_saida:
    #         vaga.status = 'livre'  # Marca vaga como livre ao finalizar estada
    #         vaga.save()
    #
    #     return response


class EstadaDeleteView(LoginRequiredMixin,DeleteView):
    model = Estada
    template_name = 'deletar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        vaga = self.object.vaga

        if vaga:
            print(f'Atualizando status da vaga {vaga.pk} para livre antes de deletar a estada {self.object.pk}')
            vaga.status = 'livre'
            vaga.save()

        response = super().delete(request, *args, **kwargs)
        print(f'Estada {self.object.pk} deletada com sucesso.')
        return response



# @login_required(login_url='login')
# def confirmar_pagamento(request, pk):
#     estada = get_object_or_404(Estada, pk=pk)
#     estada.pago = True
#     estada.save()
#     return redirect('estada:lista-estadas')  # Ou ajuste o nome se for diferente

@login_required(login_url='login')
def confirmar_pagamento(request, pk):
    estada = get_object_or_404(Estada, pk=pk)
    estada.pago = True
    estada.save()

    subject = f'Pagamento confirmado para Estada {estada.pk}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = ['EMAIL']

    # Contexto para o template HTML
    context = {
        'estada': estada,
        'veiculo': estada.veiculo,
        'vaga': estada.vaga,
        'cliente': estada.veiculo.cliente if hasattr(estada.veiculo, 'cliente') else None,
        'tempo_total': estada.data_saida - estada.data_entrada if estada.data_saida else None,
    }

    # Carrega o template HTML e o texto simples
    html_content = render_to_string('emails/pagamento_confirmado.html', context)
    text_content = render_to_string('emails/pagamento_confirmado.txt', context)

    # Cria o email multi formato
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()

    return redirect('estada:lista-estadas')
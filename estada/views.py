from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
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


class EstadaCreateView(LoginRequiredMixin,CreateView):
    model = Estada
    form_class = EstadaForm
    template_name = 'criar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')  # Ajuste o namespace e nome da url

    def form_valid(self, form):
        response = super().form_valid(form)

        # Depois de salvar a Estada, atualize o status da vaga vinculada
        vaga = self.object.vaga
        if vaga:
            vaga.status = 'ocupada'  # Marca como ocupada ao criar estada
            vaga.save()

        return response


class EstadaUpdateView(LoginRequiredMixin,UpdateView):
    model = Estada
    form_class = EstadaForm
    template_name = 'editar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')


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

    # Dados do email
    assunto = f'Pagamento confirmado para Estada {estada.pk}'
    mensagem = (
        f'O pagamento da estada do veículo {estada.veiculo} na vaga {estada.vaga} '
        f'foi confirmado com sucesso.\n\n'
        f'Data Entrada: {estada.data_entrada}\n'
        f'Data Saída: {estada.data_saida or "Não informada"}\n'
        f'Status: {"Pago" if estada.pago else "Pendente"}'
    )
    destinatario = ['SEUEMAIL@gmail.com']  # Troque pelo email real que deve receber

    send_mail(assunto, mensagem, None, destinatario)

    return redirect('estada:lista-estadas')
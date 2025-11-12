from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.checks import messages
from django.contrib import messages

from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
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

            # Excluir a estada após confirmação do pagamento
            estada.delete()

            messages.success(request, 'Pagamento confirmado, registrado e estada excluída com sucesso!')
            return redirect('estada:lista-estadas')

    else:
        form = ConfirmarPagamentoForm(instance=estada)

    context = {'estada': estada, 'form': form}
    return render(request, 'confirmar_pagamento.html', context)


def historico_pagamentos(request):
    pagamentos_list = PagamentoLog.objects.all().order_by('-data_pagamento')

    # 🔹 Define quantos registros por página (ex: 10)
    paginator = Paginator(pagamentos_list, 10)

    # 🔹 Obtém o número da página via GET (ex: ?page=2)
    page_number = request.GET.get('page')
    pagamentos = paginator.get_page(page_number)

    return render(request, 'historico_pagamentos.html', {'pagamentos': pagamentos})

from django.utils import timezone  # só uma vez no topo do arquivo


def exportar_pagamentos_txt(request):
    pagamentos = PagamentoLog.objects.all().order_by('-data_pagamento')

    linhas = []
    for idx, p in enumerate(pagamentos, start=1):
        data_local = timezone.localtime(p.data_pagamento)  # converte pro horário local


        linha = (
            f"{idx} - "
            f"Veículo: {p.veiculo} | "
            f"Vaga: {p.vaga} | "
            f"Funcionário: {p.funcionario} | "
            f"Data: {p.data_pagamento.strftime('%d/%m/%Y %H:%M')} | "
            f"Tempo: {p.tempo_total} | "
            f"Valor: R$ {p.valor_pago} | "
            f"Modalidade: {p.modalidade_pagamento}"
        )
        linhas.append(linha)
        linhas.append("")  # linha em branco para espaçamento

    conteudo = "\n".join(linhas)

    response = HttpResponse(conteudo, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=relatorio_pagamentos.txt'
    return response


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import textwrap

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from django.http import HttpResponse
from .models import PagamentoLog

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from django.http import HttpResponse
from .models import PagamentoLog

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from django.http import HttpResponse
from .models import PagamentoLog

def exportar_pagamentos_pdf(request):
    pagamentos = PagamentoLog.objects.all().order_by('-data_pagamento')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_pagamentos.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    largura, altura = A4
    y = altura - 3 * cm

    p.setFont("Helvetica-Bold", 14)
    p.drawString(2 * cm, y, "Relatório de Pagamentos - Estacionamento")
    y -= 1 * cm

    p.setFont("Helvetica", 10)

    for idx, pagamento in enumerate(pagamentos, start=1):
        # 🔹 Monta a primeira linha com somente os campos existentes
        data_local = timezone.localtime(pagamento.data_pagamento)  # converte

        linha1_partes = [
            f"{idx}. Veículo: {pagamento.veiculo}" if pagamento.veiculo else None,
            f"Vaga: {pagamento.vaga}" if pagamento.vaga else None,
            f"Funcionário: {pagamento.funcionario}" if pagamento.funcionario else None,
        ]
        linha1 = " | ".join([parte for parte in linha1_partes if parte])  # remove os None

        # 🔹 Segunda linha com os dados de tempo e pagamento
        linha2_partes = [
            f"Data: {data_local.strftime('%d/%m/%Y %H:%M')}" if pagamento.data_pagamento else None,

            f"Tempo: {pagamento.tempo_total}" if pagamento.tempo_total else None,
            f"Valor: R$ {pagamento.valor_pago}" if pagamento.valor_pago is not None else None,
            f"Modalidade: {pagamento.modalidade_pagamento}" if pagamento.modalidade_pagamento else None,
        ]
        linha2 = " | ".join([parte for parte in linha2_partes if parte])

        # 🔹 Desenha as duas linhas
        p.drawString(2 * cm, y, linha1)
        y -= 0.6 * cm
        p.drawString(2.5 * cm, y, linha2)
        y -= 0.8 * cm

        # Quebra de página automática
        if y <= 2 * cm:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = altura - 2 * cm

    p.showPage()
    p.save()
    return response

# emails

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

            # Salvar log de pagamento
            PagamentoLog.objects.create(
                veiculo=estada.veiculo,
                vaga=estada.vaga,
                funcionario=estada.funcionario_responsavel,
                data_pagamento=timezone.now(),
                valor_pago=estada.valor_pagamento,
                modalidade_pagamento=estada.modalidade_pagamento,
                tempo_total=estada.tempo_total,
            )

            # -------------------------------
            # 🔹 Enviar e-mail de confirmação
            # -------------------------------
            subject = f'Pagamento confirmado - Estada #{estada.pk}'
            from_email = settings.DEFAULT_FROM_EMAIL
            # Aqui você pode enviar para o dono do veículo, ou um email fixo do sistema:
            destinatarios = ['miguelcalistors@gmail.com']

            if hasattr(estada.veiculo, 'cliente') and estada.veiculo.cliente.email:
                destinatarios.append(estada.veiculo.cliente.email)
            else:
                # fallback: envia para o admin
                destinatarios.append(settings.DEFAULT_FROM_EMAIL)

            from valorpagamento.models import ValorPagamento  # ✅ importe no topo do arquivo (se ainda não tiver)
            valor_obj = ValorPagamento.objects.first()
            valor_hora = valor_obj.valor_hora if valor_obj else 5.00

            context = {
                'estada': estada,
                'veiculo': estada.veiculo,
                'vaga': estada.vaga,
                'funcionario': estada.funcionario_responsavel,
                'tempo_total': estada.tempo_total,
                'valor_pagamento': estada.valor_pagamento,
                'modalidade': estada.modalidade_pagamento,
                'data_saida': estada.data_saida,
                'valor_hora': valor_hora,  # ✅ adiciona ao contexto
            }

            html_content = render_to_string('emails/pagamento_confirmado.html', context)
            text_content = render_to_string('emails/pagamento_confirmado.txt', context)

            email = EmailMultiAlternatives(subject, text_content, from_email, destinatarios)
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            # -------------------------------

            # Excluir a estada após pagamento
            estada.delete()

            messages.success(request, 'Pagamento confirmado, e-mail enviado e estada excluída com sucesso!')
            return redirect('estada:lista-estadas')

    else:
        form = ConfirmarPagamentoForm(instance=estada)


    context = {'estada': estada, 'form': form}
    return render(request, 'confirmar_pagamento.html', context)



import json

class DashboardPagamentosView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard_pagamentos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagamentos = PagamentoLog.objects.all()
        agora = timezone.now()

        # 🔹 Lucro total e do mês
        lucro_total = pagamentos.aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0
        lucro_mes = pagamentos.filter(data_pagamento__month=agora.month, data_pagamento__year=agora.year).aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0

        # 🔹 Total de pagamentos
        total_pagamentos = pagamentos.count()

        # 🔹 Pagamentos por modalidade
        modalidades = (
            pagamentos.values('modalidade_pagamento')
            .annotate(total=Count('id'))
            .order_by('-total')
        )

        # 🔹 Tempo médio de permanência
        tempo_medio = pagamentos.aggregate(Avg('tempo_total'))['tempo_total__avg']
        tempo_medio_horas = round(tempo_medio.total_seconds() / 3600, 2) if tempo_medio else 0

        # 🔹 Receita anual — soma por mês do ano atual
        ano_atual = agora.year
        receitas_por_mes = (
            pagamentos.filter(data_pagamento__year=ano_atual)
            .annotate(mes=TruncMonth('data_pagamento'))
            .values('mes')
            .annotate(total=Sum('valor_pago'))
            .order_by('mes')
        )

        # Monta listas completas dos 12 meses (mesmo se algum mês não tiver dados)
        import calendar
        meses_labels = [calendar.month_abbr[m] for m in range(1, 13)]
        totais = [0] * 12

        for r in receitas_por_mes:
            mes_idx = r['mes'].month - 1
            totais[mes_idx] = float(r['total'])

        context.update({
            'lucro_total': lucro_total,
            'lucro_mes': lucro_mes,
            'total_pagamentos': total_pagamentos,
            'tempo_medio_horas': tempo_medio_horas,
            'modalidades': modalidades,
            'ano_atual': ano_atual,
            'meses_json': json.dumps(meses_labels),
            'totais_json': json.dumps(totais),
        })
        return context
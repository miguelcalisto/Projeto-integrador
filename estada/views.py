import calendar
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

from valorpagamento.models import ValorPagamento
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


class HistoricoPagamentosView(ListView):
    model = PagamentoLog
    template_name = 'historico_pagamentos.html'
    context_object_name = 'pagamentos'
    paginate_by = 10
    ordering = '-data_pagamento'
 



from django.utils import timezone  




from django.views import View
from django.http import HttpResponse
from django.utils import timezone
from .models import PagamentoLog

class ExportarPagamentosTxtView(View):
    def get(self, request, *args, **kwargs):
        pagamentos = PagamentoLog.objects.all().order_by('-data_pagamento')

        linhas = []
        for idx, p in enumerate(pagamentos, start=1):
            data_local = timezone.localtime(p.data_pagamento)  
            linha = (
                f"{idx} - "
                f"Veículo: {p.veiculo} | "
                f"Vaga: {p.vaga} | "
                f"Funcionário: {p.funcionario} | "
                f"Data: {data_local.strftime('%d/%m/%Y %H:%M')} | "
                f"Tempo: {p.tempo_total} | "
                f"Valor: R$ {p.valor_pago} | "
                f"Modalidade: {p.modalidade_pagamento}"
            )
            linhas.append(linha)
            linhas.append("")  

        conteudo = "\n".join(linhas)

        response = HttpResponse(conteudo, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=relatorio_pagamentos.txt'
        return response


class ConfirmarPagamentoView(LoginRequiredMixin, UpdateView):
    model = Estada
    form_class = ConfirmarPagamentoForm
    template_name = 'confirmar_pagamento.html'

    def form_valid(self, form):
        estada = form.save(commit=False)

        # Atualiza campos
        estada.data_saida = estada.data_saida or timezone.now()
        estada.tempo_total = estada.calcular_tempo_total()
        estada.valor_pagamento = estada.calcular_valor_pagamento()
        estada.pago = True
        estada.save()

        # Salva log de pagamento
        PagamentoLog.objects.create(
            veiculo=estada.veiculo,
            vaga=estada.vaga,
            funcionario=estada.funcionario_responsavel,
            data_pagamento=timezone.now(),
            valor_pago=estada.valor_pagamento,
            modalidade_pagamento=estada.modalidade_pagamento,
            tempo_total=estada.tempo_total,
        )

        # email
        self.enviar_email(estada)

        estada.delete()

        messages.success(self.request, 'Pagamento confirmado, e-mail enviado e estada excluída com sucesso!')
        return redirect('estada:lista-estadas')
# func email
    def enviar_email(self, estada):
        destinatarios = ['miguelcalistors@gmail.com']

        if estada.veiculo.dono and estada.veiculo.dono.email:
            destinatarios.append(estada.veiculo.dono.email)
        else:
            destinatarios.append(settings.DEFAULT_FROM_EMAIL)


        print("DESTINATÁRIOS DO E-MAIL:", destinatarios)


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
            'valor_hora': valor_hora,
        }

        texto_email = render_to_string('emails/pagamento_confirmado.txt', context)
        html_email = render_to_string('emails/pagamento_confirmado.html', context)

        email = EmailMultiAlternatives(
            subject=f'Pagamento confirmado - Estada #{estada.pk}',
            body=texto_email,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=destinatarios,
        )
        email.attach_alternative(html_email, "text/html")
        email.send(fail_silently=False)



from django.views.generic import ListView
from .models import PagamentoLog

class PagamentosGraficoView(ListView):
    model = PagamentoLog
    template_name = 'dashboard_pagamentos.html'
    context_object_name = 'pagamentos'

    def get_queryset(self):
        return PagamentoLog.objects.all().order_by('-data_pagamento')



from weasyprint import HTML

class ExportarPagamentosPdfView(View):
    template_name = 'pagamentos_pdf.html'

    def get(self, request, *args, **kwargs):
        pagamentos = PagamentoLog.objects.all().order_by('-data_pagamento')

        html_string = render_to_string(self.template_name, {
            'pagamentos': pagamentos,
            'gerado_em': timezone.now(),
        })

        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_pagamentos.pdf"'

        return response
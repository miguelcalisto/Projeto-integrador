from django.db import models
from funcionarios.models import Funcionario
from vaga.models import Vaga
from valorpagamento.models import ValorPagamento
from veiculo.models import Veiculo
from django.utils import timezone
from datetime import timedelta

class Estada(models.Model):
    DINHEIRO = 'dinheiro'
    CARTAO = 'cartao'
    PIX = 'pix'

    MODALIDADE_PAGAMENTO_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
    ]
  
    data_entrada = models.DateTimeField(auto_now_add=True)


    data_saida = models.DateTimeField(null=True, blank=True)
    vaga = models.ForeignKey(Vaga, on_delete=models.SET_NULL, null=True, blank=True)
    valor_pagamento = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    modalidade_pagamento = models.CharField(max_length=10, choices=MODALIDADE_PAGAMENTO_CHOICES, null=True, blank=True)
    # fk funcionairo
    funcionario_responsavel = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    # fk veiculo
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='estadas')
    tempo_total = models.DurationField(null=True, blank=True)
    pago = models.BooleanField(default=False)

    def __str__(self):
        status_pagamento = "Pago" if self.pago else "Pendente"
        return f"Estada do veículo {self.veiculo} na vaga {self.vaga} - Situação: {status_pagamento}"

    def calcular_tempo_total(self):
        if self.data_saida and self.data_entrada:
            return self.data_saida - self.data_entrada
        return None

    def calcular_valor_pagamento(self):
        if not (self.data_saida and self.data_entrada):
            return 0.00

        tempo_total = self.calcular_tempo_total()
        if not tempo_total:
            return 0.00

        try:
            taxa = ValorPagamento.objects.first().valor_hora
        except AttributeError:
            taxa = 5.00  

        horas = tempo_total.total_seconds() / 3600
        valor = horas * float(taxa)

        

        if self.modalidade_pagamento == self.PIX:
            valor *= 0.90

        if horas > 6:
            valor *= 1.10

    
        if self.veiculo and self.veiculo.dono and self.veiculo.dono.tipo == 'J':
            valor *= 1.15


        return round(valor, 2)

    def delete(self, *args, **kwargs):
        # Antes de apagar a estada, marca a vaga como livre.
        vaga = self.vaga
        if vaga:
            vaga.status = 'livre'
            vaga.save()
        super().delete(*args, **kwargs)






class PagamentoLog(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True)
    vaga = models.ForeignKey(Vaga, on_delete=models.SET_NULL, null=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    data_pagamento = models.DateTimeField(default=timezone.now)
    valor_pago = models.DecimalField(max_digits=8, decimal_places=2)
    modalidade_pagamento = models.CharField(max_length=10)
    tempo_total = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"Pagamento do veículo {self.veiculo} em {self.data_pagamento.strftime('%d/%m/%Y %H:%M')}"
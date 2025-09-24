from django.db import models

from funcionarios.models import Funcionario
from veiculo.models import Veiculo


# Create your models here.
class Estada(models.Model):

    DINHEIRO = 'dinheiro'
    CARTAO = 'cartao'
    PIX = 'pix'

    MODALIDADE_PAGAMENTO_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
    ]

    # Datas de entrada e saída
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField(null=True, blank=True)

    # Dados da vaga incorporados
    numero_vaga = models.CharField(max_length=10)
    status_vaga = models.BooleanField(default=True)  # True = disponível, False = ocupada

    # Dados de pagamento incorporados
    valor_pagamento = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    modalidade_pagamento = models.CharField(
        max_length=10,
        choices=MODALIDADE_PAGAMENTO_CHOICES,
        null=True,
        blank=True,
    )

    # Relacionamentos
    funcionario_responsavel = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='estadas')

    # Campos calculados
    tempo_total = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"Estada do veículo {self.veiculo} na vaga {self.numero_vaga}"
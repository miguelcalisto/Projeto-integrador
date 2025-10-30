# estada/tests.py
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from estada.models import Estada, ValorPagamento
from veiculo.models import Veiculo
from clientes.models import Cliente
from funcionarios.models import Funcionario
from vaga.models import Vaga

class RegrasEstadaTest(TestCase):

    def setUp(self):
        # Criando funcionário
        self.funcionario = Funcionario.objects.create(
            nome="Funcionario Teste",
            cpf="12345678901",
            data_nascimento="1990-01-01",
        )

        # Criando vagas
        self.vaga = Vaga.objects.create(numero=1, status="livre")

        # Criando clientes PF e PJ
        self.cliente_pf = Cliente.objects.create(nome="Cliente PF", tipo="F")
        self.cliente_pj = Cliente.objects.create(nome="Cliente PJ", tipo="J")

        # Criando veículos
        self.veiculo_pf = Veiculo.objects.create(placa="AAA1111", dono=self.cliente_pf)
        self.veiculo_pj = Veiculo.objects.create(placa="BBB2222", dono=self.cliente_pj)

        # Criando taxa de pagamento
        ValorPagamento.objects.create(valor_hora=10.0)

    def test_calculo_valores(self):
        agora = timezone.now()

        # Estada PF (5 horas, pagamento via cartão)
        estada_pf = Estada.objects.create(
            veiculo=self.veiculo_pf,
            vaga=self.vaga,
            funcionario_responsavel=self.funcionario,
            data_entrada=agora,
            data_saida=agora + timedelta(hours=5),
            modalidade_pagamento=Estada.CARTAO
        )

        # Estada PJ (7 horas, pagamento via Pix)
        estada_pj = Estada.objects.create(
            veiculo=self.veiculo_pj,
            vaga=self.vaga,
            funcionario_responsavel=self.funcionario,
            data_entrada=agora,
            data_saida=agora + timedelta(hours=7),
            modalidade_pagamento=Estada.PIX
        )

        # Calcula valores
        valor_pf = estada_pf.calcular_valor_pagamento()
        valor_pj = estada_pj.calcular_valor_pagamento()

        print("Valor PF:", valor_pf)
        print("Valor PJ:", valor_pj)

        # Regras de negócio:
        # - Estada PJ maior que 6h (+10%) e pessoa jurídica (+15%), desconto Pix (-10%)
        self.assertGreater(valor_pj, valor_pf)

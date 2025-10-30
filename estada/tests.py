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
        self.funcionario = Funcionario.objects.create(
            nome="Funcionario Teste",
            cpf="12345678901",
            data_nascimento="1990-01-01",
        )
        self.vaga = Vaga.objects.create(numero=1, status="livre")
        self.cliente_pf = Cliente.objects.create(nome="Cliente PF", tipo="F")
        self.cliente_pj = Cliente.objects.create(nome="Cliente PJ", tipo="J")
        self.veiculo_pf = Veiculo.objects.create(placa="AAA1111", dono=self.cliente_pf)
        self.veiculo_pj = Veiculo.objects.create(placa="BBB2222", dono=self.cliente_pj)
        ValorPagamento.objects.create(valor_hora=10.0)

    def test_desconto_pix(self):
        agora = timezone.now()
        estada = Estada.objects.create(
            veiculo=self.veiculo_pf,
            vaga=self.vaga,
            funcionario_responsavel=self.funcionario,
            data_entrada=agora,
            data_saida=agora + timedelta(hours=2),
            modalidade_pagamento=Estada.PIX
        )
        valor = estada.calcular_valor_pagamento()
        esperado = 10.0 * 2 * 0.9  # 2 horas * 10/h * desconto 10% Pix
        self.assertAlmostEqual(valor, esperado, places=2)

    def test_taxa_acima_6_horas(self):
        agora = timezone.now()
        estada = Estada.objects.create(
            veiculo=self.veiculo_pf,
            vaga=self.vaga,
            funcionario_responsavel=self.funcionario,
            data_entrada=agora,
            data_saida=agora + timedelta(hours=7),
            modalidade_pagamento=Estada.CARTAO
        )
        valor = estada.calcular_valor_pagamento()
        esperado = 10.0 * 7 * 1.10  # 7 horas * 10/h * +10%
        self.assertAlmostEqual(valor, esperado, places=2)

    def test_taxa_pj(self):
        agora = timezone.now()
        estada = Estada.objects.create(
            veiculo=self.veiculo_pj,
            vaga=self.vaga,
            funcionario_responsavel=self.funcionario,
            data_entrada=agora,
            data_saida=agora + timedelta(hours=3),
            modalidade_pagamento=Estada.CARTAO
        )
        valor = estada.calcular_valor_pagamento()
        esperado = 10.0 * 3 * 1.15  # 3 horas * 10/h * +15% PJ
        self.assertAlmostEqual(valor, esperado, places=2)

    def test_combinacao_pix_mais_6h_mais_pj(self):
        agora = timezone.now()
        estada = Estada.objects.create(
            veiculo=self.veiculo_pj,
            vaga=self.vaga,
            funcionario_responsavel=self.funcionario,
            data_entrada=agora,
            data_saida=agora + timedelta(hours=7),
            modalidade_pagamento=Estada.PIX
        )
        valor = estada.calcular_valor_pagamento()
        # Ordem: valor base * +10% (>6h) * +15% (PJ) * -10% (Pix)
        base = 10.0 * 7
        esperado = base * 1.10 * 1.15 * 0.9
        self.assertAlmostEqual(valor, round(esperado, 2), places=2)

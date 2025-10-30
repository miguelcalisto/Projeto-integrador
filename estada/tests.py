from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from estada.models import Estada, ValorPagamento
from veiculo.models import Veiculo
from clientes.models import Cliente
from funcionarios.models import Funcionario
from vaga.models import Vaga

class TestRegrasCombinadas(TestCase):

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

    def test_todas_combinacoes_regras(self):
        agora = timezone.now()
        combinacoes = [
            # (veiculo, horas, modalidade, descricao)
            (self.veiculo_pf, 2, Estada.DINHEIRO, "PF, 2h, Dinheiro"),
            (self.veiculo_pf, 7, Estada.DINHEIRO, "PF, 7h, Dinheiro"),
            (self.veiculo_pj, 2, Estada.DINHEIRO, "PJ, 2h, Dinheiro"),
            (self.veiculo_pj, 7, Estada.DINHEIRO, "PJ, 7h, Dinheiro"),
            (self.veiculo_pf, 2, Estada.PIX, "PF, 2h, PIX"),
            (self.veiculo_pf, 7, Estada.PIX, "PF, 7h, PIX"),
            (self.veiculo_pj, 2, Estada.PIX, "PJ, 2h, PIX"),
            (self.veiculo_pj, 7, Estada.PIX, "PJ, 7h, PIX"),
        ]

        for veiculo, horas, modalidade, descricao in combinacoes:
            with self.subTest(descricao=descricao):
                estada = Estada.objects.create(
                    veiculo=veiculo,
                    vaga=self.vaga,
                    funcionario_responsavel=self.funcionario,
                    data_entrada=agora,
                    data_saida=agora + timedelta(hours=horas),
                    modalidade_pagamento=modalidade
                )

                # Valor base
                base = 10.0 * horas

                # Aplicar regras passo a passo
                if horas > 6:
                    base *= 1.10  # +10% por mais de 6h
                if getattr(veiculo.dono, 'tipo', '') == 'J':
                    base *= 1.15  # +15% PJ
                if modalidade == Estada.PIX:
                    base *= 0.90  # -10% PIX

                valor_esperado = round(base, 2)
                valor_calculado = estada.calcular_valor_pagamento()

                self.assertAlmostEqual(valor_calculado, valor_esperado, places=2, msg=f"Falha na combinação: {descricao}")

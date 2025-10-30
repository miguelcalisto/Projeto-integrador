from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from clientes.models import Cliente
from veiculo.models import Veiculo
from estada.models import Estada
from valorpagamento.models import ValorPagamento

class RegrasEstadaTest(TestCase):
    def setUp(self):
        # 1️⃣ Garantir valor da hora
        ValorPagamento.objects.update_or_create(id=1, defaults={'valor_hora': 5})

        # 2️⃣ Criar clientes
        self.pj = Cliente.objects.create(
            nome="Empresa X", email="x@empresa.com", telefone="1111", tipo="J", cnpj="12345678000199"
        )
        self.pf = Cliente.objects.create(
            nome="João", email="joao@gmail.com", telefone="2222", tipo="F", cpf="123.456.789-00"
        )

        # 3️⃣ Criar veículos
        self.v_pj = Veiculo.objects.create(placa="AAA-1111", modelo="Carro PJ", cor="Preto", dono=self.pj)
        self.v_pf = Veiculo.objects.create(placa="BBB-2222", modelo="Carro PF", cor="Branco", dono=self.pf)

        # 4️⃣ Definir tempos
        self.agora = timezone.now()
        self.tempos = {
            "curta": self.agora - timedelta(minutes=30),   # <6h
            "longa": self.agora - timedelta(hours=7),      # >6h
        }

    def test_regras_negocio_estadas(self):
        testes = [
            {"veiculo": self.v_pj, "entrada": self.tempos["curta"], "saida": self.agora, "modalidade": "pix", "desc": "PJ + Pix <6h", "esperado": round((30/60*5)*0.9*1.15,2)},
            {"veiculo": self.v_pf, "entrada": self.tempos["curta"], "saida": self.agora, "modalidade": "pix", "desc": "PF + Pix <6h", "esperado": round((30/60*5)*0.9,2)},
            {"veiculo": self.v_pj, "entrada": self.tempos["longa"], "saida": self.agora, "modalidade": "dinheiro", "desc": "PJ + Dinheiro >6h", "esperado": round((7*5)*1.10*1.15,2)},
            {"veiculo": self.v_pf, "entrada": self.tempos["longa"], "saida": self.agora, "modalidade": "dinheiro", "desc": "PF + Dinheiro >6h", "esperado": round((7*5)*1.10,2)},
            {"veiculo": self.v_pj, "entrada": self.tempos["longa"], "saida": self.agora, "modalidade": "pix", "desc": "PJ + Pix >6h", "esperado": round((7*5)*0.9*1.10*1.15,2)},
        ]

        for t in testes:
            estada = Estada(
                veiculo=t["veiculo"],
                data_entrada=t["entrada"],
                data_saida=t["saida"],
                modalidade_pagamento=t["modalidade"]
            )
            valor_calculado = estada.calcular_valor_pagamento()
            tempo_total = estada.calcular_tempo_total()

            # Print opcional para debug
            print(f"{t['desc']}: Tempo total={tempo_total}, Valor calculado={valor_calculado}")

            # Verifica se o valor bate com a regra esperada
            self.assertAlmostEqual(valor_calculado, t["esperado"], places=2)

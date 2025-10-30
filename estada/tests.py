from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from clientes.models import Cliente
from veiculo.models import Veiculo
from estada.models import Estada
from valorpagamento.models import ValorPagamento

class RegrasEstadaTest(TestCase):
    def setUp(self):
        # 1️⃣ Criar valor de hora
        ValorPagamento.objects.update_or_create(id=1, defaults={'valor_hora': 5})

        # 2️⃣ Criar clientes
        self.pj = Cliente.objects.create(nome="Empresa X", email="x@empresa.com", telefone="1111", tipo="J", cnpj="12345678000199")
        self.pf = Cliente.objects.create(nome="João", email="joao@gmail.com", telefone="2222", tipo="F", cpf="123.456.789-00")

        # 3️⃣ Criar veículos
        self.v_pj = Veiculo.objects.create(placa="AAA-1111", modelo="Carro PJ", cor="Preto", dono=self.pj)
        self.v_pf = Veiculo.objects.create(placa="BBB-2222", modelo="Carro PF", cor="Branco", dono=self.pf)

        # 4️⃣ Definir tempos
        self.agora = timezone.now()
        self.tempos = {
            "curta": self.agora - timedelta(minutes=30),  # <6h
            "longa": self.agora - timedelta(hours=7),     # >6h
        }

    def test_regras_negocio_estadas(self):
        # Criar estadas
        testes = [
            {"veiculo": self.v_pj, "entrada": self.tempos["curta"], "saida": self.agora, "modalidade": "pix", "desc": "PJ + Pix <6h"},
            {"veiculo": self.v_pf, "entrada": self.tempos["curta"], "saida": self.agora, "modalidade": "pix", "desc": "PF + Pix <6h"},
            {"veiculo": self.v_pj, "entrada": self.tempos["longa"], "saida": self.agora, "modalidade": "dinheiro", "desc": "PJ + Dinheiro >6h"},
            {"veiculo": self.v_pf, "entrada": self.tempos["longa"], "saida": self.agora, "modalidade": "dinheiro", "desc": "PF + Dinheiro >6h"},
            {"veiculo": self.v_pj, "entrada": self.tempos["longa"], "saida": self.agora, "modalidade": "pix", "desc": "PJ + Pix >6h"},
        ]

        for t in testes:
            estada = Estada.objects.create(
                veiculo=t["veiculo"],
                data_saida=t["saida"],
                modalidade_pagamento=t["modalidade"]
            )
            # O auto_now_add deve preencher data_entrada automaticamente
            self.assertIsNotNone(estada.data_entrada)

            # Simular cálculo de tempo total e valor
            # Ajustar data_entrada manualmente para teste
            estada.data_entrada = t["entrada"]
            estada.save()
            valor = estada.calcular_valor_pagamento()
            tempo_total = estada.calcular_tempo_total()

            print(f"{t['desc']}: Tempo total={tempo_total}, Valor calculado={valor}")

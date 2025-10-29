from django.db import models

class ValorPagamento(models.Model):
    valor_hora = models.DecimalField(max_digits=6, decimal_places=2, default=5.00)

    def __str__(self):
        return f"R$ {self.valor_hora:.2f}"

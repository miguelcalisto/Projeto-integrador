from django.db import models

from clientes.models import Cliente


class Veiculo(models.Model):
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=50)
    cor = models.CharField(max_length=30)
    dono = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='veiculos', null=True , blank=True )


    def __str__(self):
        return f"{self.modelo} - {self.placa}"

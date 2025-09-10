from django.db import models

class Veiculo(models.Model):
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=50)
    cor = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.modelo} - {self.placa}"

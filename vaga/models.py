from django.db import models

class Vaga(models.Model):
    numero = models.IntegerField(unique=True)
    STATUS_CHOICES = [
        ('livre', 'Livre'),
        ('ocupada', 'Ocupada'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='livre'
    )

    def verificar_disponibilidade(self):
        return self.status == 'livre'

    def __str__(self):
        return f"Vaga {self.numero} - {self.get_status_display()}"

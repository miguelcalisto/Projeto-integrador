from django.db import models


class Vaga(models.Model):
    numero = models.IntegerField(unique=True, blank=True, null=True)

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

    def save(self, *args, **kwargs):
        if self.numero is None:
            # Pega o maior número existente e incrementa
            ultimo_numero = Vaga.objects.aggregate(models.Max('numero'))['numero__max']
            self.numero = 1 if ultimo_numero is None else ultimo_numero + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vaga {self.numero} - {self.get_status_display()}"

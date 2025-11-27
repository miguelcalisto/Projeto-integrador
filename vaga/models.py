from django.db import models
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy




class Vaga(models.Model):
    numero = models.IntegerField(unique=True,  editable=False, null=True)

    STATUS_CHOICES = [
        ('livre', 'Livre'),
        ('ocupada', 'Ocupada'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='livre'
    )

 

    def save(self, *args, **kwargs):
     

   
        if not self.numero:
            ultimo_numero = Vaga.objects.aggregate(models.Max('numero'))['numero__max']
            self.numero = 1 if ultimo_numero is None else ultimo_numero + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vaga {self.numero} - {self.get_status_display()}"






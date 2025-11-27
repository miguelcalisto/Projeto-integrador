from django.db import models

# Create your models here.
# limite de vagas
class ConfiguracaoVaga(models.Model):
    limite_maximo = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"Limite de vagas: {self.limite_maximo}"
    

from django.db import models


class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    class Meta:
        abstract = True


class Cliente(Pessoa):
    TIPO_CHOICES = (
        ('F', 'Pessoa Física'),
        ('J', 'Pessoa Jurídica'),
    )

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    # Campos específicos de PF
    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)

    # Campos específicos de PJ
    cnpj = models.CharField(max_length=18, blank=True, null=True)

    def __str__(self):
        if self.tipo == 'F':
            return f'{self.nome} (CPF: {self.cpf})'
        elif self.tipo == 'J':
            return f'{self.nome} (CNPJ: {self.cnpj})'
        return self.nome

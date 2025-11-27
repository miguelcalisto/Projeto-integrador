from django.core.exceptions import ValidationError
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

    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)

    cnpj = models.CharField(max_length=18, blank=True, null=True)

    def __str__(self):
        if self.tipo == 'F':
            return f'{self.nome} (CPF: {self.cpf})'
        elif self.tipo == 'J':
            return f'{self.nome} (CNPJ: {self.cnpj})'
        return self.nome
    

    def clean(self):
        if self.tipo == 'F' and not self.cpf:
            raise ValidationError("CPF é obrigatório para Pessoa Física.")
        if self.tipo == 'J' and not self.cnpj:
            raise ValidationError("CNPJ é obrigatório para Pessoa Jurídica.")
        






# class Cliente(models.Model):
#     nome = models.CharField(max_length=100)
#     email = models.EmailField()
#     telefone = models.CharField(max_length=20)

#     def __str__(self):
#         return self.nome



# class ClientePF(Cliente):
#     cpf = models.CharField(max_length=14)
#     data_nascimento = models.DateField()

#     def __str__(self):
#         return f"{self.nome} (CPF: {self.cpf})"

# class ClientePJ(Cliente):
#     cnpj = models.CharField(max_length=18)

#     def __str__(self):
#         return f"{self.nome} (CNPJ: {self.cnpj})"


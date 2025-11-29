from django.db import models
from clientes.models import Pessoa  
from stdimage import StdImageField


class Funcionario(Pessoa):
    tipo = models.CharField(max_length=1, default='F', editable=False)  
    data_nascimento = models.DateField()

    cpf_func = models.CharField(max_length=14, blank=True, null=True, verbose_name="CPF do Funcionário")
   
   
    foto = StdImageField(
        upload_to='funcionarios_fotos/',
        variations={
            'thumbnail': {"width": 100, "height": 100, "crop": True},
            'medium': {"width": 300, "height": 300, "crop": True},
        },
        blank=True,
        null=True,
    )


    def __str__(self):
        return f'{self.nome} '

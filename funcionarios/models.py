from django.db import models
from clientes.models import Pessoa  # Importa a classe abstrata Pessoa de Clientes
from stdimage import StdImageField


class Funcionario(Pessoa):
    tipo = models.CharField(max_length=1, default='F', editable=False)  # Fixando Pessoa Física não sei

    cpf = models.CharField(max_length=14)
    data_nascimento = models.DateField()
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

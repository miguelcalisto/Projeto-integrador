
from django.urls import path

from .views import ConfiguracaoVagaView

app_name = 'limite_vaga'

urlpatterns = [
    path('configuracao-vagas/', ConfiguracaoVagaView.as_view(), name='config-vaga'),

]

from django.urls import path
from .views import (
    VagaListView, VagaDetailView,
    VagaCreateView, VagaUpdateView, VagaDeleteView
)

app_name = 'vaga'

urlpatterns = [
    path('', VagaListView.as_view(), name='lista-vagas'),
    path('<int:pk>/', VagaDetailView.as_view(), name='detalhe-vaga'),
    path('criar/', VagaCreateView.as_view(), name='criar-vaga'),
    path('<int:pk>/editar/', VagaUpdateView.as_view(), name='editar-vaga'),
    path('<int:pk>/deletar/', VagaDeleteView.as_view(), name='deletar-vaga'),
]

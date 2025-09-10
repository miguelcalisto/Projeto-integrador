from django.urls import path
from .views import (
    VeiculoListView, VeiculoCreateView, VeiculoUpdateView, VeiculoDeleteView
)

urlpatterns = [
    path('veiculos/', VeiculoListView.as_view(), name='lista_veiculos'),
    path('veiculos/novo/', VeiculoCreateView.as_view(), name='criar_veiculo'),
    path('veiculos/<int:pk>/editar/', VeiculoUpdateView.as_view(), name='editar_veiculo'),
    path('veiculos/<int:pk>/deletar/', VeiculoDeleteView.as_view(), name='deletar_veiculo'),
]

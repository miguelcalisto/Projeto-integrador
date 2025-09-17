from django.urls import path
from .views import (
    FuncionarioListView,
    FuncionarioDetailView,
    FuncionarioCreateView,
    FuncionarioUpdateView,
    FuncionarioDeleteView,
)

app_name = 'funcionarios'

urlpatterns = [
    path('', FuncionarioListView.as_view(), name='lista-funcionarios'),
    path('novo/', FuncionarioCreateView.as_view(), name='criar-funcionario'),
    path('<int:pk>/', FuncionarioDetailView.as_view(), name='detalhe-funcionario'),
    path('<int:pk>/editar/', FuncionarioUpdateView.as_view(), name='editar-funcionario'),
    path('<int:pk>/deletar/', FuncionarioDeleteView.as_view(), name='deletar-funcionario'),
]

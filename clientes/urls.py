from django.urls import path
from .views import (
    ClienteListView,
    ClienteDetailView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,
)

urlpatterns = [
    path('', ClienteListView.as_view(), name='cliente_list'),
    path('novo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail'),
    path('<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('<int:pk>/deletar/', ClienteDeleteView.as_view(), name='cliente_delete'),
]

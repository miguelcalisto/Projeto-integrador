from django.urls import path
from .views import ValorHoraView, reset_valor

urlpatterns = [
    path('', ValorHoraView.as_view(), name='valor-hora'),
    path('reset/', reset_valor, name='valor-reset'),  # nova URL

]

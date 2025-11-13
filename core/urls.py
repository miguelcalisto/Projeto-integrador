# core/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    # home
    path('', views.index, name='index'),
    path('acesso-negado/', views.acesso_negado, name='acesso_negado'),

]

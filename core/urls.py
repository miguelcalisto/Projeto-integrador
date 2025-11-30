# core/urls.py
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    # home
    path('', views.IndexView.as_view(), name='index'),






    
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(
    template_name='login.html', 
    extra_context={'titulo': 'Alterar senha'},
    success_url='/'  
    ), name='alterar_senha'),

]

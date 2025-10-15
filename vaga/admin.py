from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vaga, ConfiguracaoVaga

admin.site.register(Vaga)
admin.site.register(ConfiguracaoVaga)

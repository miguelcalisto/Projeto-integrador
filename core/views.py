from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


# acho que ta com functions

@login_required
def index(request):
    return render(request, 'index.html')


from django.shortcuts import render

def acesso_negado(request):
    return render(request, 'acesso_negado.html', status=403)

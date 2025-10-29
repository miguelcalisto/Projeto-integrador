from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from .models import ValorPagamento

# ✅ Cria o registro automaticamente, se ainda não existir
class ValorHoraView(UpdateView):
    model = ValorPagamento
    fields = ['valor_hora']
    template_name = 'valorhora.html'
    success_url = reverse_lazy('valor-hora')

    def get_object(self):
        # Se não houver registro, cria um com valor padrão
        obj, created = ValorPagamento.objects.get_or_create(id=1, defaults={'valor_hora': 5.00})
        return obj


from django.shortcuts import redirect
from .models import ValorPagamento

def reset_valor(request):
    # Pega o primeiro (ou único) ValorPagamento
    valor = ValorPagamento.objects.first()
    if valor:
        valor.valor_hora = 5.00
        valor.save()
    return redirect('/valorpagamento/')  # volta para a lista

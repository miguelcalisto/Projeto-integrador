from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from limite_vaga.models import ConfiguracaoVaga




from django.views.generic import UpdateView

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class ConfiguracaoVagaView(PermissionRequiredMixin, LoginRequiredMixin,UpdateView):
    model = ConfiguracaoVaga
    fields = ['limite_maximo']
    template_name = 'configuracao_vaga.html'
    success_url = reverse_lazy('limite_vaga:config-vaga')

    permission_required = 'limite_vaga.change_limite_maximo'
    raise_exception = True  # 403 erro



    def get_object(self):
        obj, created = ConfiguracaoVaga.objects.get_or_create(id=1, defaults={'limite_maximo': 10})
        return obj

    def form_valid(self, form):

        limite_maximo = form.instance.limite_maximo

        messages.success(self.request, f'Limite máximo  {limite_maximo}  atualizado com sucesso!')
       

        return super().form_valid(form)

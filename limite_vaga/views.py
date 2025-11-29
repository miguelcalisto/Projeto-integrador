from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from limite_vaga.models import ConfiguracaoVaga




from django.views.generic import UpdateView

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from vaga.models import Vaga


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
        response = super().form_valid(form)

        limite = form.instance.limite_maximo
        total = Vaga.objects.count()
        
        messages.success(self.request, f"Limite definido para {limite} vagas.")

        if total < limite:
            criar = limite - total

            for _ in range(criar):
                Vaga.objects.create()

            messages.success(self.request, f"{criar} vagas criadas automaticamente!")

        elif total > limite:
                remover = total - limite

                excedentes = Vaga.objects.filter(status='livre').order_by('-numero')[:remover]
                excedentes_list = list(excedentes) 

                qtd = len(excedentes_list)

                for vaga in excedentes_list:
                    vaga.delete()

                messages.success(self.request, f"{qtd} vagas removidas automaticamente!")
         
        return response


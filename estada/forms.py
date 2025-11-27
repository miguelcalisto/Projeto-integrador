from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone

from vaga.models import Vaga
from .models import Estada

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone

from vaga.models import Vaga
from .models import Estada
from veiculo.models import Veiculo  

class EstadaForm(forms.ModelForm):
    class Meta:
        model = Estada
        fields = ['vaga', 'funcionario_responsavel', 'veiculo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'

        
        if self.instance.pk:
            self.fields['vaga'].disabled = True
            self.fields['vaga'].queryset = Vaga.objects.filter(pk=self.instance.vaga.pk)
        else:
            self.fields['vaga'].queryset = Vaga.objects.filter(status='livre')

        # Veículos
        veiculos_livres = Veiculo.objects.exclude(estadas__pago=False)
       

        if self.instance.pk:
            # edição: próprio veículo + veículos livres
            self.fields['veiculo'].queryset = veiculos_livres | Veiculo.objects.filter(pk=self.instance.veiculo.pk)
        else:
            # criar
            self.fields['veiculo'].queryset = veiculos_livres

  


class ConfirmarPagamentoForm(forms.ModelForm):  

    class Meta:
        model = Estada
        fields = ['modalidade_pagamento']
        

        def save(self, *args, **kwargs):
            estada = super().save(*args, **kwargs)
            if not estada.data_saida:
                estada.data_saida = timezone.now()
                estada.save()  
            return estada



        

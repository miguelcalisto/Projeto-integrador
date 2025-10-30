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
from veiculo.models import Veiculo  # supondo que você tenha esse model

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
        self.helper.add_input(Submit('submit', 'Salvar'))

        # Vagas
        if self.instance and self.instance.pk:
            self.fields['vaga'].disabled = True
            self.fields['vaga'].queryset = Vaga.objects.filter(pk=self.instance.vaga.pk)
        else:
            self.fields['vaga'].queryset = Vaga.objects.filter(status='livre')

        # Veículos
        veiculos_livres = Veiculo.objects.exclude(estadas__pago=False)
        if self.instance and self.instance.pk:
            # edição: inclui o próprio veículo + veículos livres
            self.fields['veiculo'].queryset = veiculos_livres | Veiculo.objects.filter(pk=self.instance.veiculo.pk)
        else:
            # criação: só veículos livres
            self.fields['veiculo'].queryset = veiculos_livres

    def clean(self):
        cleaned_data = super().clean()
        vaga = cleaned_data.get('vaga')
        veiculo = cleaned_data.get('veiculo')
        estada_atual = self.instance

        # Validação de vaga ocupada
        if vaga and vaga.status == 'ocupada':
            if not estada_atual.pk or estada_atual.vaga != vaga:
                raise forms.ValidationError(f"A vaga {vaga.numero} já está ocupada.")

        # Validação de veículo com estada ativa
        if veiculo:
            estadas_ativas = Estada.objects.filter(veiculo=veiculo, pago=False)
            if estada_atual.pk:
                estadas_ativas = estadas_ativas.exclude(pk=estada_atual.pk)
            if estadas_ativas.exists():
                raise forms.ValidationError(
                    f"O veículo {veiculo} já possui uma estada ativa. "
                    f"Finalize ou pague a estada antes de criar uma nova."
                )

        return cleaned_data


class ConfirmarPagamentoForm(forms.ModelForm):  # Mantido como na resposta anterior

    class Meta:
        model = Estada
        fields = ['modalidade_pagamento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if not instance.data_saida:
                instance.data_saida = timezone.now()  # Importe timezone de django.utils

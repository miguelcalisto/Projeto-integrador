from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone

from vaga.models import Vaga
from .models import Estada


class EstadaForm(forms.ModelForm):

    class Meta:
        model = Estada
        fields = ['vaga', 'funcionario_responsavel', 'veiculo']  # Excluídos: data_saida, valor_pagamento, tempo_total

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configuração do Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit', 'Salvar'))

        # Exibir apenas vagas com status "livre" OU a vaga já selecionada no formulário (se editar)
        if self.instance and self.instance.pk:
            # Inclui a vaga atual no queryset para poder editá-la
            self.fields['vaga'].queryset = Vaga.objects.filter(status='livre') | Vaga.objects.filter(
                pk=self.instance.vaga.pk)
        else:
            self.fields['vaga'].queryset = Vaga.objects.filter(status='livre')

    def clean(self):
        cleaned_data = super().clean()
        vaga = cleaned_data.get('vaga')

        estada_atual = self.instance

        if vaga and vaga.status == 'ocupada':
            if not estada_atual.pk or estada_atual.vaga != vaga:
                raise forms.ValidationError(f"A vaga {vaga.numero} já está ocupada.")

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
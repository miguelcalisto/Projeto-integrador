from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Vaga

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['status']  # só o campo editável

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se for edição (ou seja, a vaga já existe), mostrar o campo 'numero' como readonly
        if self.instance and self.instance.pk:
            self.fields['numero'] = forms.IntegerField(
                initial=self.instance.numero,
                label="Número da Vaga",
                disabled=True,     # torna o campo somente leitura
                required=False,
            )

        # Crispy Forms config
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.add_input(Submit('submit', 'Salvar'))

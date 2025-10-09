from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Veiculo

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'cor', 'dono']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        # Você pode deixar o botão aqui, ou colocar no template
        self.helper.add_input(Submit('submit', 'Salvar'))

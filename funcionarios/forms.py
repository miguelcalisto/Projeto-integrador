# funcionarios/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'  # ou 'get', dependendo do caso
        self.helper.form_class = 'form-horizontal'  # classe CSS do formulário
        self.helper.label_class = 'col-md-2'  # classe para os labels
        self.helper.field_class = 'col-md-8'  # classe para os campos
        self.helper.add_input(Submit('submit', 'Salvar'))

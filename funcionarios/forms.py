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
        self.helper.form_method = 'post'  
        self.helper.form_class = 'form-horizontal'  
        self.helper.label_class = 'col-md-2'  
        self.helper.field_class = 'col-md-8'  
# funcionarios/forms.py
from django import forms
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'



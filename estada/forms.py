from django import forms
from .models import Estada

class EstadaForm(forms.ModelForm):
    class Meta:
        model = Estada
        fields = '__all__'

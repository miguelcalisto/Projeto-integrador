from django import forms

from vaga.models import Vaga
from .models import Estada

class EstadaForm(forms.ModelForm):
    class Meta:
        model = Estada
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Exibir apenas vagas com status "livre"
    #     self.fields['vaga'].queryset = Vaga.objects.filter(status='livre')


    def clean(self):
        cleaned_data = super().clean()
        vaga = cleaned_data.get('vaga')

        if vaga and vaga.status == 'ocupada':
            raise forms.ValidationError(f"A vaga {vaga.numero} já está ocupada.")

        return cleaned_data

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Estada
from .forms import EstadaForm  # Você precisará criar esse form

class EstadaListView(ListView):
    model = Estada
    template_name = 'listar-estada.html'       # Ajuste o caminho conforme seu template
    context_object_name = 'estadas'


class EstadaDetailView(DetailView):
    model = Estada
    template_name = 'detalhe-estada.html'
    context_object_name = 'estada'


class EstadaCreateView(CreateView):
    model = Estada
    form_class = EstadaForm
    template_name = 'criar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')  # Ajuste o namespace e nome da url

    def form_valid(self, form):
        response = super().form_valid(form)

        # Depois de salvar a Estada, atualize o status da vaga vinculada
        vaga = self.object.vaga
        if vaga:
            vaga.status = 'ocupada'  # Marca como ocupada ao criar estada
            vaga.save()

        return response


class EstadaUpdateView(UpdateView):
    model = Estada
    form_class = EstadaForm
    template_name = 'editar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')


# altera para livre quando a vaga eh att
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #
    #     vaga = self.object.vaga
    #     if vaga and self.object.data_saida:
    #         vaga.status = 'livre'  # Marca vaga como livre ao finalizar estada
    #         vaga.save()
    #
    #     return response


class EstadaDeleteView(DeleteView):
    model = Estada
    template_name = 'deletar-estada.html'
    success_url = reverse_lazy('estada:lista-estadas')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        vaga = self.object.vaga

        if vaga:
            print(f'Atualizando status da vaga {vaga.pk} para livre antes de deletar a estada {self.object.pk}')
            vaga.status = 'livre'
            vaga.save()

        response = super().delete(request, *args, **kwargs)
        print(f'Estada {self.object.pk} deletada com sucesso.')
        return response




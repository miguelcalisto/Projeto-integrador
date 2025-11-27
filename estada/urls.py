from django.urls import path
from .views import (
    ConfirmarPagamentoView,
    EstadaListView,
    EstadaDetailView,
    EstadaCreateView,
    EstadaUpdateView,
    EstadaDeleteView,
    ExportarPagamentosPdfView,
    ExportarPagamentosTxtView,
    #ExportarPagamentosTxtView,
    HistoricoPagamentosView,PagamentosGraficoView
)

app_name = 'estada'  

urlpatterns = [
    path('', EstadaListView.as_view(), name='lista-estadas'),
    path('<int:pk>/', EstadaDetailView.as_view(), name='detalhe-estada'),
    path('criar/', EstadaCreateView.as_view(), name='criar-estada'),
    path('editar/<int:pk>/', EstadaUpdateView.as_view(), name='editar-estada'),
    path('deletar/<int:pk>/', EstadaDeleteView.as_view(), name='deletar-estada'),

    path('confirmar/<int:pk>/', ConfirmarPagamentoView.as_view(), name='confirmar-pagamento'),


   
    
    path('historico/', HistoricoPagamentosView.as_view(), name='historico-pagamentos'),


    path('exportar-pagamentos-txt/', ExportarPagamentosTxtView.as_view(), name='exportar_pagamentos_txt'),


    path('dashboard-pagamentos/', PagamentosGraficoView.as_view(), name='dashboard-pagamentos'),

    path('exportar-pagamentos/pdf/',ExportarPagamentosPdfView.as_view(),name='exportar-pagamentos-pdf'),

]

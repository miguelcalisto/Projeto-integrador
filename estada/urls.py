from django.urls import path
from .views import (
    EstadaListView,
    EstadaDetailView,
    EstadaCreateView,
    EstadaUpdateView,
    EstadaDeleteView, confirmar_pagamento, historico_pagamentos, exportar_pagamentos_txt, exportar_pagamentos_pdf,
)

app_name = 'estada'  # Namespace para o app

urlpatterns = [
    path('', EstadaListView.as_view(), name='lista-estadas'),
    path('<int:pk>/', EstadaDetailView.as_view(), name='detalhe-estada'),
    path('criar/', EstadaCreateView.as_view(), name='criar-estada'),
    path('editar/<int:pk>/', EstadaUpdateView.as_view(), name='editar-estada'),
    path('deletar/<int:pk>/', EstadaDeleteView.as_view(), name='deletar-estada'),
    path('<int:pk>/confirmar-pagamento/', confirmar_pagamento, name='confirmar-pagamento'),
    path('estada/<int:pk>/confirmar-pagamento/', confirmar_pagamento, name='confirmar_pagamento'),
    path('historico-pagamentos/', historico_pagamentos, name='historico-pagamentos'),
    path('exportar-pagamentos/', exportar_pagamentos_txt, name='exportar-pagamentos'),
    path('exportar-pagamentos-pdf/', exportar_pagamentos_pdf, name='exportar-pagamentos-pdf'),

]

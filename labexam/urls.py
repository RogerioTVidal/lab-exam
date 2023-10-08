from django.urls import path
from . import views

# request -  Solicitação de exames
# order - Pedido de exames

urlpatterns = [
    path('request-exam/', views.fRequestExams, name='request'),
    path('order-exam/', views.fOrderExams, name='order'),
    path('close-request/', views.fCloseRequest, name="closeRequest"),
]
from django.urls import path
from . import views

# order - Pedido de exames um order tem vários request
# request -  Solicitação de exames

urlpatterns = [
    path('request-exam/', views.fRequestExams, name='request'),
    path('close-request/', views.fCloseRequest, name="closeRequest"),
    path('order-management/', views.fOrderManagement, name="orderManagement"),
    path('order-cancel/<int:order_id>', views.fOrderCancel, name='orderCancel'),
    
]
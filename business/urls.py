from django.urls import path
from . import views

urlpatterns = [
    path('client-management/', views.fClientManagement, name="clientManagement"),
    path('client/<int:client_id>', views.fCliente, name="client"),
    path('cliente-exam/<int:exam_id>', views.fClientExam, name="clienteExam"),
    path('proxy-pdf/<int:exam_id>', views.fProxyPdf, name="proxyPdf"),
]
from django.urls import path
from . import views

# order - Pedido de exames um order tem vários request
# request -  Solicitação de exames

urlpatterns = [
    path('request-exam/', views.fRequestExams, name='request'),
    path('close-request/', views.fCloseRequest, name="closeRequest"),
    path('order-management/', views.fOrderManagement, name="orderManagement"),
    path('order-cancel/<int:order_id>', views.fOrderCancel, name='orderCancel'),
    path('exam-management/', views.fExamManagement, name="examManagement"),
    path('open-exame/<int:exam_id>', views.fOpenExam, name="openExam"),
    path('require-password/<int:exam_id>', views.fRequirePassword, name="requirePassword"),
    path('create-doctor-access/', views.fCreateDoctorAccess, name="createDoctorAccess"),
    path('doctor-access/<str:token>', views.fDoctorAccess, name="doctorAccess"),
]
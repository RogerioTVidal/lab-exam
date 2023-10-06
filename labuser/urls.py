from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.fRegister, name='register'),
    path('login/', views.fLogin, name='login')
]
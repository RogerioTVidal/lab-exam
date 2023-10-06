from django.shortcuts import render

# Create your views here.

def fRegister(request):
    return render(request, 'register.html')
    
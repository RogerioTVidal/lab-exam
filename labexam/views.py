from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.contrib import messages
from .models import exam_type


@login_required
def fRequestExams(request):
    typeExam = exam_type.objects.all()

    if request.method == 'GET':
        #return HttpResponse('Exams GET')
        return render(request, 'request-exam.html', {'typeExam': typeExam})
    elif request.method == 'POST':
        return HttpResponse('Exams POST')

# Create your views here.
def fOrderExams(request):
    if request.method == 'GET':
        #return HttpResponse('Order GET')
        return render(request, 'order-exam.html')
    elif request.method == 'POST':
        return HttpResponse('Order POST')


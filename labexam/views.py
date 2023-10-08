from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.contrib import messages
from .models import exam_type, exam_order, exam_request
from datetime import datetime


# request -  Solicitação de exames
# order - Pedido de exames

@login_required
def fRequestExams(request):
    typeExam = exam_type.objects.all().order_by('name').values()
##  for i in typeExam:
##      print(i.name)
##      print(i.price)
##      print('-' * 10)

    if request.method == 'GET':
        #return HttpResponse('Exams GET')
        #print(User)
        return render(request, 'request-exam.html', {'typeExam': typeExam})
    elif request.method == 'POST':
        exam_ids = request.POST.getlist('exams')
        requested_exams = exam_type.objects.filter(id__in=exam_ids).order_by('name')

        #preco_total = solicitacao_exames.aggregate(total=Sum('preco'))['total']

        total = 0

        for exam in requested_exams:
            if exam.avaliable:
                total += exam.price

        return render(request, 'request-exam.html', {'requested_exams': requested_exams, 'total': total, 'typeExam': typeExam})

@login_required
def fOrderExams(request):
    if request.method == 'GET':
        #return HttpResponse('Order GET')
        return render(request, 'order-exam.html')
    elif request.method == 'POST':
        return HttpResponse('Order POST')

@login_required
def fCloseRequest(request):
    exams_ids = request.POST.getlist('examsHidden')
    exams_type = exam_type.objects.filter(id__in=exams_ids)

    exam_order_temp = exam_order(
        user = request.user,
        date = datetime.now()
    )

    exam_order_temp.save()

    for examTemp in exams_type:
        #print(examTemp.id)
        exam_request_temp = exam_request(
            user=request.user,
            exam=examTemp,
            status="R"
        )
  
        exam_request_temp.save()
        exam_order_temp.exam.add(exam_request_temp)

    exam_order_temp.save()

    messages.add_message(request, constants.SUCCESS, 'Exams added successfuly')
    return redirect('/exam/ver_pedidos/')
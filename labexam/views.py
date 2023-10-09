from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.contrib import messages
from .models import exam_type, exam_order, exam_request, doctor_access
from datetime import datetime
from secrets import token_urlsafe
from django.utils import timezone
from datetime import timedelta


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

    messages.add_message(request, constants.SUCCESS, 'Exams added successfuly.')
    return redirect('/exam/order-management/')

@login_required
def fOrderManagement(request):
    if request.method == 'GET':
        exam_order_temp = exam_order.objects.filter(user=request.user)
        #return HttpResponse('Entrou')
        return render(request, 'order-management.html', {'ordered_exams': exam_order_temp})

@login_required
def fOrderCancel(request, order_id):
    exam_order_temp = exam_order.objects.get(id=order_id)
    if not exam_order_temp.user == request.user:
        messages.add_message(request, constants.ERROR, 'Not your order.')
        return redirect('/exam/order-management/')    
    
    exam_order_temp.scheduled = False
    exam_order_temp.save()

    #return HttpResponse('Entrou')
    messages.add_message(request, constants.SUCCESS, 'Exams canceled successfuly.')

    return redirect('/exam/order-management/')

@login_required
def fExamManagement(request):
    exam_request_temp = exam_request.objects.filter(user=request.user)
    return render(request, 'exam-management.html', {'exam_request': exam_request_temp})

@login_required
def fOpenExam(request, exam_id):
    exam_request_temp = exam_request.objects.get(id=exam_id)
    #return HttpResponse(exam_id)
    if not exam_request_temp.user == request.user:
        messages.add_message(request, constants.ERROR, 'Not your exam.')
        return redirect('/exam/exam-management/')    
  
    if not exam_request_temp.password_required:
        # verificar se o pdf existe
        return redirect(exam_request_temp.result.url)
    else:
        return redirect(f'/exam/require-password/{exam_id}')
    
@login_required
def fRequirePassword(request, exam_id):
    #return HttpResponse(exam_id)
    exam_request_temp = exam_request.objects.get(id=exam_id)

    if request.method == "GET":
        return render(request, 'require-password.html', {'exam_request': exam_request_temp})
    elif request.method == "POST":
        if not exam_request_temp.user == request.user:
            messages.add_message(request, constants.ERROR, 'Not your exam.')
            return redirect('/exam/exam-management/')    
    
        pwd = request.POST.get('password')
        if pwd == exam_request_temp.password:
            return redirect(exam_request_temp.result.url)
        else:
            messages.add_message(request, constants.ERROR, 'Invalid password')
            return redirect(f'/exam/require-password/{exam_id}')

@login_required
def fCreateDoctorAccess(request):
    if request.method == "GET":
        doctor_access_temp = doctor_access.objects.filter(user=request.user)
        return render(request, 'create-doctor-access.html', {'doctor_access': doctor_access_temp})
    elif request.method == "POST":
        identification_temp = request.POST.get('identification')
        access_time_temp = request.POST.get('access_time')
        inicial_exam_date_temp = request.POST.get("inicial_exam_date")
        final_exam_date_temp = request.POST.get("final_exam_date")

        doctor_access_temp = doctor_access(
            user = request.user,
            identification = identification_temp,
            access_time = access_time_temp,
            inicial_exam_date = inicial_exam_date_temp,
            final_exam_date = final_exam_date_temp,
            created = datetime.now(),
            token = token_urlsafe(6)
        )

        doctor_access_temp.save()

        messages.add_message(request, constants.SUCCESS, 'Access created successfuly')
        return redirect('/exam/create-doctor-access')    
    

def fDoctorAccess(request, token):
    doctor_access_temp = doctor_access.objects.get(token=token)
    Expired = False

    if timezone.now() > (doctor_access_temp.created + timedelta(hours=doctor_access_temp.access_time)):
        Expired = True
        
    if Expired:
        messages.add_message(request, constants.ERROR, 'Link expired!')
        return redirect('/user/login')

    order_temp = exam_order.objects.filter(date__gte = doctor_access_temp.inicial_exam_date).filter(date__lte = doctor_access_temp.final_exam_date).filter(user=doctor_access_temp.user)

    return render(request, 'doctor-access.html', {'orders': order_temp})
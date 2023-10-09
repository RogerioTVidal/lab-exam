from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.admin.views.decorators import staff_member_required
from .models import exam_request
from django.http import FileResponse


@staff_member_required 
def fClientManagement(request):
    client = User.objects.filter(is_staff=False)

    full_name = request.GET.get('name')
    email = request.GET.get('email')

    if email:
        client = client.filter(email__contains = email)
    if full_name:
        client = client.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(full_name__contains=full_name)


    return render(request, 'cliente-management.html', {'clients': client, 'full_name': full_name, 'email': email})


@staff_member_required 
def fClient(request, client_id):
    client_temp = User.objects.get(id=client_id)
    exams = exam_request.objects.filter(usuario=client_temp)
    return render(request, 'client.html', {'client': client_temp, 'exams': exams})

@staff_member_required 
def fClientExam(request, exam_id):
    exam_temp = exam_request.objects.get(id=exam_id)
    return render(request, 'client-exam.html', {'exams': exam_temp})


@staff_member_required 
def fProxyPdf(request, exam_id):
    exam_temp = exam_request.objects.get(id=exam_id)

    response = exam_temp.result.open()
    return FileResponse(response)
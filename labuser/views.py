from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.

def fRegister(request):
    #print(request.POST)
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        userName = request.POST.get('userName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
    
        #return HttpResponse(f'{firstName} - {lastName} - {email}')

        if not password == confirmPassword:
            messages.add_message(request, constants.ERROR, 'Password and confirmation are not equal.')
            return redirect('/user/register')
        if len(password) < 6:
            messages.add_message(request, constants.ERROR, 'Password must have more than 5 characters.')
            return redirect('/user/register')
        
        try:
            # Username must be unique!
            user = User.objects.create_user(
                first_name = firstName,
                last_name = lastName,
                username = userName,
                email = email,
                password = password,
            )
            messages.add_message(request, constants.SUCCESS, 'Data saved successfuly')
        except:
            messages.add_message(request, constants.ERROR, 'Internal error. Please contact admin.')
            return redirect('/user/register')

        return HttpResponse('Passou')
    
def fLogin(request):
    #return HttpResponse('Login')
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
    
    if user:
        login(request, user)
        return redirect('/')
    else:
        messages.add_message(request, constants.ERROR, 'Invalid user or password')
        return redirect('/user/login')
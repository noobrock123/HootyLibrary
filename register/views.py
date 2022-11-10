
from django.shortcuts import render, redirect
from django.urls import reverse
from database_models.models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from MAIN_APP import views as main_app
# Create your views here.


def register(request):
    print(request.method)
    if request.user.is_authenticated:
        return redirect('MAIN_APP:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error('password do not match')
            return render(request, 'register/templates/sign_up_and_in/sign_up.html', {})
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('MAIN_APP:home')
    return render(request, 'sign_up_and_in/signup.html', {})

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('name_email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            print("logged in!")
            login(request, user)
            return redirect('MAIN_APP:home')
    if request.method == 'GET':
        return render(request, 'sign_up_and_in/signin.html')

# def home(request):
#     print(request.user)
#     context={'user':request.user}
#     return render(request, 'templates.html',context)
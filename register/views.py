
from django.shortcuts import render, redirect
from django.urls import reverse
from database_models.models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from MAIN_APP import views as main_app
# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect('MAIN_APP:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        try:
            User.objects.get(username=username)
            messages.error(request,'This username is already exists')
            return render(request, 'register/templates/sign_up_and_in/signup.html', {})
        except:
            pass
        try:
            User.objects.get(email=email)
            messages.error(request, 'This email is already exists')
            return render(request, 'register/templates/sign_up_and_in/signup.html', {})
        except:
            pass
        if password != confirm_password:
            messages.error(request, message='password do not match')
            return render(request, 'sign_up_and_in/signup.html', {})
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
        except ValidationError:
            return redirect('register:regis')

        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request,f'{user.username}:{user.alias_name} create user successful')
        return redirect('MAIN_APP:home')
    return render(request, 'register/templates/sign_up_and_in/signup.html', {})

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('name_email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('MAIN_APP:home')
    return render(request, 'sign_up_and_in/signin.html')


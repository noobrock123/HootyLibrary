
from django.shortcuts import render, redirect
from database_models.models import *
from django.contrib.auth import login
from django.contrib import messages
from MAIN_APP import views as main_app
# Create your views here.
def register(request):
    print(request.method)
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error('password do not match')
            return render(request, 'register/templates/sign_up_and_in/sign_up.html', {})
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        login(request, user)
        return redirect('/')
    return render(request, 'register/templates/sign_up_and_in/sign_up.html', {})
# def home(request):
#     print(request.user)
#     context={'user':request.user}
#     return render(request, 'templates.html',context)
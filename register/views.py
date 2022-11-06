
from django.shortcuts import render, redirect
from django.urls import reverse
from database_models.models import *
from django.contrib.auth import login, authenticate

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
        gender=request.POST.get('gender')
        age=request.POST.get('age')
        occupation=request.POST.get('occupation')
        bio=request.POST.get('bio')
        social_link=request.POST.get('social_link')
        donation_link=request.POST.get('donation_link')
        is_staff=request.POST.get('is_staff')
        is_active=request.POST.get('is_active')
        profile_pic=request.POST.get('profile_pic')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            gender=gender,
            age=age,
            occupation=occupation,
            bio=bio,
            social_link=social_link,
            donation_link=donation_link,
            is_staff=is_staff if is_staff else User._meta.get_field('is_staff').get_default(),
            is_active=is_active if is_active else User._meta.get_field('is_active').get_default(),
            profile_pic=profile_pic,
        )
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'register/templates/sign_up_and_in/sign_up.html', {})

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('MAIN_APP:home')
    return render(request, 'sign_up_and_in/sign_in.html')

# def home(request):
#     print(request.user)
#     context={'user':request.user}
#     return render(request, 'templates.html',context)
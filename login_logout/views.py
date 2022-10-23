from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'templates/templates.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'login_logout/login.html', {
                'message': 'Invalid credentials.'
            })
    return render(request, 'login_logout/home.html')

def user_logout(request):
    logout(request)
    return render(request, 'login_logout/login.html', {
        'message': 'You are logged out.'
    })
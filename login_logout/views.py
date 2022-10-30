from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

# def home(request):
#     if not request.user.is_authenticated:
#         return redirect('/login')   
#     return render(request, 'homepage/homepage.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')   
        else:
            return render(request, 'login_logout/login.html')
    return render(request, 'homepage/homepage.html')

def user_logout(request):
    logout(request)
    return redirect('/') 

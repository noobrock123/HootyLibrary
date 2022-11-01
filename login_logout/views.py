from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')  
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        
    return render(request, 'register/templates/sign_up_and_in/sign_in.html', {})

def user_logout(request):
    logout(request)
    return redirect('/') 
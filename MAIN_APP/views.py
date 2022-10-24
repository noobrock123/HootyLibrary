from django.shortcuts import render, redirect
from django.urls import path, include

# Create your views here.
def index(request):
    return render(request, 'homepage/homepage.html')

def about(request):
    return render(request, 'hooty_library/about/about.html')
from django.shortcuts import render, redirect
from django.urls import path, include
from database_models.models import Book
from django.http import HttpResponse
from django.template import loader
from database_models.models import Book

# Create your views here.

def index(request):
    return render(request, 'homepage/homepage.html')

def about(request):
    return render(request, 'about/about.html')

def book(request):
    return render(request, )

def searchbar(request):
    if request.method == "GET":
        q = request.GET.get('q')
        if q:
            book = Book.objects.filter(book_name__icontains=q)
            return render(request, 'book_views/index.html', {'book':book})
        else:
            book = Book.objects.all()
            print("no information")
            return render(request, 'homepage/homepage.html')

def testing(request):
  mybook = Book.objects.all().values()
  template = loader.get_template('template.html')
  context = {
    'mybooks': mybook,
  }
  return HttpResponse(template.render(context, request))

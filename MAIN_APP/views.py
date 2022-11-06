from django.shortcuts import render, redirect
from django.urls import path, include, reverse
from database_models.models import Book
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from database_models.models import Book
from django.contrib.auth import logout

# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, 'homepage/homepage.html',
        {'is_user_authenticated': request.user.is_authenticated,
        'user': request.user})

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

def create_book(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect('regitser:log_in')

def sign_out(request):
    if request.method == "GET":
        logout(request)
        return HttpResponseRedirect(reverse('MAIN_APP:home'))

def testing(request):
  mybook = Book.objects.all().values()
  template = loader.get_template('template.html')
  context = {
    'mybooks': mybook,
  }
  return HttpResponse(template.render(context, request))

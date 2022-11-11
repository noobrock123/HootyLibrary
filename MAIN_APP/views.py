from django.shortcuts import render, redirect
from django.urls import path, include, reverse
from database_models.models import Book
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from database_models.models import Book
from django.contrib.auth import logout

# Create your views here.
def index(request):
    img = Book.objects.values_list('thumbnail')
    bookname = Book.objects.all().values()
    context = {
        'booknames': bookname,
    }
    #return render(request, 'homepage/homepage.html', context)
    if request.method == "GET":
        q = request.GET.get('q')
        checkbook = Book.objects.filter(book_name__iexact=q)
        if checkbook:
            book = Book.objects.get(book_name=q)
            return render(request, 'book_views/index.html', {'book':book, 'message': '',})
        else:
            return render(request, 'homepage/homepage.html', {
                'message': 'no information', 'is_user_authenticated': request.user.is_authenticated,
                'user': request.user, 'booknames': bookname})
        return render(request, 'homepage/homepage.html',
        {'is_user_authenticated': request.user.is_authenticated,
        'user': request.user, 'booknames': bookname},)

def about(request):
    return render(request, 'about/about.html')

def book(request):
    return render(request, 'book_views/index.html')

def searchbar(request):
    if request.method == "GET":
        q = request.GET.get('q')
        checkbook = Book.objects.filter(book_name__iexact=q)
        if checkbook:
            book = Book.objects.get(book_name=q)
            return render(request, 'book_views/index.html', {'book':book})
        else:
            print("no information")
            return render(request, 'homepage/homepage.html', {'message': 'no information'})

def create_book(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect('regitser:log_in')
        else:
            return render(request, 'book_views/create_book.html' )

def edit_profile(request):
    user_id = request.user.user_id
    return redirect('userProfile:editProfile', user_id)

def sign_out(request):
    if request.method == "GET":
        logout(request)
        return HttpResponseRedirect(reverse('MAIN_APP:home'))

def testing(request):
  mybook = Book.objects.all().values()
  template = loader.get_template('test.html')
  context = {
    'mybooks': mybook,
  }
  return HttpResponse(template.render(context, request))

def menu(request, id):
    name = Book.objects.all().values()
    context = {
        'names': name,
    }
    if id == 0:
        return render(request, 'homepage/menu.html', {'m':'Undiscoveredy'})
    if id == 1:
        return render(request, 'homepage/menu.html', {'m':'Popular today'})
    if id == 2:
        return render(request, 'homepage/menu.html', {'m':'Popular this week'})
    if id == 3:
        return render(request, 'homepage/menu.html', {'m':'Highest rating today'})
    if id == 4:
        return render(request, 'homepage/menu.html', {'m':'Highest rating this week'})
    if id == 5:
        return render(request, 'homepage/menu.html', {'m':'Recently update'})
    return render(request, 'homepage/menu.html', context)

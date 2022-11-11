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
    books = Book.objects.all()
    latest_book = books.order_by('-date_created')[:8]
    topics = {
        'Latest Books':latest_book,
    }
    #return render(request, 'homepage/homepage.html', context)
    if request.method == "GET":
        return render(request, 'homepage/homepage.html',
        {'is_user_authenticated': request.user.is_authenticated,
        'user': request.user, #'books': latest_book,
        'topics': topics,},)

def about(request):
    return render(request, 'about/about.html')

def book(request):
    return render(request, 'book_views/index.html')

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

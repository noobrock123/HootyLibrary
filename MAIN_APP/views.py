from django.shortcuts import render, redirect
from django.urls import path, include, reverse
from database_models.models import Book
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from database_models.models import Book
from django.contrib.auth import logout

# Create your views here.
def index(request):
    books = Book.objects.all()
    latest_book = books.order_by('-date_created').values()[:8]
    topics = {
        'Latest Books':latest_book,
    }
    
    if request.method == "GET":  
        search_query = request.GET.get('query')
        if search_query:
            SearchCheck = Book.objects.filter(book_name__contains=search_query)
            if SearchCheck:
                book = Book.objects.all().filter(book_name__startswith=search_query)
                topics = {
                    'search':book,
                }
                return render(request, 'homepage/homepage.html', {'topics':topics})

        return render(request, 'homepage/homepage.html',
            {'is_user_authenticated': request.user.is_authenticated,
            'user': request.user, #'books': latest_book,
            'topics': topics,},)


def about(request):
    return render(request, 'about/about.html')

def book(request):
    return render(request, 'book_views/index.html')

def create_book(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect('register:log_in')
        else:
            return render(request, 'book_views/create_book.html' )

def edit_profile(request):
    user_id = request.user.user_id
    return redirect('userProfile:editProfile', user_id)

def sign_out(request):
    if request.method == "GET":
        logout(request)
        return HttpResponseRedirect(reverse('MAIN_APP:home'))

def Undiscoveredy(request):
    books = Book.objects.all()
    Undiscoveredy = books.order_by('-date_created').values()[:8]
    topics = {
        'Undiscoveredy':Undiscoveredy,
    }
    if request.method == "GET":  
        search_query = request.GET.get('query')
        if search_query:
            SearchCheck = Book.objects.filter(book_name__contains=search_query)
            if SearchCheck:
                book = Book.objects.all().filter(book_name__startswith=search_query)
                topics = {
                    'search':book,
                }
                return render(request, 'homepage/homepage.html', {'topics':topics})
    return render(request, 'homepage/homepage.html', {'topics':topics})

def Popular_today(request):
    books = Book.objects.all()
    Popular_today = books.order_by('-date_created').values()[:8]
    topics = {
        'Popular today':Popular_today,
    }
    if request.method == "GET":  
        search_query = request.GET.get('query')
        if search_query:
            SearchCheck = Book.objects.filter(book_name__contains=search_query)
            if SearchCheck:
                book = Book.objects.all().filter(book_name__startswith=search_query)
                topics = {
                    'search':book,
                }
                return render(request, 'homepage/homepage.html', {'topics':topics})
    return render(request, 'homepage/homepage.html', {'topics':topics})

def Popular_week(request):
    books = Book.objects.all()
    Popular_week = books.order_by('-date_created').values()[:8]
    topics = {
        'Popular this week':Popular_week,
    }
    if request.method == "GET":  
        search_query = request.GET.get('query')
        if search_query:
            SearchCheck = Book.objects.filter(book_name__contains=search_query)
            if SearchCheck:
                book = Book.objects.all().filter(book_name__startswith=search_query)
                topics = {
                    'search':book,
                }
                return render(request, 'homepage/homepage.html', {'topics':topics})
    return render(request, 'homepage/homepage.html', {'topics':topics})

def Highest_rating_today(request):
    books = Book.objects.all()
    Highest_rating_today = books.order_by('-date_created').values()[:8]
    topics = {
        'Highest rating today':Highest_rating_today,
    }
    if request.method == "GET":  
        search_query = request.GET.get('query')
        if search_query:
            SearchCheck = Book.objects.filter(book_name__contains=search_query)
            if SearchCheck:
                book = Book.objects.all().filter(book_name__startswith=search_query)
                topics = {
                    'search':book,
                }
                return render(request, 'homepage/homepage.html', {'topics':topics})
    return render(request, 'homepage/homepage.html', {'topics':topics})

def Highest_rating_week(request):
    books = Book.objects.all()
    Highest_rating_week = books.order_by('-date_created').values()[:8]
    topics = {
        'Highest rating this week':Highest_rating_week,
    }
    if request.method == "GET":  
        search_query = request.GET.get('query')
        if search_query:
            SearchCheck = Book.objects.filter(book_name__contains=search_query)
            if SearchCheck:
                book = Book.objects.all().filter(book_name__startswith=search_query)
                topics = {
                    'search':book,
                }
                return render(request, 'homepage/homepage.html', {'topics':topics})
    return render(request, 'homepage/homepage.html', {'topics':topics})

def Recently(request):
    books = Book.objects.all()
    Recently = books.order_by('-date_created').values()[:8]
    topics = {
        'Recently':Recently,
    }
    if request.method == "GET":  
        search_query = request.GET.get('query')
        if search_query:
            SearchCheck = Book.objects.filter(book_name__contains=search_query)
            if SearchCheck:
                book = Book.objects.all().filter(book_name__startswith=search_query)
                topics = {
                    'search':book,
                }
                return render(request, 'homepage/homepage.html', {'topics':topics})
    return render(request, 'homepage/homepage.html', {'topics':topics})

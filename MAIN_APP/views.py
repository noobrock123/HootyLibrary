from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import include, path, reverse

from database_models.models import *
from database_models.models import Book
from django.utils import timezone
from datetime import datetime, timedelta



# Create your views here.
def index(request):
    books = Book.objects.all()
    latest_book = books.order_by('-date_created').values()[:8]
    topics = {
        'Latest Books':latest_book,
    }
    
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
        query = request.GET.get('query')
        checkbook = Book.objects.filter(book_name__iexact=query)
        if checkbook:
            book = Book.objects.filter(book_name__startswith=query).values()
            return render(request, 'search.html', {'book':book})
        else:
            print("no information")
            return render(request, 'homepage/homepage.html', {'message': 'no information'})

def edit_profile(request):
    user_id = request.user.user_id
    return redirect('userProfile:editProfile', user_id)

def sign_out(request):
    if request.method == "GET":
        logout(request)
        return HttpResponseRedirect(reverse('MAIN_APP:home'))

def menu(request, id):
    print(get_Popular_today())
    books = Book.objects.all()
    Undiscoveredy = books.order_by('-date_created').values()[:8]
    Popular_today = books.order_by('-date_created').values()[:8]
    Popular_week = books.order_by('-date_created').values()[:8]
    Highest_rating_today = books.order_by('-date_created').values()[:8]
    Highest_rating_week = books.order_by('-date_created').values()[:8]
    Recently = books.order_by('-date_created').values()[:8]
    if id == 0:
        return render(request, 'homepage/menu.html', {'m':'Undiscoveredy', 'context':Undiscoveredy, })
    if id == 1:
        return render(request, 'homepage/menu.html', {'m':'Popular today', 'context':Popular_today, })
    if id == 2:
        return render(request, 'homepage/menu.html', {'m':'Popular this week', 'context':Popular_week, })
    if id == 3:
        return render(request, 'homepage/menu.html', {'m':'Highest rating today', 'context':Highest_rating_today, })
    if id == 4:
        return render(request, 'homepage/menu.html', {'m':'Highest rating this week', 'context':Highest_rating_week, })
    if id == 5:
        return render(request, 'homepage/menu.html', {'m':'Recently update', 'context':Recently, })
    context = {}
    return render(request, 'homepage/menu.html', context)
def get_Undiscoveredy():
    all_book = Book.objects.values_list('book_id',flat=True).distinct()
    readed_book = Read.objects.values_list('book_refer_id',flat=True).distinct()
    no_read_book = all_book.difference(readed_book)
    return no_read_book.first()
def get_Popular_today():
    read_today = Read.objects.filter(book_read_latest_time__gte=timezone.now() - timedelta(days=1))
    book_today = read_today.values_list('book_refer_id',flat=True).distinct()
    popular_today = sorted([(i ,read_today.filter(book_refer=i).count()) for i in book_today], key= lambda x: x[1])
    return popular_today
def get_Popular_week():
    read_today = Read.objects.filter(book_read_latest_time__gte=timezone.now() - timedelta(weeks=1))
    book_today = read_today.values_list('book_refer_id',flat=True).distinct()
    popular_today = sorted([(i ,read_today.filter(book_refer=i).count()) for i in book_today], key= lambda x: x[1])
    return popular_today
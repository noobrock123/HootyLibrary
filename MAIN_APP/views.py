from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import path, include, reverse
from database_models.models import Book, Read
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import include, path, reverse

from database_models.models import *
from database_models.models import Book
from django.utils import timezone
from datetime import datetime, timedelta

def index(request):
    books = Book.objects.all()
    latest_book = books.order_by('-date_created').values()[:8]
    topics = {
        'Latest Books':latest_book,
    }
    read = Read.objects.filter(user_refer=request.user)
    recently_read = read.order_by('-book_read_latest_time')[:8]
    if request.method == "GET":
        search_query = request.GET.get('query')
        if search_query:
            topics = search(search_query)
            return render(request, 'homepage/homepage.html', {'topics':topics})
        Education_query = request.GET.get('Education')
        Entertain_query = request.GET.get('Entertain')
        oldTolate_query = request.GET.get('oldTolate')
        zToa_query = request.GET.get('zToa')
        if Education_query or Entertain_query or oldTolate_query or zToa_query:
            topics = filter(Education_query, Entertain_query, oldTolate_query, zToa_query)
            return render(request, 'homepage/homepage.html', {'topics':topics})
        return render(request, 'homepage/homepage.html',
            {'is_user_authenticated': request.user.is_authenticated,
            'user': request.user, #'books': latest_book,
            'recent_read': recently_read,
            'topics': topics,},)

def search(search_query):
    books = Book.objects.all()
    latest_book = books.order_by('-date_created').values()[:8]
    topics = {
        'Latest Books':latest_book,
    }
    if search_query:
        SearchCheck = Book.objects.filter(book_name__contains=search_query)
        if SearchCheck:
            book = Book.objects.all().filter(book_name__startswith=search_query)
            topics = {
                'search':book,
            }
            return topics

def filter(Education_query, Entertain_query, oldTolate_query, zToa_query):
    topics = { }
    book = Book.objects.all()
    if Education_query == 1:
        book = book.filter(book_type=1)
        topics.update({'Education_query':book,})
    if Entertain_query == 2:
        book = book.filter(book_type=2)
        topics.update({'Entertain_query':book,})
    if oldTolate_query:
        oldTolateBook = book.order_by('date_created').values()
        topics.update({'Oldest to Latest':oldTolateBook,})
    if  zToa_query:
        book = book.order_by('-book_name').values()
        topics.update({'Z to A':book,})
    return topics
    
    

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

def Undiscovered(request):
    books = Book.objects.all()
    Undiscovered = books.order_by('-date_created').values()[:8]
    topics = {
        'Undiscovered':Undiscovered,
    }
    if request.method == "GET":  
        search_query = request.GET.get('query')
        if search_query:
            topics = search(search_query)
            return render(request, 'homepage/homepage.html', {'topics':topics})
        Education_query = request.GET.get('Education')
        Entertain_query = request.GET.get('Entertain')
        oldTolate_query = request.GET.get('oldTolate')
        zToa_query = request.GET.get('zToa')
        if Education_query or Entertain_query or oldTolate_query or zToa_query:
            topics = filter(Education_query, Entertain_query, oldTolate_query, zToa_query)
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
            topics = search(search_query)
            return render(request, 'homepage/homepage.html', {'topics':topics})
        Education_query = request.GET.get('Education')
        Entertain_query = request.GET.get('Entertain')
        oldTolate_query = request.GET.get('oldTolate')
        zToa_query = request.GET.get('zToa')
        if Education_query or Entertain_query or oldTolate_query or zToa_query:
            topics = filter(Education_query, Entertain_query, oldTolate_query, zToa_query)
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
            topics = search(search_query)
            return render(request, 'homepage/homepage.html', {'topics':topics})
        Education_query = request.GET.get('Education')
        Entertain_query = request.GET.get('Entertain')
        oldTolate_query = request.GET.get('oldTolate')
        zToa_query = request.GET.get('zToa')
        if Education_query or Entertain_query or oldTolate_query or zToa_query:
            topics = filter(Education_query, Entertain_query, oldTolate_query, zToa_query)
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
            topics = search(search_query)
            return render(request, 'homepage/homepage.html', {'topics':topics})
        Education_query = request.GET.get('Education')
        Entertain_query = request.GET.get('Entertain')
        oldTolate_query = request.GET.get('oldTolate')
        zToa_query = request.GET.get('zToa')
        if Education_query or Entertain_query or oldTolate_query or zToa_query:
            topics = filter(Education_query, Entertain_query, oldTolate_query, zToa_query)
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
            topics = search(search_query)
            return render(request, 'homepage/homepage.html', {'topics':topics})
        Education_query = request.GET.get('Education')
        Entertain_query = request.GET.get('Entertain')
        oldTolate_query = request.GET.get('oldTolate')
        zToa_query = request.GET.get('zToa')
        if Education_query or Entertain_query or oldTolate_query or zToa_query:
            topics = filter(Education_query, Entertain_query, oldTolate_query, zToa_query)
            return render(request, 'homepage/homepage.html', {'topics':topics})
    return render(request, 'homepage/homepage.html', {'topics':topics})

def Recently(request):
    books = Book.objects.all()
    Recently = books.order_by('-date_created').values()[:8]
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

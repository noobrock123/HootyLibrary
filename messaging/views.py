from django.http import HttpResponse
from django.shortcuts import redirect, render
from database_models.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.http import HttpResponseNotFound
from django.views import defaults
# Create your views here.

def reviews(request, book_id):
    book = Book.objects.get(book_id=book_id)
    if request.method == 'POST':
        book = Book.objects.get(book_id=book_id)
        user = request.user
        title = request.POST.get('title')
        msg = request.POST.get('msg')
        try:
            Issue.objects.create(issuer=user, book_refer=book, title=title, msg=msg)
        except:
            return HttpResponse('Not Found')
        return redirect('userProfile:user_profile', user_id=user.user_id)

    return render(request, 'messaging/prototype.html', {'book': book})

@login_required(login_url='register:log_in')
def create_review(request, book_id):
    book = Book.objects.get(book_id=book_id)
    if request.method == 'POST':
        book = Book.objects.get(book_id=book_id)
        user = request.user
        title = request.POST.get('title')
        score = float(request.POST.get('score'))
        msg = request.POST.get('msg')
        try:
            Issue.objects.create(issuer=user, book_refer=book, title=title, msg=msg)
        except:
            return HttpResponse('Not Found')
        return redirect('userProfile:user_profile', user_id=user.user_id)

    return render(request, 'review/review.html', {'book': book})


def show_issues(request, book_id):
    book = Book.objects.get(book_id=book_id)
    if request.method == 'POST':
        book = Book.objects.get(book_id=book_id)
        user = request.user
        title = request.POST.get('title')
        msg = request.POST.get('msg')
        msg = "test"
        try:
            Issue.objects.create(issuer=user, book_refer=book, title=title, msg=msg)
        except:
            return HttpResponse('Not Found')
        return redirect('book_views:book', book_id=book.book_id)

    return render(request, 'messaging/prototype.html', {'book': book})

@login_required(login_url='register:log_in')
def create_issue(request, book_id):
    book = Book.objects.get(book_id=book_id)
    if request.method == 'POST':
        book = Book.objects.get(book_id=book_id)
        user = request.user
        title = request.POST.get('title')
        msg = request.POST.get('msg')
        Issue.objects.create(issuer=user, book_refer=book, title=title, msg=msg)
        return redirect('book_views:book', book_id=book.book_id)

    return render(request, 'issue/issue.html', {'book': book})

@login_required(login_url='register:log_in')
def create_report(request, book_id):
    book = Book.objects.get(book_id=book_id)
    if request.method == 'POST':
        book = Book.objects.get(book_id=book_id)
        user = request.user
        title = request.POST.get('title')
        msg = request.POST.get('msg')
        try:
            Issue.objects.create(issuer=user, book_refer=book, title=title, msg=msg)
        except:
            return HttpResponse('Not Found')
        return redirect('userProfile:user_profile', user_id=user.user_id)

    return render(request, 'report/report.html', {'book': book})
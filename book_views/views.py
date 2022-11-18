from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import FileResponse
from PIL import Image
from database_models.models import *
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views import defaults
# Create your views here.


def book_thumbnail(request, book_id):
    try:
        with open(f'{Book.objects.get(book_id=book_id).thumbnail.path}', 'rb') as thumbnail:
            return HttpResponse(thumbnail.read(), content_type="image/jpeg")
    except:
        with open(f'book_views/static/bookpage/images/not found book.jpg', 'rb') as thumbnail:
            return HttpResponse(thumbnail.read(), content_type="image/jpeg")


@xframe_options_exempt
def book_pdf(request, book_id):
    try:
        with open(f'{Book.objects.get(book_id=book_id).pdf_files.path}', 'rb') as pdf:
            return HttpResponse(pdf.read(), content_type="application/pdf")
    except Exception as e:
        return defaults.page_not_found(request, e)


def book_views(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
    except Exception as e:
        return defaults.page_not_found(request, e)
    if request.user.is_authenticated:
        user = User.objects.get(user_id=request.user.user_id)
        if book.author != user:
            read = Read.objects.get_or_create(user_refer=user, book_refer=book)
            read[0].save()

    context = {
        'book': book,
    }
    return render(request, 'book_views/templates/book_views/index.html', context)


@login_required(login_url='register:log_in')
def create_book(request):
    context = {
        'genres': Genre.objects.all(),
    }
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        description = request.POST.get('description')
        book_type = request.POST.get('book_type')
        genres = request.POST.getlist('genres')
        thumbnail = request.FILES.get('thumbnail')
        pdf_files = request.FILES.get('pdf_files')
        author = User.username
        create = True
        if not book_name:
            create = False
            messages.error(request, 'book_name is required ! ! ! ')
        if not book_type:
            create = False
            messages.error(request, 'book_type is required ! ! ! ')
        if not create:
            return render(request, 'book_views/templates/book_views/create_book.html', context)
        book = Book.objects.create(
            book_name=book_name,
            description=description,
            book_type=book_type,
            author=request.user,
            thumbnail=thumbnail,
            pdf_files=pdf_files,
            genres=genres,
        )
        return redirect('book_views:book', book.book_id)

    return render(request, 'book_views/templates/book_views/create_book.html', context)

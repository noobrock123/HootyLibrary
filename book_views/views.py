from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
from PIL import Image
from database_models.models import *
from django.views.decorators.clickjacking import xframe_options_exempt
# Create your views here.


def book_thumnail(request, book_id):
    try:
        with open(f'{Book.objects.get(book_id=book_id).thumbnail.path}', 'rb') as thumnail:
            return HttpResponse(thumnail.read(), content_type="image/jpeg")
    except:
        return HttpResponse('Not found')


@xframe_options_exempt
def book_pdf(request, book_id):
    try:
        with open(f'{Book.objects.get(book_id=book_id).pdf_files.path}', 'rb') as pdf:
            return HttpResponse(pdf.read(), content_type="application/pdf")
    except:
        return HttpResponse('Not found')


def book_views(request, book_id):
    book = Book.objects.get(book_id=book_id)
    
    context = {
        # 'book_id':book.(),
        'book_name': book.get_book_name(),
        'description': book.get_description(),
        'date_created': book.get_date_created,
        'book_type': book.get_book_type(),
        'genres': book.get_genres(),
        'author': book.get_author(),
        'reviews': book.get_reviews(),
        'favorite_books': Favorite.objects.filter(book_refer=book),
        'avg_score': book.get_avg_score(),
        'book': book,

    }
    return render(request, 'book_views/templates/book_views/index.html', context)

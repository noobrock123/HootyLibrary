from django.urls import include, path
from . import views
urlpatterns = [
    path('book/pdf/<str:book_id>', views.book_pdf, name='book_pdf'),
    path('book/thumbnail/<str:book_id>/',views.book_thumbnail, name='book_thumbnail'),
    path('book/<str:book_id>', views.book_views, name='book')
]
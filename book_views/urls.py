from django.urls import include, path
from . import views
urlpatterns = [
    path('book/pdf/<str:book_id>', views.book_pdf, name='book_pdf'),
    path('book/thumnail/<str:book_id>/',views.book_thumnail, name='book_thumnail'),
    path('book/<str:book_id>', views.book_views, name='book')
]
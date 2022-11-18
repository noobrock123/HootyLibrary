from django.urls import include, path
from . import views

app_name = "book_views"
urlpatterns = [
    path('book/create_book/', views.create_book, name='create_book'),
    path('book/<str:book_id>/pdf/', views.book_pdf, name='book_pdf'),
    path('book/<str:book_id>/thumbnail/',views.book_thumbnail, name='book_thumbnail'),
    path('book/<str:book_id>/', views.book_views, name='book'),
    
]